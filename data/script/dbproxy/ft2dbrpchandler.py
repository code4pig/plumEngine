# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import time
import script.common.exception_def as excp
import script.common.log as logger
from script.common.db.data_context import DataContext
from script.common.db.instant_box import instant_box
from script.common.game_define.alpha_fort_war_def import ALPHA_FORT_WAR_STEP_ONGOING, ALPHA_FORT_WAR_POINT_ID_THRONE, ALPHA_FORT_WAR_STEP2_POINT_ID_LIST, \
    ALPHA_FORT_WAR_BATTLE_REWARD_WIN, ALPHA_FORT_WAR_BATTLE_REWARD_LOSE, ALPHA_FORT_WAR_RESULT_WIN, ALPHA_FORT_WAR_RESULT_LOSE, ALPHA_FORT_WAR_BATTLE_REWARD_GATE_LAST, \
    ALPHA_FORT_WAR_BATTLE_REWARD_THRONE_LAST, ALPHA_FORT_WAR_POINT_ID_GATE
from script.common.game_define.battle_field_def import BF_STEP_BATTLE, FORT_WAR_POINT_ID_GATE, FORT_WAR_POINT_ID_THRONE, FORT_WAR_STEP2_POINT_ID_LIST, FORT_BATTLE_REWARD_GATE_LAST, \
    FORT_BATTLE_REWARD_THRONE_LAST, BF_CLAN_LOG_DEF_FORT_POINT_FAIL, BF_CLAN_LOG_ATK_FORT_POINT_SUCCESS, BF_CLAN_LOG_ATK_FORT_SUCCESS, BF_CLAN_LOG_DEF_FORT_FAIL
from script.common.game_define.global_def import get_server_and_user_id, get_clan_server_id
from script.common.game_define.rt_battle_define import StatDef, CombatantGroupDef, StatFactorDef, SimpleCombatantData, CombatantStatus, TeamBossBattleUnitHero, \
    TeamBossBattleUnitBoss, EnumAttrTypeDef, CombatantStatusConstDef, MasteryGroupIdDefine
from script.common.game_define.hero_def import HeroSnap
from script.common.game_define.team_define import TEAM_FUNC_TYPE_BOSS_RAID, TEAM_FUNC_TYPE_BOSS_FAFURION
from script.common.game_define.time_util import is_same_date, is_weekend
from script.dbproxy.do.alpha_fort_war_clan_do import AlphaFortWarClanDo
from script.dbproxy.do.alpha_fort_war_match_do import AlphaFortWarMatchDo
from script.dbproxy.do.alpha_fort_war_register_do import AlphaFortWarRegisterDo
from script.dbproxy.do.alpha_fort_war_step_do import AlphaFortWarStepDo
from script.dbproxy.do.alpha_fort_war_user_do import AlphaFortWarUserDo
from script.dbproxy.do.battle_field_block_do import BattleFieldBlockDo
from script.dbproxy.do.battle_field_clan_do import BattleFieldClanDo
from script.dbproxy.do.battle_field_fort_defense_do import BattleFieldFortDefenseDo
from script.dbproxy.do.battle_field_season_do import BattleFieldSeasonDo
from script.dbproxy.do.battle_field_user_do import BattleFieldUserDo
from script.dbproxy.do.clan_dungeon_warehouse_do import ClanDungeonWarehouseDo
from script.dbproxy.do.hero_do import HeroDo
from script.dbproxy.do.heroes_do import HeroesDo
from script.dbproxy.do.inventory_do import InventoryDo
from script.dbproxy.do.mail_bo import MailBo
from script.dbproxy.do.simple_clan_do import ClanDo
from script.dbproxy.do.simple_user_clan_do import UserClanDo
from script.dbproxy.do.user_mastery_do import UserMasteryDo
from script.dbproxy.do.masters_global import master_team_boss_reward_map_inst, master_combatants_inst, master_combatants_base_inst, master_level_factor_inst, \
    master_equipment_inst, master_equipment_set_option_inst, master_stat_mod_inst, master_hero_training_inst, master_transform_strengthen_inst, master_team_boss_training_inst, \
    master_team_boss_part_inst, master_mastery_stat_inst, master_hero_equipment_box_stat_inst, master_equipment_strengthen_set_inst, master_constants_inst, \
    master_alpha_fort_war_battle_reward_inst, master_team_boss_reward_inst, master_bf_battle_reward_inst
from script.dbproxy.do.team_boss_do import TeamBossDo
from script.dbproxy.do.team_do import TeamDo
from script.dbproxy.do.user_raid_do import UserRaidDo
from script.dbproxy.do.user_team_do import UserTeamDo
from script.dbproxy.rpc.irpctarget import IDbsRpcTarget


