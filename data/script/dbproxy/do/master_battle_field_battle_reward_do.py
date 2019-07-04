# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-27 19:43

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterBattleFieldBattleRewardRow(ClassObject):
    key = String(desc='key')
    field_id = Integer(desc='分组')
    reward_type = String(desc='奖励类型')
    item = String(desc='奖励id')
    count = Integer(desc='奖励数量')

    def get_index_meta(self):
        return {
            'field_id': (self.field_id, self.reward_type)
        }


class MasterBattleFieldBattleRewardDo(new_master_do_class(MasterBattleFieldBattleRewardRow, "MST_BattleFieldBattleReward")):

    def get_reward_dict(self, field_id, reward_type):
        reward_dict = {}
        for item in self.get_by_index('field_id', field_id, reward_type):
            if item.item not in reward_dict:
                reward_dict[item.item] = 0
            reward_dict[item.item] += item.count
        return reward_dict
