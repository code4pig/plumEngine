# -*- coding:utf-8 -*-

import game
import msgpack
import hashlib
import script.common.config.topoconfig as ModTopo
import script.gateway.object_factory as ModObjFac
import script.common.log as logger
import script.common.exception_def as excp
import script.common.protocol_def as proto_def
from script.common.protocol_def import CGLoginServerResponse, CGGetOnlineNumResponse, \
    CGGameServerRegisterResponse
from script.common.config.config import conf as common_config
from script.common.game_define.global_def import get_server_id, get_server_group_id


class GatewayMsgManager(object):
    def __init__(self):
        self.server_online_num_dict = {}  # 按服区分的在线玩家数 server group id -> online user

    def handle_user_login_server(self, connect_id, msg_obj):
        logger.GetLog().info('user login server : %s, %s, %s, %s' % (connect_id, msg_obj.server_user_id, msg_obj.server_id, msg_obj.sign))
        res_obj = CGLoginServerResponse()
        res_obj.return_code = excp.ExceptionSuccess.code
        gateway_app = ModObjFac.CreateApp()
        # 校验登录参数
        if not self.check_login_sign(msg_obj.server_user_id, msg_obj.server_id, msg_obj.sign):
            # 校验失败
            res_obj.return_code = excp.ExceptionCheckLoginFailed.code
        else:
            # 校验成功
            server_group_id = get_server_group_id(msg_obj.server_id)
            # TODO: 先将现有连接主动断掉?
            # 移除旧连接
            old_connect_id = gateway_app.get_conn_id_by_char_id(msg_obj.server_user_id)
            if old_connect_id != -1:
                gateway_app.del_connect(server_group_id, msg_obj.server_user_id, old_connect_id)

            # 增加连接信息
            gateway_app.add_connect(server_group_id, msg_obj.server_user_id, connect_id)
            # 同步玩家在线状态到各个chat server,更新在线人数
            gateway_app.get_gateway_2_chat_proxy_rpc().OnUserOnlineStatusUpdate(server_group_id, msg_obj.server_user_id, connect_id, True, gateway_app.get_client_connect_ip(connect_id))
            # 推送玩家在线状态给team server
            gateway_app.get_gateway_2_team_proxy_rpc().OnUserOnlineStatusUpdate(server_group_id, msg_obj.server_user_id, True)
            # # 推送玩家在线状态给scene server
            # gateway_app.get_gateway_2_scene_proxy_rpc().OnUserOnlineStatusUpdate(server_group_id, msg_obj.server_user_id, True)
        res_msg = res_obj.dump()
        logger.GetLog().debug('user login server res : %s' % res_msg)
        # 返回信息给客户端
        gateway_app.send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.COMMON, msgpack.packb(res_msg))

    def handle_game_server_register(self, connect_id, msg_obj):
        logger.GetLog().info('game server register: %s, %s, %s' % (connect_id, msg_obj.rk_zone, msg_obj.sign))
        res_obj = CGGameServerRegisterResponse()
        res_obj.return_code = excp.ExceptionSuccess.code
        if not self.check_game_server_register(msg_obj.rk_zone, msg_obj.sign):
            # 校验失败
            res_obj.return_code = excp.ExceptionCheckLoginFailed.code
        else:
            ModObjFac.CreateApp().add_game_server_connect(connect_id, msg_obj.rk_zone)
        res_msg = res_obj.dump()
        logger.GetLog().debug('game server login server res : %s' % res_msg)
        # 返回信息给游戏服
        ModObjFac.CreateApp().send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.COMMON, msgpack.packb(res_msg))

    def handle_user_logout(self, connect_id):
        connect_info = ModObjFac.CreateApp().get_connect_info(connect_id)
        logger.GetLog().debug('client disconnect: connect id = %s, has info = %s' % (connect_id, connect_info is not None))
        if connect_info:
            if connect_info.has_bind_user():
                logger.GetLog().debug('user logout : %s, %s, %s' % (connect_id, connect_info.server_group_id, connect_info.server_user_id))
                # 推送玩家下线消息给chat server, 更新在线人数
                ModObjFac.CreateApp().get_gateway_2_chat_proxy_rpc().OnUserOnlineStatusUpdate(connect_info.server_group_id, connect_info.server_user_id, connect_id, False)
                # 推送玩家下线消息给team server
                ModObjFac.CreateApp().get_gateway_2_team_proxy_rpc().OnUserOnlineStatusUpdate(connect_info.server_group_id, connect_info.server_user_id, False)
                # 推送给战斗服battle server
                ModObjFac.CreateApp().get_gateway_2_fight_proxy_rpc().OnUserOffline(connect_info.server_group_id, connect_info.server_user_id)
                # 推送玩家在线状态给scene server
                ModObjFac.CreateApp().get_gateway_2_scene_proxy_rpc().OnUserLogout(connect_info.server_group_id, connect_info.server_user_id)

            ModObjFac.CreateApp().del_connect(connect_info.server_group_id, connect_info.server_user_id, connect_id)

    def handle_get_online_num(self, connect_id):
        connect_info = ModObjFac.CreateApp().get_connect_info(connect_id)
        if connect_info and connect_info.server_group_id:
            res_obj = CGGetOnlineNumResponse()
            res_obj.online_num = self.get_server_online_num(connect_info.server_group_id)
            logger.GetLog().debug('server %s online num %s' % (connect_info.server_group_id, res_obj.online_num))
            # 返回信息给客户端
            ModObjFac.CreateApp().send_msg_to_client(connect_id, ModTopo.PROTO_TYPE.COMMON, msgpack.packb(res_obj.dump()))

    def update_server_online_num(self, server_group_id, num):
        logger.GetLog().debug(' server group online num update : server group id = %s, online num = %s' % (server_group_id, num))
        self.server_online_num_dict[server_group_id] = num

    def get_server_online_num(self, server_group_id):
        return self.server_online_num_dict.get(server_group_id, 0)

    def check_login_sign(self, server_user_id, server_id, sign):
        if server_user_id and server_id and sign and server_id == get_server_id(server_user_id):
            md5 = hashlib.md5()
            md5.update(server_user_id + server_id + proto_def.login_check_md5_ticket)
            admin_pwd = md5.hexdigest()
            logger.GetLog().debug('server_user_id: %s, server_id: %s, sign: %s, cal_sign: %s' % (server_user_id, server_id, sign, admin_pwd))
            return admin_pwd == sign
        return False

    def check_game_server_register(self, rk_zone, sign):
        if rk_zone != common_config.zone:
            logger.GetLog().warn('game rk_zone is unexpected : %s' % rk_zone)
            return False
        else:
            md5 = hashlib.md5()
            md5.update(rk_zone + proto_def.game_notice_check_md5_ticket)
            server_sign = md5.hexdigest()
            return server_sign == sign
