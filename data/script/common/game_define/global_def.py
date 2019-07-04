# coding=utf8

from __future__ import unicode_literals

from script.common.game_define.util import enum
from script.common import exceptions as excp

name_migration_dt = 1493082000
enum_server_user_id = enum('SERVER', 'USER', 'SEQ')


def make_server_user_id(server_id, user_id, seq=0):
    if server_id:
        return '_'.join([server_id, user_id, str(seq)])
    else:
        raise excp.ExceptionInvalidServer('None')


def get_user_id(server_user_id):
    return server_user_id.split('_')[enum_server_user_id.USER]


def get_server_id(server_user_id):
    return server_user_id.split('_')[enum_server_user_id.SERVER]


def get_server_user_seq(server_user_id):
    return int(server_user_id.split('_')[enum_server_user_id.SEQ])


def get_server_and_user_id(server_user_id):
    server_user_id_seq = server_user_id.split('_')

    if len(server_user_id_seq) != 3:
        raise excp.ExceptionInvalidServerUserId(server_user_id)

    return server_user_id_seq[enum_server_user_id.SERVER], server_user_id_seq[enum_server_user_id.USER]


def get_server_user_id_seq(server_user_id):
    return server_user_id.split('_')


def get_clan_server_id(clan_id):
    return clan_id.split('-')[1]


def is_server_user_id(server_user_id):
    if not server_user_id:
        return False

    if len(server_user_id.split('_')) == 3:
        return True
    else:
        return False


def is_clan_id(unknown_id):
    if not unknown_id:
        return False

    if len(unknown_id.split('-')) == 3:
        return True
    else:
        return False

server_group_map = {
    "11001": ['1001'],
    "11002": ['1002'],
}


# modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-10-23
# detail: 合并1.2.1代码后调整，修改服务器和服务器组映射逻辑
# >>>>>>>>>>>>>
def get_server_group_id(server_id):
    for group_id, server_list in server_group_map.iteritems():
        if server_id in server_list:
            return group_id
    raise excp.ExceptionInvalidServerGroupId(server_id)
# <<<<<<<<<<<<<


# modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-10-23
# detail: 合并1.2.1代码后调整，增加服务器组下服务器列表的接口
# >>>>>>>>>>>>>
def get_server_list_in_group(server_group_id):
    if server_group_id in server_group_map:
        return server_group_map[server_group_id]
    else:
        raise excp.ExceptionInvalidServerGroupId(server_group_id)
# <<<<<<<<<<<<<


