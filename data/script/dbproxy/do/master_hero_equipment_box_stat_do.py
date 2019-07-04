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

from script.common.db.class_obj import ClassObject, String, Dict, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterHeroEquipmentBoxStatRow(ClassObject):
    key = String(desc='고유키')
    group_id = String(desc='그룹 id')
    type = String(desc='수집/강화 여부')
    step = Integer(desc='강화 단계')
    step_value = Integer(desc='세부 구성 단계')
    stat = Dict(Integer(), desc='강화 스탯')
    costume = String(desc='보상 받는 costume')

    def get_index_meta(self):
        return {
            'get_stat': (self.group_id, self.step_value),
            'get_type': (self.group_id, self.type),
        }

    def can_get_costume(self):
        return self.costume is not None


class MasterHeroEquipmentBoxStatDo(new_master_do_class(MasterHeroEquipmentBoxStatRow, 'MST_HeroEquipmentBoxStat')):
    def __init__(self, data_context):
        super(MasterHeroEquipmentBoxStatDo, self).__init__(data_context)

        self.hero_costume_condition_by_group_id = {}

        for row in self.doc.items.values():

            if row.costume is not None:
                self.hero_costume_condition_by_group_id[row.group_id] = row.key

    def get_costume_key_by_equipment_stat(self,group_id):
        return self.hero_costume_condition_by_group_id[group_id]

    def get_equipment_stat_list(self, group_id, count, strength):
        return self.get_stat_list_by_type(group_id, 'collect', count) + \
            self.get_stat_list_by_type(group_id, 'enchant', strength)

    def get_stat_list_by_type(self, group_id, check_type, target_value):
        master_collect_list = self.get_by_index('get_type', group_id, check_type)
        return [o.key for o in master_collect_list if o.step_value <= target_value]

