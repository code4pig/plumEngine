# -*- coding: utf8 -*-

import script.object_factory as ModObjFac
import cPickle
import script.common.log as logger
from script.common.rpc.rpcbase import IBaseRpc


class QueryRPCHandler(IBaseRpc):
    def __init__(self):
        IBaseRpc.__init__(self)
        self.client_type = -1
        self.proto_type = None

    # sender related function >>>
    def set_args(self, client_type, *args):
        self.client_type = client_type
        self.args = args

    def _SendCall(self, msg):
        logger.GetLog().debug('QueryRPCHandler _SendCall : %s' % msg)
        msg_str = cPickle.dumps(msg)
        ModObjFac.CreateApp().send_msg_to_server_node(self.client_type, msg_str, *self.args)

    # sender related function <<<

    # receiver related function >>>
    def GetTargetChannel(self):
        # 默认情况下，为了线程数据安全，远端的target返回的是一个固定的channel
        return self._GetTarget().GetRpcChannel()

    def GetTargetThreadType(self):
        return self._GetTarget().GetRpcThreadType()

        # 普通的数据库查询消息处理。 exe in dbs

    def _CallBack(self, conn_id, proto):
        import script.dbproxy.object_factory as ModObjFac
        self.proto_type = proto
        ModObjFac.CreateApp().GetQueryRpcMgr().PushRpcJob(self, conn_id)

    def _GetTarget(self):
        import script.dbproxy.object_factory as ModObjFac
        return ModObjFac.CreateApp().GetTargetByProto(self.proto_type)

        # exe it on dbs server

    def ExeQuery(self):
        mt, ma = self.mt, self.ma
        self._ori_mt = mt
        target = self._GetTarget()
        if target:
            method = getattr(target, mt, None)
            if method:
                return method(*ma)
            else:
                print "can not find query rpc method:%s, target_class:%s" % (mt, target.__class__)
                return None
        else:
            print "can not find rpc target, query rpc msg class:%s" % (self.__class__)

        return None

        # 数据库返回消息, exe it on dbs client
    # receiver related function <<<
