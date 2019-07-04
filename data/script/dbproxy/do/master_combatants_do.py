# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import script.common.exceptions as game_excp
from script.common.db.class_obj import ClassObject, String, Dict, Class, Integer, Number, List
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase
from script.common.game_define.rt_battle_define import Combatant


class MasterCombatantsRow(ClassObject):
    key = String(desc='唯一key')
    base = String(desc='base key')
    name = String(desc='名字')
    res_id = String(desc='res_id,资源id')
    rarity = Integer(desc='rarity,品阶', default=0)
    str = Integer(desc='str,力量', default=0)
    dex = Integer(desc='dex,敏捷', default=0)
    int = Integer(desc='int,智力', default=0)
    con = Integer(desc='con,体质', default=0)
    move_speed = Number(desc='移动速度', default=0)
    atk_speed = Number(desc='攻击速度', default=0)
    p_atk = Integer(desc='物理攻击', default=0)
    m_atk = Integer(desc='魔法攻击', default=0)
    hp = Integer(desc='血量', default=0)
    p_def = Integer(desc='物理防御', default=0)
    res = Integer(desc='魔法抵抗', default=0)
    pen = Integer(desc='物理穿透', default=0)
    cond_dec = Integer(desc='被控制衰减', default=0)
    cri = Integer(desc='暴击', default=0)
    eva = Integer(desc='闪避', default=0)
    attr_res = Dict(Integer(), desc='属性抗性')
    cond_res = Dict(Integer(), desc='控制抗性')
    field_effect_immune = List(String(), desc='场景效果免疫')

    def clone_to_combatant(self):
        clone = Combatant()
        clone.key = self.key
        clone.base = self.base
        clone.name = self.name
        clone.res_id = self.res_id
        clone.rarity = self.rarity
        clone.str = self.str if self.str else 0
        clone.dex = self.dex if self.dex else 0
        clone.int = self.int if self.int else 0
        clone.con = self.con if self.con else 0
        clone.move_speed = self.move_speed if self.move_speed else 0
        clone.atk_speed = self.atk_speed if self.atk_speed else 0
        clone.p_atk = self.p_atk if self.p_atk else 0
        clone.m_atk = self.m_atk if self.m_atk else 0
        clone.hp = self.hp if self.hp else 0
        clone.p_def = self.p_def if self.p_def else 0
        clone.res = self.res if self.res else 0
        clone.pen = self.pen if self.pen else 0
        clone.cond_dec = self.cond_dec if self.cond_dec else 0
        clone.cri = self.cri if self.cri else 0
        clone.eva = self.eva if self.eva else 0
        if self.attr_res:
            for k, v in self.attr_res.iteritems():
                clone.attr_res[k] = v
        if self.cond_res:
            for k, v in self.cond_res.iteritems():
                clone.cond_res[k] = v
        if self.field_effect_immune:
                clone.field_effect_immune += self.field_effect_immune
        return clone


class MasterCombatants(ClassObject):
    version = String(desc='마스터 버전')
    items = Dict(Class(MasterCombatantsRow), desc='combatant row')


class MasterCombatantsDo(MasterDoBase):
    def __init__(self, context):
        super(MasterCombatantsDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return MasterCombatants

    @classmethod
    def get_prefix(cls):
        return 'MST_Combatants'

    @classmethod
    def get_db(cls):
        return db_game()

    def get(self, combatant_class_key, default=None, raise_exception=False):
        if combatant_class_key in self.doc.items:
            return self.doc.items[combatant_class_key]
        else:
            if raise_exception:
                raise game_excp.ExceptionCombatantsNotExist('combatants class key not exist', combatant_class_key)
            else:
                return default
