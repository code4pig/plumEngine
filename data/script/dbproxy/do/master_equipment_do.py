# coding=utf8

from __future__ import unicode_literals

import random

from script.common.db.class_obj import ClassObject, String, Integer, Boolean
from script.dbproxy.do.master_util import new_master_do_class


class MasterEquipment(ClassObject):
    key = String(desc='Equipment 의 key')
    equipment_type = String(desc='Equipment 의 분류')
    primary_option = String(desc='장비의 분류 한손무기 / 양손검 / 활 등등')
    sub_option = String(desc='장비의 옵션 아이디 값')
    sub_count = Integer(desc='서브 옵션의 개수')
    set_option = String(desc='장비의 세트 옵션 아이디 값')
    skill_option = String(desc='장비의 스킬 옵션 값 BahaviorBase 의 값')
    strengthen_rate = String(desc='장비의 강화 확률 아이디')
    strengthen_stat = String(desc='장비의 강화도에 따른 스탯 아이디')
    bless_rate = String(desc='장비의 축복 강화 확률 아이디')
    bless_stat = String(desc='장비의 축복 강화 에 따른 스탯 아이디')
    compose_key = String(desc='합성시 획득하는 포이트의 키 값')
    compose_result = Boolean(desc='합성 결과 등장 여부')
    rarity = Integer(desc='희귀도')
    safety_strengthen = Integer(desc='안전 강화 단계')
    aofei_rand_attr = String(desc="装备初始随机属性")#add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-06-20 for 装备初始随机属性

    def get_index_meta(self):
        return {
            'get_compose_result_items': (self.rarity, self.compose_result, self.equipment_type)
        }


class MasterEquipmentDo(new_master_do_class(MasterEquipment, "MST_Equipment")):
    def get_by_item_key(self, item_key):
        """

        :rtype: MasterEquipment
        """
        return self.doc.items[item_key]

    def get_strengthen_rate(self, class_key):
        return self.doc.items[class_key].strengthen_rate

    def get_strengthen_stat(self, class_key):
        return self.doc.items[class_key].strengthen_stat

    def get_compose_result_item_key(self, rarity, equip_type):

        try:
            items = self.get_by_index('get_compose_result_items', rarity, True, equip_type)
        except Exception as e:
            # 검색해도 결과가 없을 경우
            items = []

        # 혹시 데이터가 없을 경우, 등급에 따른 기본 제공 아이템을 반환한다
        if len(items) == 0:
            from script.dbproxy.do.masters_global import master_constants_inst
            return master_constants_inst.get_string('ComposeResultRarity_{0}'.format(rarity))

        dice = random.randint(0, len(items) - 1)
        return items[dice].key
