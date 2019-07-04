# coding=utf8


# Copyright (C) [2017] NCSOFT Corporation. All Rights Reserved.
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will NCSOFT Corporation (“NCSOFT”) be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software subject to acceptance
# and compliance with any agreement entered into between NCSOFT (or any of its affiliates) and the recipient.
# The following restrictions shall also apply:
#
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software.
# 2. You may not modify, alter or redistribute this software, in whole or part, unless you are entitled to
# do so by express authorization in a separate agreement between you and NCSOFT.
# 3. This notice may not be removed or altered from any source distribution.


# coding=utf8

from __future__ import unicode_literals

import time

import datetime

day_period = 60 * 60 * 24
week_period = day_period * 7
date_only_format = '%Y%m%d'


# Sun=0,Mon=1,...,Sat=6
def get_weekday(time_check, time_split=0):
    lt = time.localtime(time_check - time_split)
    return (lt.tm_wday + 1) % 7


def get_date(time_check, time_split=0):
    return time.strftime(date_only_format, time.localtime(time_check - time_split if time_check - time_split > 0 else 0))


def get_date_begin_timestamp(time_check, time_split=0):
    return int((time_check - time.timezone - time_split) / day_period) * day_period + time.timezone + time_split


def get_month(time_check, time_split=0):
    return time.strftime('%Y%m', time.localtime(time_check - time_split))


def get_next_date_timestamp(time_check, time_split=0):
    return int((time_check - time.timezone - time_split) / day_period) * day_period \
           + day_period + time.timezone + time_split


def get_next_timestamp(time_check, time_split=0):
    return int((time_check - time.timezone) / day_period) * day_period + time.timezone + time_split


def is_same_date(time_1, time_2, time_split=0):
    return get_date(time_1, time_split) == get_date(time_2, time_split)


def is_same_month(time_1, time_2, time_split=0):
    return get_month(time_1, time_split) == get_month(time_2, time_split)


def count_on_today(utcs, time_check, time_split):
    """
    리셋 시간(time_split)을 기준으로 일자를 구분하여
    time_check 와 '같은' 날에 해당하는 UTC 의 개수를 리턴한다

    :param utcs: UTC list
    :param time_check: timestamp
    :param time_split: timestamp
    :return: time_check 와 같은 리셋 기준일 UTC 원소의 개수
    """

    last_reset_moment = get_next_date_timestamp(time_check - day_period, time_split)

    return len(filter(lambda x: last_reset_moment <= x, utcs))


def get_week_start_timestamp(time_check, time_split=0):
    dt = datetime.datetime.fromtimestamp(time_check).replace(hour=0, minute=0, second=0, microsecond=0)
    monday = dt - datetime.timedelta(days=dt.weekday())
    return int(time.mktime((monday.year, monday.month, monday.day, 0, 0, 0, 0, 0, 0))) + time_split


def get_hour(time_check, time_split=0):
    return time.strftime("%H", time.localtime(time_check - time_split if time_check - time_split > 0 else 0))


def timestamp_to_date(time_check, time_split=0):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_check - time_split if time_check - time_split > 0 else 0))


# modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-20
# detail: 增加时间接口
# >>>>>>>>>>>>>
# 获取N天前的指定0点(time_split)时刻时间戳, before_days = 0表示为当天0点
def get_before_days_timestamp(time_check, before_days, time_split=0):
    if before_days < 0:
        return time_check
    t = int((time_check - time.timezone - time_split) / day_period)
    t -= before_days
    return t * day_period + time.timezone + time_split


def get_week_day_timestamp(time_check, week_day=0, time_split=0):
    """
    获取本周指定天的时间戳
    :param time_check: 指定时间
    :param week_day: 指定天（[0-6], 0:Mon, 6:Sun）
    :param time_split: 分割时间(s)
    :return:
    """
    local_time = time.localtime(time_check - time_split)
    check_time_date_timestamp = get_next_date_timestamp(time_check, time_split) - 86400
    return check_time_date_timestamp + (week_day - local_time.tm_wday) * 86400


# 获得time_check时间戳 当天 time_split 点的时间戳
def get_today_hour_timestamp(time_check, time_split=0):
    return int((time_check - time.timezone) / day_period) * day_period + time.timezone + time_split


# 获得time_check对应当天经过的秒数(以time_split为跨天点)
def get_day_seconds(time_check, time_split=0):
    normal_sec = (time_check - time.timezone) % day_period
    return normal_sec - time_split if normal_sec >= time_split else normal_sec - time_split + day_period


def is_weekend(time_check, time_split=0):
    week_day = get_weekday(time_check, time_split)
    return week_day == 0 or week_day == 6
# <<<<<<<<<<<<<
