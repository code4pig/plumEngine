# coding=utf8

# Copyright (C) [2017] NCSOFT Corporation. All Rights Reserved.
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will NCSOFT Corporation (“NCSOFT”) be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software subject to acceptance
# and compliance with any agreement entered into between NCSOFT (or any of its affiliates) and the recipient.
# The following restrictions shall also apply:

# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software.
# 2. You may not modify, alter or redistribute this software, in whole or part, unless you are entitled to
# do so by express authorization in a separate agreement between you and NCSOFT.
# 3. This notice may not be removed or altered from any source distribution.

# coding=utf8

from __future__ import unicode_literals

from script.common.db.database import db_game
from script.dbproxy.do.counter_do import ServerCounter


class CounterMailDo(ServerCounter):
    def __init__(self, server_id, receiver):
        self.server_id = server_id
        super(CounterMailDo, self).__init__(receiver)

    def db(self):
        return db_game()

    @classmethod
    def get_ttl(cls):
        return 0

    def get_server_dependant_id(self):
        return self.server_id
