# coding=utf8

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.dbproxy.do.masters_global import master_hero_level_inst
from script.common.db.database import db_game
from script.common.game_define.hero_def import Equipped, Hero, PvpAttackDeckDb


class HeroDo(BaseDo):
    deck_slot_count = 5

    def __init__(self, context, user_id, class_key, server_id=None):
        self.server_id = server_id
        super(HeroDo, self).__init__(context, user_id, class_key)

        self.doc.user_id = user_id
        if not self.doc.pvp_attack_deck:
            self.doc.pvp_attack_deck = \
                {'PVP5': PvpAttackDeckDb(), 'PVP10': PvpAttackDeckDb(), 'PVPDM': PvpAttackDeckDb()}

    @classmethod
    def cls(cls):
        return Hero

    @classmethod
    def get_prefix(cls):
        return 'USRHERO'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def get_default_doc(self):
        return Hero(equipped_preset_key='1', equipped_preset={'1': Equipped(), '2': Equipped(), '3': Equipped()})

    @property
    def level(self):
        return master_hero_level_inst.get_level(self.doc.exp)

    def get_equipped_preset(self):
        return self.doc.get_equipped_preset()




