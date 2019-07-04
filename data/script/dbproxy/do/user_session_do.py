# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import ServerIndependantUnlockDoBase
from script.common.db.class_obj import ClassObject, String, Boolean, Integer, Dict
from script.common.db.database import db_user


class UserSession(ClassObject):
    session_id = String(desc='세션의 인스턴스 id')
    user_id = String(desc='유저 id')
    platform = String(desc='접속 장비의 플랫폼. ex. aos, ios')
    server_selected = String(desc='입장 선택한 서버')
    server_group = String(desc='입장서버에 따라 그룹으로 묶인 서버')
    created = Boolean(default=False, desc='기사단 생성 여부')
    block_status = Integer(default=0, desc='유저 블록 상태. 0 : 블록 아님, 1: 정해진 기간, 2: 영구 블록')
    block_expiry_time = Integer(default=0, desc='블록 만료 시간. utc')

    time_last_request = Integer(default=0, desc='마지막 요청을 보낸 시간. utc')
    time_last_login = Integer(default=0, desc='마지막으로 로그인 성공한 시간. utc')
    country = String(desc='유저의 국가 코드. KR/JP/... 클라에서 보낸 값')
    np_id = String(desc='플랫폼 np id. 플랫폼에서는 GUID 라고도 부름')

    server_user_id_migration = Dict(Integer(), desc='서버통합 데이터로 마이그레이션 된 시각 UTC')

    aofei_account_id = String(desc='account id')
    aofei_account_name = String(desc='account name')
    last_operation = String(desc='last operation')


class UserSessionDo(ServerIndependantUnlockDoBase):
    def __init__(self, context, account_id):
        super(UserSessionDo, self).__init__(context, account_id)

        self.doc.user_id = account_id
        self.doc.aofei_account_id = account_id

    @classmethod
    def cls(cls):
        return UserSession

    @classmethod
    def get_prefix(cls):
        return 'USRSESSION'

    @classmethod
    def get_db(cls):
        return db_user()
