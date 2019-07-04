# coding=utf8


# Copyright (C) [2017] NCSOFT Corporation. All Rights Reserved.
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will NCSOFT Corporation (“NCSOFT”) be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software subject to acceptance
# and compliance with any agreement entered into between NCSOFT (or any of its affiliates) and the recipient.
# The following restrictions shall also apply:
#
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software.
# 2. You may not modify, alter or redistribute this software, in whole or part, unless you are entitled to
# do so by express authorization in a separate agreement between you and NCSOFT.
# 3. This notice may not be removed or altered from any source distribution.


# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Dict, Class, Number
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase


class MasterBattleFieldSettingRow(ClassObject):
    key = String(desc='상수명')
    value = Number(desc='값. 수.')
    s_value = String(desc='字符串数据')


class MasterBattleFieldSetting(ClassObject):
    version = String(desc='마스터 버전')
    items = Dict(Class(MasterBattleFieldSettingRow), desc='마스터. row')


class MasterBattleFieldSettingDo(MasterDoBase):
    def __init__(self, context):
        super(MasterBattleFieldSettingDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return MasterBattleFieldSetting

    @classmethod
    def get_prefix(cls):
        return 'MST_BattleFieldSetting'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_number(self, key):
        return self.doc.items[key].value

    def get_string(self, key):
        return self.doc.items[key].s_value

    def get_int(self, key):
        return int(self.get_number(key))
