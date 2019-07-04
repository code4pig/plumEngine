# -*- coding: utf8 -*-
# CThreadPool
# 

from script.dbproxy.thread.dbthread import CDbThread


class CThreadPool(object):
    def __init__(self, threadType, threadNum):
        self._threadList = []
        self._threadPos = 0
        self.Init(threadType, threadNum)

    def Init(self, threadType, threadNum):
        self._threadType = threadType
        for i in xrange(threadNum):
            t = CDbThread()
            t.start()
            self._threadList.append(t)
        print "类型为%d的DbThread开启了%d个 " % (threadType, threadNum)

    def GetThreadList(self):
        return self._threadList

    def Quit(self):
        for t in self._threadList:
            t.Exit()

    def DispatcherJob(self, job, channel=-1):
        joblen = 0
        if channel < 0:
            joblen = self._PushJob(job, self._threadPos)
            self._threadPos = (self._threadPos + 1) % len(self._threadList)
        else:
            p = channel % self.GetChannelCount()
            joblen = self._PushJob(job, p)
        return joblen

        # 返回通道数量

    def GetChannelCount(self):
        threadList = self.GetThreadList()
        if threadList is None:
            return 0
        return len(threadList)

    def _PushJob(self, job, channel):
        if channel < 0 or channel >= len(self._threadList):
            return 0

        logs = self._threadList[channel].GetLogs()
        for log in logs:
            print log

        joblen = self._threadList[channel].PushJob(job)
        if joblen <= 0:
            print "[CThreadPool]Push job failed, channel number %d." % (channel)

            jobList = self._threadList[channel]._jobList
            self._threadList[channel]._jobList = []
            self._threadList[channel].Exit()

            self._threadList[channel] = CDbThread()
            self._threadList[channel]._jobList = jobList
            self._threadList[channel].start()

            joblen = self._threadList[channel].PushJob(job)
        return joblen
