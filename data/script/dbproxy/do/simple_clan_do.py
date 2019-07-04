# coding=utf8

from __future__ import unicode_literals

from script.common.data_define import Clan
from script.common.db.base_do import BaseDo
from script.common.db.database import db_clan
from script.common.game_define.global_def import get_clan_server_id


class ClanDo(BaseDo):
    """
    혈맹의 정보
    """

    def __init__(self, context, clan_id):
        self.server_id = get_clan_server_id(clan_id)
        super(ClanDo, self).__init__(context, clan_id)

        self.clan_id = clan_id

    @classmethod
    def cls(cls):
        return Clan

    @classmethod
    def get_prefix(cls):
        return 'CLAN'

    @classmethod
    def get_db(cls):
        return db_clan()

    def get_server_dependant_id(self):
        return self.server_id
