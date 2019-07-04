# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Integer, Dict, Class, String, List, Boolean
from script.common.game_define.hero_def import HeroSnap
from script.common.game_define.user_pet_def import PetSnap


# 据点id定义
ALPHA_FORT_WAR_POINT_ID_GATE = 'gate'           # 据点id - 门
ALPHA_FORT_WAR_POINT_ID_ALCHEMY = 'alchemy'    # 据点id - 炼金术
ALPHA_FORT_WAR_POINT_ID_MAGE = 'mage'           # 据点id - 魔法师
ALPHA_FORT_WAR_POINT_ID_ARCHER = 'archer'       # 据点id - 弓兵团
ALPHA_FORT_WAR_POINT_ID_GUARDIAN = 'guardian'   # 据点id - 守护者
ALPHA_FORT_WAR_POINT_ID_BRICOLE = 'bricole'     # 据点id - 投石器
ALPHA_FORT_WAR_POINT_ID_THRONE = 'throne'       # 据点id - 水晶


ALPHA_FORT_WAR_POINT_ID_LIST = [ALPHA_FORT_WAR_POINT_ID_GATE, ALPHA_FORT_WAR_POINT_ID_ALCHEMY, ALPHA_FORT_WAR_POINT_ID_MAGE, ALPHA_FORT_WAR_POINT_ID_ARCHER,
                                ALPHA_FORT_WAR_POINT_ID_GUARDIAN, ALPHA_FORT_WAR_POINT_ID_BRICOLE, ALPHA_FORT_WAR_POINT_ID_THRONE]

ALPHA_FORT_WAR_STEP2_POINT_ID_LIST = [ALPHA_FORT_WAR_POINT_ID_ALCHEMY, ALPHA_FORT_WAR_POINT_ID_MAGE, ALPHA_FORT_WAR_POINT_ID_ARCHER,
                                      ALPHA_FORT_WAR_POINT_ID_GUARDIAN, ALPHA_FORT_WAR_POINT_ID_BRICOLE]

ALPHA_FORT_WAR_BATTLE_REWARD_WIN = 'battle_win'
ALPHA_FORT_WAR_BATTLE_REWARD_LOSE = 'battle_lose'
ALPHA_FORT_WAR_BATTLE_REWARD_GATE_LAST = 'gate_last_attack'
ALPHA_FORT_WAR_BATTLE_REWARD_THRONE_LAST = 'throne_last_attack'

# 阶段定义
ALPHA_FORT_WAR_STEP_REGISTER = 0    # 报名期
ALPHA_FORT_WAR_STEP_PREPARE = 1     # 准备期
ALPHA_FORT_WAR_STEP_ONGOING = 2     # 进行中
ALPHA_FORT_WAR_STEP_FINISHED = 3    # 已结束

# 赛季重置时刻点
ALPHA_FORT_WAR_SEASON_RESET_DOW = 1         # 赛季重置日期(周一)
ALPHA_FORT_WAR_SEASON_LAST_TIME = 604800    # 赛季持续时间( 7 days)

# 要塞战结果定义
ALPHA_FORT_WAR_RESULT_NONE = 0      # 没结果
ALPHA_FORT_WAR_RESULT_LOSE = 1      # 失败
ALPHA_FORT_WAR_RESULT_WIN = 2       # 胜利

# 展示代表人数
ALPHA_FORT_WAR_SIDE_REP_COUNT = 5

# 坑位范围定义
ALPHA_FORT_WAR_HERO_SLOT_MIN = 1
ALPHA_FORT_WAR_HERO_SLOT_MAX = 5
ALPHA_FORT_WAR_PET_SLOT_MIN = 1
ALPHA_FORT_WAR_PET_SLOT_MAX = 45

# 防守布阵数量定义
ALPHA_FORT_WAR_DEFENSE_MAX_PER_USER = 10

# 赛季初始积分
ALPHA_FORT_WAR_SEASON_INIT_SCORE = 1000
ALPHA_FORT_WAR_LOSE_SCORE = 50
ALPHA_FORT_WAR_WIN_SCORE_MIN = 100
ALPHA_FORT_WAR_WIN_SCORE_FACTOR = 800


# ========================== to client ==========================
class AlphaFortClanRepInfo(ClassObject):
    server_user_id = String(desc='server user id', default='')
    user_name = String(desc='玩家名', default='')
    hero_snap = Class(HeroSnap, desc='英雄信息')
    rank = Integer(desc='排名', default=0)


class AlphaFortWarPointSnap(ClassObject):
    point_id = String(desc='据点id')
    total_count = Integer(desc='据点总量', default=0)
    rest_count = Integer(desc='据点剩余量', default=0)


class AlphaFortWarPointStatus(AlphaFortWarPointSnap):
    is_in_battle = Boolean(desc='是否战斗中', default=False)


class AlphaFortWarSideInfo(ClassObject):
    clan_id = String(desc='公会id', default='')
    clan_name = String(desc='公会名', default='')
    mark = String(desc='公会图标', default='')
    mark_frame = String(desc='公会图标外框', default='')
    defense_count = Integer(desc='防守者数量', default=0)
    rep_list = List(Class(AlphaFortClanRepInfo), desc='公会代表信息')
    fort_point_snap_list = List(Class(AlphaFortWarPointSnap), desc='据点snap')


class AlphaFortDefenseHeroSlotInfo(ClassObject):
    slot_no = Integer(desc='坑位编号', default=0)
    server_user_id = String(desc='玩家server user id')
    class_key = String(desc='class key')
    level = Integer(default=0, desc='等级')
    equipped_costume = String(desc='穿戴时装id', default=None)


