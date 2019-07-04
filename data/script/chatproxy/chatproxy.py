# -*- coding: utf8 -*-


import game

import random
import time
import script.common.config.topoconfig as ModTopo
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase


class CChatProxy(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.server_user_dict = {}      # server group id -> {server_user_id: connect_id},方便统计在线人数
        self.user_login_time_dict = {}  # server_user_id -> login time
        self.chat_msg_count = 0
        self.notice_msg_count = 0

    # ========== child class must override functions ==========
    def get_node_type(self):
        return ModTopo.NODE_TYPE.CHAT_PROXY

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # chat proxy的服务器节点: monitor、gateway
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type == ModTopo.NODE_TYPE.MONITOR:
            game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
        elif server_node_type == ModTopo.NODE_TYPE.GATEWAY:
            if server_node_type in self.connect_server_dict:
                if client_type == server_node_type:
                    # 广播给所有的gateway
                    for real_client_type in self.connect_server_dict[server_node_type].keys():
                        game.SendMsgToServer(real_client_type, ModTopo.PROTO_TYPE.CHAT, msg_str)
                else:
                    game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.CHAT, msg_str)
            else:
                logger.GetLog().warn('no gateway connect')
        else:
            logger.GetLog().error('send msg to an unexpected server node : %s, %s, %s' % (client_type, msg_str, args))

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # chat proxy的客户端节点: chat (可能还有其他逻辑节点, 可以支持)
        if client_node_type == ModTopo.NODE_TYPE.CHAT:
            if args:
                self._send_msg_to_chat(msg_str, args[0])
            else:
                self._send_msg_to_chat(msg_str)
        else:
            logger.GetLog().error('send msg to an unexpected client node : %s, %s, %s' % (client_node_type, msg_str, args))

    # ========== C++ API ==========
    def OnStartUp(self, conf_file):
        CAppBase.OnStartUp(self, conf_file)
        # 启动在线人数日志定时器并注册事件
        self.RegTick(self._timer_online_num_log, None, 300000)

    # ========== public functions ==========
    def get_chat_proxy_2_chat_rpc(self, chat_node_id=None):
        if chat_node_id:
            return self.get_server_rpc_handler(ModTopo.NODE_TYPE.CHAT, chat_node_id)
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.CHAT)

    def get_chat_proxy_2_gateway_rpc(self, client_type=None):
        if client_type:
            return self.get_client_rpc_handler(client_type)
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.GATEWAY)

    def get_chat_proxy_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_chat_node_id_list(self):
        if ModTopo.NODE_TYPE.CHAT in self.connect_client_dict:
            return self.connect_client_dict[ModTopo.NODE_TYPE.CHAT].keys()
        logger.GetLog().info('no chat node connected')
        return []

    # ========== private functions ==========
    def _send_msg_to_chat(self, msg_str, chat_node_id=None):
        if ModTopo.NODE_TYPE.CHAT in self.connect_client_dict:
            if chat_node_id:
                if chat_node_id in self.connect_client_dict[ModTopo.NODE_TYPE.CHAT]:
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, self.connect_client_dict[ModTopo.NODE_TYPE.CHAT][chat_node_id], ModTopo.PROTO_TYPE.CHAT, msg_str)
                else:
                    logger.GetLog().warn('chat node %s not connected' % chat_node_id)
            else:
                for chat_node_conn_id in self.connect_client_dict[ModTopo.NODE_TYPE.CHAT].values():
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, chat_node_conn_id, ModTopo.PROTO_TYPE.CHAT, msg_str)
        else:
            logger.GetLog().warn('no chat node in connect_client_dict')

    def _timer_online_num_log(self, _args=None):
        logger.GetLog().info('online num log timer : %s' % time.time())
        chat_node_dict = self.connect_client_dict.get(ModTopo.NODE_TYPE.CHAT, None)
        if chat_node_dict:
            # 随机一个聊天服处理在线玩家日志
            chat_node_id = random.choice(chat_node_dict.keys())
            user_num_dict = {}
            for server_group_id, data in self.server_user_dict.iteritems():
                user_num_dict[server_group_id] = len(data)
            if user_num_dict:
                self.get_chat_proxy_2_chat_rpc(chat_node_id).OnWriteOnlineNumLog(user_num_dict)

    def _handle_user_online(self, server_group_id, server_user_id, connect_id, ip):
        logger.GetLog().debug('chat proxy handle user online : %s, %s, %s, %s' % (server_group_id, server_user_id, connect_id, ip))
        is_exist = (server_group_id in self.server_user_dict and server_user_id in self.server_user_dict[server_group_id])
        if server_group_id not in self.server_user_dict:
            self.server_user_dict[server_group_id] = {}
        self.server_user_dict[server_group_id][server_user_id] = connect_id
        logger.GetLog().debug('chat proxy handle online : %s, %s, %s' % (server_group_id, server_user_id, is_exist))

        # 处理玩家登录时间
        if server_user_id not in self.user_login_time_dict:
            self.user_login_time_dict[server_user_id] = int(time.time())

        if not is_exist:
            # 更新gateway在线人数
            server_online_num = len(self.server_user_dict[server_group_id])
            self.get_chat_proxy_2_gateway_rpc().OnSynServerOnlineNum(server_group_id, server_online_num)
            # 更新db在线人数数据(LogServerOnlineDo)
            self._update_server_online_db_data(server_group_id, server_online_num)

    def _handle_user_offline(self, server_group_id, server_user_id, connect_id):
        logger.GetLog().debug('chat proxy handle user offline: %s, %s, %s' % (server_group_id, server_user_id, connect_id))
        if server_user_id and server_group_id and connect_id:
            if server_group_id in self.server_user_dict and server_user_id in self.server_user_dict[server_group_id] and \
               connect_id == self.server_user_dict[server_group_id][server_user_id]:
                self.server_user_dict[server_group_id].pop(server_user_id, None)
                # 更新gateway在线人数
                server_online_num = len(self.server_user_dict[server_group_id])
                self.get_chat_proxy_2_gateway_rpc().OnSynServerOnlineNum(server_group_id, server_online_num)
                # 更新db在线人数数据(LogServerOnlineDo, CharacterLogInfoDo)
                logout_time = int(time.time())
                login_time = self.user_login_time_dict.get(server_user_id, logout_time)
                online_time = max(0, logout_time - login_time)
                self._update_server_online_db_data(server_group_id, server_online_num)
                self._write_user_offline_log(server_user_id, logout_time, online_time)

        # 处理登录时间
        self.user_login_time_dict.pop(server_user_id, None)

    def _update_server_online_db_data(self, server_group_id, online_num):
        chat_node_id_list = self.get_chat_node_id_list()
        if chat_node_id_list:
            # 随机一个聊天服处理db在线人数数据
            chat_node_id = random.choice(chat_node_id_list)
            self.get_chat_proxy_2_chat_rpc(chat_node_id).OnUpdateServerOnlineDBData(server_group_id, online_num)

    def _write_user_offline_log(self, server_user_id, logout_time, online_time):
        chat_node_id_list = self.get_chat_node_id_list()
        if chat_node_id_list:
            # 随机一个聊天服处理玩家log信息
            chat_node_id = random.choice(chat_node_id_list)
            self.get_chat_proxy_2_chat_rpc(chat_node_id).OnWriteUserOfflineLog(server_user_id, logout_time, online_time)

    # ========== rpc 相关 ==========
    # chat to proxy >>>
    def OnMsgFromChat(self, server_group_id, chat_msg_data, receiver_id_list, except_id_list):
        """
        收到聊天服消息，转发下去
        """
        self.get_chat_proxy_2_gateway_rpc().OnMsgFromChat(server_group_id, chat_msg_data, receiver_id_list, except_id_list)

    def OnHandleSendChatMsgResponse(self, server_sender_id, return_code):
        """
        处理发送聊天消息返回，转发下去
        """
        self.get_chat_proxy_2_gateway_rpc().OnHandleSendChatMsgResponse(server_sender_id, return_code)

    def OnOfflineMsgResponse(self, server_user_id, public_msg_list, clan_msg_list, p2p_msg_list):
        """
        离线消息返回,转发下去
        """
        self.get_chat_proxy_2_gateway_rpc().OnOfflineMsgResponse(server_user_id, public_msg_list, clan_msg_list, p2p_msg_list)
    # chat to proxy <<<

    # gateway to proxy >>>
    def OnChatMsg(self, server_group_id, server_user_id, str_msg):
        """
         收到网关转发过来的聊天消息
        """
        # 先随机一个chat node id
        chat_node_id_list = self.get_chat_node_id_list()
        chat_node_id = chat_node_id_list[self.chat_msg_count % len(chat_node_id_list)]
        self.get_chat_proxy_2_chat_rpc(chat_node_id).OnChatMsg(server_group_id, server_user_id, str_msg)
        self.chat_msg_count += 1

    def OnGameNotice(self, str_msg):
        """
         收到网关转发过来的游戏推送消息
        """
        # 先随机一个chat node id
        chat_node_id_list = self.get_chat_node_id_list()
        chat_node_id = chat_node_id_list[self.notice_msg_count % len(chat_node_id_list)]
        self.get_chat_proxy_2_chat_rpc(chat_node_id).OnGameNotice(str_msg)
        self.notice_msg_count += 1

    def OnUserOnlineStatusUpdate(self, server_group_id, server_user_id, connect_id, is_online, ip=None):
        """
        玩家在线状态改变
        """
        # 更新proxy记录的玩家在线信息
        if is_online:
            self._handle_user_online(server_group_id, server_user_id, connect_id, ip)
        else:
            self._handle_user_offline(server_group_id, server_user_id, connect_id)
        # 同步玩家在线状态到所有chat server
        chat_node_id_list = self.get_chat_node_id_list()
        for chat_node_id in chat_node_id_list:
            self.get_chat_proxy_2_chat_rpc(chat_node_id).OnUserOnlineStatusUpdate(server_group_id, server_user_id, is_online)

    def print_msg_count(self):
        logger.GetLog().info('====== count : chat = %s, notice = %s ========' % (self.chat_msg_count, self.notice_msg_count))
    # gateway to proxy <<<

    # monitor to proxy >>>
    # ====================================================================================
    # ================================ gm command handler ================================
    # ====================================================================================
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('chat proxy on gm msg, gm_cmd : %s, params : %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_chat_proxy_2_monitor_rpc().OnGMMsgResponse('chat proxy executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:   # 所有文件重load成功
                self.get_chat_proxy_2_monitor_rpc().OnGMMsgResponse('chat proxy executed gm command %s success' % gm_cmd)
        else:
            # 参数不对或者不支持的
            return_msg = 'chat proxy unsupported gm command or param unexpected : %s' % gm_cmd
            logger.GetLog().warn(return_msg)
            self.get_chat_proxy_2_monitor_rpc().OnGMMsgResponse(return_msg)
    # monitor to proxy <<<
