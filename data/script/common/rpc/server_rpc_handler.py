# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-10-16 15:06

from __future__ import unicode_literals

import script.object_factory as ModObjFac
import cPickle
import script.common.log as logger
from script.common.rpc.rpcbase import IBaseRpc


class ServerRPCHandler(IBaseRpc):
    def __init__(self, *args):
        IBaseRpc.__init__(self, *args)
        self.client_node_type = -1

    def set_args(self, client_node_type, *args):
        self.client_node_type = client_node_type
        self.args = args

    def _SendCall(self, msg):
        logger.GetLog().debug('ServerRPCHandler _SendCall : %s' % msg)
        msg_str = cPickle.dumps(msg)
        ModObjFac.CreateApp().send_msg_to_client_node(self.client_node_type, msg_str, *self.args)
