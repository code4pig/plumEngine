# -*- coding:utf8 -*-

from __future__ import unicode_literals

import msgpack
import time
import script.common.log as logger
import script.common.exception_def as excp
import script.common.protocol_def as proto_def
import script.fight.object_factory as ModObjFac
from script.common.protocol_def import *
from script.fight.battle_handler_base import BattleHandlerBase

WRITE_BACK_INTERVAL = 10        # 回写数据时间间隔
SYNC_INTERVAL = 2               # 同步间隔


class BattleHandlerFortWar(BattleHandlerBase):
    def __init__(self):
        self.server_group_id = None         # server group id
        self.battle_unique_id = None        # 战斗唯一id
        self.self_clan_id = None            # 己方公会id
        self.enemy_clan_id = None           # 敌方公会id
        self.point_id = None                # 据点id
        self.start_time = 0                 # 开启时间
        self.end_time = 0                   # 战斗结束时间(阶段结束)
        self.total_hp = 0                   # 总血量
        self.rest_hp = 0                    # 剩余血量
        self.last_damage_time = 0           # 上一次伤害时间
        self.last_write_back_time = 0       # 上一次回写血量时间
        self.last_sync_time = 0             # 上一次同步时间
        self.user_damage_dict = {}          # 玩家伤害统计字典{server_user_id:damage},两次回写之间的伤害增量
        self.battle_user_dict = {}          # 当前战斗玩家字典{server_user_id:last_damage_time}
        self.is_finish = False              # 是否已结束

    def init_battle(self, server_group_id, battle_unique_id, self_clan_id, enemy_clan_id, point_id, battle_start_time, battle_end_time, total_hp, rest_hp):
        self.server_group_id = server_group_id
        self.battle_unique_id = battle_unique_id
        self.self_clan_id = self_clan_id
        self.enemy_clan_id = enemy_clan_id
        self.point_id = point_id
        self.start_time = battle_start_time
        self.end_time = battle_end_time
        self.total_hp = total_hp
        self.rest_hp = rest_hp

    def get_cur_battle_user_list(self):
        return self.battle_user_dict.keys()

    def handle_battle_msg(self, server_user_id, cmd, msg):
        if cmd == proto_def.bt_submit_fort_war_damage:
            # 战斗初始化完成
            is_finish = self._handle_damage(server_user_id, msg)
            return is_finish
        elif cmd == proto_def.bt_quit_battle:
            self._handle_quit_battle(server_user_id)
        else:
            logger.GetLog().warn('this battle protocol is unexpected, cmd is : %s' % cmd)
        return False

    def handle_sec_timer(self, current_time):
        if self.is_finish:
            return True
        else:
            # 检查是否要同步当前血量
            if current_time - self.last_sync_time >= SYNC_INTERVAL and self.battle_user_dict and self.last_damage_time > self.last_sync_time:
                # 达到同步时间且还有人且上一次同步后还有伤害
                syn_to_mem = BTSyncFortWarBattle()
                syn_to_mem.rest_hp = self.rest_hp
                ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_to_mem.dump()), self.battle_user_dict.keys())
                self.last_sync_time = current_time
            # 先检查是否要回写数据
            if (current_time - self.last_write_back_time >= WRITE_BACK_INTERVAL and self.last_damage_time > self.last_write_back_time) or current_time >= self.end_time:
                # 有新伤害需要回写 或 时间到已结束
                ModObjFac.CreateApp().get_fight_2_db_rpc().FortWarBattleWriteBack(self.server_group_id, self.self_clan_id, self.enemy_clan_id, self.battle_unique_id,
                                                                                  self.point_id, self.rest_hp, self.user_damage_dict)
                self.user_damage_dict = {}
                self.last_write_back_time = current_time
            if current_time >= self.end_time:
                # 已结束, 处理
                self.is_finish = True
                return True
            elif self.last_write_back_time >= self.last_damage_time and not self.battle_user_dict:
                # 回写时间大于伤害时间,且没人了,也按结束处理
                return True
        return False

    def handle_db_callback(self, handle_flag, *args):
        return False

    def handle_user_leave(self, server_user_id):
        self.battle_user_dict.pop(server_user_id, None)
        ModObjFac.CreateApp().get_fight_2_db_rpc().FortWarUpdateBattleUser(self.server_group_id, self.enemy_clan_id, self.point_id, len(self.battle_user_dict), server_user_id)

    def handle_user_join(self, server_user_id):
        if server_user_id not in self.battle_user_dict:
            self.battle_user_dict[server_user_id] = 0
        ModObjFac.CreateApp().get_fight_2_db_rpc().FortWarUpdateBattleUser(self.server_group_id, self.enemy_clan_id, self.point_id, len(self.battle_user_dict))
        # 返回给客户端
        res = BTJoinFortWarBattleResponse()
        res.total_hp = self.total_hp
        res.rest_hp = self.rest_hp
        res.return_code = excp.ExceptionSuccess.code
        ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(res.dump()), [server_user_id])

    def _handle_damage(self, server_user_id, msg):
        recv_obj = BTSubmitFortWarDamage.new_from_data(msg)
        if not self.is_finish and self.rest_hp > 0 and recv_obj.damage > 0:
            self.rest_hp = max(0, self.rest_hp - recv_obj.damage)
            # 更新伤害统计
            if server_user_id not in self.user_damage_dict:
                self.user_damage_dict[server_user_id] = 0
            self.user_damage_dict[server_user_id] += recv_obj.damage
            cur_time = time.time()
            # 更新最后一次受击
            self.last_damage_time = cur_time
            # 更新当前战斗玩家列表
            self.battle_user_dict[server_user_id] = cur_time
            if self.rest_hp == 0:
                # 已结束
                syn_to_mem = BTSyncFortWarBattle()
                syn_to_mem.rest_hp = 0
                ModObjFac.CreateApp().get_fight_2_fight_proxy_rpc().OnFightMsgFromFight(self.server_group_id, msgpack.packb(syn_to_mem.dump()), self.battle_user_dict.keys())
                self.last_sync_time = cur_time
                # 回写一次数据
                ModObjFac.CreateApp().get_fight_2_db_rpc().FortWarBattleWriteBack(self.server_group_id, self.self_clan_id, self.enemy_clan_id, self.battle_unique_id,
                                                                                  self.point_id, self.rest_hp, self.user_damage_dict, server_user_id)
                self.user_damage_dict = {}
                self.last_write_back_time = cur_time
                self.is_finish = True
                return True
        return False

    def _handle_quit_battle(self, server_user_id):
        self.handle_user_leave(server_user_id)
