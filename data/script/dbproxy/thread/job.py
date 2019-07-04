# -*- coding: utf8 -*-
# 
import game
import traceback
import script.dbproxy.object_factory as ModObjFac


class IJob(object):
    def __init__(self):
        self._errLogList = []

    def WriteLog(self, msg):
        print msg

    def GetLogs(self):
        if getattr(self, "_errLogList", None) is None:
            setattr(self, "_errLogList", [])

        return self._errLogList

    def GetLogicKey(self):  # 用来踢出thread中相同logickey的job
        return None

    def Merge(self, old_job):
        pass

    def IsThreadBusy(self):
        return getattr(self, "_threadbusy", False)

    def SetThreadBusy(self, busy):
        self._threadbusy = busy

    def Prepare(self):
        pass

    def Execute(self):
        pass

    def Release(self):
        pass

    def RollBack(self):
        pass

    def Commit(self):
        pass

    def RunJob(self):
        try:
            self.Prepare()
            if game.isdebug:
                exeResult = self.prof_exe()
            else:
                exeResult = self.Execute()

            self.Commit()
            self.Release()
            return exeResult
        except:
            self.WriteLog(traceback.format_exc())
            try:
                self.RollBack()
            except:
                self.WriteLog(traceback.format_exc())
                # rollback和release分开try， 防止rollback异常无法release
            try:
                self.Release()
            except:
                self.WriteLog(traceback.format_exc())

        return None

    def prof_exe(self):
        t = game.GetFastTimeInMs()
        exeResult = self.Execute()
        subtime = game.GetFastTimeInMs() - t
        if subtime > 50:
            print "[WARNING]Job执行时间过长 %s毫秒。 请速度查证 %s" % (subtime, self)
        return exeResult


# rpc 查询
class CRpcJob(IJob):
    def __init__(self, queryRpcMsg, connid):
        self._queryRpcMsg = queryRpcMsg
        self._connid = connid

    def Execute(self):  # called by  db thread
        ret = self._queryRpcMsg.ExeQuery()
        if ret is not None:  # 默认规则是如果返回None则不返回结果给client
            ModObjFac.CreateApp().OnQueryResult(self._connid, self._queryRpcMsg.proto_type, self._queryRpcMsg._ori_mt, ret)


class CLocalJob(IJob):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def Execute(self):
        self.func(*self.args)
