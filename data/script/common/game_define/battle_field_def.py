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

from script.common.db.class_obj import ClassObject, String, Integer, List, Class, Dict, Boolean, Float
from script.common.game_define.hero_def import HeroSnap
from script.common.game_define.time_util import week_period
from script.common.game_define.user_pet_def import PetSnap
from script.common.game_define.util import enum


const_battle_field_document_ttl = week_period * 2  # 2 주 （2 weeks）

BF_FIELD_BATTLE_CLAN_MAX = 15

BF_FIELD_PRODUCT_SUMMARIZE_CHECK_INTERVAL = 600     # 每600s检查一次(比据点产出小一点)
BF_FIELD_BLOCK_PRODUCT_CHECK_INTERVAL = 1800    # 每1800s产出一次

BF_STEP_BEFORE_REGISTER = 'before_register'
BF_STEP_REGISTER = 'register'
BF_STEP_BEFORE_PREPARE = 'before_prepare'
BF_STEP_PREPARE = 'prepare'
BF_STEP_ARRANGE = 'arrange'
BF_STEP_BATTLE = 'battle'
BF_STEP_FREEZE = 'freeze'

BF_BLOCK_TYPE_NORMAL = 'normal'
BF_BLOCK_TYPE_FORT = 'fort'

BF_NORMAL_BLOCK_USER_MAX_DEFENSE = 10
BF_FORT_BLOCK_USER_MAX_DEFENSE = 10
BF_NORMAL_BLOCK_MAX_DEFENSE = 10
BF_FORT_BLOCK_MAX_DEFENSE = 50

FORT_HERO_SLOT_MIN = 1
FORT_HERO_SLOT_MAX = 5
FORT_PET_SLOT_MIN = 1
FORT_PET_SLOT_MAX = 45

const_battle_field_period_sec = week_period     # 持续时间 一周
const_battle_field_register_begin_sec = 36000   # 10 * 3600, 周1 10:00
const_battle_field_register_end_sec = 421200    # 4 * 86400 + 21 * 3600, 周5 21:00
const_battle_field_prepare_begin_sec = 468000   # 5 * 86400 + 10 * 3600, 周6 10:00
const_battle_field_prepare_end_sec = 505800     # 5 * 86400 + 20 * 3600 + 30 * 60, 周6 20:30
const_battle_field_arrange_begin_sec = const_battle_field_prepare_end_sec   # 周6 20:30
const_battle_field_arrange_end_sec = 507600     # 5 * 86400 + 21 * 3600, 周6 21:00
const_battle_field_battle_begin_sec = const_battle_field_arrange_end_sec    # 周6 21:00
const_battle_field_battle_end_sec = 513000      # 5 * 86400 + 22 * 3600 + 30 * 60, 周6 22:30
const_battle_field_result_sec = const_battle_field_battle_end_sec   # 周6 22:30

# BF_FORT_BLOCK_ID_LIST = [int(bid) for bid in battle_field_setting_constants_inst.get_string('battle_field_fort_block_id_list').split(',')]

battle_field_snapshot_refresh_interval = 30     # snapshot刷新间隔(s)

enum_block_status = enum('NEUTRAL', 'NORMAL', 'BATTLE', 'COOL_DOWN', "FORT_READY", 'FORT_WAR')
enum_battle_field_result_type = enum('LOSE', 'NORMAL_WIN', 'NPC_WIN')

FORT_WAR_POINT_ID_GATE = 'gate'           # 据点id - 门
FORT_WAR_POINT_ID_ALCHEMY = 'alchemy'    # 据点id - 炼金术
FORT_WAR_POINT_ID_MAGE = 'mage'           # 据点id - 魔法师
FORT_WAR_POINT_ID_ARCHER = 'archer'       # 据点id - 弓兵团
FORT_WAR_POINT_ID_GUARDIAN = 'guardian'   # 据点id - 守护者
FORT_WAR_POINT_ID_BRICOLE = 'bricole'     # 据点id - 投石器
FORT_WAR_POINT_ID_THRONE = 'throne'       # 据点id - 水晶


