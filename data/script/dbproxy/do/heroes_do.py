# coding=utf8

from __future__ import unicode_literals
from script.common.db.class_obj import ClassObject, String, List, Dict, Integer
from script.common.db.database import db_game
from script.common.db.base_do import BaseDo


class Heroes(ClassObject):
    user_id = String(desc='히어로를 소유한 유저의 id')

    active = String(desc='현재 선택된 디폴트 히어로. 히어로의 class_key.')
    heroes = List(String(), desc='히어로 목록. [영웅 class_key, ...]')
    skins = Dict(Dict(Integer()), desc="英雄皮肤")	#add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-07-19 for 英雄装备服装，不存在英雄时临时保存


class HeroesDo(BaseDo):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(HeroesDo, self).__init__(context, user_id)

        self.doc.user_id = user_id

    @classmethod
    def cls(cls):
        return Heroes

    @classmethod
    def get_prefix(cls):
        return 'USRHEROES'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

