# -*- coding: utf8 -*-

import game

import random
import script.common.config.topoconfig as ModTopo
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase


class CFightProxy(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.user_battle_dict = {}  # 玩家战斗映射，user server id -> battle_id
        self.battle_route_dict = {}  # 战斗服务器路由字典，battle_id -> fight_node_id

    # ========== child class must override functions ==========
    def get_node_type(self):
        return ModTopo.NODE_TYPE.FIGHT_PROXY

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # fight proxy的服务器节点: monitor、gateway
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type == ModTopo.NODE_TYPE.MONITOR:
            game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
        elif server_node_type == ModTopo.NODE_TYPE.GATEWAY:
            if server_node_type in self.connect_server_dict:
                if client_type == server_node_type:
                    # 广播给所有的gateway
                    for real_client_type in self.connect_server_dict[server_node_type].keys():
                        game.SendMsgToServer(real_client_type, ModTopo.PROTO_TYPE.FIGHT, msg_str)
                else:
                    game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.FIGHT, msg_str)
            else:
                logger.GetLog().warn('no gateway connect')
        else:
            logger.GetLog().error('send msg to an unexpected server node : %s, %s, %s' % (client_type, msg_str, args))

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # fight proxy的客户端节点: fight (可能还有其他逻辑节点)
        if client_node_type == ModTopo.NODE_TYPE.FIGHT:
            if args:
                self._send_msg_to_fight(msg_str, args[0])
            else:
                self._send_msg_to_fight(msg_str)
        else:
            logger.GetLog().error('send msg to an unexpected client node : %s, %s, %s' % (client_node_type, msg_str, args))

    # ========== C++ API ==========
    # None

    # ========== public functions ==========
    def get_fight_proxy_2_fight_rpc(self, fight_node_id=None):
        if fight_node_id:
            return self.get_server_rpc_handler(ModTopo.NODE_TYPE.FIGHT, fight_node_id)
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.FIGHT)

    def get_fight_proxy_2_gateway_rpc(self, client_type=None):
        if client_type is not None:
            return self.get_client_rpc_handler(client_type)
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.GATEWAY)

    def get_fight_proxy_to_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_user_battle_id(self, server_user_id):
        if server_user_id in self.user_battle_dict:
            return self.user_battle_dict[server_user_id]
        return None

    def get_fight_node_id_by_user_id(self, server_user_id):
        battle_id = self.user_battle_dict.get(server_user_id, None)
        if battle_id and battle_id in self.battle_route_dict:
            return self.battle_route_dict[battle_id]
        return None

    def add_user_battle_map_data(self, server_user_id, battle_id):
        self.user_battle_dict[server_user_id] = battle_id

    def add_fight_node_route_data(self, battle_id, fight_node_id):
        self.battle_route_dict[battle_id] = fight_node_id

    def remove_user_battle_map_data(self, server_user_id, battle_unique_id):
        if server_user_id in self.user_battle_dict and self.user_battle_dict[server_user_id] == battle_unique_id:
            self.user_battle_dict.pop(server_user_id, None)

    def remove_fight_node_route_data(self, battle_unique_id, from_fight_node_id):
        if battle_unique_id in self.battle_route_dict and self.battle_route_dict[battle_unique_id] == from_fight_node_id:
            self.battle_route_dict.pop(battle_unique_id, None)

    def get_fight_node_route_data(self, battle_unique_id):
        if battle_unique_id in self.battle_route_dict:
            return self.battle_route_dict[battle_unique_id]
        return None

    def get_fight_node_id_list(self):
        if ModTopo.NODE_TYPE.FIGHT in self.connect_client_dict:
            return self.connect_client_dict[ModTopo.NODE_TYPE.FIGHT].keys()
        logger.GetLog().info('no fight node connected')
        return []

    # ========== private functions ==========
    def _send_msg_to_fight(self, msg_str, fight_node_id=None):
        if ModTopo.NODE_TYPE.FIGHT in self.connect_client_dict:
            if fight_node_id:
                if fight_node_id in self.connect_client_dict[ModTopo.NODE_TYPE.FIGHT]:
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, self.connect_client_dict[ModTopo.NODE_TYPE.FIGHT][fight_node_id], ModTopo.PROTO_TYPE.FIGHT, msg_str)
                else:
                    logger.GetLog().warn('fight node %s not connected' % fight_node_id)
            else:
                for fight_node_conn_id in self.connect_client_dict[ModTopo.NODE_TYPE.FIGHT].values():
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, fight_node_conn_id, ModTopo.PROTO_TYPE.FIGHT, msg_str)
        else:
            logger.GetLog().warn('no fight node in connect_client_dict')

    # ========== rpc 相关 ==========
    # gateway to proxy >>>
    def OnFightMsg(self, server_group_id, server_user_id, msg):
        """
         收到网关转发过来的战斗消息
        """
        logger.GetLog().debug('on fight msg : %s, %s' % (server_group_id, server_user_id))
        battle_unique_id = self.get_user_battle_id(server_user_id)
        if battle_unique_id:
            map_fight_node_id = self.get_fight_node_id_by_user_id(server_user_id)
        else:
            # 没找到对应的战斗
            logger.GetLog().info('fight msg no map server id : %s' % (server_user_id,))
            fight_node_id_list = self.get_fight_node_id_list()
            map_fight_node_id = random.choice(fight_node_id_list)  # 随机一条用来处理
        self.get_fight_proxy_2_fight_rpc(map_fight_node_id).OnFightMsg(server_group_id, server_user_id, msg, battle_unique_id)

    def OnUserOffline(self, server_group_id, server_user_id):
        """
        战斗中玩家下线处理
        """
        logger.GetLog().debug('fight proxy user offline : %s, %s' % (server_group_id, server_user_id))
        battle_unique_id = self.get_user_battle_id(server_user_id)
        if battle_unique_id:
            map_fight_node_id = self.get_fight_node_id_by_user_id(server_user_id)
            self.get_fight_proxy_2_fight_rpc(map_fight_node_id).OnUserOffline(server_group_id, server_user_id, battle_unique_id)
    # gateway to proxy <<<

    # fight to proxy>>>
    def OnFightMsgFromFight(self, server_group_id, str_msg, receiver_id_list=None, exclude_id_list=None):
        """
        收到战斗消息，转发下去
        """
        self.get_fight_proxy_2_gateway_rpc().OnFightMsgFromFight(server_group_id, str_msg, receiver_id_list, exclude_id_list)

    def OnRegisterBattle(self, from_fight_node_id, battle_unique_id, server_user_id_list):
        logger.GetLog().debug('on register battle : %s, %s, %s' % (from_fight_node_id, battle_unique_id, server_user_id_list))
        for server_user_id in server_user_id_list:
            self.add_user_battle_map_data(server_user_id, battle_unique_id)
        self.add_fight_node_route_data(battle_unique_id, from_fight_node_id)

    def OnUnRegisterBattle(self, from_fight_node_id, battle_unique_id, server_user_id_list):
        logger.GetLog().debug('on un register battle : %s, %s, %s' % (from_fight_node_id, battle_unique_id, server_user_id_list))
        for server_user_id in server_user_id_list:
            self.remove_user_battle_map_data(server_user_id, battle_unique_id)
        self.remove_fight_node_route_data(battle_unique_id, from_fight_node_id)

    def OnRegisterFortWarBattle(self, battle_unique_id, server_group_id, server_user_id, temp_init_data):
        logger.GetLog().debug('on find fort war battle : %s, %s' % (battle_unique_id, server_user_id))
        map_fight_node_id = self.get_fight_node_route_data(battle_unique_id)
        if not map_fight_node_id:
            # 没有战斗, 增加数据
            fight_node_id_list = self.get_fight_node_id_list()
            map_fight_node_id = random.choice(fight_node_id_list)  # 随机一条用来处理
            self.add_fight_node_route_data(battle_unique_id, map_fight_node_id)
        self.add_user_battle_map_data(server_user_id, battle_unique_id)
        # 注册反馈
        self.get_fight_proxy_2_fight_rpc(map_fight_node_id).OnRegisterFortWarBattleResponse(server_group_id, server_user_id, battle_unique_id, temp_init_data)

    def OnRegisterFortBattle(self, battle_unique_id, server_group_id, server_user_id, temp_init_data):
        logger.GetLog().debug('on find fort battle : %s, %s' % (battle_unique_id, server_user_id))
        map_fight_node_id = self.get_fight_node_route_data(battle_unique_id)
        if not map_fight_node_id:
            # 没有战斗, 增加数据
            fight_node_id_list = self.get_fight_node_id_list()
            map_fight_node_id = random.choice(fight_node_id_list)  # 随机一条用来处理
            self.add_fight_node_route_data(battle_unique_id, map_fight_node_id)
        self.add_user_battle_map_data(server_user_id, battle_unique_id)
        # 注册反馈
        self.get_fight_proxy_2_fight_rpc(map_fight_node_id).OnRegisterFortBattleResponse(server_group_id, server_user_id, battle_unique_id, temp_init_data)
    # fight to proxy <<<

    # monitor to proxy>>>
    # ====================================================================================
    # ================================ gm command handler ================================
    # ====================================================================================
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('fight proxy on gm msg , gm_cmd : %s, params_str: %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_fight_proxy_to_monitor_rpc().OnGMMsgResponse('fight proxy executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:   # 所有文件重load成功
                self.get_fight_proxy_to_monitor_rpc().OnGMMsgResponse('fight proxy executed gm command %s success' % gm_cmd)
        else:
            # 参数不对或者不支持的
            return_msg = 'fight proxy unsupported gm command or param unexpected : %s' % gm_cmd
            logger.GetLog().warn(return_msg)
            self.get_fight_proxy_to_monitor_rpc().OnGMMsgResponse(return_msg)

    # monitor to proxy <<<