FORT_WAR_POINT_ID_LIST = [FORT_WAR_POINT_ID_GATE, FORT_WAR_POINT_ID_ALCHEMY, FORT_WAR_POINT_ID_MAGE, FORT_WAR_POINT_ID_ARCHER,
                          FORT_WAR_POINT_ID_GUARDIAN, FORT_WAR_POINT_ID_BRICOLE, FORT_WAR_POINT_ID_THRONE]

FORT_WAR_STEP2_POINT_ID_LIST = [FORT_WAR_POINT_ID_ALCHEMY, FORT_WAR_POINT_ID_MAGE, FORT_WAR_POINT_ID_ARCHER,
                                FORT_WAR_POINT_ID_GUARDIAN, FORT_WAR_POINT_ID_BRICOLE]

FORT_BATTLE_REWARD_GATE_LAST = 'gate_last_attack'
FORT_BATTLE_REWARD_THRONE_LAST = 'throne_last_attack'

BLOCK_LOG_NORMAL_CHANGE_DEFENSE = 'normal_change_defense'
BLOCK_LOG_FORT_CHANGE_DEFENSE = 'fort_change_defense'
BLOCK_LOG_FORT_ARRANGE_DEFENSE = 'fort_arrange_defense'

BF_CLAN_LOG_BLOCK_ATK_SUCCESS = 'bf_block_attack_success'
BF_CLAN_LOG_BLOCK_DEF_FAIL = 'bf_block_defense_fail'
BF_CLAN_LOG_FORT_DECLARE = 'bf_fort_declare'
BF_CLAN_LOG_FORT_BE_DECLARED = 'bf_fort_be_declared'
BF_CLAN_LOG_ATK_FORT_POINT_SUCCESS = 'bf_fort_point_attack_success'
BF_CLAN_LOG_DEF_FORT_POINT_FAIL = 'bf_fort_point_defense_fail'
BF_CLAN_LOG_ATK_FORT_SUCCESS = 'bf_fort_attack_success'
BF_CLAN_LOG_DEF_FORT_FAIL = 'bf_fort_defense_fail'


class BattleFieldSeasonStatus(ClassObject):
    season_key = Integer(desc='赛季', default=0)
    season_begin_time = Integer(desc='赛季开始时间', default=0)
    season_end_time = Integer(desc='赛季结束时间', default=0)
    season_step = String(desc='赛季阶段', default=BF_STEP_FREEZE)
    step_begin_time = Integer(desc='阶段开始时间', default=0)
    step_end_time = Integer(desc='阶段结束时间', default=0)
    update_time = Integer(desc='数据更新时间', default=0)


class BattleFieldRegisterClan(ClassObject):
    clan_id = String(desc='公会id')
    rank = Integer(desc='排名', default=0)
    clan_name = String(desc='公会名')
    clan_lv = Integer(desc='公会等级')
    clan_active = Integer(desc='公会活跃度')
    register_time = Integer(desc='报名时间')


class BattleFieldRegisterInfo(ClassObject):
    season_key = Integer(desc='赛季')
    field_id = String(desc='区域id')
    register_clan_dict = Dict(Integer(), desc='报名的公会字典, clan_id => register time')
    is_pass_result = Boolean(desc='是否出结果', default=False)
    pass_clan_dict = Dict(Class(BattleFieldRegisterClan), desc='通过的公会字典, clan_id => clan info')


class BattleFieldClanLog(ClassObject):
    log_type = String(desc='日志类型')
    log_time = Integer(desc='日志时间', default=0)
    param_list = List(String(), desc='参数列表')


class BattleFieldClanInfo(ClassObject):
    clan_id = String(desc='公会id')
    season_key = Integer(desc='赛季')
    register_field_id = String(desc='报名的区域id')
    register_time = Integer(desc='报名时间')
    own_blocks = List(Integer(), desc='拥有的地块编号列表')
    is_give_reward = Boolean(desc='是否已给奖励', default=False)
    reward_items = Dict(Integer(), desc='奖励内容')
    reward_time = Integer(desc='给奖励时间', default=0)
    log_list = List(Class(BattleFieldClanLog), desc='公会相关日志列表')