class Ft2DbRpcHandler(IDbsRpcTarget):
    def __init__(self):
        pass

    def Reload(self, modname):
        import script.common.utils.utils as utils
        utils.Reload(modname)

    def DoStartTeamBoss(self, server_group_id, server_user_id, part_key):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not TeamBossDo.is_in_team_boss_activity_time(instant_box.time_current):
            return server_group_id, server_user_id, excp.ExceptionNotActivityTime.code
        if not user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        if team_do.doc.server_leader_id != server_user_id:
            return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
        # if not team_do.is_member_full():
        #     return server_group_id, server_user_id, excp.ExceptionMemberNotEnough.code
        team_boss_do = TeamBossDo.TryLock(500)(data_context, team_do.team_id)
        if team_boss_do.is_new or team_boss_do.is_boss_expired() or team_boss_do.is_team_boss_finish():
            return server_group_id, server_user_id, excp.ExceptionLeaderNotOpen.code
        if not team_boss_do.is_all_member_ready(team_do.doc.member_id_list):
            return server_group_id, server_user_id, excp.ExceptionMemberNotReady.code
        # 检查第一阶段是否完成
        if not team_boss_do.doc.first_step.is_finish:
            return server_group_id, server_user_id, excp.ExceptionTeamBossPreNotFinish.code
        if part_key not in team_boss_do.doc.second_step.part_dict:
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionParamError.code
        if team_boss_do.doc.second_step.part_dict[part_key].is_finish:
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionTeamBossPartFinish.code
        if team_boss_do.is_second_step_in_battle():
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionTeamBossInBattle.code
        # 水龙只能按顺序挑战
        if team_boss_do.doc.func_type == TEAM_FUNC_TYPE_BOSS_FAFURION:
            count = 0
            for part in team_boss_do.doc.second_step.part_dict.values():
                if part.is_finish:
                    count += 1
            if ('Head' in part_key and count < 2) or ('Arm' in part_key and count < 1):
                return server_group_id, server_user_id, excp.ExceptionTeamBossPreNotFinish.code
        team_boss_do.begin_second_battle(part_key, instant_box.time_current)
        # 队长永远是准备状态
        team_boss_do.member_be_ready(server_user_id)
        # 构造战斗数据
        hero_snap_dict = {}
        for server_member_id in team_do.doc.member_id_list:
            member_server_id, member_id = get_server_and_user_id(server_member_id)
            hero_snap = HeroSnap()
            active_hero_key = HeroesDo.Reader()(data_context, member_id, member_server_id).doc.active
            hero_doc = HeroDo.Reader()(data_context, member_id, active_hero_key, member_server_id).doc
            inventory_doc = InventoryDo.Reader()(data_context, member_id, member_server_id).doc
            mastery_doc = UserMasteryDo.Reader()(data_context, member_id, member_server_id).doc
            hero_snap.load_from_hero(hero_doc, inventory_doc, mastery_doc)
            hero_snap_dict[server_member_id] = hero_snap
        tb_battle_hero_dict = self.construct_tb_battle_hero_dict(hero_snap_dict)
        tb_battle_boss = self.construct_tb_battle_boss(team_boss_do.doc.second_step)
        # 最后save
        data_context.save()
        data_context.unlock()
        return server_group_id, server_user_id, excp.ExceptionSuccess.code, part_key, team_boss_do.doc, team_do.doc, tb_battle_hero_dict, tb_battle_boss

    def TeamBossBattleRealStart(self, server_group_id, team_id, battle_unique_id, real_start_time, end_time):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        team_boss_do = TeamBossDo.TryLock(500)(data_context, team_id)
        if not team_boss_do.is_new and team_boss_do.doc.second_step and team_boss_do.doc.second_step.battle_unique_id == battle_unique_id:
            team_boss_do.doc.end_time = max(end_time, team_boss_do.doc.end_time)
            team_boss_do.doc.second_step.battle_real_start_time = real_start_time
            team_boss_do.doc.second_step.end_time = end_time
            team_boss_do.update()
            data_context.save()
            data_context.unlock()
            return True, team_id, battle_unique_id, real_start_time, end_time
        return False, team_id, battle_unique_id, real_start_time, end_time

    def TeamBossBattleTimeout(self, server_group_id, team_id, team_boss_unique_id, battle_unique_id, cur_hp):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        team_boss_do = TeamBossDo.TryLock(500)(data_context, team_id)
        if team_boss_do.doc.unique_id == team_boss_unique_id and team_boss_do.doc.second_step.battle_unique_id == battle_unique_id:
            # team_boss_do.doc.second_step.part_dict[team_boss_do.doc.second_step.attack_part].cur_hp = cur_hp
            team_boss_do.doc.second_step.attack_part = None
            team_boss_do.doc.second_step.battle_start_time = 0
            team_boss_do.doc.second_step.battle_real_start_time = 0
            team_boss_do.doc.second_step.battle_end_time = 0
            team_boss_do.update()
            data_context.save()
            data_context.unlock()
            return True, server_group_id, team_id, team_boss_unique_id, battle_unique_id, cur_hp
        return False, server_group_id, team_id, team_boss_unique_id, battle_unique_id, cur_hp

    def TeamBossBattleFinish(self, server_group_id, team_id, team_boss_unique_id, battle_unique_id, member_id_list, server_leader_id):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        team_boss_do = TeamBossDo.TryLock(500)(data_context, team_id)
        if team_boss_do.doc.unique_id == team_boss_unique_id and team_boss_do.doc.second_step.battle_unique_id == battle_unique_id:
            team_boss_do.doc.second_step.part_dict[team_boss_do.doc.second_step.attack_part].is_finish = True
            team_boss_do.doc.second_step.part_dict[team_boss_do.doc.second_step.attack_part].cur_hp = 0
            team_boss_do.doc.second_step.attack_part = None
            team_boss_do.doc.second_step.battle_start_time = 0
            team_boss_do.doc.second_step.battle_real_start_time = 0
            team_boss_do.doc.second_step.battle_end_time = 0
            if team_boss_do.all_part_finish():
                # 所有部位已完成,
                try:
                    team_boss_do.doc.second_step.is_finish = True
                    if team_boss_do.doc.func_type == TEAM_FUNC_TYPE_BOSS_RAID:
                        leader_server, leader_id = get_server_and_user_id(server_leader_id)
                        user_raid_do = UserRaidDo(instant_box.data_context, leader_id, leader_server)
                        user_raid_do.finish_raid()
                    reward_conf = master_team_boss_reward_map_inst.get_item(team_boss_do.doc.boss_key)
                    leader_reward_dict = master_team_boss_reward_inst.get_reward_dict(reward_conf.leader_reward_key)
                    member_reward_dict = master_team_boss_reward_inst.get_reward_dict(reward_conf.member_reward_key)
                    reward_result_dict = {}
                    for server_member_id in member_id_list:
                        if server_member_id == server_leader_id:
                            reward_dict = leader_reward_dict
                        else:
                            reward_dict = member_reward_dict
                        mem_server, mem_id = get_server_and_user_id(server_member_id)
                        mem_user_raid_do = UserRaidDo.TryLock(500)(instant_box.data_context, mem_id, mem_server)
                        can_reward = mem_user_raid_do.add_reward_times(instant_box.time_current)
                        reward_result_dict[server_member_id] = can_reward
                        if reward_dict and can_reward:
                            member_server_id, member_id = get_server_and_user_id(server_member_id)
                            # 邮件给奖励
                            MailBo(instant_box.data_context).create_mail('ALPHA_TEAM_BOSS_FINISH_REWARD', member_id, master_constants_inst.get_string('MailSystemID'),
                                                                         team_boss_do.doc.boss_key, instant_box.time_current, reward_dict, None, None, member_server_id)
                    team_boss_do.update()
                    data_context.save()
                    data_context.unlock()
                    return True, server_group_id, member_id_list, reward_result_dict, server_leader_id, leader_reward_dict, member_reward_dict
                except Exception as e:
                    logger.GetLog().error('team battle finish, give reward catch an error : %s, %s, %s, %s' % (team_boss_do.doc.boss_key, member_id_list,
                                                                                                               server_leader_id, e))
            team_boss_do.update()
            data_context.save()
            data_context.unlock()
            return True, server_group_id, member_id_list
        return False, server_group_id

    def TeamBossBattleFail(self, server_group_id, team_id, team_boss_unique_id, battle_unique_id):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        team_boss_do = TeamBossDo.TryLock(500)(data_context, team_id)
        if team_boss_do.doc.unique_id == team_boss_unique_id and team_boss_do.doc.second_step.battle_unique_id == battle_unique_id:
            team_boss_do.doc.second_step.attack_part = None
            team_boss_do.doc.second_step.battle_start_time = 0
            team_boss_do.doc.second_step.battle_real_start_time = 0
            team_boss_do.doc.second_step.battle_end_time = 0
            team_boss_do.update()
            data_context.save()
            data_context.unlock()
            return True, server_group_id, team_id, team_boss_unique_id, battle_unique_id
        return False, server_group_id, team_id, team_boss_unique_id, battle_unique_id

    def DoCheckJoinFortWarBattle(self, server_group_id, server_user_id, point_id):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.server_selected, user_id = get_server_and_user_id(server_user_id)
        instant_box.data_context = DataContext()
        # 检查是否有公会
        user_clan_do_reader = UserClanDo.Reader()(instant_box.data_context, user_id, instant_box.server_selected)
        if user_clan_do_reader.is_new or user_clan_do_reader.doc.clan_id is None:
            return server_group_id, server_user_id, excp.ExceptionClanIdIsNone.code
        # 检查公会是否有报名
        register_do_reader = AlphaFortWarRegisterDo.Reader()(instant_box.data_context)
        if not register_do_reader.is_clan_registered(user_clan_do_reader.doc.clan_id):
            return server_group_id, server_user_id, excp.ExceptionNotRegisterAlphaFortWar.code
        # 检查是否在还在战斗阶段
        if AlphaFortWarStepDo.Reader()(instant_box.data_context).step != ALPHA_FORT_WAR_STEP_ONGOING:
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarNotBattlePeriod.code
        # 是否是幸运公会
        match_do_reader = AlphaFortWarMatchDo.Reader()(instant_box.data_context)
        if user_clan_do_reader.doc.clan_id not in match_do_reader.doc.match_dict or not match_do_reader.doc.match_dict[user_clan_do_reader.doc.clan_id]:
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarLuckyClan.code
        # 拿到敌人公会id
        enemy_clan_id = match_do_reader.doc.match_dict[user_clan_do_reader.doc.clan_id]
        # 检查是否已打完
        fort_war_clan_doc = AlphaFortWarClanDo.Reader()(instant_box.data_context, enemy_clan_id).doc
        if fort_war_clan_doc.point_dict[point_id].rest_count <= 0:
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarPointFinish.code
        # 检查是否已开放
        if point_id == ALPHA_FORT_WAR_POINT_ID_THRONE:
            is_pre_finish = True
            for k, info in fort_war_clan_doc.point_dict.iteritems():
                if k in ALPHA_FORT_WAR_STEP2_POINT_ID_LIST and info.rest_count > 0:
                    is_pre_finish = False
                    break
            if not is_pre_finish:
                return server_group_id, server_user_id, excp.ExceptionAlphaFortWarPreNotFinish.code
        # 检查是否在个人战斗冷却中
        fort_war_user_do = AlphaFortWarUserDo(instant_box.data_context, user_id, instant_box.server_selected)
        cur_time = time.time()
        if fort_war_user_do.is_in_frozen_time(cur_time, point_id):
            instant_box.data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarUserFrozenTime.code
        conf_str = master_constants_inst.get_string('aofei_fort_war_step_start_time')
        conf_list = conf_str.split('|')
        end_time = int((cur_time - time.timezone) / 86400) * 86400 + time.timezone + int(conf_list[3])
        attack_time = cur_time + master_constants_inst.get_int('aofei_fort_war_gate_battle_time_limit') if point_id == ALPHA_FORT_WAR_POINT_ID_GATE else \
            master_constants_inst.get_int('aofei_fort_war_throne_battle_time_limit')
        fort_war_user_do.update_attack_data(attack_time, point_id)
        try:
            fort_war_clan_do = AlphaFortWarClanDo.TryLock(1000)(instant_box.data_context, user_clan_do_reader.doc.clan_id)
            fort_war_clan_do.append_attend_user(server_user_id)
        except:
            logger.GetLog().warn('user attend alpha fort war update attend but lock fail : %s' % server_user_id)
        instant_box.data_context.save()
        instant_box.data_context.unlock()
        return server_group_id, server_user_id, excp.ExceptionSuccess.code, user_clan_do_reader.doc.clan_id, enemy_clan_id, point_id, \
            fort_war_clan_doc.point_dict[point_id].total_count, fort_war_clan_doc.point_dict[point_id].rest_count, end_time

    def FortWarBattleWriteBack(self, server_group_id, self_clan_id, enemy_clan_id, battle_unique_id, point_id, rest_hp, user_damage_dict, last_attack_server_user_id=None):
        logger.GetLog().debug('fort war write back : %s, %s, %s, %s' % (self_clan_id, enemy_clan_id, point_id, rest_hp))
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.server_selected = get_clan_server_id(enemy_clan_id)
        instant_box.data_context = DataContext()
        # 先更新数据
        try:
            enemy_fort_war_clan_do = AlphaFortWarClanDo.TryLock(1000)(instant_box.data_context, enemy_clan_id)      # 此处使用try lock
            if is_same_date(instant_box.time_current, enemy_fort_war_clan_do.doc.result_time, master_constants_inst.get_number('GlobalResetTimestamp')):
                # 已结算
                return server_group_id, battle_unique_id, enemy_fort_war_clan_do.doc.result == ALPHA_FORT_WAR_RESULT_WIN
            else:
                enemy_fort_war_clan_do.update_point_rest_count(point_id, rest_hp, instant_box.time_current, last_attack_server_user_id)
                instant_box.data_context.save()
                instant_box.data_context.unlock()
        except Exception as e:
            logger.GetLog().warn('fort war battle write back fail : %s, %s, %s, %s, %s' % (enemy_clan_id, point_id, rest_hp, user_damage_dict, last_attack_server_user_id))
            instant_box.data_context.unlock()

        # 检查是否是据点完成结算
        if point_id == ALPHA_FORT_WAR_POINT_ID_THRONE and rest_hp == 0:
            instant_box.data_context = DataContext()
            # 水晶完成, 给奖励
            try:
                self_fort_war_clan_do = AlphaFortWarClanDo.TryLock(1000)(instant_box.data_context, self_clan_id)  # 此处使用try lock
                enemy_fort_war_clan_do = AlphaFortWarClanDo.TryLock(1000)(instant_box.data_context, enemy_clan_id)  # 此处使用try lock
                if not is_same_date(instant_box.time_current, enemy_fort_war_clan_do.doc.result_time, master_constants_inst.get_number('GlobalResetTimestamp')):
                    self_fort_war_clan_do.update_result(ALPHA_FORT_WAR_RESULT_WIN, instant_box.time_current)
                    enemy_fort_war_clan_do.update_result(ALPHA_FORT_WAR_RESULT_LOSE, instant_box.time_current)
                    group_no = self_fort_war_clan_do.doc.group_no
                    weekend = is_weekend(instant_box.time_current)
                    win_reward_dict = master_alpha_fort_war_battle_reward_inst.get_reward_dict(group_no, ALPHA_FORT_WAR_BATTLE_REWARD_WIN, weekend)
                    lose_reward_dict = master_alpha_fort_war_battle_reward_inst.get_reward_dict(group_no, ALPHA_FORT_WAR_BATTLE_REWARD_LOSE, weekend)
                    for self_attend_user in self_fort_war_clan_do.doc.attend_user_list:
                        sid, uid = get_server_and_user_id(self_attend_user)
                        MailBo(instant_box.data_context).create_mail('ALPHA_FORT_WAR_BATTLE_WIN_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                     '', instant_box.time_current, win_reward_dict, None, None, sid)

                    for enemy_attend_user in enemy_fort_war_clan_do.doc.attend_user_list:
                        sid, uid = get_server_and_user_id(enemy_attend_user)
                        MailBo(instant_box.data_context).create_mail('ALPHA_FORT_WAR_BATTLE_LOSE_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                     '', instant_box.time_current, lose_reward_dict, None, None, sid)

                    # 给玩家最后一击奖励
                    gate_reward_dict = master_alpha_fort_war_battle_reward_inst.get_reward_dict(group_no, ALPHA_FORT_WAR_BATTLE_REWARD_GATE_LAST, weekend)
                    throne_reward_dict = master_alpha_fort_war_battle_reward_inst.get_reward_dict(group_no, ALPHA_FORT_WAR_BATTLE_REWARD_THRONE_LAST, weekend)
                    if self_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_GATE].last_attack_server_user_id:
                        sid, uid = get_server_and_user_id(self_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_GATE].last_attack_server_user_id)
                        MailBo(instant_box.data_context).create_mail('ALPHA_FORT_WAR_GATE_LAST_ATTACK_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                     '', instant_box.time_current, gate_reward_dict, None, None, sid)
                    if self_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_THRONE].last_attack_server_user_id:
                        sid, uid = get_server_and_user_id(self_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_THRONE].last_attack_server_user_id)
                        MailBo(instant_box.data_context).create_mail('ALPHA_FORT_WAR_THRONE_LAST_ATTACK_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                     '', instant_box.time_current, throne_reward_dict, None, None, sid)
                    if enemy_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_GATE].last_attack_server_user_id:
                        sid, uid = get_server_and_user_id(enemy_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_GATE].last_attack_server_user_id)
                        MailBo(instant_box.data_context).create_mail('ALPHA_FORT_WAR_GATE_LAST_ATTACK_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                     '', instant_box.time_current, gate_reward_dict, None, None, sid)
                    if enemy_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_THRONE].last_attack_server_user_id:
                        sid, uid = get_server_and_user_id(enemy_fort_war_clan_do.doc.point_dict[ALPHA_FORT_WAR_POINT_ID_THRONE].last_attack_server_user_id)
                        MailBo(instant_box.data_context).create_mail('ALPHA_FORT_WAR_THRONE_LAST_ATTACK_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                     '', instant_box.time_current, throne_reward_dict, None, None, sid)
                    instant_box.data_context.save()
                    instant_box.data_context.unlock()
            except:
                logger.GetLog().error('fort war battle finish, give reward catch an error : %s, %s' % (self_clan_id, enemy_clan_id))
                instant_box.data_context.unlock()

    def FortWarUpdateBattleUser(self, server_group_id, enemy_clan_id, point_id, battle_user_count, leave_server_user_id=None):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.server_selected = get_clan_server_id(enemy_clan_id)
        instant_box.data_context = DataContext()
        # 更新数据
        try:
            fort_war_clan_do = AlphaFortWarClanDo.TryLock(1000)(instant_box.data_context, enemy_clan_id)  # 此处使用try lock
            fort_war_clan_do.update_point_battle_user_count(point_id, battle_user_count)
            if leave_server_user_id:
                server_id, user_id = get_server_and_user_id(leave_server_user_id)
                fort_war_user_do = AlphaFortWarUserDo(instant_box.data_context, user_id, server_id)
                fort_war_user_do.update_attack_time_only(instant_box.time_current)
            instant_box.data_context.save()
            instant_box.data_context.unlock()
        except Exception as e:
            logger.GetLog().warn('fort war battle write back fail FortWarUpdateBattleUser: %s, %s, %s' % (enemy_clan_id, point_id, battle_user_count))
            instant_box.data_context.unlock()

    def DoCheckJoinFortBattle(self, server_group_id, server_user_id, field_id, block_id, point_id):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.server_selected, user_id = get_server_and_user_id(server_user_id)
        instant_box.data_context = DataContext()
        # 检查point_id是否正常
        if point_id != FORT_WAR_POINT_ID_GATE and point_id != FORT_WAR_POINT_ID_THRONE:
            return server_group_id, server_user_id, excp.ExceptionInvalidParameter.code
        # 检查是否有公会
        user_clan_do_reader = UserClanDo.Reader()(instant_box.data_context, user_id, instant_box.server_selected)
        if not user_clan_do_reader.doc.clan_id:
            return server_group_id, server_user_id, excp.ExceptionClanIdIsNone.code
        # 检查当前状态
        bf_status = BattleFieldSeasonDo(instant_box.data_context, instant_box.time_current).get_season_status()
        if bf_status.season_key != BF_STEP_BATTLE:
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarNotBattlePeriod.code
        # 检查是否是自己公会战斗
        block_reader_do = BattleFieldBlockDo.Reader()(instant_box.data_context, bf_status.season_key, field_id, block_id)
        if block_reader_do.doc.fort_war_clan_id != user_clan_do_reader.doc.clan_id or not block_reader_do.is_fort_in_battle(instant_box.time_current):
            return server_group_id, server_user_id, excp.ExceptionClanNotFortBattle.code
        # 检查是否已完结
        fort_defense_reader_do = BattleFieldFortDefenseDo.Reader()(instant_box.data_context, bf_status.season_key, field_id, block_id)
        if fort_defense_reader_do.doc.point_detail_dict[point_id].rest_count <= 0:
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarPointFinish.code
        # 检查前置是否完成
        if point_id == FORT_WAR_POINT_ID_THRONE:
            is_pre_finish = True
            for k, info in fort_defense_reader_do.doc.point_detail_dict.iteritems():
                if k in FORT_WAR_STEP2_POINT_ID_LIST and info.rest_count > 0:
                    is_pre_finish = False
                    break
            if not is_pre_finish:
                return server_group_id, server_user_id, excp.ExceptionAlphaFortWarPreNotFinish.code
        # 检查自己是否在冷却中
        try:
            bf_user_do = BattleFieldUserDo.TryLock(1000)(instant_box.time_current, bf_status.season_key, user_id, instant_box.server_selected)
        except:
            return server_group_id, server_user_id, excp.ExceptionBattleFieldBusyAndTryLate.code
        if bf_user_do.is_in_frozen_time(instant_box.time_current, block_id, point_id):
            return server_group_id, server_user_id, excp.ExceptionAlphaFortWarUserFrozenTime.code
        # 检查完毕
        bf_user_do.update_attack_data(instant_box, block_id, point_id)
        instant_box.data_context.save()
        instant_box.data_context.unlock()
        return server_group_id, server_user_id, excp.ExceptionSuccess.code, field_id, block_id, point_id, \
            block_reader_do.doc.clan_id, block_reader_do.doc.fort_war_clan_id, \
            fort_defense_reader_do.doc.point_detail_dict[point_id].total_count, \
            fort_defense_reader_do.doc.point_detail_dict[point_id].rest_count,\
            block_reader_do.doc.fort_war_end_time

    def FortBattleWriteBack(self, server_group_id, battle_unique_id, field_id, block_id, point_id, defense_clan_id, attack_clan_id,
                            rest_hp, user_damage_dict, last_attack_server_user_id=None):
        logger.GetLog().debug('fort battle write back : %s, %s, %s, %s' % (field_id, block_id, point_id, rest_hp))
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.server_selected = None
        instant_box.data_context = DataContext()
        # 先更新数据
        try:
            bf_status = BattleFieldSeasonDo(instant_box.data_context, instant_box.time_current).get_season_status()
            bf_block_do = BattleFieldBlockDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, field_id, block_id)  # 此处使用try lock
            bf_fort_defense_do = BattleFieldFortDefenseDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, field_id, block_id)
        except Exception as e:
            logger.GetLog().warn('fort battle write back fail : %s, %s, %s, %s, %s, %s, %s, %s' %
                                 (field_id, block_id, defense_clan_id, attack_clan_id, point_id, rest_hp, user_damage_dict, last_attack_server_user_id))
            instant_box.data_context.unlock()
            return

        if bf_block_do.doc.fort_war_clan_id == attack_clan_id and bf_block_do.doc.fort_war_end_time > instant_box.time_current:
            bf_fort_defense_do.update_point_rest_count(point_id, rest_hp, instant_box.time_current, last_attack_server_user_id)
        elif bf_block_do.doc.clan_id == attack_clan_id:
            return server_group_id, battle_unique_id, ALPHA_FORT_WAR_RESULT_WIN
        else:
            return server_group_id, battle_unique_id, ALPHA_FORT_WAR_RESULT_LOSE

        defense_clan_id = bf_block_do.doc.clan_id
        # 检查是否是据点完成结算
        if point_id == FORT_WAR_POINT_ID_THRONE and rest_hp == 0:
            # 水晶完成
            instant_box.data_context = DataContext()
            # 水晶完成, 更改区块数据, 区块防守数据, 玩家布阵数据,
            try:
                if defense_clan_id:
                    # 有公会, 删除原有公会拥有的block
                    bf_defense_clan_do = BattleFieldClanDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, defense_clan_id)
                    if not bf_defense_clan_do.is_new:
                        bf_defense_clan_do.remove_own_block(field_id, block_id)
                # 新公会增加block
                bf_attack_clan_do = BattleFieldClanDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, attack_clan_id)
                if not bf_attack_clan_do.is_new:
                    bf_attack_clan_do.add_own_block(field_id, block_id)
                # 给玩家最后一击奖励
                gate_reward_dict = master_bf_battle_reward_inst.get_reward_dict(field_id, FORT_BATTLE_REWARD_GATE_LAST)
                throne_reward_dict = master_bf_battle_reward_inst.get_reward_dict(field_id, FORT_BATTLE_REWARD_THRONE_LAST)

                if bf_fort_defense_do.doc.point_detail_dict[FORT_WAR_POINT_ID_GATE].last_attack_server_user_id:
                    sid, uid = get_server_and_user_id(bf_fort_defense_do.doc.point_detail_dict[ALPHA_FORT_WAR_POINT_ID_GATE].last_attack_server_user_id)
                    MailBo(instant_box.data_context).create_mail('BF_FORT_BATTLE_GATE_LAST_ATTACK_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                 '{0},{1}'.format(field_id, block_id), instant_box.time_current, gate_reward_dict, None, None, sid)
                if bf_fort_defense_do.doc.point_detail_dict[FORT_WAR_POINT_ID_THRONE].last_attack_server_user_id:
                    sid, uid = get_server_and_user_id(bf_fort_defense_do.doc.point_detail_dict[FORT_WAR_POINT_ID_THRONE].last_attack_server_user_id)
                    MailBo(instant_box.data_context).create_mail('BF_FORT_BATTLE_THRONE_LAST_ATTACK_REWARD', uid, master_constants_inst.get_string('MailSystemID'),
                                                                 '{0},{1}'.format(field_id, block_id), instant_box.time_current, throne_reward_dict, None, None, sid)
                # 更改block的拥有公会
                bf_block_do.change_block_clan_id(attack_clan_id, instant_box.time_current)
                # 重置fort defense 数据
                bf_fort_defense_do.reset_data_all()
                instant_box.data_context.save()
                instant_box.data_context.unlock()
            except:
                logger.GetLog().error('fort battle finish, update data catch an error : %s, %s, %s, %s, %s' % (field_id, block_id, point_id,
                                                                                                               defense_clan_id, attack_clan_id))
                instant_box.data_context.unlock()

        # 处理战斗日志
        if rest_hp == 0:
            instant_box.data_context = DataContext()
            try:
                # 攻破据点日志
                attack_clan_name = ClanDo.Reader()(instant_box.data_context, attack_clan_id).doc.name
                defense_clan_name = None
                if defense_clan_id:
                    bf_defense_clan_do = BattleFieldClanDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, defense_clan_id)
                    bf_defense_clan_do.add_log(BF_CLAN_LOG_DEF_FORT_POINT_FAIL, instant_box.time_current, [attack_clan_name, point_id])
                    if point_id == FORT_WAR_POINT_ID_THRONE:
                        bf_defense_clan_do.add_log(BF_CLAN_LOG_DEF_FORT_FAIL, instant_box.time_current, [attack_clan_name])
                    defense_clan_name = ClanDo.Reader()(instant_box.data_context, bf_block_do.doc.clan_id).doc.name
                bf_attack_clan_do = BattleFieldClanDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, attack_clan_id)
                bf_attack_clan_do.add_log(BF_CLAN_LOG_ATK_FORT_POINT_SUCCESS, instant_box.time_current, [defense_clan_name, point_id])
                # 检查是否是完成要塞战
                if point_id == FORT_WAR_POINT_ID_THRONE:
                    bf_attack_clan_do.add_log(BF_CLAN_LOG_ATK_FORT_SUCCESS, instant_box.time_current, [defense_clan_name])
                instant_box.data_context.save()
                instant_box.data_context.unlock()
            except:
                logger.GetLog().warn('fort battle clan log fail : %s, %s, %s' % (attack_clan_id, bf_block_do.doc.clan_id, point_id))
                instant_box.data_context.unlock()

    def FortBattleUpdateBattleUser(self, server_group_id, field_id, block_id, point_id, battle_user_count):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.server_selected = None
        instant_box.data_context = DataContext()
        # 更新数据
        try:
            bf_status = BattleFieldSeasonDo(instant_box.data_context, instant_box.time_current).get_season_status()
            fort_defense_do = BattleFieldFortDefenseDo.TryLock(1000)(instant_box.data_context, bf_status.season_key, field_id, block_id)  # 此处使用try lock
            fort_defense_do.update_point_battle_user_count(point_id, battle_user_count)
            instant_box.data_context.save()
            instant_box.data_context.unlock()
        except Exception as e:
            logger.GetLog().warn('fort battle write back fail FortWarUpdateBattleUser: %s, %s, %s, %s' % (field_id, block_id, point_id, battle_user_count))
            instant_box.data_context.unlock()

    # ===============================================================
    # ============ internal functions ============
    # ===============================================================
    def construct_tb_battle_hero_dict(self, hero_snap_dict):
        unit_id = 1000
        battle_hero_dict = {}
        for server_user_id, hero_snap in hero_snap_dict.iteritems():
            battle_hero = TeamBossBattleUnitHero()
            battle_hero.hero_snap = hero_snap
            battle_hero.combatant_data = convert_hero_snap_to_combatant_data(hero_snap)
            battle_hero.transform_combatant_data = convert_hero_snap_to_transform_combatant_data(hero_snap)
            if battle_hero.combatant_data:
                battle_hero.combatant_data.id = unit_id
                if battle_hero.transform_combatant_data:
                    battle_hero.transform_combatant_data.id = unit_id
            battle_hero_dict[server_user_id] = battle_hero
            unit_id += 1
        return battle_hero_dict

    def construct_tb_battle_boss(self, second_step):
        unit_id = 5000
        battle_boss = TeamBossBattleUnitBoss()
        part_key = second_step.attack_part
        battle_boss.combatant_data = convert_team_boss_to_combatant_data(part_key, second_step.part_dict[part_key].cur_hp, second_step.part_dict[part_key].max_hp)
        battle_boss.combatant_data.id = unit_id
        for part_info in second_step.part_dict.itervalues():
            if part_info.is_finish:
                battle_boss.dead_part_list.append(part_info.part_key)
        unit_id += 1
        return battle_boss


