# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import time

from script.common.db.game_log_formatter import func_factory
from script.dbproxy.do.alpha_fluentd_logger import alpha_fluentd_logger_inst
from script.dbproxy.do.client_device_info_do import ClientDeviceInfoDo
from script.common.db.instant_box import instant_box
from script.common.db.game_log_def import GameLogFieldName


class GameLogger(object):
    def __init__(self):
        self.params = {}
        self.account_id = None
        self.operation = None

    def update_date_param(self, params):
        dt = time.localtime(instant_box.time_current)
        params[GameLogFieldName.log_ymd] = str(dt.tm_year * 10000 + dt.tm_mon * 100 + dt.tm_mday)
        params[GameLogFieldName.log_ym] = str(dt.tm_year * 100 + dt.tm_mon)
        params[GameLogFieldName.year] = str(dt.tm_year)
        params[GameLogFieldName.month] = str(dt.tm_mon)
        params[GameLogFieldName.day] = str(dt.tm_mday)
        params[GameLogFieldName.hour] = str(dt.tm_hour)
        params[GameLogFieldName.minute] = str(dt.tm_min)
        params[GameLogFieldName.week] = time.strftime('%W', dt)

    def log(self, account_id, operation, params):
        self.update_date_param(params)
        if account_id:
            client_device_info_do = ClientDeviceInfoDo(instant_box.data_context, account_id)
            # params.update(client_device_info_do.doc.dump())
            params[GameLogFieldName.ip] = client_device_info_do.doc.ip
            params[GameLogFieldName.device_model] = client_device_info_do.doc.device_model
            params[GameLogFieldName.os_name] = client_device_info_do.doc.os_name
            params[GameLogFieldName.os_ver] = client_device_info_do.doc.os_ver
            params[GameLogFieldName.group_id] = client_device_info_do.doc.os_id
            params[GameLogFieldName.mac_addr] = client_device_info_do.doc.mac_addr
            params[GameLogFieldName.udid] = client_device_info_do.doc.device_uid
            params[GameLogFieldName.app_channel] = client_device_info_do.doc.channel_name
            params[GameLogFieldName.channel_id] = client_device_info_do.doc.channel_id
            params[GameLogFieldName.app_ver] = client_device_info_do.doc.app_ver
            params[GameLogFieldName.network] = client_device_info_do.doc.net_work
            params[GameLogFieldName.device_screen] = client_device_info_do.doc.device_screen
            params[GameLogFieldName.platform_tag] = client_device_info_do.doc.platform_tag

        # 调用格式化函数,直接转换为字符串
        date_str = self.get_log_date(instant_box.time_current, '{0:04d}_{1:02d}_{2:02d}')
        log_str = func_factory.get(operation)(params)
        server_id = '1001' if not instant_box.server_selected else instant_box.server_selected
        alpha_fluentd_logger_inst.bi(date_str, server_id, operation, log_str)

    def start_log(self, account_id, operation):
        self.params = {}
        self.account_id = account_id
        self.operation = operation

    def push_log_param(self, key, value):
        if isinstance(value, (str, unicode)):
            self.params[key] = value
        else:
            self.params[key] = str(value)

    def end_log(self):
        if self.account_id and "pvprobot" in self.account_id:   # 屏蔽竞技场机器人
            return
        self.log(self.account_id, self.operation, self.params)

    @staticmethod
    def get_log_date(timestamp, date_format='{0:04d}{1:02d}{2:02d}'):
        dt = time.localtime(timestamp)
        return date_format.format(dt.tm_year, dt.tm_mon, dt.tm_mday)


game_logger_inst = GameLogger()