class FieldProductSummarizeInfo(ClassObject):
    season_key = Integer(desc='赛季')
    field_id = String(desc='区域id')
    last_refresh_flag = Integer(desc='上一次完全刷新flag', default=0)
    last_refresh_time = Integer(desc='上一次刷新时间', default=0)
    product_items = Dict(Integer(), desc='产出道具信息, item id => item count')


class BattleFieldBlockInfo(ClassObject):
    season_key = Integer(desc='赛季')
    field_id = String(desc='区域id')
    block_id = Integer(desc='区块id')
    clan_id = String(desc='所属公会id')
    set_time = Integer(desc='设置时间', default=0)
    protect_defense_end_time = Integer(desc='保护部署防守阵容时间', default=0)
    protect_start_time = Integer(desc='保护开始时间', default=0)
    protect_end_time = Integer(desc='保护结束时间', default=0)
    battle_clan_id = String(desc='战斗中的公会id', default=0)
    battle_server_user_id = String(desc='战斗中的玩家server_user_id')
    battle_timeout = Integer(desc='战斗超时时间戳', default=0)
    fort_war_clan_id = String(desc='攻击该要塞的公会id')
    fort_war_start_time = Integer(desc='要塞战开始时间戳(针对要塞据点)', default=0)
    fort_war_end_time = Integer(desc='要塞战结束时间戳(针对要塞据点)', default=0)


class BattleFieldClanMission(ClassObject):
    mission_type = Integer(desc='군주 명령의 종류')
    expired_dt = Integer(desc='군주 명령이 유효한 시간 utc timestamp')


class BattleFieldDefenseUnit(ClassObject):
    server_user_id = String(desc='玩家server_user_id')
    base_key = String(desc='base key')
    class_key = String(desc='class key')
    is_hero = Boolean(desc='是否是英雄', default=False)
    level = Integer(desc='等级', default=0)
    training = String(desc='养成key,CombatantsTraining.key')
    bless_key = String(desc='祝福key')
    extra = String(desc='其他信息')
    is_dead = Boolean(desc='是否死亡', default=False)
    rest_hp = Integer(desc='剩余血量', default=0)


class BattleFieldBlockInfoToC(ClassObject):
    is_fort = Boolean(desc='是否是要塞', default=False)
    status = Integer(desc='据点状态')
    clan_id = String(desc='公会id')
    clan_mission = Class(BattleFieldClanMission, desc='公会指示')
    protect_end_time = Integer(desc='保护结束时间', default=0)
    battle_server_user_id = String(desc='战斗中的玩家server_user_id')
    battle_timeout = Integer(desc='战斗超时时间戳', default=0)
    fort_war_clan_id = String(desc='攻击该要塞的公会id')
    fort_war_start_time = Integer(desc='要塞战开始时间戳(针对要塞据点)', default=0)
    fort_war_end_time = Integer(desc='要塞战结束时间戳(针对要塞据点)', default=0)
    product_items = Dict(Integer(), desc='据点产出的物品字典')
    last_product_time = Integer(desc='据点上一次产出时间', default=0)
    defense_unit_count = Integer(desc='当前防守单位数量', default=0)
    defense_info = List(Class(BattleFieldDefenseUnit), desc='防守信息')


class BFBlockDefenseLog(ClassObject):
    log_type = String(desc='日志类型')
    log_time = Integer(desc='日志时间', default=0)
    param_list = List(String(), desc='参数列表')


class BattleFieldDefenseUnitBase(ClassObject):
    server_user_id = String(desc='玩家server_user_id')
    base_key = String(desc='base key')
    class_key = String(desc='class key')
    is_hero = Boolean(desc='是否是英雄', default=False)
    is_dead = Boolean(desc='是否死亡', default=False)
    rest_hp = Integer(desc='剩余血量', default=0)
    extra = String(desc='其他信息')


