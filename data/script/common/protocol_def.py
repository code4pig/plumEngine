# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.chat.chatting_def import ChattingMsg, P2POfflineMsg
from script.common.db.class_obj import ClassObject, String, Integer, List, Class, Boolean, Dict
from script.common.game_define.rt_battle_define import TeamBossBattleUnitBoss, TeamBossBattleUnitHero
from script.common.game_define.scene_def import SceneUserInfo, SceneTeamInfo, PositionItem, SceneMemberInfo

# 协议号定义(cmd)
# common ======>
cg_login_server = 'login_server'  # 登录服务器
cg_common_return_error = 'common_return_error'  # 返回码通用返回协议
# common <======

# chat ======>
cg_send_chat = 'send_chat'  # 发送聊天信息（ g => p & s ）
cg_recv_chat = 'receive_chat'  # 接收聊天信息
cg_get_offline_msg = 'get_offline_msg'  # 获取离线信息（ g => p & s ）
cg_offline_msg_confirm = 'offline_msg_confirm'  # 离线信息获取确认（ g => p & s ）
cg_get_online_num = 'get_online_num'  # 获取在线玩家人数
cg_game_server_register = 'game_server_register'  # 游戏服注册
cg_game_server_notice = 'game_server_notice'  # 游戏服推送公告
# chat <=======

# team ======>
cg_get_team_info = 'get_team_info'  # 请求自己的队伍的信息
cg_create_team = 'create_team'  # 创建队伍
cg_set_team_condi = 'set_team_condi'  # 设置队伍条件
cg_syn_team_condi = 'syn_team_condi'  # 队伍条件变动推送
cg_send_team_invite = 'send_team_invite'  # 发送队伍邀请
cg_syn_team_invite = 'syn_team_invite'  # 队伍邀请推送(给被邀请者)
cg_deal_team_invite = 'deal_team_invite'  # 处理入队邀请
cg_syn_deal_team_invite = 'syn_deal_team_invite'  # 入队邀请处理同步(给邀请者)
cg_syn_add_member = 'syn_add_new_member'  # 同步队伍增加成员
cg_team_enter_match = 'team_enter_match'  # 队伍请求匹配
cg_user_enter_match = 'user_enter_match'  # 玩家请求匹配
cg_disband_team = 'disband_team'  # 解散队伍
cg_syn_team_disband = 'syn_team_disband'  # 同步队伍解散
cg_leave_team = 'leave_team'  # 退出组队
cg_syn_member_leave = 'syn_member_leave_team'  # 同步成员离开
cg_kickout_member = 'kickout_member'  # 踢出成员
cg_user_cancel_match = 'user_cancel_match'  # 玩家取消匹配
cg_accept_team_call = 'accept_team_call'  # 响应队伍召唤
cg_team_cancel_match = 'team_cancel_match'  # 队伍取消匹配
cg_syn_team_match_status = 'syn_team_match_status'  # 同步队伍匹配状态
cg_syn_member_online_status = 'syn_member_online_status'  # 同步成员在线状态
cg_apply_enter_team = 'apply_enter_team'  # 玩家申请入队
cg_syn_apply_enter_team = 'syn_apply_team'  # 同步申请入队信息给队长
cg_get_team_list = 'get_team_list'  # 获取队伍列表
cg_deal_team_apply = 'deal_team_apply'  # 处理入队申请
cg_syn_deal_apply = 'syn_deal_team_apply'  # 推送入队申请处理结果给申请者
cg_team_enter_func = 'team_enter_func'  # 队长召唤成员进入玩法
cg_call_mem_enter_func = 'call_mem_enter_func'  # 同步召唤队员进入玩法
cg_mem_enter_ready = 'mem_enter_ready'  # 队员进入准备状态
cg_mem_cancel_ready = 'mem_cancel_ready'  # 队员取消准备状态
cg_syn_mem_ready_status = 'syn_mem_ready_status'  # 同步队员准备状态
cg_get_all_ready_mem = 'get_all_mem_ready_status'  # 获取所有成员准备状态
cg_get_opened_team_func = 'get_opened_team_func'  # 获取队伍当前开启的组队玩法
cg_open_team_func = 'open_team_func'  # 开启组队玩法
cg_give_up_team_func = 'give_up_team_func'  # 放弃组队玩法
cg_syn_opened_team_func = 'syn_opened_team_func'  # 同步副本玩法开启状态

