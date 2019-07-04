# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Dict, Integer, List, Boolean
from script.dbproxy.do.master_util import new_master_do_class


class MasterItem(ClassObject):
    key = String(desc='아이템의 키(id)')
    name = String(desc='이름')
    type = String(desc='아이템 종류. 무기/방어구/장신구/기술서/재화/재료/영혼석/물약')
    equip_pos = String(desc='아이템 장착 위치. weapon/helm/armor/cloak/gloves/boots/ear/ring')
    rarity = Integer(desc='희구도. 별개수.')
    quality = String(desc='아이템 등급. 고급/일반=high/general')
    option = String(desc='장비품의 옵션 정보')
    set_option = String(desc='장비품의 세트 옵션 정보')
    owner_class = String(desc='사용 가능한 직업군. Combatant 의 key.')
    resource_id = String(desc='리소스 id')
    int_attr = Dict(Integer(), desc='정수로 표시되는 아이템 속성 값. {p_atk: 100, level: 2, ...}')
    str_attr = Dict(String(), desc='문자로 표시되는 아이템 속성 값. {key: 커츠, target: 천재, ...}')
    stage = List(String(), desc='출현 스테이지. [1-1, 2-3, ...]')
    strengthen_rate = String(desc='아이템 강화도 확률 아이디')
    strengthen_stat = String(desc='아이템 강화도 스텟 아이디')
    desc = String(desc='아이템 설명')
    price = Integer(desc='판매 가격')
    imprint_exp = Integer(desc='각인 경험치')
    # add by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-03-29
    # detail: 装备初始属性随机相关
    aofei_int_type = String(desc='装备随机属性类型')
    aofei_int_min = Integer(desc='装备随机属性下限')
    aofei_int_max = Integer(desc='装备随机属性上限')
    # >>add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 增加道具流通属性
    aofei_tradable = Boolean(desc='可交易')
    aofei_start_price = Integer(desc='初始均价')
    aofei_time_tradable = Integer(desc='交易间隔')
    aofei_look_time_trade = Integer(desc='公示期')
    aofei_order_type = String(desc='交易行分类')
    aofei_review_time = Integer(desc="审核时间（秒）")
    # <<add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 增加道具流通属性

    def can_equip_by_hero(self, hero_class_key):
        return self.owner_class in ['Common', hero_class_key]

    def get_index_meta(self):
        """
        인덱싱에 사용할 메타 정보 반환
        :return: dict: {인덱스 이름: 인덱스 컬럼 리스트, ...}
        """
        return {
            'type': (self.type,)  # 스킬 보유 캐릭터 기준 인덱싱
        }


class MasterItemDo(new_master_do_class(MasterItem, 'MST_Items')):
    def get_rarity(self, key):
        return self.doc.items[key].rarity

    def get_type(self, key):
        return self.doc.items[key].type