class BattleFieldBlockDefenseInfo(ClassObject):
    user_heroes = Dict(String(), desc='玩家防守英雄列表, server_user_id => hero class key')
    user_pets = Dict(List(String(), desc='pet base key list'), desc='玩家召唤兽列表, server_user_id => pet base key list')
    defense_list = List(Class(BattleFieldDefenseUnitBase), desc='防守列表')
    npc_party_key = Integer(desc='中立怪组id', default=-1)
    neutral_reward = Dict(Integer(), desc='中立怪奖励信息')
    defense_log_list = List(Class(BFBlockDefenseLog), desc='防守变更日志列表')


class BlockProductInfo(ClassObject):
    season_key = Integer(desc='赛季')
    field_id = String(desc='区域id')
    block_id = Integer(desc='区块id')
    last_product_time = Integer(desc='上一次产出时间', default=0)
    product_items = Dict(Integer(), desc='产出道具信息, item id => item count')


class BattleFieldBlockSnapshot(ClassObject):
    block_id = Integer(desc='区块id')
    clan_id = String(desc='公会id')
    is_fort = Boolean(desc='是否是堡垒')
    status = Integer(desc="据点状态", default=enum_block_status.NEUTRAL)
    battle_timeout = Integer(desc='战斗超时时间戳,针对普通据点', default=0)
    fort_war_end_time = Integer(desc='占领战结束时间戳', default=0)
    protect_end_time = Integer(desc='据点保护结束时间', default=0)


class BattleFieldFieldSnapshot(ClassObject):
    season_key = Integer(desc='赛季')
    field_id = String(desc='区域id')
    block_dict = Dict(Class(BattleFieldBlockSnapshot), desc='区块快照信息字典, block_id str => snap info')
    refresh_season_step = String(desc='刷新的阶段')
    refresh_time = Integer(desc='刷新时间', default=0)


class BattleFieldClanMissionList(ClassObject):
    clan_id = String(desc='clan_id')
    season_key = Integer(desc='season_key')

    mission = Dict(Dict(Class(BattleFieldClanMission)), desc='公会指示, {field_id:{block_id str:BattleFieldClanMission, ...}, ...}')

    update_dt = Integer(desc='更新时间')


class BattleFieldUsedPetInfo(ClassObject):
    field_id = String(desc='区域id field_id')
    block_id = Integer(desc='区块id block_id')
    point_id = String(desc='要塞据点id')
    set_time = Integer(desc='设置时间', default=0)


class BattleFieldUserInfo(ClassObject):
    user_id = String(desc='user_id')
    server_user_id = String(desc='server_user_id')
    season_key = Integer(desc='season_key')
    defense_info_dict = Dict(Class(BattleFieldUsedPetInfo), desc='使用的英雄|召唤兽对应的区块信息 {class_key | base_key:BattleUsedPetInfo')
    last_attack_time = Integer(desc='上一次攻击时间', default=0)
    last_attack_block_id = Integer(desc='上一次攻击区块id', default=-1)
    last_attack_point_id = String(desc='上一次进攻要塞据点id')


class BFBattleDefenseChangeInfo(ClassObject):
    server_user_id = String(desc='玩家server_user_id')
    key = String(desc='hero class key| pet base key')
    total_hp = Integer(desc='总血量', default=0)
    rest_hp = Integer(desc='剩余血量', default=0)


class BFBattleDefenseHeroSnap(HeroSnap):
    rest_hp = Integer(desc='剩余血量', default=0)


class BFBattleDefensePetSnap(PetSnap):
    rest_hp = Integer(desc='剩余血量', default=0)


