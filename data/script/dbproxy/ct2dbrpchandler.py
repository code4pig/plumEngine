# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import json

import time

import script.common.exception_def as excp
import script.common.log as logger
import script.chat.chatting_def as chat_def

from script.chat.chatting_def import P2POfflineMsg
from script.common.db.data_context import DataContext
from script.common.db.instant_box import instant_box
from script.dbproxy.do.character_log_info_do import CharacterLogInfoDo
from script.dbproxy.do.clan_chatting_msg_do import ClanChattingMsgDo
from script.dbproxy.do.log_server_online_do import LogServerOnlineDo
from script.dbproxy.do.p2p_chatting_msg_do import P2PChattingMsgDo
from script.dbproxy.do.public_chatting_msg_do import PublicChattingMsgDo
from script.dbproxy.do.simple_clan_do import ClanDo
from script.dbproxy.do.simple_user_clan_do import UserClanDo
from script.dbproxy.do.team_do import TeamDo
from script.dbproxy.do.user_session_do import UserSessionDo
from script.dbproxy.do.user_team_do import UserTeamDo
from script.dbproxy.rpc.irpctarget import IDbsRpcTarget
from script.dbproxy.do.user_do import UserDo
from script.dbproxy.do.game_logger import game_logger_inst
from script.common.db.game_log_def import GameLogOperation, GameLogFieldName
from script.common.game_define.global_def import get_server_list_in_group, get_server_and_user_id


