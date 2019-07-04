# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Dict
from script.dbproxy.do.master_util import new_master_do_class


class MasterTeamBossTraining(ClassObject):
    key = String(desc='part key')
    atk_speed = Integer(desc='atk speed')
    p_atk = Integer(desc='physical atk')
    m_atk = Integer(desc='magical atk')
    hp = Integer(desc='hp')
    p_def = Integer(desc='physical def')
    res = Integer(desc='magical def')
    pen = Integer(desc='pen')
    cond_dec = Integer(desc='cond dec')
    attr_res = Dict(Integer(), desc='attr res')
    cond_res = Dict(Integer(), desc='cond res')
    cri = Integer(desc='critical')
    eva = Integer(desc='evade')


class MasterTeamBossTrainingDo(new_master_do_class(MasterTeamBossTraining, "MST_TeamBossTraining")):
    pass