class BFBattleDefenseDeck(ClassObject):
    hero = Class(BFBattleDefenseHeroSnap, desc='英雄')
    pets = List(Class(BFBattleDefensePetSnap), desc='召唤兽列表')

    def set_hero(self, hero_do, inventory_do, rest_hp):
        self.hero = BFBattleDefenseHeroSnap()
        self.hero.load_from_hero(hero_do.doc, inventory_do.doc)
        self.hero.rest_hp = rest_hp

        return self

    def add_pet(self, user_id, server_id, pet, pets_do, rest_hp):
        add_pet = BFBattleDefensePetSnap.make_from_pets(server_id, user_id, pets_do.doc.pets, [pet]).values()[0]
        add_pet.rest_hp = rest_hp
        self.pets.append(add_pet)

        return self


class BattleFieldBlockThumbnail(BattleFieldBlockSnapshot):
    clan_mission = Class(BattleFieldClanMission, desc='公会指示')

    def make_data_from_snapshot(self, snapshot):
        self.block_id = snapshot.block_id
        self.clan_id = snapshot.clan_id
        self.is_fort = snapshot.is_fort
        self.status = snapshot.status
        self.battle_timeout = snapshot.battle_timeout
        self.fort_war_end_time = snapshot.fort_war_end_time
        self.protect_end_time = snapshot.protect_end_time
        return self


class FortDefenseHeroSlotInfo(ClassObject):
    slot_no = Integer(desc='坑位编号', default=0)
    server_user_id = String(desc='玩家server user id')
    class_key = String(desc='class key')
    level = Integer(default=0, desc='等级')
    equipped_costume = String(desc='穿戴时装id', default=None)


class FortDefensePetSlotInfo(ClassObject):
    slot_no = Integer(desc='坑位编号')
    server_user_id = String(desc='玩家server user id')
    base_key = String(desc='CombatantsBase.key')
    class_key = String(desc='Combatants.key')
    level = Integer(desc='等级', default=0)
    training_key = String(default=None, desc='CombatantsTraining')
    equipped_costume = String(desc='穿戴时装id', default=None)
    bless_key = String(default=None, desc='祝福等级')


class FortPointSnap(ClassObject):
    point_id = String(desc='据点id')
    total_count = Integer(desc='据点总量', default=0)
    rest_count = Integer(desc='据点剩余量', default=0)


class FortPointStatus(FortPointSnap):
    is_in_battle = Boolean(desc='是否战斗中', default=False)


class FortFacility(ClassObject):
    facility_name = String(desc='据点id(名字)')
    reinforce_list = List(Integer(), desc='加强经验值列表')


class FortPointSlotPair(ClassObject):
    point_id = String(desc='据点id')
    slot_no = Integer(desc='坑位')


class FortChangeDefenseItem(ClassObject):
    slot_no = Integer(desc='坑位')
    ori_slot_no = Integer(desc='原始坑位')


class FortBattleDefenseHeroUnit(ClassObject):
    hero_snap = Class(HeroSnap, desc='英雄信息')
    rest_hp = Integer(desc='剩余血量', default=0)


class FortBattleDefensePetUnit(ClassObject):
    pet_snap = Class(PetSnap, desc='召唤兽信息')
    rest_hp = Integer(desc='剩余血量', default=0)


class FortBattleResultUnit(ClassObject):
    server_user_id = String(desc='server user id')
    key = String(desc='hero class key | pet base key')
    rest_hp = Integer(desc='剩余血量', default=0)


class FortBeforeBattleDefense(ClassObject):
    point_used_hero_slot = Dict(List(Integer(), desc='slot no list'), desc='point_id => slot no list')
    point_used_pet_slot = Dict(List(Integer(), desc='slot no list'), desc='point_id => slot no list')
    point_hero_defense = Dict(Dict(Class(FortDefenseHeroSlotInfo), desc='str_slot_no => hero info'), desc='point_id => info dict')
    point_pet_defense = Dict(Dict(Class(FortDefensePetSlotInfo), desc='str_slot_no => pet info'), desc='point_id => info dict')
    user_hero_defense = Dict(Dict(Class(FortPointSlotPair), desc='hero class key => point slot pair'), desc='server user id => hero dict')
    user_pet_defense = Dict(Dict(Class(FortPointSlotPair), desc='pet base key => point slot pair'), desc='server user id => pet dict')


