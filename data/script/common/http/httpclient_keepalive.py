# -*- coding: utf8 -*-
"""
非阻塞httpclient短连接.
"""

import socket
import traceback
import errno
import httplib
import cStringIO
import game
import script.common.netdriver as netdriver
import script.common.http.dns_cache as dns_cache

global connid
connid = 0


def CreateConnId():
    global connid
    connid += 1
    return connid


class CAsyncHttpResponseKeepLive(object):
    READ_SIZE_EACH_TIME = 4096

    def __init__(self, http, callback=None, cbdata=None, printlog=False):
        self.http = http
        self.callback = callback  # 回调函数
        self.callback_para = cbdata
        self._msgBuf = []
        self.msgsendleft = None
        self.requestmsg = None
        self.printlog = printlog
        self.try_count = 0  # 尝试的次数。大于一定数量，放弃.
        self.max_try_count = 3
        self._Clean()

    def _Clean(self):
        self.body = cStringIO.StringIO()
        self.headfp = cStringIO.StringIO()
        self.msg = None  # return headmsg
        self.cur_body_size = 0
        self.body_end = False
        self.bReadingBody = False
        self.recv_buf = cStringIO.StringIO()
        self.headmsg = []
        self.status = None
        self.version = None
        self.reason = None
        self.length = None
        self.body_index = 0
        self.header_reading_pos = 0
        self.chunk_left = None
        self.ended = False
        self.sended = False
        self.sendedtime = None
        self.body_2_send = None

    def AddTryCount(self):
        self.try_count += 1

    def GetTryCount(self):
        return self.try_count

    def GetMaxTryCount(self):
        return self.max_try_count

    def SetMaxTryCount(self, x=3):
        self.max_try_count = x

    def SetSended(self, bSend=True):
        self.sended = bSend
        self.sendedtime = game.GetFastTimeInSec()
        # 确认发送完，打一条log. 发送完不等于访问成功。 接收信息在DoCallBack中打印。可以对比调试.
        if bSend and self.printlog:
            print "sended-httprequest. id:", id(self), " msg:", self.requestmsg, " cbpara:", self.callback_para

    def GetSendedTime(self):
        return self.sendedtime

    def IsSended(self):
        return self.sended

    def IsEnded(self):
        return self.sended and self.ended

    # 常用的重载函数， 实现回调
    def OnGetHeaderSucc(self):
        pass

    def OnGetHeaderFailed(self):
        print "get response failed code: %s" % self.status

    # 常用的重载函数， 实现回调
    def OnGetBodySucc(self):
        self.DoCallBack(True)

    def OnGetBodyFailed(self):
        self.DoCallBack(False)

    def OnHttpCallFailed(self):
        self.DoCallBack(False)

    def DoCallBack(self, bSucc):
        if self.printlog:
            try:
                print "got http response. id:", id(self), \
                    "ifSucc:", bSucc, \
                    "status:", self.status, \
                    "requestmsg:", self.requestmsg, \
                    "resultmsg:", self.msg, \
                    "length:", self.length, \
                    "body:", self.body.getvalue(), \
                    "para:", self.callback_para
            except:
                traceback.print_exc()

        if self.callback is None:
            return
        try:
            self.callback(bSucc, self.status, self.msg, self.length, self.body.getvalue(), self.callback_para)
        except:
            print "http回调函数执行异常!"  # 这里拦截异常，是为了保证正常的http read流程不被破坏。
            print self.status, self.requestmsg, self.body.getvalue()
            traceback.print_exc()

    def RecvData(self):
        http = self.http
        result = None
        try:
            result = http.sock.recv(self.READ_SIZE_EACH_TIME)
        except socket.error, err:
            if err[0] == http.GetRecvIgnoreError():
                # print "这个情况可以无视 非阻塞的connect会有这个err"
                pass
            else:
                raise

        if not result:
            raise socket.error("read nothing, maybe server has closed it...")
            return

        self.recv_buf.write(result)

        if not self.bReadingBody:
            self.ReadHeader()

        if self.bReadingBody:
            self.ReadBody()

    def ReadHeader(self):
        self.recv_buf.seek(self.header_reading_pos)
        line = self.recv_buf.readline()
        while line:
            if line == "\r\n":
                self.bReadingBody = True  # end header
                self.body_index = self.recv_buf.tell()
                self.OnHeaderEnd()
                break
            elif line.rfind("\n") >= 0:
                self.AddHeader(line)
                line = self.recv_buf.readline()
            else:
                self.header_reading_pos = self.recv_buf.tell() - len(line)
                print self.header_reading_pos
                break

    def AddHeader(self, line):
        if self.status is None:
            self._read_status(line)
            return
        self.headfp.write(line)

    def PrintHeader(self):
        for hdr in self.msg.headers:
            print "header:", hdr,

    def OnHeaderEnd(self):
        self.headfp.seek(0)
        self.msg = httplib.HTTPMessage(self.headfp)

        # are we using the chunked-style of transfer encoding?
        tr_enc = self.msg.getheader('transfer-encoding')
        if tr_enc and tr_enc.lower() == "chunked":
            self.chunked = 1
            self.chunk_left = None
        else:
            self.chunked = 0

        # do we have a Content-Length?
        # NOTE: RFC 2616, S4.4, #3 says we ignore this if tr_enc is "chunked"
        length = self.msg.getheader('content-length')
        if length and not self.chunked:
            try:
                self.length = int(length)
            except ValueError:
                self.length = None
        else:
            self.length = None

        # does the body have a fixed length? (of zero)
        if (self.status == httplib.NO_CONTENT or self.status == httplib.NOT_MODIFIED or 100 <= self.status < 200):
            self.length = 0

        if self.status == httplib.OK:
            self.OnGetHeaderSucc()
        else:
            self.OnGetHeaderFailed()

    def ReadBody(self):
        if self.length:
            self.ReadContent()
        elif self.chunked:
            self.ReadChunk()
        else:
            self.OnGetBodyFailed()
            self.ended = True
            return

        if self.body_end:
            self.OnGetBodySucc()
            self.ended = True
            return

    def ReadContent(self):
        self.recv_buf.seek(self.body_index)
        nbytes = self.recv_buf.read()
        self.recv_buf.truncate(0)  # body may be very large ,so clear after read buf
        self.body_index = 0

        left_size = self.length - self.cur_body_size
        if len(nbytes) > left_size:
            self.PushBody(nbytes[:left_size])
        else:
            self.PushBody(nbytes)

        if self.cur_body_size == self.length:
            self.body_end = True

    def ReadChunk(self):
        self.recv_buf.seek(self.body_index)
        unprocessed_bytes = None
        while True:
            if self.chunk_left > 0:
                nbytes = self.recv_buf.read(self.chunk_left)
                if nbytes:
                    self.PushBody(nbytes)
                    self.chunk_left -= len(nbytes)
                else:
                    break

            elif self.chunk_left == 0:
                nbytes = self.recv_buf.read(2)  # toss the CRLF at the end of the chunk
                if len(nbytes) == 2:
                    self.chunk_left = None
                else:
                    unprocessed_bytes = nbytes
                    break

            elif self.chunk_left is None:
                line = self.recv_buf.readline()
                if line:
                    if line.rfind("\n") != -1:
                        i = line.find(';')
                        if i >= 0:
                            line = line[:i]  # strip chunk-extensions
                        self.chunk_left = int(line, 16)
                        if self.chunk_left == 0:
                            self.body_end = True
                            return
                    else:
                        unprocessed_bytes = line
                        break
                else:
                    break
            else:
                raise Exception("it's a unknown error!")

        self.recv_buf.truncate(0)  # body may be very large ,so clear after read buf
        self.body_index = 0
        if unprocessed_bytes:
            self.recv_buf.write(unprocessed_bytes)

    def PushBody(self, nbytes):
        self.body.write(nbytes)
        self.cur_body_size += len(nbytes)

    def _read_status(self, line):
        version = None
        status = None
        reason = None
        # Initialize with Simple-Response defaults
        if not line:
            # Presumably, the server closed the connection before
            # sending a valid response.
            raise httplib.BadStatusLine(line)
        try:
            [version, status, reason] = line.split(None, 2)
        except ValueError:
            try:
                [version, status] = line.split(None, 1)
                reason = ""
            except ValueError:
                # empty version will cause next test to fail and status
                # will be treated as 0.9 response.
                version = ""
        if not version.startswith('HTTP/'):
            print repr(line)
            errinfo = "error http status"
            raise socket.error(errinfo)

        # The status code is a three-digit number
        try:
            status = int(status)
            if status < 100 or status > 999:
                raise httplib.BadStatusLine(line)
        except ValueError:
            raise httplib.BadStatusLine(line)

        self.status = status
        self.reason = reason.strip()
        if version == 'HTTP/1.0':
            self.version = 10
        elif version.startswith('HTTP/1.'):
            self.version = 11
        elif version == 'HTTP/0.9':
            self.version = 9
        else:
            raise httplib.UnknownProtocol(version)

    def parse_request(self, method, url, body, headers):
        # honour explicitly requested Host: and Accept-Encoding headers
        self._msgBuf = []
        if headers is None:
            headers = {}
        header_names = dict.fromkeys([k.lower() for k in headers])
        skips = {}
        if 'host' in header_names:
            skips['skip_host'] = 1
        if 'accept-encoding' in header_names:
            skips['skip_accept_encoding'] = 1

        self.putrequest(method, url, **skips)

        if body and ('content-length' not in header_names):
            self.putheader('Content-Length', str(len(body)))
        for hdr, value in headers.iteritems():
            self.putheader(hdr, value)

        if body:
            self.body_2_send = body

        self.endheaders()

    def GetHttpVer(self):
        return self.http._http_vsn

    def putrequest(self, method, url, skip_host=0, skip_accept_encoding=0):
        if not url:
            url = '/'
        s = '%s %s %s' % (method, url, self.http._http_vsn_str)

        self.AddMsg(s)

        if self.GetHttpVer() == 11:
            if not skip_host:
                netloc = ''
                if url.startswith('http'):
                    nil, netloc, nil, nil, nil = httplib.urlsplit(url)

                if netloc:
                    try:
                        netloc_enc = netloc.encode("ascii")
                    except UnicodeEncodeError:
                        netloc_enc = netloc.encode("idna")
                    self.putheader('Host', netloc_enc)
                else:
                    try:
                        host_enc = self.http.host.encode("ascii")
                    except UnicodeEncodeError:
                        host_enc = self.http.host.encode("idna")
                    if self.http.port == self.http.HTTP_PORT:
                        self.putheader('Host', host_enc)
                    else:
                        self.putheader('Host', "%s:%s" % (host_enc, self.http.port))

            if not skip_accept_encoding:
                self.putheader('Accept-Encoding', 'identity')

        else:
            # For HTTP/1.0, the server will assume "not chunked"
            pass

    def putheader(self, header, value):
        s = '%s: %s' % (header, value)
        self.AddMsg(s)

    def AddMsg(self, s):
        self._msgBuf.append(s)

    def endheaders(self):
        self._msgBuf.extend(("", ""))
        msg = "\r\n".join(self._msgBuf)

        if self.body_2_send:
            msg = "%s%s" % (msg, self.body_2_send)

        self.requestmsg = msg
        self.msgsendleft = msg

    def GetMsg2Send(self):
        return self.msgsendleft

    def SetMsg2Send(self, msg):
        self.msgsendleft = msg

    def ResetMsg(self):
        self.msgsendleft = self.requestmsg
        self._Clean()

    def OnGiveUp(self):
        self.status = 400
        self.msg = ""
        self.length = 0
        self.DoCallBack(False)


