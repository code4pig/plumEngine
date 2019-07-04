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

from script.common.db.class_obj import ClassObject, String, Integer, Boolean
from script.dbproxy.do.master_util import new_master_do_class


class MasterMailRow(ClassObject):
    key = String(desc='master data 의 고유 키')
    category = String(desc='메일의 탭 분류 스트링 값')
    category_code = Integer(desc='메일의 탭 아이디 값 0 : 시스템 1: 친구')
    keep_time = Integer(desc='메일 받은 후 보유 기간')
    reward_all = Boolean(desc='메일 전체 수령 가능 여부')


class MasterMailDo(new_master_do_class(MasterMailRow, 'MST_Mail')):
    def get_reward_type(self, key):
        reward = self.doc.items[key].reward_all
        return reward

    def get_mail_category_code(self, key):
        return self.doc.items[key].category_code

