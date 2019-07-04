# -*- coding: utf8 -*-

import select
from script.common.netdriver.netdriver_base import CNetDriverBase

TICK_INTERVAL = 100

EPOLL_COMMON_ERR = select.EPOLLERR | select.EPOLLHUP | select.POLLNVAL


class CNetDriverEpoll(CNetDriverBase):
    def __init__(self):
        CNetDriverBase.__init__(self)
        self.epoll = select.epoll()  # for linux
        self.conns_binged_event = {}  # fileid->(conn, state)

        # override

    def OnTick(self, *args):
        events = self.epoll.poll(timeout=0, maxevents=10)
        if not events:
            return
        for fileno, event in events:
            if event & select.EPOLLERR:
                self.conns[fileno].OnSocketError("server disconnected")

            elif event & select.EPOLLHUP:
                self.conns[fileno].OnSocketError("socket hand up")

            elif event & select.EPOLLIN:
                self.conns[fileno].TryRecv()

            elif event & select.EPOLLOUT:
                self.conns[fileno].TrySend()

            elif event & select.POLLPRI:
                print "pollpri event", fileno
                self.conns[fileno].TryRecv()

            elif event & select.POLLNVAL:  # 增加一种异常, 也许这个会出现
                self.conns[fileno].OnSocketError("Invalid request: descriptor not open")
            else:
                print "unreged  epoll event ", fileno, event

                # override

    def StartWrite(self, conn):
        self._BindEvent(conn, select.EPOLLOUT)

        # override

    def StartRead(self, conn):
        self._BindEvent(conn, select.EPOLLIN | select.POLLPRI)

        # override

    def StartReadWrite(self, conn):
        self._BindEvent(conn, select.EPOLLIN | select.POLLPRI | select.EPOLLOUT)

    def _BindEvent(self, conn, event):
        event = event | EPOLL_COMMON_ERR
        fno = conn.GetFileID()
        if self.conns_binged_event.has_key(fno):
            self.epoll.modify(fno, event)
            self.conns_binged_event[fno][1] = event
        else:
            self.epoll.register(fno, event)
            self.conns_binged_event[fno] = [conn, event]

        print "socket file:%s _BindEvent epoll event:%s" % (fno, event)

        # override

    def UnRegConn(self, conn):
        fno = conn.GetFileID()
        if self.conns_binged_event.has_key(fno):
            self.epoll.unregister(fno)
            del self.conns_binged_event[fno]

        CNetDriverBase.UnRegConn(self, conn)
