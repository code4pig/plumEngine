# -*- coding: utf8 -*-

import cPickle
import script.common.log as logger


class CMessageHandler(object):

    def LoadRpcMsg(self, msg_str):
        return cPickle.loads(msg_str)

    def OnRpcMsg(self, conn_id, proto, msg_str):
        try:
            rpc_msg = self.LoadRpcMsg(msg_str)
            self.common_handle(rpc_msg, conn_id, proto)
        except:
            logger.GetLog().error('load rpc error : %s' % msg_str)
            raise

    def common_handle(self, rpc_msg, conn_id, proto):
        logger.GetLog().debug('rpc message handler common handler : %s, %s, %s' % (rpc_msg, type(rpc_msg), rpc_msg.__class__))
        callback = getattr(rpc_msg.__class__, "_CallBack", None)
        if callback:
            callback(rpc_msg, conn_id, proto)
        else:
            logger.GetLog().error('common msg_handle can not find _CallBack method of script msg_cls: %s  msg: %s' % (rpc_msg.__class__, rpc_msg))
