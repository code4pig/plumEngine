# coding=utf8

from __future__ import unicode_literals

import bisect

from script.common import exceptions as excp
from script.common.db.class_obj import ClassObject, String, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterUserLevelRow(ClassObject):
    key = String(desc='레벨')

    exp = Integer(desc='필요 누적 경험치')
    max_ap = Integer(desc='max ap')
    give_ap = Integer(desc='레벨업 시 지급하는 ap 양')

    @property
    def level(self):
        return int(self.key)


class MasterUserLevelDo(new_master_do_class(MasterUserLevelRow, 'MST_MasterLevel')):
    def __init__(self, data_context):
        super(MasterUserLevelDo, self).__init__(data_context)

        # 경험치를 이용해 row 를 찾기 위한 index
        self.sorted_by_exp = sorted([row for row in self.doc.items.itervalues()], key=lambda x: x.exp)
        self._sorted_index_by_exp = [row.exp for row in self.sorted_by_exp]

    def get_by_exp(self, exp):
        """
        주어진 누적 경험치 값에 해당하는 row 를 반환한다.
        :param exp: 찾을 누적 경험치
        :return: MasterUserLevelRow
        :rtype: MasterUserLevelRow
        """
        try:
            return self.sorted_by_exp[bisect.bisect(self._sorted_index_by_exp, exp)]
        except IndexError as e:
            raise excp.ExceptionExceedMaxExp(exp)

    def get_max_exp_of_level(self, level):
        return self.doc.items[str(level)].exp - 1

    def get_max_exp(self):
        return self.sorted_by_exp[-1].exp - 1
