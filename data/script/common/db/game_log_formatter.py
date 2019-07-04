# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.game_log_def import GameLogFieldName


class GameLogFormatFunFactory(object):
    def __init__(self):
        self.format_func_dict = {}

    def get(self, operation):
        return self.format_func_dict[operation]

    def register(self, operation, func):
        self.format_func_dict[operation] = func


func_factory = GameLogFormatFunFactory()


class LogFormatterFunc(object):
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, func):
        func_factory.register(self.operation, func)

        print u'log formatter function register :', self.operation, func.__name__
        return func


@LogFormatterFunc('Activation')
def format_log_str_activation(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.active_time, '0'))])


@LogFormatterFunc('LoginUI')
def format_log_str_login_ui(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reach_login_time, '0'))])


@LogFormatterFunc('Update')
def format_log_str_update(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reach_update_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.update_status, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.update_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.use_time, '0'))])


@LogFormatterFunc('Identification')
def format_log_str_identification(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reach_login_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, ''))])


@LogFormatterFunc('CreateRole')
def format_log_str_create_role(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.create_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_job, '0'))])


@LogFormatterFunc('LoadinUI')
def format_log_str_loadin_ui(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.activate_game_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reach_game_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.load_time_long, '0'))])


@LogFormatterFunc('OnlineRoleNum')
def format_log_str_online_role_num(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.online, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.online_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.ip_online_num, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, ''))])


@LogFormatterFunc('LoginRole')
def format_log_str_login_role(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_screen, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.create_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_job, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.login_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.last_logout_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.offline_item, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.total_pay, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.vip_level, ''))])


@LogFormatterFunc('LogoutRole')
def format_log_str_logout_role(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network_operators, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_screen, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.create_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_job, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.exp, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.logout_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.online_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.scene, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.last_operation, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.total_pay, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.vip_level, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.total_time, ''))])


@LogFormatterFunc('ItemBuy')
def format_log_str_item_buy(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.mall_source, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_type, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.buy_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.expire_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.price, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.huobi_type, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.use_huobi, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.left_huobi, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.create_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.total_pay, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.vip_level, ''))])


@LogFormatterFunc('Tutorial')
def format_log_str_tutorial(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.tutorial_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.tutorial_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.begin_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.begin_role_level, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.use_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.step_type, '0'))])


@LogFormatterFunc('Chat')
def format_log_str_chat(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.content, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.scene, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.chat_time, '0'))])


@LogFormatterFunc('ActorExpChange')
def format_log_str_actor_exp_change(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_role_level, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.get_actor_exp, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.total_actor_exp, '0'))])


@LogFormatterFunc('HeroCreate')
def format_log_str_hero_create(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_option, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0'))])


@LogFormatterFunc('HeroChanged')
def format_log_str_hero_changed(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_h_lv, '0'))])


@LogFormatterFunc('SkillUp')
def format_log_str_skill_up(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_s_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.skill_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.use_gold, '0'))])


@LogFormatterFunc('ExpChange')
def format_log_str_exp_change(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_exp, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.get_exp, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_exp, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.full_exp, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0'))])


@LogFormatterFunc('GetTransform')
def format_log_str_get_transform(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.transform_key, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.trans_stren_key, ''))])


@LogFormatterFunc('TransformChanged')
def format_log_str_transform_changed(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_transform_key, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_trans_stren_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_transform_key, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_trans_stren_key, ''))])


@LogFormatterFunc('TransformLvUp')
def format_log_str_transform_lv_up(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.transform_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_trans_stren_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_trans_stren_key, ''))])


@LogFormatterFunc('SummonGet')
def format_log_str_summon_get(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.nor_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.su_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_xl_lv, ''))])


@LogFormatterFunc('SummonSx')
def format_log_str_summon_sx(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.su_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_xl_lv, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, ''))])


@LogFormatterFunc('SummonXl')
def format_log_str_summon_xl(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.nor_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.su_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_xl_lv, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_xl_lv, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.skill_id, ''))])


@LogFormatterFunc('SummonWishUp')
def format_log_str_summon_wish_up(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.nor_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_bless_exp, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_bless_exp, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_xl_lv, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, ''))])