class Ct2DbRpcHandler(IDbsRpcTarget):
    def __init__(self):
        pass

    def Reload(self, modname):
        import script.common.utils.utils as utils
        utils.Reload(modname)

    def AddPublicChatMsg(self, msg_content, msg_time, server_sender_id, server_group_id):
        logger.GetLog().debug('add public chat msg : %s, %s, %s' % (server_sender_id, server_group_id, msg_content))
        instant_box.server_group = server_group_id
        instant_box.server_user_id = server_sender_id
        instant_box.time_current = msg_time
        instant_box.data_context = DataContext()
        try:
            PublicChattingMsgDo(instant_box.data_context).add_msg(msg_content, instant_box.time_current, server_sender_id)
            if server_sender_id:
                # 有发送者的公共聊天信息,存日志
                server_id, sender_id = get_server_and_user_id(server_sender_id)
                instant_box.server_selected = server_id
                user_do = UserDo.Reader()(instant_box.data_context, sender_id)
                aofei_account_id = user_do.doc.aofei_account_id
                if aofei_account_id:
                    game_logger_inst.start_log(aofei_account_id, GameLogOperation.chat)
                    game_logger_inst.push_log_param(GameLogFieldName.server, server_id)
                    game_logger_inst.push_log_param(GameLogFieldName.account_id, aofei_account_id)
                    game_logger_inst.push_log_param(GameLogFieldName.role_id, sender_id)
                    game_logger_inst.push_log_param(GameLogFieldName.role_name, user_do.name)
                    game_logger_inst.push_log_param(GameLogFieldName.role_level, user_do.level)
                    game_logger_inst.push_log_param(GameLogFieldName.content, json.dumps(msg_content).decode('unicode-escape'))
                    game_logger_inst.push_log_param(GameLogFieldName.channel, chat_def.CHAT_CHANNEL_TYPE_PUBLIC)
                    game_logger_inst.push_log_param(GameLogFieldName.chat_time, instant_box.time_current)
                    game_logger_inst.end_log()
            instant_box.data_context.save()
        except Exception as e:
            logger.GetLog().error('add public chat msg or write chat log err : %s, %s, %s, %s' % (server_sender_id, server_group_id, msg_content, e))
        finally:
            instant_box.data_context.unlock()  # 主动unlock

    def AddPublicChatMsgBatch(self, msg_dict):
        logger.GetLog().debug('add public chat msg batch: %s' % len(msg_dict))
        for server_group_id in msg_dict:
            instant_box.server_group = server_group_id
            instant_box.data_context = DataContext()
            instant_box.time_current = time.time()
            try:
                public_msg_do = PublicChattingMsgDo.TryLock(1000)(instant_box.data_context)
            except Exception as e:
                logger.GetLog().error('lock public chatting msg error : %s, %s, %s' % (server_group_id, e, e.message))
                return
            for chat_msg_data, msg_time, server_sender_id in msg_dict[server_group_id]:
                public_msg_do.add_msg(chat_msg_data, msg_time, server_sender_id)
                try:
                    if server_sender_id:
                        # 有发送者的公共聊天信息,存日志
                        server_id, sender_id = get_server_and_user_id(server_sender_id)
                        instant_box.server_selected = server_id
                        instant_box.server_user_id = server_sender_id
                        instant_box.user_id = sender_id
                        user_do = UserDo.Reader()(instant_box.data_context, sender_id)
                        aofei_account_id = user_do.doc.aofei_account_id
                        if aofei_account_id:
                            game_logger_inst.start_log(aofei_account_id, GameLogOperation.chat)
                            game_logger_inst.push_log_param(GameLogFieldName.server, server_id)
                            game_logger_inst.push_log_param(GameLogFieldName.account_id, aofei_account_id)
                            game_logger_inst.push_log_param(GameLogFieldName.role_id, sender_id)
                            game_logger_inst.push_log_param(GameLogFieldName.role_name, user_do.name)
                            game_logger_inst.push_log_param(GameLogFieldName.role_level, user_do.level)
                            game_logger_inst.push_log_param(GameLogFieldName.content, json.dumps(chat_msg_data).decode('unicode-escape'))
                            game_logger_inst.push_log_param(GameLogFieldName.channel, chat_def.CHAT_CHANNEL_TYPE_PUBLIC)
                            game_logger_inst.push_log_param(GameLogFieldName.chat_time, instant_box.time_current)
                            game_logger_inst.end_log()
                except Exception as e:
                    logger.GetLog().error('write chat log err : %s, %s, %s' % (server_group_id, e, e.message))
            instant_box.data_context.save()
            instant_box.data_context.unlock()

    def AddP2PChatMsg(self, msg_content, msg_time, server_sender_id, server_receiver_id):
        logger.GetLog().debug('add p2p chat msg : %s, %s, %s' % (server_sender_id, server_receiver_id, msg_content))
        instant_box.time_current = msg_time
        data_context = DataContext()
        instant_box.data_context = data_context
        # 处理离线消息
        receiver_server_id, receiver_id = get_server_and_user_id(server_receiver_id)
        p2p_chat_do = P2PChattingMsgDo(data_context, receiver_id, receiver_server_id)
        if p2p_chat_do.is_msg_box_full(server_sender_id):
            data_context.unlock()
            return excp.ExceptionReceiverMsgFull.code, server_sender_id
        p2p_chat_do.add_msg(server_sender_id, msg_content, msg_time)
        # 处理聊天日志
        if server_sender_id:
            sender_server_id, sender_id = get_server_and_user_id(server_sender_id)
            instant_box.server_selected = sender_server_id
            # 有发送者的公共聊天信息,存日志
            user_do = UserDo.Reader()(data_context, sender_id, sender_server_id)
            aofei_account_id = user_do.doc.aofei_account_id
            if aofei_account_id:
                game_logger_inst.start_log(aofei_account_id, GameLogOperation.chat)
                game_logger_inst.push_log_param(GameLogFieldName.server, sender_server_id)
                game_logger_inst.push_log_param(GameLogFieldName.account_id, aofei_account_id)
                game_logger_inst.push_log_param(GameLogFieldName.role_id, sender_id)
                game_logger_inst.push_log_param(GameLogFieldName.role_name, user_do.name)
                game_logger_inst.push_log_param(GameLogFieldName.role_level, user_do.level)
                game_logger_inst.push_log_param(GameLogFieldName.content, json.dumps(msg_content).decode('unicode-escape'))
                game_logger_inst.push_log_param(GameLogFieldName.channel, chat_def.CHAT_CHANNEL_TYPE_P2P)
                game_logger_inst.push_log_param(GameLogFieldName.chat_time, instant_box.time_current)
                game_logger_inst.end_log()
        data_context.save()
        data_context.unlock()
        return excp.ExceptionSuccess.code, server_sender_id

    def LoadClanDataToSendMsg(self, chat_msg_data, msg_time, server_group_id, server_sender_id):
        logger.GetLog().debug('load clan data to send msg : %s, %s, %s' % (server_group_id, server_sender_id, chat_msg_data))
        instant_box.server_group = server_group_id
        instant_box.time_current = msg_time
        data_context = DataContext()
        instant_box.data_context = data_context
        sender_server_id, sender_id = get_server_and_user_id(server_sender_id)
        user_clan_view_do = UserClanDo.Reader()(data_context, sender_id, sender_server_id)
        if user_clan_view_do.doc.clan_id:
            member_id_list = ClanDo.Reader()(data_context, user_clan_view_do.doc.clan_id).doc.member_list.keys()
            # 将消息加入到消息列表
            ClanChattingMsgDo(data_context, user_clan_view_do.doc.clan_id).add_msg(chat_msg_data,
                                                                                   instant_box.time_current,
                                                                                   server_sender_id)
            if server_sender_id:
                # 有发送者的公共聊天信息,存日志
                user_do = UserDo.Reader()(data_context, sender_id, sender_server_id)
                aofei_account_id = user_do.doc.aofei_account_id
                if aofei_account_id:
                    game_logger_inst.start_log(aofei_account_id, GameLogOperation.chat)
                    game_logger_inst.push_log_param(GameLogFieldName.server, sender_server_id)
                    game_logger_inst.push_log_param(GameLogFieldName.account_id, aofei_account_id)
                    game_logger_inst.push_log_param(GameLogFieldName.role_id, sender_id)
                    game_logger_inst.push_log_param(GameLogFieldName.role_name, user_do.name)
                    game_logger_inst.push_log_param(GameLogFieldName.role_level, user_do.level)
                    game_logger_inst.push_log_param(GameLogFieldName.content, json.dumps(chat_msg_data).decode('unicode-escape'))
                    game_logger_inst.push_log_param(GameLogFieldName.channel, chat_def.CHAT_CHANNEL_TYPE_P2P)
                    game_logger_inst.push_log_param(GameLogFieldName.chat_time, instant_box.time_current)
                    game_logger_inst.end_log()

            data_context.save()
            data_context.unlock()  # 主动unlock
            return excp.ExceptionSuccess.code, chat_msg_data, server_group_id, server_sender_id, member_id_list
        return excp.ExceptionClanNotFound.code, server_sender_id

    def HandleSendTeamMsg(self, chat_msg_data, msg_time, server_group_id, server_sender_id):
        sender_server_id, sender_id = get_server_and_user_id(server_sender_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = sender_server_id
        instant_box.time_current = msg_time
        instant_box.data_context = DataContext()
        user_team_do = UserTeamDo.Reader()(instant_box.data_context, sender_id)
        if not user_team_do.has_team():
            return excp.ExceptionHasNoTeam.code, server_group_id, server_sender_id
        team_do = TeamDo.Reader()(instant_box.data_context, user_team_do.doc.team_id)
        if team_do.is_new:
            return excp.ExceptionHasNoTeam.code, server_group_id, server_sender_id
        # 聊天日志
        user_do = UserDo.Reader()(instant_box.data_context, sender_id, sender_server_id)
        aofei_account_id = user_do.doc.aofei_account_id
        if aofei_account_id:
            game_logger_inst.start_log(aofei_account_id, GameLogOperation.chat)
            game_logger_inst.push_log_param(GameLogFieldName.server, sender_server_id)
            game_logger_inst.push_log_param(GameLogFieldName.account_id, aofei_account_id)
            game_logger_inst.push_log_param(GameLogFieldName.role_id, sender_id)
            game_logger_inst.push_log_param(GameLogFieldName.role_name, user_do.name)
            game_logger_inst.push_log_param(GameLogFieldName.role_level, user_do.level)
            game_logger_inst.push_log_param(GameLogFieldName.content, json.dumps(chat_msg_data).decode('unicode-escape'))
            game_logger_inst.push_log_param(GameLogFieldName.channel, chat_def.CHAT_CHANNEL_TYPE_TEAM)
            game_logger_inst.push_log_param(GameLogFieldName.chat_time, instant_box.time_current)
            game_logger_inst.end_log()

        return excp.ExceptionSuccess.code, server_group_id, server_sender_id, chat_msg_data, team_do.doc.member_id_list

    def LoadOfflineMsgToSend(self, server_group_id, server_user_id, last_public_time, last_clan_time):
        logger.GetLog().debug('load offline msg : %s, %s, %s, %s' % (server_group_id, server_user_id, last_public_time, last_clan_time))
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        instant_box.data_context = DataContext()
        return server_user_id, self.get_public_msg_list(last_public_time), self.get_clan_msg_list(user_id, last_clan_time), self.get_p2p_msg_list(user_id)

    def ConfirmGetOfflineMsg(self, server_user_id):
        logger.GetLog().debug('chat db handle confirm offline msg : %s' % server_user_id)
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        p2p_chat_do = P2PChattingMsgDo(data_context, user_id)
        p2p_chat_do.clear_msg_dict()
        data_context.save()
        data_context.unlock()  # 主动unlock
        return server_user_id

    def LoadClanDataToSendNotice(self, notice_msg_data, msg_time, clan_id, server_group_id):
        instant_box.time_current = msg_time
        data_context = DataContext()
        member_id_list = ClanDo.Reader()(data_context, clan_id).doc.member_list.keys()
        return notice_msg_data, server_group_id, member_id_list

    def UpdateServerOnlineDBData(self, server_group_id, online_num):
        instant_box.server_group = server_group_id
        instant_box.time_current = time.time()
        instant_box.data_context = DataContext()
        try:
            online_list_do = LogServerOnlineDo(instant_box.data_context)
            online_list_do.set_online_num(server_group_id, online_num)
            instant_box.data_context.save()
        except Exception as e:
            logger.GetLog().error('update server online db data fail : %s, %s, %s' % (server_group_id, online_num, e))
        finally:
            instant_box.data_context.unlock()

    def WriteUserOfflineLog(self, server_user_id, logout_time, online_time):
        try:
            server_id, user_id = get_server_and_user_id(server_user_id)
            instant_box.server_selected = server_id
            instant_box.time_current = logout_time
            instant_box.data_context = DataContext()
            user_do = UserDo.Reader()(instant_box.data_context, user_id)
            character_log_info_do = CharacterLogInfoDo(instant_box.data_context, user_id, server_id)
            character_log_info_do.update_info(online_time, logout_time)
            user_session_do = UserSessionDo(instant_box.data_context, user_id)

            game_logger_inst.start_log(user_do.doc.aofei_account_id, GameLogOperation.logout_role)
            game_logger_inst.push_log_param(GameLogFieldName.server, int(server_id))
            game_logger_inst.push_log_param(GameLogFieldName.account_id, user_do.doc.aofei_account_id)
            game_logger_inst.push_log_param(GameLogFieldName.role_id, user_id)
            game_logger_inst.push_log_param(GameLogFieldName.role_name, user_do.name)
            game_logger_inst.push_log_param(GameLogFieldName.create_time, int(user_do.doc.time_created))
            game_logger_inst.push_log_param(GameLogFieldName.role_level, user_do.level)
            game_logger_inst.push_log_param(GameLogFieldName.role_job, 0)
            game_logger_inst.push_log_param(GameLogFieldName.exp, user_do.doc.exp)
            game_logger_inst.push_log_param(GameLogFieldName.logout_time, logout_time)
            game_logger_inst.push_log_param(GameLogFieldName.online_time, online_time)
            game_logger_inst.push_log_param(GameLogFieldName.scene, 'Unknown')
            game_logger_inst.push_log_param(GameLogFieldName.last_operation, user_session_do.doc.last_operation)
            game_logger_inst.push_log_param(GameLogFieldName.total_pay, 0)
            game_logger_inst.push_log_param(GameLogFieldName.vip_level, 0)
            game_logger_inst.push_log_param(GameLogFieldName.total_time, character_log_info_do.doc.total_online_time)
            game_logger_inst.end_log()
            instant_box.data_context.save()
        except Exception as e:
            logger.GetLog().error('write user offline log fail : %s, %s, %s, %s' % (server_user_id, logout_time, online_time, e))
        finally:
            if instant_box.data_context:
                instant_box.data_context.unlock()

    def WriteOnlineNumLog(self, user_num_dict):
        instant_box.time_current = time.time()
        instant_box.data_context = DataContext()
        for server_group_id, num in user_num_dict.iteritems():
            try:
                for server_id in get_server_list_in_group(server_group_id):
                    instant_box.server_selected = server_id
                    game_logger_inst.start_log(None, GameLogOperation.online_role_num)
                    game_logger_inst.push_log_param(GameLogFieldName.app_channel, '1000')
                    game_logger_inst.push_log_param(GameLogFieldName.platform_tag, 'aofei')
                    game_logger_inst.push_log_param(GameLogFieldName.group_id, 2)
                    game_logger_inst.push_log_param(GameLogFieldName.channel_id, 1000)
                    game_logger_inst.push_log_param(GameLogFieldName.server, int(server_id))
                    game_logger_inst.push_log_param(GameLogFieldName.ip_online_num, '0')
                    game_logger_inst.push_log_param(GameLogFieldName.online, num)
                    game_logger_inst.push_log_param(GameLogFieldName.online_time, int(instant_box.time_current))
                    game_logger_inst.push_log_param(GameLogFieldName.os_name, 'CentOS')
                    game_logger_inst.end_log()
            except Exception as e:
                logger.GetLog().error('write online num log fail : %s, %s' % (server_id, num))
        instant_box.data_context.save()
        instant_box.data_context.unlock()

    def get_public_msg_list(self, flag_time):
        return PublicChattingMsgDo.Reader()(instant_box.data_context).get_new_msg_list(flag_time)

    def get_clan_msg_list(self, user_id, flag_time):
        user_clan_view_do = UserClanDo.Reader()(instant_box.data_context, user_id)
        if not user_clan_view_do.is_new and user_clan_view_do.doc.clan_id:
            return ClanChattingMsgDo.Reader()(instant_box.data_context, user_clan_view_do.doc.clan_id).get_new_msg_list(flag_time)
        return []

    def get_p2p_msg_list(self, user_id):
        msg_dict = P2PChattingMsgDo.Reader()(instant_box.data_context, user_id).get_msg_dict()
        ret_list = []
        if msg_dict:
            for key, value in msg_dict.iteritems():
                if value and value.msg_list:
                    ret_item = P2POfflineMsg()
                    ret_item.server_sender_id = key
                    ret_item.msg_list = value.msg_list
                    ret_list.append(ret_item.dump())
        return ret_list