class FortPointDetail(ClassObject):
    total_count = Integer(desc='总量', default=0)
    rest_count = Integer(desc='剩余量', default=0)
    update_time = Integer(desc='更新时间', default=0)
    battle_user_count = Integer(desc='当前攻击玩家数量, 第一、三阶段据点使用', default=0)
    point_battle_hero = List(Class(FortBattleDefenseHeroUnit), desc='hero list, 第二阶段据点使用')
    point_battle_pet = List(Class(FortBattleDefensePetUnit), desc='pet list, 第二阶段据点使用')
    battle_server_user_id = String(desc='当前战斗的server user id, 第二阶段据点使用')
    battle_end_time = Integer(desc='战斗结束时间, 第二阶段据点使用', default=0)
    last_attack_server_user_id = String(desc='最后一击玩家server user id')


class BattleFieldFortDefenseInfo(ClassObject):
    rest_defense_count = Integer(desc='剩余防守者数量', default=0)
    is_battle_data_init = Boolean(desc='战斗数据是否初始化', default=False)
    battle_data_init_time = Integer(desc='战斗数据初始化时间', default=0)
    point_detail_dict = Dict(Class(FortPointDetail), desc='据点信息, point_id => info')
    before_battle_defense = Class(FortBeforeBattleDefense, desc='战前防守阵容信息')
    facility_info_list = List(Class(FortFacility), desc='公会建筑信息')
    defense_log_list = List(Class(BFBlockDefenseLog), desc='防守变更日志列表')


