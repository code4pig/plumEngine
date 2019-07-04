# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import time

import script.common.exception_def as excp
import script.common.game_define.team_define as team_def
import script.common.log as logger
from script.common.db.data_context import DataContext
from script.common.db.instant_box import instant_box
from script.common.game_define.global_def import get_server_and_user_id
from script.common.game_define.team_define import TeamMatchUserItem, TeamMatchTeamItem
from script.dbproxy.do.counter_team_do import CounterTeamDo
from script.dbproxy.do.masters_global import master_team_boss_inst
from script.dbproxy.do.team_apply_info_do import TeamApplyInfoDo
from script.dbproxy.do.team_boss_do import TeamBossDo
from script.dbproxy.do.team_do import TeamDo
from script.dbproxy.do.user_do import UserDo
from script.dbproxy.do.user_raid_do import UserRaidDo
from script.dbproxy.do.user_team_do import UserTeamDo
from script.dbproxy.rpc.irpctarget import IDbsRpcTarget
from script.dbproxy.scene2dbrpchandler import Scene2DbRpcHandler


class Tm2DbRpcHandler(IDbsRpcTarget):
    def __init__(self):
        pass

    def Reload(self, modname):
        import script.common.utils.utils as utils
        utils.Reload(modname)

    def HandleForUserOnline(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, None
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            logger.GetLog().error('team data is not match : %s, %s, %s' % (server_group_id, server_user_id, user_team_do.doc.team_id))
            return server_group_id, server_user_id, None
        return server_group_id, server_user_id, team_do.doc

    def HandleForUserOffline(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, None
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            logger.GetLog().error('team data is not match : %s, %s, %s' % (server_group_id, server_user_id, user_team_do.doc.team_id))
            return server_group_id, server_user_id, None
        return server_group_id, server_user_id, team_do.doc

    def HandleTeamBossForUserOffline(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                return False,
            team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                logger.GetLog().error('team data is not match : %s, %s, %s' % (server_group_id, server_user_id, user_team_do.doc.team_id))
                return False,
            team_boss_do = TeamBossDo.TryLock(500)(data_context, user_team_do.doc.team_id)
            if team_boss_do.is_new:
                data_context.unlock()
                return False,
            if server_user_id != team_do.doc.server_leader_id and server_user_id in team_boss_do.doc.ready_member_list:
                team_boss_do.member_cancel_ready(server_user_id)
                data_context.save()
                data_context.unlock()
                return True, server_group_id, server_user_id, team_do.doc.opened_func_type, team_boss_do.doc.boss_key, team_do.doc.member_id_list
            data_context.unlock()
            return False,
        except Exception as e:
            logger.GetLog().error('HandleTeamBossForUserOffline catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return False,

    def LoadTeamForGetTeamInfo(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, None
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            logger.GetLog().error('team data is not match : %s, %s, %s' % (server_group_id, server_user_id, user_team_do.doc.team_id))
            return server_group_id, server_user_id, None
        return server_group_id, server_user_id, team_do.doc

    def DoCreateTeam(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_do = UserDo.Reader()(data_context, user_id)
        user_lv = user_do.level
        need_lv = 1     # TODO: 读取配置表组队系统开放等级(或其他检查)
        if user_lv < need_lv:
            return server_group_id, server_user_id, excp.ExceptionLvNotEnough.code

        user_team_do = UserTeamDo(data_context, user_id)
        if user_team_do.has_team():
            # 已有队伍
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code
        try:
            team_id = CounterTeamDo().increase()
            team_do = TeamDo(data_context, team_id)
            team_do.create_new_team(team_id, server_user_id, user_do.name, instant_box.time_current)
            user_team_do.update_user_team(team_id)
            scene_user_info = Scene2DbRpcHandler.make_scene_user_info(data_context, server_user_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_id, scene_user_info
        except Exception as e:
            logger.GetLog().error('create team catch an exception : %s' % e)
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionCreateTeamFail.code

    def DoSetTeamCondi(self, server_group_id, server_user_id, func_type, func_flag):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        if (not func_type and not func_flag) or self.check_func_valid(func_type, func_flag):
            # 设置目标为空 或 有设置目标
            data_context = DataContext()
            instant_box.data_context = data_context
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            else:
                # if func_type == team_def.TEAM_FUNC_TYPE_BOSS_RAID:
                #     # 地龙，额外检查是否队长有选择条件
                #     user_raid_do = UserRaidDo.Reader()(data_context, user_id)
                #     if not user_raid_do.doc.boss:
                #         return server_group_id, server_user_id, excp.ExceptionUserHasNoRaid.code
                #     elif user_raid_do.doc.boss.time_end <= instant_box.time_current:
                #         return server_group_id, server_user_id, excp.ExceptionUserRaidTimeout.code
                try:
                    team_do = TeamDo(data_context, user_team_do.doc.team_id)
                    if team_do.doc.server_leader_id != server_user_id:
                        data_context.unlock()
                        return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
                    else:
                        team_do.update_team_match_condi(func_type, func_flag)
                        data_context.save()
                        data_context.unlock()
                        return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.doc
                except Exception as e:
                    logger.GetLog().error('DoSetTeamCondi catch an error : %s' % excp.log_exceptions(exception=e))
                    data_context.unlock()
                    return server_group_id, server_user_id, excp.ExceptionUnknown.code
        else:
            return server_group_id, server_user_id, excp.ExceptionTeamCondiParam.code

    def SendTeamInvite(self, server_group_id, server_user_id, target_server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        # 是否有组队
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            logger.GetLog().error('team data not match : %s, %s, %s' % (server_group_id, server_user_id, user_team_do.doc.team_id))
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        # 是否队伍已满
        if team_do.is_member_full():
            return server_group_id, server_user_id, excp.ExceptionTeamFull.code

        # 成员也可以邀请好友,所以取消判断
        # if team_do.doc.server_leader_id != server_user_id:
        #     data_context.unlock()
        #     return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code

        # 被邀者是否有组队
        target_server_id, target_user_id = get_server_and_user_id(target_server_user_id)
        target_user_team_do = UserTeamDo.Reader()(data_context, target_user_id, target_server_id)
        if target_user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code

        target_user_do = UserDo.Reader()(data_context, target_user_id, target_server_id)
        if target_user_do.is_new:
            return server_group_id, server_user_id, excp.ExceptionUserNotExist.code
        # TODO：检查被邀者的等级是否达到组队, 是否在战斗中?
        need_lv = 1
        if target_user_do.level < need_lv:
            return server_group_id, server_user_id, excp.ExceptionLvNotEnough.code
        user_name = UserDo.Reader()(data_context, user_id).name
        return server_group_id, server_user_id, excp.ExceptionSuccess.code, target_server_user_id, user_name, team_do.doc

    def DoAgreeTeamInvitation(self, server_group_id, server_user_id, team_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo(data_context, user_id)
            if user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code

            team_do = TeamDo(data_context, team_id)
            if team_do.is_new:
                data_context.unlock()   # 主动释放
                return server_group_id, server_user_id, excp.ExceptionTeamNotExist.code
            if team_do.is_member_full():
                data_context.unlock()   # 主动释放
                return server_group_id, server_user_id, excp.ExceptionTeamFull.code

            user_team_do.update_user_team(team_do.team_id)
            team_do.add_member(server_user_id)
            user_name = UserDo.Reader()(data_context, user_id).name
            scene_user_info = Scene2DbRpcHandler.make_scene_user_info(data_context, server_user_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, user_name, team_do.doc, team_do.is_member_full(), scene_user_info
        except Exception as e:
            logger.GetLog().error('DoAgreeTeamInvitation catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def DoDenyTeamInvitation(self, server_group_id, server_user_id, team_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        team_do = TeamDo.Reader()(data_context, team_id)
        if team_do.is_new or team_do.is_member_full():
            return False,
        user_name = UserDo.Reader()(data_context, user_id).name
        return True, server_group_id, team_do.doc.server_leader_id, server_user_id, user_name

    def DoDisbandTeam(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo(data_context, user_id)
            if not user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            team_do = TeamDo(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                logger.GetLog().error('user team has data but team data not found : %s, %s' % (server_user_id, user_team_do.doc.team_id))
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if team_do.doc.server_leader_id != server_user_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
            logger.GetLog().info('disband team success: %s, %s, %s' % (server_group_id, server_user_id, team_do.team_id))
            user_team_do.delete()
            recv_id_list = []
            for server_mem_id in team_do.doc.member_id_list:
                if server_mem_id != server_user_id:
                    mem_server_id, mem_id = get_server_and_user_id(server_mem_id)
                    mem_team_do = UserTeamDo(data_context, mem_id, mem_server_id)
                    mem_team_do.delete()
                    recv_id_list.append(server_mem_id)
            team_do.delete()
            team_apply_do = TeamApplyInfoDo(data_context, team_do.team_id)
            if not team_apply_do.is_new:
                team_apply_do.delete()
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.team_id, recv_id_list
        except Exception as e:
            logger.GetLog().error('DoDisbandTeam catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def DoLeaveTeam(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo(data_context, user_id)
            if not user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            team_do = TeamDo(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                logger.GetLog().error('user team data is not match: %s, %s' % (server_user_id, user_team_do.doc.team_id))
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if team_do.doc.server_leader_id == server_user_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamLeaderCannotLeave.code
            user_team_do.delete()
            team_do.member_leave(server_user_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.doc.team_id, team_do.doc.member_id_list
        except Exception as e:
            logger.GetLog().error('DoLeaveTeam catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def DoKickOutMember(self, server_group_id, server_user_id, server_member_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            team_do = TeamDo(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                logger.GetLog().error('user team data is not match: %s, %s' % (server_user_id, user_team_do.doc.team_id))
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if team_do.doc.server_leader_id != server_user_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
            if server_member_id not in team_do.doc.member_id_list:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionKickNotMember.code
            member_server_id, member_id = get_server_and_user_id(server_member_id)
            mem_team_do = UserTeamDo(data_context, member_id, member_server_id)
            mem_team_do.delete()
            recv_id_list = [x for x in team_do.doc.member_id_list]  # 被踢消息要推送给所有人,包括被踢者,所以要放到member_leave之前
            team_do.member_leave(server_member_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.doc.team_id, server_member_id, recv_id_list
        except Exception as e:
            logger.GetLog().error('DoKickOutMember catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def UserEnterMatch(self, server_group_id, server_user_id, func_flag, match_team_id_list, match_team_item_dict):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo(data_context, user_id)
            if user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code
            user_lv = UserDo.Reader()(data_context, user_id).level
            # 构造item对象
            match_item = TeamMatchUserItem()
            match_item.server_user_id = server_user_id
            match_item.user_lv = user_lv
            match_item.func_flag = func_flag
            if not match_team_item_dict:
                # 队伍匹配队列无数据
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, False, match_item
            # 遍历找到合适的
            team_do = self.find_match_team_for_user(data_context, match_item, match_team_id_list, match_team_item_dict)
            if team_do is None:
                # 没找到匹配的队伍
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, False, match_item
            # 更新玩家队伍数据
            user_team_do.update_user_team(team_do.team_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, True, team_do.doc, team_do.is_member_full()
        except Exception as e:
            logger.GetLog().error('UserEnterMatch catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def TeamEnterMatch(self, server_group_id, server_user_id, match_user_id_list, match_user_item_dict, match_team_item_dict):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if match_team_item_dict and user_team_do.doc.team_id in match_team_item_dict:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionAlreadyInMatch.code
            team_do = TeamDo(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                data_context.unlock()
                logger.GetLog().error('data not match : %s, %s, %s' % (server_group_id, server_user_id, user_team_do.doc.team_id))
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if team_do.doc.server_leader_id != server_user_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
            if not team_do.doc.func_type or not team_do.doc.func_flag:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionNoTeamCondi.code
            if team_do.is_member_full():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamFull.code
            match_item = TeamMatchTeamItem()
            match_item.team_id = team_do.team_id
            match_item.func_flag = team_do.doc.func_flag
            if not match_user_item_dict:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, None, match_item
            find_user_id_list = self.find_match_user_for_team(data_context, team_do, match_item, match_user_id_list, match_user_item_dict)
            if not find_user_id_list:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, None, match_item
            data_context.save()
            data_context.unlock()
            if team_do.is_member_full():
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, find_user_id_list, True, team_do.doc
            else:
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, find_user_id_list, False, team_do.doc, match_item
        except Exception as e:
            logger.GetLog().error('TeamEnterMatch catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def AcceptTeamCall(self, server_group_id, server_user_id, team_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            team_do = TeamDo(data_context, team_id)
            if team_do.is_new:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamNotExist.code
            if team_do.is_member_full():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamFull.code
            user_team_do = UserTeamDo(data_context, user_id)
            if user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code
            recv_id_list = [x for x in team_do.doc.member_id_list]
            team_do.add_member(server_user_id)
            user_team_do.update_user_team(team_id)
            scene_user_info = Scene2DbRpcHandler.make_scene_user_info(data_context, server_user_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.doc, recv_id_list, team_do.is_member_full(), scene_user_info
        except Exception as e:
            logger.GetLog().error('AcceptTeamCall catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def ApplyEnterTeam(self, server_group_id, server_user_id, team_id, is_team_in_match):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            if is_team_in_match:
                user_team_do = UserTeamDo(data_context, user_id)
            else:
                user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if user_team_do.has_team():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code
            if is_team_in_match:
                team_do = TeamDo(data_context, team_id)
            else:
                team_do = TeamDo.Reader()(data_context, team_id)
            if team_do.is_new or not team_do.doc.team_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamNotExist.code
            if team_do.is_member_full():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamFull.code
            user_do = UserDo.Reader()(data_context, user_id)
            user_lv = user_do.level
            # TODO:检查是否开放了组队
            team_apply_do = TeamApplyInfoDo(data_context, team_id)
            if is_team_in_match:
                # 自动匹配的队伍,直接自动入队
                user_team_do.update_user_team(team_id)
                team_do.add_member(server_user_id)
                team_apply_do.remove_team_apply(server_user_id)
                data_context.save()
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, True, team_do.doc, team_do.is_member_full()
            else:
                if team_apply_do.is_in_apply(server_user_id):
                    data_context.unlock()
                    return server_group_id, server_user_id, excp.ExceptionAlreadyApplyEnterTeam.code
                team_apply_do.add_team_apply(server_user_id)
                data_context.save()
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, False, team_do.doc, user_lv, user_do.name
        except Exception as e:
            logger.GetLog().error('ApplyEnterTeam catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def AgreeTeamApply(self, server_group_id, server_user_id, server_applyer_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            team_do = TeamDo(data_context, user_team_do.doc.team_id)
            if team_do.is_new or not team_do.doc.team_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if team_do.doc.server_leader_id != server_user_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
            if team_do.is_member_full():
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionTeamFull.code
            # 删除申请列表数据
            team_apply_do = TeamApplyInfoDo(data_context, team_do.doc.team_id)
            team_apply_do.remove_team_apply(server_applyer_id)
            applyer_server_id, applyer_id = get_server_and_user_id(server_applyer_id)
            applyer_team_do = UserTeamDo(data_context, applyer_id, applyer_server_id)
            if applyer_team_do.doc.team_id:
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code
            applyer_team_do.update_user_team(team_do.doc.team_id)
            team_do.add_member(server_applyer_id)
            scene_user_info = Scene2DbRpcHandler.make_scene_user_info(data_context, server_applyer_id)
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, server_applyer_id, scene_user_info, team_do.doc, team_do.is_member_full()
        except Exception as e:
            logger.GetLog().error('AgreeTeamApply catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def DenyTeamApply(self, server_group_id, server_user_id, server_applyer_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new or not team_do.doc.team_id:
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        if team_do.doc.server_leader_id != server_user_id:
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
        # 删除申请列表数据
        team_apply_do = TeamApplyInfoDo(data_context, team_do.doc.team_id)
        team_apply_do.remove_team_apply(server_applyer_id)
        # 检查是否已有组队
        applyer_server_id, applyer_id = get_server_and_user_id(server_applyer_id)
        applyer_team_do = UserTeamDo.Reader()(data_context, applyer_id, applyer_server_id)
        if applyer_team_do.has_team():
            data_context.save()
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionAlreadyHasTeam.code
        data_context.save()
        data_context.unlock()
        return server_group_id, server_user_id, excp.ExceptionSuccess.code, server_applyer_id, team_do.doc.team_id, team_do.doc.leader_name

    def LoadTeamForCancelTeamMatch(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new or not team_do.doc.team_id:
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        if team_do.doc.server_leader_id != server_user_id:
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
        return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.doc.team_id, team_do.doc.member_id_list

    def InternalCheckTeamMatch(self, server_group_id, team_id, match_user_id_list, match_user_item_dict):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            team_do = TeamDo(data_context, team_id)
            if team_do.is_new or not team_do.doc.team_id:
                data_context.unlock()
                return False,
            if not team_do.doc.func_type or not team_do.doc.func_flag:
                data_context.unlock()
                return False,
            if team_do.is_member_full():
                data_context.unlock()
                return False,
            match_item = TeamMatchTeamItem()
            match_item.team_id = team_do.team_id
            match_item.func_flag = team_do.doc.func_flag
            if not match_user_item_dict:
                data_context.unlock()
                return False,
            find_user_id_list = self.find_match_user_for_team(data_context, team_do, match_item, match_user_id_list, match_user_item_dict)
            if not find_user_id_list:
                data_context.unlock()
                return False,
            data_context.save()
            data_context.unlock()
            if team_do.is_member_full():
                return True, server_group_id, find_user_id_list, True, team_do.doc
            else:
                return True, server_group_id, find_user_id_list, False, team_do.doc, match_item
        except Exception as e:
            logger.GetLog().error('InternalCheckTeamMatch catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return False,

    def HandleSendCallMemEnterFunc(self, server_group_id, server_user_id, func_type, func_flag):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        if not self.check_func_valid(func_type, func_flag):
            return server_group_id, server_user_id, excp.ExceptionParamError.code
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)

        if team_do.is_new:
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        if team_do.doc.server_leader_id != server_user_id:
            return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
        if team_do.doc.opened_func_type != func_type:
            return server_group_id, server_user_id, excp.ExceptionFuncFlagNotCurOpened.code
        if func_type == team_def.TEAM_FUNC_TYPE_BOSS_FAFURION or func_type == team_def.TEAM_FUNC_TYPE_BOSS_VALAKAS:
            if not TeamBossDo.is_in_team_boss_activity_time(instant_box.time_current):
                return server_group_id, server_user_id, excp.ExceptionNotActivityTime.code
            team_boss_do = TeamBossDo.Reader()(data_context, team_do.team_id)
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, team_boss_do.doc.boss_key, team_do.doc.member_id_list
        elif func_type == team_def.TEAM_FUNC_TYPE_BOSS_RAID:
            team_boss_do = TeamBossDo.Reader()(data_context, team_do.team_id)
            if team_boss_do.doc.end_time <= instant_box.time_current:
                return server_group_id, server_user_id, excp.ExceptionTeamBossFinished.code
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, team_boss_do.doc.boss_key, team_do.doc.member_id_list
        return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def HandleMemEnterReady(self, server_group_id, server_user_id, func_type, func_flag):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            if not TeamBossDo.is_in_team_boss_activity_time(instant_box.time_current):
                return server_group_id, server_user_id, excp.ExceptionNotActivityTime.code
            if not self.check_func_valid(func_type, func_flag):
                return server_group_id, server_user_id, excp.ExceptionParamError.code
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if func_type in team_def.TEAM_FUNC_TYPE_LIST:
                team_boss_do = TeamBossDo.TryLock(500)(data_context, team_do.team_id)
                if team_boss_do.is_boss_expired():
                    data_context.unlock()
                    return server_group_id, server_user_id, excp.ExceptionTeamBossExpired.code
                if team_boss_do.is_team_boss_finish():
                    data_context.unlock()
                    return server_group_id, server_user_id, excp.ExceptionTeamBossFinished.code
                if team_do.doc.opened_func_type != func_type or team_boss_do.doc.boss_key != func_flag:
                    return server_group_id, server_user_id, excp.ExceptionFuncFlagNotCurOpened.code
                if team_boss_do.is_second_step_in_battle():
                    data_context.unlock()
                    return server_group_id, server_user_id, excp.ExceptionTeamBossInBattle.code
                team_boss_do.member_be_ready(server_user_id)
                data_context.save()
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, team_boss_do.doc.boss_key, team_do.doc.server_leader_id == server_user_id,\
                    team_do.doc.member_id_list
            return server_group_id, server_user_id, excp.ExceptionUnknown.code
        except Exception as e:
            logger.GetLog().error('HandleMemEnterReady catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def HandleMemCancelReady(self, server_group_id, server_user_id, func_type, func_flag):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            if not TeamBossDo.is_in_team_boss_activity_time(instant_box.time_current):
                return server_group_id, server_user_id, excp.ExceptionNotActivityTime.code
            if not self.check_func_valid(func_type, func_flag):
                return server_group_id, server_user_id, excp.ExceptionParamError.code
            user_team_do = UserTeamDo.Reader()(data_context, user_id)
            if not user_team_do.has_team():
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
            if team_do.is_new:
                return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
            if func_type in team_def.TEAM_FUNC_TYPE_LIST:
                team_boss_do = TeamBossDo.TryLock(500)(data_context, team_do.team_id)
                team_boss_do.member_cancel_ready(server_user_id)
                data_context.save()
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, func_flag, team_do.doc.member_id_list
            return server_group_id, server_user_id, excp.ExceptionUnknown.code
        except Exception as e:
            logger.GetLog().error('HandleMemCancelReady catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def HandleGetAllReadyMem(self, server_group_id, server_user_id, func_type, func_flag):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        if not self.check_func_valid(func_type, func_flag):
            return server_group_id, server_user_id, excp.ExceptionParamError.code, func_type, func_flag
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code, func_type, func_flag
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code, func_type, func_flag
        if func_type in team_def.TEAM_FUNC_TYPE_LIST:
            team_boss_do = TeamBossDo.Reader()(data_context, team_do.team_id)
            if team_boss_do.is_new or team_boss_do.is_boss_expired() or team_boss_do.is_team_boss_finish():
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, func_flag, []
            return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, func_flag, team_boss_do.doc.ready_member_list
        return server_group_id, server_user_id, excp.ExceptionUnknown.code, func_type, func_flag

    def HandleGetTeamOpenedFunc(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, None, None
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return server_group_id, server_user_id, None, None
        if not team_do.doc.opened_func_type:
            return server_group_id, server_user_id, None, None
        if team_do.doc.opened_func_type in team_def.TEAM_FUNC_TYPE_LIST:
            team_boss_do = TeamBossDo.Reader()(data_context, team_do.team_id)
            if team_boss_do.is_new or team_boss_do.is_boss_expired() or team_boss_do.is_team_boss_finish():
                return server_group_id, server_user_id, None, None
            else:
                return server_group_id, server_user_id, team_do.doc.opened_func_type, team_boss_do.doc.boss_key
        return server_group_id, server_user_id, None, None

    def HandleOpenTeamFunc(self, server_group_id, server_user_id, func_type, func_flag):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not self.check_func_valid(func_type, func_flag):
            return server_group_id, server_user_id, excp.ExceptionParamError.code
        if not user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        if team_do.doc.server_leader_id != server_user_id:
            return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
        try:
            # 检查当前开启的玩法是否还在进行
            if team_do.doc.opened_func_type in team_def.TEAM_FUNC_TYPE_LIST:
                # 检查组队BOSS是否进行中
                team_boss_do = TeamBossDo.Reader()(data_context, team_do.team_id)
                if team_boss_do.is_on_going():
                    return server_group_id, server_user_id, excp.ExceptionOtherFuncOnGoing.code
            # 没有玩法正在进行,可以开启该玩法
            if func_type in team_def.TEAM_FUNC_TYPE_LIST:
                create_time = instant_box.time_current
                end_time = 0
                # 检查是否在可开启时间
                if func_type == team_def.TEAM_FUNC_TYPE_BOSS_FAFURION or func_type == team_def.TEAM_FUNC_TYPE_BOSS_VALAKAS:
                    if not TeamBossDo.is_in_team_boss_activity_time(instant_box.time_current):
                        return server_group_id, server_user_id, excp.ExceptionNotActivityTime.code
                    end_time = TeamBossDo.cal_team_boss_end_time(instant_box.time_current)
                elif func_type == team_def.TEAM_FUNC_TYPE_BOSS_RAID:
                    user_raid_do = UserRaidDo.Reader()(data_context, user_id)
                    if not user_raid_do.doc.boss:
                        return server_group_id, server_user_id, excp.ExceptionUserHasNoRaid.code
                    elif user_raid_do.doc.boss.time_end <= instant_box.time_current:
                        return server_group_id, server_user_id, excp.ExceptionUserRaidTimeout.code
                    create_time = user_raid_do.doc.boss.time_start
                    end_time = user_raid_do.doc.boss.time_end
                team_boss_do = TeamBossDo.TryLock(500)(data_context, team_do.team_id)
                team_boss_do.refresh_new_team_boss(func_type, func_flag, create_time, end_time)
                team_boss_do.member_be_ready(server_user_id)
                # 更新队伍玩法状态数据
                team_do = TeamDo(data_context, user_team_do.doc.team_id)
                team_do.update_team_opened_func(func_type)
                data_context.save()
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, func_type, func_flag, team_do.doc.member_id_list
            data_context.unlock()
            logger.GetLog().error('================== HandleOpenTeamFunc unexpected func type : %s' % func_type)
            return server_group_id, server_user_id, excp.ExceptionParamError.code
        except Exception as e:
            logger.GetLog().error('HandleOpenTeamFunc catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    def HandleGiveUpTeamFunc(self, server_group_id, server_user_id):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return server_group_id, server_user_id, excp.ExceptionHasNoTeam.code
        if team_do.doc.server_leader_id != server_user_id:
            return server_group_id, server_user_id, excp.ExceptionNotTeamLeader.code
        try:
            if not team_do.doc.func_type:
                return server_group_id, server_user_id, excp.ExceptionNoFuncOpened.code
            if team_do.doc.opened_func_type in team_def.TEAM_FUNC_TYPE_LIST:
                team_boss_do = TeamBossDo.TryLock(500)(data_context, team_do.team_id)
                if team_boss_do.is_any_battle_going():
                    return server_group_id, server_user_id, excp.ExceptionAnyBattleOnGoing.code
                team_boss_do.give_up()
                team_do = TeamDo(data_context, user_team_do.doc.team_id)
                team_do.update_team_opened_func(None)
                data_context.save()
                data_context.unlock()
                return server_group_id, server_user_id, excp.ExceptionSuccess.code, team_do.doc.member_id_list
            data_context.unlock()
            logger.GetLog().error('================== HandleGiveUpTeamFunc unexpected func type : %s' % team_do.doc.opened_func_type)
            return server_group_id, server_user_id, excp.ExceptionParamError.code
        except Exception as e:
            logger.GetLog().error('HandleGiveUpTeamFunc catch an error : %s' % excp.log_exceptions(exception=e))
            data_context.unlock()
            return server_group_id, server_user_id, excp.ExceptionUnknown.code

    # ===============================================================
    # ============ internal functions ============
    # ===============================================================
    def find_match_team_for_user(self, data_context, match_item, match_team_id_list, match_team_item_dict):
        for team_id in match_team_id_list:
            team_item = match_team_item_dict.get(team_id)
            if team_item.func_flag == match_item.func_flag:
                # 找到目标,检查是否满足
                team_do = TeamDo(data_context, team_item.team_id)
                if not team_do.is_new and not team_do.is_member_full():
                    # 有队伍且还有位置,添加到队伍
                    team_do.add_member(match_item.server_user_id)
                    return team_do
        return None

    def find_match_user_for_team(self, data_context, team_do, match_item, match_user_id_list, match_user_item_dict):
        find_user_id_list = []
        for server_user_id in match_user_id_list:
            user_item = match_user_item_dict.get(server_user_id)
            if user_item.func_flag == match_item.func_flag:
                # 找到目标,检查条件
                user_team_do = UserTeamDo(data_context, server_user_id)
                if not user_team_do.has_team():
                    # 当前还没有队伍
                    team_do.add_member(server_user_id)
                    user_team_do.update_user_team(team_do.team_id)
                    find_user_id_list.append(server_user_id)
                    if team_do.is_member_full():
                        return find_user_id_list
        return find_user_id_list

    def check_func_valid(self, func_type, func_flag):
        """
        根据不同类型玩法,分别检查具体玩法标识是否合法
        """
        return func_flag and func_flag in master_team_boss_inst.get_func_type_key_list(func_type)
        # if func_type == team_def.TEAM_FUNC_TYPE_BOSS_FAFURION:
        #     return func_flag and func_flag in master_team_boss_inst.get_func_type_key_list(func_type)
        # elif func_type == team_def.TEAM_FUNC_TYPE_BOSS_RAID:
        #     return func_flag and func_flag in master_team_boss_inst.get_func_type_key_list(func_type)
        # elif func_type == team_def.TEAM_FUNC_TYPE_BOSS_VALAKAS:
        #     return func_flag and func_flag in master_team_boss_inst.get_func_type_key_list(func_type)
        # return False

    # ==================================================
    #   temp functions or test functions
    # ==================================================
    def TestTeamPressure(self, server_group_id, server_user_id, is_reader, dist_type):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        try:
            user_do = UserDo(data_context, user_id)
            user_team_do = UserTeamDo(data_context, user_id)
            team_id = int(user_id) % 10 + 10000
            team_do = TeamDo(data_context, team_id)
            data_context.save()
            data_context.unlock()
            return True, server_group_id, server_user_id, dist_type
        except Exception as e:
            logger.GetLog().error('============== test team pressure error : %s' % e)
        finally:
            data_context.unlock()
            return False, server_group_id, server_user_id, dist_type

    def HandleTestFishing(self, server_group_id, server_user_id, msg):
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_team_do = UserTeamDo.Reader()(data_context, user_id)
        if not user_team_do.has_team():
            return server_group_id, server_user_id, msg
        team_do = TeamDo.Reader()(data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return server_group_id, server_user_id, msg
        return server_group_id, server_user_id, msg, team_do.doc.member_id_list