@LogFormatterFunc('SummonDestiny')
def format_log_str_summon_destiny(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.nor_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.su_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_xl_lv, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.destiny_type, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.destiny_index, '0'))])


@LogFormatterFunc('SummonCostumeBuy')
def format_log_str_summon_costume_buy(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.costume_id, ''))])


@LogFormatterFunc('SummonCostumeUse')
def format_log_str_summon_costume_use(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.s_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.nor_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.su_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.s_xl_lv, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_costume_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_costume_id, ''))])


@LogFormatterFunc('QuestComplete')
def format_log_str_quest_complete(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hero_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.quest_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.quest_id, ''))])


@LogFormatterFunc('AttendReward')
def format_log_str_attend_reward(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.attend_times, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.event, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.event_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.get_item, ''))])


@LogFormatterFunc('Mail')
def format_log_str_mail(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.send_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mail_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.runout_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.activate_time, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.mail_item, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mail_content, ''))])


@LogFormatterFunc('Friend')
def format_log_str_friend(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.action, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.friend_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.other_role_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.other_role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.other_clan_id, ''))])


@LogFormatterFunc('IncreaseAP')
def format_log_str_increase_ap(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_ap_data, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reason_detail, ''))])


@LogFormatterFunc('DecreaseAP')
def format_log_str_decrease_ap(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_ap_data, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reason_detail, ''))])


@LogFormatterFunc('MoneyChang')
def format_log_str_money_chang(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.money_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.chang_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_money_data, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_money_data, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.reason_detail, ''))])


@LogFormatterFunc('ItemChang')
def format_log_str_item_chang(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_up, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.chang_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_money_data, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.reason_detail, ''))])


@LogFormatterFunc('Gacha')
def format_log_str_gacha(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.gacha_code, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.gacha_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.mileage, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cost, '0'))])


@LogFormatterFunc('StageStar')
def format_log_str_stage_star(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.section_key, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.get_item, ''))])


@LogFormatterFunc('EquipItem')
def format_log_str_equip_item(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.equip_type, '0'))])


@LogFormatterFunc('DecomposeItem')
def format_log_str_decompose_item(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.decompose, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.gauge, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.critical, ''))])


@LogFormatterFunc('DigestionResult')
def format_log_str_digestion_result(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.zuanshi_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.gauge, '0'))])


@LogFormatterFunc('ManufactureItem')
def format_log_str_manufacture_item(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.option, ''))])


@LogFormatterFunc('ManufactureMaterial')
def format_log_str_manufacture_material(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_item_data, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.recipe_id, '0'))])


@LogFormatterFunc('ConvertItemOption')
def format_log_str_convert_item_option(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.option_type, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_option, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_option, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_option, ''))])


@LogFormatterFunc('ConvertMaterial')
def format_log_str_convert_material(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.a_item_data, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_key, ''))])


@LogFormatterFunc('EnchantItem')
def format_log_str_enchant_item(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_uid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.item_grade, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.item_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.new_item_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.enchant_type, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.enchant_result, ''))])


@LogFormatterFunc('StartPveStage')
def format_log_str_start_pve_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.actor_exp, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.b_ap, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_ap, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.summon_1, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.summon_2, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.summon_3, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.summon_4, ''))])


@LogFormatterFunc('EndPveStage')
def format_log_str_end_pve_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.actor_exp, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.get_star, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.sendtime, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_ap, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_ap, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.summon_1, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.summon_2, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.summon_3, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.summon_4, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_live, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_dead, '0'))])


@LogFormatterFunc('EventInPveStage')
def format_log_str_event_in_pve_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.event_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.boss_lv, '0'))])


@LogFormatterFunc('SweepResult')
def format_log_str_sweep_result(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.sweep_times, '0'))])


@LogFormatterFunc('StartOmanStage')
def format_log_str_start_oman_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.stage_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.boss_remain_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_remain_hp, '0'))])


@LogFormatterFunc('EndOmanStage')
def format_log_str_end_oman_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.stage_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.usecount, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.surpluscount, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.usetime, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_live, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_dead, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.boss_remain_time, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_remain_hp, '0'))])


