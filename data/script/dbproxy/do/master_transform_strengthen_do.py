# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Dict
from script.dbproxy.do.master_util import new_master_do_class


class MasterTransformStrengthenRow(ClassObject):
    key = String(desc='master TransformStrengthen key')
    base = String(desc='변신의 대상이 되는 소환수의 키 CombatantsBase 의 키')
    level = Integer(desc='변신의 강화 단계')
    scroll = String(desc='해당 변신 의 주문서')
    scroll_count = Integer(desc='주문서 필요 개수')
    ring = String(desc='해당 변신 의 주문 반지')
    ring_count = Integer(desc='반지 필요 개수')
    atk_speed = Integer(desc='攻速')
    p_atk = Integer(desc='物攻')
    m_atk = Integer(desc='法攻')
    hp = Integer(desc='血量')
    p_def = Integer(desc='物防')
    res = Integer(desc='法抗')
    pen = Integer(desc='物穿')
    cond_dec = Integer(desc='被控制衰减')
    attr_res = Dict(Integer(), desc='属性抗性')
    cond_res = Dict(Integer(), desc='控制抗性')
    cri = Integer(desc='暴击')
    eva = Integer(desc='闪避')

    def get_index_meta(self):
        """
        인덱싱에 사용할 메타 정보 반환
        :return: dict: {인덱스 이름: 인덱스 컬럼 리스트, ...}
        """
        return {
            'base': (self.base, self.level)
        }

MasterTransformStrengthenDo = new_master_do_class(MasterTransformStrengthenRow, 'MST_TransformStrengthen')
