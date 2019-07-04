# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.alpha_fort_war_def import AlphaFortWarMatch


class AlphaFortWarMatchDo(BaseDo):
    def __init__(self, context):
        super(AlphaFortWarMatchDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return AlphaFortWarMatch

    @classmethod
    def get_prefix(cls):
        return 'ALPHAFORTWARMATCH'

    @classmethod
    def get_db(cls):
        return db_game()

    @classmethod
    def is_server_group_do(cls):
        return True

    def reset_match(self, current_time):
        self.doc.last_reset_time = int(current_time)
        self.doc.match_dict.clear()
        self.update()

    def add_match_item(self, clan_id_1, clan_id_2=None):
        self.doc.match_dict[clan_id_1] = clan_id_2
        if clan_id_2:
            self.doc.match_dict[clan_id_2] = clan_id_1
        self.update()
