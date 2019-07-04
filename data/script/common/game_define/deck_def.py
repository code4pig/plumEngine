# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, List, Class


class MercenaryDeck(ClassObject):
    server_user_id = String(desc='용병의 server_user_id')
    user_id = String(desc='용병의 아이디 user_id')
    pet = String(desc='용병 소환수의 소환수 키')


class CommonAttackDeck(ClassObject):
    hero = String(desc='공격 댁 영웅의 정보. hero_class_key')
    pets = List(String(), desc='공격 덱 소환수의 정보. pet_base_key')
    mercenary = Class(MercenaryDeck, desc='공격 덱 용병')


class CommonAttackDeckMultiMercenary(ClassObject):
    hero = String(desc='공격 댁 영웅의 정보. hero_class_key')
    pets = List(String(), desc='공격 덱 소환수의 정보. pet_base_key')
    mercenary_list = List(Class(MercenaryDeck, desc='공격 덱 용병'), desc='雇佣兵列表')
