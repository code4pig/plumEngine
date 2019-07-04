# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-06-28 15:38

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_battle_field
from script.common.game_define.battle_field_def import const_battle_field_document_ttl, BattleFieldClanInfo, BattleFieldClanLog


class BattleFieldClanDo(BaseDo):
    def __init__(self, context, season_key, clan_id):
        super(BattleFieldClanDo, self).__init__(context, season_key, clan_id)
        self.doc.season_key = season_key
        self.doc.clan_id = clan_id

    @classmethod
    def cls(cls):
        return BattleFieldClanInfo

    @classmethod
    def get_prefix(cls):
        return 'BF_CLAN'

    @classmethod
    def get_db(cls):
        return db_battle_field()

    @classmethod
    def is_server_group_do(cls):
        return True

    @classmethod
    def get_ttl(cls):
        return const_battle_field_document_ttl

    def get_clan_info(self):
        return self.doc

    def register_field(self, field_id, current_time):
        self.doc.register_field_id = field_id
        self.doc.register_time = current_time
        self.update()

    def cancel_register_field(self):
        self.doc.register_field_id = None
        self.doc.register_time = 0
        self.update()

    def init_own_blocks(self, block_list):
        self.doc.own_blocks = block_list
        self.update()

    def is_own_block(self, field_id, block_id):
        if self.doc.register_field_id == field_id:
            if block_id in self.doc.own_blocks:
                return True
        return False

    def remove_own_block(self, field_id, block_id):
        if field_id != self.doc.register_field_id:
            print '===== [ERROR] ===== remove own block but field not match :', self.doc.register_field_id, field_id
        if block_id in self.doc.own_blocks:
            self.doc.own_blocks.remove(block_id)
            self.update()

    def add_own_block(self, field_id, block_id):
        if field_id != self.doc.register_field_id:
            print '===== [ERROR] ===== add own block but field not match :', self.doc.register_field_id, field_id
        if block_id not in self.doc.own_blocks:
            self.doc.own_blocks.append(block_id)
            self.update()

    def mark_give_season_reward(self, total_items, current_time):
        self.doc.is_give_reward = True
        self.doc.reward_items = total_items
        self.doc.reward_time = current_time
        self.update()

    def add_log(self, log_type, log_time, params):
        log = BattleFieldClanLog()
        log.log_type = log_type
        log.log_time = log_time
        log.param_list = params
        self.doc.log_list.append(log)
        self.update()
