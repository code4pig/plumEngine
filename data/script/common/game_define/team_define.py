# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer

TEAM_FUNC_TYPE_BOSS_FAFURION = 'team_boss_Fafurion'
TEAM_FUNC_TYPE_BOSS_RAID = 'team_boss_Antharas'
TEAM_FUNC_TYPE_BOSS_VALAKAS = 'team_boss_Valakas'

TEAM_FUNC_TYPE_LIST = [TEAM_FUNC_TYPE_BOSS_FAFURION, TEAM_FUNC_TYPE_BOSS_RAID, TEAM_FUNC_TYPE_BOSS_VALAKAS]     # 队伍条件功能类型列表

# 处理类型
TEAM_OP_AGREE = 0
TEAM_OP_DENY = 1

# 队伍最大人数
TEAM_MAX_MEMBER_NUM = 5

# 离开队伍类型
LEAVE_TEAM_TYPE_MANUAL = 0
LEAVE_TEAM_TYPE_KICK = 1


TEAM_APPLY_DICT_MAX_COUNT = 15      # 入队申请列表最大数量
TEAM_APPLY_LAST_TIME = 900      # 入队申请有效时间


# 匹配队列元素（个人）
class TeamMatchUserItem(ClassObject):
    server_user_id = String(desc='玩家server user id', default=None)
    user_lv = Integer(desc='玩家等级', default=0)
    func_flag = String(desc='玩法具体标识', default=None)


# 匹配队列元素（队伍）
class TeamMatchTeamItem(ClassObject):
    team_id = Integer(desc='队伍id', default=0)
    func_flag = String(desc='玩法具体标识', default=None)


# 队伍列表数据
class TeamListTeamItem(ClassObject):
    team_id = Integer(desc='队伍id', default=0)
    leader_name = String(desc='队长名', default=None)
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)
    member_count = Integer(desc='玩家人数', default=0)