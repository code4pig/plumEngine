# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from script.common.db.class_obj import ClassObject, String, Integer, List, Class, Boolean, Dict, Number, Float
from script.common.game_define.deck_def import CommonAttackDeckMultiMercenary
from script.common.game_define.hero_def import HeroSnap

TEAM_BOSS_STEP_FIRST = 0
TEAM_BOSS_STEP_SECOND = 1
TEAM_BOSS_STEP_ALL_DONE = 2

BATTLE_RESULT_TYPE_FINISH = 1
BATTLE_RESULT_TYPE_TIMEOUT = 2
BATTLE_RESULT_TYPE_FAIL = 3

TEAM_BOSS_BATTLE_STEP_INIT = 0
TEAM_BOSS_BATTLE_STEP_GOING = 1
TEAM_BOSS_BATTLE_STEP_DONE = 2

TEAM_BOSS_BATTLE_INIT_MAX_TIME = 20     # 组队boss战斗初始化等待最长时间


# group 相关定义
class CombatantGroupDef(object):
    COMBATANT_GROUP_HERO = 'HERO'
    COMBATANT_GROUP_PET = 'PET'
    COMBATANT_GROUP_MONSTER = 'MONSTER'
    COMBATANT_GROUP_NPC = 'NPC'
    COMBATANT_GROUP_TRANSFORM = 'TRANSFORM'
    COMBATANT_GROUP_BOSS = 'BOSS'
    COMBATANT_GROUP_FIELD_EFFECT = 'FIELD_EFFECT'
    COMBATANT_GROUP_TU_HERO = 'TU_HERO'
    COMBATANT_GROUP_TU_PET = 'TU_PET'
    COMBATANT_GROUP_TU_MONSTER = 'TU_MONSTER'
    COMBATANT_GROUP_TU_TRANSFORM = 'TU_TRANSFORM'


# stat 定义
class StatDef(object):
    STAT_DEF_STR = 'str'
    STAT_DEF_DEX = 'dex'
    STAT_DEF_INT = 'int'
    STAT_DEF_CON = 'con'
    STAT_DEF_ATK_SPEED = 'atk_speed'
    STAT_DEF_P_ATK = 'p_atk'
    STAT_DEF_M_ATK = 'm_atk'
    STAT_DEF_HP = 'hp'
    STAT_DEF_P_DEF = 'p_def'
    STAT_DEF_RES = 'res'
    STAT_DEF_PEN = 'pen'
    STAT_DEF_COND_DEC = 'cond_dec'
    STAT_DEF_CRI = 'cri'
    STAT_DEF_EVA = 'eva'
    STAT_DEF_BOSS_ATK = 'boss_atk'
    STAT_DEF_CRI_DMG = 'cri_dmg'
    STAT_DEF_SKILLGAUGE = 'skillgauge'
    STAT_DEF_EXP = 'exp'
    STAT_DEF_ADENA = 'adena'
    STAT_DEF_HIGHBOX = 'highbox'
    STAT_DEF_FIRE = 'fire'
    STAT_DEF_WATER = 'water'
    STAT_DEF_WIND = 'wind'
    STAT_DEF_LAND = 'land'
    STAT_DEF_DARKNESS = 'darkness'
    STAT_DEF_STUN = 'stun'
    STAT_DEF_SLEEP = 'sleep'
    STAT_DEF_PETRIFY = 'petrify'
    STAT_DEF_FREEZE = 'freeze'
    STAT_DEF_CHARM = 'charm'
    STAT_DEF_BIND = 'bind'
    STAT_DEF_TERRIFY = 'terrify'
    STAT_DEF_SILENCE = 'silence'
    STAT_DEF_EXPEL = 'expel'
    STAT_DEF_COND_RES_ALL = 'cond_res_all'
    STAT_DEF_AGGRO = 'aggro'
    STAT_DEF_P_ATK_PERCENT = 'p_atk_percent'
    STAT_DEF_M_ATK_PERCENT = 'm_atk_percent'
    STAT_DEF_HP_PERCENT = 'hp_percent'
    STAT_DEF_P_DEF_PERCENT = 'p_def_percent'
    STAT_DEF_RES_PERCENT = 'res_percent'
    STAT_DEF_CRITICAL_PERCENT = 'critical_percent'
    STAT_DEF_P_IMMUNE = 'p_immune_percent'
    STAT_DEF_M_IMMUNE = 'm_immune_percent'
    STAT_DEF_PVP_HP_UP_RATE = 'pvp_hp_up_rate'

    STAT_DEF_COND_RES = 'cond_res'
    STAT_DEF_ATTR_RES = 'attr_res'


