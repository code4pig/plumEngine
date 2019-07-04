# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-06-14 12:14

from __future__ import unicode_literals

import uuid
import script.common.log as logger

from fluent import sender
from fluent import event
from script.common.config.config import conf as common_config


def buffer_overflow_handler(pending_events):
    buffer_clear = False
    try:
        sender.get_global_sender()._send_data(pending_events)

        buffer_clear = True
    except:
        pass
    finally:
        pass

    if not buffer_clear:
        f = None
        try:
            if not common_config.debug:
                f = open("./pending_{0}.bin".format(uuid.uuid4().hex), 'wb')
                f.write(pending_events)
        except:
            pass
        finally:
            if f:
                f.close()


class AlphaFluentdLogger(object):
    def __init__(self):
        sender.setup('rk', host=common_config.fluentd_host, port=common_config.fluentd_port, bufmax=5 * 1024 * 1024, timeout=5.0,
                     verbose=False, buffer_overflow_handler=buffer_overflow_handler)

        self.root_dir = common_config.bi_root_path
        self.zone = common_config.zone

    @classmethod
    def send_retry(cls, try_count=1, make_file=False):
        global_sender = sender.get_global_sender()
        if global_sender.pendings:
            buffer_clear = False
            for i in xrange(try_count):
                try:
                    global_sender.lock.acquire()
                    global_sender._send_data(global_sender.pendings)
                    global_sender.pendings = None
                    buffer_clear = True
                    break
                except Exception as e:
                    logger.GetLog().error('=====[ERROR]===== sender data to fluentd error :', e, e.message, global_sender.pendings)
                finally:
                    global_sender.lock.release()
            if make_file:
                if not buffer_clear:
                    f = None
                    try:
                        if not common_config.debug:
                            f = open("./restart_{0}.bin".format(uuid.uuid4().hex), 'wb')
                            f.write(sender.get_global_sender().pendings)
                    except:
                        pass
                    finally:
                        if f:
                            f.close()

    def bi(self, date, server_id, operation, str_data):
        # 内部会调用到emit函数
        event.Event('bi.' +
                    self.root_dir + '.' +
                    self.zone + "." +
                    date + '.' +
                    server_id + '.' +
                    operation,
                    {'bi_log': str_data})
        # 尝试重发(如果event.Event中没能发送成功的)
        self.send_retry()

alpha_fluentd_logger_inst = AlphaFluentdLogger()
