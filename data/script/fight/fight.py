# -*- coding: utf8 -*-

import game

import time
import random
import script.common.config.topoconfig as ModTopo
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase
from script.fight.battle_manager import BattleManager


class CFight(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.battle_manager = BattleManager()
        self.sec_tick_handlers = []

    # child class must override functions >>>
    def get_node_type(self):
        return ModTopo.NODE_TYPE.FIGHT

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # fight的服务器节点: monitor、fight proxy、db
        logger.GetLog().debug('send_msg_to_server_node : %s, %s' % (client_type, args))
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type in self.connect_server_dict and self.connect_server_dict[server_node_type]:
            if server_node_type == ModTopo.NODE_TYPE.MONITOR:
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.FIGHT_PROXY:
                if client_type == server_node_type:
                    # 需要查找一个实际的node
                    client_type = self.connect_server_dict[server_node_type].keys()[0]     # 因为proxy只有1个, 所以直接取
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.FIGHT, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.DB_PROXY:
                if client_type == server_node_type:
                    # 随机一个db节点处理即可
                    client_type = random.choice(self.connect_server_dict[server_node_type].keys())
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.FIGHT, msg_str)
            else:
                logger.GetLog().error('send msg to an unsupported server node : %s, %s, %s' % (client_type, msg_str, args))
        else:
            logger.GetLog().error('send msg to server node %s but there is no one in connect_server_dict' % server_node_type)

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # fight 节点没有客户端
        logger.GetLog().warn('fight has no client node, please check the code: %s, %s, %s' % (client_node_type, msg_str, args))

    # child class must override functions <<<

    # C++ API >>>
    def OnStartUp(self, conf_file):
        CAppBase.OnStartUp(self, conf_file)
        # 启动定时器并注册事件
        self.RegTick(self._sec_tick, None, 1000)
        self._register_sec_tick_handler(self.battle_manager.battle_sec_timer)
        self.RegTick(self._battle_sync_tick, None, 200)
    # C++ API <<<

    # public functions >>>
    def get_fight_2_fight_proxy_rpc(self, client_type=None):
        if client_type:
            return self.get_client_rpc_handler(client_type)
        # 没有传参数,则传入node type, 在send_msg_to_server_node处再做判断
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.FIGHT_PROXY)

    def get_fight_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_fight_2_db_rpc(self):
        return self.get_send_query_rpc_handler(ModTopo.NODE_TYPE.DB_PROXY)

    def get_battle_manager(self):
        return self.battle_manager
    # public functions <<<

    # private functions >>>
    def _sec_tick(self, _msg):
        if self.sec_tick_handlers:
            now_time = int(time.time())
            # logger.GetLog().debug('sec tick : %s' % now_time)
            for handler in self.sec_tick_handlers:
                handler(now_time)

    def _register_sec_tick_handler(self, handler):
        if handler not in self.sec_tick_handlers:
            self.sec_tick_handlers.append(handler)

    def _battle_sync_tick(self, _):
        self.battle_manager.battle_sync_timer()

    # private functions <<<

    # rpc 相关 >>>
    # from fight proxy >>>
    def OnFightMsg(self, server_group_id, server_user_id, msg, battle_unique_id):
        self.get_battle_manager().handle_battle_msg(server_group_id, server_user_id, msg, battle_unique_id)

    def OnUserOffline(self, server_group_id, server_user_id, battle_unique_id):
        self.get_battle_manager().handle_user_offline(server_group_id, server_user_id, battle_unique_id)

    def OnRegisterFortWarBattleResponse(self, server_group_id, server_user_id, battle_unique_id, temp_init_data):
        self.get_battle_manager().handle_register_fort_war_battle_response(server_group_id, server_user_id, battle_unique_id, temp_init_data)

    def OnRegisterFortBattleResponse(self, server_group_id, server_user_id, battle_unique_id, temp_init_data):
        self.get_battle_manager().handle_register_fort_battle_response(server_group_id, server_user_id, battle_unique_id, temp_init_data)

    # from fight proxy <<<

    # from db >>>
    def OnDoStartTeamBoss(self, result):
        logger.GetLog().debug('handle team boss start : %s' % (result,))
        self.get_battle_manager().callback_start_team_boss(*result)

    def OnTeamBossBattleRealStart(self, result):
        logger.GetLog().debug('handle team boss real start : %s' % (result,))
        pass

    def OnTeamBossBattleTimeout(self, result):
        logger.GetLog().debug('handle team boss battle time out : %s' % (result,))
        pass

    def OnTeamBossBattleFinish(self, result):
        logger.GetLog().debug('handle team boss battle finish : %s' % (result,))
        if result[0]:
            self.get_battle_manager().callback_team_boss_finish(*result[1:])

    def OnTeamBossBattleFail(self, result):
        logger.GetLog().debug('handle team boss battle fail : %s' % (result,))
        pass

    def OnDoCheckJoinFortWarBattle(self, result):
        logger.GetLog().debug('handle check join fort war battle : %s' % (result,))
        self.get_battle_manager().callback_check_join_fort_war_battle(*result)

    def OnFortWarBattleWriteBack(self, result):
        logger.GetLog().debug('handle fort war battle write back : %s' % (result,))
        if result and len(result) > 0:
            self.get_battle_manager().callback_battle_write_back(*result)

    def OnDoCheckJoinFortBattle(self, result):
        logger.GetLog().debug('handle check join fort battle : %s' % (result,))
        self.get_battle_manager().callback_check_join_fort_battle(*result)

    def OnFortBattleWriteBack(self, result):
        logger.GetLog().debug('handle fort battle write back : %s' % (result,))
        if result and len(result) > 0:
            self.get_battle_manager().callback_battle_write_back(*result)
    # from db <<<

    # from monitor >>>
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('fight on gm msg content = %s, %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_fight_2_monitor_rpc().OnGMMsgResponse('fight %s executed gm command %s fail, fail files : %s' % (self.get_node_id(), gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_fight_2_monitor_rpc().OnGMMsgResponse('fight %s executed gm command %s success' % (self.get_node_id(), gm_cmd))
        else:
            return_msg = 'fight unsupported gm command or param unexpected : %s, %s' % (gm_cmd, params_str)
            logger.GetLog().warn(return_msg)
            self.get_fight_2_monitor_rpc().OnGMMsgResponse(return_msg)
    # from monitor <<<
    # rpc 相关 <<<