# -*- coding: utf8 -*-


import game

import random
import msgpack
import time
import script.chat.chatting_def as chat_def
import script.common.config.topoconfig as ModTopo
import script.common.exception_def as excp
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.protocol_def as proto_def
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase
from script.common.online_user_manager import OnlineUserManager
from script.common.protocol_def import CGGetChatOfflineMsgRequest, CGSendChatMsgRequest, CGSynChatMsgToClient, CGGameServerNotice


class CChat(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.online_manager = OnlineUserManager()
        self.temp_public_msg_dict = {}

    # child class must override functions >>>
    def get_node_type(self):
        return ModTopo.NODE_TYPE.CHAT

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # chat的服务器节点: monitor、chat proxy、db
        logger.GetLog().debug('send_msg_to_server_node : %s, %s' % (client_type, args))
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type in self.connect_server_dict and self.connect_server_dict[server_node_type]:
            if server_node_type == ModTopo.NODE_TYPE.MONITOR:
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.CHAT_PROXY:
                if client_type == server_node_type:
                    # 需要查找一个实际的node
                    client_type = self.connect_server_dict[server_node_type].keys()[0]     # 因为proxy只有1个, 所以直接取
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.CHAT, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.DB_PROXY:
                if client_type == server_node_type:
                    # 随机一个db节点处理即可
                    client_type = random.choice(self.connect_server_dict[server_node_type].keys())
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.CHAT, msg_str)
            else:
                logger.GetLog().error('send msg to an unsupported server node : %s, %s, %s' % (client_type, msg_str, args))
        else:
            logger.GetLog().error('send msg to server node %s but there is no one in connect_server_dict' % server_node_type)

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # chat 节点没有客户端
        logger.GetLog().warn('chat has no client node, please check the code: %s, %s, %s' % (client_node_type, msg_str, args))

    # child class must override functions <<<

    # C++ API >>>
    def OnStartUp(self, conf_file):
        CAppBase.OnStartUp(self, conf_file)
        # 启动回写定时器
        self.RegTick(self._write_back_timer, None, 5000)

    # C++ API <<<

    # public functions >>>
    def get_chat_2_chat_proxy_rpc(self, client_type=None):
        if client_type:
            return self.get_client_rpc_handler(client_type)
        # 没有传参数,则传入node type, 在send_msg_to_server_node处再做判断
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.CHAT_PROXY)

    def get_chat_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_chat_2_db_rpc(self):
        return self.get_send_query_rpc_handler(ModTopo.NODE_TYPE.DB_PROXY)

    # public functions <<<

    # private functions >>>
    def _write_back_timer(self, _arg):
        msg_dict = self.temp_public_msg_dict
        self.temp_public_msg_dict = {}
        if msg_dict:
            self.get_chat_2_db_rpc().AddPublicChatMsgBatch(msg_dict)

    def _handle_update_user_online_status(self, server_group_id, server_user_id, is_online):
        logger.GetLog().debug('chat handle update user online status: %s, %s, %s' % (server_group_id, server_user_id, is_online))
        if is_online:
            self.online_manager.user_online(server_group_id, server_user_id)
        else:
            self.online_manager.user_offline(server_group_id, server_user_id)

    def _handle_chat_msg(self, server_group_id, server_sender_id, msg):
        logger.GetLog().debug('handle chat msg : %s, %s, %s' % (server_group_id, server_sender_id, msg))
        msg_obj = CGSendChatMsgRequest.new_from_data(msg)
        # 更新服务器id
        msg_time = time.time()
        chat_msg_data = self._pack_push_chat_msg_data(msg_obj, msg_time, server_sender_id)
        return_code = None
        if msg_obj.channel_type in [chat_def.CHAT_CHANNEL_TYPE_PUBLIC, chat_def.CHAT_CHANNEL_TYPE_NOTICE]:
            # 公共聊天或系统推送
            return_code = self._process_public_chat(chat_msg_data, msg_time, server_group_id, server_sender_id)
        elif msg_obj.channel_type == chat_def.CHAT_CHANNEL_TYPE_CLAN:
            # 公会聊天
            self._process_clan_chat(chat_msg_data, msg_time, server_group_id, server_sender_id)
        elif msg_obj.channel_type == chat_def.CHAT_CHANNEL_TYPE_P2P:
            # 私聊
            return_code = self._process_p2p_chat(chat_msg_data, msg_time, server_group_id, server_sender_id, msg_obj.server_receiver_id)
        elif msg_obj.channel_type == chat_def.CHAT_CHANNEL_TYPE_TEAM:
            # 队伍内部聊天
            self._process_team_chat(chat_msg_data, msg_time, server_group_id, server_sender_id)
        else:
            logger.GetLog().warn('chat server handle unexcept channel type msg : %s' % msg)
            return_code = excp.ExceptionChatBase.code

        # 发送消息成功返回给发送者
        if server_sender_id and return_code is not None:  # return_code为None,表示异步处理
            self.get_chat_2_chat_proxy_rpc().OnHandleSendChatMsgResponse(server_sender_id, return_code)

    def _handle_game_notice(self, msg):
        logger.GetLog().debug('handle game notice : %s' % msg)
        msg_obj = CGGameServerNotice.new_from_data(msg)
        msg_time = time.time()
        notice_msg_data = self._pack_push_game_notice_data(msg_obj, msg_time)
        if msg_obj.channel_type in [chat_def.CHAT_CHANNEL_TYPE_PUBLIC, chat_def.CHAT_CHANNEL_TYPE_NOTICE]:
            # 公共推送
            self._process_public_notice(notice_msg_data, msg_time, msg_obj.server_group_id)
        elif msg_obj.channel_type == chat_def.CHAT_CHANNEL_TYPE_CLAN:
            # 公会推送
            self._process_clan_notice(notice_msg_data, msg_time, msg_obj.server_receiver_id, msg_obj.server_group_id)

    def _process_public_notice(self, push_chat_msg, msg_time, server_group_id):
        self._process_public_chat(push_chat_msg, msg_time, server_group_id)

    def _process_clan_notice(self, notice_msg_data, msg_time, clan_id, server_group_id):
        if clan_id:
            self.get_chat_2_db_rpc().LoadClanDataToSendNotice(notice_msg_data, msg_time, clan_id, server_group_id)
        return False

    def _process_public_chat(self, chat_msg_data, msg_time, server_group_id, server_sender_id=None):
        except_id_list = None
        if server_sender_id:
            except_id_list = [server_sender_id]
            # 公共消息,存储到db
            # self.get_chat_2_db_rpc().AddPublicChatMsg(chat_msg_data, msg_time, server_sender_id, server_group_id)
            if server_group_id not in self.temp_public_msg_dict:
                self.temp_public_msg_dict[server_group_id] = []
            self.temp_public_msg_dict[server_group_id].append((chat_msg_data, msg_time, server_sender_id))
            if len(self.temp_public_msg_dict[server_group_id]) >= 100:
                self.temp_public_msg_dict[server_group_id] = self.temp_public_msg_dict[server_group_id][-100:]
        # 消息广播给其他玩家
        self.get_chat_2_chat_proxy_rpc().OnMsgFromChat(server_group_id, chat_msg_data, None, except_id_list)
        return excp.ExceptionSuccess.code

    def _process_clan_chat(self, chat_msg_data, msg_time, server_group_id, server_sender_id):
        # 取出sender_id对应的所有帮派成员id，过滤掉自己
        self.get_chat_2_db_rpc().LoadClanDataToSendMsg(chat_msg_data, msg_time, server_group_id, server_sender_id)

    def _process_p2p_chat(self, chat_msg_data, msg_time, server_group_id, server_sender_id, server_receiver_id):
        if server_receiver_id:
            if self.online_manager.is_user_online(server_group_id, server_receiver_id):
                self.get_chat_2_chat_proxy_rpc().OnMsgFromChat(server_group_id, chat_msg_data, [server_receiver_id], None)
                return excp.ExceptionSuccess.code
            else:  # 接收者不在线,将消息加入到消息列表
                if server_sender_id:  # 是否要过滤
                    self.get_chat_2_db_rpc().AddP2PChatMsg(chat_msg_data, msg_time, server_sender_id, server_receiver_id)
                    # 异步处理,返回None
                    return
                return excp.ExceptionSuccess.code
        else:
            logger.GetLog().debug('receiver id is none : %s' % server_receiver_id)
            return excp.ExceptionUserNotFound.code

    def _process_team_chat(self, chat_msg_data, msg_time, server_group_id, server_sender_id):
        self.get_chat_2_db_rpc().HandleSendTeamMsg(chat_msg_data, msg_time, server_group_id, server_sender_id)

    def _handle_get_offline_msg(self, server_group_id, server_user_id, msg):
        logger.GetLog().debug('get offline msg : %s, %s, %s' % (server_group_id, server_user_id, msg))
        msg_obj = CGGetChatOfflineMsgRequest.new_from_data(msg)
        self.get_chat_2_db_rpc().LoadOfflineMsgToSend(server_group_id, server_user_id, msg_obj.last_public_time, msg_obj.last_clan_time)

    def _handle_confirm_offline_msg(self, server_user_id, msg):
        logger.GetLog().debug('confirm get offline msg : %s' % server_user_id)
        self.get_chat_2_db_rpc().ConfirmGetOfflineMsg(server_user_id)

    def _handle_update_server_online_db_data(self, server_group_id, online_num):
        logger.GetLog().debug('handle update server online db data : %s, %s' % (server_group_id, online_num))
        self.get_chat_2_db_rpc().UpdateServerOnlineDBData(server_group_id, online_num)

    def _handle_write_user_offline_log(self, server_user_id, logout_time, online_time):
        logger.GetLog().debug('handle write user offline log : %s, %s, %s' % (server_user_id, logout_time, online_time))
        self.get_chat_2_db_rpc().WriteUserOfflineLog(server_user_id, logout_time, online_time)

    def _handle_write_online_num_log(self, user_num_dict):
        logger.GetLog().debug('handle write online num log : %s' % user_num_dict)
        self.get_chat_2_db_rpc().WriteOnlineNumLog(user_num_dict)

    def _pack_push_chat_msg_data(self, msg_obj, msg_time, server_sender_id=None):
        syn_msg_data = CGSynChatMsgToClient()
        syn_msg_data.channel_type = msg_obj.channel_type
        syn_msg_data.server_sender_id = server_sender_id
        syn_msg_data.msg_time = msg_time
        syn_msg_data.data = msg_obj.data
        return syn_msg_data.dump()

    def _pack_push_game_notice_data(self, msg_obj, msg_time):
        syn_msg_data = CGSynChatMsgToClient()
        syn_msg_data.channel_type = msg_obj.channel_type
        syn_msg_data.msg_time = msg_time
        syn_msg_data.data = msg_obj.data
        return syn_msg_data.dump()

    # private functions <<<

    # rpc 相关 >>>
    # proxy to chat >>>
    def OnChatMsg(self, server_group_id, server_user_id, str_msg):
        msg = msgpack.unpackb(str_msg)
        logger.GetLog().debug('chat server receive msg: %s, %s, %s' % (server_group_id, server_user_id, len("%s"%msg)))
        cmd = msg.get(proto_def.field_name_cmd, None)
        if cmd is None:
            logger.GetLog().warn('format of this chat msg is unexpected : %s' % msg)
        else:
            if cmd == proto_def.cg_send_chat:  # 发送聊天消息
                self._handle_chat_msg(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_get_offline_msg:  # 获取离线数据
                self._handle_get_offline_msg(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_offline_msg_confirm:  # 离线消息确认
                self._handle_confirm_offline_msg(server_user_id, msg)
            else:
                logger.GetLog().warn('chat server receive unexpected cmd msg : %s' % msg)

    def OnGameNotice(self, str_msg):
        msg = msgpack.unpackb(str_msg)
        cmd = msg.get(proto_def.field_name_cmd, None)
        if cmd is None:
            logger.GetLog().warn('format of this game notice msg is unexpected : %s' % msg)
        else:
            if cmd == proto_def.cg_game_server_notice:
                self._handle_game_notice(msg)
            else:
                logger.GetLog().warn('chat server receive unexpected cmd msg : %s' % msg)

    def OnUserOnlineStatusUpdate(self, server_group_id, server_user_id, is_online):
        """
        更新玩家在线状态
        """
        self._handle_update_user_online_status(server_group_id, server_user_id, is_online)

    def OnUpdateServerOnlineDBData(self, server_group_id, online_num):
        self._handle_update_server_online_db_data(server_group_id, online_num)

    def OnWriteUserOfflineLog(self, server_user_id, logout_time, online_time):
        self._handle_write_user_offline_log(server_user_id, logout_time, online_time)

    def OnWriteOnlineNumLog(self, user_num_dict):
        self._handle_write_online_num_log(user_num_dict)

    # proxy to chat <<<

    # db to chat >>>
    def OnAddP2PChatMsg(self, (return_code, server_sender_id)):
        logger.GetLog().debug('on add p2p chat msg to db : %s, %s' % (return_code, server_sender_id))
        # 返回信息给客户端
        if server_sender_id:
            self.get_chat_2_chat_proxy_rpc().OnHandleSendChatMsgResponse(server_sender_id, return_code)

    def OnLoadClanDataToSendMsg(self, result):
        return_code = result[0]
        if return_code == excp.ExceptionSuccess.code:
            # 成功,继续逻辑
            _, chat_msg_data, server_group_id, server_sender_id, member_id_list = result
            if not member_id_list:
                return
            member_id_list.remove(server_sender_id)
            # 推送公会信息
            if member_id_list:
                self.get_chat_2_chat_proxy_rpc().OnMsgFromChat(server_group_id, chat_msg_data, member_id_list, None)
        else:
            # 失败,返回
            server_sender_id = result[1]
        # 给信息发送者返回结果
        if server_sender_id:
            self.get_chat_2_chat_proxy_rpc().OnHandleSendChatMsgResponse(server_sender_id, return_code)

    def OnHandleSendTeamMsg(self, result):
        if result[0] == excp.ExceptionSuccess.code:
            _, server_group_id, server_sender_id, chat_msg_data, member_id_list = result
            if not member_id_list:
                return
            member_id_list.remove(server_sender_id)
            if member_id_list:
                self.get_chat_2_chat_proxy_rpc().OnMsgFromChat(server_group_id, chat_msg_data, member_id_list, None)
        else:
            server_sender_id = result[2]
        if server_sender_id:
            self.get_chat_2_chat_proxy_rpc().OnHandleSendChatMsgResponse(server_sender_id, result[0])

    def OnConfirmGetOfflineMsg(self, result):
        logger.GetLog().debug('on confirm offline msg result : %s' % result)

    def OnLoadOfflineMsgToSend(self, result):
        server_user_id, public_msg_list, clan_msg_list, p2p_msg_list = result
        self.get_chat_2_chat_proxy_rpc().OnOfflineMsgResponse(server_user_id, public_msg_list, clan_msg_list, p2p_msg_list)

    def OnLoadClanDataToSendNotice(self, result):
        notice_msg_data, server_group_id, member_id_list = result
        # 推送公会信息
        if member_id_list:
            self.get_chat_2_chat_proxy_rpc().OnMsgFromChat(server_group_id, notice_msg_data, member_id_list, None)
    # db to chat <<<

    # monitor to chat >>>
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('chat on gm msg, gm_cmd : %s, params : %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_chat_2_monitor_rpc().OnGMMsgResponse('chat executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:   # 所有文件重load成功
                self.get_chat_2_monitor_rpc().OnGMMsgResponse('chat executed gm command %s success' % gm_cmd)
        else:
            # 参数不对或者不支持的
            return_msg = 'chat unsupported gm command or param unexpected : %s' % gm_cmd
            logger.GetLog().warn(return_msg)
            self.get_chat_2_monitor_rpc().OnGMMsgResponse(return_msg)
    # monitor to chat <<<

    # rpc 相关 <<<
