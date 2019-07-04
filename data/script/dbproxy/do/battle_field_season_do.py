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

from couchbase.exceptions import KeyExistsError

from script.common import exceptions as excp
from script.common.db.base_do import UnlockedDoBase
from script.common.db.database import db_battle_field
from script.common.db.instant_box import instant_box
from script.common.game_define.battle_field_def import *
from script.common.game_define.time_util import get_week_start_timestamp


def get_season_range(current_time):
    # 计算当前时间所处的赛季的开始、结束
    begin_time = get_week_start_timestamp(current_time)
    end_time = begin_time + const_battle_field_period_sec
    return begin_time, end_time


def get_season_register_time_range(season_begin_time):
    return season_begin_time + const_battle_field_register_begin_sec, season_begin_time + const_battle_field_register_end_sec


def get_season_prepare_time_range(season_begin_time):
    return season_begin_time + const_battle_field_prepare_begin_sec, season_begin_time + const_battle_field_prepare_end_sec


def get_season_arrange_time_range(season_begin_time):
    return season_begin_time + const_battle_field_arrange_begin_sec, season_begin_time + const_battle_field_arrange_end_sec


def get_season_battle_time_range(season_begin_time):
    return season_begin_time + const_battle_field_battle_begin_sec, season_begin_time + const_battle_field_battle_end_sec


def get_season_freeze_time_range(season_begin_time):
    return season_begin_time + const_battle_field_result_sec, season_begin_time + const_battle_field_period_sec


def get_battle_field_step(season_begin_time, current_time):
    register_begin, register_end = get_season_register_time_range(season_begin_time)
    if season_begin_time <= current_time < register_begin:
        # 报名前阶段
        return BF_STEP_BEFORE_REGISTER, season_begin_time, register_begin
    elif register_begin <= current_time < register_end:
        # 报名阶段
        return BF_STEP_REGISTER, register_begin, register_end
    prepare_begin, prepare_end = get_season_prepare_time_range(season_begin_time)
    if register_end <= current_time < prepare_begin:
        # 准备期前阶段
        return BF_STEP_BEFORE_PREPARE, register_end, prepare_begin
    elif prepare_begin <= current_time < prepare_end:
        # 准备期
        return BF_STEP_PREPARE, prepare_begin, prepare_end
    arrange_begin, arrange_end = get_season_arrange_time_range(season_begin_time)
    if arrange_begin <= current_time < arrange_end:
        # 调整期
        return BF_STEP_ARRANGE, arrange_begin, arrange_end
    battle_begin, battle_end = get_season_battle_time_range(season_begin_time)
    if battle_begin <= current_time < battle_end:
        # 战斗期
        return BF_STEP_BATTLE, battle_begin, battle_end
    freeze_begin, freeze_end = get_season_freeze_time_range(season_begin_time)
    if freeze_begin <= current_time:
        # 结束冷却期
        return BF_STEP_FREEZE, freeze_begin, freeze_end
    print '===== [ERROR] ===== no match battle field step :', current_time, season_begin_time
    return BF_STEP_FREEZE, season_begin_time, current_time


class BattleFieldSeasonDo(UnlockedDoBase):
    def __init__(self, context, current_time):
        super(BattleFieldSeasonDo, self).__init__(context)

        if self.is_new:
            self._make_season_status(current_time)
        else:
            # 如果是旧数据,则检查是否要切换赛季
            self._check_changed_season_status(current_time)

    @classmethod
    def cls(cls):
        return BattleFieldSeasonStatus

    @classmethod
    def get_prefix(cls):
        return 'BF_SEASON'

    @classmethod
    def get_db(cls):
        return db_battle_field()

    @classmethod
    def is_server_group_do(cls):
        return True

    def get_season_status(self):
        return self.doc

    def _make_season_status(self, current_time):
        # 构造赛季状态数据(第一次构造数据)
        try:
            # 因为该do是unlock的,所以以该方式获取写权限
            if self.get_db().insert('SEASON_STATUS_{0}'.format(instant_box.server_group), {}, 3):
                pass
        except KeyExistsError:
            # 报错即有人正在操作中
            raise excp.ExceptionBattleFieldRequireRetry

        self.doc.season_key = 1
        self.doc.update_time = current_time
        self.doc.season_begin_time, self.doc.season_end_time = get_season_range(current_time)
        self.doc.season_step, self.doc.step_begin_time, self.doc.step_end_time = get_battle_field_step(self.doc.season_begin_time, current_time)

        self.update()

        try:
            self.get_db().delete('SEASON_STATUS_{0}'.format(instant_box.server_group))
        except:
            pass

    def _check_changed_season_status(self, current_time):
        if self.doc.season_end_time <= current_time:
            # 已经切换赛季，需要更新赛季
            try:
                # 因为该do是unlock的,所以以该方式获取写权限
                if self.get_db().insert('SEASON_STATUS_{0}'.format(instant_box.server_group), {}, 3):
                    pass
            except KeyExistsError:
                # 报错即有人正在操作中
                raise excp.ExceptionBattleFieldRequireRetry

            self.doc.season_key += 1
            self.doc.update_time = current_time
            self.doc.season_begin_time, self.doc.season_end_time = get_season_range(current_time)
            self.doc.season_step, self.doc.step_begin_time, self.doc.step_end_time = get_battle_field_step(self.doc.season_begin_time, current_time)

            self.update()

            try:
                self.get_db().delete('SEASON_STATUS_{0}'.format(instant_box.server_group))
            except:
                pass
        elif self.doc.step_end_time <= current_time:
            # 赛季未切换,检查是否需要更新阶段(此处不加锁处理似乎无问题?)
            self.doc.season_step, self.doc.step_begin_time, self.doc.step_end_time = get_battle_field_step(self.doc.season_begin_time, current_time)
            self.update()
        return True