class StatFactorDef(object):
    STAT_FACTOR_NONE = None
    STAT_FACTOR_STR = 'str'
    STAT_FACTOR_DEX = 'dex'
    STAT_FACTOR_INT = 'int'
    STAT_FACTOR_CON = 'con'
    STAT_FACTOR_FACTOR = 'factor'


class EnumAttrTypeDef(object):
    NONE = 'NONE'
    FIRE = 'FIRE'
    WATER = 'WATER'
    WIND = 'WIND'
    LAND = 'LAND'
    DARKNESS = 'DARKNESS'
    MAX = 'MAX'

    all_attr_type_list = [NONE, FIRE, WATER, WIND, LAND, DARKNESS]


class CombatantStatusConstDef(object):
    CRI = 650.0
    DEF = 517.0
    PEN = 479.0
    EVA = 774.0
    RES = 734.0
    DEC = 349.0
    ATTR_RES = 173.0
    DEFAULT_ATTR_RES = 87.0
    ATK_SPEED = 117.0
    CRI_DAMAGE = 1.5
    MES_RES = 431.0

    CHARGE = 500.0
    CHARGE_FRONT_ATK = 1.0
    CHARGE_MID_ATK = 1.0
    CHARGE_BACK_ATK = 1.0
    CHARGE_FRONT_DAMAGE = 1.0
    CHARGE_MID_DAMAGE = 1.0
    CHARGE_BACK_DAMAGE = 1.0
    CHARGE_TURN = 50.0
    CHARGE_PHASE = 200.0
    CHARGE_KILL = 200.0
    CHARGE_FIRE_SKILL = 1.0
    CHARGE_DEAD = 200.0

    PHY_DAMAGE_FREEZED = 1.2
    MAG_DAMAGE_PETRIFIED = 1.2
    PHY_DAMAGE_TRANSFORMED = 1.2
    MAG_DAMAGE_TRANSFORMED = 1.2
    MAG_CRI_TERRIFIED = 1.1


class MasteryGroupIdDefine(object):
    MASTERY_GROUP_ID_HERO = 'Hero'
    MASTERY_GROUP_ID_TRIBE = 'Tribe'
    MASTERY_GROUP_ID_CONTENTS = 'Contents'
    MASTERY_GROUP_ID_CLASS = 'Class'


class ContentsGroupDefine(object):
    ALL = 'all'
    PVE = 'pve'
    PVP = 'pvp'
    CLAN = 'clan'


class Combatant(ClassObject):
    key = String(desc='唯一key')
    base = String(desc='base key')
    name = String(desc='名字')
    res_id = String(desc='res_id,资源id')
    rarity = Integer(desc='rarity,品阶')
    str = Integer(desc='str,力量', default=0)
    dex = Integer(desc='dex,敏捷', default=0)
    int = Integer(desc='int,智力', default=0)
    con = Integer(desc='con,体质', default=0)
    move_speed = Number(desc='移动速度', default=0)
    atk_speed = Number(desc='攻击速度', default=0)
    p_atk = Integer(desc='物理攻击', default=0)
    m_atk = Integer(desc='魔法攻击', default=0)
    hp = Integer(desc='血量', default=0)
    p_def = Integer(desc='物理防御', default=0)
    res = Integer(desc='魔法抵抗', default=0)
    pen = Integer(desc='物理穿透', default=0)
    cond_dec = Integer(desc='被控制衰减', default=0)
    cri = Integer(desc='暴击', default=0)
    eva = Integer(desc='闪避', default=0)
    attr_res = Dict(Integer(), desc='属性抗性')
    cond_res = Dict(Integer(), desc='控制抗性')
    field_effect_immune = List(String(), desc='场景效果免疫')
    cri_damage = Float(desc='暴击伤害', default=0.0)
    base_gauge = Integer(desc='技能槽', default=0)
    level = Integer(desc='等级', default=0)
    aggro = Integer(desc='仇恨值', default=0)
    cri_rate = Float(desc='暴击率', default=0.0)
    p_immune = Float(desc='物攻伤害减免', default=0.0)
    m_immune = Float(desc='法攻伤害减免', default=0.0)
    cond_res_all = Float(desc='全部控制抗性', default=0.0)


