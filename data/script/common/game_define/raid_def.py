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

from script.common.db.class_obj import String, Integer, ClassObject, Dict, Class, List, Boolean

const_raidTTLKey = 'RaidTTL'
const_raidBattlePeriodKey = 'RaidBattlePeriod'

const_raidRewardType = {'all': 'ALL', 'finder': 'FINDER', 'last': 'LAST', 'top': 'TOP'}


class UserDeck(ClassObject):
    pets = List(String(), desc='소환수의 Combatants Key 리스트')


class UserBoss(ClassObject):
    raid_id = String(desc='레이드 아이디')
    raid_seq = String(desc='raid seq')
    level = Integer(default=1, desc='보스의 레벨')
    time_start = Integer(desc='보스 발견 시간')
    time_end = Integer(desc='结束时间戳')
    boss_clear = Boolean(desc='보스 클리어 여부')


class BeginRaid(ClassObject):
    raid_id = String(desc='레이드 아이')
    raid_seq_id = String(desc='레이드 시퀀스 아이디')
    raid_start_time = Integer(desc='레이드 전투 시작 시간')
    begin_part = String(desc='레이드 파트')
    hero_class_key = String(desc='레이드 진행 중인 영웅의 키')


class UserRaidInfo(ClassObject):
    user_id = String(desc='유저의 아이디 정보')
    raid_deck = Dict(Dict(Class(UserDeck)), desc='유저의 덱 정보')
    boss = Class(UserBoss)
    raid_notice_confirm = Integer(default=0)
    begin_raid = Class(BeginRaid)
    raid_seq_checked_list = List(String(), desc='유저가 검색한 레이스 시퀀스 리스트')
    end_approach_time = Integer(default=0, desc='가장 빠르게 종료될 예정인 레이드의 종료 시간')
    init_inheritance_boss_level_flag = Boolean(default=False, desc='시즌 초기화 시 계승레벨 초기화 플래그 값')
    inheritance_boss_level = Integer(default=1, desc='시즌 종료 시 보스 레벨 계승')
    # add by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-05-10
    # detail: 修改战斗力计算公式
    # >>>>>>>>>>>>>
    reward_times = Integer(desc='获取奖励次数', default=0)
    reward_time = Integer(desc='获取奖励时间', default=0)
    # <<<<<<<<<<<<<
