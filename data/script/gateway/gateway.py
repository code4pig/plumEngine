# -*- coding: utf8 -*-

import msgpack

import game

import script.common.config.topoconfig as ModTopo
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase
from script.common.protocol_def import CGSendChatMsgResponse, CGGetChatOfflineMsgResponse
from script.gateway.client_connect import ClientConnect
from script.gateway.gateway_msg_manager import GatewayMsgManager
from script.gateway.gw4climsghandler import CGw4CliMsgHandler


class CGateWay(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.user_connect_dict = {}  # 保存玩家角色id到连接id的映射 server user id -> connect id
        self.connect_info_dict = {}  # 连接信息字典 connect id -> ClientConnect obj
        self.group_connect_dict = {}  # 按服区分的连接映射 server group id -> connect id dict
        self.client_msg_handler = CGw4CliMsgHandler()       # 接收处理客户端消息
        self.msg_manager = GatewayMsgManager()              # 处理本节点需要处理的消息
        self.game_server_connect = {}   # 游戏服连接connect id -> rk_zone

    # ========== child class must override functions ==========
    def get_node_type(self):
        return ModTopo.NODE_TYPE.GATEWAY

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # gateway的服务器节点: monitor
        server_node_id = self.get_node_type_by_client_type(client_type)
        if server_node_id == ModTopo.NODE_TYPE.MONITOR:
            game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
        else:
            logger.GetLog().error('send msg to an unexpected server node : %s, %s, %s' % (client_type, msg_str, args))

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # gateway的客户端节点: 所有 proxy
        if client_node_type == ModTopo.NODE_TYPE.CHAT_PROXY:
            self._send_msg_to_chat_proxy(msg_str)
        elif client_node_type == ModTopo.NODE_TYPE.TEAM_PROXY:
            self._send_msg_to_team_proxy(msg_str)
        elif client_node_type == ModTopo.NODE_TYPE.FIGHT_PROXY:
            self._send_msg_to_fight_proxy(msg_str)
        elif client_node_type == ModTopo.NODE_TYPE.SCENE_PROXY:
            self._send_msg_to_scene_proxy(msg_str)
        else:
            logger.GetLog().error('send msg to an unexpected client node : %s, %s, %s' % (client_node_type, msg_str, args))

    # ========== C++ API ==========
    def OnStartUp(self, config_file):
        CAppBase.OnStartUp(self, config_file)

    def OnClientConnected(self, service_type, conn_id, ip):
        logger.GetLog().debug('OnClientConnected : %s, %s, %s' % (service_type, conn_id, ip))
        if service_type == ModTopo.SERVICE_TYPE.FOR_CLIENT:
            # 是客户端连接
            self.connect_info_dict[conn_id] = ClientConnect(conn_id)
        CAppBase.OnClientConnected(self, service_type, conn_id, ip)

    def OnClientDisconnect(self, service_type, conn_id):
        if service_type == ModTopo.SERVICE_TYPE.FOR_CLIENT:
            self.msg_manager.handle_user_logout(conn_id)
            self.del_game_server_connect(conn_id)
        CAppBase.OnClientDisconnect(self, service_type, conn_id)

    def OnClientRpcMsg(self, service_type, conn_id, proto, msg_str):
        if service_type == ModTopo.SERVICE_TYPE.FOR_CLIENT:
            # 是客户端发来的消息
            if proto == ModTopo.PROTO_TYPE.COMMON:
                # common 类型协议,网关自己处理
                self.get_client_msg_handler().OnClientCommonMsg(conn_id, msg_str)
                return
            if proto == ModTopo.PROTO_TYPE.CHAT:
                # 普通聊天类型协议
                self.get_client_msg_handler().OnClientChatMsg(conn_id, msg_str)
            elif proto == ModTopo.PROTO_TYPE.TEAM:
                # 组队协议
                self.get_client_msg_handler().OnClientTeamMsg(conn_id, msg_str)
            elif proto == ModTopo.PROTO_TYPE.FIGHT:
                self.get_client_msg_handler().OnClientBattleMsg(conn_id, msg_str)
            elif proto == ModTopo.PROTO_TYPE.SCENE:
                self.get_client_msg_handler().OnClientSceneMsg(conn_id, msg_str)
            else:
                logger.GetLog().warn('OnClientMsg from client %s receive unexpected proto : %s' % (conn_id, proto))
            return
        else:
            # 是节点发来的消息
            CAppBase.OnClientRpcMsg(self, service_type, conn_id, proto, msg_str)

    # ========== public functions ==========
    def get_gateway_2_chat_proxy_rpc(self):
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.CHAT_PROXY)

    def get_gateway_2_team_proxy_rpc(self):
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.TEAM_PROXY)

    def get_gateway_2_fight_proxy_rpc(self):
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.FIGHT_PROXY)

    def get_gateway_2_scene_proxy_rpc(self):
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.SCENE_PROXY)

    def get_gateway_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_client_msg_handler(self):
        return self.client_msg_handler

    def get_conn_id_by_char_id(self, char_id):
        return self.user_connect_dict.get(char_id, -1)

    def get_char_id_by_conn_id(self, conn_id):
        connect_info = self.connect_info_dict.get(conn_id, None)
        if connect_info:
            return connect_info.server_user_id
        return None

    def get_connect_info(self, connect_id):
        return self.connect_info_dict.get(connect_id, None)

    def get_msg_manager(self):
        return self.msg_manager

    def add_connect(self, server_group_id, server_user_id, connect_id):
        if server_group_id not in self.group_connect_dict:
            self.group_connect_dict[server_group_id] = {}
        self.group_connect_dict[server_group_id][connect_id] = 0
        self.connect_info_dict[connect_id].bind_user(server_user_id, server_group_id)
        # server user id -> connect id 字典
        self.user_connect_dict[server_user_id] = connect_id

    def del_connect(self, server_group_id, server_user_id, connect_id):
        if server_user_id in self.user_connect_dict and self.user_connect_dict[server_user_id] == connect_id:
            self.user_connect_dict.pop(server_user_id)
        if server_group_id in self.group_connect_dict:
            self.group_connect_dict[server_group_id].pop(connect_id, None)
        self.connect_info_dict.pop(connect_id, None)

    def add_game_server_connect(self, connect_id, rk_zone):
        self.game_server_connect[connect_id] = rk_zone

    def del_game_server_connect(self, connect_id):
        self.game_server_connect.pop(connect_id, None)

    def is_game_server_connect(self, connect_id):
        return connect_id in self.game_server_connect

    def get_client_connect_ip(self, connect_id):
        return self.get_connect_ip(ModTopo.SERVICE_TYPE.FOR_CLIENT, connect_id)

    def united_send_msg_to_user_client(self, proto_type, server_group_id, str_msg, receiver_id_list=None, except_id_list=None):
        if receiver_id_list is not None:
            # 有指定的接收者
            for receiver_id in receiver_id_list:
                self.send_msg_to_client_by_user_id(proto_type, receiver_id, str_msg)
        else:
            except_connect_id_list = []
            if except_id_list:
                for except_id in except_id_list:
                    connect_id = self.get_conn_id_by_char_id(except_id)
                    if connect_id != -1:
                        except_connect_id_list.append(connect_id)
            if server_group_id in self.group_connect_dict:
                logger.GetLog().debug('connect id dict : %s, except id list: %s' % (self.group_connect_dict[server_group_id], except_connect_id_list))
                for connect_id in self.group_connect_dict[server_group_id]:
                    if connect_id not in except_connect_id_list:
                        self.send_msg_to_client(connect_id, proto_type, str_msg)

    def send_msg_to_client_by_user_id(self, proto_type, server_user_id, str_msg):
        connect_id = self.get_conn_id_by_char_id(server_user_id)
        if connect_id != -1:
            self.send_msg_to_client(connect_id, proto_type, str_msg)

    def send_msg_to_client(self, connect_id, proto_type, msg):
        if self.get_connect_ip(ModTopo.SERVICE_TYPE.FOR_CLIENT, connect_id):
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_CLIENT, connect_id, proto_type, msg)
        else:
            logger.GetLog().warn('send_msg_to_client but not connected : %s, %s' % (connect_id, proto_type))

    # ========== private functions ==========
    def _send_msg_to_chat_proxy(self, msg):
        conn_id_list = self.get_client_node_connect_id_list(ModTopo.NODE_TYPE.CHAT_PROXY)
        if conn_id_list:
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, conn_id_list[0], ModTopo.PROTO_TYPE.CHAT, msg)
        else:
            logger.GetLog().warn('_send_msg_to_chat_proxy but no connect')

    def _send_msg_to_team_proxy(self, msg):
        conn_id_list = self.get_client_node_connect_id_list(ModTopo.NODE_TYPE.TEAM_PROXY)
        if conn_id_list:
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, conn_id_list[0], ModTopo.PROTO_TYPE.TEAM, msg)
        else:
            logger.GetLog().warn('_send_msg_to_team_proxy but no connect')

    def _send_msg_to_fight_proxy(self, msg):
        conn_id_list = self.get_client_node_connect_id_list(ModTopo.NODE_TYPE.FIGHT_PROXY)
        if conn_id_list:
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, conn_id_list[0], ModTopo.PROTO_TYPE.FIGHT, msg)
        else:
            logger.GetLog().warn('_send_msg_to_fight_proxy but no connect')

    def _send_msg_to_scene_proxy(self, msg):
        conn_id_list = self.get_client_node_connect_id_list(ModTopo.NODE_TYPE.SCENE_PROXY)
        if conn_id_list:
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, conn_id_list[0], ModTopo.PROTO_TYPE.SCENE, msg)
        else:
            logger.GetLog().warn('_send_msg_to_scene_proxy but no connect')

    # ========== RPC functions ==========
    # from chat proxy >>>
    def OnMsgFromChat(self, server_group_id, chat_msg_data, receiver_id_list, except_id_list):
        """
        正常是转发给对应的客户端
        """
        logger.GetLog().debug('on msg from chat : %s, %s, %s, %s' % (server_group_id, chat_msg_data, receiver_id_list, except_id_list))
        # 聊天消息广播推送
        self.united_send_msg_to_user_client(ModTopo.PROTO_TYPE.CHAT, server_group_id, msgpack.packb(chat_msg_data), receiver_id_list, except_id_list)

    def OnHandleSendChatMsgResponse(self, server_sender_id, return_code):
        ret_obj = CGSendChatMsgResponse()
        ret_obj.return_code = return_code
        logger.GetLog().debug('handle chat msg response: %s, %s' % (server_sender_id, return_code))
        self.send_msg_to_client_by_user_id(ModTopo.PROTO_TYPE.CHAT, server_sender_id, msgpack.packb(ret_obj.dump()))

    def OnOfflineMsgResponse(self, server_user_id, public_msg_list, clan_msg_list, p2p_msg_list):
        logger.GetLog().debug('handle get offline msg response: %s, %s, %s, %s' % (server_user_id, len(public_msg_list), len(clan_msg_list), len(p2p_msg_list)))
        ret_obj = CGGetChatOfflineMsgResponse()
        ret_data = ret_obj.dump()
        ret_data.update({'public_msg_list': public_msg_list, 'clan_msg_list': clan_msg_list, 'p2p_msg_list': p2p_msg_list})
        self.send_msg_to_client_by_user_id(ModTopo.PROTO_TYPE.CHAT, server_user_id, msgpack.packb(ret_data))

    def OnSynServerOnlineNum(self, server_group_id, online_num):
        """
        同步服务器在线人数
        """
        self.get_msg_manager().update_server_online_num(server_group_id, online_num)
    # from chat proxy <<<

    # from fight proxy >>>
    def OnFightMsgFromFight(self, server_group_id, str_msg, receiver_id_list=None, exclude_id_list=None):
        """
        正常是转发给对应的客户端
        """
        logger.GetLog().debug('on battle msg from battle : %s, %s, %s' % (server_group_id, receiver_id_list, exclude_id_list))
        self.united_send_msg_to_user_client(ModTopo.PROTO_TYPE.FIGHT, server_group_id, str_msg, receiver_id_list, exclude_id_list)
    # from fight proxy <<<

    # from team proxy >>>
    def OnTeamMsgFromTeam(self, server_group_id, str_msg, receiver_id_list=None, except_id_list=None):
        """
        正常是转发给对应的客户端
        """
        logger.GetLog().debug('on team msg from team : %s, %s, %s' % (server_group_id, receiver_id_list, except_id_list))
        self.united_send_msg_to_user_client(ModTopo.PROTO_TYPE.TEAM, server_group_id, str_msg, receiver_id_list, except_id_list)
    # from team proxy <<<

    # from scene proxy >>>
    def OnSceneMsgFromScene(self, server_group_id, msg, receiver_id_list=None, except_id_list=None):
        """
        正常是转发给对应的客户端
        """
        logger.GetLog().debug('on scene msg from scene : %s, %s, %s' % (server_group_id, receiver_id_list, except_id_list))
        self.united_send_msg_to_user_client(ModTopo.PROTO_TYPE.SCENE, server_group_id, msg, receiver_id_list, except_id_list)
    # from scene proxy <<<

    # from monitor >>>
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('gateway on gm msg content = %s, %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_gateway_2_monitor_rpc().OnGMMsgResponse('gateway %s executed gm command %s fail, fail files : %s' % (self.get_node_id(), gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_gateway_2_monitor_rpc().OnGMMsgResponse('gateway executed gm command %s success' % gm_cmd)
        else:
            return_msg = 'gateway unsupported gm command or param unexpected : %s, %s' % (gm_cmd, params_str)
            logger.GetLog().warn(return_msg)
            self.get_gateway_2_monitor_rpc().OnGMMsgResponse(return_msg)
    # from monitor <<<

    # self.RegTick(self.SecTick, "this is tick", 1000)
    #
    # def SecTick(self, msg):
    #     """
    #     tick测试
    #     """
    #     if not getattr(self, "ticks", None):
    #         self.ticks = 1
    #     if self.ticks > 5:
    #         print "before httptest"
    #         self.HttpTest()
    #         print "after httptest"
    #         self.DelTick(self.SecTick)
    #     else:
    #         print "sectick args %s" % msg
    #         self.ticks += 1
    #
    # def HttpTest(self):
    #     import script.common.http.httpclientwithcallback as HTTPCB
    #     HTTPCB.GetHttpMgr().AddRequestWithCallback(
    #         "baidu.com", None,
    #         "POST", "www.baidu.com",
    #         [OnBaiduResponse, ("hello", 1024)],
    #     )
    #
    # def OnBaiduResponse(bSucc, httpStatus, httpHeader, httpBodyLength, httpBody, param):
    #     print "**********OnBaiduResponse", bSucc, httpStatus, httpBody, param



