# -*- coding: utf8 -*-

import game

import random
import script.common.config.topoconfig as ModTopo
import script.common.exception_def as excp
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
from script.common.game_define.team_define import TeamListTeamItem, TeamMatchTeamItem, TeamMatchUserItem
from script.common.nodebase.appbase import CAppBase
from script.team.team_manager import TeamManager


class CTeam(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.team_manager = TeamManager()

    # child class must override functions >>>
    def get_node_type(self):
        return ModTopo.NODE_TYPE.TEAM

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # team的服务器节点: monitor、team proxy、scene proxy、db
        logger.GetLog().debug('send_msg_to_server_node : %s, %s' % (client_type, args))
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type in self.connect_server_dict and self.connect_server_dict[server_node_type]:
            if server_node_type == ModTopo.NODE_TYPE.MONITOR:
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.TEAM_PROXY:
                if client_type == server_node_type:
                    # 需要查找一个实际的node
                    client_type = self.connect_server_dict[server_node_type].keys()[0]     # 因为proxy只有1个, 所以直接取
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.TEAM, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.DB_PROXY:
                if client_type == server_node_type:
                    # 随机一个db节点处理即可
                    client_type = random.choice(self.connect_server_dict[server_node_type].keys())
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.TEAM, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.SCENE_PROXY:
                if client_type == server_node_type:
                    # 需要查找一个实际的node
                    client_type = self.connect_server_dict[server_node_type].keys()[0]     # 因为proxy只有1个, 所以直接取
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.TEAM, msg_str)
            else:
                logger.GetLog().error('send msg to an unsupported server node : %s, %s, %s' % (client_type, msg_str, args))
        else:
            logger.GetLog().error('send msg to server node %s but there is no one in connect_server_dict' % server_node_type)

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # team 节点没有客户端
        logger.GetLog().warn('team has no client node, please check the code: %s, %s, %s' % (client_node_type, msg_str, args))

    # child class must override functions <<

    # C++ API >>>
    # None
    # C++ API <<<

    # public functions >>>
    def get_team_2_team_proxy_rpc(self, client_type=None):
        if client_type:
            return self.get_client_rpc_handler(client_type)
        # 没有传参数,则传入node type, 在send_msg_to_server_node处再做判断
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.TEAM_PROXY)

    def get_team_2_scene_proxy_rpc(self, client_type=None):
        if client_type:
            return self.get_client_rpc_handler(client_type)
        # 没有传参数,则传入node type, 在send_msg_to_server_node处再做判断
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.SCENE_PROXY)

    def get_team_2_db_rpc(self):
        return self.get_send_query_rpc_handler(ModTopo.NODE_TYPE.DB_PROXY)

    def get_team_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_team_manager(self):
        return self.team_manager

    # public functions <<<

    # from team proxy >>>
    def OnTeamMsg(self, server_group_id, server_user_id, str_msg):
        logger.GetLog().debug('team server receive msg')
        self.get_team_manager().handle_team_msg(server_group_id, server_user_id, str_msg)

    def OnUserOnlineStatusUpdate(self, server_group_id, server_user_id, is_online, handle_flag):
        """
        玩家在线状态改变处理
        """
        self.get_team_manager().handle_user_online_status_update(server_group_id, server_user_id, is_online, handle_flag)

    def OnAddMatchUserItem(self, server_group_id, match_item):
        """
        同步增加玩家匹配队列
        """
        logger.GetLog().debug('syn add match user item : %s, %s' % (server_group_id, match_item))
        self.get_team_manager().add_user_to_match(server_group_id, TeamMatchUserItem.new_from_data(match_item))

    def OnAddMatchTeamItem(self, server_group_id, match_item):
        """
        同步增加队伍匹配队列
        """
        logger.GetLog().debug('syn add match team item : %s, %s' % (server_group_id, match_item))
        self.get_team_manager().add_team_to_match(server_group_id, TeamMatchTeamItem.new_from_data(match_item))

    def OnRemoveMatchItem(self, server_group_id, remove_user_id_list, remove_team_id):
        """
        同步删除匹配队列
        """
        logger.GetLog().debug('syn remove match item : %s, %s, %s' % (server_group_id, remove_user_id_list, remove_team_id))
        if remove_user_id_list:
            for server_user_id in remove_user_id_list:
                self.get_team_manager().remove_match_user(server_group_id, server_user_id)
        if remove_team_id:
            self.get_team_manager().remove_match_team(server_group_id, remove_team_id)

    def OnUpdateTeamListItem(self, server_group_id, team_item):
        """
        同步更新队伍列表
        """
        logger.GetLog().debug('syn update team list item: %s, %s' % (server_group_id, team_item))
        self.get_team_manager().update_team_list_item(server_group_id, TeamListTeamItem.new_from_data(team_item))

    def OnRemoveTeamListItem(self, server_group_id, team_id):
        """
        同步删除队伍列表数据
        """
        logger.GetLog().debug('syn remove team list item: %s, %s' % (server_group_id, team_id))
        self.get_team_manager().remove_team_list_item(server_group_id, team_id)

    def OnUpdateTeamListItemMemCount(self, server_group_id, team_id, mem_count):
        """
        同步队伍列表中队伍成员数量
        """
        logger.GetLog().debug('syn update team list item mem count: %s, %s, %s' % (server_group_id, team_id, mem_count))
        self.get_team_manager().update_team_list_item_mem_count(server_group_id, team_id, mem_count)

    # from team proxy <<<

    # from db >>>
    def OnHandleForUserOnline(self, result):
        if result[2]:
            # 有队伍
            self.get_team_manager().callback_handle_for_user_online(*result)

    def OnHandleForUserOffline(self, result):
        if result[2]:
            # 有队伍
            self.get_team_manager().callback_handle_for_user_offline(*result)

    def OnHandleTeamBossForUserOffline(self, result):
        if result[0]:
            self.get_team_manager().callback_handle_team_boss_for_user_offline(*result[1:])

    def OnLoadTeamForGetTeamInfo(self, result):
        logger.GetLog().debug('on load team info for get : %s' % (result,))
        self.get_team_manager().callback_handle_get_team_info(*result)

    def OnDoCreateTeam(self, result):
        logger.GetLog().debug('on create team result : %s' % (result,))
        self.get_team_manager().callback_do_create_team(*result)

    def OnDoSetTeamCondi(self, result):
        logger.GetLog().debug('on do set team condition result: %s' % (result,))
        self.get_team_manager().callback_do_set_team_condi(*result)

    def OnSendTeamInvite(self, result):
        logger.GetLog().debug('on send team invite result : %s' % (result,))
        self.get_team_manager().callback_send_team_invite(*result)

    def OnDoAgreeTeamInvitation(self, result):
        logger.GetLog().debug('on do agree team invite result : %s' % (result,))
        self.get_team_manager().callback_do_agree_invite(*result)

    def OnDoDenyTeamInvitation(self, result):
        logger.GetLog().debug('on do deny team invite result : %s' % (result,))
        if result[0]:   # 需要推送给邀请发起者
            self.get_team_manager().callback_do_deny_invite(*result[1:])

    def OnDoDisbandTeam(self, result):
        logger.GetLog().debug('on do disband team result : %s' % (result,))
        self.get_team_manager().callback_do_disband_team(*result)

    def OnDoLeaveTeam(self, result):
        logger.GetLog().debug('on do leave team result : %s' % (result,))
        self.get_team_manager().callback_do_leave_team(*result)

    def OnDoKickOutMember(self, result):
        logger.GetLog().debug('on do kick out team member result : %s' % (result,))
        self.get_team_manager().callback_do_kickout_mem(*result)

    def OnUserEnterMatch(self, result):
        logger.GetLog().debug('on user enter match result : %s' % (result,))
        if result[2] == excp.ExceptionSuccess.code:
            if result[3]:   # is_match
                self.get_team_manager().callback_user_enter_match(result[0], result[1], result[2], team_doc=result[4], is_team_full=result[5])
            else:
                self.get_team_manager().callback_user_enter_match(result[0], result[1], result[2], result[4])
        else:
            self.get_team_manager().callback_user_enter_match(result[0], result[1], result[2])

    def OnTeamEnterMatch(self, result):
        logger.GetLog().debug('on team enter match result : %s' % (result,))
        if result[2] == excp.ExceptionSuccess.code:
            if result[3]:   # find_user_id_list
                # 找到了玩家
                is_full = result[4]
                if is_full:
                    self.get_team_manager().callback_team_enter_match(result[0], result[1], result[2], result[3], result[5])
                else:
                    self.get_team_manager().callback_team_enter_match(result[0], result[1], result[2], result[3], result[5], result[6])
            else:
                # 没找到玩家
                self.get_team_manager().callback_team_enter_match(result[0], result[1], result[2], match_item=result[4])
        else:
            self.get_team_manager().callback_team_enter_match(result[0], result[1], result[2])

    def OnAcceptTeamCall(self, result):
        logger.GetLog().debug('on accept team call result : %s' % (result,))
        self.get_team_manager().callback_accept_team_call(*result)

    def OnApplyEnterTeam(self, result):
        server_group_id = result[0]
        server_user_id = result[1]
        return_code = result[2]
        if return_code == excp.ExceptionSuccess.code:
            if result[3]:
                self.get_team_manager().callback_apply_enter_team(server_group_id, server_user_id, return_code, result[3], result[4], result[5])
            else:
                self.get_team_manager().callback_apply_enter_team(server_group_id, server_user_id, return_code, result[3], result[4], user_lv=result[5],
                                                                                   user_name=result[6])
        else:
            self.get_team_manager().callback_apply_enter_team(server_group_id, server_user_id, return_code)

    def OnAgreeTeamApply(self, result):
        logger.GetLog().debug('on agree team apply result : %s' % (result,))
        self.get_team_manager().callback_agree_team_apply(*result)

    def OnDenyTeamApply(self, result):
        logger.GetLog().debug('on deny team apply result : %s' % (result,))
        self.get_team_manager().callback_deny_team_apply(*result)

    def OnLoadTeamForCancelTeamMatch(self, result):
        self.get_team_manager().callback_team_cancel_match(*result)

    def OnInternalCheckTeamMatch(self, result):
        if result[0]:
            if result[3]:
                self.get_team_manager().callback_internal_check_team_match(result[1], result[2], result[3], result[4])
            else:
                self.get_team_manager().callback_internal_check_team_match(result[1], result[2], result[3], result[4], result[5])

    def OnHandleSendCallMemEnterFunc(self, result):
        self.get_team_manager().callback_send_call_mem_enter_func(*result)

    def OnHandleMemEnterReady(self, result):
        self.get_team_manager().callback_member_enter_ready(*result)

    def OnHandleMemCancelReady(self, result):
        self.get_team_manager().callback_member_cancel_ready(*result)

    def OnHandleGetAllReadyMem(self, result):
        self.get_team_manager().callback_get_all_ready_mem(*result)

    def OnHandleGetTeamOpenedFunc(self, result):
        self.get_team_manager().callback_get_team_opened_func(*result)

    def OnHandleOpenTeamFunc(self, result):
        self.get_team_manager().callback_open_team_func(*result)

    def OnHandleGiveUpTeamFunc(self, result):
        self.get_team_manager().callback_give_up_team_func(*result)

    def OnHandleTestFishing(self, result):
        self.get_team_manager().callback_test_fishing(*result)

    # from db <<<

    # from monitor >>>
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('team on gm msg content = %s, %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_team_2_monitor_rpc().OnGMMsgResponse('team %s executed gm command %s fail, fail files : %s' % (self.get_node_id(), gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_team_2_monitor_rpc().OnGMMsgResponse('team %s executed gm command %s success' % (self.get_node_id(), gm_cmd))
        else:
            return_msg = 'team unsupported gm command or param unexpected : %s, %s' % (gm_cmd, params_str)
            logger.GetLog().warn(return_msg)
            self.get_team_2_monitor_rpc().OnGMMsgResponse(return_msg)
    # from monitor <<<

