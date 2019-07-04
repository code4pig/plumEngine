# -*- coding: utf-8 -*-
''' 
@author: bbz
'''

'''
client
gateway
chatproxy
chat
battleproxy
battle
sceneproxy
scene
dbproxy
monitor
...
'''

import script.common.utils.myconst as ModConst

PROTO_TYPE = ModConst.Const()   # 从1开始配置，1以前禁止使用
PROTO_TYPE.HEARTBEAT = 0        # 保留：C++层使用
PROTO_TYPE.COMMON = 1
PROTO_TYPE.CHAT = 2
PROTO_TYPE.FIGHT = 3
PROTO_TYPE.TEAM = 4
PROTO_TYPE.SCENE = 5
PROTO_TYPE.DB = 100              # db -> monitor

NODE_TYPE = ModConst.Const()
NODE_TYPE.CLIENT = 1
NODE_TYPE.MONITOR = 100
NODE_TYPE.GATEWAY = 200
NODE_TYPE.DB_PROXY = 300
NODE_TYPE.CHAT_PROXY = 400
NODE_TYPE.CHAT = 500
NODE_TYPE.TEAM_PROXY = 600
NODE_TYPE.TEAM = 700
NODE_TYPE.FIGHT_PROXY = 800
NODE_TYPE.FIGHT = 900
NODE_TYPE.SCENE_PROXY = 1000
NODE_TYPE.SCENE = 1100

# 服务类型(节点作为服务器的服务类型)
SERVICE_TYPE = ModConst.Const()
SERVICE_TYPE.FOR_NODE = 1           # 对其他节点的服务
SERVICE_TYPE.FOR_CLIENT = 2         # 对客户端(非节点)的服务

