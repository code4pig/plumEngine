# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_team
from script.common.db.class_obj import ClassObject, String, Integer


class UserTeam(ClassObject):
    user_id = String(desc='玩家id', default=None)
    team_id = Integer(desc='队伍id', default=0)


class UserTeamDo(BaseDo):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(UserTeamDo, self).__init__(context, user_id)
        self.user_id = user_id

    @classmethod
    def cls(cls):
        return UserTeam

    @classmethod
    def get_prefix(cls):
        return 'USERTEAM'

    @classmethod
    def get_db(cls):
        return db_team()

    def get_server_dependant_id(self):
        return self.server_id

    def update_user_team(self, team_id):
        self.doc.user_id = self.user_id
        self.doc.team_id = team_id
        self.update()

    def has_team(self):
        if self.is_new or not self.doc.team_id:
            return False
        return True