# 构造战斗数据相关函数
def convert_hero_snap_to_combatant_data(hero_snap):
    combat = cal_hero_combatant(hero_snap.class_key, hero_snap.level, hero_snap.equipment, hero_snap.equipment_box, hero_snap.mastery_group_list)
    combat_data = make_combatant_data(combat)
    return combat_data


def convert_hero_snap_to_transform_combatant_data(hero_snap):
    if hero_snap.equipped_transform and hero_snap.equipped_transform.keys()[0]:
        trans_combat = cal_transform_combatant(hero_snap.equipped_transform.keys()[0], hero_snap.class_key, hero_snap.equipped_transform.values()[0], hero_snap.level,
                                               hero_snap.equipment, hero_snap.equipment_box, hero_snap.mastery_group_list)
        trans_combat_data = make_combatant_data(trans_combat)
        return trans_combat_data
    return None


def convert_team_boss_to_combatant_data(boss_key, cur_hp, max_hp):
    combat = cal_team_boss_combatant(boss_key)
    combat_data = make_combatant_data(combat)
    combat_data.default_status.max_hp = max_hp
    combat_data.default_status.cur_hp = cur_hp
    return combat_data


def cal_hero_combatant(combat_key, lv, equipment_dict, equipment_box_dict, mastery_group_dict=None):
    if not combat_key or lv <= 0:
        logger.GetLog().error('combatant key : %s, lv : %s' % (combat_key, lv))
        return None

    # 基础属性
    combatant_conf = master_combatants_inst.get(combat_key)
    if not combatant_conf:
        logger.GetLog().error('combatant key : %s config is none' % combat_key)
        return None
    combatant_base_conf = master_combatants_base_inst.get(combatant_conf.base)
    if not combatant_base_conf or not combatant_base_conf.is_hero_group():
        logger.GetLog().error('combatant base conf is none or is not hero group: %s' % combat_key)
        return None
    combatant = combatant_conf.clone_to_combatant()
    combatant.level = lv
    combatant.aggro = combatant_base_conf.aggro

    # 随等级成长的一级属性
    factor_conf = master_level_factor_inst.get_item(combatant_base_conf.c_class_d)
    apply_lv = lv - 1
    combatant.str += (apply_lv * factor_conf.str)
    combatant.dex += (apply_lv * factor_conf.dex)
    combatant.int += (apply_lv * factor_conf.int)
    combatant.con += (apply_lv * factor_conf.con)

    # 二级属性转化
    stat_mod_conf_list = master_stat_mod_inst.get_row_list_by_group_rarity(CombatantGroupDef.COMBATANT_GROUP_HERO, None)
    if stat_mod_conf_list:
        for stat_mod_conf in stat_mod_conf_list:
            val1 = get_stat_factor_value(stat_mod_conf.stat_1, combatant, combatant_base_conf.factor)
            val2 = get_stat_factor_value(stat_mod_conf.stat_2, combatant, combatant_base_conf.factor)
            conf_val1 = stat_mod_conf.val_1 if stat_mod_conf.val_1 else 0.0
            conf_val2 = stat_mod_conf.val_2 if stat_mod_conf.val_2 else 0.0
            val = round(val1 * conf_val1 + val2 * conf_val2)
            if stat_mod_conf.result_stat == StatDef.STAT_DEF_P_ATK:
                combatant.p_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_M_ATK:
                combatant.m_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_HP:
                combatant.hp += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_P_DEF:
                combatant.p_def += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_RES:
                combatant.res += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_PEN:
                combatant.pen += val
            else:
                logger.GetLog().warn('------------------------ unsupported stat : %s' % stat_mod_conf.result_stat)

    # 记录当前的二级属性值
    p_atk_by_mastery = combatant.p_atk
    m_atk_by_mastery = combatant.m_atk
    hp_by_mastery = combatant.hp
    p_def_by_mastery = combatant.p_def
    res_by_mastery = combatant.res
    pen_by_mastery = combatant.pen

    # 星云属性
    if mastery_group_dict:
        # 百分比属性
        percent_stat_dict = {}
        if MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO in mastery_group_dict:
            for k, v in mastery_group_dict[MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO].mastery_list.iteritems():
                star_group = k
                level = v
                mastery_info = master_mastery_stat_inst.get_by_index('get_stat', MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO, star_group, level)[0]
                cal_mastery_stat_by_multiply(mastery_info, percent_stat_dict)

        if MasteryGroupIdDefine.MASTERY_GROUP_ID_CONTENTS in mastery_group_dict:
            for k, v in mastery_group_dict[MasteryGroupIdDefine.MASTERY_GROUP_ID_CONTENTS].mastery_list.iteritems():
                star_group = k
                level = v
                mastery_info = master_mastery_stat_inst.get_by_index('get_stat', MasteryGroupIdDefine.MASTERY_GROUP_ID_CONTENTS, star_group, level)[0]
                if mastery_info and mastery_info.property and mastery_info.property == 'pve':
                    cal_mastery_stat_by_multiply(mastery_info, percent_stat_dict)

        for stat_key, stat_value in percent_stat_dict.iteritems():
            if stat_value != 0.0:
                cal_option_by_multiply(stat_key, stat_value, combatant)

    # 记录星云属性导致的属性增加值
    p_atk_by_mastery = combatant.p_atk - p_atk_by_mastery
    m_atk_by_mastery = combatant.m_atk - m_atk_by_mastery
    hp_by_mastery = combatant.hp - hp_by_mastery
    p_def_by_mastery = combatant.p_def - p_def_by_mastery
    res_by_mastery = combatant.res - res_by_mastery
    pen_by_mastery = combatant.pen - pen_by_mastery

    # 将受星云属性影响的属性值重置
    ori_combatant = combatant_conf.clone_to_combatant()
    combatant.p_atk = ori_combatant.p_atk
    combatant.m_atk = ori_combatant.m_atk
    combatant.hp = ori_combatant.hp
    combatant.p_def = ori_combatant.p_def
    combatant.res = ori_combatant.res
    combatant.pen = ori_combatant.pen

    # 装备属性
    if equipment_dict:
        set_dict = {}
        weapon_strengthen = 0
        other_strengthen = 0
        other_count = 0
        for equip_type, equipment in equipment_dict.iteritems():
            if equipment:
                # 强化大师相关
                if equip_type == 'weapon':
                    weapon_strengthen = equipment.strengthen
                else:
                    other_strengthen = min(equipment.strengthen, other_strengthen) if other_strengthen else equipment.strengthen
                    other_count += 1

                # 套装数量统计
                equip_conf = master_equipment_inst.get_by_item_key(equipment.class_key)
                if equip_conf.set_option:
                    if equip_conf.set_option in set_dict:
                        set_dict[equip_conf.set_option] += 1
                    else:
                        set_dict[equip_conf.set_option] = 1

                # 装备主属性计算
                pri_stat_key = equipment.primary_stat.keys()[0]
                cal_option(pri_stat_key, equipment.primary_stat[pri_stat_key], combatant)
                # 装备固定部分随机属性计算
                for pri_item in equipment.primary_option:
                    pri_option_key = pri_item.keys()[0]
                    cal_option(pri_option_key, pri_item[pri_option_key], combatant)
                # 装备随机部分随机属性计算
                if equipment.sub_option:
                    if equipment.strengthen >= 3:
                        max_count = equipment.strengthen / 3
                        option_count = min(max_count, len(equipment.sub_option))
                        for index in range(0, option_count):
                            for k, v in equipment.sub_option[index].iteritems():
                                cal_option(k, v, combatant)
        # 强化大师属性计算
        if weapon_strengthen > 0:
            for strengthen_set_info in master_equipment_strengthen_set_inst.get_by_index('get_by_type', "WEAPON", combat_key):
                if strengthen_set_info.strengthen <= weapon_strengthen:
                    cal_option(strengthen_set_info.set_option, strengthen_set_info.option_value, combatant)

        if other_strengthen > 0 and other_count >= 8:
            for strengthen_set_info in master_equipment_strengthen_set_inst.get_by_index('get_by_type', "OTHER", combat_key):
                if strengthen_set_info.strengthen <= other_strengthen:
                    cal_option(strengthen_set_info.set_option, strengthen_set_info.option_value, combatant)

        # 套装属性计算
        if len(set_dict) > 0:
            for k, v in set_dict.iteritems():
                for set_option_info in master_equipment_set_option_inst.get_by_index('get_set_options', k):
                    if set_option_info.set_option and set_option_info.option_value and v >= set_option_info.set_count:
                        cal_option(set_option_info.set_option, set_option_info.option_value, combatant)

    # 装备盒子属性计算
    if equipment_box_dict:
        for k, v in equipment_box_dict.iteritems():
            for key, status in v.stat_list.iteritems():
                master_data = master_hero_equipment_box_stat_inst.get_item(key)
                for stat, value in master_data.stat.iteritems():
                    cal_option(stat, value, combatant)

    # 星云属性计算
    if mastery_group_dict:
        if MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO in mastery_group_dict:
            for k, v in mastery_group_dict[MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO].mastery_list.iteritems():
                star_group = k
                level = v
                mastery_info = master_mastery_stat_inst.get_by_index('get_stat', MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO, star_group, level)[0]
                if mastery_info:
                    for stat_key, stat_value in mastery_info.factor.iteritems():
                        cal_option(stat_key, stat_value, combatant)

    # 重新计算二级属性转化
    if stat_mod_conf_list:
        for stat_mod_conf in stat_mod_conf_list:
            val1 = get_stat_factor_value(stat_mod_conf.stat_1, combatant, combatant_base_conf.factor)
            val2 = get_stat_factor_value(stat_mod_conf.stat_2, combatant, combatant_base_conf.factor)
            conf_val1 = stat_mod_conf.val_1 if stat_mod_conf.val_1 else 0.0
            conf_val2 = stat_mod_conf.val_2 if stat_mod_conf.val_2 else 0.0
            val = round(val1 * conf_val1 + val2 * conf_val2)
            if stat_mod_conf.result_stat == StatDef.STAT_DEF_P_ATK:
                combatant.p_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_M_ATK:
                combatant.m_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_HP:
                combatant.hp += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_P_DEF:
                combatant.p_def += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_RES:
                combatant.res += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_PEN:
                combatant.pen += val
            else:
                logger.GetLog().warn('------------------------ unsupported stat : %s' % stat_mod_conf.result_stat)

    # 属性加上星云属性
    combatant.p_atk += p_atk_by_mastery
    combatant.m_atk += m_atk_by_mastery
    combatant.hp += hp_by_mastery
    combatant.p_def += p_def_by_mastery
    combatant.res += res_by_mastery
    combatant.pen += pen_by_mastery

    # 养成属性处理
    hero_training_conf = master_hero_training_inst.get_by_index('get_training_info', combatant_conf.base, lv)[0]
    if hero_training_conf:
        combatant.atk_speed += (hero_training_conf.atk_speed if hero_training_conf.atk_speed else 0)
        combatant.p_atk += (hero_training_conf.p_atk if hero_training_conf.p_atk else 0)
        combatant.m_atk += (hero_training_conf.m_atk if hero_training_conf.m_atk else 0)
        combatant.hp += (hero_training_conf.hp if hero_training_conf.hp else 0)
        combatant.p_def += (hero_training_conf.p_def if hero_training_conf.p_def else 0)
        combatant.res += (hero_training_conf.res if hero_training_conf.res else 0)
        combatant.pen += (hero_training_conf.pen if hero_training_conf.pen else 0)
        combatant.cond_dec += (hero_training_conf.cond_dec if hero_training_conf.cond_dec else 0)
        combatant.cri += (hero_training_conf.cri if hero_training_conf.cri else 0)
        combatant.eva += (hero_training_conf.eva if hero_training_conf.eva else 0)

        for k, v in hero_training_conf.attr_res.iteritems():
            if k in combatant.attr_res:
                combatant.attr_res[k] += v
            else:
                combatant.attr_res[k] = v
        for k, v in hero_training_conf.cond_res:
            if k in combatant.cond_res:
                combatant.cond_res[k] += v
            else:
                combatant.cond_res[k] = v

    return combatant


