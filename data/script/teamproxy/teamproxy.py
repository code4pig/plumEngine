# -*- coding: utf8 -*-


import game

import random
import script.common.config.topoconfig as ModTopo
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase


class CTeamProxy(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.team_msg_count = 0

    # ========== child class must override functions ==========
    def get_node_type(self):
        return ModTopo.NODE_TYPE.TEAM_PROXY

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # team proxy的服务器节点: monitor、gateway
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type == ModTopo.NODE_TYPE.MONITOR:
            game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
        elif server_node_type == ModTopo.NODE_TYPE.GATEWAY:
            if server_node_type in self.connect_server_dict:
                if client_type == server_node_type:
                    # 广播给所有的gateway
                    for real_client_type in self.connect_server_dict[server_node_type].keys():
                        game.SendMsgToServer(real_client_type, ModTopo.PROTO_TYPE.TEAM, msg_str)
                else:
                    game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.TEAM, msg_str)
            else:
                logger.GetLog().warn('no gateway connect')
        else:
            logger.GetLog().error('send msg to an unexpected server node : %s, %s, %s' % (client_type, msg_str, args))

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # team proxy的客户端节点: team (可能还有其他逻辑节点)
        if client_node_type == ModTopo.NODE_TYPE.TEAM:
            if args:
                self._send_msg_to_team(msg_str, args[0])
            else:
                self._send_msg_to_team(msg_str)
        else:
            logger.GetLog().error('send msg to an unexpected client node : %s, %s, %s' % (client_node_type, msg_str, args))

    # ========== C++ API ==========
    # None

    # ========== public functions ==========
    def get_team_proxy_2_team_rpc(self, team_node_id=None):
        if team_node_id:
            return self.get_server_rpc_handler(ModTopo.NODE_TYPE.TEAM, team_node_id)
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.TEAM)

    def get_team_proxy_2_gateway_rpc(self, client_type=None):
        if client_type is not None:
            return self.get_client_rpc_handler(client_type)
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.GATEWAY)

    def get_team_proxy_to_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_team_node_id_list(self):
        if ModTopo.NODE_TYPE.TEAM in self.connect_client_dict:
            return self.connect_client_dict[ModTopo.NODE_TYPE.TEAM].keys()
        logger.GetLog().info('no team node connected')
        return []

    # ========== private functions ==========
    def _send_msg_to_team(self, msg_str, team_node_id=None):
        if ModTopo.NODE_TYPE.TEAM in self.connect_client_dict:
            if team_node_id:
                if team_node_id in self.connect_client_dict[ModTopo.NODE_TYPE.TEAM]:
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, self.connect_client_dict[ModTopo.NODE_TYPE.TEAM][team_node_id], ModTopo.PROTO_TYPE.TEAM, msg_str)
                else:
                    logger.GetLog().warn('team node %s not connected' % team_node_id)
            else:
                for team_node_conn_id in self.connect_client_dict[ModTopo.NODE_TYPE.TEAM].values():
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, team_node_conn_id, ModTopo.PROTO_TYPE.TEAM, msg_str)
        else:
            logger.GetLog().warn('no team node in connect_client_dict')

    # ========== rpc 相关 ==========
    # gateway to proxy >>>
    def OnTeamMsg(self, server_group_id, server_user_id, str_msg):
        """
         收到网关转发过来的组队消息
        """
        # 先随机一个team_server_id
        team_node_id_list = self.get_team_node_id_list()
        team_node_id = team_node_id_list[self.team_msg_count % len(team_node_id_list)]
        logger.GetLog().debug('on team msg : %s, %s, %s' % (team_node_id, server_group_id, server_user_id))
        self.get_team_proxy_2_team_rpc(team_node_id).OnTeamMsg(server_group_id, server_user_id, str_msg)
        self.team_msg_count += 1

    def OnUserOnlineStatusUpdate(self, server_group_id, server_user_id, is_online):
        """
        玩家状态改变,广播到所有server
        """
        logger.GetLog().debug('on user status update : %s, %s, %s' % (server_group_id, server_user_id, is_online))
        team_node_id_list = self.get_team_node_id_list()
        rand_id = random.choice(team_node_id_list)  # 随机一条用来处理
        for team_node_id in team_node_id_list:
            self.get_team_proxy_2_team_rpc(team_node_id).OnUserOnlineStatusUpdate(server_group_id, server_user_id, is_online, rand_id == team_node_id)

    def print_msg_count(self):
        logger.GetLog().info('====== print team msg count : %s ========' % self.team_msg_count)
    # gateway to proxy <<<

    # team to proxy>>>
    def OnTeamMsgFromTeam(self, server_group_id, msg, receiver_id_list=None, exclude_id_list=None):
        """
        收到聊天消息，转发下去
        """
        self.get_team_proxy_2_gateway_rpc().OnTeamMsgFromTeam(server_group_id, msg, receiver_id_list, exclude_id_list)

    def OnSynAddMatchUserItem(self, server_group_id, from_team_server_id, match_item):
        """
        同步增加玩家匹配
        """
        team_node_id_list = self.get_team_node_id_list()
        for team_node_id in team_node_id_list:
            if team_node_id != from_team_server_id:
                self.get_team_proxy_2_team_rpc(team_node_id).OnAddMatchUserItem(server_group_id, match_item)

    def OnSynAddMatchTeamItem(self, server_group_id, from_team_node_id, match_item):
        team_node_id_list = self.get_team_node_id_list()
        for team_node_id in team_node_id_list:
            if team_node_id != from_team_node_id:
                self.get_team_proxy_2_team_rpc(team_node_id).OnAddMatchTeamItem(server_group_id, match_item)

    def OnSynRemoveMatchItem(self, server_group_id, from_team_node_id, remove_user_id_list, remove_team_id):
        team_node_id_list = self.get_team_node_id_list()
        for team_node_id in team_node_id_list:
            if team_node_id != from_team_node_id:
                self.get_team_proxy_2_team_rpc(team_node_id).OnRemoveMatchItem(server_group_id, remove_user_id_list, remove_team_id)

    def OnSynUpdateTeamList(self, server_group_id, from_team_node_id, team_item):
        team_node_id_list = self.get_team_node_id_list()
        for team_node_id in team_node_id_list:
            if team_node_id != from_team_node_id:
                self.get_team_proxy_2_team_rpc(team_node_id).OnUpdateTeamListItem(server_group_id, team_item)

    def OnSynRemoveTeamListItem(self, server_group_id, from_team_node_id, team_id):
        team_node_id_list = self.get_team_node_id_list()
        for team_node_id in team_node_id_list:
            if team_node_id != from_team_node_id:
                self.get_team_proxy_2_team_rpc(team_node_id).OnRemoveTeamListItem(server_group_id, team_id)

    def OnSynUpdateTeamListItemMemCount(self, server_group_id, from_team_node_id, team_id, mem_count):
        team_node_id_list = self.get_team_node_id_list()
        for team_node_id in team_node_id_list:
            if team_node_id != from_team_node_id:
                self.get_team_proxy_2_team_rpc(team_node_id).OnUpdateTeamListItemMemCount(server_group_id, team_id, mem_count)
    # team to proxy <<<

    # monitor to proxy >>>
    # ====================================================================================
    # ================================ gm command handler ================================
    # ====================================================================================
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('team proxy on gm msg, gm_cmd : %s, params_str: %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_team_proxy_to_monitor_rpc().OnGMMsgResponse('team proxy executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_team_proxy_to_monitor_rpc().OnGMMsgResponse('team proxy executed gm command %s success' % gm_cmd)
        else:
            # 参数不对或者不支持的
            return_msg = 'team proxy unsupported gm command or param unexpected : %s' % gm_cmd
            logger.GetLog().warn(return_msg)
            self.get_team_proxy_to_monitor_rpc().OnGMMsgResponse(return_msg)

    # monitor to proxy <<<
