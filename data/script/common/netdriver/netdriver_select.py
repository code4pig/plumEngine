# -*- coding: utf8 -*-
from script.common.netdriver.netdriver_base import CNetDriverBase

# select 也抽象成一种NetDriver的子类，方便epoll和select随意移植。

SELECT_READ = 1
SELECT_WRITE = 2

import socket
import select
import errno


class CNetDriverSelect(CNetDriverBase):
    def __init__(self):
        CNetDriverBase.__init__(self)
        self.conns_binged_event = {}  # fileid->st

    def OnTick(self, *args):
        for fno, conn in self.conns.items():
            event = self.conns_binged_event.get(fno)
            if event is None:
                print "event is None. unreg it", conn
                self.UnRegConn(conn)
                continue

            if event & SELECT_READ:
                try:
                    infds, outfds, errfds = select.select([conn.sock, ], [], [conn.sock, ], 0)
                except socket.error, err:
                    if err[0] == conn.GetServerAbortedError():
                        conn.OnSocketError("httpserver soft aborted...")
                    elif err[0] == errno.EPIPE:
                        conn.OnSocketError("httpserver disconnected...")
                    else:
                        conn.OnSocketError(err)
                    continue

                if len(infds) != 0:
                    conn.TryRecv()

            elif event & SELECT_WRITE:
                try:
                    infds, outfds, errfds = select.select([], [conn.sock, ], [conn.sock, ], 0)
                except socket.error, err:
                    if err[0] == conn.GetServerAbortedError():
                        conn.OnSocketError("httpserver soft aborted...")
                    elif err[0] == errno.EPIPE:
                        conn.OnSocketError("httpserver disconnected...")
                    else:
                        conn.OnSocketError(err)
                    continue

                if len(outfds) != 0:
                    conn.TrySend()
            else:
                print "unreged  epoll event ", fno, event

                # override

    def UnRegConn(self, conn):
        fno = conn.GetFileID()
        if self.conns_binged_event.has_key(fno):
            del self.conns_binged_event[fno]

        CNetDriverBase.UnRegConn(self, conn)

        # override

    def StartWrite(self, conn):
        self._BindEvent(conn, SELECT_WRITE)

        # override

    def StartRead(self, conn):
        self._BindEvent(conn, SELECT_READ)

        # override

    def StartReadWrite(self, conn):
        self._BindEvent(conn, SELECT_READ | SELECT_WRITE)

    def _BindEvent(self, conn, event):
        fno = conn.GetFileID()
        self.conns_binged_event[fno] = event