def cal_transform_combatant(transform_key, combat_key, transform_stren_key, lv, equipment_dict, equipment_box_dict, mastery_group_dict=None):
    if not transform_key or lv <= 0:
        logger.GetLog().error('transform key : %s, lv : %s' % (transform_key, lv))
        return None

    # 基础属性
    combatant_conf = master_combatants_inst.get(transform_key)
    if not combatant_conf:
        logger.GetLog().error('transform key : %s config is none' % transform_key)
        return None
    combatant_base_conf = master_combatants_base_inst.get(combatant_conf.base)
    if not combatant_base_conf or not combatant_base_conf.is_hero_group():
        logger.GetLog().error('transform combatant base conf is none or is not hero group: %s' % transform_key)
        return None
    combatant = combatant_conf.clone_to_combatant()
    combatant.level = lv
    combatant.aggro = combatant_base_conf.aggro

    # 随等级成长的一级属性
    factor_conf = master_level_factor_inst.get_item(combatant_base_conf.c_class_d)
    apply_lv = lv - 1
    combatant.str += (apply_lv * factor_conf.str)
    combatant.dex += (apply_lv * factor_conf.dex)
    combatant.int += (apply_lv * factor_conf.int)
    combatant.con += (apply_lv * factor_conf.con)

    # 二级属性转化
    stat_mod_conf_list = master_stat_mod_inst.get_row_list_by_group_rarity(CombatantGroupDef.COMBATANT_GROUP_HERO)
    if stat_mod_conf_list:
        for stat_mod_conf in stat_mod_conf_list:
            val1 = get_stat_factor_value(stat_mod_conf.stat_1, combatant, combatant_base_conf.factor)
            val2 = get_stat_factor_value(stat_mod_conf.stat_2, combatant, combatant_base_conf.factor)
            conf_val1 = stat_mod_conf.val_1 if stat_mod_conf.val_1 else 0.0
            conf_val2 = stat_mod_conf.val_2 if stat_mod_conf.val_2 else 0.0
            val = round(val1 * conf_val1 + val2 * conf_val2)
            if stat_mod_conf.result_stat == StatDef.STAT_DEF_P_ATK:
                combatant.p_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_M_ATK:
                combatant.m_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_HP:
                combatant.hp += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_P_DEF:
                combatant.p_def += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_RES:
                combatant.res += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_PEN:
                combatant.pen += val
            else:
                logger.GetLog().warn('------------------------ unsupported stat : %s' % stat_mod_conf.result_stat)

    # 记录当前的二级属性值
    p_atk_by_mastery = combatant.p_atk
    m_atk_by_mastery = combatant.m_atk
    hp_by_mastery = combatant.hp
    p_def_by_mastery = combatant.p_def
    res_by_mastery = combatant.res
    pen_by_mastery = combatant.pen

    # 星云属性
    if mastery_group_dict:
        # 百分比属性
        percent_stat_dict = {}
        if MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO in mastery_group_dict:
            for k, v in mastery_group_dict[MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO].mastery_list.iteritems():
                star_group = k
                level = v
                mastery_info = master_mastery_stat_inst.get_by_index('get_stat', MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO, star_group, level)[0]
                cal_mastery_stat_by_multiply(mastery_info, percent_stat_dict)

        if MasteryGroupIdDefine.MASTERY_GROUP_ID_CONTENTS in mastery_group_dict:
            for k, v in mastery_group_dict[MasteryGroupIdDefine.MASTERY_GROUP_ID_CONTENTS].mastery_list.iteritems():
                star_group = k
                level = v
                mastery_info = master_mastery_stat_inst.get_by_index('get_stat', MasteryGroupIdDefine.MASTERY_GROUP_ID_CONTENTS, star_group, level)[0]
                if mastery_info and mastery_info.property and mastery_info.property == 'pve':
                    cal_mastery_stat_by_multiply(mastery_info, percent_stat_dict)

        for stat_key, stat_value in percent_stat_dict.iteritems():
            if stat_value != 0.0:
                cal_option_by_multiply(stat_key, stat_value, combatant)

    # 记录星云属性导致的属性增加值
    p_atk_by_mastery = combatant.p_atk - p_atk_by_mastery
    m_atk_by_mastery = combatant.m_atk - m_atk_by_mastery
    hp_by_mastery = combatant.hp - hp_by_mastery
    p_def_by_mastery = combatant.p_def - p_def_by_mastery
    res_by_mastery = combatant.res - res_by_mastery
    pen_by_mastery = combatant.pen - pen_by_mastery

    # 将受星云属性影响的属性值重置
    ori_combatant = combatant_conf.clone_to_combatant()
    combatant.p_atk = ori_combatant.p_atk
    combatant.m_atk = ori_combatant.m_atk
    combatant.hp = ori_combatant.hp
    combatant.p_def = ori_combatant.p_def
    combatant.res = ori_combatant.res
    combatant.pen = ori_combatant.pen

    # 装备属性
    if equipment_dict:
        set_dict = {}
        weapon_strengthen = 0
        other_strengthen = 0
        other_count = 0
        for equip_type, equipment in equipment_dict.iteritems():
            if equipment:
                # 强化大师相关
                if equip_type == 'weapon':
                    weapon_strengthen = equipment.strengthen
                else:
                    other_strengthen = min(equipment.strengthen, other_strengthen) if other_strengthen else equipment.strengthen
                    other_count += 1

                # 套装数量统计
                equip_conf = master_equipment_inst.get_by_item_key(equipment.class_key)
                if equip_conf.set_option:
                    if equip_conf.set_option in set_dict:
                        set_dict[equip_conf.set_option] += 1
                    else:
                        set_dict[equip_conf.set_option] = 1

                # 装备主属性计算
                pri_stat_key = equipment.primary_stat.keys()[0]
                cal_option(pri_stat_key, equipment.primary_stat[pri_stat_key], combatant)
                # 装备固定部分随机属性计算
                for pri_item in equipment.primary_option:
                    pri_option_key = pri_item.keys()[0]
                    cal_option(pri_option_key, pri_item[pri_option_key], combatant)
                # 装备随机部分随机属性计算
                if equipment.sub_option:
                    if equipment.strengthen >= 3:
                        max_count = equipment.strengthen / 3
                        option_count = min(max_count, len(equipment.sub_option))
                        for index in range(0, option_count):
                            for k, v in equipment.sub_option[index].iteritems():
                                cal_option(k, v, combatant)
        # 强化大师属性计算
        if weapon_strengthen > 0:
            for strengthen_set_info in master_equipment_strengthen_set_inst.get_by_index('get_by_type', "WEAPON", combat_key):
                if strengthen_set_info.strengthen <= weapon_strengthen:
                    cal_option(strengthen_set_info.set_option, strengthen_set_info.option_value, combatant)

        if other_strengthen > 0 and other_count >= 8:
            for strengthen_set_info in master_equipment_strengthen_set_inst.get_by_index('get_by_type', "OTHER", combat_key):
                if strengthen_set_info.strengthen <= other_strengthen:
                    cal_option(strengthen_set_info.set_option, strengthen_set_info.option_value, combatant)

        # 套装属性计算
        if len(set_dict) > 0:
            for k, v in set_dict.iteritems():
                for set_option_info in master_equipment_set_option_inst.get_by_index('get_set_options', k):
                    if set_option_info.set_option and set_option_info.option_value and v >= set_option_info.set_count:
                        cal_option(set_option_info.set_option, set_option_info.option_value, combatant)

    # 装备盒子属性计算
    if equipment_box_dict:
        for k, v in equipment_box_dict.iteritems():
            for key, status in v.stat_list.iteritems():
                master_data = master_hero_equipment_box_stat_inst.get_item(key)
                for stat, value in master_data.stat.iteritems():
                    cal_option(stat, value, combatant)

    # 星云属性计算
    if mastery_group_dict:
        if MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO in mastery_group_dict:
            for k, v in mastery_group_dict[MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO].mastery_list.iteritems():
                star_group = k
                level = v
                mastery_info = master_mastery_stat_inst.get_by_index('get_stat', MasteryGroupIdDefine.MASTERY_GROUP_ID_HERO, star_group, level)[0]
                if mastery_info:
                    for stat_key, stat_value in mastery_info.factor.iteritems():
                        cal_option(stat_key, stat_value, combatant)

    # 重新计算二级属性转化
    if stat_mod_conf_list:
        for stat_mod_conf in stat_mod_conf_list:
            val1 = get_stat_factor_value(stat_mod_conf.stat_1, combatant, combatant_base_conf.factor)
            val2 = get_stat_factor_value(stat_mod_conf.stat_2, combatant, combatant_base_conf.factor)
            conf_val1 = stat_mod_conf.val_1 if stat_mod_conf.val_1 else 0.0
            conf_val2 = stat_mod_conf.val_2 if stat_mod_conf.val_2 else 0.0
            val = round(val1 * conf_val1 + val2 * conf_val2)
            if stat_mod_conf.result_stat == StatDef.STAT_DEF_P_ATK:
                combatant.p_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_M_ATK:
                combatant.m_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_HP:
                combatant.hp += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_P_DEF:
                combatant.p_def += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_RES:
                combatant.res += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_PEN:
                combatant.pen += val
            else:
                logger.GetLog().warn('------------------------ unsupported stat : %s' % stat_mod_conf.result_stat)

    # 属性加上星云属性
    combatant.p_atk += p_atk_by_mastery
    combatant.m_atk += m_atk_by_mastery
    combatant.hp += hp_by_mastery
    combatant.p_def += p_def_by_mastery
    combatant.res += res_by_mastery
    combatant.pen += pen_by_mastery

    # 养成属性处理
    hero_training_conf = master_hero_training_inst.get_by_index('get_training_info', combat_key, lv)[0]
    if hero_training_conf:
        combatant.atk_speed += (hero_training_conf.atk_speed if hero_training_conf.atk_speed else 0)
        combatant.p_atk += (hero_training_conf.p_atk if hero_training_conf.p_atk else 0)
        combatant.m_atk += (hero_training_conf.m_atk if hero_training_conf.m_atk else 0)
        combatant.hp += (hero_training_conf.hp if hero_training_conf.hp else 0)
        combatant.p_def += (hero_training_conf.p_def if hero_training_conf.p_def else 0)
        combatant.res += (hero_training_conf.res if hero_training_conf.res else 0)
        combatant.pen += (hero_training_conf.pen if hero_training_conf.pen else 0)
        combatant.cond_dec += (hero_training_conf.cond_dec if hero_training_conf.cond_dec else 0)
        combatant.cri += (hero_training_conf.cri if hero_training_conf.cri else 0)
        combatant.eva += (hero_training_conf.eva if hero_training_conf.eva else 0)

        for k, v in hero_training_conf.attr_res.iteritems():
            if k in combatant.attr_res:
                combatant.attr_res[k] += v
            else:
                combatant.attr_res[k] = v
        for k, v in hero_training_conf.cond_res:
            if k in combatant.cond_res:
                combatant.cond_res[k] += v
            else:
                combatant.cond_res[k] = v

    # 变身属性
    if transform_stren_key:
        trans_stren_conf = master_transform_strengthen_inst.get_item(transform_stren_key)
        if trans_stren_conf:
            combatant.atk_speed += (trans_stren_conf.atk_speed if trans_stren_conf.atk_speed else 0)
            combatant.p_atk += (trans_stren_conf.p_atk if trans_stren_conf.p_atk else 0)
            combatant.m_atk += (trans_stren_conf.m_atk if trans_stren_conf.m_atk else 0)
            combatant.hp += (trans_stren_conf.hp if trans_stren_conf.hp else 0)
            combatant.p_def += (trans_stren_conf.p_def if trans_stren_conf.p_def else 0)
            combatant.res += (trans_stren_conf.res if trans_stren_conf.res else 0)
            combatant.pen += (trans_stren_conf.pen if trans_stren_conf.pen else 0)
            combatant.cond_dec += (trans_stren_conf.cond_dec if trans_stren_conf.cond_dec else 0)
            combatant.cri += (trans_stren_conf.cri if trans_stren_conf.cri else 0)
            combatant.eva += (trans_stren_conf.eva if trans_stren_conf.eva else 0)

            for k, v in trans_stren_conf.attr_res.iteritems():
                if k in combatant.attr_res:
                    combatant.attr_res[k] += v
                else:
                    combatant.attr_res[k] = v

            for k, v in trans_stren_conf.cond_res.iteritems():
                if k in combatant.cond_res:
                    combatant.cond_res[k] += v
                else:
                    combatant.cond_res[k] = v

    return combatant


