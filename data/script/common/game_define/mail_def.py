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

from script.common.db.class_obj import ClassObject, String, Integer, Dict, List, Class

enum_user_mail_tab = {
    '0': 'SYSTEM',
    '1': 'CLAN',
    '2': 'FRIEND'
}

mail_storage_ttl = 60 * 60 * 72  # 메일함 보관 기간


class ItemBase(ClassObject):
    type = String(desc='아이템의 타입 default=None, view 용으로 조회시 해당 아이템이 랜덤 지급인지 구분', default=None)
    item_class_key = String(desc='아이템의 클래스 키')
    count = Integer(desc='아이템 수량')
    extra = Integer(desc='아이템 추가 정보, view 용으로 조회시 아이템을 얻을 수 있는 갯수로 표시 ')
    options_trade = Dict(String(), desc="装备属性值")    #add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-04-06 for 交易行邮件装备固定属性


class UserMailBox(ClassObject):
    confirm_dt = Integer(desc='메일 확인 일시 seconds from 1970-01-01. utc.')


class Mail(ClassObject):
    mail_id = Integer(desc='Mail id')
    mail_type = String(desc='MailType')
    tab_id = Integer(desc='MailType 에 따른 tab_id')

    receiver = String(desc='받는사람')
    sender = String(desc='보낸사람')
    contents = String(desc='내용')
    attach = List(Class(ItemBase), desc='첨부 아이템 목록 [ItemBase, ...]')

    create_dt = Integer(desc='메일 발송 일시. seconds from 1970-01-01. utc.')
    expired_dt = Integer(desc='메일 보관만료 일시. seconds from 1970-01-01 utc.')

    sender_clan_role = String(default=None, desc='보내는 사람의 클랜 직위 ( 클랜 메일 용)')


class ReadMail(Mail):
    read_expired_dt = Integer(desc='메일 받은 일시 seconds from 1970-01-01. utc.')


class MailList(ClassObject):
    mail_list = List(Class(Mail), desc='우편 목록')


class UserMailTab(ClassObject):
    mail_list = List(Class(Mail), desc='우편 목록')
    read_mail_list = List(Class(ReadMail), desc='읽은 우편 목록')
    add_mail_count = Integer(default=0, desc='기록된 메일 카운트')


class UserMailList(ClassObject):
    mails = Dict(Class(UserMailTab), desc='유저 탭별 메일 정보')
