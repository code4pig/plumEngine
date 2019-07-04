# coding=utf8


# Copyright (C) [2017] NCSOFT Corporation. All Rights Reserved.
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will NCSOFT Corporation (“NCSOFT”) be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software subject to acceptance
# and compliance with any agreement entered into between NCSOFT (or any of its affiliates) and the recipient.
# The following restrictions shall also apply:
#
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software.
# 2. You may not modify, alter or redistribute this software, in whole or part, unless you are entitled to
# do so by express authorization in a separate agreement between you and NCSOFT.
# 3. This notice may not be removed or altered from any source distribution.


# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Dict, Class, List
from script.common.game_define.mastery_def import MasteryGroup


class PetEquipment(ClassObject):
    item_id = String(desc='소환수 아이템의 아이디')
    stat_id = String(desc='소환수 아이템의 스탯 아이디')
    grade = String(desc='소환수 장비의 등급')
    step = Integer(desc='소환수 장비의 단계')
    level = Integer(desc='소환수 장비의 레벨')


class SubEquipment(PetEquipment):
    exp = Integer(desc='소환수 엠블렘 및 비급의 의 경험치')


class PetThumbnail(ClassObject):
    base_key = String(desc='소환수 베이스 키. CombatantsBase.key')
    class_key = String(desc='소환수 등급별 키. Combatants.key')
    level = Integer(desc='경험치 레벨')
    training_key = String(default=None, desc='소환수의 연성 클래스 키 CombatantsTraining')
    costume = String(desc='장착중인 코스튬의 키. 미장착 중이면 None. RK_Master.Costume.key')
    bless_exp = Integer(default=0, desc='소환수의 축복 상태 값')
    bless_key = String(default=None, desc='소환수의 축복 등급 상태')
    power = Integer(default=0, desc='소환수 전투력')

    primary_equipment = Dict(Class(PetEquipment), desc='소환수의 장비 정보')
    sub_equipment = Dict(Class(SubEquipment), desc='소환수의 장비 정보')
    pet_power_list = Dict(Integer(), desc='컨텐츠별 소환수 전투력')

    def load_from_pet(self, server_id, user_id, pet_base_key, pet):
        self.base_key = pet_base_key
        self.class_key = pet.class_key
        self.training_key = pet.training_key
        self.level = pet.level
        self.costume = pet.costume
        self.bless_exp = pet.bless_exp
        self.bless_key = pet.bless_key
        self.power = pet.power
        self.primary_equipment = pet.primary_equipment
        self.sub_equipment = pet.sub_equipment
        self.pet_power_list = pet.pet_power_list

        return self


class PetSnap(PetThumbnail):
    user_id = String(desc="归属者ID")  # add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-11-01 for 合版本召唤兽时装
    server_user_id = String(desc='server user id')  # add by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2018-01-25，增加server user id
    skill = Dict(Integer(), desc='보유 스킬. {스킬 키: 스킬 레벨, ...}')
    destiny = Dict(List(Integer()), desc='숙명. 완료 인덱스 리스트. 딕셔너리키 : AchievementCombatants.destiny')

    primary_equipment = Dict(Class(PetEquipment), desc='소환수의 장비 정보')
    sub_equipment = Dict(Class(SubEquipment), desc='소환수의 장비 정보')
    mastery_group_list = Dict(Class(MasteryGroup), desc='마스터리 목록')

    def __init__(self, *arg, **kwargs):
        super(PetSnap, self).__init__(*arg, **kwargs)
        self.check = False

    def load_from_pet(self, server_id, user_id, pet_base_key, pet, mastery_doc=None):
        super(PetSnap, self).load_from_pet(server_id, user_id, pet_base_key, pet)

        # self.skill = dict((skill.key, skill.level) for skill in pet.skill)
        self.user_id = user_id  # add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-11-01 for 合版本召唤兽时装
        self.server_user_id = pet.server_user_id    # add by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2018-01-25，增加server user id
        self.skill = pet.skill
        self.destiny = pet.destiny
        self.primary_equipment = pet.primary_equipment
        self.sub_equipment = pet.sub_equipment
        self.mastery_group_list = mastery_doc.mastery_group_list
        self.pet_power_list = pet.pet_power_list

        return self

    def get_power(self, contents='normal'):
        return self.pet_power_list.get(contents, self.power)


class Pet(ClassObject):
    class_key = String(desc='소환수의 클래스. Combatant 의 key.')
    created = Integer(desc='소환수 생성 일')
    training_key = String(default=None, desc='소환수의 연성 클래스 키 CombatantsTraining')
    user_id = String(desc='소유 유저의 id')
    server_user_id = String(desc='소유 유져의 server_user_id')
    exp = Integer(default=0, desc='exp')
    skill = Dict(Integer(), desc='보유 스킬.')
    costume = String(default="", desc='장착중인 코스튬의 키. 미장착 중이면 None. RK_Master.Costume.key')   # add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-28 for 召唤兽时装，默认时装为""
    destiny = Dict(List(Integer()), desc='숙명. 완료 인덱스 리스트. 딕셔너리키 : AchievementCombatants.destiny')
    bless_exp = Integer(default=0, desc='소환수의 축복 상태 값')
    bless_key = String(default=None, desc='소환수의 축복 등급 상태')
    power = Integer(default=0, desc='소환수 전투력')

    primary_equipment = Dict(Class(PetEquipment), desc='소환수의 장비 정보')
    sub_equipment = Dict(Class(SubEquipment), desc='소환수의 장비 정보')

    pet_power_list = Dict(Integer(), desc='컨텐츠별 소환수 전투력')

    def get_power(self, content='normal'):
        return self.pet_power_list.get(content, self.power)


class Pets(ClassObject):
    user_id = String(desc='소유 유저의 id')
    pets = Dict(Class(Pet), desc='소유한 소환수 목록. {소환수 base_class_key: 소환수 정보, ...}')
    costumes = Dict(List(String()), desc='보유한 소환수 코스튬 목록. {소환수 base_class_key: [코스튬1, 코스튬2], ...}')
    diamond_training_count = Integer(desc='일 다이아 연성 가능 횟수')
    diamond_training_cool_time = Integer(desc='마지막 업데이트 일자')

    server_user_id_migration = Integer(default=0, desc='서버통합 데이터로 마이그레이션 된 시각 UTC')
