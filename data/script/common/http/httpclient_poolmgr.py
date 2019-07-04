# -*- coding: utf8 -*-

import httpclient_pool


class CHttpClientPoolMgr(object):
    def __init__(self):
        self._httppools = {}

    def GetHttpPool(self, host, port=80, clientcount=httpclient_pool.DEFAULT_CLIENT_NUM):
        # 这个函数，
        # 如果ip、port对应的httppool不存在，就创建
        # 否则，返回原来的httppool
        if clientcount <= 0:
            clientcount = httpclient_pool.DEFAULT_CLIENT_NUM
        k = (host, port)
        httppool = self._httppools.get(k)
        if httppool and httppool.GetClientNum() > 0:
            # 查看是否有个数调整？
            oldnum = httppool.GetClientNum()
            if clientcount and clientcount != oldnum:
                httppool.SetClientNum(clientcount)
        else:
            # 创建一个新的pool，且设置有效的client数量
            self._httppools[k] = httpclient_pool.CHttpClientPool(host, port, clientcount)
            httppool = self._httppools[k]
            print "create new http pool by poolmgr", (host, port)
        # 返回一个可以工作的httppool
        return httppool
