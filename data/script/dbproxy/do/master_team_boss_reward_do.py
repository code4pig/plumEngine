# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Dict, String, Class
from script.dbproxy.do.master_util import new_master_do_class


class MasterTeamBossRewardRow(ClassObject):
    key = String(desc='key.')
    reward_key = String('奖励key')
    item = String(desc='奖励id')
    count = String(desc='奖励数量')

    def get_index_meta(self):
        return {
            'reward_key': (self.reward_key,)
        }


class MasterTeamBossReward(ClassObject):
    version = String(desc='版本号')
    items = Dict(Class(MasterTeamBossRewardRow), desc='数据字典')


class MasterTeamBossRewardDo(new_master_do_class(MasterTeamBossRewardRow, 'MST_TeamBossReward')):
    def get_reward_dict(self, reward_key):
        reward_dict = {}
        for boss_reward in self.get_by_index('reward_key', reward_key):
            reward_dict[boss_reward.item] = boss_reward.count
        return reward_dict

