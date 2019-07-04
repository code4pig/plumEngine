# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import script.common.game_define.team_define as team_def
from script.common.db.base_do import ServerIndependantLockDoBase
from script.common.db.class_obj import ClassObject, String, Integer, List
from script.common.db.database import db_team


class TeamInfo(ClassObject):
    team_id = Integer(desc='队伍id', default=0)
    server_leader_id = String(desc='队长server user id', default=None)
    leader_name = String(desc='队长名字', default=None)
    create_time = Integer(desc='创建时间', default=0)
    member_id_list = List(String(), desc='成员server user id列表')
    func_type = String(desc='选定的玩法类型', default=None)
    func_flag = String(desc='选定的玩法具体标识', default=None)
    opened_func_type = String(desc='已开启的玩法类型', default=None)


class TeamDo(ServerIndependantLockDoBase):
    """
    组队数据
    """
    def __init__(self, context, team_id):
        super(TeamDo, self).__init__(context, team_id)
        self.team_id = team_id

    @classmethod
    def cls(cls):
        return TeamInfo

    @classmethod
    def get_prefix(cls):
        return 'TEAM'

    @classmethod
    def get_db(cls):
        return db_team()

    def create_new_team(self, team_id, server_user_id, user_name, current_time):
        self.doc.team_id = team_id
        self.doc.server_leader_id = server_user_id
        self.doc.leader_name = user_name
        self.doc.create_time = current_time
        self.doc.member_id_list = [server_user_id]
        self.update()

    def update_team_match_condi(self, func_type, func_flag):
        self.doc.func_type = func_type
        self.doc.func_flag = func_flag
        self.update()

    def is_member_full(self):
        return len(self.doc.member_id_list) >= team_def.TEAM_MAX_MEMBER_NUM

    def add_member(self, server_user_id):
        if self.doc.member_id_list is None:
            self.doc.member_id_list = []
        if server_user_id not in self.doc.member_id_list:
            self.doc.member_id_list.append(server_user_id)
            self.update()

    def member_leave(self, server_user_id):
        if server_user_id in self.doc.member_id_list:
            self.doc.member_id_list.remove(server_user_id)
            self.update()

    def update_team_opened_func(self, func_type):
        self.doc.opened_func_type = func_type
        self.update()
