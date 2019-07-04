# coding=utf8
from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.class_obj import *
from script.common.db.database import db_user
from script.dbproxy.do.masters_global import master_user_level_inst


class User(ClassObject):
    user_id = String(desc='유저 id')
    server_user_id = String(desc='server_user_id')

#>>>add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-27 for 奥飞账号
    aofei_account_id = String(desc='账号ID')
    aofei_account_name = String(desc='账号昵称')
#<<<add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-27 for 奥飞账号

    name = String(required=True, desc='유저이름')
    asset = Dict(Integer(), desc='자산. 아데나/다이아몬드/배틀코인. {아이템 key: 보유 수량, ...}')
    exp = Integer(default=0, desc='마스터 레벨의 누적 경험치')

    time_created = Integer(desc='유저 계정 생성 시간')
    ap = Integer(default=0, desc='행동력. 실제 ap = ap + ap_timestamp 이후 재생한 ap')
    ap_timestamp = Integer(default=0, desc='ap 재생 기준 시각. utc. seconds from 1970-01-01 09:00:00.')

    guild_id = String(desc='길드 id')
    chaotic = Integer(default=0, desc='성향치')

    # hero_dice = Integer(desc='영웅 생성 시 추가 스탯 주사위값. 주사위를 굴릴때마다 값을 저장. 임시값')

    phase_event_cooldown = Dict(Integer(), desc='이동이벤트 쿨다운 목록. {이벤트 키: 쿨 만료 시각. utc, ...}')
    phase_event_merchant_open = Boolean(desc='이동이벤트 암상인 롤코 만났는지 여부. 스토리 전달.')

    transform = Dict(List(String()), desc='구매한 변신 자격. {바슈: [부자왕, 광개토대왕], 애슐리: [..]..}')

    tutorial = List(String(), desc='완료한 튜토리얼 내역. 튜토리얼 키 리스트')
    unlocked = List(String(), desc='오픈된 컨텐츠의 키 리스트')

    mail_sent_2 = Dict(Integer(), desc='{공지로 보낸 메일들의 키: expired dt, ...')
    done_event = Dict(Integer(), desc='{이벤트 키: expired dt, ...')
    social_id = String(desc='소셜 계정 id. abc@facebook.com')

    slime_brob = Integer(default=0, desc='아이템을 먹는 슬라임 의 수치')
    last_login_time = Integer(default=0, desc='마지막 로그인 시간. utc')
    returning_time = Integer(default=0, desc='휴면 유저가 복귀한 시간. utc')

    change_name_ticket_count = Integer(default=0, desc='이름변경 쿠폰 카운트')

    tutorial_pvp5_checked_170531 = Boolean(default=False, desc='v1.1.7 - 콜로세움 개편 - 관련 이슈 임시 수정안, 임시 변수')

    @property
    def level(self):
        return int(master_user_level_inst.get_by_exp(self.exp).key)

    def get_phase_event_cooldown(self, time_current):
        return [key for key, time_till in self.phase_event_cooldown.iteritems() if time_till > time_current]

    def add_phase_event_cooldown(self, event_key, time_till):
        self.phase_event_cooldown[event_key] = time_till


class UserDo(BaseDo):
    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(UserDo, self).__init__(context, user_id)

        self.doc.user_id = user_id

    @classmethod
    def cls(cls):
        return User

    @classmethod
    def get_prefix(cls):
        return 'USR'

    @classmethod
    def get_db(cls):
        return db_user()

    def get_server_dependant_id(self):
        return self.server_id

    @property
    def max_ap(self):
        return master_user_level_inst.get_by_exp(self.doc.exp).max_ap

    @property
    def level(self):
        return int(master_user_level_inst.get_by_exp(self.doc.exp).key)

    @property
    def name(self):
        return self.doc.name
