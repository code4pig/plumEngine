# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Dict


# 公会相关
class Clan(ClassObject):
    clan_id = String(desc='公会id')
    name = String(desc='公会名')
    member_list = Dict(Integer(), desc='成员列表')


class UserClanInfo(ClassObject):
    user_id = String(desc='角色id')
    clan_id = String(desc='公会id')