class AlphaFortDefensePetSlotInfo(ClassObject):
    slot_no = Integer(desc='坑位编号')
    server_user_id = String(desc='玩家server user id')
    base_key = String(desc='CombatantsBase.key')
    class_key = String(desc='Combatants.key')
    level = Integer(desc='等级', default=0)
    training_key = String(default=None, desc='CombatantsTraining')
    equipped_costume = String(desc='穿戴时装id', default=None)
    bless_key = String(default=None, desc='祝福等级')


class AlphaFortWarChangeDefenseItem(ClassObject):
    slot_no = Integer(desc='坑位')
    ori_slot_no = Integer(desc='原始坑位')


class AlphaFortWarBattleResultUnit(ClassObject):
    server_user_id = String(desc='server user id')
    key = String(desc='hero class key | pet base key')
    rest_hp = Integer(desc='剩余血量', default=0)

# ========================== to client ==========================


class AlphaFortWarSeason(ClassObject):
    season_no = Integer(desc='赛季', default=0)
    season_start_time = Integer(desc='赛季开始时间', default=0)
    season_end_time = Integer(desc='赛季结束时间', default=0)
    last_reset_time = Integer(desc='上一次重置时间', default=0)
    give_reward_time = Integer(desc='结算时间', default=0)


class AlphaFortWarStep(ClassObject):
    step = Integer(desc='阶段', default=ALPHA_FORT_WAR_STEP_FINISHED)
    last_set_time = Integer(desc='上一次设置时间', default=0)


class AlphaFortWarRegisterItem(ClassObject):
    clan_id = String(desc='血盟id', default=None)
    group_no = Integer(desc='组别', default=0)
    register_time = Integer(desc='报名时间', default=0)


class AlphaFortWarRegisterInfo(ClassObject):
    last_reset_time = Integer(desc='上一次重置时间', default=0)
    register_dict = Dict(Class(AlphaFortWarRegisterItem), desc='clan_id: AlphaFortWarRegisterItem')
    group_dict = Dict(List(String(), desc='clan id列表'), desc='str group no => clan id list')


class AlphaFortWarMatch(ClassObject):
    last_reset_time = Integer(desc='上一次重置时间', default=0)
    match_dict = Dict(String(), desc='匹配队列, {A:B, B:A}')


class AlphaFortWarPointSlotPair(ClassObject):
    point_id = String(desc='据点id')
    slot_no = Integer(desc='坑位')


class AlphaFortWarBBDefense(ClassObject):
    last_reset_time = Integer(desc='重置时间')
    point_used_hero_slot = Dict(List(Integer(), desc='slot no list'), desc='point_id => slot no list')
    point_used_pet_slot = Dict(List(Integer(), desc='slot no list'), desc='point_id => slot no list')
    point_hero_defense = Dict(Dict(Class(AlphaFortDefenseHeroSlotInfo), desc='str_slot_no => hero info'), desc='point_id => info dict')
    point_pet_defense = Dict(Dict(Class(AlphaFortDefensePetSlotInfo), desc='str_slot_no => pet info'), desc='point_id => info dict')
    user_hero_defense = Dict(Dict(Class(AlphaFortWarPointSlotPair), desc='hero class key => point slot pair'), desc='server user id => hero dict')
    user_pet_defense = Dict(Dict(Class(AlphaFortWarPointSlotPair), desc='pet base key => point slot pair'), desc='server user id => pet dict')


class AlphaFortWarBattleDefenseHeroUnit(ClassObject):
    hero_snap = Class(HeroSnap, desc='英雄信息')
    rest_hp = Integer(desc='剩余血量', default=0)


class AlphaFortWarBattleDefensePetUnit(ClassObject):
    pet_snap = Class(PetSnap, desc='召唤兽信息')
    rest_hp = Integer(desc='剩余血量', default=0)


class AlphaFortWarPointDetail(ClassObject):
    total_count = Integer(desc='总量', default=0)
    rest_count = Integer(desc='剩余量', default=0)
    update_time = Integer(desc='更新时间', default=0)
    battle_user_count = Integer(desc='当前攻击玩家数量, 第一、三阶段据点使用', default=0)
    point_battle_hero = List(Class(AlphaFortWarBattleDefenseHeroUnit), desc='hero list, 第二阶段据点使用')
    point_battle_pet = List(Class(AlphaFortWarBattleDefensePetUnit), desc='pet list, 第二阶段据点使用')
    battle_server_user_id = String(desc='当前战斗的server user id, 第二阶段据点使用')
    battle_end_time = Integer(desc='战斗结束时间, 第二阶段据点使用', default=0)
    last_attack_server_user_id = String(desc='最后一击玩家server user id')


class AlphaFortFacility(ClassObject):
    facility_name = String(desc='据点id(名字)')
    reinforce_list = List(Integer(), desc='加强经验值列表')


class AlphaFortWarClan(ClassObject):
    season_no = Integer(desc='赛季', default=0)
    group_no = Integer(desc='组别', default=0)
    streak_win_count = Integer(desc='连胜次数', default=0)
    result = Integer(desc='要塞战结果', default=ALPHA_FORT_WAR_RESULT_NONE)
    result_time = Integer(desc='要塞战结果时间', default=0)
    last_reset_time = Integer(desc='上一次重置时间', default=0)
    battle_data_init_time = Integer(desc='第二阶段防守阵容数据是否初始化', default=0)
    rest_defense_count = Integer(desc='剩余防守者数量', default=0)
    point_dict = Dict(Class(AlphaFortWarPointDetail), desc='据点信息, point_id => info')
    facility_info_list = List(Class(AlphaFortFacility), desc='公会建筑信息')
    attend_user_list = List(String(), desc='参与玩家server_user_id列表')


class AlphaFortWarUserInfo(ClassObject):
    last_attack_time = Integer(desc='上一次攻击时间', default=0)
    last_attack_point_id = String(desc='上一次进攻据点id')

