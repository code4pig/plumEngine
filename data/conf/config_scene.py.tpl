# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-09 11:26

from __future__ import unicode_literals
from script.common.config.topoconfig import NODE_TYPE

conf = {
    'FrameRate': 30,
    'LogLevel': 1,      # 默认日志级别, DEBUG = 1, INFO = 2, WARNING = 3, ERROR = 4

    'MonitorAddr': ('127.0.0.1', 30000),      # monitor 地址 & 端口
    'ServerNodeList': [NODE_TYPE.SCENE_PROXY, NODE_TYPE.DB_PROXY],       # 需要连接的服务器类型列表
}
