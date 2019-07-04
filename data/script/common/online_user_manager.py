# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import time


class OnlineUserManager(object):
    def __init__(self):
        self.online_user_dict = {}  # server group id -> {server user id:time}

    def user_online(self, server_group_id, server_user_id):
        if server_group_id not in self.online_user_dict:
            self.online_user_dict[server_group_id] = {}
        if server_user_id not in self.online_user_dict[server_group_id]:
            self.online_user_dict[server_group_id][server_user_id] = time.time()

    def user_offline(self, server_group_id, server_user_id):
        if server_group_id in self.online_user_dict:
            self.online_user_dict[server_group_id].pop(server_user_id, None)

    def is_user_online(self, server_group_id, server_user_id):
        return server_group_id in self.online_user_dict and server_user_id in self.online_user_dict[server_group_id]

    def get_group_online_user_list(self, server_group_id):
        if server_group_id in self.online_user_dict:
            return self.online_user_dict[server_group_id].keys()
        return []
