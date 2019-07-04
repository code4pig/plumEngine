# -*- coding: utf-8 -*-
"""
@author: bbz
"""
from script.common.config.topoconfig import NODE_TYPE

conf = {
    "AppId": 0,
    "FrameRate": 30,
    "ServerIds": {
        NODE_TYPE.GATEWAY: 0,
    },
    "LogLevel": 1,      # 默认日志级别, DEBUG = 1, INFO = 2, WARNING = 3, ERROR = 4
    # for test
    'for_test': {
        'user_id': '10001',
        'server_id': '1001',
        'send_count': 1,
        'send_interval': 1000,
        'p2p_receiver': '10002',
        'notice_clan_id': 'dev_test-1001-000001',
        'req_online_interval': 10000,
        'client_type': 1,   # 1 - user, 2 - game server
        # 1 - 请求离线消息；2 - 发送公共聊天；3 - 发送公会聊天；4 - 发送私聊； 5 - 公共公告，
        # 6 - 公会公告, 7 - 获取在线人数, 8 - 获取离线消息确认, 9 - 请求自己的队伍信息
        'test_proto': [2]
    }
}
