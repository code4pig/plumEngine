# -*- coding:utf8 -*-

from __future__ import unicode_literals

import abc


class BattleHandlerBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def init_battle(self, *args):
        """
        初始化战斗
        :param args: 参数
        :return:
        """
        pass

    @abc.abstractmethod
    def handle_battle_msg(self, server_user_id, cmd, msg):
        """
        处理战斗消息
        :param server_group_id: server group id
        :param server_user_id: server user id
        :param battle_unique_id: 战斗唯一id
        :param cmd: 协议
        :param msg: 战斗消息数据
        :return: 是否结束
        """
        return False

    @abc.abstractmethod
    def handle_sec_timer(self, current_time):
        """
        处理定时器逻辑
        :param current_time:
        :return: 是否结束
        """
        return False

    @abc.abstractmethod
    def handle_db_callback(self, handle_flag, *args):
        """
        处理db回调
        :param handle_flag: 操作类型
        :param args: 返回数据
        :return:
        """
        pass

    @abc.abstractmethod
    def handle_user_leave(self, server_user_id):
        """
        处理玩家离开
        :return:
        """
        pass

