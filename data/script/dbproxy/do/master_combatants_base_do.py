# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import script.common.exceptions as game_excp
from script.common.db.class_obj import ClassObject, String, Dict, List, Integer, Number, Class
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase
from script.common.game_define.rt_battle_define import CombatantGroupDef


class MasterCombatantsBaseRow(ClassObject):
    key = String(desc='base key')
    category = String(desc='分类')
    c_class_d = String(desc='类别(坦克，治疗等)')
    property = List(String(), desc='属性')
    factor = String(desc='主要属性(力、敏、智)')
    group = String(desc='组(英雄,宠物,变身,NPC等)')
    row = String(desc='站位(前,中,后)')
    res_id = String(desc='资源id')
    rarity_min = Integer(desc='品阶最小值', default=0)
    rarity_max = Integer(desc='品阶最大值', default=0)
    size = Number(desc='大小', default=0)
    aggro = Integer(desc='仇恨值', default=0)
    available = String(desc='玩家是否可得到(Y|N)')
    grade = String(desc='品质级别(A|B|SS等)')

    def is_hero_group(self):
        return self.group in [CombatantGroupDef.COMBATANT_GROUP_HERO, CombatantGroupDef.COMBATANT_GROUP_TU_HERO, CombatantGroupDef.COMBATANT_GROUP_TRANSFORM,
                              CombatantGroupDef.COMBATANT_GROUP_TU_TRANSFORM]

    def is_pet_group(self):
        return self.group in [CombatantGroupDef.COMBATANT_GROUP_PET, CombatantGroupDef.COMBATANT_GROUP_TU_PET, CombatantGroupDef.COMBATANT_GROUP_MONSTER,
                              CombatantGroupDef.COMBATANT_GROUP_TU_MONSTER, CombatantGroupDef.COMBATANT_GROUP_NPC]


class MasterCombatantsBase(ClassObject):
    version = Integer(desc='마스터의 버전')
    items = Dict(Class(MasterCombatantsBaseRow), desc='{Combatant base key: MasterCombatantsBaseRow, ...}')


class MasterCombatantsBaseDo(MasterDoBase):
    def __init__(self, context):
        super(MasterCombatantsBaseDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return MasterCombatantsBase

    @classmethod
    def get_prefix(cls):
        return 'MST_CombatantsBase'

    @classmethod
    def get_db(cls):
        return db_game()

    def get(self, base_key, default=None, raise_exception=False):
        if base_key in self.doc.items:
            return self.doc.items[base_key]
        else:
            if raise_exception:
                raise game_excp.ExceptionCombatantsNotExist('combatants base not exist', base_key)
            else:
                return default