tm_test_fishing = 'test_team_fishing'  # 测试钓鱼同步
# team <======

# battle ======>
bt_start_team_boss = 'start_team_boss'  # 队长发起组队boss
bt_syn_init_team_boss = 'syn_init_team_boss'  # 同步组队boss初始化数据
bt_team_boss_result = 'team_boss_result'  # 组队boss结算
bt_battle_init_finish = 'battle_init_finish'  # 战斗初始化完成
bt_real_start_battle = 'real_start_battle'  # 正式战斗开始
bt_battle_op = 'battle_op'  # 战斗操作转发
bt_sync_battle_tick = 'sync_battle_tick'  # 战斗tick同步
bt_change_ctrl_user = 'change_ctrl_user'  # 切换控制玩家
bt_syn_team_boss_hp = 'syn_team_boss_hp_in_battle'  # 战斗中同步组队boss血量
bt_join_fort_war_battle = 'join_fort_war_battle'  # 加入要塞战战斗
bt_sync_fort_war_battle = 'sync_fort_war_battle'  # 同步要塞战战斗
bt_submit_fort_war_damage = 'submit_fort_war_damage'  # 提交要塞战伤害
bt_quit_battle = 'quit_battle'  # 主动退出战斗(离开战场)
bt_push_battle_lose = 'push_battle_lose'  # 推送战斗失败消息
bt_join_fort_battle = 'join_fort_battle'    # 加入占领战要塞据点战斗
# battle <======

# scene ======>
sc_enter_scene = 'enter_scene'  # 进入场景
sc_sync_scene_users = 'sync_scene_users'  # 同步玩家进入
sc_player_move = 'player_move'  # 玩家移动
sc_sync_player_move = 'sync_player_move'    # 同步玩家移动
sc_update_follow_leader = 'update_follow_leader'    # 修改跟随队长
sc_sync_follow_leader = 'sync_member_follow_leader'     # 跟随队长数据同步
sc_sync_create_team = 'sync_create_world_team'      # 同步创建队伍
sc_sync_disband_team = 'sync_disband_world_team'    # 同步解散队伍
sc_sync_join_team = 'sync_join_world_team_member'       # 同步加入队伍
sc_sync_leave_team = 'sync_leave_world_team_member'     # 同步离开队伍
# scene <======


# 协议装饰器
def protocol_deco(cmd):
    def deco(cls):
        class DecoClass(cls):
            def __init__(self, **kwargs):
                super(DecoClass, self).__init__(**kwargs)
                self.cmd = cmd

        return DecoClass

    return deco


# 协议定义
class ProtocolBase(ClassObject):
    cmd = String(desc='协议号', required=True)


# ======= 协议嵌套对象 =======
class MemberInfo(ClassObject):
    server_member_id = String(desc='队员信息', default=None)
    is_online = Boolean(desc='是否在线', default=False)


class TeamListItem(ClassObject):
    team_id = Integer(desc='队伍id', default=0)
    leader_name = String(desc='队长名', default=None)
    func_flag = String(desc='玩法具体标识', default=None)
    member_count = Integer(desc='当前成员数', default=0)


class AddNewTeamMember(ClassObject):
    server_member_id = String(desc='成员id', default=None)
    is_online = Boolean(desc='是否在线', default=False)


class BattleExtInfo(ClassObject):
    is_self_die = Boolean(desc='是否自己死亡', default=False)
    server_caster_id = String(desc='攻击者server user id', default=None)
    server_target_id = String(desc='目标server user id', default=None)
    damage = String(desc='伤害值', default=0)


class ServerNodeInfo(ClassObject):
    node_type = Integer(desc='节点类型', required=True)
    node_id = Integer(desc='节点id', required=True)
    node_addr = String(desc='节点地址', required=True)
    node_port = Integer(desc='节点端口', required=True)


# >>>>>>>> client <=> gateway >>>>>>>>
# 登录服务器请求
@protocol_deco(cg_login_server)
class CGLoginServerRequest(ProtocolBase):
    server_user_id = String(desc='玩家server user id', required=True)
    server_id = String(desc='服务器id', required=True)
    sign = String(desc='登录校验key', default='')


