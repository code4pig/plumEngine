# -*- coding: utf8 -*-

# dns cache  避免每次httpclient 建立socket dns请求阻塞

import socket
import time
import game
from script.common.utils.singleton import Singleton


class CDnsCache(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.http_dns_cache = {}  # (host, port)-> addinfo

    def GetHttpAddrInfo(self, host, port):
        key = (host, port)
        info = self.http_dns_cache.get(key)
        if info:
            return info

        begin = time.time()
        print "http dns not hit. to refresh it... host:%s, port:%s" % key
        try:
            res = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
        except:
            print "getaddrinfo failed", (host, port)
            return None
        if len(res) <= 0:
            print "获取地址失败！！host:%s, port:%s" % (host, port)
            if game.isdev:
                raise Exception("获取地址失败！！host:%s, port:%s" % (host, port))
            return None
        else:
            info = res[0]  # af, socktype, proto, canonname, sa
            self.http_dns_cache[key] = info
            t = time.time() - begin
            print "http dns get succ. %s  usetime:%s" % (info, t)
            return info


g_Inst = None


def GetDnsCache():
    global g_Inst
    if g_Inst is None:
        g_Inst = CDnsCache()
    return g_Inst
