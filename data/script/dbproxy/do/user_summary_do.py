# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-08-14 14:52

from __future__ import unicode_literals


from script.common.db.database import db_game
from script.common.db.base_do import UnlockedDoBase
from script.common.db.class_obj import ClassObject, String, Integer


class UserSummary(ClassObject):
    user_id = String(desc='유져 id', default=None)
    server_user_id = String(desc='server_user_id')
    social_id = String(desc='유저의 소셜 id. plaync.co.kr 등등. 로그인 시에 설정된다')
    user_nickname = String(desc='유져 nickname', default=None)
    user_lv = Integer(desc='기사단 레벨', default=None)
    selected_hero_class_key = String(desc='활성화된 영웅 class key', default=None)
    selected_hero_lv = Integer(desc='활성화된 영웅의 Lv', default=None)
    clan_id = String(desc='가입 혈맹 아이디', default=None)
    clan_name = String(desc='가입 혈맹 이름', default=None)
    clan_role = String(desc='가입 혈맹 직책', default=None)


class UserSummaryDo(UnlockedDoBase):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        self.user_id = user_id

        super(UserSummaryDo, self).__init__(context, user_id)

        self.doc.user_id = user_id

    @classmethod
    def cls(cls):
        return UserSummary

    @classmethod
    def get_prefix(cls):
        return 'USRSUMMARY'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id
