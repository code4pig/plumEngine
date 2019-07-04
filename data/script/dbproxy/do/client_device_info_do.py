# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String
from script.common.db.database import db_game
from script.common.db.base_do import ServerIndependantUnlockDoBase


class ClientDeviceInfo(ClassObject):
    ip = String(default='0.0.0.0', desc='ip')
    device_model = String(default='Unknown', desc='设备型号')
    os_name = String(default='ios', desc='os name')
    os_ver = String(default='0.0', desc='os version')
    os_id = String(default='0', desc='group id')
    mac_addr = String(default='00:00:00:00:00:00', desc='mac addr')
    device_uid = String(default='Unknown', desc='设备唯一标识')
    channel_name = String(default='Unknown', desc='渠道名')
    channel_id = String(default='0', desc='渠道id')
    app_ver = String(default='0.0', desc='app version')
    net_work = String(default='Unknown', desc='network')
    device_screen = String(default='Unknown', desc='屏幕分辨率')
    platform_tag = String(default='aofei', desc='发行tag')
    network_operators = String(default='Unknown', desc='运营商')


class ClientDeviceInfoDo(ServerIndependantUnlockDoBase):
    def __init__(self, context, account_id):
        super(ClientDeviceInfoDo, self).__init__(context, account_id)

    @classmethod
    def cls(cls):
        return ClientDeviceInfo

    @classmethod
    def get_prefix(cls):
        return 'CLIENTDEVICEINFO'

    @classmethod
    def get_db(cls):
        return db_game()

    def update_client_device_info(self, info):
        self.doc = info
        self.update()
