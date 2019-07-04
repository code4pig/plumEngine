# coding=utf8

from __future__ import unicode_literals

import time


class RollbackCounterInfo(object):
    def __init__(self, db, key, inc, delta, ttl_period):
        self.db = db
        self.key = key
        self.inc = inc
        self.delta = delta
        self.ttl_period = ttl_period


class InstantBox(object):
    def __init__(self):
        self.box = {}

        self.time_current = None
        self.user_id = None
        self.data_context = None
        self.ticket = None
        self.server_selected = None
        self.server_group = None
        self.server_user_id = None
        self.server_user_seq = 0
        self.ignore_database_timeout = False

        # [RollbackCounterInfo, ...]
        self.rollback_counter = []

        # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-12
        # detail: 增加aofei_account_id, aofei_account_name字段,原user_id字段意义变为玩家(角色)id
        # >>>>>>>>>>>>>
        self.aofei_account_id = None
        self.aofei_account_name = None
        # <<<<<<<<<<<<<

        # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-14
        # detail: 增加游戏业务日志支持
        self.aofei_remote_addr = None

    def set(self, k, v):
        self.box[k] = v

    def get(self, k, default=None):
        return self.box.get(k, default)

    def clear(self):
        self.box = {}

    def make_temporary(self, context, account_id, account_name, user_id, server_selected, ticket=None, time_current=time.time()):
        self.time_current = time_current
        self.user_id = user_id
        self.data_context = context
        self.ticket = ticket
        self.server_selected = server_selected

        # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-12
        # detail: 增加aofei_account_id, aofei_account_name字段,原user_id字段意义变为玩家(角色)id
        # >>>>>>>>>>>>>
        self.aofei_account_id = account_id
        self.aofei_account_name = account_name
        # <<<<<<<<<<<<<

instant_box = InstantBox()