class CAsyncHttpClientKeepAlive(object):
    _http_vsn = 11
    _http_vsn_str = 'HTTP/1.1'
    HTTP_PORT = 80
    MAX_REQUEST_COUNT_PER_SOCKET = 80  # 一般服务器默认允许一条链接访问100次

    if game.islinux:
        CONNECT_IGNORE_ERROR_4_NONBLOCK = errno.EINPROGRESS
        RECV_IGNORE_ERROR_4_NONBLOCK = errno.EAGAIN
        SERVER_ABORTED = errno.ECONNABORTED

    else:
        CONNECT_IGNORE_ERROR_4_NONBLOCK = errno.WSAEWOULDBLOCK
        RECV_IGNORE_ERROR_4_NONBLOCK = errno.WSAEWOULDBLOCK
        SERVER_ABORTED = errno.WSAECONNABORTED

    def __init__(self, host, port=None):
        self.host = None
        self.port = None
        self.connid = CreateConnId()
        self._set_hostport(host, port)
        self._get_addrinfo()
        self.sock = None
        self._bIsConnecting = False
        self.response_queue = []
        self.netReged = False
        self.max_request_count = self.MAX_REQUEST_COUNT_PER_SOCKET
        self.request_count = 0
        self.timeout = 5  # 5s超时

    def GetDefaultResponseCls(self):
        return CAsyncHttpResponseKeepLive

    def info(self):
        return "httpclient-keepalive. host:%s port:%s connid:%s fileno:%s rcount:%s" % (
        self.host, self.port, self.connid, self.GetFileID(), self.request_count)

    def GetTimeout(self):
        return self.timeout

    def SetTimeout(self, t):
        self.timeout = t

    def Shutdown(self):
        self.CloseSocket()
        self._stop()

    def GetConnectIgnoreError(self):
        return self.CONNECT_IGNORE_ERROR_4_NONBLOCK

    def GetServerAbortedError(self):
        return self.SERVER_ABORTED

    def GetRecvIgnoreError(self):
        return self.RECV_IGNORE_ERROR_4_NONBLOCK

    def request(self, method, url, callback=None, callback_para=None, responsecls=None, body=None, headers=None,
                printlog=False, trycount=3):
        return self.AddRequest(method, url, callback, callback_para, responsecls, body, headers, printlog, trycount)

    def AddRequest(self, method, url, callback, callback_para, responsecls=None, body=None, headers=None,
                   printlog=False, trycount=3):
        if responsecls is None:
            responsecls = self.GetDefaultResponseCls()  # 默认的

        response = responsecls(self, callback, callback_para, printlog)
        response.SetMaxTryCount(trycount)
        response.parse_request(method, url, body, headers)  # 预处理请求， 并保存成要发送的Buf
        self.response_queue.append(response)
        count = len(self.response_queue)
        if count > 100:
            s = "报警！http请求堆积过多！count:%s %s giveup all..." % (count, self.info())
            print s
            try:
                raise Exception(s)
            except:
                traceback.print_exc()
            self.response_queue = [response]
            self.ReStart()
            return response
        else:
            self._start()
            return response

    def _reset(self):
        self._stop()
        if self.response_queue:
            res = self.response_queue[0]
            res.ResetMsg()
            self._start()  # restart

    def _clear(self):
        self.CloseSocket()
        self._reset()

    def _set_hostport(self, host, port):
        if port is None:
            i = host.rfind(':')
            j = host.rfind(']')  # ipv6 addresses have [...]
            if i > j:
                try:
                    port = int(host[i + 1:])
                except ValueError:
                    raise Exception("nonnumeric port: '%s'" % host[i + 1:])
                host = host[:i]
            else:
                port = self.HTTP_PORT
            if host and host[0] == '[' and host[-1] == ']':
                host = host[1:-1]
        self.host = host
        self.port = port

    def _get_addrinfo(self):
        info = dns_cache.GetDnsCache().GetHttpAddrInfo(self.host, self.port)
        if info:
            self.af, self.socktype, self.proto, self.canonname, self.sa = info
        else:
            self.af = self.socktype = self.proto = self.canonname = self.sa = None

    def _start(self):
        self.TryConnect()
        self._RegDrive()

    def _stop(self):
        self._UnRegDrive()

    def TryConnect(self):
        if self.af is None:
            print "http addrinfo is invalid, ignore connect", self.host, self.port
            return

        try:
            if not self._bIsConnecting:
                print "try-httpconnect.... %s" % self.info()
                self.CloseSocket()  # 先关闭sock
                self.sock = socket.socket(self.af, self.socktype, self.proto)
                self.sock.setblocking(0)  # 不阻塞
                self._bIsConnecting = True
                self.sock.connect(self.sa)  # 这步connect必然会有traceback  除非改python源码，否则只能无视了
        except socket.error, err:
            if err[0] == self.GetConnectIgnoreError():
                pass  # print "这个情况可以无视 非阻塞的connect会有这个err"
            else:
                print "httpconnect failed! %s" % self.info()
                self.sock = None
                self._bIsConnecting = False
                raise

    def GetCurResponse(self):
        if self.response_queue:
            return self.response_queue[0]
        return None

    def GetLastResponse(self):
        if self.response_queue:
            return self.response_queue[-1]
        return None

    def GetFileID(self):
        if self.sock:
            return self.sock.fileno()
        return None

    def GetNetDriver(self):
        return netdriver.GetNetDriver()

    def _RegDrive(self):
        if self.netReged:
            return

        if not self.sock:
            print "_start http failed. no socket"
            return

        netDriver = self.GetNetDriver()
        netDriver.RegConn(self)
        netDriver.StartWrite(self)
        self.netReged = True

    def _UnRegDrive(self):
        if self.netReged:
            self.netReged = False
            self.GetNetDriver().UnRegConn(self)

    def ReStart(self):
        self.CloseSocket()
        if self.response_queue:
            res = self.response_queue[0]
            res.ResetMsg()
            self._start()  # restart

    def CloseSocket(self):
        try:
            self._stop()
            if self.sock is not None:
                self.GetNetDriver().UnRegConn(self)
                self.sock.close()
        except:
            import traceback
            traceback.print_exc()
        self.sock = None
        self._bIsConnecting = False

    def Close(self):
        # keep alive, so only unregdrive, not closesocket
        self.Shutdown()

    def OnResposeAllDone(self):
        self._stop()

    def TrySend(self):
        try:
            res = self.SendRequest()
            if res and res.IsSended():
                self.GetNetDriver().StartRead(self)
            if len(self.response_queue) <= 0:
                self.OnResposeAllDone()
        except socket.error, err:
            if err[0] == self.GetServerAbortedError():
                self.OnSocketError("httpserver soft aborted...")
            elif err[0] == errno.EPIPE:
                self.OnSocketError("httpserver disconnected...")
            else:
                self.OnSocketError(err)

        except Exception, err:
            print "sendfailed!. http on tick other error:%s, will reconnect on nexttick %s" % (err, self.info())
            traceback.print_exc()
            self._GiveUpCurRes()
            self.ReStart()  # restart

    def SendRequest(self):
        res = self.GetCurResponse()
        if not res:
            return None

        if res.IsSended():
            return res

        self.SendBuf(res)

        if not res.GetMsg2Send():
            res.SetSended(True)  # send end
        return res

    def SendBuf(self, res):
        msg = res.GetMsg2Send()
        if not msg:
            return
        try:
            byteswritten = self.sock.send(msg)
        except:
            res.ResetMsg()  # send error
            raise

        if byteswritten > 0:
            msgleft = msg[byteswritten:]
            res.SetMsg2Send(msgleft)

    def TryRecv(self):
        try:
            self.ReadResponse()
            if len(self.response_queue) <= 0:
                self.OnResposeAllDone()

        except socket.error, err:
            if err[0] == self.GetServerAbortedError():
                self.OnSocketError("httpserver soft aborted...")
            elif err[0] == errno.EPIPE:
                self.OnSocketError("httpserver disconnected...")
            else:
                self.OnSocketError(err)

        except Exception, err:
            print "readfailed!. http on tick other error:%s, will reconnect on nexttick %s" % (err, self.info())
            traceback.print_exc()
            self._GiveUpCurRes()
            self.ReStart()  # restart

    def OnSocketError(self, msg):
        res = self.GetCurResponse()
        state = "no-res"
        if res:
            res.AddTryCount()
            if res.IsSended():
                state = "read"
            else:
                state = "send"

            if res.GetTryCount() >= res.GetMaxTryCount():
                print "matched max try count. so give up it curres..."
                self._GiveUpCurRes()

        print "httpfailed-%s!. %s  %s" % (state, msg, self.info())
        print "to restart http..."
        self.ReStart()

    def _GiveUpCurRes(self):
        if self.response_queue:
            res = self.response_queue[0]
            del self.response_queue[0]
            print "give up http", res.requestmsg
            res.OnGiveUp()

    def ReadResponse(self):
        if not self.sock:
            print self
            raise Exception("ReadResponse error. sock is null")

        res = self.GetCurResponse()
        if res is None:
            return

        if not res.IsSended():
            print "read http but res is not sended", self
            raise Exception("read http but res is not sended")

        try:
            res.RecvData()
        except:
            raise

        if res.IsEnded():
            del self.response_queue[0]
            self.request_count += 1
            if self.response_queue:
                self.GetNetDriver().StartWrite(self)
