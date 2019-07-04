# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterBehaviorRow(ClassObject):
    key = String(desc='master behavior key')
    name = String(desc='스킬 이름')
    owner_class = String(desc='스킬 보유 캐릭터 CombatantsBase key')
    type = String(desc='스킬 타입 active/passive/basic/lethal')
    evolve = String(desc='각성 스킬 여부')
    succeed = String(desc='스킬 상속 여부')
    slot = Integer(desc='스킬 위치 영웅:(1,2 : 약티브, 3,4: 패시브, 5: 필살기) 소환수(1,2: 액티브 3: 패시브')
    cat_1 = String(desc='스킬 대분류')
    skill_battle_power = String(desc='스킬에 붙는 전투력의 그룹 아이디')

    def get_index_meta(self):
        """
        인덱싱에 사용할 메타 정보 반환
        :return: dict: {인덱스 이름: 인덱스 컬럼 리스트, ...}
        """
        return {
            'owner': (self.owner_class, self.slot),  # 스킬 보유 캐릭터 기준 인덱싱
            'owner_all': (self.owner_class,)
        }


class MasterBehaviorDo(new_master_do_class(MasterBehaviorRow, 'MST_Behavior')):

    pet_skill_slot_count = 1

    def get_type(self, skill_key):
        try:
            return self.doc.items[skill_key].type
        except KeyError as e:
            return None

    def get_behaviors(self, pet_base_key):
        return (self.get_by_index('owner', pet_base_key, slot)
                for slot in range(1, self.__class__.pet_skill_slot_count + 1))
