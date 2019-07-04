# -*- coding:utf8 -*-

from __future__ import unicode_literals

import msgpack
import time
import script.common.log as logger
import script.common.protocol_def as proto_def
import script.fight.object_factory as ModObjFac
from script.common.protocol_def import *
from script.common.game_define.rt_battle_define import TEAM_BOSS_BATTLE_STEP_INIT, TEAM_BOSS_BATTLE_STEP_GOING, TEAM_BOSS_BATTLE_STEP_DONE, \
    BATTLE_RESULT_TYPE_FINISH, BATTLE_RESULT_TYPE_FAIL, TEAM_BOSS_BATTLE_INIT_MAX_TIME, BATTLE_RESULT_TYPE_TIMEOUT
from script.fight.battle_handler_base import BattleHandlerBase


class BattleHandlerTeamBoss(BattleHandlerBase):
    def __init__(self):
        self.battle_unique_id = None        # 战斗唯一id
        self.boss_unique_id = None          # team boss 唯一id
        self.battle_status = 0              # 战斗状态
        self.start_time = 0                 # 开启时间
        self.real_start_time = 0            # 战斗实际开启时间
        self.end_time = 0                   # 战斗结束时间
        self.ctrl_server_user_id = None     # 当前控制的玩家id
        self.member_data_dict = {}          # 战斗玩家数据
        self.boss_data = None               # boss 数据
        self.server_group_id = None         # server group id
        self.team_id = 0                    # 队伍id
        self.leader_server_user_id = None   # 队长server user id
        self.tick_count = 0                 # tick_count
        self.tick_op_list = []              # 当前tick的操作列表
        self.op_list_log = []               # 操作日志
        self.member_auto_status_dict = {}   # 战斗玩家自动状态字典

    def init_battle(self, server_group_id, team_id, battle_unique_id, boss_unique_id, battle_start_time, battle_end_time, leader_server_user_id, member_dict, boss_data):
        self.server_group_id = server_group_id
        self.team_id = team_id
        self.battle_unique_id = battle_unique_id
        self.boss_unique_id = boss_unique_id
        self.battle_status = TEAM_BOSS_BATTLE_STEP_INIT
        self.start_time = battle_start_time
        self.end_time = battle_end_time
        self.leader_server_user_id = leader_server_user_id
        self.ctrl_server_user_id = leader_server_user_id    # 默认为队长做控制
        self.member_data_dict = member_dict
        self.boss_data = boss_data

    def handle_battle_msg(self, server_user_id, cmd, msg):
        if cmd == proto_def.bt_battle_init_finish:
            # 战斗初始化完成
            self._handle_battle_init_finish(server_user_id, msg)
        elif cmd == proto_def.bt_battle_op:
            # 战斗操作转发
            is_finish = self._handle_battle_op(server_user_id, msg)
            return is_finish
        elif cmd == proto_def.bt_quit_battle:
            self._handle_quit_battle(server_user_id)
        else:
            logger.GetLog().warn('this battle protocol is unexpected, cmd is : %s' % cmd)
        return False

    def handle_sec_timer(self, current_time):
        if self._is_all_member_leave():     # 所有人都退出了
            logger.GetLog().debug('team boss battle timeout timer : %s, %s' % (self.server_group_id, self.team_id))
            cur_hp = self.boss_data.combatant_data.default_status.cur_hp
            self.battle_status = TEAM_BOSS_BATTLE_STEP_DONE
            ModObjFac.CreateApp().get_fight_2_db_rpc().TeamBossBattleTimeout(self.server_group_id, self.team_id, self.boss_unique_id, self.battle_unique_id, cur_hp)
            return True
        elif self.battle_status == TEAM_BOSS_BATTLE_STEP_INIT:        # 等待客户端初始化
            if self.start_time + TEAM_BOSS_BATTLE_INIT_MAX_TIME <= current_time:
                logger.GetLog().debug('team boss battle init timeout timer : %s, %s' % (self.server_group_id, self.team_id))
                self.battle_status = TEAM_BOSS_BATTLE_STEP_GOING
                self.real_start_time = current_time
                diff_time = max(0, self.real_start_time - self.start_time)
                self.end_time += diff_time
                # 推送正式开始战斗给所有成员
                syn_real_start = BTRealStartBattle()
                syn_real_start.auto_status_dict = self.member_auto_status_dict
                # 更新db结束时间数据
                ModObjFac.CreateApp().get_fight_2_db_rpc().TeamBossBattleRealStart(self.server_group_id, self.team_id, self.battle_unique_id, self.real_start_time, self.end_time)
                on_mem_id_list = [server_mem_id for server_mem_id, mem_data in self.member_data_dict.iteritems() if not mem_data.is_off]
                # 消息推送客户端
                ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_real_start.dump()), on_mem_id_list)
        elif self.battle_status == TEAM_BOSS_BATTLE_STEP_GOING:     # 进行中
            if self.end_time <= current_time:
                logger.GetLog().debug('team boss battle timeout timer : %s, %s' % (self.server_group_id, self.team_id))
                cur_hp = self.boss_data.combatant_data.default_status.cur_hp
                self.battle_status = TEAM_BOSS_BATTLE_STEP_DONE
                ModObjFac.CreateApp().get_fight_2_db_rpc().TeamBossBattleTimeout(self.server_group_id, self.team_id, self.boss_unique_id, self.battle_unique_id, cur_hp)
                # 同步结算给客户端
                syn_to_mem = BTTeamBossResult()
                syn_to_mem.result_type = BATTLE_RESULT_TYPE_TIMEOUT
                on_mem_id_list = [server_mem_id for server_mem_id, mem_data in self.member_data_dict.iteritems() if not mem_data.is_off]
                ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_to_mem.dump()), on_mem_id_list)
                # TODO：部分战斗数据日志保存？
                return True
        return False

    def handle_battle_sync_timer(self):
        if self.battle_status == TEAM_BOSS_BATTLE_STEP_GOING:
            self.tick_count += 1
            sync_obj = BTSyncBattleTick()
            sync_obj.tick_count = self.tick_count
            sync_obj.op_list = self.tick_op_list
            self.op_list_log.append(sync_obj)
            self.tick_op_list = []
            on_mem_id_list = [server_mem_id for server_mem_id, mem_data in self.member_data_dict.iteritems() if not mem_data.is_off]
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(sync_obj.dump()), on_mem_id_list)

    def handle_db_callback(self, handle_flag, *args):
        return False

    def handle_user_leave(self, server_user_id):
        self.member_data_dict[server_user_id].is_off = True
        if self.ctrl_server_user_id == server_user_id:
            # 是当前的接管者,转换接管者
            next_ctrl_member = None
            recv_id_list = []
            for server_member_id, mem in self.member_data_dict.iteritems():
                if not mem.is_off:
                    recv_id_list.append(server_member_id)
                    if not next_ctrl_member:
                        next_ctrl_member = server_member_id
            if next_ctrl_member:
                # 有找到新的继承者，推送消息
                self.ctrl_server_user_id = next_ctrl_member
                if recv_id_list:
                    change_ctrl = BTChangeBattleCtrlUser()
                    change_ctrl.ctrl_server_user_id = next_ctrl_member
                    ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(change_ctrl.dump()), recv_id_list)
            else:
                # TODO:找不到一个满足条件的,所有人都离线了
                self.ctrl_server_user_id = None
                pass

    def _handle_battle_init_finish(self, server_user_id, msg):
        if self.battle_status != TEAM_BOSS_BATTLE_STEP_INIT:
            logger.GetLog().warn('battle is not init: %s, %s, %s' % (self.server_group_id, server_user_id, self.battle_unique_id))
            return
        if server_user_id not in self.member_data_dict:
            logger.GetLog().warn('user not in battle mem: %s, %s, %s' % (self.server_group_id, server_user_id, self.battle_unique_id))
            return
        self.member_data_dict[server_user_id].is_init_ok = True
        recv_obj = BTBattleInitFinish.new_from_data(msg)
        self.member_auto_status_dict[server_user_id] = 1 if recv_obj.auto_status else 0
        if self._is_all_member_init_ok():
            self.battle_status = TEAM_BOSS_BATTLE_STEP_GOING
            self.real_start_time = time.time()
            diff_time = max(0, self.real_start_time - self.start_time)
            self.end_time += diff_time
            # 推送正式开始战斗给所有成员
            syn_real_start = BTRealStartBattle()
            syn_real_start.auto_status_dict = self.member_auto_status_dict
            # 更新db结束时间数据
            ModObjFac.CreateApp().get_fight_2_db_rpc().TeamBossBattleRealStart(self.server_group_id, self.team_id, self.battle_unique_id, self.real_start_time, self.end_time)
            # 消息推送客户端
            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_real_start.dump()), self.member_data_dict.keys())

    def _handle_battle_op(self, server_user_id, msg):
        """

        :param server_user_id:
        :param msg:
        :return: 是否战斗结束， Boolean
        """
        if self.battle_status != TEAM_BOSS_BATTLE_STEP_GOING:
            logger.GetLog().warn('battle is not going: %s, %s, %s' % (self.server_group_id, server_user_id, self.battle_unique_id))
            return True
        if server_user_id not in self.member_data_dict:
            logger.GetLog().warn('user not in battle mem: %s, %s, %s' % (self.server_group_id, server_user_id, self.battle_unique_id))
            return False
        # 消息转发
        recv_obj = BTBattleOpSend.new_from_data(msg)
        if recv_obj.content:
            self.tick_op_list.append(recv_obj.content)
        if recv_obj.ext_info_list:
            on_mem_id_list = [server_mem_id for server_mem_id, mem_data in self.member_data_dict.iteritems() if not mem_data.is_off]
            for ext_info in recv_obj.ext_info_list:
                if ext_info.is_self_die:  # 自己死亡
                    dead_list = [x for x in ext_info.server_target_id.split('|') if x]
                    for dead_server_user_id in dead_list:
                        self.member_data_dict[dead_server_user_id].is_dead = True
                    # 检查是否所有人都死了
                    is_all_dead = True
                    for mem in self.member_data_dict.itervalues():
                        if not mem.is_dead:
                            is_all_dead = False
                            break
                    if is_all_dead:
                        # 更新db数据
                        ModObjFac.CreateApp().get_fight_2_db_rpc().TeamBossBattleFail(self.server_group_id, self.team_id, self.boss_unique_id, self.battle_unique_id)
                        # 同步结算给客户端
                        syn_to_mem = BTTeamBossResult()
                        syn_to_mem.result_type = BATTLE_RESULT_TYPE_FAIL
                        ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_to_mem.dump()), on_mem_id_list)
                        # 失败,删除数据
                        return True
                if ext_info.server_target_id:  # 目标是boss
                    if str(self.boss_data.combatant_data.id) in [x for x in ext_info.server_target_id.split('|') if x]:
                        # boss在目标列表中
                        if ext_info.damage > 0:
                            self.boss_data.combatant_data.default_status.cur_hp = self.boss_data.combatant_data.default_status.cur_hp - ext_info.damage
                            syn_boss_hp = BTSynTeamBossHp()
                            syn_boss_hp.cur_hp = max(0, self.boss_data.combatant_data.default_status.cur_hp)
                            ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_boss_hp.dump()), on_mem_id_list)
                            # 处理boss血量,检查是否已完成
                            if self.boss_data.combatant_data.default_status.cur_hp <= 0:
                                # 更新状态
                                self.battle_status = TEAM_BOSS_BATTLE_STEP_DONE
                                # 更新db数据
                                ModObjFac.CreateApp().get_fight_2_db_rpc().TeamBossBattleFinish(self.server_group_id, self.team_id, self.boss_unique_id,
                                                                                                self.battle_unique_id, self.member_data_dict.keys(),
                                                                                                self.leader_server_user_id)
                                # 同步结算给客户端(移到给完奖励后再推送)
                                # syn_to_mem = BTTeamBossResult()
                                # syn_to_mem.result_type = BATTLE_RESULT_TYPE_FINISH
                                # ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, json.dumps(syn_to_mem.dump()), on_mem_id_list)
                                return True
        return False

    def _handle_quit_battle(self, server_user_id):
        self.handle_user_leave(server_user_id)

    def _is_all_member_init_ok(self):
        for v in self.member_data_dict.itervalues():
            if not v.is_init_ok:
                return False
        return True

    def _is_all_member_leave(self):
        for v in self.member_data_dict.itervalues():
            if not v.is_off:
                return False
        return True
