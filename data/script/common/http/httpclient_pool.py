# -*- coding: utf8 -*-
from script.common.http.httpclient_keepalive import CAsyncHttpClientKeepAlive

DEFAULT_CLIENT_NUM = 1


class CHttpClientPool(object):
    def __init__(self, host, port=None, num=DEFAULT_CLIENT_NUM):
        self.host = host
        self.port = port
        self.clients = []
        self.SetClientNum(num)
        self.cur_index = 0
        self.last_index = 0

    def Shutdown(self):
        for http in self.clients:
            http.Shutdown()

    def SetClientNum(self, num):
        excount = num - len(self.clients)
        for i in xrange(excount):
            http = self.CreateHttp(self.host, self.port)
            self.clients.append(http)

    def CreateHttp(self, *args):
        return CAsyncHttpClientKeepAlive(*args)

    def GetClientNum(self):
        return len(self.clients)

    def request(self, method, url, callback=None, callback_para=None, responsecls=None, body=None, headers=None,
                printlog=False, trycount=3):
        if self.cur_index >= self.GetClientNum():
            self.cur_index = 0
        self.last_index = self.cur_index
        response = self.clients[self.cur_index].request(method, url, callback, callback_para, responsecls, body,
                                                        headers, printlog, trycount)
        self.cur_index += 1
        return response

    def GetLastResponse(self):
        if self.last_index >= self.GetClientNum():
            return None
        return self.clients[self.last_index].GetLastResponse()
