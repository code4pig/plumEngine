# -*- coding: utf8 -*-
import game


class CNetDriverBase(object):
    TICK_INTERVAL = 60

    def __init__(self):
        self.conns = {}  # fileid->conn
        self.regticked = False

    def _RegTick(self):
        game.RegTick(self.OnTick, None, self.TICK_INTERVAL)
        self.regticked = True

    def _UnRegTick(self):
        if self.regticked:
            game.DelTick(self.OnTick)
            self.regticked = False

    def RegConn(self, conn):
        fno = conn.GetFileID()
        if fno is None:
            print "can not regconn, fileid is None", conn
            return
        if self.conns.has_key(fno):
            raise Exception("dulplicate conn fileno while regconn %s" % fno)
            return
        self.conns[fno] = conn

        if not self.regticked:
            self._RegTick()

    def UnRegConn(self, conn):
        fno = conn.GetFileID()
        self.conns.pop(fno, None)
        if not self.conns:
            self._UnRegTick()

    def OnTick(self, *args):
        pass

    def StartWrite(self, conn):
        pass

    def StartRead(self, conn):
        pass

    def StartReadWrite(self, conn):
        pass