class CombatantStatus(ClassObject):
    # main stat
    str = Float(desc='力量', default=0.0)
    dex = Float(desc='敏捷', default=0.0)
    int = Float(desc='智力', default=0.0)

    # sub stat
    phy_atk = Float(desc='物攻', default=0.0)
    mag_atk = Float(desc='法攻', default=0.0)
    cri = Float(desc='暴击', default=0.0)
    cri_inc = Float(desc='暴击加成', default=0.0)
    phy_pen = Float(desc='物理穿透', default=0.0)
    phy_def = Float(desc='物防', default=0.0)
    mag_res = Float(desc='法抗', default=0.0)
    eva = Float(desc='闪避', default=0.0)
    cur_hp = Float(desc='当前血量', default=0.0)
    max_hp = Float(desc='最大血量', default=0.0)
    cond_dec = Float(desc='异常状态时间减少', default=0.0)
    move_speed = Float(desc='移速', default=0.0)
    atk_speed = Float(desc='攻速', default=0.0)
    aggro = Float(desc='仇恨值', default=0.0)
    high_power = Float(desc='', default=0.0)
    attr_res = Dict(Float(), desc='属性抗性')
    mesmerize_res = Dict(Float(), desc='控制抗性')
    field_immune = List(String(), desc='场景效果免疫')

    # develop stat
    class_immune = Dict(Float(), desc='类型攻击免疫')
    attr_immune = Dict(Float(), desc='属性攻击免疫')
    eva_rate = Float(desc='闪避率', default=0.0)
    mes_eva_rate = Float(desc='控制闪避率', default=0.0)
    taunt = Float(desc='嘲讽值', default=0.0)

    # caster
    mesmerize = List(String(), desc='异常状态列表')
    cri_rate = Float(desc='暴击率', default=0.0)

    # active skill charge rate
    charge_turn_rate = Float(desc='主动技能恢复比例', default=0.0)


class SimpleCombatantData(ClassObject):
    key = String(desc='combatant key')
    base_key = String(desc='combatant base key')
    lv = Integer(desc='等级')
    training = Integer(desc='培养等级')
    id = Integer(desc='战斗单位id')
    add_gauge = Float(desc='技能槽')
    default_status = Class(CombatantStatus, desc='初始状态')


class TeamBossBattleUnitHero(ClassObject):
    hero_snap = Class(HeroSnap, desc='hero snap')
    combatant_data = Class(SimpleCombatantData, desc='战斗数据')
    transform_combatant_data = Class(SimpleCombatantData, desc='变身战斗数据')


class TeamBossBattleUnitBoss(ClassObject):
    combatant_data = Class(SimpleCombatantData, desc='战斗数据')
    dead_part_list = List(String(), desc='已死亡部位列表')


class TeamBossFirstStageDetail(ClassObject):
    stage_id = String(desc='副本id', default=None)
    is_finish = Boolean(desc='是否已完成', default=False)
    battle_server_mem_id = String(desc='正在战斗中的玩家server user id', default=None)
    battle_mem_name = String(desc='正在战斗的玩家名', default=None)
    battle_mem_hero_key = String(desc='正在战斗的玩家主角id', default=None)
    battle_start_time = Integer(desc='战斗开始时间', default=0)
    battle_end_time = Integer(desc='战斗结束时间', default=0)
    deck = Class(CommonAttackDeckMultiMercenary, desc='战斗阵容信息')


