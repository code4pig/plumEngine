# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-10 14:42

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Class, Float, Boolean, Dict, List
from script.common.game_define.hero_def import HeroSnap

CHANNEL_ID_MAX = 1000000

SCENE_USER_MAX_NUM_PER_CHANNEL = 20

LEAVE_SCENE_REASON_LOGOUT = 'Logout'
LEAVE_SCENE_REASON_CREATE_TEAM = 'CreateTeam'
LEAVE_SCENE_REASON_JOIN_TEAM = 'JoinTeam'
LEAVE_SCENE_REASON_MANUAL = 'Manual'


class PositionItem(ClassObject):
    x = Float(desc='x坐标', default=0.0)
    y = Float(desc='y坐标', default=0.0)
    z = Float(desc='z坐标', default=0.0)
    rotation = Float(desc='旋转朝向', default=0.0)


class SceneUserInfo(ClassObject):
    server_user_id = String(desc='玩家server_user_id')
    name = String(desc='玩家名')
    level = Integer(default=1, desc='玩家等级')
    hero_snap = Class(HeroSnap, desc='英雄信息')
    clan_id = String(desc='公会id')
    clan_name = String(desc='公会名')
    team_id = String(desc='队伍id')
    position_info = Class(PositionItem, desc='坐标信息')


class SceneMemberInfo(ClassObject):
    server_user_id = String(desc='成员server_user_id')
    follow_leader = Boolean(desc='是否跟随队长', default=False)


class SceneTeamInfo(ClassObject):
    leader_server_user_id = String(desc='队长server_user_id')
    member_dict = Dict(Class(SceneMemberInfo), desc='成员字典')