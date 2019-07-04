# -*- coding:utf8 -*-

from __future__ import unicode_literals

from script.common.db.database import db_team
from script.dbproxy.do.counter_do import Counter


class CounterTeamDo(Counter):
    def __init__(self):
        super(CounterTeamDo, self).__init__("TEAM")

    def db(self):
        return db_team()