# 返回码通用返回
@protocol_deco(cg_common_return_error)
class CGCommonErrorResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


# 登录服务器返回
@protocol_deco(cg_login_server)
class CGLoginServerResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


# 发送聊天请求
@protocol_deco(cg_send_chat)
class CGSendChatMsgRequest(ProtocolBase):
    channel_type = Integer(desc='频道类型,公告 - 1, 公共 - 2, 公会 - 3, 个人 - 4', default=2)
    server_receiver_id = String(desc='接收者server user id', default=None)
    data = Dict(String(), desc='消息内容')


# 发送聊天返回
@protocol_deco(cg_send_chat)
class CGSendChatMsgResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


# 同步聊天信息给客户端
@protocol_deco(cg_recv_chat)
class CGSynChatMsgToClient(ProtocolBase):
    channel_type = Integer(desc='频道类型,公告 - 1, 公共 - 2, 公会 - 3, 个人 - 4', default=2)
    server_sender_id = String(desc='发送者server user id', default=None)
    msg_time = String(desc='消息时间', default=0)
    data = Dict(String(), desc='消息内容')


# 请求离线消息
@protocol_deco(cg_get_offline_msg)
class CGGetChatOfflineMsgRequest(ProtocolBase):
    last_public_time = Integer(desc='公共聊天时间点', default=0)
    last_clan_time = Integer(desc='公会聊天时间点', default=0)


# 请求离线信息返回
@protocol_deco(cg_get_offline_msg)
class CGGetChatOfflineMsgResponse(ProtocolBase):
    public_msg_list = List(Class(ChattingMsg), desc='公共聊天')
    clan_msg_list = List(Class(ChattingMsg), desc='公会聊天')
    p2p_msg_list = List(Class(P2POfflineMsg), desc='个人聊天')


# 离线消息确认请求
@protocol_deco(cg_offline_msg_confirm)
class CGConfirmChatOfflineMsgRequest(ProtocolBase):
    pass


# 请求在线人数
@protocol_deco(cg_get_online_num)
class CGGetOnlineNumRequest(ProtocolBase):
    pass


# 请求在线人数返回
@protocol_deco(cg_get_online_num)
class CGGetOnlineNumResponse(ProtocolBase):
    online_num = Integer(desc='在线人数', default=0)


# 游戏服推送信息
@protocol_deco(cg_game_server_notice)
class CGGameServerNotice(ProtocolBase):
    server_group_id = String(desc='服务器id', default=None)
    channel_type = Integer(desc='频道类型,公告 - 1, 公共 - 2, 公会 - 3, 个人 - 4', default=1)
    server_receiver_id = String(desc='接收者server user id', default=None)
    data = String(desc='消息内容', default='')


# 游戏服注册请求
@protocol_deco(cg_game_server_register)
class CGGameServerRegisterRequest(ProtocolBase):
    rk_zone = String(desc='RKZONE', required=True)
    sign = String(desc='校验key', default='')


# 登录服务器返回
@protocol_deco(cg_game_server_register)
class CGGameServerRegisterResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_get_team_info)
class CGGetTeamInfoRequest(ProtocolBase):
    pass


@protocol_deco(cg_get_team_info)
class CGGetTeamInfoResponse(ProtocolBase):
    team_id = Integer(desc='队伍id', default=0)
    server_leader_id = String(desc='队长server user id', default=None)
    member_info_list = List(Class(MemberInfo), desc='成员信息列表')
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)
    is_in_match = Boolean(desc='是否在自动匹配中', default=False)


@protocol_deco(cg_create_team)
class CGCreateTeamRequest(ProtocolBase):
    pass


@protocol_deco(cg_create_team)
class CGCreateTeamResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)
    team_id = Integer(desc='队伍id', default=0)


@protocol_deco(cg_set_team_condi)
class CGSetTeamCondiRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_set_team_condi)
class CGSetTeamCondiResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_team_condi)
class CGSynTeamCondi(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_send_team_invite)
class CGSendTeamInviteRequest(ProtocolBase):
    target_server_user_id = String(desc='被邀请玩家server user id', default=None)


