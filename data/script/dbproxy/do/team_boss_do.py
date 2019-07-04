# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import time
import uuid

from script.common import exceptions as excp
from script.common.db.base_do import ServerIndependantLockDoBase
from script.common.db.database import db_team
from script.common.game_define.rt_battle_define import TeamBossDetail, TeamBossFirstDetail, TeamBossSecondDetail, TeamBossPartDetail, TeamBossFirstStageDetail
from script.common.game_define.team_define import TEAM_FUNC_TYPE_BOSS_FAFURION, TEAM_FUNC_TYPE_BOSS_RAID, TEAM_FUNC_TYPE_BOSS_VALAKAS
from script.dbproxy.do.masters_global import master_constants_inst, master_team_boss_part_inst, master_team_boss_stage_inst, master_team_boss_training_inst


class TeamBossDo(ServerIndependantLockDoBase):
    def __init__(self, context, team_id):
        super(TeamBossDo, self).__init__(context, team_id)
        self.team_id = team_id

    @classmethod
    def cls(cls):
        return TeamBossDetail

    @classmethod
    def get_prefix(cls):
        return 'TEAMBOSS'

    @classmethod
    def get_db(cls):
        return db_team()

    def refresh_new_team_boss(self, func_type, boss_key, create_time, end_time):
        team_boss_detail = TeamBossDetail()
        team_boss_detail.team_id = self.team_id
        team_boss_detail.unique_id = uuid.uuid4().hex
        team_boss_detail.func_type = func_type
        team_boss_detail.boss_key = boss_key
        team_boss_detail.create_time = create_time
        team_boss_detail.end_time = end_time
        team_boss_detail.ready_member_list = []
        if func_type == TEAM_FUNC_TYPE_BOSS_VALAKAS:
            team_boss_detail.first_step = TeamBossFirstDetail()
            team_boss_detail.first_step.is_finish = False
            for stage_conf in master_team_boss_stage_inst.get_stages_by_boss_key(boss_key):
                stage = TeamBossFirstStageDetail()
                stage.stage_id = stage_conf.key
                stage.is_finish = False
                team_boss_detail.first_step.stage_dict[stage.stage_id] = stage
        elif func_type == TEAM_FUNC_TYPE_BOSS_RAID or func_type == TEAM_FUNC_TYPE_BOSS_FAFURION:
            team_boss_detail.first_step = TeamBossFirstDetail()
            team_boss_detail.first_step.is_finish = True
        team_boss_detail.second_step = TeamBossSecondDetail()
        team_boss_detail.second_step.is_finish = False
        parts_conf = master_team_boss_part_inst.get_parts(boss_key)
        for k, v in parts_conf.iteritems():
            part_data = TeamBossPartDetail()
            part_data.part_key = k
            part_data.max_hp = int(master_team_boss_training_inst.get_item(k).hp)
            part_data.cur_hp = part_data.max_hp
            part_data.is_finish = False
            team_boss_detail.second_step.part_dict[k] = part_data
        self.doc = team_boss_detail
        self.update()

    def give_up(self):
        self.delete()

    def is_all_member_ready(self, member_id_list):
        if not self.doc.ready_member_list:
            return False
        for server_member_id in member_id_list:
            if server_member_id not in self.doc.ready_member_list:
                return False
        return True

    def clear_member_ready_list(self):
        self.doc.ready_member_list = []
        self.update()

    def member_be_ready(self, server_member_id):
        if server_member_id in self.doc.ready_member_list:
            return
        self.doc.ready_member_list.append(server_member_id)
        self.update()

    def member_cancel_ready(self, server_member_id):
        if server_member_id in self.doc.ready_member_list:
            self.doc.ready_member_list.remove(server_member_id)
            self.update()

    def is_on_going(self):
        return not self.is_new and not self.is_boss_expired() and not self.is_team_boss_finish()

    def is_boss_expired(self):
        return time.time() > self.doc.end_time

    def is_team_boss_finish(self):
        return self.doc.first_step.is_finish and self.doc.second_step.is_finish

    def is_second_step_in_battle(self):
        now_time = time.time()
        return self.doc.second_step.battle_unique_id and self.doc.second_step.battle_start_time <= now_time < self.doc.second_step.battle_end_time

    def is_first_step_stage_in_battle(self, stage_id):
        stage_detail = self.doc.first_step.stage_dict[stage_id]
        return not stage_detail.is_finish and stage_detail.battle_server_mem_id and stage_detail.battle_start_time < time.time() < stage_detail.battle_end_time

    def begin_first_step_stage_attack(self, stage_id, server_user_id, user_name, hero_key, current_time, deck):
        self.doc.first_step.stage_dict[stage_id].battle_server_mem_id = server_user_id
        self.doc.first_step.stage_dict[stage_id].battle_mem_name = user_name
        self.doc.first_step.stage_dict[stage_id].battle_mem_hero_key = hero_key
        self.doc.first_step.stage_dict[stage_id].battle_start_time = current_time
        self.doc.first_step.stage_dict[stage_id].battle_end_time = current_time + master_constants_inst.get_int('aofei_team_boss_first_battle_period')
        self.doc.first_step.stage_dict[stage_id].deck = deck
        self.update()

    def finish_first_step_stage(self, stage_id, server_user_id, current_time):
        stage_detail = self.doc.first_step.stage_dict[stage_id]
        if stage_detail.battle_server_mem_id != server_user_id:
            raise excp.ExceptionTeamBossFirstStageInBattle()
        if stage_detail.battle_start_time > current_time or stage_detail.battle_end_time < current_time:
            raise excp.ExceptionTeamBossFirstStageTimeout()
        stage_detail.is_finish = True
        stage_detail.battle_server_mem_id = None
        stage_detail.battle_mem_name = None
        stage_detail.battle_mem_hero_key = None
        stage_detail.battle_start_time = 0
        stage_detail.battle_end_time = 0
        stage_detail.deck = None
        self.update()
        # 检查第一阶段是否均完成
        for stage in self.doc.first_step.stage_dict.itervalues():
            if not stage.is_finish:
                return
        self.doc.first_step.is_finish = True

    def begin_second_battle(self, part_key, begin_time):
        self.doc.second_step.battle_unique_id = uuid.uuid4().hex
        self.doc.second_step.attack_part = part_key
        self.doc.second_step.battle_start_time = begin_time
        self.doc.second_step.battle_end_time = begin_time + master_constants_inst.get_int('aofei_team_boss_second_battle_period')
        self.clear_member_ready_list()
        self.update()

    def finish_second_battle(self, part_key, new_hp):
        self.doc.second_step.battle_unique_id = None
        self.doc.second_step.attack_part = None
        self.doc.second_step.battle_start_time = 0
        self.doc.second_step.battle_real_start_time = 0
        self.doc.second_step.battle_end_time = 0
        self.doc.second_step.part_dict[part_key].cur_hp = max(0, new_hp)
        any_not_finish = False
        if new_hp <= 0:
            self.doc.second_step.part_dict[part_key].is_finish = True
            for part_info in self.doc.second_step.part_dict.iteritems():
                if not part_info.is_finish:
                    any_not_finish = True
                    break
        if not any_not_finish:
            # 所有的已完成
            self.doc.is_finish = True
        self.update()
        return not any_not_finish

    def is_any_battle_going(self):
        if self.is_team_boss_finish():
            return False
        if not self.doc.first_step.is_finish:
            for stage_id in self.doc.first_step.stage_dict.keys():
                if self.is_first_step_stage_in_battle(stage_id):
                    return True
        elif not self.doc.first_step.is_finish:
            return self.is_second_step_in_battle()
        return False

    def all_part_finish(self):
        for part in self.doc.second_step.part_dict.itervalues():
            if not part.is_finish:
                return False
        return True

    @staticmethod
    def is_in_team_boss_activity_time(timestamp):
        conf_str = master_constants_inst.get_string('aofei_team_boss_activity_time')
        today_secs = (timestamp - time.timezone) % 86400
        for time_pair in conf_str.split('|'):
            start_time_str, last_time_str = time_pair.split(',')
            start_time = int(start_time_str)
            end_time = start_time + int(last_time_str)
            if start_time <= today_secs < end_time:
                return True
        return False

    @staticmethod
    def cal_team_boss_end_time(timestamp):
        conf_str = master_constants_inst.get_string('aofei_team_boss_activity_time')
        today_secs = (timestamp - time.timezone) % 86400
        for time_pair in conf_str.split('|'):
            start_time_str, last_time_str = time_pair.split(',')
            start_time = int(start_time_str)
            end_time = start_time + int(last_time_str)
            if start_time <= today_secs < end_time:
                return timestamp - today_secs + end_time
        return timestamp
