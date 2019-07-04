# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-06-19 15:25


class Config(object):
    # db host
    couchbase_host_game = ['192.168.26.56']
    couchbase_host_util = ['192.168.26.56']

    # 增加db bucket名称后缀，方便创建不同服bucket
    bucket_postfix = __name__.split('.')[-1]

    # bi log dir
    bi_root_path = '/data/game_bi_log'
    fluentd_host = 'localhost'
    fluentd_port = 24224
