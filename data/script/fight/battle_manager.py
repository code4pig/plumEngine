# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import time
import msgpack
import script.common.log as logger
import script.common.exception_def as excp
import script.common.protocol_def as proto_def
import script.fight.object_factory as ModObjFac
from script.common.protocol_def import *
from script.common.game_define.util import get_random_seed
from script.common.game_define.rt_battle_define import TeamBossBattleMember, FortWarBattleInitTempData, BATTLE_RESULT_TYPE_FINISH, FortBattleInitTempData
from script.common.game_define.alpha_fort_war_def import ALPHA_FORT_WAR_POINT_ID_THRONE, ALPHA_FORT_WAR_POINT_ID_GATE
from script.fight.battle_handler_team_boss import BattleHandlerTeamBoss
from script.fight.battle_handler_fort_war import BattleHandlerFortWar
from script.fight.battle_handler_fort_battle import BattleHandlerFortBattle


class BattleManager(object):
    def __init__(self):
        self.battle_handler_dict = {}       # battle unique id -> battle handler
        self.battle_user_dict = {}          # battle unique id -> server user id list

    def handle_battle_msg(self, server_group_id, server_user_id, str_msg, battle_unique_id):
        msg = msgpack.unpackb(str_msg)
        logger.GetLog().debug('handle battle msg : %s, %s, %s' % (server_group_id, server_user_id, msg))
        cmd = msg.get(proto_def.field_name_cmd, None)
        try:
            if cmd is None:
                logger.GetLog().warn('format of this battle msg is unexpected , cmd is None')
            elif cmd == proto_def.bt_start_team_boss:
                # 开始队伍boss
                self._start_team_boss(server_group_id, server_user_id, msg)
            elif cmd == proto_def.bt_join_fort_war_battle:
                # 加入要塞战战斗
                self._check_join_fort_war_battle(server_group_id, server_user_id, msg)
            elif cmd == proto_def.bt_join_fort_battle:
                # 加入占领战要塞据点战斗
                self._check_join_fort_battle(server_group_id, server_user_id, msg)
            elif battle_unique_id:
                if battle_unique_id in self.battle_handler_dict:
                    is_battle_finish = self.battle_handler_dict[battle_unique_id].handle_battle_msg(server_user_id, cmd, msg)
                    if is_battle_finish:
                        # 删除战斗
                        self.battle_handler_dict.pop(battle_unique_id)
                        # 调用proxy接口,注册战斗
                        if battle_unique_id in self.battle_user_dict and self.battle_user_dict[battle_unique_id]:
                            app_obj = ModObjFac.CreateApp()
                            app_obj.get_fight_2_fight_proxy_rpc().OnUnRegisterBattle(app_obj.get_node_id(), battle_unique_id, self.battle_user_dict[battle_unique_id])
                            self.battle_user_dict.pop(battle_unique_id, None)
                else:
                    logger.GetLog().error('battle handler is not found, cmd is : %s, %s' % (cmd, battle_unique_id))
            else:
                logger.GetLog().warn('this battle protocol need battle unique id but none, cmd is : %s' % cmd)
        except Exception as e:
            logger.GetLog().error('handle battle msg catch an error : %s' % excp.log_exceptions(cmd=cmd, exception=e))

    def handle_user_offline(self, server_group_id, server_user_id, battle_unique_id):
        logger.GetLog().debug('handle battle user offline : %s, %s, %s' % (server_group_id, server_user_id, battle_unique_id))
        if battle_unique_id in self.battle_handler_dict:
            self.battle_handler_dict[battle_unique_id].handle_user_leave(server_user_id)

    def handle_register_fort_war_battle_response(self, server_group_id, server_user_id, battle_unique_id, temp_init_data):
        logger.GetLog().debug('handle register fort war battle response : %s, %s, %s' % (server_user_id, battle_unique_id, temp_init_data))
        if battle_unique_id not in self.battle_handler_dict:
            temp_init_data_obj = FortWarBattleInitTempData.new_from_data(temp_init_data)
            battle_handler = BattleHandlerFortWar()
            battle_handler.init_battle(server_group_id, battle_unique_id, temp_init_data_obj.self_clan_id, temp_init_data_obj.enemy_clan_id, temp_init_data_obj.point_id,
                                       time.time(), temp_init_data_obj.end_time, temp_init_data_obj.total_hp, temp_init_data_obj.rest_hp)
            self.battle_handler_dict[battle_unique_id] = battle_handler
        # 处理玩家加入战斗
        self.battle_handler_dict[battle_unique_id].handle_user_join(server_user_id)
        if battle_unique_id not in self.battle_user_dict:
            self.battle_user_dict[battle_unique_id] = []
        if server_user_id not in self.battle_user_dict[battle_unique_id]:
            self.battle_user_dict[battle_unique_id].append(server_user_id)

    def handle_register_fort_battle_response(self, server_group_id, server_user_id, battle_unique_id, temp_init_data):
        logger.GetLog().debug('handle register fort battle response : %s, %s, %s' % (server_user_id, battle_unique_id, temp_init_data))
        if battle_unique_id not in self.battle_handler_dict:
            temp_init_data_obj = FortBattleInitTempData.new_from_data(temp_init_data)
            battle_handler = BattleHandlerFortBattle()
            battle_handler.init_battle(server_group_id, battle_unique_id, temp_init_data_obj.field_id, temp_init_data_obj.block_id,
                                       temp_init_data_obj.point_id, temp_init_data_obj.defense_clan_id, temp_init_data_obj.attack_clan_id,
                                       time.time(), temp_init_data_obj.end_time, temp_init_data_obj.total_hp, temp_init_data_obj.rest_hp)
            self.battle_handler_dict[battle_unique_id] = battle_handler
        # 处理玩家加入战斗
        self.battle_handler_dict[battle_unique_id].handle_user_join(server_user_id)
        if battle_unique_id not in self.battle_user_dict:
            self.battle_user_dict[battle_unique_id] = []
        if server_user_id not in self.battle_user_dict[battle_unique_id]:
            self.battle_user_dict[battle_unique_id].append(server_user_id)

    def _start_team_boss(self, server_group_id, server_user_id, msg):
        msg_obj = BTStartTeamBossRequest.new_from_data(msg)
        ModObjFac.CreateApp().get_fight_2_db_rpc().DoStartTeamBoss(server_group_id, server_user_id, msg_obj.part)

    def callback_start_team_boss(self, server_group_id, server_user_id, return_code, part_key=None, team_boss_doc=None, team_doc=None, tb_battle_hero_dict=None,
                                 tb_battle_boss=None):
        r_2_c = BTStartTeamBossResponse()
        r_2_c.return_code = return_code
        app_obj = ModObjFac.CreateApp()
        app_obj.get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(r_2_c.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 发起战斗成功,将信息转发给所有成员
            second_step = team_boss_doc.second_step
            random_seed = get_random_seed()
            rand_seed = random_seed
            syn_init_battle = BTSynInitTeamBoss()
            syn_init_battle.random_seed = random_seed
            syn_init_battle.rand_seed = rand_seed
            syn_init_battle.ctrl_server_user_id = server_user_id
            syn_init_battle.func_type = team_boss_doc.func_type
            syn_init_battle.team_boss = tb_battle_boss
            syn_init_battle.hero_dict = tb_battle_hero_dict
            app_obj.get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(syn_init_battle.dump()), team_doc.member_id_list)
            # 构造战斗handler
            self.battle_handler_dict[second_step.battle_unique_id] = BattleHandlerTeamBoss()
            member_dict = {}
            for server_member_id, battle_data in tb_battle_hero_dict.iteritems():
                battle_mem = TeamBossBattleMember()
                battle_mem.server_user_id = server_member_id
                battle_mem.battle_data = battle_data
                member_dict[server_member_id] = battle_mem
            self.battle_handler_dict[second_step.battle_unique_id].init_battle(server_group_id, team_doc.team_id, second_step.battle_unique_id, team_boss_doc.unique_id,
                                                                               second_step.battle_start_time, second_step.battle_end_time, server_user_id, member_dict,
                                                                               tb_battle_boss)
            self.battle_user_dict[second_step.battle_unique_id] = member_dict.keys()
            # 调用proxy接口,注册战斗
            app_obj.get_fight_2_fight_proxy_rpc().OnRegisterBattle(app_obj.get_node_id(), second_step.battle_unique_id, member_dict.keys())

    def callback_team_boss_finish(self, server_group_id, member_id_list, reward_result_dict=None, server_leader_id=None, leader_reward_dict=None, member_reward_dict=None):
        if member_id_list:
            syn_to_mem = BTTeamBossResult()
            syn_to_mem.result_type = BATTLE_RESULT_TYPE_FINISH
            # 推送给队长
            if server_leader_id:
                if leader_reward_dict and reward_result_dict and reward_result_dict[server_leader_id]:
                    syn_to_mem.reward_dict = leader_reward_dict
                ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(syn_to_mem.dump()), [server_leader_id])
            # 推送给队员
            if server_leader_id in member_id_list:
                member_id_list.remove(server_leader_id)
            if member_id_list:
                has_reward_list = []
                no_reward_list = []
                for server_member_id in member_id_list:
                    if reward_result_dict and reward_result_dict[server_member_id]:
                        has_reward_list.append(server_member_id)
                    else:
                        no_reward_list.append(server_member_id)
                if has_reward_list:
                    syn_to_mem.reward_dict = member_reward_dict
                    ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(syn_to_mem.dump()), has_reward_list)
                if no_reward_list:
                    syn_to_mem.reward_dict = {}
                    ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(syn_to_mem.dump()), no_reward_list)

    def _check_join_fort_war_battle(self, server_group_id, server_user_id, msg):
        msg_obj = BTJoinFortWarBattleRequest.new_from_data(msg)
        if msg_obj.point_id == ALPHA_FORT_WAR_POINT_ID_GATE or msg_obj.point_id == ALPHA_FORT_WAR_POINT_ID_THRONE:
            ModObjFac.CreateApp().get_fight_2_db_rpc().DoCheckJoinFortWarBattle(server_group_id, server_user_id, msg_obj.point_id)
        else:
            res = BTJoinFortWarBattleResponse()
            res.return_code = excp.ExceptionInvalidParameter.code
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(res.dump()), [server_user_id])

    def callback_check_join_fort_war_battle(self, server_group_id, server_user_id, return_code, self_clan_id=None, enemy_clan_id=None, point_id=0, total_hp=0, rest_hp=0, end_time=0):
        if return_code == excp.ExceptionSuccess.code:
            # 检查成功
            # 调用proxy接口,注册战斗
            battle_unique_id = 'FORT_WAR_BATTLE_{0}_{1}'.format(enemy_clan_id, point_id)
            temp_init_data = FortWarBattleInitTempData()
            temp_init_data.self_clan_id = self_clan_id
            temp_init_data.enemy_clan_id = enemy_clan_id
            temp_init_data.point_id = point_id
            temp_init_data.total_hp = total_hp
            temp_init_data.rest_hp = rest_hp
            temp_init_data.end_time = end_time
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnRegisterFortWarBattle(battle_unique_id, server_group_id, server_user_id, temp_init_data.dump())
        else:
            # 校验失败
            res = BTJoinFortWarBattleResponse()
            res.return_code = return_code
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(res.dump()), [server_user_id])

    def _check_join_fort_battle(self, server_group_id, server_user_id, msg):
        msg_obj = BTJoinFortBattleRequest.new_from_data(msg)
        ModObjFac.CreateApp().get_fight_2_db_rpc().DoCheckJoinFortBattle(server_group_id, server_user_id, msg_obj.point_id)

    def callback_check_join_fort_battle(self, server_group_id, server_user_id, return_code, field_id=None, block_id=-1, point_id=None, defense_clan_id=None,
                                        attack_clan_id=None, total_hp=0, rest_hp=0, end_time=0):
        if return_code == excp.ExceptionSuccess.code:
            # 检查成功
            # 调用proxy接口,注册战斗
            battle_unique_id = 'FORT_BATTLE_{0}_{1}_{2}'.format(field_id, block_id, point_id)
            temp_init_data = FortBattleInitTempData()
            temp_init_data.field_id = field_id
            temp_init_data.block_id = block_id
            temp_init_data.point_id = point_id
            temp_init_data.defense_clan_id = defense_clan_id
            temp_init_data.attack_clan_id = attack_clan_id
            temp_init_data.total_hp = total_hp
            temp_init_data.rest_hp = rest_hp
            temp_init_data.end_time = end_time
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnRegisterFortBattle(battle_unique_id, server_group_id, server_user_id, temp_init_data.dump())
        else:
            # 校验失败
            res = BTJoinFortBattleResponse()
            res.return_code = return_code
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(res.dump()), [server_user_id])

    def callback_battle_write_back(self, server_group_id, battle_unique_id, is_enemy_win):
        if is_enemy_win and battle_unique_id in self.battle_handler_dict:
            # 通知战斗中所有成员, 战斗结束
            push_msg = BTPushBattleLose()
            app_obj = ModObjFac.CreateApp()
            app_obj.get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(server_group_id, msgpack.packb(push_msg.dump()),
                                                                      self.battle_handler_dict[battle_unique_id].get_cur_battle_user_list())
            # 删除战斗数据
            app_obj.get_fight_2_fight_proxy_rpc().OnUnRegisterBattle(app_obj.get_node_id(), battle_unique_id, self.battle_user_dict.get(battle_unique_id, []))
            self.battle_user_dict.pop(battle_unique_id, None)
            self.battle_handler_dict.pop(battle_unique_id)

    def battle_sec_timer(self, cur_time):
        for battle_unique_id in self.battle_handler_dict.keys():
            battle_handler = self.battle_handler_dict.get(battle_unique_id, None)
            if battle_handler:
                is_finish = battle_handler.handle_sec_timer(cur_time)
                if is_finish:
                    app_obj = ModObjFac.CreateApp()
                    app_obj.get_fight_2_fight_proxy_rpc().OnUnRegisterBattle(app_obj.get_node_id(), battle_unique_id, self.battle_user_dict.get(battle_unique_id, []))
                    self.battle_user_dict.pop(battle_unique_id, None)
                    self.battle_handler_dict.pop(battle_unique_id)

    def battle_sync_timer(self):
        for battle_unique_id in self.battle_handler_dict.keys():
            battle_handler = self.battle_handler_dict.get(battle_unique_id, None)
            if battle_handler and hasattr(battle_handler, 'handle_battle_sync_timer'):
                battle_handler.handle_battle_sync_timer()
