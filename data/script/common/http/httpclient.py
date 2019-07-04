# -*- coding: utf8 -*-
"""
非阻塞httpclient短连接.
"""

from script.common.http.httpclient_keepalive import CAsyncHttpClientKeepAlive


class CAsyncHttpClientOnce(CAsyncHttpClientKeepAlive):
    # override parent
    # 成功处理完所有的http就就关闭socket
    def OnResposeAllDone(self):
        self.Shutdown()
