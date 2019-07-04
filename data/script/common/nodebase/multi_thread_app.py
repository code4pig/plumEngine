# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-10-22 15:07

import script.dbproxy.db_define as ModThreadConf
import script.dbproxy.thread.threadpool as ModThreadPool
import script.common.log as logger
from script.common.nodebase.appbase import CAppBase


class CMultiThreadApp(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.thread_pool_dict = {}    # thread_type -> thread_pool

    def get_thread_pool(self, thread_type):
        return self.thread_pool_dict[thread_type]

    def get_thread_config_count(self, thread_type):
        thread_config = self.get_config('ThreadCount')
        if thread_config and thread_type in thread_config:
            return thread_config[thread_type]
        logger.GetLog().warn('thread type %s has no config in config' % thread_type)
        return 1

    def init_thread_pool(self):
        for thread_type in ModThreadConf.DBS.THREAD_TYPE.GetValueList():
            self.thread_pool_dict[thread_type] = ModThreadPool.CThreadPool(thread_type, self.get_thread_config_count(thread_type))

    def OnStartUp(self, config_file):
        # 移除json的钩子，因为 ujson不支持separators关键字,会在couchbase sdk中调用时报错
        import script.common.initscript as init_script
        init_script.HOOK_MODULES.pop('json', None)
        import couchbase._bootstrap
        reload(couchbase._bootstrap)

        CAppBase.OnStartUp(self, config_file)
        self.init_thread_pool()

        # # 初始化战斗常量配置数据
        # masters_global.init_battle_config_const_value()