# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Number, Dict
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase
from script.dbproxy.do.master_util import new_master_do_class


class MasterHeroTrainingRow(ClassObject):
    key = String(desc='연성 고유키')
    base = String(desc='CombatantsBase의 키')
    level = Integer(desc='영웅 레벨')
    # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-05-10
    # detail: 修改战斗力计算公式
    # >>>>>>>>>>>>>
    atk_speed = Number(desc='공격속도')
    # <<<<<<<<<<<<<
    p_atk = Integer(desc='물리공격력')
    m_atk = Integer(desc='마법공격력')
    hp = Integer(desc='체력')
    p_def = Integer(desc='물리방어')
    res = Integer(desc='마법저항')
    pen = Integer(desc='물리관통')
    cond_dec = Integer(desc='상태이상 지속 시간 감소')
    attr_res = Dict(Integer(), desc='속성 저항. 지수화풍흑무.(e_res, w_res, f_res, a_res, d_res, n_res)')
    cond_res = Dict(Integer(), desc='상태이상 저항(sstun_res 스턴 저항,sleep_res 수면 저항,petrify_res 석화 저항,...)')
    cri = Integer(desc='치명타')
    eva = Integer(desc='물리 회피')

    def get_index_meta(self):
        return {
            'get_training_info': (self.base, self.level)
        }


class MasterHeroTrainingDo(new_master_do_class(MasterHeroTrainingRow, 'MST_HeroTraining')):
    def __init__(self, data_context):
        super(MasterHeroTrainingDo, self).__init__(data_context)

    # def get_stats(self, combatants_base_key, level):
    #     stats = Stat()
    #     for training_info in self.get_by_index('get_training_info', combatants_base_key, level):
    #         # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-05-10
    #         # detail: 修改战斗力计算公式
    #         # >>>>>>>>>>>>>
    #         stats.add('atk_speed', training_info.atk_speed)
    #         # <<<<<<<<<<<<<
    #         stats.add('p_atk', training_info.p_atk)
    #         stats.add('m_atk', training_info.m_atk)
    #         stats.add('hp', training_info.hp)
    #         stats.add('p_def', training_info.p_def)
    #         stats.add('res', training_info.res)
    #         stats.add('pen', training_info.pen)
    #         # stats.add('cond_dec', training_info.cond_dec)
    #         # stats.add('attr_res', training_info.attr_res)
    #         # stats.add('cond_res', training_info.cond_res)
    #         stats.add('cri', training_info.cri)
    #         stats.add('eva', training_info.eva)
    #
    #     return stats

