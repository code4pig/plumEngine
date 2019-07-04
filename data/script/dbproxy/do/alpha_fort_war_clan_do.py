# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.dbproxy.do.masters_global import master_constants_inst
from script.common.game_define.global_def import get_clan_server_id
from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.alpha_fort_war_def import AlphaFortWarClan, ALPHA_FORT_WAR_RESULT_NONE, ALPHA_FORT_WAR_POINT_ID_LIST, AlphaFortWarPointDetail, ALPHA_FORT_WAR_RESULT_WIN


class AlphaFortWarClanDo(BaseDo):
    def __init__(self, context, clan_id):
        self.server_id = get_clan_server_id(clan_id)
        super(AlphaFortWarClanDo, self).__init__(context, clan_id)
        self.doc.clan_id = clan_id

    @classmethod
    def cls(cls):
        return AlphaFortWarClan

    @classmethod
    def get_prefix(cls):
        return 'ALPHAFORTWARCLAN'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def reset_data(self, season_no, group_no, current_time):
        if self.doc.season_no != season_no:
            self.doc.season_no = season_no
            self.doc.streak_win_count = 0
        self.doc.group_no = group_no
        self.doc.result = ALPHA_FORT_WAR_RESULT_NONE
        self.doc.result_time = 0
        self.doc.last_reset_time = int(current_time)
        self.doc.battle_data_init_time = 0
        self.doc.rest_defense_count = 0
        self.doc.point_dict.clear()
        self.doc.attend_user_list = []
        for point_id in ALPHA_FORT_WAR_POINT_ID_LIST:
            info = AlphaFortWarPointDetail()
            self.doc.point_dict[point_id] = info
        self.doc.facility_info_list = list()
        self.update()

    def update_battle_init_time(self, current_time):
        self.doc.battle_data_init_time = current_time
        self.update()

    def update_total_rest_defense_count(self, defense_count):
        if self.doc.rest_defense_count != defense_count:
            self.doc.rest_defense_count = defense_count
            self.update()

    def update_facility_info(self, facility_list):
        self.doc.facility_info_list = facility_list
        self.update()

    def set_update_attend_user(self, attend_user_list):
        self.doc.attend_user_list = attend_user_list
        self.update()

    def append_attend_user(self, attend_server_user_id):
        if attend_server_user_id not in self.doc.attend_user_list:
            self.doc.attend_user_list.append(attend_server_user_id)
            self.update()

    def init_point_defense_detail(self, point_id, total_count, rest_count, def_hero_list=None, def_pet_list=None):
        self.doc.point_dict[point_id].total_count = total_count
        self.doc.point_dict[point_id].rest_count = rest_count
        self.doc.point_dict[point_id].point_battle_hero = def_hero_list if def_hero_list else []
        self.doc.point_dict[point_id].point_battle_pet = def_pet_list if def_pet_list else []
        self.update()

    def cal_rest_defense_count(self, point_id, current_time):
        new_point_count = 0
        if self.doc.point_dict[point_id].point_battle_hero:
            new_point_count += len(self.doc.point_dict[point_id].point_battle_hero)
        if self.doc.point_dict[point_id].point_battle_pet:
            new_point_count += len(self.doc.point_dict[point_id].point_battle_pet)
        old_point_count = self.doc.point_dict[point_id].rest_count
        if old_point_count != new_point_count:
            self.doc.point_dict[point_id].rest_count = new_point_count
            self.doc.point_dict[point_id].update_time = current_time
            diff_count = old_point_count - new_point_count
            if diff_count < 0 or self.doc.rest_defense_count < diff_count:
                print '===== [ERROR] ===== defense count error : ', old_point_count, new_point_count, self.doc.rest_defense_count
            self.doc.rest_defense_count = max(0, self.doc.rest_defense_count - diff_count)
            self.update()

    def update_point_rest_count(self, point_id, rest_count, current_time, last_attack_server_user_id):
        if self.doc.point_dict[point_id].rest_count != rest_count:
            self.doc.point_dict[point_id].rest_count = rest_count
            self.doc.point_dict[point_id].update_time = current_time
            if last_attack_server_user_id:
                self.doc.point_dict[point_id].last_attack_server_user_id = last_attack_server_user_id
            self.update()

    def update_point_battle_user_count(self, point_id, user_count):
        if self.doc.point_dict[point_id].battle_user_count != user_count:
            self.doc.point_dict[point_id].battle_user_count = user_count
            self.update()

    def user_start_battle(self, point_id, server_user_id, current_time):
        self.doc.point_dict[point_id].battle_server_user_id = server_user_id
        self.doc.point_dict[point_id].battle_end_time = current_time + master_constants_inst.get_number('aofei_fort_war_step2_battle_time_limit')
        self.update()

    def clear_battle_user(self, point_id):
        self.doc.point_dict[point_id].battle_server_user_id = None
        self.doc.point_dict[point_id].battle_end_time = 0
        self.update()

    def delete_hero_data(self, point_id, server_user_id, key):
        delete_ok = False
        for info in self.doc.point_dict[point_id].point_battle_hero:
            if info.hero_snap.server_user_id == server_user_id and info.hero_snap.class_key == key:
                self.doc.point_dict[point_id].point_battle_hero.remove(info)
                delete_ok = True
                self.update()
                break
        return delete_ok

    def update_hero_data(self, point_id, server_user_id, key, rest_hp):
        update_ok = False
        for info in self.doc.point_dict[point_id].point_battle_hero:
            if info.hero_snap.server_user_id == server_user_id and info.hero_snap.class_key == key:
                info.rest_hp = rest_hp
                update_ok = True
                self.update()
                break
        return update_ok

    def delete_pet_data(self, point_id, server_user_id, key):
        delete_ok = False
        for info in self.doc.point_dict[point_id].point_battle_pet:
            if info.pet_snap.server_user_id == server_user_id and info.pet_snap.base_key == key:
                self.doc.point_dict[point_id].point_battle_pet.remove(info)
                delete_ok = True
                self.update()
                break
        return delete_ok

    def update_pet_data(self, point_id, server_user_id, key, rest_hp):
        update_ok = False
        for info in self.doc.point_dict[point_id].point_battle_pet:
            if info.pet_snap.server_user_id == server_user_id and info.pet_snap.base_key == key:
                info.rest_hp = rest_hp
                update_ok = True
                self.update()
                break
        return update_ok

    def update_result(self, result, current_time):
        self.doc.result = result
        self.doc.result_time = current_time
        if result == ALPHA_FORT_WAR_RESULT_WIN:
            self.doc.streak_win_count += 1
        else:
            self.doc.streak_win_count = 0
        self.update()


