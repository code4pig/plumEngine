# -*- coding: utf8 -*-
"""
@author: bbz
"""

import game
import script.common.log as logger
import script.common.config.topoconfig as ModTopo
from script.common.rpc.client_rpc_handler import ClientRPCHandler
from script.common.rpc.server_rpc_handler import ServerRPCHandler
from script.common.rpc.query_rpc_handler import QueryRPCHandler
from script.common.utils.singleton import Singleton
from script.common.tickobj import TickObj
from script.common.network.messagehandler import CMessageHandler


class CAppBase(TickObj):
    __metaclass__ = Singleton

    def __init__(self):
        TickObj.__init__(self)
        self.node_id = -1
        self.cur_conn_id = None
        self.cur_proto = None
        self.config = {}  # config key->config value，通过读取配置文件得到
        self.message_handler = CMessageHandler()
        self.server_rpc_handler = ServerRPCHandler()
        self.client_rpc_handler = ClientRPCHandler()
        self.query_rpc_handler = QueryRPCHandler()
        self.connect_server_dict = {}       # node type => client type => connect id
        self.connect_client_dict = {}       # node type => node id => connect id
        self.client_connect_id_dict = {}    # service type => connect id => ip
        self.connect_to_node_dict = {}      # connect id => (node type, node id)

    # child class must override functions >>>
    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        logger.GetLog().error('function send_msg_to_client_node no define in child class : %s, %s, %s' % (client_node_type, msg_str, args))

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        logger.GetLog().error('function send_msg_to_server_node no define in child class : %s, %s, %s' % (client_type, msg_str, args))

    def get_node_type(self):
        logger.GetLog().error('function get_node_type no define in child class')

    # child class must override functions <<<

    # C++ API >>>
    def OnStartUp(self, config_file):
        self._load_config_file(config_file)
        game.InitFrameRate(self.get_config('FrameRate', 60))
        game.OpenHeartBeat(self.get_config('HeartBeat', 1000), self.get_config('HeartBeatCheck', 5000))
        # 设置日志数据级别,默认为info
        self._set_log_level(self.get_config('LogLevel', game.LOG_LV_INFO))
        # 启动网络服务
        self._start_net_service()
        # 检查是否连接Monitor
        if self.get_node_type() != ModTopo.NODE_TYPE.MONITOR:
            # 自己不是Monitor节点，连接Monitor节点
            self._start_connect_monitor()
            if self.get_config('ServerNodeList'):
                # 有关注的server列表, 启动定时器请求关注的服务器列表
                self.RegTick(self._timer_get_want_server_list, None, 30000)  # 启动一个定时器, 请求关注的server_list

    def OnUpdate(self):
        pass

    def OnShutDown(self):
        pass

    def OnClientConnected(self, service_type, conn_id, from_ip):
        logger.GetLog().debug('----------on client connect : %s, %s, %s' % (service_type, conn_id, from_ip))
        if service_type not in self.client_connect_id_dict:
            self.client_connect_id_dict[service_type] = {}
        self.client_connect_id_dict[service_type][conn_id] = from_ip

    def OnClientDisconnect(self, service_type, conn_id):
        logger.GetLog().debug('----------on client disconnect : %s, %s' % (service_type, conn_id))
        # 从客户端连接字典中删除数据
        if service_type in self.client_connect_id_dict:
            self.client_connect_id_dict[service_type].pop(conn_id, None)
        if service_type == ModTopo.SERVICE_TYPE.FOR_NODE and conn_id in self.connect_to_node_dict:
            client_node_type, client_node_id = self.connect_to_node_dict[conn_id]
            if client_node_type in self.connect_client_dict:
                self.connect_client_dict[client_node_type].pop(client_node_id, None)

    def OnClientRpcMsg(self, service_type, conn_id, proto, msg_str):
        self.message_handler.OnRpcMsg(conn_id, proto, msg_str)

    def OnConnectToServerFailed(self, client_type, errmsg):
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type == ModTopo.NODE_TYPE.MONITOR:
            # 连接monitor失败, 尝试重连
            logger.GetLog().error('Connect Monitor Failed, Try to Connect')
            self._start_connect_monitor()

    def OnServerDisconnect(self, client_type):
        # 先删除字典记录的server信息
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type in self.connect_server_dict:
            self.connect_server_dict[server_node_type].pop(client_type, None)
        # 各种节点处理
        if server_node_type == ModTopo.NODE_TYPE.MONITOR:
            # 如果是Monitor断开, 尝试重连
            logger.GetLog().error('Monitor Node Disconnected, Try to Connect')
            self._start_connect_monitor()

    def OnConnectToServer(self, client_type, conn_id, ip):
        # 先将连接信息加入到字典
        node_type = self.get_node_type_by_client_type(client_type)
        if node_type not in self.connect_server_dict:
            self.connect_server_dict[node_type] = {}
        self.connect_server_dict[node_type][client_type] = conn_id

        if node_type == ModTopo.NODE_TYPE.MONITOR:
            # 连接的是Monitor节点, 发送注册协议
            self.register_node_to_monitor(client_type)
        else:
            # 连接到其他节点，发起握手协议
            self.send_handshake(client_type)

    def OnServerRpcMsg(self, client_type, conn_id, proto, msg_str):
        self.message_handler.OnRpcMsg(conn_id, proto, msg_str)

    # C++ API <<<

    # normal functions >>>
    def get_node_id(self):
        return self.node_id

    def get_config(self, config_key, default_value=None):
        return self.config.get(config_key, default_value)

    def get_connect_ip(self, service_type, conn_id):
        if service_type in self.client_connect_id_dict and conn_id in self.client_connect_id_dict[service_type]:
            return self.client_connect_id_dict[service_type][conn_id]
        return None

    def get_server_rpc_handler(self, client_node_type, *args):
        self.server_rpc_handler.set_args(client_node_type, *args)  # 作为server而言, 都是对于节点的, 所以用client node type即可
        return self.server_rpc_handler

    def get_client_rpc_handler(self, client_type, *args):
        self.client_rpc_handler.set_args(client_type, *args)
        return self.client_rpc_handler

    def get_send_query_rpc_handler(self, client_type, *args):
        self.query_rpc_handler.set_args(client_type, *args)
        return self.query_rpc_handler

    def get_client_node_connect_id_list(self, client_node_type):
        if client_node_type in self.connect_client_dict:
            return self.connect_client_dict[client_node_type].values()
        return []

    def get_server_node_connect_id_list(self, server_node_type):
        if server_node_type in self.connect_server_dict:
            return self.connect_server_dict[server_node_type].values()
        return []

    def get_client_connect_id(self, client_node_type, client_node_id):
        if client_node_type in self.connect_client_dict:
            return self.connect_client_dict[client_node_type].get(client_node_id, -1)
        return -1

    def get_server_node_connect_id(self, server_node_type, client_type):
        if server_node_type in self.connect_server_dict:
            return self.connect_server_dict[server_node_type].get(client_type, -1)
        return -1

    @staticmethod
    def get_node_type_by_client_type(client_type):
        return client_type / 100 * 100  # 此处意味着每种节点不能超过100个

    @staticmethod
    def get_node_id_by_client_type(client_type):
        return client_type % 100

    @staticmethod
    def construct_client_type(server_node_type, server_node_id):
        """
        client_type is makeup by server_node_type and server_node_id
        """
        return server_node_type + server_node_id

    # normal functions <<<

    # private functions >>>
    def _start_net_service(self):
        service_dict = self.get_config('Services')
        if service_dict:
            for service_type, addr_info in service_dict.iteritems():
                game.StartNetwork(service_type, addr_info[0], addr_info[2], addr_info[3], addr_info[4])

    def _start_connect_monitor(self):
        monitor_addr = self.get_config('MonitorAddr')
        if monitor_addr:
            logger.GetLog().info('node start to connect monitor')
            game.ConnectToServer(ModTopo.NODE_TYPE.MONITOR, monitor_addr[0], monitor_addr[1])
        else:
            logger.GetLog().error('MonitorAddr not in config file: %s'.format(self.get_node_type()))

    def _load_config_file(self, config_file):
        if config_file:
            mod_conf = __import__(config_file.replace('/', '.'), globals(), locals(), ['conf', ], -1)
            self.config = mod_conf.conf
            logger.GetLog().info('load_config_file : %s, content: %s' % (config_file, self.config))
        else:
            logger.GetLog().error('load_config_file but filename is empty')

    def _set_log_level(self, log_level):
        if log_level not in [game.LOG_LV_DEBUG, game.LOG_LV_INFO, game.LOG_LV_WARNING, game.LOG_LV_ERROR]:
            logger.GetLog().error('set log level : %s is invalid', log_level)
            return
        game.SetLogLevel(log_level)

    def _timer_get_want_server_list(self, args=None):
        logger.GetLog().debug('_timer_get_want_server_list')
        if ModTopo.NODE_TYPE.MONITOR in self.connect_server_dict and self.connect_server_dict[ModTopo.NODE_TYPE.MONITOR]:
            self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR).GetWantServerList(self.get_config('ServerNodeList'))
        else:
            logger.GetLog().warn('monitor node is not in connect_server_dict')

    def _start_connect_server(self, server_node_type, server_node_id, server_node_addr, server_node_port):
        if server_node_type not in self.connect_server_dict or \
           self.construct_client_type(server_node_type, server_node_id) not in self.connect_server_dict[server_node_type]:
            # 节点未连接, 发起连接
            logger.GetLog().info('start connect server node : %s, %s, %s, %s' % (server_node_type, server_node_id, server_node_addr, server_node_port))
            game.ConnectToServer(self.construct_client_type(server_node_type, server_node_id), server_node_addr, server_node_port)

    # private functions <<<

    # base rpc functions >>>
    def register_node_to_monitor(self, client_type):
        for_node_addr = None
        for_node_port = None
        service_conf = self.get_config('Services')
        if service_conf and ModTopo.SERVICE_TYPE.FOR_NODE in service_conf:
            for_node_addr = service_conf[ModTopo.SERVICE_TYPE.FOR_NODE][1]
            for_node_port = service_conf[ModTopo.SERVICE_TYPE.FOR_NODE][2]
        self.get_client_rpc_handler(client_type).RegisterNode(self.get_node_type(), for_node_addr, for_node_port, self.get_config('ServerNodeList'))

    def send_handshake(self, client_type):
        handshake_msg = 'Hello, I\'m %s [%s]' % (self.__class__.__name__, self.get_node_id())
        logger.GetLog().info('send_handshake : %s, %s' % (client_type, handshake_msg))
        self.get_client_rpc_handler(client_type).HandShake(handshake_msg, self.get_node_type(), self.get_node_id())

    def RegisterNodeResponse(self, node_id, server_node_info_list=None):
        logger.GetLog().info('RegisterNodeResponse : %s, %s' % (node_id, server_node_info_list))
        self.node_id = node_id
        if server_node_info_list:
            # 连接节点
            for server_node_type, server_node_id, server_node_addr, server_node_port in server_node_info_list:
                self._start_connect_server(server_node_type, server_node_id, server_node_addr, server_node_port)

    def HandShake(self, handshake_msg, client_node_type, client_node_id):
        logger.GetLog().info('receive HandShake : %s, %s, %s' % (handshake_msg, client_node_type, client_node_id))
        # 将节点信息保存到字典
        if client_node_type not in self.connect_client_dict:
            self.connect_client_dict[client_node_type] = {}
        self.connect_client_dict[client_node_type][client_node_id] = self.cur_conn_id
        self.connect_to_node_dict[self.cur_conn_id] = (client_node_type, client_node_id)
        # 握手协议返回
        handshake_response = 'Hello I\'m %s [%s]' % (self.__class__.__name__, self.get_node_id())
        self.get_server_rpc_handler(client_node_type, client_node_id).HandShakeResponse(handshake_response)

    def HandShakeResponse(self, handshake_response):
        logger.GetLog().info('receive HandShakeResponse %s' % handshake_response)

    def GetWantServerListResponse(self, server_node_info_list):
        logger.GetLog().info('GetWantServerListResponse : %s' % server_node_info_list)
        if server_node_info_list:
            for server_node_type, server_node_id, server_node_addr, server_node_port in server_node_info_list:
                self._start_connect_server(server_node_type, server_node_id, server_node_addr, server_node_port)
    # base rpc functions <<<
