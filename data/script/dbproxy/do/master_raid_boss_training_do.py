# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterRaidBossTraining(ClassObject):
    key = String(desc='키. 파트+레벨')
    base = String(desc='파트')
    level = Integer(desc='보스 레벨')
    hp = Integer(desc='hp')

    def get_index_meta(self):
        return {
            'base_level': (self.base, self.level)
        }


class MasterRaidBossTrainingDo(new_master_do_class(MasterRaidBossTraining, "MST_RaidBossTraining")):
    pass

