# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Integer, String, Dict, Class, List, Boolean
from script.common.game_define.item_def import Equipment
from script.common.game_define.mastery_def import MasteryGroup


class Equipped(ClassObject):
    helm = String(desc='투구. 아이템의 instance key')
    cloak = String(desc='망토. 아이템의 instance key')
    gloves = String(desc='장갑. 아이템의 instance key')
    armor = String(desc='상의. 아이템의 instance key')
    weapon = String(desc='무기. 아이템의 instance key')
    boots = String(desc='신발. 아이템의 instance key')
    ring = String(desc='반지. 아이템의 instance key')
    earring = String(desc='귀걸이. 아이템의 instance key')
    necklace = String(desc='목걸이. 아이템의 instance key')

    def iteritems(self):
        yield 'helm', self.helm
        yield 'cloak', self.cloak
        yield 'gloves', self.gloves
        yield 'armor', self.armor
        yield 'weapon', self.weapon
        yield 'boots', self.boots
        yield 'ring', self.ring
        yield 'earring', self.earring
        yield 'necklace', self.necklace

    items = iteritems

    def values(self):
        yield self.helm
        yield self.cloak
        yield self.gloves
        yield self.armor
        yield self.weapon
        yield self.boots
        yield self.ring
        yield self.earring
        yield self.necklace


class HeroSkills(ClassObject):
    active = Dict(Integer(), desc='액티브 스킬. { behavior key : level}')
    passive = Dict(Integer(), desc='패시브 스킬. { behavior key : level }')
    lethal = Integer(desc='필살기 레벨')

    equip = Dict(String(), desc='장착중인 액티브 스킬. {슬롯 key: 스킬 key}, {1: 쇼크스턴, 2: 이럽션, ...}')


class HeroEquipmentBox(ClassObject):
    item_list = Dict(Integer(), desc='장비의 강화도')
    stat_list = Dict(Integer(), desc='스탯 목록. value 0: 활성 가능한 상태. 1: 활성 상태')
    open = Boolean(default=False, desc='오픈 여부')


class HeroThumbnail(ClassObject):
    class_key = String(desc='영웅의 class_key. 전사/마법사/... Combatant 의 key. 간략 정보에 포함됨.')
    level = Integer(default=0, desc='경험치 레벨')
    equipped_costume = String(desc='착용중인Costume')

    def load_from_hero(self, hero_doc, inventory_doc=None):
        self.class_key = hero_doc.class_key
        self.level = hero_doc.level
        self.equipped_costume = hero_doc.equipped_costume
        return self


class HeroSnap(HeroThumbnail):
    exp = Integer(default=0, desc='경험치')
    equipment = Dict(Class(Equipment), desc='장착중인 장비. {부위(weapon/armor...): 장비 정보, ...}')
    equipped_costume = String(desc='착용중인Costume')
    skill = Dict(Integer(), desc='보유 스킬.')
    equipped_transform = Dict(String(), desc='장착중인 영웅, { 변신 영웅의 키 : 변신 영웅의 강화 키')
    equipment_box = Dict(Class(HeroEquipmentBox), desc='영웅 장비함')
    mastery_group_list = Dict(Class(MasteryGroup), desc='마스터리 목록')
    user_id = String(desc='유저 id')
    server_user_id = String(desc='소유 유져의 server_user_id')
    weapon_strengthen = Integer(default=0, desc="武器强化等级")#add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-11-21 for 强化大师
    other_strengthen = Integer(default=0, desc="全身强化等级")#add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-11-21 for 强化大师

    def load_from_hero(self, hero_doc, inventory_doc=None, mastery_doc=None):
        if not hero_doc.class_key:
            return self

        super(HeroSnap, self).load_from_hero(hero_doc, inventory_doc)

        self.exp = hero_doc.exp

        if inventory_doc: #add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-08-11 for 最低战力通关
            #>>>add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-11-21 for 强化大师
            other_count = 0
            other_strengthen = 0
            for pos, item_instance_key in hero_doc.get_equipped_preset().iteritems():
                self.equipment[pos] = inventory_doc.get_equipment(item_instance_key, raise_exception=False)
                equipment = self.equipment[pos]
                if equipment:
                    if pos == "weapon":
                        self.weapon_strengthen = equipment.strengthen
                    else:
                        other_strengthen = min(equipment.strengthen, other_strengthen) if other_strengthen else equipment.strengthen
                        other_count += 1
            if other_strengthen > 0 and other_count >= 8:
                self.other_strengthen = other_strengthen
            #<<<add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-11-21 for 强化大师
        self.skill = hero_doc.skill

        if hero_doc.equipped_transform is not None:
            transform = hero_doc.equipped_transform
            self.equipped_transform = {transform: hero_doc.transform_list[transform]}

        self.equipment_box = hero_doc.equipment_box

        if mastery_doc:
            self.mastery_group_list = mastery_doc.mastery_group_list

        self.user_id = hero_doc.user_id
        self.server_user_id = hero_doc.server_user_id

        self.equipped_costume = hero_doc.equipped_costume

        return self


class PvpAttackDeckDb(ClassObject):
    pets = List(String(), desc='소환수 목록. 소환수의 base key.')


class Hero(ClassObject):
    user_id = String(desc='소유 유저의 id.')
    server_user_id = String(desc='소유 유져의 server_user_id')

    class_key = String(desc='영웅의 class_key. 전사/마법사/... Combatant 의 key. 간략 정보에 포함됨.')
    created = Integer(desc='영웅 생성 일')

    level = Integer(default=1, desc='레벨')
    exp = Integer(default=0, desc='경험치')

    equipped_preset_key = String(desc='현재 장착 중인 프리셋 키')
    equipped_preset = Dict(Class(Equipped), desc='프리셋 목록. {"1": Equipped, "2":..., ...}')

    skill = Dict(Integer(), desc='보유 스킬.')

    equipped_costume = String(desc='장착중인 코스튬의 키. 미장착 중이면 None. RK_Master.HeroCostume.key')
    costumes = List(String(), desc='보유 코스튬')

    equipped_transform = String(default=None, desc='현재 장착된 변신 영웅의 상태 CombatantsBase.key. 기본 상태일 경우 None')
    transform_list = Dict(String(), desc='현재 보유한 변신 영웅들의 목록 및 상태')

    pvp_attack_deck = Dict(Class(PvpAttackDeckDb), desc='PVP 공격덱, {mode(PVP5/PVP10/PVPDM): 덱, ...}')

    server_user_id_migration = Integer(default=0, desc='서버통합 데이터로 마이그레이션 된 시각 UTC')

    equipment_box = Dict(Class(HeroEquipmentBox), desc='영웅 장비함. key: group_id')
    equipment_box_version = String(default=None, desc='영웅 장비함 버전. 마이그레이션을 위함')

    # >>>add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-07-11 for 英雄装备服装
    equip_costumes = Dict(Integer(), desc="装备服装(key,endtime)")  # add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-07-19 for 英雄装备服装，不存在英雄时临时保存
    equipping_costume = String(default="", desc="穿戴中的服装")

    # <<<add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-07-11 for 英雄装备服装

    def get_level(self):
        return self.level  # master_hero_level_inst.get_level(self.exp)

    def get_equipped_preset(self):
        return self.equipped_preset[self.equipped_preset_key]

    def clear_costumes(self):
        self.costumes = []
