# -*- coding: utf8 -*-
import cPickle

import game

import script.common.config.topoconfig as ModTopo
import script.common.gm_define as gm_def
import script.common.log as logger
import script.common.utils.utils as utils
import script.dbproxy.db_define as ModConf
import script.dbproxy.thread.threadpool as ModTPool
from script.common.nodebase.appbase import CAppBase
from script.dbproxy.ct2dbrpchandler import Ct2DbRpcHandler
from script.dbproxy.do import masters_global
from script.dbproxy.ft2dbrpchandler import Ft2DbRpcHandler
from script.dbproxy.rpc.query_rpc_mgr import CQueryRpcMgr
from script.dbproxy.scene2dbrpchandler import Scene2DbRpcHandler
from script.dbproxy.tm2dbrpchandler import Tm2DbRpcHandler


class CDbProxy(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.ctrpcHandler = Ct2DbRpcHandler()
        self.tmrpcHandler = Tm2DbRpcHandler()
        self.ftrpcHandler = Ft2DbRpcHandler()
        self.scene_rpc_handler = Scene2DbRpcHandler()

        self.threadPool = {}  # threadType -> threadpool
        self.queryrpcMgr = CQueryRpcMgr()

    # child class must override functions >>>
    def get_node_type(self):
        return ModTopo.NODE_TYPE.DB_PROXY

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # db的服务器节点: monitor
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type in self.connect_server_dict and self.connect_server_dict[server_node_type]:
            if server_node_type == ModTopo.NODE_TYPE.MONITOR:
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
            else:
                logger.GetLog().error('send msg to an unsupported server node : %s, %s, %s' % (client_type, msg_str, args))
        else:
            logger.GetLog().error('send msg to server node %s but there is no one in connect_server_dict' % server_node_type)

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # db的客户端节点: 所有逻辑节点, 可能有
        if client_node_type in (ModTopo.NODE_TYPE.CHAT, ModTopo.NODE_TYPE.TEAM, ModTopo.NODE_TYPE.FIGHT, ModTopo.NODE_TYPE.SCENE) and args:
            if client_node_type == ModTopo.NODE_TYPE.CHAT:
                proto_type = ModTopo.PROTO_TYPE.CHAT
            elif client_node_type == ModTopo.NODE_TYPE.TEAM:
                proto_type = ModTopo.PROTO_TYPE.TEAM
            elif client_node_type == ModTopo.NODE_TYPE.FIGHT:
                proto_type = ModTopo.PROTO_TYPE.FIGHT
            elif client_node_type == ModTopo.NODE_TYPE.SCENE:
                proto_type = ModTopo.PROTO_TYPE.SCENE
            else:
                proto_type = ModTopo.PROTO_TYPE.COMMON
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, self.connect_client_dict[client_node_type][args[0]], proto_type, msg_str)
        else:
            logger.GetLog().error('send msg to an unexpected client node or none args: %s, %s, %s' % (client_node_type, msg_str, args))

    # child class must override functions <<<

    # C++ API >>>
    def OnStartUp(self, conf_file):
        # 移除json的钩子，因为ujson不支持separators关键字,会在couchbase sdk中调用时报错
        import script.common.initscript as init_script
        init_script.HOOK_MODULES.pop('json', None)
        import couchbase._bootstrap
        reload(couchbase._bootstrap)

        CAppBase.OnStartUp(self, conf_file)
        self.InitThreadPool()

        # 初始化战斗常量配置数据
        masters_global.init_battle_config_const_value()
    # C++ API <<<

    # public functions >>>
    def get_db_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)
    # public functions <<<

    def GetTargetByProto(self, proto_type):
        if proto_type == ModTopo.PROTO_TYPE.CHAT:
            return self.GetCt2DbProxyRpcHandler()
        elif proto_type == ModTopo.PROTO_TYPE.FIGHT:
            return self.GetFt2DbProxyRpcHandler()
        elif proto_type == ModTopo.PROTO_TYPE.TEAM:
            return self.GetTm2DbProxyRpcHandler()
        elif proto_type == ModTopo.PROTO_TYPE.SCENE:
            return self.GetScene2DbProxyRpcHandler()

    def GetCt2DbProxyRpcHandler(self):
        return self.ctrpcHandler
    
    def GetTm2DbProxyRpcHandler(self):
        return self.tmrpcHandler
    
    def GetFt2DbProxyRpcHandler(self):
        return self.ftrpcHandler

    def GetScene2DbProxyRpcHandler(self):
        return self.scene_rpc_handler

    def GetThreadPool(self, threadType):
        return self.threadPool[threadType]

    def GetThreadCount(self, threadType):
        return self.get_config("ThreadCount", {}).get(threadType, 1)

    def InitThreadPool(self):
        for threadType in ModConf.DBS.THREAD_TYPE.GetValueList():
            self.threadPool[threadType] = ModTPool.CThreadPool(threadType, self.GetThreadCount(threadType))

    def GetQueryRpcMgr(self):
        return self.queryrpcMgr

    def OnQueryResult(self, conn_id, proto_type, mt, ma):
        """
        查询发送回去
        """
        client_node_type = -1
        if proto_type == ModTopo.PROTO_TYPE.CHAT:
            client_node_type = ModTopo.NODE_TYPE.CHAT
        elif proto_type == ModTopo.PROTO_TYPE.TEAM:
            client_node_type = ModTopo.NODE_TYPE.TEAM
        elif proto_type == ModTopo.PROTO_TYPE.FIGHT:
            client_node_type = ModTopo.NODE_TYPE.FIGHT
        elif proto_type == ModTopo.PROTO_TYPE.SCENE:
            client_node_type = ModTopo.NODE_TYPE.SCENE
        if client_node_type != -1:
            result_rpc = self.get_server_rpc_handler(ModTopo.NODE_TYPE.DB_PROXY, conn_id)
            result_rpc.mt = "On%s" % mt
            result_rpc.ma = (ma,)
            game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, conn_id, proto_type, cPickle.dumps(result_rpc))
        else:
            logger.GetLog().error('OnQueryResult unsupported proto type : %s, %s, %s' % (conn_id, proto_type, mt))

    # monitor to db >>>
    # ====================================================================================
    # ================================ gm command handler ================================
    # ====================================================================================
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('db proxy on gm msg content = %s, %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_db_2_monitor_rpc().OnGMMsgResponse('db proxy %s executed gm command %s fail, fail files : %s' % (self.get_node_id(), gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_db_2_monitor_rpc().OnGMMsgResponse('db proxy %s executed gm command %s success' % (self.get_node_id(), gm_cmd))
        elif gm_cmd == gm_def.gm_cmd_update_data:
            reload_master_list = [x.strip() for x in params_str.split(',') if x]
            logger.GetLog().debug('db reload master : %s' % reload_master_list)
            fail_file_list = []
            for master_inst_name in reload_master_list:
                try:
                    masters_global.reload_data_inst(master_inst_name)
                except Exception as e:
                    fail_file_list.append(master_inst_name)
            if fail_file_list:  # 有失败的文件
                self.get_db_2_monitor_rpc().OnGMMsgResponse('db proxy %s executed gm command %s fail, fail files : %s' % (self.get_node_id(), gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_db_2_monitor_rpc().OnGMMsgResponse('db proxy %s executed gm command %s success' % (self.get_node_id(), gm_cmd))
        else:
            return_msg = 'db proxy unsupported gm command or param unexpected : %s, %s' % (gm_cmd, params_str)
            logger.GetLog().warn(return_msg)
            self.get_db_2_monitor_rpc().OnGMMsgResponse(return_msg)
    # monitor to db <<<