@protocol_deco(cg_send_team_invite)
class CGSendTeamInviteResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_team_invite)
class CGSynTeamInvite(ProtocolBase):
    from_team_id = Integer(desc='队伍id', default=0)
    from_user_name = String(desc='玩家名', default=None)
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_deal_team_invite)
class CGDealTeamInviteRequest(ProtocolBase):
    op_type = Integer(desc='操作类型(0-同意,1-拒绝)', default=0)
    team_id = Integer(desc='发起邀请的队伍id', default=0)


@protocol_deco(cg_deal_team_invite)
class CGDealTeamInviteResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_deal_team_invite)
class CGSynDealTeamInvite(ProtocolBase):
    invited_server_user_id = String(desc='被邀者玩家server user id', default=None)
    invited_user_name = String(desc='被邀者玩家名', default=None)
    op_type = Integer(desc='操作类型(0-同意,1-拒绝)', default=0)


@protocol_deco(cg_syn_add_member)
class CGSynAddNewMember(ProtocolBase):
    add_member_list = List(Class(AddNewTeamMember), desc='新增成员信息')


@protocol_deco(cg_team_enter_match)
class CGTeamEnterMatchRequest(ProtocolBase):
    pass


@protocol_deco(cg_team_enter_match)
class CGTeamEnterMatchResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_user_enter_match)
class CGUserEnterMatchRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_user_enter_match)
class CGUserEnterMatchResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_disband_team)
class CGDisbandTeamRequest(ProtocolBase):
    pass


@protocol_deco(cg_disband_team)
class CGDisbandTeamResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_team_disband)
class CGSynDisbandTeam(ProtocolBase):
    pass


@protocol_deco(cg_leave_team)
class CGLeaveTeamRequest(ProtocolBase):
    pass


@protocol_deco(cg_leave_team)
class CGLeaveTeamResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_member_leave)
class CGSynMemberLeave(ProtocolBase):
    server_member_id = String(desc='成员server user id', default=None)
    leave_reason = Integer(desc='退出原因(0 - 主动退出, 1 - 被踢)', default=0)


@protocol_deco(cg_kickout_member)
class CGKickoutMemberRequest(ProtocolBase):
    server_member_id = String(desc='成员server user id', default=None)


@protocol_deco(cg_kickout_member)
class CGKickOutMemberResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_user_cancel_match)
class CGUserCancelMatch(ProtocolBase):
    pass


@protocol_deco(cg_accept_team_call)
class CGAcceptTeamCallRequest(ProtocolBase):
    team_id = Integer(desc='发起邀请的队伍id', default=0)


@protocol_deco(cg_accept_team_call)
class CGAcceptTeamCallResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_team_cancel_match)
class CGTeamCancelMatch(ProtocolBase):
    pass


@protocol_deco(cg_team_cancel_match)
class CGTeamCancelMatchResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_team_match_status)
class CGSynTeamMatchStatus(ProtocolBase):
    is_in_match = Boolean(desc='是否在自动匹配中', default=False)


@protocol_deco(cg_syn_member_online_status)
class CGSynMemberOnlineStatus(ProtocolBase):
    server_member_id = String(desc='成员server user id', default=None)
    is_online = Boolean(desc='是否在线', default=False)


@protocol_deco(cg_apply_enter_team)
class CGApplyEnterTeam(ProtocolBase):
    team_id = Integer(desc='发起邀请的队伍id', default=0)


@protocol_deco(cg_apply_enter_team)
class CGApplyEnterTeamResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_apply_enter_team)
class CGSynApplyEnterTeam(ProtocolBase):
    server_applyer_id = String(desc='申请者server user id', default=None)
    applyer_name = String(desc='申请者名字', default=None)
    applyer_lv = Integer(desc='申请者等级', default=0)


@protocol_deco(cg_get_team_list)
class CGGetTeamListRequest(ProtocolBase):
    pass


@protocol_deco(cg_get_team_list)
class CGGetTeamListResponse(ProtocolBase):
    team_list = List(Class(TeamListItem), desc='队伍列表')


@protocol_deco(cg_deal_team_apply)
class CGDealTeamApply(ProtocolBase):
    server_applyer_id = String(desc='申请者server user id', default=None)
    op_type = Integer(desc='操作类型(0 - 同意, 1 - 拒绝)', default=0)


