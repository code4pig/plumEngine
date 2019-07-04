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

from script.dbproxy.do.masters_global import master_battle_field_setting_inst
from script.common.db.base_do import BaseDo
from script.common.db.database import db_battle_field
from script.common.game_define.battle_field_def import const_battle_field_document_ttl, BattleFieldBlockInfo


# BF_FORT_BLOCK_ID_LIST = [int(bid) for bid in master_battle_field_setting_inst.get_string('battle_field_fort_block_id_list').split(',')]
BF_FORT_BLOCK_ID_LIST = [80, 49, 130, 97, 63, 19, 141, 84, 76, 27, 133, 24, 136, 138, 22]


def is_fort(block_id):
    return block_id in BF_FORT_BLOCK_ID_LIST


def get_block_protect_time(block_id):
    if is_fort(block_id):
        # 堡垒
        return master_battle_field_setting_inst.get_number('battle_field_protect_time_fort')
    else:
        return master_battle_field_setting_inst.get_number('battle_field_protect_time_normal')


def get_block_protect_set_defense_time():
    return master_battle_field_setting_inst.get_number('battle_field_protect_set_defense_time')


class BattleFieldBlockDo(BaseDo):
    """
    据点信息
    """

    def __init__(self, context, season_key, field_id, block_id):
        super(BattleFieldBlockDo, self).__init__(context, season_key, field_id, block_id)

        self.doc.season_key = season_key
        self.doc.field_id = field_id
        self.doc.block_id = block_id

    @classmethod
    def cls(cls):
        return BattleFieldBlockInfo

    @classmethod
    def get_prefix(cls):
        return 'BF_BLOCK'

    @classmethod
    def get_db(cls):
        return db_battle_field()

    @classmethod
    def is_server_group_do(cls):
        return True

    @classmethod
    def get_ttl(cls):
        return const_battle_field_document_ttl + 10

    def change_block_clan_id(self, clan_id, current_time=0):
        self.doc.clan_id = clan_id
        self.doc.set_time = current_time
        if current_time:
            self.doc.protect_defense_end_time = current_time + get_block_protect_set_defense_time()
            self.doc.protect_start_time = current_time
            self.doc.protect_end_time = current_time + get_block_protect_time(self.doc.block_id)

        self.doc.battle_server_user_id = None
        self.doc.battle_timeout = 0
        self.doc.fort_war_clan_id = None
        self.doc.fort_war_start_time = 0
        self.doc.fort_war_end_time = 0

        self.update()

    def update_protect_time_without_defense(self, current_time):
        self.doc.protect_defense_end_time = 0
        self.doc.protect_end_time = current_time + get_block_protect_time(self.doc.block_id)
        self.update()

    def is_in_set_defense_time(self, current_time):
        return self.doc.protect_start_time < current_time <= self.doc.protect_defense_end_time

    def is_in_arrange_time(self, current_time):
        return self.doc.protect_defense_end_time < current_time <= self.doc.protect_end_time

    def is_in_protect_time(self, current_time):
        return self.doc.protect_start_time < current_time <= self.doc.protect_end_time

    def is_other_in_battle(self, server_user_id, current_time):
        return self.doc.battle_server_user_id and self.doc.battle_server_user_id != server_user_id and self.doc.battle_timeout >= current_time

    def is_self_in_battle(self, server_user_id, current_time):
        return self.doc.battle_server_user_id == server_user_id and self.doc.battle_timeout >= current_time

    def update_battle_user(self, clan_id, server_user_id, current_time=0):
        self.doc.battle_clan_id = clan_id
        self.doc.battle_server_user_id = server_user_id
        if current_time > 0:
            self.doc.battle_timeout = current_time + master_battle_field_setting_inst.get_number('battle_field_block_battle_max_time')
            # 同时先更新一次保护时间，防止攻击中途没打完退出
            self.doc.protect_start_time = self.doc.battle_timeout
            self.doc.protect_end_time = self.doc.battle_timeout + get_block_protect_time(self.doc.block_id)
        else:
            self.doc.battle_timeout = 0
        self.update()

    def is_fort_in_battle(self, current_time):
        return self.doc.fort_war_clan_id and current_time < self.doc.fort_war_end_time

    def declare_update_data(self, clan_id, current_time):
        self.doc.fort_war_clan_id = clan_id
        self.doc.fort_war_start_time = current_time
        self.doc.fort_war_end_time = current_time + master_battle_field_setting_inst.get_number('battle_field_fort_war_time')
        # 要塞直接更新保护时间
        self.doc.protect_start_time = self.doc.fort_war_end_time
        self.doc.protect_defense_end_time = self.doc.fort_war_end_time + get_block_protect_set_defense_time()
        self.doc.protect_end_time = self.doc.fort_war_end_time + get_block_protect_time(self.doc.block_id)
        self.update()
