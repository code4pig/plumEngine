# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Integer, Dict
from script.common.db.database import db_game
from script.common.db.base_do import ServerIndependantUnlockDoBase


class LogServerOnline(ClassObject):
    online_num_dict = Dict(Integer(), desc='server online count dict')


class LogServerOnlineDo(ServerIndependantUnlockDoBase):
    def __init__(self, context):
        super(LogServerOnlineDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return LogServerOnline

    @classmethod
    def get_prefix(cls):
        return 'ONLINELIST'

    @classmethod
    def get_db(cls):
        return db_game()

    @classmethod
    def is_server_group_do(cls):
        return True

    def get_online_num(self, server_group_id):
        if server_group_id not in self.doc.online_num_dict:
            return 0
        return self.doc.online_num_dict[server_group_id]

    def set_online_num(self, server_group_id, num):
        self.doc.online_num_dict[server_group_id] = num
        self.update()
