# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Dict, Class, Integer, Float
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase


class MasterStatModRow(ClassObject):
    key = String(desc='고유키. seq')

    group = String(desc='소속 그룹. CombatantsBase.group. MONSTER 도 일단 PET 으로')
    rarity = Integer(desc='등급. 별개수.')

    result_stat = String(desc='영향받는 스탯')

    stat_1 = String(desc='영향 주는 스탯')
    val_1 = Float(desc='스탯 1 계수')
    stat_2 = String(desc='영향 주는 스탯')
    val_2 = Float(desc='스탯 2 계수')


class MasterStatMod(ClassObject):
    version = String(desc='마스터 버전')
    items = Dict(Class(MasterStatModRow), desc='마스터. row')


class MasterStatModDo(MasterDoBase):
    def __init__(self, context):
        super(MasterStatModDo, self).__init__(context)

        # 인덱싱
        self.pk = {}
        for v in self.doc.items.itervalues():
            if v.group not in self.pk:
                self.pk[v.group] = {}
            if v.rarity not in self.pk[v.group]:
                self.pk[v.group][v.rarity] = {}
            self.pk[v.group][v.rarity][v.result_stat] = v

    @classmethod
    def cls(cls):
        return MasterStatMod

    @classmethod
    def get_prefix(cls):
        return 'MST_StatMod'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_item(self, key):
        return self.doc.items[key]

    def _convert_group(self, group):
        if group in self.pk:
            return group
        else:
            return 'PET'

    def get_row_by(self, group, rarity, stat):
        group = self._convert_group(group)
        if group in self.pk:
            if rarity in self.pk[group]:
                return self.pk[group][rarity].get(stat)

    def get_row_list_by_group_rarity(self, group, rarity=0):
        if group in self.pk:
            if rarity in self.pk[group]:
                return self.pk[group][rarity].values()
        return None