def cal_team_boss_combatant(boss_key):
    team_boss_part_conf = master_team_boss_part_inst.get_item(boss_key)
    combatant_conf = master_combatants_inst.get(team_boss_part_conf.combatant_key)
    combatant_base_conf = master_combatants_base_inst.get(combatant_conf.base)
    team_boss_training_conf = master_team_boss_training_inst.get_item(boss_key)
    if combatant_base_conf.group != CombatantGroupDef.COMBATANT_GROUP_BOSS:
        logger.GetLog().error('team boss group is not boss: %s, %s' % (boss_key, combatant_base_conf.group))
        return None
    combatant = combatant_conf.clone_to_combatant()
    combatant.level = team_boss_part_conf.level

    # 基础属性
    factor_conf = master_level_factor_inst.get_item(combatant_base_conf.c_class_d)
    apply_lv = team_boss_part_conf.level - 1 if team_boss_part_conf.level > 0 else 0
    combatant.str += (apply_lv * factor_conf.str)
    combatant.dex += (apply_lv * factor_conf.dex)
    combatant.int += (apply_lv * factor_conf.int)
    combatant.con += (apply_lv * factor_conf.con)

    # 二级属性
    stat_mod_conf_list = master_stat_mod_inst.get_row_list_by_group_rarity(combatant_base_conf.group)
    if stat_mod_conf_list:
        for stat_mod_conf in stat_mod_conf_list:
            val1 = get_stat_factor_value(stat_mod_conf.stat_1, combatant, combatant_base_conf.factor)
            val2 = get_stat_factor_value(stat_mod_conf.stat_2, combatant, combatant_base_conf.factor)
            conf_val1 = stat_mod_conf.val_1 if stat_mod_conf.val_1 else 0.0
            conf_val2 = stat_mod_conf.val_2 if stat_mod_conf.val_2 else 0.0
            val = round(val1 * conf_val1 + val2 * conf_val2)
            if stat_mod_conf.result_stat == StatDef.STAT_DEF_P_ATK:
                combatant.p_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_M_ATK:
                combatant.m_atk += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_HP:
                combatant.hp += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_P_DEF:
                combatant.p_def += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_RES:
                combatant.res += val
            elif stat_mod_conf.result_stat == StatDef.STAT_DEF_PEN:
                combatant.pen += val
            else:
                logger.GetLog().warn('------------------------ unsupported stat : %s' % stat_mod_conf.result_stat)

    # 养成属性
    if team_boss_training_conf:
        combatant.atk_speed += (team_boss_training_conf.atk_speed if team_boss_training_conf.atk_speed else 0)
        combatant.p_atk += (team_boss_training_conf.p_atk if team_boss_training_conf.p_atk else 0)
        combatant.m_atk += (team_boss_training_conf.m_atk if team_boss_training_conf.m_atk else 0)
        combatant.hp += (team_boss_training_conf.hp if team_boss_training_conf.hp else 0)
        combatant.p_def += (team_boss_training_conf.p_def if team_boss_training_conf.p_def else 0)
        combatant.res += (team_boss_training_conf.res if team_boss_training_conf.res else 0)
        combatant.pen += (team_boss_training_conf.pen if team_boss_training_conf.pen else 0)
        combatant.cond_dec += (team_boss_training_conf.cond_dec if team_boss_training_conf.cond_dec else 0)
        combatant.cri += (team_boss_training_conf.cri if team_boss_training_conf.cri else 0)
        combatant.eva += (team_boss_training_conf.eva if team_boss_training_conf.eva else 0)

        for k, v in team_boss_training_conf.attr_res.iteritems():
            if k in combatant.attr_res:
                combatant.attr_res[k] += v
            else:
                combatant.attr_res[k] = v
        for k, v in team_boss_training_conf.cond_res:
            if k in combatant.cond_res:
                combatant.cond_res[k] += v
            else:
                combatant.cond_res[k] = v

    return combatant


