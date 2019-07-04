# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.alpha_fort_war_def import AlphaFortWarRegisterInfo, AlphaFortWarRegisterItem


class AlphaFortWarRegisterDo(BaseDo):
    def __init__(self, context):
        super(AlphaFortWarRegisterDo, self).__init__(context)
        self.context = context

    @classmethod
    def cls(cls):
        return AlphaFortWarRegisterInfo

    @classmethod
    def get_prefix(cls):
        return 'ALPHAFORTWARREGISTER'

    @classmethod
    def get_db(cls):
        return db_game()

    @classmethod
    def is_server_group_do(cls):
        return True

    @classmethod
    def get_ttl(cls):
        return 86400    # one day

    def reset_register_info(self, current_time):
        self.doc.last_reset_time = int(current_time)
        self.doc.register_dict.clear()
        self.doc.group_dict.clear()
        self.update()

    def is_clan_registered(self, clan_id):
        return clan_id in self.doc.register_dict

    def clan_register(self, group_no, clan_id, current_time):
        item = AlphaFortWarRegisterItem()
        item.clan_id = clan_id
        item.group_no = group_no
        item.register_time = current_time
        self.doc.register_dict[clan_id] = item
        str_group_no = str(group_no)
        if str_group_no not in self.doc.group_dict:
            self.doc.group_dict[str_group_no] = []
        self.doc.group_dict[str_group_no].append(clan_id)
        self.update()



