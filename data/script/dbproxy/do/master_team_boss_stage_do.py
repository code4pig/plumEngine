# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.exceptions import ExceptionIndexNotExist
from script.common.db.class_obj import ClassObject, String
from script.dbproxy.do.master_util import new_master_do_class


class MasterTeamBossStageRow(ClassObject):
    key = String(desc='副本key')
    boss_key = String(desc='boss key')

    def get_index_meta(self):
        return {
            'boss_key': (self.boss_key,)
        }


class MasterTeamBossStageDo(new_master_do_class(MasterTeamBossStageRow, 'MST_TeamBossStage')):
    def get_stages_by_boss_key(self, boss_key):
        try:
            return self.get_by_index('boss_key', boss_key)
        except ExceptionIndexNotExist:
            return []
