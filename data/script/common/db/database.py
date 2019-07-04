# coding=utf8

from __future__ import unicode_literals

import script.common.log as logger
from script.common.config.config import conf as common_config

_db_connector = None

_db_game = None
_db_mail = None
_db_clan = None
_db_battle_field = None
_db_friend = None
_db_invest = None
_db_user = None
# modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-06-14
# detail: 增加db接口
# >>>>>>>>>>>>>
_db_admin = None
_db_chat = None
_db_leaderboard = None
_db_team = None
_db_storage_srv = None
# <<<<<<<<<<<<<


def create_db_connector(use_gevent):
    global _db_connector

    if use_gevent:
        from couchbase import experimental

        experimental.enable()
        from gcouchbase.connection import GConnection

        _db_connector = GConnection
    else:
        from couchbase import Couchbase

        _db_connector = Couchbase.connect

    return _db_connector


def reset_db_obj():
    global _db_game
    global _db_mail
    global _db_clan
    global _db_battle_field
    global _db_friend
    global _db_invest
    global _db_user
    # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-06-14
    # detail: 增加db接口
    # >>>>>>>>>>>>>
    global _db_admin
    global _db_chat
    global _db_leaderboard
    global _db_team
    global _db_storage_srv
    # <<<<<<<<<<<<<

    _db_game = None
    _db_mail = None
    _db_clan = None
    _db_battle_field = None
    _db_friend = None
    _db_invest = None
    _db_user = None
    # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-06-14
    # detail: 增加db接口
    # >>>>>>>>>>>>>
    _db_admin = None
    _db_chat = None
    _db_leaderboard = None
    _db_team = None
    _db_storage_srv = None
    # <<<<<<<<<<<<<


def db_game():
    global _db_game

    if not _db_game:
        logger.GetLog().info('DB:game:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_game = _db_connector(bucket=common_config.get_bucket_name('game'), host=common_config.couchbase_host_game)

    return _db_game


def db_mail():
    global _db_mail

    if not _db_mail:
        logger.GetLog().info('DB:mail:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_mail = _db_connector(bucket=common_config.get_bucket_name('mail'), host=common_config.couchbase_host_game)

    return _db_mail


def db_clan():
    global _db_clan

    if not _db_clan:
        logger.GetLog().info('DB:clan:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_clan = _db_connector(bucket=common_config.get_bucket_name('clan'), host=common_config.couchbase_host_game)

    return _db_clan


def db_battle_field():
    global _db_battle_field

    if not _db_battle_field:
        logger.GetLog().info('DB:battle_field:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_battle_field = _db_connector(bucket=common_config.get_bucket_name('battle_field'), host=common_config.couchbase_host_game)

    return _db_battle_field


def db_friend():
    global _db_friend

    if not _db_friend:
        logger.GetLog().info('DB:friend:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_friend = _db_connector(bucket=common_config.get_bucket_name('friend'), host=common_config.couchbase_host_game)

    return _db_friend


def db_invest():
    global _db_invest

    if not _db_invest:
        logger.GetLog().info('DB:invest:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_invest = _db_connector(bucket=common_config.get_bucket_name('invest'), host=common_config.couchbase_host_game)

    return _db_invest


def db_user():
    global _db_user

    if not _db_user:
        logger.GetLog().info('DB:user:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_user = _db_connector(bucket=common_config.get_bucket_name('user'), host=common_config.couchbase_host_game)

    return _db_user


# modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-06-14
# detail: 增加db接口
# >>>>>>>>>>>>>
def db_admin():
    global _db_admin

    if not _db_admin:
        logger.GetLog().info('DB:admin:Connecting: {0}'.format(common_config.couchbase_host_util))
        _db_admin = _db_connector(bucket=common_config.get_bucket_name('admin'), host=common_config.couchbase_host_util)

    return _db_admin


def db_chat():
    global _db_chat
    if not _db_chat:
        logger.GetLog().info('DB:chat:Connecting: {0}'.format(common_config.couchbase_host_util))
        _db_chat = _db_connector(bucket=common_config.get_bucket_name('chat'), host=common_config.couchbase_host_util)

    return _db_chat


def db_leaderboard():
    global _db_leaderboard
    if not _db_leaderboard:
        logger.GetLog().info('DB:leaderboard:Connecting: {0}'.format(common_config.couchbase_host_util))
        _db_leaderboard = _db_connector(bucket=common_config.get_bucket_name('leaderboard'), host=common_config.couchbase_host_util)
    return _db_leaderboard


def db_team():
    global _db_team
    if not _db_team:
        logger.GetLog().info('DB:team:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_team = _db_connector(bucket=common_config.get_bucket_name('team'), host=common_config.couchbase_host_game)
    return _db_team


def db_storage_srv():
    global _db_storage_srv
    if not _db_storage_srv:
        logger.GetLog().info('DB:storage_srv:Connecting: {0}'.format(common_config.couchbase_host_game))
        _db_storage_srv = _db_connector(bucket=common_config.get_bucket_name('storage_srv'), host=common_config.couchbase_host_game)
    return _db_storage_srv

# <<<<<<<<<<<<<

create_db_connector(False)
