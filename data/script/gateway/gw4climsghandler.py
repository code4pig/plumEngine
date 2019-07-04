# -*- coding: utf-8 -*-
"""
@author: bbz
"""

import msgpack
import script.common.protocol_def as proto_def
import script.gateway.object_factory as ModObjFac
import script.common.config.topoconfig as ModTopo
import script.common.log as logger
import script.common.exception_def as excp
from script.common.protocol_def import CGLoginServerRequest, CGSendChatMsgResponse, CGGameServerRegisterRequest, CGCommonErrorResponse


class CGw4CliMsgHandler(object):
    def __init__(self):
        pass

    def OnClientCommonMsg(self, connect_id, str_msg):
        msg = msgpack.unpackb(str_msg)
        logger.GetLog().debug('gateway on client common msg : connect id = %s, msg = %s' % (connect_id, msg))
        cmd = msg.get(proto_def.field_name_cmd, None)
        if cmd is None:
            logger.GetLog().warn('gateway on client common msg unexpected cmd : %s' % cmd)
        else:
            if cmd == proto_def.cg_login_server:
                # 登录服务器
                msg_obj = CGLoginServerRequest.new_from_data(msg)
                ModObjFac.CreateApp().get_msg_manager().handle_user_login_server(connect_id, msg_obj)
            elif cmd == proto_def.cg_get_online_num:
                ModObjFac.CreateApp().get_msg_manager().handle_get_online_num(connect_id)
            elif cmd == proto_def.cg_game_server_register:
                # 游戏服登录
                msg_obj = CGGameServerRegisterRequest.new_from_data(msg)
                ModObjFac.CreateApp().get_msg_manager().handle_game_server_register(connect_id, msg_obj)
            else:
                logger.GetLog().warn('gateway on client common msg unexpected cmd : %s' % cmd)

    def OnClientChatMsg(self, connect_id, str_msg):
        logger.GetLog().debug('gateway on client chat msg : connect id = %s' % (connect_id, ))
        connect_info = ModObjFac.CreateApp().get_connect_info(connect_id)
        if connect_info and connect_info.has_bind_user():
            # 直接转发,gateway 不做逻辑处理,交给具体业务服处理
            ModObjFac.CreateApp().get_gateway_2_chat_proxy_rpc().OnChatMsg(connect_info.server_group_id, connect_info.server_user_id, str_msg)
        elif ModObjFac.CreateApp().is_game_server_connect(connect_id):
            # 游戏服发来的直接转发,gateway 不做逻辑处理,交给具体业务服处理
            ModObjFac.CreateApp().get_gateway_2_chat_proxy_rpc().OnGameNotice(str_msg)
        else:
            # 还未登录,返回失败
            logger.GetLog().warn('connect send msg but has not bind user : %s' % connect_id)
            ret_msg = CGSendChatMsgResponse()
            ret_msg.return_code = excp.ExceptionNeedLogin.code
            ModObjFac.CreateApp().send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.CHAT, msgpack.packb(ret_msg.dump()))

    def OnClientTeamMsg(self, connect_id, str_msg):
        logger.GetLog().debug('gateway on client team msg : connect id = %s' % (connect_id,))
        connect_info = ModObjFac.CreateApp().get_connect_info(connect_id)
        if connect_info and connect_info.has_bind_user():
            # 直接转发,gateway 不做逻辑处理,交给具体业务服处理
            ModObjFac.CreateApp().get_gateway_2_team_proxy_rpc().OnTeamMsg(connect_info.server_group_id, connect_info.server_user_id, str_msg)
        else:
            # 还未登录,返回失败
            logger.GetLog().warn('connect send msg but has not bind user : %s' % connect_id)
            ret_msg = CGCommonErrorResponse()
            ret_msg.return_code = excp.ExceptionNeedLogin.code
            ModObjFac.CreateApp().send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.COMMON, msgpack.packb(ret_msg.dump()))

    def OnClientBattleMsg(self, connect_id, str_msg):
        logger.GetLog().debug('gateway on client battle msg : connect id = %s' % (connect_id,))
        connect_info = ModObjFac.CreateApp().get_connect_info(connect_id)
        if connect_info and connect_info.has_bind_user():
            # 直接转发,gateway 不做逻辑处理,交给具体业务服处理
            ModObjFac.CreateApp().get_gateway_2_fight_proxy_rpc().OnFightMsg(connect_info.server_group_id, connect_info.server_user_id, str_msg)
        else:
            # 还未登录,返回失败
            logger.GetLog().warn('connect send msg but has not bind user : %s' % connect_id)
            ret_msg = CGCommonErrorResponse()
            ret_msg.return_code = excp.ExceptionNeedLogin.code
            ModObjFac.CreateApp().send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.COMMON, msgpack.packb(ret_msg.dump()))

    def OnClientSceneMsg(self, connect_id, str_msg):
        logger.GetLog().debug('gateway on client scene msg : connect id = %s' % (connect_id, ))
        connect_info = ModObjFac.CreateApp().get_connect_info(connect_id)
        if connect_info and connect_info.has_bind_user():
            # 直接转发,gateway 不做逻辑处理,交给具体业务服处理
            ModObjFac.CreateApp().get_gateway_2_scene_proxy_rpc().OnSceneMsg(connect_info.server_group_id, connect_info.server_user_id, str_msg)
        else:
            # 还未登录,返回失败
            logger.GetLog().warn('connect send msg but has not bind user : %s' % connect_id)
            ret_msg = CGCommonErrorResponse()
            ret_msg.return_code = excp.ExceptionNeedLogin.code
            ModObjFac.CreateApp().send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.COMMON, msgpack.packb(ret_msg.dump()))