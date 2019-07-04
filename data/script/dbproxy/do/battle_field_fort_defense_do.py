# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-23 15:48


from __future__ import unicode_literals

from script.dbproxy.do.masters_global import master_battle_field_setting_inst
from script.common.db.base_do import BaseDo
from script.common.db.database import db_battle_field
from script.common.game_define.battle_field_def import const_battle_field_document_ttl, BattleFieldFortDefenseInfo, FortPointSlotPair, FORT_HERO_SLOT_MIN, FORT_HERO_SLOT_MAX, \
    FORT_PET_SLOT_MIN, FORT_PET_SLOT_MAX, FortBeforeBattleDefense, FortPointDetail


class BattleFieldFortDefenseDo(BaseDo):
    """
    据点防守信息
    """

    def __init__(self, context, season_key, field_id, block_id):
        super(BattleFieldFortDefenseDo, self).__init__(context, season_key, field_id, block_id)

        self.doc.season_key = season_key
        self.doc.field_id = field_id
        self.doc.block_id = block_id

        if self.is_new and self.writer:
            self.doc.before_battle_defense = FortBeforeBattleDefense()
            self.update()

    @classmethod
    def cls(cls):
        return BattleFieldFortDefenseInfo

    @classmethod
    def get_prefix(cls):
        return 'BF_FORT_DEFENSE'

    @classmethod
    def get_db(cls):
        return db_battle_field()

    @classmethod
    def is_server_group_do(cls):
        return True

    @classmethod
    def get_ttl(cls):
        return const_battle_field_document_ttl + 10

    def update_user_defense(self, server_user_id, point_id, hero_info, pet_info_dict):
        self._do_update_defense(server_user_id, point_id, hero_info, pet_info_dict)
        self.doc.rest_defense_count = self.get_total_defense_count()
        # 此处不更新每个据点战斗阶段数据，在宣战成功时初始化时更新，以及战斗过程中更新
        # cur_point_count = self.get_point_defense_count(point_id)
        # self._do_update_point_defense_count(point_id, cur_point_count, cur_point_count)

    def get_total_defense_count(self):
        defense_count = 0
        for v in self.doc.before_battle_defense.point_used_hero_slot.itervalues():
            defense_count += len(v)
        for v in self.doc.before_battle_defense.point_used_pet_slot.itervalues():
            defense_count += len(v)
        return defense_count

    def get_point_defense_count(self, point_id):
        point_count = 0
        if point_id in self.doc.before_battle_defense.point_used_hero_slot:
            point_count += len(self.doc.before_battle_defense.point_used_hero_slot[point_id])
        if point_id in self.doc.before_battle_defense.point_used_pet_slot:
            point_count += len(self.doc.before_battle_defense.point_used_pet_slot[point_id])
        return point_count

    def user_start_battle(self, point_id, server_user_id, current_time):
        self.doc.point_detail_dict[point_id].battle_server_user_id = server_user_id
        self.doc.point_detail_dict[point_id].battle_end_time = current_time + master_battle_field_setting_inst.get_number('battle_field_fort_step2_battle_time_limit')
        self.update()

    def delete_hero_data(self, point_id, server_user_id, key):
        delete_ok = False
        for info in self.doc.point_detail_dict[point_id].point_battle_hero:
            if info.hero_snap.server_user_id == server_user_id and info.hero_snap.class_key == key:
                self.doc.point_detail_dict[point_id].point_battle_hero.remove(info)
                delete_ok = True
                self.update()
                break
        return delete_ok

    def update_hero_data(self, point_id, server_user_id, key, rest_hp):
        update_ok = False
        for info in self.doc.point_detail_dict[point_id].point_battle_hero:
            if info.hero_snap.server_user_id == server_user_id and info.hero_snap.class_key == key:
                info.rest_hp = rest_hp
                update_ok = True
                self.update()
                break
        return update_ok

    def delete_pet_data(self, point_id, server_user_id, key):
        delete_ok = False
        for info in self.doc.point_detail_dict[point_id].point_battle_pet:
            if info.pet_snap.server_user_id == server_user_id and info.pet_snap.base_key == key:
                self.doc.point_detail_dict[point_id].point_battle_pet.remove(info)
                delete_ok = True
                self.update()
                break
        return delete_ok

    def update_pet_data(self, point_id, server_user_id, key, rest_hp):
        update_ok = False
        for info in self.doc.point_detail_dict[point_id].point_battle_pet:
            if info.pet_snap.server_user_id == server_user_id and info.pet_snap.base_key == key:
                info.rest_hp = rest_hp
                update_ok = True
                self.update()
                break
        return update_ok

    def clear_battle_user(self, point_id):
        self.doc.point_detail_dict[point_id].battle_server_user_id = None
        self.doc.point_detail_dict[point_id].battle_end_time = 0
        self.update()

    def cal_rest_defense_count(self, point_id, current_time):
        new_point_count = 0
        if self.doc.point_detail_dict[point_id].point_battle_hero:
            new_point_count += len(self.doc.point_detail_dict[point_id].point_battle_hero)
        if self.doc.point_detail_dict[point_id].point_battle_pet:
            new_point_count += len(self.doc.point_detail_dict[point_id].point_battle_pet)
        old_point_count = self.doc.point_detail_dict[point_id].rest_count
        if old_point_count != new_point_count:
            self.doc.point_detail_dict[point_id].rest_count = new_point_count
            self.doc.point_detail_dict[point_id].update_time = current_time
            diff_count = old_point_count - new_point_count
            if diff_count < 0 or self.doc.rest_defense_count < diff_count:
                print '===== [ERROR] ===== defense count error : ', old_point_count, new_point_count, self.doc.rest_defense_count
            self.doc.rest_defense_count = max(0, self.doc.rest_defense_count - diff_count)
            self.update()

    def rest_battle_data_all(self):
        self.doc.point_detail_dict = {}
        self.doc.facility_info_list = []
        self.update()

    def reset_data_all(self):
        self.doc = BattleFieldFortDefenseInfo()
        self.doc.before_battle_defense = FortBeforeBattleDefense()
        self.update()

    def init_point_defense_detail(self, point_id, total_count, rest_count, current_time, def_hero_list=None, def_pet_list=None):
        self.doc.point_detail_dict[point_id] = FortPointDetail()
        self.doc.point_detail_dict[point_id].total_count = total_count
        self.doc.point_detail_dict[point_id].rest_count = rest_count
        self.doc.point_detail_dict[point_id].update_time = current_time
        self.doc.point_detail_dict[point_id].point_battle_hero = def_hero_list if def_hero_list is None else []
        self.doc.point_detail_dict[point_id].point_battle_pet = def_pet_list if def_pet_list is None else []
        self.update()

    def update_battle_init_time(self, current_time):
        self.doc.is_battle_data_init = True
        self.doc.battle_data_init_time = current_time
        self.update()

    def update_facility_info(self, facility_list):
        self.doc.facility_info_list = facility_list
        self.update()

    def update_point_battle_user_count(self, point_id, user_count):
        if self.doc.point_detail_dict[point_id].battle_user_count != user_count:
            self.doc.point_detail_dict[point_id].battle_user_count = user_count
            self.update()

    def update_point_rest_count(self, point_id, rest_count, current_time, last_attack_server_user_id):
        if self.doc.point_detail_dict[point_id].rest_count != rest_count:
            self.doc.point_detail_dict[point_id].rest_count = rest_count
            self.doc.point_detail_dict[point_id].update_time = current_time
            if last_attack_server_user_id:
                self.doc.point_detail_dict[point_id].last_attack_server_user_id = last_attack_server_user_id
            self.update()

    def _do_update_defense(self, server_user_id, point_id, hero_info, pet_info_dict):
        """
        特别注意：相信外部判断逻辑，该方法中不再做更多的检查
        """
        if self.doc.before_battle_defense is None:
            self.doc.before_battle_defense = FortBeforeBattleDefense()
        # 处理英雄
        # 先检查hero列表数据
        if server_user_id not in self.doc.before_battle_defense.user_hero_defense:
            self.doc.before_battle_defense.user_hero_defense[server_user_id] = {}
        if point_id not in self.doc.before_battle_defense.point_used_hero_slot:
            self.doc.before_battle_defense.point_used_hero_slot[point_id] = []
        if point_id not in self.doc.before_battle_defense.point_hero_defense:
            self.doc.before_battle_defense.point_hero_defense[point_id] = {}

        if hero_info:  # 需要设置英雄
            if len(self.doc.before_battle_defense.user_hero_defense[server_user_id]) > 0:  # 已有设置了的英雄，替换，更新数据
                # 更新hero_info 的 slot_no
                hero_info.slot_no = self.doc.before_battle_defense.user_hero_defense[server_user_id].values()[0].slot_no
                # 更新 point_hero_defense
                self.doc.before_battle_defense.point_hero_defense[point_id][str(hero_info.slot_no)] = hero_info
                # user_hero_defense 清除旧数据
                self.doc.before_battle_defense.user_hero_defense[server_user_id].clear()
                # user_hero_defense 添加新数据
                hero_point_slot_pair = FortPointSlotPair()
                hero_point_slot_pair.point_id = point_id
                hero_point_slot_pair.slot_no = hero_info.slot_no
                self.doc.before_battle_defense.user_hero_defense[server_user_id][hero_info.class_key] = hero_point_slot_pair
            else:  # 玩家没设过英雄
                # 找一个空的坑位
                for slot_no in xrange(FORT_HERO_SLOT_MIN, FORT_HERO_SLOT_MAX + 1):
                    if slot_no not in self.doc.before_battle_defense.point_used_hero_slot[point_id]:
                        hero_info.slot_no = slot_no
                        break
                # 更新 point_used_hero_slot
                self.doc.before_battle_defense.point_used_hero_slot[point_id].append(hero_info.slot_no)
                # 更新 point_hero_defense
                self.doc.before_battle_defense.point_hero_defense[point_id][str(hero_info.slot_no)] = hero_info
                # 更新 user_hero_defense
                hero_point_slot_pair = FortPointSlotPair()
                hero_point_slot_pair.point_id = point_id
                hero_point_slot_pair.slot_no = hero_info.slot_no
                self.doc.before_battle_defense.user_hero_defense[server_user_id][hero_info.class_key] = hero_point_slot_pair
        else:  # 英雄设置为空
            if len(self.doc.before_battle_defense.user_hero_defense[server_user_id]) > 0:  # 原来设置有英雄
                if self.doc.before_battle_defense.user_hero_defense[server_user_id].values()[0].point_id == point_id:  # 原有英雄是该据点的英雄
                    # 下阵原来设置的英雄
                    old_hero_slot_no = self.doc.before_battle_defense.user_hero_defense[server_user_id].values()[0].slot_no
                    # 删除 point_used_hero_slot 数据
                    self.doc.before_battle_defense.point_used_hero_slot[point_id].remove(old_hero_slot_no)
                    # 删除 point_hero_defense 数据
                    self.doc.before_battle_defense.point_hero_defense[point_id].pop(str(old_hero_slot_no), None)
                    # 删除 user_hero_defense 数据
                    self.doc.before_battle_defense.user_hero_defense[server_user_id].clear()  # 一个玩家只能设置一个英雄,所以直接清掉

        # 处理召唤兽
        # 先检查pet列表数据
        if server_user_id not in self.doc.before_battle_defense.user_pet_defense:
            self.doc.before_battle_defense.user_pet_defense[server_user_id] = {}
        if point_id not in self.doc.before_battle_defense.point_pet_defense:
            self.doc.before_battle_defense.point_pet_defense[point_id] = {}
        if point_id not in self.doc.before_battle_defense.point_used_pet_slot:
            self.doc.before_battle_defense.point_used_pet_slot[point_id] = []

        # 计算原来没有，这次有的召唤兽(待添加的)
        old_pet_key_list = self.doc.before_battle_defense.user_pet_defense[server_user_id].keys()
        will_add_pet_key_list = []
        for k in pet_info_dict:
            if k not in old_pet_key_list:
                will_add_pet_key_list.append(k)

        # 计算原来有，这次没有的召唤兽(待删除的)
        will_remove_pet_key_list = []
        will_remove_pet_slot_list = []
        for k, v in self.doc.before_battle_defense.user_pet_defense[server_user_id].iteritems():
            if v.point_id == point_id and k not in pet_info_dict:  # 原来是该据点的召唤兽, 但是这次设置没有, 相当于下阵了
                will_remove_pet_key_list.append(k)
                will_remove_pet_slot_list.append(v.slot_no)

        # 删除下阵的召唤兽相关数据
        for slot_no in will_remove_pet_slot_list:
            # 删除 point_used_pet_slot
            self.doc.before_battle_defense.point_used_pet_slot[point_id].remove(slot_no)
            # 删除 point_pet_defense
            self.doc.before_battle_defense.point_pet_defense[point_id].pop(str(slot_no))
        for pet_key in will_remove_pet_key_list:
            # 删除 user_pet_defense
            self.doc.before_battle_defense.user_pet_defense[server_user_id].pop(pet_key)

        # 添加新上阵的召唤兽相关数据
        will_add_pet_count = len(will_add_pet_key_list)
        if will_add_pet_count > 0:  # 有新增的召唤兽
            will_slot_no_list = []
            # 找到指定数量的坑位
            for slot_no in xrange(FORT_PET_SLOT_MIN, FORT_PET_SLOT_MAX + 1):
                if slot_no not in self.doc.before_battle_defense.point_used_pet_slot[point_id]:
                    will_slot_no_list.append(slot_no)
                    if len(will_slot_no_list) >= will_add_pet_count:
                        break
            temp_count = 0
            for k, v in pet_info_dict.iteritems():
                v.slot_no = will_slot_no_list[temp_count]
                # 修改 point_used_pet_slot
                self.doc.before_battle_defense.point_used_pet_slot[point_id].append(v.slot_no)
                # 修改 point_pet_defense
                self.doc.before_battle_defense.point_pet_defense[point_id][str(v.slot_no)] = v
                # 修改 user_pet_defense
                pet_point_slot_pair = FortPointSlotPair()
                pet_point_slot_pair.point_id = point_id
                pet_point_slot_pair.slot_no = v.slot_no
                self.doc.before_battle_defense.user_pet_defense[server_user_id][v.class_key] = pet_point_slot_pair
                temp_count += 1

        self.update()