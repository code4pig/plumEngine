# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer
from script.common.exceptions import ExceptionIndexNotExist
from script.dbproxy.do.master_util import new_master_do_class


class MasterTeamBossRow(ClassObject):
    key = String(desc='key. boss key')
    func_type = String(desc='玩法类型标识')
    difficulty = Integer(desc='难度')

    def get_index_meta(self):
        return {
            'func_type': (self.func_type,)
        }


class MasterTeamBossDo(new_master_do_class(MasterTeamBossRow, 'MST_TeamBoss')):
    def get_key_list(self):
        return self.doc.items.keys()

    def get_func_type_key_list(self, func_type):
        try:
            data_list = self.get_by_index('func_type', func_type)
            return [x.key for x in data_list]
        except ExceptionIndexNotExist as e:
            print 'func type %s is not in config' % func_type
            return []
