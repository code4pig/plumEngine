# coding=utf8


# Copyright (C) [2017] NCSOFT Corporation. All Rights Reserved.
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will NCSOFT Corporation (“NCSOFT”) be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software subject to acceptance
# and compliance with any agreement entered into between NCSOFT (or any of its affiliates) and the recipient.
# The following restrictions shall also apply:
#
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software.
# 2. You may not modify, alter or redistribute this software, in whole or part, unless you are entitled to
# do so by express authorization in a separate agreement between you and NCSOFT.
# 3. This notice may not be removed or altered from any source distribution.


# coding=utf8

from __future__ import unicode_literals

from script.common.db.instant_box import instant_box
from script.dbproxy.do.masters_global import master_battle_field_setting_inst
from script.common.db.database import db_battle_field
from script.common.game_define.global_def import make_server_user_id
from script.common.db.base_do import BaseDo
from script.common.game_define.battle_field_def import BattleFieldUserInfo, const_battle_field_document_ttl, BattleFieldUsedPetInfo, FORT_WAR_STEP2_POINT_ID_LIST


class BattleFieldUserDo(BaseDo):
    """
    점령전 유져 정보
    占领战玩家数据
    """

    def __init__(self, context, season_key, user_id, server_id=None):
        self.server_id = server_id
        super(BattleFieldUserDo, self).__init__(context, season_key, user_id)

        self.doc.season_key = season_key
        self.doc.user_id = user_id

        if not self.doc.server_user_id:
            if self.server_id:
                self.doc.server_user_id = make_server_user_id(self.server_id, user_id)
            else:
                self.doc.server_user_id = make_server_user_id(instant_box.server_selected, user_id)

        self.block_defense_map = {}
        self.make_block_defense_pets_map()

    @classmethod
    def cls(cls):
        return BattleFieldUserInfo

    @classmethod
    def get_prefix(cls):
        return 'BF_USR'

    @classmethod
    def get_db(cls):
        return db_battle_field()

    @classmethod
    def get_ttl(cls):
        return const_battle_field_document_ttl + 10

    def get_server_dependant_id(self):
        return self.server_id

    def get_user_defense_info_dict(self):
        return self.doc.defense_info_dict

    def make_block_defense_pets_map(self):
        # 先清空
        self.block_defense_map.clear()
        # 构造区块部署的防守信息, (field_id, block_id) => hero class key | pet base key
        for pet_key, info in self.doc.defense_info_dict.iteritems():
            key = (info.field_id, info.block_id)
            if key not in self.block_defense_map:
                self.block_defense_map[key] = []

            self.block_defense_map[key].append(pet_key)

    def replace_user_block_defense(self, field_id, block_id, hero_class_key=None, pet_key_list=None, point_id=None):
        if pet_key_list is None:
            pet_key_list = []
        key = (field_id, block_id)
        if key in self.block_defense_map:
            # 先删除下阵的
            for pet_key in self.block_defense_map[key]:
                if pet_key != hero_class_key and pet_key not in pet_key_list:
                    self.doc.defense_info_dict.pop(pet_key, None)
        if hero_class_key or pet_key_list:
            pet_block = BattleFieldUsedPetInfo()
            pet_block.field_id = field_id
            pet_block.block_id = block_id
            pet_block.point_id = point_id
            # 再检查新增的
            if hero_class_key:
                self.doc.defense_info_dict[hero_class_key] = pet_block
            for pet_key in pet_key_list:
                self.doc.defense_info_dict[pet_key] = pet_block
        # 再刷新映射表
        self.make_block_defense_pets_map()
        self.update()

    def is_hero_pet_used_at_other_point(self, field_id, block_id, key):
        return key in self.doc.defense_info_dict and (self.doc.defense_info_dict[key].field_id != field_id or
                                                      self.doc.defense_info_dict[key].block_id != block_id)

    def is_in_frozen_time(self, current_time, block_id=None, point_id=None):
        if point_id:
            # 是进攻的要塞
            # 进攻不同区块 or 同一区块且统一据点, 则需要检查冷却时间
            is_same_step_point = (self.doc.last_attack_block_id >= 0 and self.doc.last_attack_point_id != block_id) or \
                                 (point_id == self.doc.last_attack_point_id) or \
                                 (point_id in FORT_WAR_STEP2_POINT_ID_LIST and
                                  self.doc.last_attack_point_id in FORT_WAR_STEP2_POINT_ID_LIST)
            return is_same_step_point and (self.doc.last_attack_time + master_battle_field_setting_inst.get_number('battle_field_user_battle_interval') > current_time)
        else:
            # 普通据点
            return self.doc.last_attack_time + master_battle_field_setting_inst.get_number('battle_field_user_battle_interval') > current_time

    def update_attack_data(self, attack_time, block_id, point_id=None):
        self.doc.last_attack_block_id = block_id
        self.doc.last_attack_point_id = point_id
        self.doc.last_attack_time = attack_time
        self.update()