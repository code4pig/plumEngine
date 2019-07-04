# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import MasterDoBase
from script.common.db.class_obj import ClassObject, Dict, String, Class
from script.common.db.database import db_game


class MasterTeamBossPartRow(ClassObject):
    key = String(desc='key. Training key')
    combatant_key = String(desc='Combatants.key')
    level = String(desc='等级')
    boss_key = String(desc='boss key. TeamBoss.key')
    part = String(desc='部位. core/part')


class MasterTeamBossPart(ClassObject):
    version = String(desc='마스터 버전.')
    items = Dict(Class(MasterTeamBossPartRow), desc='보스 파트')


class MasterTeamBossPartDo(MasterDoBase):
    def __init__(self, context):
        super(MasterTeamBossPartDo, self).__init__(context)

        self.boss_idx = {}
        for v in self.doc.items.itervalues():
            if v.boss_key not in self.boss_idx:
                self.boss_idx[v.boss_key] = {}
            self.boss_idx[v.boss_key][v.key] = v

    @classmethod
    def cls(cls):
        return MasterTeamBossPart

    @classmethod
    def get_prefix(cls):
        return 'MST_TeamBossPart'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_item(self, key):
        return self.doc.items[key]

    def get_parts(self, boss_key):
        if boss_key in self.boss_idx:
            return self.boss_idx.get(boss_key)

    def get_part_type(self, boss_key, part_key):
        if boss_key in self.boss_idx:
            parts = self.boss_idx.get(boss_key)
            if part_key in parts:
                return parts.get(part_key).part

        return None