def cal_option(key, value, combatant):
    if key == StatDef.STAT_DEF_STR:
        combatant.str += value
    elif key == StatDef.STAT_DEF_DEX:
        combatant.dex += value
    elif key == StatDef.STAT_DEF_INT:
        combatant.int += value
    elif key == StatDef.STAT_DEF_CON:
        combatant.con += value
    elif key == StatDef.STAT_DEF_M_ATK:
        combatant.m_atk += value
    elif key == StatDef.STAT_DEF_P_ATK:
        combatant.p_atk += value
    elif key == StatDef.STAT_DEF_PEN:
        combatant.pen += value
    elif key == StatDef.STAT_DEF_ATK_SPEED:
        combatant.atk_speed += value
    elif key == StatDef.STAT_DEF_CRI:
        combatant.cri += value
    elif key == StatDef.STAT_DEF_HP:
        combatant.hp += value
    elif key == StatDef.STAT_DEF_COND_DEC:
        combatant.cond_dec += value
    elif key == StatDef.STAT_DEF_EVA:
        combatant.eva += value
    elif key == StatDef.STAT_DEF_P_DEF:
        combatant.p_def += value
    elif key == StatDef.STAT_DEF_RES:
        combatant.res += value
    elif key in [StatDef.STAT_DEF_FIRE, StatDef.STAT_DEF_WATER, StatDef.STAT_DEF_WIND, StatDef.STAT_DEF_LAND, StatDef.STAT_DEF_DARKNESS]:
        if key in combatant.attr_res:
            combatant.attr_res[key] += value
        else:
            combatant.attr_res[key] = value
    elif key in [StatDef.STAT_DEF_STUN, StatDef.STAT_DEF_SLEEP, StatDef.STAT_DEF_PETRIFY, StatDef.STAT_DEF_FREEZE, StatDef.STAT_DEF_CHARM, StatDef.STAT_DEF_BIND,
                 StatDef.STAT_DEF_TERRIFY, StatDef.STAT_DEF_SILENCE]:
        if key in combatant.cond_res:
            combatant.cond_res[key] += value
        else:
            combatant.cond_res[key] = value
    elif key == StatDef.STAT_DEF_CRI_DMG:
        combatant.cri_damage = value * 0.01
    elif key == StatDef.STAT_DEF_SKILLGAUGE:
        combatant.base_gauge = value
    elif key in [StatDef.STAT_DEF_HP_PERCENT, StatDef.STAT_DEF_M_ATK_PERCENT, StatDef.STAT_DEF_P_ATK_PERCENT, StatDef.STAT_DEF_P_DEF_PERCENT, StatDef.STAT_DEF_RES_PERCENT]:
        pass
    else:
        logger.GetLog().warn('------------------------ cal option unsupported option - key: %s, value: %s' % (key, value))


