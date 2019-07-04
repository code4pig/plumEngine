# -*- coding: utf8 -*-

import msgpack

import game

import script.chat.chatting_def as chat_def
import script.common.config.topoconfig as ModTopo
import script.common.exception_def as excp
import script.common.log as logger
import script.common.protocol_def as proto_def
from script.common.nodebase.appbase import CAppBase
from script.common.protocol_def import CGLoginServerRequest, CGSendChatMsgRequest, CGGetChatOfflineMsgRequest, \
    CGGameServerNotice, CGGetOnlineNumRequest, CGConfirmChatOfflineMsgRequest, CGGameServerRegisterRequest, \
    CGGetTeamInfoRequest
from script.common.protocol_def import CGLoginServerResponse, CGGameServerRegisterResponse


class CTestClient(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.chatTimes = 0

    def get_node_type(self):
        return ModTopo.NODE_TYPE.CLIENT

    def OnStartUp(self, confFile):
        CAppBase.OnStartUp(self, confFile)
        self.start_net_client()

    def OnUpdate(self):
        pass

    def OnShutDown(self):
        CAppBase.OnShutDown(self)

    def SendMsg(self, msg, proto):
        game.SendMsgToServer(ModTopo.NODE_TYPE.GATEWAY, proto, msgpack.packb(msg))

    def SendChatMsg(self, msg):
        self.SendMsg(msg, ModTopo.PROTO_TYPE.CHAT)
        
    def SendTeamMsg(self, msg):
        self.SendMsg(msg, ModTopo.PROTO_TYPE.TEAM)
        
    def SendFightMsg(self, msg):
        self.SendMsg(msg, ModTopo.PROTO_TYPE.FIGHT)

    def SendCommonMsg(self, msg):
        self.SendMsg(msg, ModTopo.PROTO_TYPE.COMMON)

    def OnConnectToServer(self, t_cli, connid, ip):
        CAppBase.OnConnectToServer(self, t_cli, connid, ip)
        if self.get_test_param('client_type') == 2:
            self.TestGameServerLogin()
        else:
            self.TestUserLogin()
        # self.TestGetOfflineMsg()
        # self.TestChat()

    def TestGameServerLogin(self):
        req = CGGameServerRegisterRequest()
        req.rk_zone = 'test_game_server'
        import hashlib
        md5 = hashlib.md5()
        md5.update(req.rk_zone + proto_def.game_notice_check_md5_ticket)
        req.sign = md5.hexdigest()
        req_dump = req.dump()
        logger.GetLog().debug('TestGameServerLogin req: %s' % req_dump)
        self.SendCommonMsg(req_dump)

    def TestUserLogin(self):
        req = CGLoginServerRequest()
        req.user_id = self.get_test_param('server_user_id')
        req.server_id = self.get_test_param('server_id')
        import hashlib
        md5 = hashlib.md5()
        md5.update(req.user_id + req.server_id + proto_def.login_check_md5_ticket)
        req.sign = md5.hexdigest()
        req_dump = req.dump()
        logger.GetLog().debug('TestUserLogin req: %s' % req_dump)
        self.SendCommonMsg(req_dump)

    def TestGetOfflineMsg(self):
        req = CGGetChatOfflineMsgRequest()
        req_dump = req.dump()
        logger.GetLog().debug('TestGetOfflineMsg req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestPublicChat(self, args=None):
        self.chatTimes += 1
        req = CGSendChatMsgRequest()
        req.channel_type = chat_def.CHAT_CHANNEL_TYPE_PUBLIC
        # req.data = 'Public Chat --- i am user : %s, times %d' % (self.get_test_param('user_id'), self.chatTimes)
        req.data = {"A": "", "B": "", "C": 0, "D": "", "E": "", "F": "Public", "G": 0, "H": "",
                    "I": "实时框架协议定义PROTO_TYPE.COMMON", "J": 0, "K": None}
        req_dump = req.dump()
        logger.GetLog().debug('TestPublicChat req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestClanChat(self, args=None):
        self.chatTimes += 1
        req = CGSendChatMsgRequest()
        req.channel_type = chat_def.CHAT_CHANNEL_TYPE_CLAN
        req.data = 'Clan Chat --- i am user : %s, times %d' % (self.get_test_param('user_id'), self.chatTimes)
        req_dump = req.dump()
        logger.GetLog().debug('TestClanChat req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestP2PChat(self, args=None):
        self.chatTimes += 1
        req = CGSendChatMsgRequest()
        req.channel_type = chat_def.CHAT_CHANNEL_TYPE_P2P
        req.receiver_id = self.get_test_param('p2p_receiver')
        req.data = 'P2P Chat --- i am user : %s, times %d' % (self.get_test_param('user_id'), self.chatTimes)
        req_dump = req.dump()
        logger.GetLog().debug('TestP2PChat req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestConfirmOfflineMsg(self, args=None):
        req = CGConfirmChatOfflineMsgRequest()
        req_dump = req.dump()
        logger.GetLog().debug('TestGetOnlineNum req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestPublicNotice(self, args=None):
        req = CGGameServerNotice()
        req.server_id = self.get_test_param('server_id')
        req.channel_type = chat_def.CHAT_CHANNEL_TYPE_NOTICE
        req.data = 'Public Notice --- From Test Client : %s' % self.config.get('AppId', None)
        # 计算验证key
        req_dump = req.dump()
        logger.GetLog().debug('TestPublicNotice req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestClanNotice(self, args=None):
        req = CGGameServerNotice()
        req.server_id = self.get_test_param('server_id')
        req.channel_type = chat_def.CHAT_CHANNEL_TYPE_CLAN
        req.receiver_id = self.get_test_param('notice_clan_id')
        req.data = 'Clan Notice --- From Test Client : %s' % self.config.get('AppId', None)
        # 计算验证key
        req_dump = req.dump()
        logger.GetLog().debug('TestClanNotice req : %s' % req_dump)
        self.SendChatMsg(req_dump)

    def TestGetOnlineNum(self, args=None):
        req = CGGetOnlineNumRequest()
        req_dump = req.dump()
        logger.GetLog().debug('TestGetOnlineNum req : %s' % req_dump)
        self.SendCommonMsg(req_dump)

    def TestGetTeamInfo(self, args=None):
        req = CGGetTeamInfoRequest()
        req_dump = req.dump()
        logger.GetLog().debug('TestGetTeamInfo req : %s' % req_dump)
        self.SendTeamMsg(req_dump)

    def OnLoginResponse(self, res):
        if res.return_code == excp.ExceptionSuccess.code:
            test_proto_list = self.get_test_param('test_proto')
            if 1 in test_proto_list:  # 取离线数据
                self.TestGetOfflineMsg()
            if 2 in test_proto_list:  # 公共聊天
                self.RegTick(self.TestPublicChat, None, self.get_test_param('send_interval'),
                             self.get_test_param('send_count'))
            if 3 in test_proto_list:  # 公会聊天
                self.RegTick(self.TestClanChat, None, self.get_test_param('send_interval'),
                             self.get_test_param('send_count'))
            if 4 in test_proto_list:  # 私聊
                self.RegTick(self.TestP2PChat, None, self.get_test_param('send_interval'),
                             self.get_test_param('send_count'))
            if 5 in test_proto_list:  # 公共推送公告
                self.TestPublicNotice()
            if 6 in test_proto_list:  # 公会推送公告
                self.TestClanNotice()
            if 7 in test_proto_list:  # 获取在线人数
                self.RegTick(self.TestGetOnlineNum, None, self.get_test_param('req_online_interval'))
            if 8 in test_proto_list:  # 确认离线消息获取
                self.TestConfirmOfflineMsg()
            if 9 in test_proto_list:  # 请求自己队伍信息
                self.TestGetTeamInfo()
        else:
            logger.GetLog().debug('login fail : %s, %s' % (self.get_test_param('user_id'), res.return_code))

    def OnConnectToServerFailed(self, t_cli, errmsg):
        CAppBase.OnConnectToServerFailed(self, t_cli, errmsg)

    def OnServerDisconnect(self, t_cli):
        CAppBase.OnServerDisconnect(self, t_cli)

    def OnServerRpcMsg(self, t_cli, connid, proto, msgstr):
        if t_cli == ModTopo.NODE_TYPE.GATEWAY:
            #客户端不支持rpc通信，需要自己实现此方法
            logger.GetLog().debug('OnRpcMsg connect_id : %s, proto : %s, msg : %s' % (connid, proto, msgstr))
            msg = msgpack.unpackb(msgstr)
            if msg[proto_def.field_name_cmd] == proto_def.cg_login_server:
                self.OnLoginResponse(CGLoginServerResponse.new_from_data(msg))
            elif msg[proto_def.field_name_cmd] == proto_def.cg_game_server_register:
                self.OnLoginResponse(CGGameServerRegisterResponse.new_from_data(msg))
        CAppBase.OnServerRpcMsg(self, t_cli, connid, proto, msgstr)

    def get_test_param(self, key):
        return self.config['for_test'].get(key, None)
