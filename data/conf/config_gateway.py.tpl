# -*- coding: utf-8 -*-
"""
@author: bbz
"""

from __future__ import unicode_literals
from script.common.config.topoconfig import SERVICE_TYPE

conf = {
    'FrameRate': 30,
    'HeartBeat': 1000,          # 心跳间隔
    'HeartBeatCheck': 10000,    # 心跳检查间隔
    'LogLevel': 1,      # 默认日志级别, DEBUG = 1, INFO = 2, WARNING = 3, ERROR = 4

    'MonitorAddr': ('127.0.0.1', 30000),      # monitor 地址 & 端口
    'Services': {
        # service type : （'监听地址', '对外地址', '监听端口', '客户端连接每秒消息限制条数(最大65535)', '消息条数超过限制的次数(最大127)'）
        SERVICE_TYPE.FOR_NODE: ('0.0.0.0', '127.0.0.1', 32000, 0, 0),       # 对 Node 开放的服务
        SERVICE_TYPE.FOR_CLIENT: ('0.0.0.0', '127.0.0.1', 31000, 50, 5),    # 对 Client 开放的服务
    },
}