@protocol_deco(cg_deal_team_apply)
class CGDealTeamApplyResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_deal_apply)
class CGSynDealTeamApplyResult(ProtocolBase):
    team_id = Integer(desc='队伍id', default=0)
    leader_name = String(desc='队长名', default=None)
    op_type = Integer(desc='操作类型(0 - 同意, 1 - 拒绝)', default=0)


@protocol_deco(cg_call_mem_enter_func)
class CGCallMemEnterFunc(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_mem_enter_ready)
class CGMemEnterReadyRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_mem_enter_ready)
class CGMemEnterReadyResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_mem_cancel_ready)
class CGMemCancelReadyRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_mem_cancel_ready)
class CGMemCancelReadyResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_mem_ready_status)
class CGSynMemReadyStatus(ProtocolBase):
    server_member_id = String(desc='成员server user id', default=None)
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)
    is_ready = Boolean(desc='是否准备', default=False)


@protocol_deco(cg_team_enter_func)
class CGTeamEnterFuncRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_team_enter_func)
class CGTeamEnterFuncResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_get_all_ready_mem)
class CGGetAllReadyMemRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_get_all_ready_mem)
class CGGetAllReadyMemResponse(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)
    ready_mem_list = List(String(), default=None)


@protocol_deco(cg_get_opened_team_func)
class CGGetOpenedTeamFuncRequest(ProtocolBase):
    pass


@protocol_deco(cg_get_opened_team_func)
class CGGetOpenedTeamFuncResponse(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_open_team_func)
class CGOpenTeamFuncRequest(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_open_team_func)
class CGOpenTeamFuncResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(cg_give_up_team_func)
class CGGiveUpTeamFuncRequest(ProtocolBase):
    pass


@protocol_deco(cg_give_up_team_func)
class CGGiveUpTeamFuncResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(cg_syn_opened_team_func)
class CGSynOpenedTeamFunc(ProtocolBase):
    func_type = String(desc='玩法类型', default=None)
    func_flag = String(desc='玩法具体标识', default=None)


@protocol_deco(tm_test_fishing)
class TMTestFishing(ProtocolBase):
    content = String(desc='同步数据')


# battle ==========>
@protocol_deco(bt_start_team_boss)
class BTStartTeamBossRequest(ProtocolBase):
    part = String(desc='部位key')


@protocol_deco(bt_start_team_boss)
class BTStartTeamBossResponse(ProtocolBase):
    return_code = Integer(desc='返回码', default=0)


@protocol_deco(bt_syn_init_team_boss)
class BTSynInitTeamBoss(ProtocolBase):
    rand_seed = Integer(desc='随机种子')
    random_seed = Integer(desc='随机种子')
    ctrl_server_user_id = String(desc='当前控制的玩家server user id')
    func_type = String(desc='玩法类型')
    team_boss = Class(TeamBossBattleUnitBoss, desc='boss信息')
    hero_dict = Dict(Class(TeamBossBattleUnitHero), desc='成员参战英雄信息')


@protocol_deco(bt_team_boss_result)
class BTTeamBossResult(ProtocolBase):
    result_type = Integer(desc='结算类型')
    reward_dict = Dict(Integer(), desc='奖励')


@protocol_deco(bt_battle_init_finish)
class BTBattleInitFinish(ProtocolBase):
    auto_status = Boolean(desc='自动状态')


@protocol_deco(bt_real_start_battle)
class BTRealStartBattle(ProtocolBase):
    auto_status_dict = Dict(Integer(), desc='成员准备状态同步')


@protocol_deco(bt_battle_op)
class BTBattleOpSend(ProtocolBase):
    content = String(desc='同步数据')
    ext_info_list = List(Class(BattleExtInfo), desc='额外信息,用于校验')


@protocol_deco(bt_sync_battle_tick)
class BTSyncBattleTick(ProtocolBase):
    tick_count = Integer(desc='tick计数')
    op_list = List(String(), desc='转发操作数据列表')


@protocol_deco(bt_change_ctrl_user)
class BTChangeBattleCtrlUser(ProtocolBase):
    ctrl_server_user_id = String(desc='控制玩家server user id')


