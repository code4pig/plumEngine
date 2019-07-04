# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer
from script.common.db.database import db_game
from script.common.db.base_do import UnlockedDoBase


class CharacterLogInfo(ClassObject):
    user_id = String(desc='user id')
    total_online_time = Integer(default=0, desc='user total online time')
    last_logout_time = Integer(default=0, desc='user last logout time')


class CharacterLogInfoDo(UnlockedDoBase):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(CharacterLogInfoDo, self).__init__(context, user_id, server_id)
        self.doc.user_id = user_id

    @classmethod
    def cls(cls):
        return CharacterLogInfo

    @classmethod
    def get_prefix(cls):
        return 'CHARACTERLOGINFO'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def update_info(self, online_time, logout_time):
        self.doc.total_online_time += online_time
        self.doc.last_logout_time = logout_time

        self.update()
