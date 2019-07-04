# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterAlphaFortWarBattleRewardRow(ClassObject):
    key = String(desc='key')
    group_no = Integer(desc='分组')
    reward_type = String(desc='奖励类型')
    item = String(desc='奖励id')
    count = Integer(desc='奖励数量')

    def get_index_meta(self):
        return {
            'group_type': (self.group_no, self.reward_type)
        }


class MasterAlphaFortWarBattleRewardDo(new_master_do_class(MasterAlphaFortWarBattleRewardRow, "MST_AlphaFortWarBattleReward")):

    def get_reward_dict(self, group_no, reward_type, is_weekend=False):
        reward_dict = {}
        for item in self.get_by_index('group_type', group_no, reward_type):
            if item.item not in reward_dict:
                reward_dict[item.item] = 0
            if is_weekend:
                reward_dict[item.item] += item.count * 2
            else:
                reward_dict[item.item] += item.count
        return reward_dict

