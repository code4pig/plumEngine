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


from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.raid_def import UserRaidInfo
from script.common.game_define.time_util import is_same_date
from script.dbproxy.do.masters_global import master_constants_inst


class UserRaidDo(BaseDo):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(UserRaidDo, self).__init__(context, user_id)
        self.doc.user_id = user_id

    @classmethod
    def cls(cls):
        return UserRaidInfo

    @classmethod
    def get_prefix(cls):
        return 'USRRAID'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def init_raid_info(self, reset_season):
        new_raid_info = UserRaidInfo()
        new_raid_info.user_id = self.doc.user_id
        new_raid_info.raid_deck = self.doc.raid_deck
        new_raid_info.init_inheritance_boss_level_flag = reset_season
        if not reset_season:
            new_raid_info.inheritance_boss_level = self.doc.inheritance_boss_level
        self.doc = new_raid_info
        self.update()

    def finish_raid(self):
        self.doc.boss = None
        self.update()

    def add_reward_times(self, cur_time):
        if not is_same_date(self.doc.reward_time, cur_time, master_constants_inst.get_int('GlobalResetTimestamp')):
            self.doc.reward_times = 0
        if self.doc.reward_times >= master_constants_inst.get_int('aofei_raid_reward_max_times_per_day'):
            return False
        else:
            self.doc.reward_times += 1
            self.doc.reward_time = cur_time
            self.update()
            return True


