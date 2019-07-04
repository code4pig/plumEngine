# -*- coding: utf8 -*-

import game
from script.common.netdriver.netdriver_select import CNetDriverSelect

g_NetDriver = None


def GetNetDriver():
    global g_NetDriver
    if g_NetDriver is None:
        if game.islinux:
            from script.globalcommon.netdriver.netdriver_epoll import CNetDriverEpoll
            print "py use epoll netdriver"
            g_NetDriver = CNetDriverEpoll()
        else:  # windows use select driver
            print "py use select netdriver"
            g_NetDriver = CNetDriverSelect()

    return g_NetDriver
