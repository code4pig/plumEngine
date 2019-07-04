# -*- coding: utf8 -*-
"""
在httpclient的基础上
设置一个回调函数用于处理成功获取到的返回内容
这样对一些简单的应用来说
就不需要做复杂的派生类了
只需要写一个处理函数即可
"""

import httpclient_poolmgr


class CHttpWithCallbackClientPoolMgr(httpclient_poolmgr.CHttpClientPoolMgr):
    CLIENT_COUNT = 2

    def __init__(self):
        super(CHttpWithCallbackClientPoolMgr, self).__init__()

    def AddRequestWithCallback(self, host, port, method, url, callbackdata, body=None, header=None,
                               paraCnt=CLIENT_COUNT, printlog=True, trycount=3):
        httppool = self.GetHttpPool(host, port, paraCnt)
        if not httppool:
            print "gethttppool 为None, 这不可能嘛？"
            return False

        # 发请求
        # 底层会生成一个新的response数据
        # 而且这个请求不是马上发送的
        # 是以tick的方式延迟发生
        # 所以下一步的setcallback是有效的
        callback, param = callbackdata
        httppool.request(method, url, callback, param, None, body, header, printlog, trycount)
        return True


g_mgr = None


def GetHttpMgr():
    global g_mgr
    if not g_mgr:
        g_mgr = CHttpWithCallbackClientPoolMgr()
    return g_mgr
