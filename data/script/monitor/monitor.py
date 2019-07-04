# -*- coding: utf-8 -*-
# __author__ = 'Yoray'

import game

import script.common.log as logger
import script.common.config.topoconfig as ModTopo
from script.common.utils.singleton import Singleton
from script.common.tickobj import TickObj
from script.common.rpc.server_rpc_handler import ServerRPCHandler
from script.common.network.messagehandler import CMessageHandler
from script.monitor.gm_msg_handler import GMMsgHandler


class NodeInfo(object):
    connect_id = None
    from_ip = None
    node_type = None
    node_id = None
    node_addr = None
    node_port = 0


class CMonitor(TickObj):
    __metaclass__ = Singleton

    def __init__(self):
        TickObj.__init__(self)
        self.config = {}                # config key->config value，通过读取配置文件得到
        self.connect_dict = {}          # 连接字典 service_type => conn_id => from ip
        # node节点记录
        self.node_counter_dict = {}         # node type => counter
        self.node_connect_info_dict = {}    # connect id -> node info
        self.node_type_connect_dict = {}    # node type -> connect id list
        # rpc
        self.cur_conn_id = None
        self.cur_proto = None
        self.server_rpc_handler = ServerRPCHandler()
        self.rpc_message_handler = CMessageHandler()
        # for client
        self.gm_msg_handler = GMMsgHandler()

    # >>> 获得rpc 对象
    def get_monitor_2_node_rpc(self, client_node_type=0, connect_id=None):
        self.server_rpc_handler.set_args(client_node_type, connect_id)
        return self.server_rpc_handler
    # <<< 获得rpc 对象

    # >>> 给节点发送消息接口
    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        if client_node_type != ModTopo.NODE_TYPE.CLIENT:
            if args and args[0] > 0:
                # 有指定的connect id
                connect_id = args[0]
                game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, connect_id, ModTopo.PROTO_TYPE.COMMON, msg_str)
            else:
                # 没有指定的connect id，广播给所有该类型节点
                if client_node_type in self.node_type_connect_dict:
                    for connect_id in self.node_type_connect_dict[client_node_type]:
                        game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, connect_id, ModTopo.PROTO_TYPE.COMMON, msg_str)
                else:
                    logger.GetLog().warn('will send msg to node {0}, but node not found'.format(client_node_type))

    @staticmethod
    def send_msg_to_client(connect_id, msg_str):
        game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_CLIENT, connect_id, ModTopo.PROTO_TYPE.COMMON, msg_str)
    # <<< 给节点发送消息接口

    # >>> C++ 层回调用函数
    def OnStartUp(self, config_file):
        self._load_config_file(config_file)
        game.InitFrameRate(self._get_config('FrameRate', 60))
        game.OpenHeartBeat(self._get_config('HeartBeat', 1000), self._get_config('HeartBeatCheck', 5000))
        # 设置日志数据级别,默认为warning
        self._set_log_level(self._get_config('LogLevel', game.LOG_LV_WARNING))
        # 启动服务
        self._start_net_service()

    def OnUpdate(self):
        pass

    def OnShutDown(self):
        pass

    def OnClientConnected(self, service_type, conn_id, from_ip):
        logger.GetLog().info('on client connect to monitor : %s, %s, %s' % (service_type, conn_id, from_ip))
        # 添加到字典
        self._add_connect(service_type, conn_id, from_ip)

    def OnClientDisconnect(self, service_type, conn_id):
        logger.GetLog().info('on client disconnect from monitor : %s, %s' % (service_type, conn_id))
        self._del_connect(service_type, conn_id)

    def OnClientRpcMsg(self, service_type, conn_id, proto_type, msg_str):
        logger.GetLog().info('receive client message from %s, %s, %s' % (service_type, conn_id, proto_type))
        if service_type == ModTopo.SERVICE_TYPE.FOR_NODE:
            # 是来自node的消息
            self.rpc_message_handler.OnRpcMsg(conn_id, proto_type, msg_str)
        elif service_type == ModTopo.SERVICE_TYPE.FOR_CLIENT:
            # 是来自客户端的消息
            self.gm_msg_handler.handle_gm_msg(conn_id, proto_type, msg_str)
    # <<< C++ 层回调用函数

    # >>> 基础服务接口
    @staticmethod
    def get_node_type():
        return ModTopo.NODE_TYPE.MONITOR

    def _get_config(self, config_key, default_value=None):
        return self.config.get(config_key, default_value)

    def _load_config_file(self, config_file):
        if config_file:
            mod_conf = __import__(config_file.replace('/', '.'), globals(), locals(), ['conf', ], -1)
            self.config = mod_conf.conf
            logger.GetLog().info('_load_config_file %s : %s' % (config_file, self.config))
        else:
            logger.GetLog().error('_load_config_file but filename is empty')

    def _start_net_service(self):
        service_dict = self._get_config('Services')
        if service_dict:
            for service_type, addr_info in service_dict.iteritems():
                game.StartNetwork(service_type, addr_info[0], addr_info[1], addr_info[2], addr_info[3])

    @staticmethod
    def _set_log_level(log_level):
        if log_level not in [game.LOG_LV_DEBUG, game.LOG_LV_INFO, game.LOG_LV_WARNING, game.LOG_LV_ERROR]:
            logger.GetLog().error('set log level : %s is invalid', log_level)
            return
        game.SetLogLevel(log_level)
    # <<< 基础服务接口

    # >>> 连接信息接口
    def _add_node_connect_info(self, node_info):
        self.node_connect_info_dict[node_info.connect_id] = node_info
        if node_info.node_type not in self.node_type_connect_dict:
            self.node_type_connect_dict[node_info.node_type] = []
        self.node_type_connect_dict[node_info.node_type].append(node_info.connect_id)

    def _del_node_connect_info(self, connect_id):
        node_connect_info = self.node_connect_info_dict.get(connect_id, None)
        if node_connect_info:
            if node_connect_info.node_type in self.node_type_connect_dict and \
               connect_id in self.node_type_connect_dict[node_connect_info.node_type]:
                self.node_type_connect_dict[node_connect_info.node_type].remove(connect_id)
            self.node_connect_info_dict.pop(connect_id, None)

    def _add_connect(self, service_type, connect_id, from_ip):
        if service_type not in self.connect_dict:
            self.connect_dict[service_type] = {}
        self.connect_dict[service_type][connect_id] = from_ip

    def _del_connect(self, service_type, connect_id):
        if service_type in self.connect_dict:
            self.connect_dict[service_type].pop(connect_id, None)
        if service_type == ModTopo.SERVICE_TYPE.FOR_NODE:
            # 是节点断开, 则同时剔除节点信息
            self._del_node_connect_info(connect_id)

    def get_node_connect_ids(self, node_type):
        return self.node_type_connect_dict.get(node_type, None)
    # <<< 连接信息接口

    # >>> 定时器函数
    # self.RegTick(self.SecTick, "this is tick", 1000)
    # def SecTick(self, msg):
    #     """
    #     tick测试
    #     """
    #     self.DelTick(self.SecTick)
    # <<< 定时器函数

    # >>> rpc 相关
    def RegisterNode(self, node_type, node_addr, node_port, want_server_node_list):
        logger.GetLog().info('Node register : %s, %s, %s' % (node_type, node_addr, node_port))
        if node_type not in self.node_counter_dict:
            self.node_counter_dict[node_type] = 0
        # 先将节点id计数器自增
        self.node_counter_dict[node_type] += 1
        if self.node_counter_dict[node_type] >= 90:
            logger.GetLog().warn('node type counter maybe reach the max : %s' % node_type)
        # 构造节点连接信息
        node_info = NodeInfo()
        node_info.connect_id = self.cur_conn_id
        node_info.from_ip = self.connect_dict[ModTopo.SERVICE_TYPE.FOR_NODE].get(self.cur_conn_id, None)
        node_info.node_type = node_type
        node_info.node_id = self.node_counter_dict[node_type]
        node_info.node_addr = node_addr
        node_info.node_port = node_port
        # 将节点信息添加字典里
        self._add_node_connect_info(node_info)
        # 构造返回信息
        server_list = None
        if want_server_node_list:
            server_list = []
            for want_server_type in want_server_node_list:
                if want_server_type in self.node_type_connect_dict:
                    for want_server_connect_id in self.node_type_connect_dict[want_server_type]:
                        want_server = self.node_connect_info_dict[want_server_connect_id]
                        server_list.append([want_server.node_type, want_server.node_id, want_server.node_addr, want_server.node_port])
        self.get_monitor_2_node_rpc(node_type, self.cur_conn_id).RegisterNodeResponse(node_info.node_id, server_list)

    def GetWantServerList(self, want_server_node_list):
        if want_server_node_list:
            server_list = []
            for want_server_type in want_server_node_list:
                if want_server_type in self.node_type_connect_dict:
                    for want_server_connect_id in self.node_type_connect_dict[want_server_type]:
                        want_server = self.node_connect_info_dict[want_server_connect_id]
                        server_list.append([want_server.node_type, want_server.node_id, want_server.node_addr, want_server.node_port])
            self.get_monitor_2_node_rpc(0, self.cur_conn_id).GetWantServerListResponse(server_list)

    def OnGMMsgResponse(self, ret_msg):
        # 结果返回给操作请求者
        self.gm_msg_handler.OnGMMsgHandleResponse(ret_msg)
    # <<< rpc 相关