@protocol_deco(bt_syn_team_boss_hp)
class BTSynTeamBossHp(ProtocolBase):
    cur_hp = Integer(desc='boss血量', default=0)


@protocol_deco(bt_join_fort_war_battle)
class BTJoinFortWarBattleRequest(ProtocolBase):
    point_id = String(desc='据点id')


@protocol_deco(bt_join_fort_war_battle)
class BTJoinFortWarBattleResponse(ProtocolBase):
    return_code = Integer(desc='返回码')
    total_hp = Integer(desc='总血量', default=0)
    rest_hp = Integer(desc='剩余血量', default=0)


@protocol_deco(bt_submit_fort_war_damage)
class BTSubmitFortWarDamage(ProtocolBase):
    damage = Integer(desc='伤害值', default=0)


@protocol_deco(bt_sync_fort_war_battle)
class BTSyncFortWarBattle(ProtocolBase):
    rest_hp = Integer(desc='剩余血量', default=0)


@protocol_deco(bt_quit_battle)
class BTQuitBattle(ProtocolBase):
    pass


@protocol_deco(bt_push_battle_lose)
class BTPushBattleLose(ProtocolBase):
    pass


@protocol_deco(bt_join_fort_battle)
class BTJoinFortBattleRequest(ProtocolBase):
    field_id = String(desc='区域id')
    block_id = Integer(desc='区块id')
    point_id = String(desc='据点id')


@protocol_deco(bt_join_fort_battle)
class BTJoinFortBattleResponse(ProtocolBase):
    return_code = Integer(desc='返回码')
    total_hp = Integer(desc='总血量', default=0)
    rest_hp = Integer(desc='剩余血量', default=0)

# battle <==========


# scene ==========>
@protocol_deco(sc_enter_scene)
class SCEnterSceneRequest(ProtocolBase):
    scene = String(desc='场景类型, lobby')


@protocol_deco(sc_enter_scene)
class SCEnterSceneResponse(ProtocolBase):
    scene_user_list = List(Class(SceneUserInfo), desc='场景玩家数据列表')
    team_info = Class(SceneTeamInfo, desc='队伍信息')


@protocol_deco(sc_sync_scene_users)
class SCSyncSceneUsers(ProtocolBase):
    enter_users = List(Class(SceneUserInfo), desc='场景玩家数据列表')
    leave_users = List(String(), desc='leave users\' server_user_id list')


@protocol_deco(sc_player_move)
class SCPlayerMoveRequest(ProtocolBase):
    position_info = Class(PositionItem, desc='移动信息')


@protocol_deco(sc_sync_player_move)
class SCSyncPlayerMove(ProtocolBase):
    server_user_id = String(desc='玩家server user id')
    position_info = Class(PositionItem, desc='移动信息')


@protocol_deco(sc_update_follow_leader)
class SCUpdateFollowLeaderRequest(ProtocolBase):
    follow_leader = Boolean(desc='是否跟随队长')


@protocol_deco(sc_update_follow_leader)
class SCUpdateFollowLeaderResponse(ProtocolBase):
    return_code = Integer(desc='返回码')


@protocol_deco(sc_sync_follow_leader)
class SCSyncMemFollowLeader(ProtocolBase):
    server_user_id = String(desc='玩家server user id')
    follow_leader = Boolean(desc='是否跟随')


@protocol_deco(sc_sync_create_team)
class SCSyncCreateTeam(ProtocolBase):
    team_info = Class(SceneTeamInfo, desc='队伍信息')


@protocol_deco(sc_sync_disband_team)
class SCSyncDisbandTeam(ProtocolBase):
    pass


@protocol_deco(sc_sync_join_team)
class SCSyncJoinTeam(ProtocolBase):
    member = Class(SceneMemberInfo, desc='队员信息')


@protocol_deco(sc_sync_leave_team)
class SCSyncLeaveTeam(ProtocolBase):
    server_user_id = String(desc='玩家server user id')

# scene <==========

# <<<<<<<< client <=> gateway <<<<<<<<


# 字段名定义
field_name_cmd = 'cmd'
field_name_game_notice_sign = 'sign'

login_check_md5_ticket = '5afef724-727d-4c95-ae9a-e562d7567b72'
game_notice_check_md5_ticket = '5c9c7b0c-9d2d-4550-953a-f5fb4fb84109'
