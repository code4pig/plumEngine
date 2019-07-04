# -*- coding: utf-8 -*-
"""
@author: bbz
"""
import script.object_factory as ModObjFac
import script.common.log as logger


class IBaseRpc(object):
    def __init__(self, *args):
        self._local = True
        self.mt = None
        self.ma = None
        self.args = args

    def set_args(self, *args):
        logger.GetLog().error('function set_args no define in child class : %s' % (args, ))

    def __str__(self):
        return "cls:%s mt:%s" % (self.__class__, self.mt)

    def __setstate__(self, data):
        self.__dict__ = data
        self._local = False

    def __getattr__(self, method_name):
        if self.__dict__.get("_local"):
            if method_name[:2] == "__":
                raise AttributeError("rpc obj has no method:%s :: %s" % (self.__class__, method_name))

            method = self._CreateRpcMethod(method_name)
            setattr(self.__class__, method_name, method)
            return getattr(self, method_name)
        else:
            raise AttributeError("rpc msg handler' attribute _local is False: %s :: %s" % (self.__class__, method_name))

    def __set_as_caller__(self):
        self._local = True

    def _GetTarget(self):
        return ModObjFac.CreateApp()

    def _CreateRpcMethod(self, method_name):
        def __rpccall__(self, *ma):  # args of method call
            self.mt = method_name
            self.ma = ma
            self._SendCall(self)
            return None
        return __rpccall__

    def _SendCall(self, msg):
        logger.GetLog().error('function _SendCall no define in child class : %s' % msg)

    def _CallBack(self, conn_id, proto):
        try:
            target = self._GetTarget()
            if target:
                target.cur_conn_id = conn_id
                target.cur_proto = proto
                method = getattr(target, self.mt, None)
                if method:
                    method(*self.ma)
                    return True
                else:
                    logger.GetLog().warn('can not find rpc method: %s, %s' % (self.mt, target.__class__))
            else:
                logger.GetLog().warn('not rpc target method:%s args:%s cls:%s' % (self.mt, self.ma, self.__class__))
        except:
            logger.GetLog().error('rpc callback error. method:%s args:%s' % (self.mt, self.ma))
            raise

        return False
