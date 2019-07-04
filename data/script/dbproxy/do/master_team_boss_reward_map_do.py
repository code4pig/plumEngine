# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import MasterDoBase
from script.common.db.class_obj import ClassObject, Dict, String, Class
from script.common.db.database import db_game


class MasterTeamBossRewardMapRow(ClassObject):
    key = String(desc='key. team boss key')

    leader_reward_key = String(desc='队长奖励key')
    member_reward_key = String(desc='队员奖励key')


class MasterTeamBossRewardMap(ClassObject):
    version = String(desc='版本号')
    items = Dict(Class(MasterTeamBossRewardMapRow), desc='数据字典')


class MasterTeamBossRewardMapDo(MasterDoBase):
    def __init__(self, context):
        super(MasterTeamBossRewardMapDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return MasterTeamBossRewardMap

    @classmethod
    def get_prefix(cls):
        return 'MST_TeamBossRewardMap'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_item(self, key):
        return self.doc.items[key]