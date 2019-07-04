# coding=utf8


from __future__ import unicode_literals

from script.common.game_define.mail_def import mail_storage_ttl
from script.dbproxy.do.individual_mail_do import IndividualMailDo
from script.dbproxy.do.counter_mail import CounterMailDo
from script.dbproxy.do.masters_global import master_mail_do_inst


class MailBo(object):
    def __init__(self, context):
        self.context = context

    def create_mail(self, mail_type, receiver, sender, contents, create_dt, attach=None, attach_item_base_obj=None,
                    time_expire=None, server_id=None):

        if time_expire is None:
            time_expire = create_dt + mail_storage_ttl

        if server_id is None:
            from script.common.db.instant_box import instant_box
            server_id = instant_box.server_selected

        tab = master_mail_do_inst.get_mail_category_code(mail_type)

        # 유저 별 개별 메일을 생성 해 준다
        individual_mail_do = IndividualMailDo(self.context, receiver, CounterMailDo(server_id, receiver).increase(), tab, server_id)
        individual_mail_do.create_mail(mail_type, receiver, sender, contents, create_dt, attach, time_expire, attach_item_base_obj)
        individual_mail_do.update()

        return individual_mail_do.doc

