# -*- coding: utf-8 -*-
'''
@author: bbz
'''
import script.common.utils.myconst as myconst

DBS = myconst.Const()
DBS.THREAD_TYPE = myconst.Enum()
DBS.THREAD_TYPE.DEFAULT  # 默认线程类型。
DBS.THREAD_TYPE.HARD  # 提供给计算繁重的工作。 主要是不影响默认线程池玩家数据存取。


# 也可以为特定事务定义专有的channel，同样channel会放在同样的线程执行
DBS.RPC_CHANNEL = myconst.Enum()
DBS.RPC_CHANNEL.LOW_LEVEL  # log等优先级不高的
DBS.RPC_CHANNEL.MID_LEVEL  # 排行榜等
DBS.RPC_CHANNEL.HI_LEVEL  # 逻辑事务。比如人际，离线事件