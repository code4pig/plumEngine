# -*- coding:utf-8 -*-

from __future__ import unicode_literals


class ClientConnect(object):
    def __init__(self, connect_id):
        self.connect_id = connect_id
        self.server_user_id = None
        self.server_group_id = None

    def bind_user(self, server_user_id, server_group_id):
        self.server_user_id = server_user_id
        self.server_group_id = server_group_id

    def has_bind_user(self):
        return self.server_user_id is not None

    def unbind_user(self):
        self.server_user_id = None
        self.server_group_id = None
