# coding=utf8

from __future__ import unicode_literals

import uuid

from script.common import exceptions as excp
from script.common.db.class_obj import String, Integer, ClassObject, Dict, Class, List, Boolean


class MasterInventory(ClassObject):
    key = String(desc='아이템 종류. 무기/방어구/장신구/기술서/재화/재료/영혼석/물약')

    inven = String(desc='인벤 저장소')
    cat_1 = String(desc='인벤토리 대분류 ')
    stack = Boolean(desc='아이템 누적 여부')


class Item(ClassObject):
    key = String(desc='인스턴스 키')
    class_key = String(desc='아이템의 클래스. Item 시트의 key')

    @staticmethod
    def new(class_key):
        return Item(key=uuid.uuid4().hex, class_key=class_key)


class Stackable(ClassObject):
    count = Integer(default=0, desc='보유 개수')
    time_add = Integer(default=0, desc='최종 획득 시각. utc.')
    time_tradable = Integer(default=0, desc='可交易的保护时间') #add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-03-17 for 增加道具流通属性


class Equipment(ClassObject):
    key = String(desc='인스턴스 키')
    class_key = String(desc='아이템의 클래스. Item 의 key')

    primary_stat = Dict(Integer(), desc='주스탯')
    primary_option = List(Dict(Integer()), desc='주옵션 { str: 100}, {hp: 200}')
    sub_option = List(Dict(Integer()), desc='보조 옵션. 주 스탯이 아닌 보조 옵션들')
    skill_option = String(desc='아이템의 붙는 스킬 옵션 키')

    strengthen = Integer(desc='현재 장비의 강화도')

    remodeling_chance = Integer(desc='아이템 개조 횟수')
    remodeling_type = String(desc='리모델링 타입 primay / sub')
    remodeling_slot = Integer(desc='옵션 수정 위치 { 주/보조 옵션 : 슬롯 위치')

    curse = Boolean(default=False, desc='아이템 저부 여부 True 일 경우 저주 상태')
    bless = Boolean(default=False, desc='아이템의 축복 여부 True 일 경우 축복 상태')
    lock = Boolean(desc='아이템 잠금 여부')

    equipped = String(desc='이 아이템을 장착한 히어로의 key. 비 장착 중이면 None')
    equipped_preset_key = List(String(), desc='장착된 프리셋의 키. [2, 1, ...]')

    time_add = Integer(default=0, desc='획득 시각. utc.')
    aofei_bind = Boolean(default=False, desc='绑定') #add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 增加道具流通属性
    time_tradable = Integer(default=0, desc='可交易的保护时间') #add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-03-17 for 增加道具流通属性


class Asset(ClassObject):
    """
    유저의 현재 자산 정보
    """
    common = Dict(Integer(), desc='소유한 자산 목록. 아데나/다이아.... {아이템 class key: 개수, ...}')

    ap = Integer(default=0, desc='ap. 이 값에 ap_timestamp 시각 부터 재생된 값을 더해야 현재 ap 가 나온다')
    ap_timestamp = Integer(default=0, desc='마지막 갱신 시각. utc. 이 시각 이후로 값을 재생시킨다')


class Inventory(ClassObject):
    user_id = String(desc='소유 유저의 id')
    server_user_id = String(desc='server_user_id')

    equipment = Dict(Class(Equipment), desc='소유한 장비 목록. {장비 인스턴스 id: 장비 인스턴스 정보, ...}')
    stackable = Dict(Class(Stackable), desc='소유한 누적성 아이템 목록. 999개 제한 {아이템 class_key : 아이템 정보, ...}')

    auto_exchange_version = Integer(default=0, desc='자동 아이템 변환 처리 버전. (연성 재료 강제 교환)')

    def get_equipment(self, instance_key, raise_exception=True):
        """
        인스턴스 키로 조건에 맞는 1개의 장비 아이템의 정보를 리턴한다

        :param instance_key: 가져올 장비의 인스턴스 키
        :param raise_exception: 찾지 못할 경우 예외를 발생시킬 것인지 여부. False 이며 장비가 존재하지 않으면 return None
        """
        result = self.equipment.get(instance_key)

        if not result and raise_exception:
            raise excp.ExceptionItemNotExist(instance_key)

        return result

    def get_equipment_by_class_key(self, class_key):
        """
        클래스 키를 이용하여 장비를 조회한다.
        @param class_key: RK_Master.Items.key
        @return: list(Equipment)
        """
        result = []

        for equipment in self.equipment.itervalues():
            if equipment.class_key == class_key:
                result.append(equipment)

        return result


class ProduceItem(ClassObject):
    key = String(desc='제작 베이스 키, 장비의 Item_key')
    adena = Integer(desc='제작에 필요한 아데나')
    open_recipe = Integer(desc='오픈 레시피 조건')