class TeamBossFirstDetail(ClassObject):
    is_finish = Boolean(desc='是否已完成', default=True)
    stage_dict = Dict(Class(TeamBossFirstStageDetail), desc='第一阶段所有副本信息')


class TeamBossPartDetail(ClassObject):
    part_key = String(desc='boss部位key, part表key')
    cur_hp = Integer(desc='当前血量')
    max_hp = Integer(desc='最大血量')
    is_finish = Boolean(desc='是否已完成', default=True)


class TeamBossSecondDetail(ClassObject):
    is_finish = String(desc='是否已结束', default=True)
    battle_unique_id = String(desc='战斗唯一id', default=None)
    attack_part = String(desc='当前攻击的部位key', default=None)
    battle_start_time = Integer(desc='战斗开始时间', default=0)
    battle_real_start_time = Integer(desc='战斗实际开始时间', default=0)
    battle_end_time = Integer(desc='战斗结束时间', default=0)
    part_dict = Dict(Class(TeamBossPartDetail), desc='boss副本详细信息')


class TeamBossDetail(ClassObject):
    team_id = Integer(desc='队伍id', default=0)
    unique_id = String(desc='team boss唯一id', default=None)
    func_type = String(desc='team boss func', default=None)
    boss_key = String(desc='boss key', default=None)
    create_time = Integer(desc='创建时间', default=0)
    end_time = Integer(desc='结束时间', default=0)
    ready_member_list = List(String(), desc='已准备的成员server user id列表')
    first_step = Class(TeamBossFirstDetail, desc='第一阶段详细信息')
    second_step = Class(TeamBossSecondDetail, desc='第二阶段详细信息')


class TeamBossBattleMember(ClassObject):
    server_user_id = String(desc='玩家server user id')
    is_off = Boolean(desc='是否断线', default=False)
    is_init_ok = Boolean(desc='是否初始化完成', default=False)
    is_dead = Boolean(desc='是否死亡', default=False)
    battle_data = Class(TeamBossBattleUnitHero, desc='战斗数据')


class TeamBossBattleDetail(ClassObject):
    battle_unique_id = String(desc='战斗唯一id')
    team_boss_unique_id = String(desc='team boss唯一id')
    battle_status = Integer(desc='战斗状态(0-准备期,1-进行中,2-已结束)', default=0)
    start_time = Integer(desc='开始时间', default=0)
    real_start_time = Integer(desc='实际开始时间', default=0)
    end_time = Integer(desc='结束时间', default=0)
    ctrl_server_user_id = String(desc='当前控制的玩家id', default=None)
    member_data_dict = Dict(Class(TeamBossBattleMember), desc='战斗成员信息')
    boss_data = Class(TeamBossBattleUnitBoss, desc='boss信息')
    server_group_id = String(desc='服务器server group id')
    team_id = Integer(desc='队伍id')
    server_leader_id = String(desc='队长server user id')
    op_list = List(String(), desc='操作列表')


class FortWarBattleInitTempData(ClassObject):
    self_clan_id = String(desc='自己公会id')
    enemy_clan_id = String(desc='敌方公会id')
    point_id = String(desc='据点id')
    total_hp = Integer(desc='总血量')
    rest_hp = Integer(desc='剩余血量')
    end_time = Integer(desc='结束时间')


class FortBattleInitTempData(ClassObject):
    field_id = String(desc='区域id')
    block_id = Integer(desc='区块id', default=-1)
    point_id = String(desc='据点id')
    defense_clan_id = String(desc='防守公会id')
    attack_clan_id = String(desc='攻击公会id')
    total_hp = Integer(desc='总血量', default=0)
    rest_hp = Integer(desc='剩余血量', default=0)
    end_time = Integer(desc='结束时间', default=0)