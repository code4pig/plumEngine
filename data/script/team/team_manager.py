# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import sys

from script.common.game_define.global_def import get_server_and_user_id, make_server_user_id

reload(sys)
sys.setdefaultencoding('utf-8')

import msgpack
import script.common.log as logger
import script.common.exception_def as excp
import script.common.protocol_def as proto_def
import script.team.object_factory as ModObjFac
import script.common.game_define.team_define as team_def
from script.common.protocol_def import *
from script.common.online_user_manager import OnlineUserManager
from script.common.game_define.team_define import TeamListTeamItem


class TeamManager(object):
    def __init__(self):
        self.match_team_id_dict = {}  # server_group_id => team id list
        self.match_user_id_dict = {}  # server_group_id => user id list
        self.match_team_item_dict = {}  # server_group_id => team match item dict
        self.match_user_item_dict = {}  # server_group_id => user match item dict
        self.online_team_dict = {}  # server_group_id => team item dict
        self.online_manager = OnlineUserManager()

    def handle_user_online_status_update(self, server_group_id, server_user_id, is_online, handle_flag):
        logger.GetLog().debug('handle user online status : %s, %s, %s' % (server_group_id, server_user_id, is_online))
        if is_online:
            self.online_manager.user_online(server_group_id, server_user_id)
            # 检查是否要处理队伍列表等
            if handle_flag:
                ModObjFac.CreateApp().get_team_2_db_rpc().HandleForUserOnline(server_group_id, server_user_id)
        else:
            self.online_manager.user_offline(server_group_id, server_user_id)
            # 玩家下线,移除匹配队列数据
            self.remove_match_user(server_group_id, server_user_id)
            # 检查是否要处理队伍列表等
            if handle_flag:
                ModObjFac.CreateApp().get_team_2_db_rpc().HandleForUserOffline(server_group_id, server_user_id)
                ModObjFac.CreateApp().get_team_2_db_rpc().HandleTeamBossForUserOffline(server_group_id, server_user_id)

    def callback_handle_for_user_online(self, server_group_id, server_user_id, team_doc):
        # 同步在线状态给其他成员
        recv_id_list = [x for x in team_doc.member_id_list if x != server_user_id]
        if recv_id_list:
            syn_to_mem = CGSynMemberOnlineStatus()
            syn_to_mem.server_member_id = server_user_id
            syn_to_mem.is_online = True
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
        # 如果是队长,加入数据到队伍列表
        if team_doc.server_leader_id == server_user_id:
            team_item = TeamListTeamItem()
            team_item.team_id = team_doc.team_id
            team_item.leader_name = team_doc.leader_name
            team_item.func_type = team_doc.func_type
            team_item.func_flag = team_doc.func_flag
            team_item.member_count = len(team_doc.member_id_list)
            self.update_team_list_item(server_group_id, team_item)
            # 同步给其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamList(server_group_id, ModObjFac.CreateApp().get_node_id(), team_item.dump())

    def callback_handle_for_user_offline(self, server_group_id, server_user_id, team_doc):
        # 同步在线状态给其他成员
        recv_id_list = [x for x in team_doc.member_id_list if x != server_user_id]
        if recv_id_list:
            syn_to_mem = CGSynMemberOnlineStatus()
            syn_to_mem.server_member_id = server_user_id
            syn_to_mem.is_online = False
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
        # 如果是队长,队伍列表中删除数据,匹配队列删除队伍数据
        if team_doc.server_leader_id == server_user_id:
            self.remove_team_list_item(server_group_id, team_doc.team_id)
            is_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
            self.remove_match_team(server_group_id, team_doc.team_id)
            if is_in_match and recv_id_list:
                # 如果原先在匹配队列，则更新匹配状态给其他成员
                syn_match_status = CGSynTeamMatchStatus()
                syn_match_status.is_in_match = False
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), recv_id_list)
            # 同步给其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [], team_doc.team_id)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveTeamListItem(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id)

    def callback_handle_team_boss_for_user_offline(self, server_group_id, server_user_id, func_type, func_flag, member_id_list):
        recv_id_list = [x for x in member_id_list if x != server_user_id]
        if recv_id_list:
            syn_to_mem = CGSynMemReadyStatus()
            syn_to_mem.func_type = func_type
            syn_to_mem.func_flag = func_flag
            syn_to_mem.server_member_id = server_user_id
            syn_to_mem.is_ready = False
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)

    def handle_team_msg(self, server_group_id, server_user_id, str_msg):
        msg = msgpack.unpackb(str_msg)
        logger.GetLog().debug('handle team msg : %s, %s, %s' % (server_group_id, server_user_id, msg))
        try:
            cmd = msg.get(proto_def.field_name_cmd, None)
            if cmd is None:
                logger.GetLog().warn('format of this team msg is unexpected , cmd is None')
            elif cmd == proto_def.cg_get_team_info:
                self.handle_get_team_info(server_group_id, server_user_id)
            elif cmd == proto_def.cg_create_team:
                self.handle_create_team(server_group_id, server_user_id)
            elif cmd == proto_def.cg_set_team_condi:
                self.handle_set_team_condi(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_send_team_invite:
                self.handle_send_team_invite(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_deal_team_invite:
                self.handle_deal_team_invite(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_team_enter_match:
                self.handle_team_enter_match(server_group_id, server_user_id)
            elif cmd == proto_def.cg_user_enter_match:
                self.handle_user_enter_match(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_disband_team:
                self.handle_disband_team(server_group_id, server_user_id)
            elif cmd == proto_def.cg_leave_team:
                self.handle_leave_team(server_group_id, server_user_id)
            elif cmd == proto_def.cg_kickout_member:
                self.handle_kickout_member(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_user_cancel_match:
                self.handle_user_cancel_match(server_group_id, server_user_id)
            elif cmd == proto_def.cg_accept_team_call:
                self.handle_accept_team_call(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_apply_enter_team:
                self.handle_apply_enter_team(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_deal_team_apply:
                self.handle_deal_team_apply(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_team_cancel_match:
                self.handle_team_cancel_match(server_group_id, server_user_id)
            elif cmd == proto_def.cg_get_team_list:
                self.handle_get_team_list(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_team_enter_func:
                self.handle_send_call_mem_enter_func(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_mem_enter_ready:
                self.handle_member_enter_ready(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_mem_cancel_ready:
                self.handle_member_cancel_ready(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_get_all_ready_mem:
                self.handle_get_all_ready_mem(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_get_opened_team_func:
                self.handle_get_team_opened_func(server_group_id, server_user_id)
            elif cmd == proto_def.cg_open_team_func:
                self.handle_open_team_func(server_group_id, server_user_id, msg)
            elif cmd == proto_def.cg_give_up_team_func:
                self.handle_give_up_team_func(server_group_id, server_user_id)
            elif cmd == proto_def.tm_test_fishing:
                self.handle_test_fishing(server_group_id, server_user_id, msg)
            # ======================= for test =====================================
            elif cmd == 'test_team_pressure':
                is_reader = msg.get('is_reader', True)
                dist_type = msg.get('dist_type', 0)
                include_db = msg.get('include_db', False)
                if include_db:
                    ModObjFac.CreateApp().get_team_2_db_rpc().TestTeamPressure(server_group_id, server_user_id, is_reader)
                else:
                    self.callback_test_team_pressure(True, server_group_id, server_user_id, dist_type)
            # ======================= for test =====================================
            else:
                logger.GetLog().warn('format of this team msg is unexpected, has no match branch : %s' % cmd)
        except Exception as e:
            logger.GetLog().error('handle team msg catch an error : %s' % excp.log_exceptions(server_group_id=server_group_id, server_user_id=server_user_id,
                                                                                              str_msg="%s"%msg, exception=e))

    def handle_get_team_info(self, server_group_id, server_user_id):
        """
        处理获取队伍信息
        """
        ModObjFac.CreateApp().get_team_2_db_rpc().LoadTeamForGetTeamInfo(server_group_id, server_user_id)

    def callback_handle_get_team_info(self, server_group_id, server_user_id, team_doc):
        self.do_send_team_info(server_group_id, team_doc, [server_user_id])

    def handle_create_team(self, server_group_id, server_user_id):
        """
        创建队伍,检查是否满足创建条件
        """
        ModObjFac.CreateApp().get_team_2_db_rpc().DoCreateTeam(server_group_id, server_user_id)

    def callback_do_create_team(self, server_group_id, server_user_id, return_code, team_id=0, scene_user_info=None):
        """
        创建队伍回调
        """
        logger.GetLog().debug('check team for create team callback: %s, %s, %s, %s' % (server_group_id, server_user_id, return_code, team_id))
        res_to_client = CGCreateTeamResponse()
        res_to_client.return_code = return_code
        res_to_client.team_id = team_id
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(res_to_client.dump()), [server_user_id])

        if return_code == excp.ExceptionSuccess.code:
            # 创建队伍成功
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnUserCreateTeam(server_user_id, team_id, scene_user_info)

    def handle_set_team_condi(self, server_group_id, server_user_id, msg):
        """
        设置队伍条件
        """
        msg_obj = CGSetTeamCondiRequest.new_from_data(msg)
        if msg_obj.func_type and msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            res_to_client = CGSetTeamCondiResponse()
            res_to_client.return_code = excp.ExceptionTeamCondiParam.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(res_to_client.dump()), [server_user_id])
            return
        else:
            ModObjFac.CreateApp().get_team_2_db_rpc().DoSetTeamCondi(server_group_id, server_user_id, msg_obj.func_type, msg_obj.func_flag)

    def callback_do_set_team_condi(self, server_group_id, server_user_id, return_code, team_doc=None):
        """
        修改队伍匹配条件回调
        """
        res_to_client = CGSetTeamCondiResponse()
        res_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(res_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 修改成功,将设置广播给其他成员
            recv_id_list = [x for x in team_doc.member_id_list if x != server_user_id]
            if recv_id_list:
                syn_to_member = CGSynTeamCondi()
                syn_to_member.func_type = team_doc.func_type
                syn_to_member.func_flag = team_doc.func_flag
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_member.dump()), recv_id_list)
            if not team_doc.func_type and not team_doc.func_flag:
                # 目标副本设置为空, 删除队伍列表数据
                self.remove_team_list_item(server_group_id, team_doc.team_id)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveTeamListItem(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id)
            else:
                # 队伍加入到队伍列表
                team_item = TeamListTeamItem()
                team_item.team_id = team_doc.team_id
                team_item.leader_name = team_doc.leader_name
                team_item.func_type = team_doc.func_type
                team_item.func_flag = team_doc.func_flag
                team_item.member_count = len(team_doc.member_id_list)
                self.update_team_list_item(server_group_id, team_item)
                # 同步给其他节点
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamList(server_group_id, ModObjFac.CreateApp().get_node_id(), team_item.dump())
            # 如果队伍在匹配列表中,触发一次匹配检查
            if self.is_team_in_match(server_group_id, team_doc.team_id):
                if not team_doc.func_type and not team_doc.func_flag:
                    # 目标设置为空, 移除匹配队列数据
                    is_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
                    # 移除匹配队列
                    self.remove_match_team(server_group_id, team_doc.team_id)
                    # 同步移除其他节点
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), None, team_doc.team_id)
                    if is_in_match:
                        # 自动匹配状态改变,推送给所有成员
                        syn_match_status = CGSynTeamMatchStatus()
                        syn_match_status.is_in_match = False
                        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), team_doc.member_id_list)
                else:
                    # 检查一次匹配
                    match_user_id_list = self.match_user_id_dict.get(server_group_id, None)
                    match_user_item_dict = self.match_user_item_dict.get(server_group_id, None)
                    ModObjFac.CreateApp().get_team_2_db_rpc().InternalCheckTeamMatch(server_group_id, team_doc.team_id, match_user_id_list, match_user_item_dict)

    def callback_internal_check_team_match(self, server_group_id, find_id_list, is_team_full, team_doc, match_item=None):
        # 推送新增成员给老成员
        recv_id_list = [x for x in team_doc.member_id_list if x not in find_id_list]
        if recv_id_list:
            syn_add_mem = CGSynAddNewMember()
            for find_id in find_id_list:
                find_mem = AddNewTeamMember()
                find_mem.server_member_id = find_id
                find_mem.is_online = self.online_manager.is_user_online(server_group_id, find_id)
                syn_add_mem.add_member_list.append(find_mem)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_add_mem.dump()), recv_id_list)
        if is_team_full:
            self.remove_match_team(server_group_id, team_doc.team_id)
            # 同步给其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [], team_doc.team_id)
            # 推送组队状态变动给老成员
            if recv_id_list:
                syn_match_status = CGSynTeamMatchStatus()
                syn_match_status.is_in_match = False
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), recv_id_list)
        else:
            # 更新匹配队列队伍信息
            self.add_team_to_match(server_group_id, match_item)
            # 同步到其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynAddMatchTeamItem(server_group_id, ModObjFac.CreateApp().get_node_id(), match_item.dump())

        # 给新成员推送队伍信息
        self.do_send_team_info(server_group_id, team_doc, find_id_list)

        # 删除匹配队列中这些玩家
        for find_id in find_id_list:
            self.remove_match_user(server_group_id, find_id)
        # 同步删除其他节点的这些玩家
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), find_id_list, None)

    def handle_send_team_invite(self, server_group_id, server_user_id, msg):
        """
         发送组队邀请
        """
        msg_obj = CGSendTeamInviteRequest.new_from_data(msg)
        if not self.online_manager.is_user_online(server_group_id, server_user_id):
            # 玩家不在线
            ret_to_client = CGSendTeamInviteResponse()
            ret_to_client.return_code = excp.ExceptionUserNotOnline.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        else:
            # 玩家在线,检查其他条件
            ModObjFac.CreateApp().get_team_2_db_rpc().SendTeamInvite(server_group_id, server_user_id, msg_obj.target_server_user_id)

    def callback_send_team_invite(self, server_group_id, server_user_id, return_code, target_server_user_id=0, user_name=None, team_doc=None):
        """
        发送组队邀请检查回调
        """
        ret_to_client = CGSendTeamInviteResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 检查成功
            syn_to_invited_user = CGSynTeamInvite()
            syn_to_invited_user.from_team_id = team_doc.team_id
            syn_to_invited_user.from_user_name = user_name
            syn_to_invited_user.func_type = team_doc.func_type
            syn_to_invited_user.func_flag = team_doc.func_flag
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_invited_user.dump()), [target_server_user_id])

    def handle_deal_team_invite(self, server_group_id, server_user_id, msg):
        """
        处理组队邀请
        """
        msg_obj = CGDealTeamInviteRequest.new_from_data(msg)
        if msg_obj.op_type == team_def.TEAM_OP_AGREE:
            # 同意邀请
            ModObjFac.CreateApp().get_team_2_db_rpc().DoAgreeTeamInvitation(server_group_id, server_user_id, msg_obj.team_id)
        else:
            # 拒绝邀请
            ModObjFac.CreateApp().get_team_2_db_rpc().DoDenyTeamInvitation(server_group_id, server_user_id, msg_obj.team_id)

    def callback_do_agree_invite(self, server_group_id, server_user_id, return_code, user_name=None, team_doc=None, is_team_full=False, scene_user_info=None):
        """
        同意邀请回调
        """
        ret_to_client = CGDealTeamInviteResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 成功入队
            # 给队长推送操作消息
            syn_to_inviter = CGSynDealTeamInvite()
            syn_to_inviter.invited_server_user_id = server_user_id
            syn_to_inviter.invited_user_name = user_name
            syn_to_inviter.op_type = team_def.TEAM_OP_AGREE
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_inviter.dump()), [team_doc.server_leader_id])
            # 其他队员同步新增成员id
            recv_id_list = [x for x in team_doc.member_id_list if x != server_user_id]
            if recv_id_list:
                syn_add_mem = CGSynAddNewMember()
                find_mem = AddNewTeamMember()
                find_mem.server_member_id = server_user_id
                find_mem.is_online = self.online_manager.is_user_online(server_group_id, server_user_id)
                syn_add_mem.add_member_list.append(find_mem)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_add_mem.dump()), recv_id_list)
            # 若队伍已满,移除匹配队列队伍数据
            if is_team_full:
                is_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
                self.remove_match_team(server_group_id, team_doc.team_id)
                # 同步给其他节点
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [], team_doc.team_id)
                if is_in_match:
                    # 自动匹配状态改变,推送给其他所有成员
                    if recv_id_list:
                        syn_match_status = CGSynTeamMatchStatus()
                        syn_match_status.is_in_match = False
                        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), recv_id_list)
            # 给当前玩家推送队伍信息
            self.do_send_team_info(server_group_id, team_doc, [server_user_id])
            # 更新队伍列表中,队伍成员数量
            new_mem_count = len(team_doc.member_id_list)
            self.update_team_list_item_mem_count(server_group_id, team_doc.team_id, new_mem_count)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id, new_mem_count)
            # 推送给场景proxy
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnUserJoinTeam(server_user_id, scene_user_info, team_doc.team_id, team_doc.server_leader_id, team_doc.member_id_list)

    def callback_do_deny_invite(self, server_group_id, server_inviter_id, server_invitee_id, invitee_name):
        """
        拒绝邀请回调
        """
        if self.online_manager.is_user_online(server_group_id, server_inviter_id):
            syn_to_inviter = CGSynDealTeamInvite()
            syn_to_inviter.invited_server_user_id = server_invitee_id
            syn_to_inviter.invited_user_name = invitee_name
            syn_to_inviter.op_type = team_def.TEAM_OP_DENY
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_inviter.dump()), [server_inviter_id])

    def handle_team_enter_match(self, server_group_id, server_user_id):
        """
        处理队伍加入匹配队列
        """
        match_user_id_list = self.match_user_id_dict.get(server_group_id, None)
        match_user_item_dict = self.match_user_item_dict.get(server_group_id, None)
        match_team_item_dict = self.match_team_item_dict.get(server_group_id, None)

        ModObjFac.CreateApp().get_team_2_db_rpc().TeamEnterMatch(server_group_id, server_user_id, match_user_id_list, match_user_item_dict, match_team_item_dict)

    def callback_team_enter_match(self, server_group_id, server_user_id, return_code, find_id_list=None, team_doc=None, match_item=None):
        ret_to_client = CGTeamEnterMatchResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            if match_item:
                # 还需要加入队列
                self.add_team_to_match(server_group_id, match_item)
                # 同步到其他节点
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynAddMatchTeamItem(server_group_id, ModObjFac.CreateApp().get_node_id(), match_item.dump())
            # 匹配成功
            if find_id_list:
                # 有找到玩家,推送队伍信息给这些玩家
                self.do_send_team_info(server_group_id, team_doc, find_id_list)
                # 将这些玩家同步给原来队伍里的人
                recv_id_list = [x for x in team_doc.member_id_list if x not in find_id_list]
                if recv_id_list:
                    syn_to_mem = CGSynAddNewMember()
                    for find_id in find_id_list:
                        find_mem = AddNewTeamMember()
                        find_mem.server_member_id = find_id
                        find_mem.is_online = self.online_manager.is_user_online(server_group_id, find_id)
                        syn_to_mem.add_member_list.append(find_mem)
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
                # 删除匹配队列中这些玩家
                for find_id in find_id_list:
                    self.remove_match_user(server_group_id, find_id)
                # 同步删除其他节点的这些玩家
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), find_id_list, None)
                # 同步匹配状态改变给原来队伍里的人
                if match_item and recv_id_list:
                    syn_match_status = CGSynTeamMatchStatus()
                    syn_match_status.is_in_match = True
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), recv_id_list)
                # 更新队伍列表中,队伍成员数量
                new_mem_count = len(team_doc.member_id_list)
                self.update_team_list_item_mem_count(server_group_id, team_doc.team_id, new_mem_count)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id,
                                                                                                  new_mem_count)

    def handle_user_enter_match(self, server_group_id, server_user_id, msg):
        """
        处理玩家加入匹配队列
        """
        msg_obj = CGUserEnterMatchRequest.new_from_data(msg)
        if msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            ret_to_client = CGUserEnterMatchResponse()
            ret_to_client.return_code = excp.ExceptionTeamCondiParam.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return

        match_team_id_list = self.match_team_id_dict.get(server_group_id, None)
        match_team_item_dict = self.match_team_item_dict.get(server_group_id, None)

        ModObjFac.CreateApp().get_team_2_db_rpc().UserEnterMatch(server_group_id, server_user_id, msg_obj.func_flag, match_team_id_list, match_team_item_dict)

    def callback_user_enter_match(self, server_group_id, server_user_id, return_code, match_item=None, team_doc=None, is_team_full=False):
        # 结果返回给玩家
        ret_to_client = CGUserEnterMatchResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 匹配成功
            if team_doc:
                # 处理匹配队列,并同步状态
                is_team_match_status_change = False
                if is_team_full:
                    self.remove_match_team(server_group_id, team_doc.team_id)
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [], team_doc.team_id)
                    is_team_match_status_change = True

                # 已匹配到队伍,推送队伍信息给玩家，
                self.do_send_team_info(server_group_id, team_doc, [server_user_id])
                # 推送增加新成员信息给其他成员
                recv_id_list = [x for x in team_doc.member_id_list if x != server_user_id]
                if recv_id_list:
                    syn_to_mem = CGSynAddNewMember()
                    find_mem = AddNewTeamMember()
                    find_mem.server_member_id = server_user_id
                    find_mem.is_online = self.online_manager.is_user_online(server_group_id, server_user_id)
                    syn_to_mem.add_member_list.append(find_mem)
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
                if is_team_match_status_change and recv_id_list:
                    # 匹配状态改变,推送给原有成员
                    syn_match_status = CGSynTeamMatchStatus()
                    syn_match_status.is_in_match = False
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), recv_id_list)
                # 更新队伍列表中,队伍成员数量
                new_mem_count = len(team_doc.member_id_list)
                self.update_team_list_item_mem_count(server_group_id, team_doc.team_id, new_mem_count)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id, new_mem_count)
            else:
                # 没找到匹配的队伍，将数据加入到匹配队列
                self.add_user_to_match(server_group_id, match_item)
                # 广播给其他节点,更新字典
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynAddMatchUserItem(server_group_id, ModObjFac.CreateApp().get_node_id(), match_item.dump())

    def handle_disband_team(self, server_group_id, server_user_id):
        """
        处理解散队伍
        """
        ModObjFac.CreateApp().get_team_2_db_rpc().DoDisbandTeam(server_group_id, server_user_id)

    def callback_do_disband_team(self, server_group_id, server_user_id, return_code, team_id=None, recv_id_list=None):
        """
        解散队伍回调
        """
        ret_to_client = CGDisbandTeamResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        # 推送其他成员队伍解散
        if return_code == excp.ExceptionSuccess.code:
            if recv_id_list:
                syn_to_mem = CGSynDisbandTeam()
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
            # 移除匹配队列中队伍数据
            self.remove_match_team(server_group_id, team_id)
            # 同步给其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [], team_id)
            # 移除队伍列表
            self.remove_team_list_item(server_group_id, team_id)
            # 同步给其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveTeamListItem(server_group_id, ModObjFac.CreateApp().get_node_id(), team_id)
            # 同步给场景proxy,
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnTeamDisband(team_id)

    def handle_leave_team(self, server_group_id, server_user_id):
        """
        处理队员离开队伍
        """
        ModObjFac.CreateApp().get_team_2_db_rpc().DoLeaveTeam(server_group_id, server_user_id)

    def callback_do_leave_team(self, server_group_id, server_user_id, return_code, team_id=None, recv_id_list=None):
        """
        离开队伍回调
        """
        ret_to_client = CGLeaveTeamResponse()
        if return_code in [excp.ExceptionHasNoTeam.code]:  # 特定错误当做成功处理
            ret_to_client.return_code = excp.ExceptionSuccess.code
        else:
            ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            if recv_id_list:
                syn_to_mem = CGSynMemberLeave()
                syn_to_mem.server_member_id = server_user_id
                syn_to_mem.leave_reason = team_def.LEAVE_TEAM_TYPE_MANUAL
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
            # 更新队伍列表中,队伍成员数量
            new_mem_count = len(recv_id_list)
            self.update_team_list_item_mem_count(server_group_id, team_id, new_mem_count)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_id, new_mem_count)
            # 同步给场景, 玩家被踢出
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnUserLeaveTeam(server_user_id, team_id)

    def handle_kickout_member(self, server_group_id, server_user_id, msg):
        """
        处理踢出成员
        """
        msg_obj = CGKickoutMemberRequest.new_from_data(msg)
        if server_user_id == msg_obj.server_member_id:
            ret_to_client = CGKickOutMemberResponse()
            ret_to_client.return_code = excp.ExceptionTeamKickSelf.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        ModObjFac.CreateApp().get_team_2_db_rpc().DoKickOutMember(server_group_id, server_user_id, msg_obj.server_member_id)

    def callback_do_kickout_mem(self, server_group_id, server_user_id, return_code, team_id=None, server_member_id=None, recv_id_list=None):
        ret_to_client = CGKickOutMemberResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 被踢消息推送给其他成员
            if recv_id_list:
                syn_to_mem = CGSynMemberLeave()
                syn_to_mem.server_member_id = server_member_id
                syn_to_mem.leave_reason = team_def.LEAVE_TEAM_TYPE_KICK
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
            # 更新队伍列表中,队伍成员数量
            new_mem_count = len(recv_id_list) - 1
            self.update_team_list_item_mem_count(server_group_id, team_id, new_mem_count)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_id, new_mem_count)
            # 同步给场景, 玩家被踢出
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnUserLeaveTeam(server_member_id, team_id)

    def handle_user_cancel_match(self, server_group_id, server_user_id):
        self.remove_match_user(server_group_id, server_user_id)
        # 同步给其他节点
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_user_id], None)

    def handle_accept_team_call(self, server_group_id, server_user_id, msg):
        """
        接受队伍召唤
        """
        msg_obj = CGAcceptTeamCallRequest.new_from_data(msg)
        ModObjFac.CreateApp().get_team_2_db_rpc().AcceptTeamCall(server_group_id, server_user_id, msg_obj.team_id)

    def callback_accept_team_call(self, server_group_id, server_user_id, return_code, team_doc=None, recv_id_list=None, is_team_full=False, scene_user_info=None):
        ret_to_client = CGAcceptTeamCallResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 删除该玩家匹配队列信息
            self.remove_match_user(server_group_id, server_user_id)
            # 检查删除队伍匹配列表, 同步删除其他节点
            is_team_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
            if is_team_full:
                self.remove_match_team(server_group_id, team_doc.team_id)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_user_id], team_doc.team_id)
                if is_team_in_match and recv_id_list:
                    # 队伍匹配状态改变，推送给其他成员
                    syn_team_status = CGSynTeamMatchStatus()
                    syn_team_status.is_in_match = False
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_team_status.dump()), recv_id_list)
            else:
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_user_id], None)

            # 广播新成员加入消息给其他队员
            if recv_id_list:
                syn_to_mem = CGSynAddNewMember()
                find_mem = AddNewTeamMember()
                find_mem.server_member_id = server_user_id
                find_mem.is_online = self.online_manager.is_user_online(server_group_id, server_user_id)
                syn_to_mem.add_member_list.append(find_mem)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
            # 广播队伍信息给该玩家
            self.do_send_team_info(server_group_id, team_doc, [server_user_id])
            # 更新队伍列表中,队伍成员数量
            new_mem_count = len(team_doc.member_id_list)
            self.update_team_list_item_mem_count(server_group_id, team_doc.team_id, new_mem_count)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id, new_mem_count)
            # 推送给场景proxy
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnUserJoinTeam(server_user_id, scene_user_info, team_doc.team_id, team_doc.server_leader_id, team_doc.member_id_list)

    def handle_apply_enter_team(self, server_group_id, server_user_id, msg):
        """
        申请加入队伍
        """
        msg_obj = CGApplyEnterTeam.new_from_data(msg)
        ModObjFac.CreateApp().get_team_2_db_rpc().ApplyEnterTeam(server_group_id, server_user_id, msg_obj.team_id, self.is_team_in_match(server_group_id, msg_obj.team_id))

    def callback_apply_enter_team(self, server_group_id, server_user_id, return_code, is_in_team=False, team_doc=None, is_team_full=False, user_lv=0, user_name=None):
        """
        申请入队回调
        """
        ret_to_client = CGApplyEnterTeamResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            if is_in_team:
                # 直接进入组队
                # 推送新队员入队消息
                recv_id_list = [x for x in team_doc.member_id_list if x != server_user_id]
                if recv_id_list:
                    syn_add_mem = CGSynAddNewMember()
                    find_mem = AddNewTeamMember()
                    find_mem.server_member_id = server_user_id
                    find_mem.is_online = self.online_manager.is_user_online(server_group_id, server_user_id)
                    syn_add_mem.add_member_list.append(find_mem)
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_add_mem.dump()), recv_id_list)

                self.remove_match_user(server_group_id, server_user_id)
                # 队伍已满,删除匹配列表
                is_team_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
                if is_team_full:
                    self.remove_match_team(server_group_id, team_doc.team_id)
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_user_id], team_doc.team_id)
                    if is_team_in_match and recv_id_list:
                        # 推送匹配状态变化给原队伍成员
                        syn_team_status = CGSynTeamMatchStatus()
                        syn_team_status.is_in_match = False
                        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_team_status.dump()), recv_id_list)

                else:
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_user_id], None)
                # 推送队伍信息给该玩家
                self.do_send_team_info(server_group_id, team_doc, [server_user_id])
            elif self.online_manager.is_user_online(server_group_id, team_doc.server_leader_id):
                # 推送消息给队长
                syn_to_leader = CGSynApplyEnterTeam()
                syn_to_leader.server_applyer_id = server_user_id
                syn_to_leader.applyer_lv = user_lv
                syn_to_leader.applyer_name = user_name
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_leader.dump()), [team_doc.server_leader_id])

    def handle_deal_team_apply(self, server_group_id, server_user_id, msg):
        """
        处理入队申请
        """
        msg_obj = CGDealTeamApply.new_from_data(msg)
        if not self.online_manager.is_user_online(server_group_id, msg_obj.server_applyer_id):
            ret_to_client = CGDealTeamApplyResponse()
            ret_to_client.return_code = excp.ExceptionUserNotOnline.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        if msg_obj.op_type == team_def.TEAM_OP_AGREE:
            ModObjFac.CreateApp().get_team_2_db_rpc().AgreeTeamApply(server_group_id, server_user_id, msg_obj.server_applyer_id)
        else:
            ModObjFac.CreateApp().get_team_2_db_rpc().DenyTeamApply(server_group_id, server_user_id, msg_obj.server_applyer_id)

    def callback_agree_team_apply(self, server_group_id, server_user_id, return_code, server_applyer_id=None, applyer_scene_user_info=None, team_doc=None, is_team_full=False):
        """
        同意申请回调
        """
        ret_to_client = CGDealTeamApplyResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 推送新队员入队消息
            recv_id_list = [x for x in team_doc.member_id_list if x != server_applyer_id]
            if recv_id_list:
                syn_add_mem = CGSynAddNewMember()
                find_mem = AddNewTeamMember()
                find_mem.server_member_id = server_applyer_id
                find_mem.is_online = self.online_manager.is_user_online(server_group_id, server_applyer_id)
                syn_add_mem.add_member_list.append(find_mem)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_add_mem.dump()), recv_id_list)

            self.remove_match_user(server_group_id, server_applyer_id)
            # 队伍已满,删除匹配列表
            is_team_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
            if is_team_full:
                self.remove_match_team(server_group_id, team_doc.team_id)
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_applyer_id], team_doc.team_id)
                if is_team_in_match and recv_id_list:
                    # 队伍匹配状态改变,推送给原有成员
                    syn_team_status = CGSynTeamMatchStatus()
                    syn_team_status.is_in_match = False
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_team_status.dump()), recv_id_list)
            else:
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), [server_applyer_id], None)
            # 推送处理结果返回给申请者
            if self.online_manager.is_user_online(server_group_id, server_applyer_id):
                syn_to_applyer = CGSynDealTeamApplyResult()
                syn_to_applyer.team_id = team_doc.team_id
                syn_to_applyer.leader_name = team_doc.leader_name
                syn_to_applyer.op_type = team_def.TEAM_OP_AGREE
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_applyer.dump()), [server_applyer_id])
                # 推送队伍信息给该玩家
                self.do_send_team_info(server_group_id, team_doc, [server_applyer_id])
            # 更新队伍列表中,队伍成员数量
            new_mem_count = len(team_doc.member_id_list)
            self.update_team_list_item_mem_count(server_group_id, team_doc.team_id, new_mem_count)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynUpdateTeamListItemMemCount(server_group_id, ModObjFac.CreateApp().get_node_id(), team_doc.team_id, new_mem_count)
            # 推送给场景proxy
            ModObjFac.CreateApp().get_team_2_scene_proxy_rpc().OnUserJoinTeam(server_applyer_id, applyer_scene_user_info, team_doc.team_id, team_doc.server_leader_id,
                                                                              team_doc.member_id_list)

    def callback_deny_team_apply(self, server_group_id, server_user_id, return_code, server_applyer_id=None, team_id=0, leader_name=None):
        ret_to_client = CGDealTeamApplyResponse()
        if return_code in [excp.ExceptionAlreadyHasTeam.code]:  # 特定错误当做成功
            ret_to_client.return_code = excp.ExceptionSuccess.code
        else:
            ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 推送拒绝消息给申请者
            syn_to_applyer = CGSynDealTeamApplyResult()
            syn_to_applyer.team_id = team_id
            syn_to_applyer.leader_name = leader_name
            syn_to_applyer.op_type = team_def.TEAM_OP_DENY
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_applyer.dump()), [server_applyer_id])

    def handle_team_cancel_match(self, server_group_id, server_user_id):
        """
        队伍取消匹配
        """
        ModObjFac.CreateApp().get_team_2_db_rpc().LoadTeamForCancelTeamMatch(server_group_id, server_user_id)

    def callback_team_cancel_match(self, server_group_id, server_user_id, return_code, team_id=0, mem_id_list=None):
        ret_to_client = CGTeamCancelMatchResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            is_in_match = self.is_team_in_match(server_group_id, team_id)
            # 移除匹配队列
            self.remove_match_team(server_group_id, team_id)
            # 同步移除其他节点
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnSynRemoveMatchItem(server_group_id, ModObjFac.CreateApp().get_node_id(), None, team_id)
            # 推送匹配状态变动给客户端
            if is_in_match and mem_id_list:
                syn_match_status = CGSynTeamMatchStatus()
                syn_match_status.is_in_match = False
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_match_status.dump()), mem_id_list)

    def handle_get_team_list(self, server_group_id, server_user_id, msg):
        """
        请求队伍列表
        """
        team_list = self.get_server_online_team_list(server_group_id)
        ret_to_client = CGGetTeamListResponse()
        for team in team_list:
            team_item = TeamListItem()
            team_item.team_id = team.team_id
            team_item.leader_name = team.leader_name
            team_item.func_flag = team.func_flag
            team_item.member_count = team.member_count
            ret_to_client.team_list.append(team_item)
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])

    def handle_send_call_mem_enter_func(self, server_group_id, server_user_id, msg):
        msg_obj = CGTeamEnterFuncRequest.new_from_data(msg)
        if msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            ret_to_client = CGTeamEnterFuncResponse()
            ret_to_client.return_code = excp.ExceptionParamError.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleSendCallMemEnterFunc(server_group_id, server_user_id, msg_obj.func_type, msg_obj.func_flag)

    def callback_send_call_mem_enter_func(self, server_group_id, server_user_id, return_code, func_type=None, func_flag=None, member_id_list=None):
        ret_to_client = CGTeamEnterFuncResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            recv_id_list = [x for x in member_id_list if x != server_user_id]
            if recv_id_list:
                syn_to_mem = CGCallMemEnterFunc()
                syn_to_mem.func_type = func_type
                syn_to_mem.func_flag = func_flag
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)

    def handle_member_enter_ready(self, server_group_id, server_user_id, msg):
        msg_obj = CGMemEnterReadyRequest.new_from_data(msg)
        if msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            ret_to_client = CGMemEnterReadyResponse()
            ret_to_client.return_code = excp.ExceptionParamError.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleMemEnterReady(server_group_id, server_user_id, msg_obj.func_type, msg_obj.func_flag)

    def callback_member_enter_ready(self, server_group_id, server_user_id, return_code, func_type=None, func_flag=None, is_leader=False, member_id_list=None):
        ret_to_client = CGMemEnterReadyResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            recv_id_list = [x for x in member_id_list if x != server_user_id]
            if recv_id_list:
                if is_leader:
                    # 是队长准备,推送给其他成员进入玩法
                    syn_to_mem = CGCallMemEnterFunc()
                    syn_to_mem.func_type = func_type
                    syn_to_mem.func_flag = func_flag
                    ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)
                # 推送消息给所有成员进入玩法
                syn_to_mem = CGSynMemReadyStatus()
                syn_to_mem.func_type = func_type
                syn_to_mem.func_flag = func_flag
                syn_to_mem.server_member_id = server_user_id
                syn_to_mem.is_ready = True

                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)

    def handle_member_cancel_ready(self, server_group_id, server_user_id, msg):
        msg_obj = CGMemCancelReadyRequest.new_from_data(msg)
        if msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            ret_to_client = CGMemCancelReadyResponse()
            ret_to_client.return_code = excp.ExceptionParamError.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleMemCancelReady(server_group_id, server_user_id, msg_obj.func_type, msg_obj.func_flag)

    def callback_member_cancel_ready(self, server_group_id, server_user_id, return_code, func_type=None, func_flag=None, member_id_list=None):
        ret_to_client = CGMemCancelReadyResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 推送消息给所有成员进入玩法
            recv_id_list = [x for x in member_id_list if x != server_user_id]
            if recv_id_list:
                syn_to_mem = CGSynMemReadyStatus()
                syn_to_mem.func_type = func_type
                syn_to_mem.func_flag = func_flag
                syn_to_mem.server_member_id = server_user_id
                syn_to_mem.is_ready = False
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)

    def handle_get_all_ready_mem(self, server_group_id, server_user_id, msg):
        msg_obj = CGGetAllReadyMemRequest.new_from_data(msg)
        if msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            ret_to_client = CGGetAllReadyMemResponse()
            ret_to_client.func_type = msg_obj.func_type
            ret_to_client.func_flag = msg_obj.func_flag
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleGetAllReadyMem(server_group_id, server_user_id, msg_obj.func_type, msg_obj.func_flag)

    def callback_get_all_ready_mem(self, server_group_id, server_user_id, return_code, func_type, func_flag, member_id_list=None):
        ret_to_client = CGGetAllReadyMemResponse()
        ret_to_client.func_type = func_type
        ret_to_client.func_flag = func_flag
        if return_code == excp.ExceptionSuccess.code:
            ret_to_client.ready_mem_list = member_id_list
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])

    def handle_get_team_opened_func(self, server_group_id, server_user_id):
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleGetTeamOpenedFunc(server_group_id, server_user_id)

    def callback_get_team_opened_func(self, server_group_id, server_user_id, func_type=None, func_flag=None):
        ret_to_client = CGGetOpenedTeamFuncResponse()
        ret_to_client.func_type = func_type
        ret_to_client.func_flag = func_flag
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])

    def handle_open_team_func(self, server_group_id, server_user_id, msg):
        msg_obj = CGOpenTeamFuncRequest.new_from_data(msg)
        if msg_obj.func_type not in team_def.TEAM_FUNC_TYPE_LIST:
            ret_to_client = CGOpenTeamFuncResponse()
            ret_to_client.return_code = excp.ExceptionParamError.code
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
            return
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleOpenTeamFunc(server_group_id, server_user_id, msg_obj.func_type, msg_obj.func_flag)

    def callback_open_team_func(self, server_group_id, server_user_id, return_code, func_type=None, func_flag=None, member_id_list=None):
        ret_to_client = CGOpenTeamFuncResponse()
        ret_to_client.return_code = return_code
        ret_to_client.func_type = func_type
        ret_to_client.func_flag = func_flag
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 同步状态变化给其他成员
            recv_id_list = [x for x in member_id_list if x != server_user_id]
            if recv_id_list:
                syn_to_mem = CGSynOpenedTeamFunc()
                syn_to_mem.func_type = func_type
                syn_to_mem.func_flag = func_flag
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)

    def handle_give_up_team_func(self, server_group_id, server_user_id):
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleGiveUpTeamFunc(server_group_id, server_user_id)

    def callback_give_up_team_func(self, server_group_id, server_user_id, return_code, member_id_list=None):
        ret_to_client = CGGiveUpTeamFuncResponse()
        ret_to_client.return_code = return_code
        ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        if return_code == excp.ExceptionSuccess.code:
            # 同步状态变化给其他成员
            recv_id_list = [x for x in member_id_list if x != server_user_id]
            if recv_id_list:
                syn_to_mem = CGSynOpenedTeamFunc()
                syn_to_mem.func_type = None
                syn_to_mem.func_flag = None
                ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(syn_to_mem.dump()), recv_id_list)

    # ===============================================================
    # ============ internal functions ============
    # ===============================================================
    def do_send_team_info(self, server_group_id, team_doc, user_id_list):
        if user_id_list:
            res_to_client = CGGetTeamInfoResponse()
            if team_doc:
                # 有队伍
                res_to_client.team_id = team_doc.team_id
                res_to_client.server_leader_id = team_doc.server_leader_id
                res_to_client.func_type = team_doc.func_type
                res_to_client.func_flag = team_doc.func_flag
                res_to_client.is_in_match = self.is_team_in_match(server_group_id, team_doc.team_id)
                for mem_id in team_doc.member_id_list:
                    mem_info = MemberInfo()
                    mem_info.server_member_id = mem_id
                    mem_info.is_online = self.online_manager.is_user_online(server_group_id, mem_id)
                    res_to_client.member_info_list.append(mem_info)
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(res_to_client.dump()), user_id_list)

    def add_user_to_match(self, server_group_id, match_item):
        if server_group_id not in self.match_user_id_dict:
            self.match_user_id_dict[server_group_id] = []
        if match_item.server_user_id in self.match_user_id_dict[server_group_id]:
            self.match_user_id_dict[server_group_id].remove(match_item.server_user_id)
        self.match_user_id_dict[server_group_id].append(match_item.server_user_id)
        if server_group_id not in self.match_user_item_dict:
            self.match_user_item_dict[server_group_id] = {}
        self.match_user_item_dict[server_group_id][match_item.server_user_id] = match_item

    def add_team_to_match(self, server_group_id, match_item):
        if server_group_id not in self.match_team_id_dict:
            self.match_team_id_dict[server_group_id] = []
        if match_item.team_id in self.match_team_id_dict[server_group_id]:
            self.match_team_id_dict[server_group_id].remove(match_item.team_id)
        self.match_team_id_dict[server_group_id].append(match_item.team_id)
        if server_group_id not in self.match_team_item_dict:
            self.match_team_item_dict[server_group_id] = {}
        self.match_team_item_dict[server_group_id][match_item.team_id] = match_item

    def remove_match_user(self, server_group_id, server_user_id):
        if server_group_id in self.match_user_id_dict and server_user_id in self.match_user_id_dict[server_group_id]:
            self.match_user_id_dict[server_group_id].remove(server_user_id)

        if server_group_id in self.match_user_item_dict:
            self.match_user_item_dict[server_group_id].pop(server_user_id, None)

    def remove_match_team(self, server_group_id, team_id):
        if server_group_id in self.match_team_id_dict and team_id in self.match_team_id_dict[server_group_id]:
            self.match_team_id_dict[server_group_id].remove(team_id)

        if server_group_id in self.match_team_item_dict:
            self.match_team_item_dict[server_group_id].pop(team_id, None)

    def is_team_in_match(self, server_group_id, team_id):
        return server_group_id in self.match_team_id_dict and team_id in self.match_team_id_dict[server_group_id]

    def update_team_list_item(self, server_group_id, team_item):
        if server_group_id not in self.online_team_dict:
            self.online_team_dict[server_group_id] = {}
        self.online_team_dict[server_group_id][team_item.team_id] = team_item

    def remove_team_list_item(self, server_group_id, team_id):
        if server_group_id in self.online_team_dict:
            self.online_team_dict[server_group_id].pop(team_id, None)

    def update_team_list_item_mem_count(self, server_group_id, team_id, mem_count):
        if server_group_id in self.online_team_dict and team_id in self.online_team_dict[server_group_id]:
            self.online_team_dict[server_group_id][team_id].member_count = mem_count

    def get_server_online_team_list(self, server_group_id):
        if server_group_id not in self.online_team_dict:
            return []
        return self.online_team_dict[server_group_id].values()

    # ==================================================
    #   temp functions or test functions
    # ==================================================
    def callback_test_team_pressure(self, is_success, server_group_id, server_user_id, dist_type):
        return_data = {'is_success': is_success, 'server_group_id': server_group_id, 'server_user_id': server_user_id}
        if dist_type == 0:
            # 广播
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(return_data))
        else:
            # 模拟推送给组员
            server_id, user_id = get_server_and_user_id(server_user_id)
            start_id = (int(user_id) - 1) / 5 * 5 + 1
            recv_id_list = [ make_server_user_id(server_id, str(x), 0) for x in xrange(start_id, start_id + 5)]
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(return_data), recv_id_list)

    def handle_test_fishing(self, server_group_id, server_user_id, msg):
        ModObjFac.CreateApp().get_team_2_db_rpc().HandleTestFishing(server_group_id, server_user_id, msg)

    def callback_test_fishing(self, server_group_id, server_user_id, msg, member_id_list=None):
        if member_id_list:
            recv_id_list = [x for x in member_id_list if x != server_user_id]
            ModObjFac.CreateApp().get_team_2_team_proxy_rpc().OnTeamMsgFromTeam(server_group_id, msgpack.packb(msg), recv_id_list)