@LogFormatterFunc('FindOmanBoss')
def format_log_str_find_oman_boss(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.set_stage, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.boss_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_remain_time, '0'))])


@LogFormatterFunc('StartWorldBossRaid')
def format_log_str_start_world_boss_raid(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.raid_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.raid_seq, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.use_ap, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.surplus_ap, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.surplustime, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.part_key, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.detail_boss_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.boss_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_hp, ''))])


@LogFormatterFunc('EndWorldBossRaid')
def format_log_str_end_world_boss_raid(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.raid_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.raid_seq, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.damage, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.surplustime, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_live, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.auto, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.usetime, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.part_key, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.detail_boss_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.boss_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.boss_hp, ''))])


@LogFormatterFunc('StartTodayStage')
def format_log_str_start_today_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, ''))])


@LogFormatterFunc('EndTodayStage')
def format_log_str_end_today_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.stage_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.difficulty, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.bonus_step, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.get_star, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.usetime, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_live, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_dead, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.team, ''))])


@LogFormatterFunc('EndPvpAttackStage')
def format_log_str_end_pvp_attack_stage(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_rank, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_rank, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_rank, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_server, '0'))])


@LogFormatterFunc('EndPvpArenaAttack')
def format_log_str_end_pvp_arena_attack(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.b_rank, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.a_rank, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.count, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.season, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.getpoint, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.winning_streak, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_server, '0'))])


@LogFormatterFunc('UseComrade')
def format_log_str_use_comrade(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_item, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.place, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.peer_role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.peer_role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.peer_team, ''))])


@LogFormatterFunc('StartExplore')
def format_log_str_start_explore(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.send_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.cost_cloak, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cloak_summon_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, ''))])


@LogFormatterFunc('EndExplore')
def format_log_str_end_explore(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_key, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.send_time, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, ''))])


@LogFormatterFunc('FieldAttackResult')
def format_log_str_field_attack_result(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.block_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.field_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.get_point, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.all_point, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_name, ''))])


@LogFormatterFunc('FieldDefenseSetting')
def format_log_str_field_defense_setting(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.block_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.field_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.block_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.help_power, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hero_power, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.help_count, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.block_role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.block_role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0'))])


@LogFormatterFunc('FieldDefenseGiveUp')
def format_log_str_field_defense_give_up(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.block_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.block_type, '0'))])


@LogFormatterFunc('FortBuild')
def format_log_str_fort_build(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.block_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.fort_count, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.fort_role_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.fort_role_name, ''))])


@LogFormatterFunc('FortSiegeStart')
def format_log_str_fort_siege_start(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.block_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.field_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.team, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0'))])


@LogFormatterFunc('FortSiegeResult')
def format_log_str_fort_siege_result(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_dbid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.end_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.block_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.field_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.point, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.rival_role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0'))])


@LogFormatterFunc('CreateGuild')
def format_log_str_create_guild(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.cost_item, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.all_item, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_id, ''))])


@LogFormatterFunc('GuildJoin')
def format_log_str_guild_join(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.join_type, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_id, ''))])


@LogFormatterFunc('GuildExpChange')
def format_log_str_guild_exp_change(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.role_name, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_level, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.h_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.h_lv, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.reason, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.join_type, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_lv, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.clan_exp, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.clan_exp_all, ''))])


@LogFormatterFunc('CgBegin')
def format_log_str_cg_begin(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, ''))])


@LogFormatterFunc('CgEnd')
def format_log_str_cg_end(log_dict):
    return ','.join(['"{0}"'.format(log_dict.get(GameLogFieldName.log_ymd, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.log_ym, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.year, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.month, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.day, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.hour, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.minute, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.week, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.ip, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.device_model, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.os_name, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.os_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.mac_addr, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.udid, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.app_channel, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.app_ver, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.network, '')), '"{0}"'.format(log_dict.get(GameLogFieldName.platform_tag, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.group_id, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.channel_id, '0')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.server, '0')), '"{0}"'.format(log_dict.get(GameLogFieldName.account_id, '')),
                     '"{0}"'.format(log_dict.get(GameLogFieldName.role_id, ''))])
