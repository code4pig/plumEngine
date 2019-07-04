# -*- coding:utf-8 -*-

import script.common.log as logger
from script.chat.chatting_def import ChattingMsgList, ChattingMsg
from script.common.db.base_do import BaseDo
from script.common.db.database import db_chat
from script.dbproxy.do.masters_global import master_constants_inst


class PublicChattingMsgDo(BaseDo):
    def __init__(self, context):
        super(PublicChattingMsgDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return ChattingMsgList

    @classmethod
    def get_prefix(cls):
        return 'PUBLIC_MSG'

    @classmethod
    def get_db(cls):
        return db_chat()

    @classmethod
    def is_server_group_do(cls):
        return True

    def add_msg(self, content, time, server_sender_id=None):
        # 数据已满
        if len(self.doc.msg_list) >= master_constants_inst.get_int('aofei_public_chat_msg_save_num'):
            self.doc.msg_list.pop(0)

        new_msg = ChattingMsg(msg_time=time, msg_content=content, msg_server_sender_id=server_sender_id)
        self.doc.msg_list.append(new_msg)

        self.update()

    def clear_all_msg(self):
        if self.doc.msg_list:
            logger.GetLog().debug('clear all public chatting msg : %s' % len(self.doc.msg_list))
        self.doc.msg_list = []
        self.update()

    def get_new_msg_list(self, time):
        msg_list = []
        for msg in self.doc.msg_list:
            if msg.msg_time > time:  # 是否要加上等号
                msg_list.append(msg.dump())
        return msg_list