def cal_option_by_multiply(key, value, combatant):
    rate = value * 0.01
    if key == StatDef.STAT_DEF_M_ATK:
        combatant.m_atk += int(combatant.m_atk * rate)
    elif key == StatDef.STAT_DEF_P_ATK:
        combatant.p_atk += int(combatant.p_atk * rate)
    elif key == StatDef.STAT_DEF_PEN:
        combatant.pen += int(combatant.pen * rate)
    elif key == StatDef.STAT_DEF_ATK_SPEED:
        combatant.atk_speed += int(combatant.atk_speed * rate)
    elif key == StatDef.STAT_DEF_CRI:
        combatant.cri += int(combatant.cri * rate)
    elif key == StatDef.STAT_DEF_HP:
        combatant.hp += int(combatant.hp * rate)
    elif key == StatDef.STAT_DEF_COND_DEC:
        combatant.cond_dec += int(combatant.cond_dec * rate)
    elif key == StatDef.STAT_DEF_EVA:
        combatant.eva += int(combatant.eva * rate)
    elif key == StatDef.STAT_DEF_P_DEF:
        combatant.p_def += int(combatant.p_def * rate)
    elif key == StatDef.STAT_DEF_RES:
        combatant.res += int(combatant.res * rate)
    elif key == StatDef.STAT_DEF_CRI_DMG:
        combatant.cri_damage += value
    elif key == StatDef.STAT_DEF_P_IMMUNE:
        combatant.p_immune += value
    elif key == StatDef.STAT_DEF_M_IMMUNE:
        combatant.m_immune += value
    elif key == StatDef.STAT_DEF_COND_RES_ALL:
        combatant.cond_res_all += value
    elif key == StatDef.STAT_DEF_CRITICAL_PERCENT:
        combatant.cri_rate += value
    elif key == StatDef.STAT_DEF_P_ATK_PERCENT:
        combatant.p_atk += int(combatant.p_atk * value)
    elif key == StatDef.STAT_DEF_M_ATK_PERCENT:
        combatant.m_atk += int(combatant.m_atk * value)
    elif key == StatDef.STAT_DEF_P_DEF_PERCENT:
        combatant.p_def += int(combatant.p_def * value)
    elif key == StatDef.STAT_DEF_RES_PERCENT:
        combatant.res += int(combatant.res * value)
    elif key == StatDef.STAT_DEF_HP_PERCENT:
        combatant.hp += int(combatant.hp * value)
    elif key == StatDef.STAT_DEF_PVP_HP_UP_RATE:
        combatant.hp += int(combatant.hp * value)
    else:
        logger.GetLog().warn('------------------------ cal option multiply unsupported option - key: %s, value: %s' % (key, value))


