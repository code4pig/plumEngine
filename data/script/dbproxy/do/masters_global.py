# coding=utf8

from __future__ import unicode_literals

import game
import script.common.log as logger
import sys

from script.common.db.master_context import context
from script.common.game_define.rt_battle_define import CombatantStatusConstDef
from script.dbproxy.do.master_alpha_fort_war_battle_reward_do import MasterAlphaFortWarBattleRewardDo
from script.dbproxy.do.master_battle_field_battle_reward_do import MasterBattleFieldBattleRewardDo
from script.dbproxy.do.master_battle_field_setting import MasterBattleFieldSettingDo
from script.dbproxy.do.master_behavior_do import MasterBehaviorDo
from script.dbproxy.do.master_character_level_do import MasterHeroLevelDo, MasterPetLevelDo
from script.dbproxy.do.master_combatants_base_do import MasterCombatantsBaseDo
from script.dbproxy.do.master_combatants_do import MasterCombatantsDo
from script.dbproxy.do.master_constants_do import MasterConstantDo
from script.dbproxy.do.master_equipment_do import MasterEquipmentDo
from script.dbproxy.do.master_equipment_set_option_do import MasterEquipmentSetOptionDo
from script.dbproxy.do.master_equipment_strengthen_set_do import MasterEquipmentStrengthenSetDo
from script.dbproxy.do.master_hero_equipment_box_stat_do import MasterHeroEquipmentBoxStatDo
from script.dbproxy.do.master_hero_training_do import MasterHeroTrainingDo
from script.dbproxy.do.master_item_do import MasterItemDo
from script.dbproxy.do.master_level_factor_do import MasterLevelFactorDo
from script.dbproxy.do.master_mail_do import MasterMailDo
from script.dbproxy.do.master_mastery_stat_do import MasterMasteryStatDo
from script.dbproxy.do.master_raid_boss_training_do import MasterRaidBossTrainingDo
from script.dbproxy.do.master_stat_mod_do import MasterStatModDo
from script.dbproxy.do.master_strengthen_equip_stat_do import MasterStrengthenEquipmentStatDo
from script.dbproxy.do.master_team_boss_do import MasterTeamBossDo
from script.dbproxy.do.master_team_boss_part_do import MasterTeamBossPartDo
from script.dbproxy.do.master_team_boss_reward_do import MasterTeamBossRewardDo
from script.dbproxy.do.master_team_boss_reward_map_do import MasterTeamBossRewardMapDo
from script.dbproxy.do.master_team_boss_stage_do import MasterTeamBossStageDo
from script.dbproxy.do.master_team_boss_training_do import MasterTeamBossTrainingDo
from script.dbproxy.do.master_transform_strengthen_do import MasterTransformStrengthenDo
from script.dbproxy.do.master_user_level_do import MasterUserLevelDo

data_context = context

master_constants_inst = MasterConstantDo(data_context)
master_equipment_inst = MasterEquipmentDo(data_context)
master_strengthen_equip_stat_inst = MasterStrengthenEquipmentStatDo(data_context)
master_team_boss_part_inst = MasterTeamBossPartDo(data_context)
master_team_boss_training_inst = MasterTeamBossTrainingDo(data_context)
master_hero_level_inst = MasterHeroLevelDo(data_context)
master_pet_level_inst = MasterPetLevelDo(data_context)
master_user_level_inst = MasterUserLevelDo(context)
master_item_do_inst = MasterItemDo(data_context)
master_behavior_inst = MasterBehaviorDo(data_context)
master_team_boss_stage_inst = MasterTeamBossStageDo(data_context)
master_team_boss_reward_map_inst = MasterTeamBossRewardMapDo(data_context)
master_team_boss_reward_inst = MasterTeamBossRewardDo(data_context)
master_team_boss_inst = MasterTeamBossDo(data_context)
master_raid_boss_training_inst = MasterRaidBossTrainingDo(data_context)
master_combatants_inst = MasterCombatantsDo(data_context)
master_combatants_base_inst = MasterCombatantsBaseDo(data_context)
master_level_factor_inst = MasterLevelFactorDo(data_context)
master_equipment_set_option_inst = MasterEquipmentSetOptionDo(data_context)
master_stat_mod_inst = MasterStatModDo(data_context)
master_hero_training_inst = MasterHeroTrainingDo(data_context)
master_transform_strengthen_inst = MasterTransformStrengthenDo(data_context)
master_mastery_stat_inst = MasterMasteryStatDo(data_context)
master_hero_equipment_box_stat_inst = MasterHeroEquipmentBoxStatDo(data_context)
master_equipment_strengthen_set_inst = MasterEquipmentStrengthenSetDo(data_context)
master_alpha_fort_war_battle_reward_inst = MasterAlphaFortWarBattleRewardDo(data_context)
master_mail_do_inst = MasterMailDo(data_context)
master_battle_field_setting_inst = MasterBattleFieldSettingDo(data_context)
master_bf_battle_reward_inst = MasterBattleFieldBattleRewardDo(data_context)

