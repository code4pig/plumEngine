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

from script.common.db.class_obj import ClassObject, String, Dict, Integer, Float
from script.dbproxy.do.master_util import new_master_do_class


class MasterMasteryStatRow(ClassObject):
    key = String(desc='고유키')
    group = String(desc='상위 분류.마스터리 그룹명')
    property = String(desc='하위 분류')
    star_group = String(desc='별 그룹')
    level = Integer(desc='레벨')
    req_point = Integer(desc='필요 포인트')
    factor = Dict(Float(), desc='증가 스탯')
    factor_local = String(desc='증가 스탯 로컬용')

    def get_index_meta(self):
        """
        인덱싱에 사용할 메타 정보 반환
        :return: dict: {인덱스 이름: 인덱스 컬럼 리스트, ...}
        """
        return {
            'get_stat':  (self.group, self.star_group, self.level),
            'get_star_group': (self.group, self.star_group),
            'get_group': (self.group,)
        }


class MasterMasteryStatDo(new_master_do_class(MasterMasteryStatRow, 'MST_MasteryStat')):
    def __init__(self, data_context):
        super(MasterMasteryStatDo, self).__init__(data_context)

        self.max_count_by_group = {}
        for k, v in self.doc.items.iteritems():
            count = self.max_count_by_group.get(v.group, 0)
            count += v.req_point
            self.max_count_by_group[v.group] = count

        self.max_count_by_star_group = {}
        for k, v in self.doc.items.iteritems():
            count = self.max_count_by_star_group.get((v.group, v.star_group), 0)
            count += v.req_point
            self.max_count_by_star_group[(v.group, v.star_group)] = count

        self.max_level_by_star_group = {}
        for k, v in self.doc.items.iteritems():
            level = self.max_level_by_star_group.get((v.group, v.star_group), 0)
            if level < v.level:
                self.max_level_by_star_group[(v.group, v.star_group)] = v.level

    def get_group_max_point(self, group_id):
        return self.max_count_by_group.get(group_id, 0)

    def get_star_group_max_point(self, group_id, star_group_id):
        return self.max_count_by_star_group.get((group_id, star_group_id), 0)

    def get_used_point(self, group_id, star_group_id, current_level):
        temp = sorted(self.get_by_index('get_star_group', group_id, star_group_id), key=lambda x: int(x.level))

        total_point = 0
        for o in temp:
            if o.level > current_level:
                break

            total_point += o.req_point

        return total_point

    def get_star_group_max_level(self, group_id, star_group_id):
        return self.max_level_by_star_group.get((group_id, star_group_id), 0)
