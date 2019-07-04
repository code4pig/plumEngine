# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import time

import script.common.game_define.team_define as team_def
from script.common.db.base_do import ServerIndependantLockDoBase
from script.common.db.class_obj import ClassObject, String, Integer, Dict, Class
from script.common.db.database import db_team


class TeamApplyItem(ClassObject):
    server_user_id = String(desc='申请玩家server user id')
    apply_time = Integer(desc='申请时间', default=0)


class TeamApplyInfo(ClassObject):
    team_id = Integer(desc='队伍id', default=0)
    apply_dict = Dict(Class(TeamApplyItem), desc='申请字典')


class TeamApplyInfoDo(ServerIndependantLockDoBase):
    """
    组队数据
    """
    def __init__(self, context, team_id):
        super(TeamApplyInfoDo, self).__init__(context, team_id)
        self.doc.team_id = team_id

    @classmethod
    def cls(cls):
        return TeamApplyInfo

    @classmethod
    def get_prefix(cls):
        return 'TEAMAPPLY'

    @classmethod
    def get_db(cls):
        return db_team()

    def is_in_apply(self, server_user_id):
        return server_user_id in self.doc.apply_dict and self.doc.apply_dict[server_user_id].apply_time + team_def.TEAM_APPLY_LAST_TIME > time.time()

    def add_team_apply(self, server_user_id):
        self.doc.apply_dict[server_user_id] = TeamApplyItem(server_user_id=server_user_id, apply_time=int(time.time()))
        # 检查过期申请
        self._remove_timeout_apply()
        # 检查申请列表长度
        if len(self.doc.apply_dict) > team_def.TEAM_APPLY_DICT_MAX_COUNT:
            temp_item = None
            for apply_item in self.doc.apply_dict.itervalues():
                if temp_item is None or temp_item.apply_time > apply_item.apply_time:
                    temp_item = apply_item
            self.doc.apply_dict.pop(temp_item.server_user_id)
        self.update()

    def remove_team_apply(self, server_user_id):
        ret = self.doc.apply_dict.pop(server_user_id, None)
        if ret:
            self.update()

    def get_apply_list(self):
        ret_list = []
        time_flag = int(time.time()) - team_def.TEAM_APPLY_LAST_TIME
        for item in self.doc.apply_dict.itervalues():
            if item.apply_time > time_flag:
                ret_list.append(item)
        return ret_list

    def clear_all_apply(self):
        if self.doc.apply_dict:
            self.doc.apply_dict.clear()
            self.update()

    def _remove_timeout_apply(self):
        flag_time = int(time.time()) - team_def.TEAM_APPLY_LAST_TIME
        is_any = False
        for key in self.doc.apply_dict.keys():
            if self.doc.apply_dict[key].apply_time <= flag_time:
                is_any = True
                self.doc.apply_dict.pop(key)
        return is_any