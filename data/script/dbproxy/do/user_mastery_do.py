# coding=utf8

from __future__ import unicode_literals

from script.common.db.database import db_game
from script.common.game_define.mastery_def import MasteryInfo
from script.common.db.base_do import BaseDo


class UserMasteryDo(BaseDo):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(UserMasteryDo, self).__init__(context, user_id)

    @classmethod
    def cls(cls):
        return MasteryInfo

    @classmethod
    def get_prefix(cls):
        return 'USRMASTERY'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id







