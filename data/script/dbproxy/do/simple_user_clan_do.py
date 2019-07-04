# coding=utf8

from __future__ import unicode_literals

from script.common.data_define import UserClanInfo
from script.common.db.base_do import BaseDo
from script.common.db.database import db_clan


class UserClanDo(BaseDo):
    """
    혈맹원의 정보
    """

    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(UserClanDo, self).__init__(context, user_id)

        self.user_id = user_id

    @classmethod
    def cls(cls):
        return UserClanInfo

    @classmethod
    def get_prefix(cls):
        return 'USRCLAN'

    @classmethod
    def get_db(cls):
        return db_clan()

    def get_server_dependant_id(self):
        return self.server_id
