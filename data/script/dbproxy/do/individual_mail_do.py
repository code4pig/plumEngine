# coding=utf8

# Copyright (C) [2017] NCSOFT Corporation. All Rights Reserved.
#
# This software is provided 'as-is', without any express or implied warranty.
# In no event will NCSOFT Corporation (“NCSOFT”) be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software subject to acceptance
# and compliance with any agreement entered into between NCSOFT (or any of its affiliates) and the recipient.
# The following restrictions shall also apply:

# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software.
# 2. You may not modify, alter or redistribute this software, in whole or part, unless you are entitled to
# do so by express authorization in a separate agreement between you and NCSOFT.
# 3. This notice may not be removed or altered from any source distribution.


# coding=utf8

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.mail_def import Mail, mail_storage_ttl, ItemBase
from script.dbproxy.do.masters_global import master_mail_do_inst


class IndividualMailDo(BaseDo):
    def __init__(self, context, user_id, counter, tab_id, server_id=None):
        self.server_id = server_id
        self.mail_id = counter
        super(IndividualMailDo, self).__init__(context, user_id, counter, tab_id)

    @classmethod
    def cls(cls):
        return Mail

    @classmethod
    def get_prefix(cls):
        return 'USRINDIVISUALMAIL'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def create_mail(self, mail_type, receiver, sender, contents, create_dt, attach=None, ttl=mail_storage_ttl,
                    attach_item_base_obj=None):
        """
        새로운 메일을 생성한다

        :param mail_type: 우편 타입
        :param receiver: 받는사람
        :param sender: 보낸사람
        :param contents: 본문 내용 string
        :param create_dt: 메일이 생성(활성화)되는 시간
        :param attach: 첨부 아이템이 있을경우 첨부아이템 {item_class_key: count, ...}
        :param ttl: 우편이 만료되는 시간. (초). create_dt 기준으로 흐르는 시간
        :param attach_item_base_obj: 첨부아이템을 ItemBase 형태로 지급하는경우 [ItemBase, ...]
        :rtype: mail_do.Mail
        """
        # if ttl is None:
        #     ttl = mail_storage_ttl
        #
        self.doc = self.create_new_mail(self.mail_id, mail_type, receiver, sender, contents, attach, ttl, create_dt,
                                        attach_item_base_obj)
        self.set_ttl(int(self.doc.expired_dt))

        return self.doc

    @classmethod
    def create_new_mail(cls, mail_id, mail_type, receiver, sender, contents, attach, ttl, create_dt,
                        attach_item_base_obj=None):
        """
        새로운 메일을 생성한다

        :param mail_id: id
        :param mail_type: 우편 타입
        :param receiver: 받는사람
        :param sender: 보낸사람
        :param contents: 본문 내용 string
        :param attach: 첨부 아이템이 있을경우 첨부아이템 {item_class_key: count, ...}
        :param ttl: 우편의 보관기간
        :param create_dt: 우편이 생성(활성화) 되는 시간
        :param attach_item_base_obj: 첨부아이템을 ItemBase 로 처리하는경우 [ItemBase, ...]
        :rtype: mail_do.Mail
        """
        mail = Mail()

        mail.mail_id = mail_id
        mail.mail_type = mail_type
        mail.receiver = receiver
        mail.sender = sender
        mail.contents = contents
        mail.create_dt = create_dt

        mail.expired_dt = mail.create_dt + ttl

        # 유져가 보내는메일에 첨부 아이템이 있는경우 인벤토리에서 차감해줘야한다. 아직은 그런 기획 없음

        if attach:
            for item_id, count in attach.iteritems():
                item = ItemBase()
                item.item_class_key = item_id
                item.count = count

                mail.attach.append(item)

        if attach_item_base_obj:
            mail.attach.extend(attach_item_base_obj)

        mail.tab_id = master_mail_do_inst.get_mail_category_code(mail_type)

        return mail