if not master_constants_inst.doc.items or len(master_constants_inst.doc.items) == 0:
    logger.GetLog().error('!!!!!!!!!!!!!!!! db data is not ok  !!!!!!!!!!!!!!!!')
    game.GenCrash('db game config data error')


def reload_data_inst(inst_name):
    this_mod = sys.modules[__name__]
    if hasattr(this_mod, inst_name):
        data_context.reload(getattr(sys.modules[__name__], inst_name).get_doc_cache_key())
    elif inst_name == 'all':
        data_context.reload()
    else:
        logger.GetLog().warn('reload data inst : %s not found' % inst_name)
        return

    if inst_name == 'master_constants_inst' or inst_name == 'all':
        init_battle_config_const_value()


# 初始化战斗常量数据
def init_battle_config_const_value():
    logger.GetLog().debug('start init battle config const value')
    CombatantStatusConstDef.CRI = master_constants_inst.get_number("Cri")
    CombatantStatusConstDef.DEF = master_constants_inst.get_number("Def")
    CombatantStatusConstDef.RES = master_constants_inst.get_number("Res")
    CombatantStatusConstDef.PEN = master_constants_inst.get_number("Pen")
    CombatantStatusConstDef.EVA = master_constants_inst.get_number("Eva")
    CombatantStatusConstDef.DEC = master_constants_inst.get_number("Dec")
    CombatantStatusConstDef.ATTR_RES = master_constants_inst.get_number("AttrRes")
    CombatantStatusConstDef.DEFAULT_ATTR_RES = master_constants_inst.get_number("DefaultAttrRes")
    CombatantStatusConstDef.ATK_SPEED = master_constants_inst.get_number("AtkSpd")
    CombatantStatusConstDef.CRI_DAMAGE = master_constants_inst.get_number("CriDamage")
    CombatantStatusConstDef.MES_RES = master_constants_inst.get_number("MesRes")
    CombatantStatusConstDef.CHARGE = master_constants_inst.get_number("Charge")
    CombatantStatusConstDef.CHARGE_FRONT_ATK = master_constants_inst.get_number("ChargeFrtAttack")
    CombatantStatusConstDef.CHARGE_MID_ATK = master_constants_inst.get_number("ChargeMidAttack")
    CombatantStatusConstDef.CHARGE_BACK_ATK = master_constants_inst.get_number("ChargeBckAttack")
    CombatantStatusConstDef.CHARGE_FRONT_DAMAGE = master_constants_inst.get_number("ChargeFrtDamage")
    CombatantStatusConstDef.CHARGE_MID_DAMAGE = master_constants_inst.get_number("ChargeMidDamage")
    CombatantStatusConstDef.CHARGE_BACK_DAMAGE = master_constants_inst.get_number("ChargeBckDamage")
    CombatantStatusConstDef.CHARGE_TURN = master_constants_inst.get_number("ChargeTurn")
    CombatantStatusConstDef.CHARGE_PHASE = master_constants_inst.get_number("ChargePhase")
    CombatantStatusConstDef.CHARGE_KILL = master_constants_inst.get_number("ChargeKill")
    CombatantStatusConstDef.CHARGE_FIRE_SKILL = master_constants_inst.get_number("ChargeFireSkill")
    CombatantStatusConstDef.CHARGE_DEAD = master_constants_inst.get_number("ChargeDead")
    CombatantStatusConstDef.PHY_DAMAGE_FREEZED = master_constants_inst.get_number("PDamageFreezed")
    CombatantStatusConstDef.MAG_DAMAGE_PETRIFIED = master_constants_inst.get_number("MDamagePetrified")
    CombatantStatusConstDef.PHY_DAMAGE_TRANSFORMED = master_constants_inst.get_number("PDamageTransformed")
    CombatantStatusConstDef.MAG_DAMAGE_TRANSFORMED = master_constants_inst.get_number("MDamageTransformed")
    CombatantStatusConstDef.MAG_CRI_TERRIFIED = master_constants_inst.get_number("MCriTerrified")
    logger.GetLog().debug('finish init battle config const value')