def get_stat_factor_value(factor, combatant, base_factor):
    if not factor:
        return 0.0
    main_factor = base_factor.lower() if factor == StatFactorDef.STAT_FACTOR_FACTOR else factor
    if main_factor == StatFactorDef.STAT_FACTOR_STR:
        return float(combatant.str)
    elif main_factor == StatFactorDef.STAT_FACTOR_DEX:
        return float(combatant.dex)
    elif main_factor == StatFactorDef.STAT_FACTOR_INT:
        return float(combatant.int)
    elif main_factor == StatFactorDef.STAT_FACTOR_CON:
        return float(combatant.con)
    else:
        return 0.0


def cal_mastery_stat_by_multiply(mastery_info, stat_dict):
    if mastery_info and mastery_info.factor:
        for s_key, s_value in mastery_info.factor.iteritems():
            stat_value = s_value
            if s_key == "p_atk_percent":
                stat_key = StatDef.STAT_DEF_P_ATK_PERCENT
            elif s_key == "m_atk_percent":
                stat_key = StatDef.STAT_DEF_M_ATK_PERCENT
            elif s_key == "hp_percent":
                stat_key = StatDef.STAT_DEF_HP_PERCENT
            elif s_key == "p_def_percent":
                stat_key = StatDef.STAT_DEF_P_DEF_PERCENT
            elif s_key == "res_percent":
                stat_key = StatDef.STAT_DEF_RES_PERCENT
            elif s_key == "critical_percent":
                stat_key = StatDef.STAT_DEF_CRITICAL_PERCENT
            elif s_key == "critical_damage_percent":
                stat_key = StatDef.STAT_DEF_CRI_DMG
            elif s_key == "mes_res_percent":
                stat_key = StatDef.STAT_DEF_COND_RES_ALL
            elif s_key == "p_immune_percent":
                stat_key = StatDef.STAT_DEF_P_IMMUNE
            elif s_key == "m_immune_percent":
                stat_key = StatDef.STAT_DEF_M_IMMUNE
            else:
                continue
            if stat_key not in stat_dict:
                stat_dict[stat_key] = 0.0
            stat_dict[stat_key] += stat_value


def make_combatant_data(combatant):
    if not combatant:
        return None

    combatant_data = SimpleCombatantData()

    combatant_data.key = combatant.key
    combatant_data.base_key = combatant.base
    combatant_data.lv = combatant.level
    combatant_data.training = -1
    combatant_data.add_gauge = combatant.base_gauge

    combatant_data.default_status = CombatantStatus()
    combatant_data.default_status.str = combatant.str
    combatant_data.default_status.dex = combatant.dex
    combatant_data.default_status.int = combatant.int
    combatant_data.default_status.phy_atk = combatant.p_atk
    combatant_data.default_status.mag_atk = combatant.m_atk
    combatant_data.default_status.cri = combatant.cri
    combatant_data.default_status.cri_inc = combatant.cri_damage
    combatant_data.default_status.phy_pen = combatant.pen
    combatant_data.default_status.phy_def = combatant.p_def
    combatant_data.default_status.mag_res = combatant.res
    combatant_data.default_status.eva = combatant.eva
    combatant_data.default_status.cur_hp = combatant.hp
    combatant_data.default_status.max_hp = combatant.hp
    combatant_data.default_status.cond_dec = combatant.cond_dec
    combatant_data.default_status.move_speed = combatant.move_speed
    combatant_data.default_status.atk_speed = combatant.atk_speed
    combatant_data.default_status.aggro = combatant.aggro
    combatant_data.default_status.high_power = 1.0

    for attr_type in EnumAttrTypeDef.all_attr_type_list:
        if attr_type in combatant.attr_res:
            combatant_data.default_status.attr_res[attr_type] = float(combatant.attr_res[attr_type])
        else:
            combatant_data.default_status.attr_res[attr_type] = CombatantStatusConstDef.DEFAULT_ATTR_RES

    for k, v in combatant.cond_res.iteritems():
        combatant_data.default_status.mesmerize_res[k] = float(v)

    combatant_data.default_status.field_immune = combatant.field_effect_immune

    combatant_data.default_status.class_immune['PHYSICAL'] = combatant.p_immune
    combatant_data.default_status.class_immune['MAGIC'] = combatant.m_immune

    combatant_data.default_status.mes_eva_rate = combatant.cond_res_all
    combatant_data.default_status.cri_rate = combatant.cri_rate

    combatant_data.default_status.charge_turn_rate = 1.0

    return combatant_data