# def get_season_range(current_time):
#     # 计算当前时间所处的赛季的开始、结束
#     begin_time = get_week_start_timestamp(current_time)
#     end_time = begin_time + const_battle_field_period_sec
#     return begin_time, end_time
#
#
# def get_season_register_time_range(season_begin_time):
#     return season_begin_time + const_battle_field_register_begin_sec, season_begin_time + const_battle_field_register_end_sec
#
#
# def get_season_prepare_time_range(season_begin_time):
#     return season_begin_time + const_battle_field_prepare_begin_sec, season_begin_time + const_battle_field_prepare_end_sec
#
#
# def get_season_arrange_time_range(season_begin_time):
#     return season_begin_time + const_battle_field_arrange_begin_sec, season_begin_time + const_battle_field_arrange_end_sec
#
#
# def get_season_battle_time_range(season_begin_time):
#     return season_begin_time + const_battle_field_battle_begin_sec, season_begin_time + const_battle_field_battle_end_sec
#
#
# def get_season_freeze_time_range(season_begin_time):
#     return season_begin_time + const_battle_field_result_sec, season_begin_time + const_battle_field_period_sec
#
#
# def get_battle_field_step(season_begin_time, current_time):
#     register_begin, register_end = get_season_register_time_range(season_begin_time)
#     if season_begin_time <= current_time < register_begin:
#         # 报名前阶段
#         return BF_STEP_BEFORE_REGISTER, season_begin_time, register_begin
#     elif register_begin <= current_time < register_end:
#         # 报名阶段
#         return BF_STEP_REGISTER, register_begin, register_end
#     prepare_begin, prepare_end = get_season_prepare_time_range(season_begin_time)
#     if register_end <= current_time < prepare_begin:
#         # 准备期前阶段
#         return BF_STEP_BEFORE_PREPARE, register_end, prepare_begin
#     elif prepare_begin <= current_time < prepare_end:
#         # 准备期
#         return BF_STEP_PREPARE, prepare_begin, prepare_end
#     arrange_begin, arrange_end = get_season_arrange_time_range(season_begin_time)
#     if arrange_begin <= current_time < arrange_end:
#         # 调整期
#         return BF_STEP_ARRANGE, arrange_begin, arrange_end
#     battle_begin, battle_end = get_season_battle_time_range(season_begin_time)
#     if battle_begin <= current_time < battle_end:
#         # 战斗期
#         return BF_STEP_BATTLE, battle_begin, battle_end
#     freeze_begin, freeze_end = get_season_freeze_time_range(season_begin_time)
#     if freeze_begin <= current_time:
#         # 结束冷却期
#         return BF_STEP_FREEZE, freeze_begin, freeze_end
#     print '===== [ERROR] ===== no match battle field step :', current_time, season_begin_time
#     return BF_STEP_FREEZE, season_begin_time, current_time
#
#
# def get_adjoin_block_id_list(field_id, block_id):
#     block_id_list = []
#
#     if block_id < 0:
#         return block_id_list
#     block_count = master_battle_field_inst.get_block_count(field_id)
#     if block_id >= block_count:
#         return block_id_list
#
#     odd_count, even_count = master_battle_field_inst.get_block_size(field_id)
#     block_col = get_block_column(block_id, odd_count, even_count)
#     for temp_id in [block_id - (odd_count + even_count), block_id - even_count, block_id - odd_count,
#                     block_id + odd_count, block_id + even_count, block_id + (odd_count + even_count)]:
#         if 0 < temp_id < block_count and abs(block_col - get_block_column(temp_id, odd_count, even_count)) <= 1:
#             block_id_list.append(temp_id)
#     return block_id_list
#
#
# def get_block_column(block_id, odd_count, even_count):
#     rest = block_id % (odd_count + even_count)
#     if rest < min(odd_count, even_count):
#         return (rest + 1) * 2
#     else:
#         return (rest - min(odd_count, even_count)) * 2 + 1
#
#
# def is_fort(block_id):
#     return block_id in BF_FORT_BLOCK_ID_LIST
#
#
# def get_block_protect_time(block_id):
#     if is_fort(block_id):
#         # 堡垒
#         return battle_field_setting_constants_inst.get_number('battle_field_protect_time_fort')
#     else:
#         return battle_field_setting_constants_inst.get_number('battle_field_protect_time_normal')
#
#
# def get_block_protect_set_defense_time():
#     return battle_field_setting_constants_inst.get_number('battle_field_protect_set_defense_time')
#
#
# def is_step_after_register(step):
#     return step != BF_STEP_BEFORE_REGISTER and step != BF_STEP_REGISTER
#
#
# def get_battle_field_block_status(block_info, current_time):
#     block_is_fort = is_fort(block_info.block_id)
#     if block_info.protect_end_time >= current_time:
#         return enum_block_status.COOL_DOWN
#
#     if block_is_fort:
#         if block_info.fort_war_clan_id and block_info.fort_war_start_time >= current_time > block_info.fort_war_end_time:
#             return enum_block_status.FORT_WAR
#         elif block_info.clan_id:
#             return enum_block_status.FORT_READY
#     else:
#         if block_info.battle_server_user_id and block_info.battle_timeout > current_time:
#             return enum_block_status.BATTLE
#         elif block_info.clan_id:
#             return enum_block_status.NORMAL
#     return enum_block_status.NEUTRAL
#
#
# def get_adjoin_fort_block(field_id, block_id):
#     for adjoin_block_id in get_adjoin_block_id_list(field_id, block_id):
#         if adjoin_block_id in BF_FORT_BLOCK_ID_LIST:
#             return adjoin_block_id
#     return -1
#
#
# def get_side_block_id_by_position(field_id, block_id, position):
#     """
#             1
#         0       2
#             X
#         5       3
#             4
#     """
#     odd_count, even_count = master_battle_field_inst.get_block_size(field_id)
#     side_block_id = 0
#     if position == 0:
#         side_block_id = block_id - even_count
#     elif position == 1:
#         side_block_id = block_id - (odd_count + even_count)
#     elif position == 2:
#         side_block_id = block_id - odd_count
#     elif position == 3:
#         side_block_id = block_id + even_count
#     elif position == 4:
#         side_block_id = block_id + (odd_count + even_count)
#     elif position == 5:
#         side_block_id = block_id + odd_count
#
#     return side_block_id

