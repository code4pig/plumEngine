# -*- coding: utf8 -*-
# 

import traceback
import threading, time


class CDbThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = False
        self._jobList = []
        self._jobListLock = threading.RLock()
        self._logLock = threading.RLock()
        self._errLogList = []
        self._logicJobMap = {}

    def start(self):
        self._running = True
        threading.Thread.start(self)

    def Exit(self):
        self._running = False

        # clear job
        job = self._PopJob()
        while job:
            try:
                job and job.RunJob()
            except:
                traceback.print_exc()
            job = self._PopJob()

    def GetLogicJobMap(self):
        if getattr(self, "_logicJobMap", None) is None:
            self._logicJobMap = {}
        return self._logicJobMap

    def PushJob(self, job):
        if not self.isAlive():
            return 0

        self._jobListLock.acquire()

        bReplaceJob = False  # 标识是替换或append
        if len(self._jobList) >= self.GetBushJobCount():  # 超过一定数量需要检测唯一性
            logicKey = job.GetLogicKey()
            if logicKey is not None:  # 需要检测唯一key的job
                print "logic thread is busy while pushjob. jobcount:%s logickey:%s" % (len(self._jobList), logicKey)
                cur_job = self.GetLogicJobMap().get(logicKey)
                if cur_job:  # 已经存在
                    job.Merge(cur_job)
                    cur_job.__dict__ = job.__dict__  # replace
                    bReplaceJob = True
                    print "replace logicjob: %s" % logicKey

        if not bReplaceJob:  # 正常append
            self._jobList.append(job)
            logicKey = job.GetLogicKey()
            if logicKey is not None:  # 需要检测唯一key的job
                self.GetLogicJobMap()[logicKey] = job
                # print "append logicjob: %s" % logicKey

        joblen = len(self._jobList)
        self._jobListLock.release()
        return joblen  # 正常必然>0

    def GetBushJobCount(self):
        return 200

    def _PopJob(self):
        self._jobListLock.acquire()

        job = None
        if len(self._jobList) != 0:
            job = self._jobList[0]
            del self._jobList[0]

            logicKey = job.GetLogicKey()
            if logicKey is not None:  # 需要检测唯一key的job
                jobMap = self.GetLogicJobMap()
                jobMap.pop(logicKey, None)
                # print "pop logic job: %s" % logicKey

            if len(self._jobList) >= self.GetBushJobCount():
                job.SetThreadBusy(True)
                if logicKey is not None:
                    print "logic thread is busy while popjob. jobcount:%s logickey:%s" % (len(self._jobList), logicKey)

        self._jobListLock.release()

        return job

    def WriteLog(self, log):
        self._logLock.acquire()
        self._errLogList.append(log)
        self._logLock.release()

    def WriteLogs(self, logs):
        self._logLock.acquire()
        self._errLogList.extend(logs)
        self._logLock.release()

    def GetLogs(self):
        self._logLock.acquire()
        logs = self._errLogList
        self._errLogList = []
        self._logLock.release()
        return logs

    def sleep(self):
        time.sleep(0.01)

    def run(self):
        while self._running:
            self._run()

    def _run(self):
        self.runjobs()

    def runjobs(self):
        job = None
        try:
            job = self._PopJob()
            if job is None:
                self.sleep()
            else:
                job.RunJob()
                self.WriteLogs(job.GetLogs())

        except:
            self.WriteLog(traceback.format_exc())
            print traceback.format_exc()
