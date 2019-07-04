# -*- coding:utf-8 -*-

from script.chat.chatting_def import ChattingMsgList, ChattingMsg, P2PChattingMsgList
from script.common.db.base_do import BaseDo
from script.common.db.database import db_chat
from script.dbproxy.do.masters_global import master_constants_inst


class P2PChattingMsgDo(BaseDo):
    def __init__(self, context, receiver_id, server_id=None):
        self.server_id = server_id
        super(P2PChattingMsgDo, self).__init__(context, receiver_id)

    @classmethod
    def cls(cls):
        return P2PChattingMsgList

    @classmethod
    def get_prefix(cls):
        return 'P2P_MSG'

    @classmethod
    def get_db(cls):
        return db_chat()

    def get_server_dependant_id(self):
        return self.server_id

    def add_msg(self, server_sender_id, content, time):
        if server_sender_id not in self.doc.msg_dict:
            self.doc.msg_dict[server_sender_id] = ChattingMsgList()

        if len(self.doc.msg_dict[server_sender_id].msg_list) >= master_constants_inst.get_int('aofei_p2p_chat_msg_save_num'):
            self.doc.msg_dict[server_sender_id].pop(0)

        new_msg = ChattingMsg()
        new_msg.msg_time = time
        new_msg.msg_content = content
        new_msg.msg_server_sender_id = server_sender_id
        self.doc.msg_dict[server_sender_id].msg_list.append(new_msg)

        self.update()

    def get_msg_dict(self):
        return self.doc.msg_dict

    def clear_msg_dict(self):
        self.doc.msg_dict.clear()
        self.update()

    def is_msg_box_full(self, server_sender_id):
        return (server_sender_id in self.doc.msg_dict and len(self.doc.msg_dict[server_sender_id].msg_list) >=
                master_constants_inst.get_int('aofei_p2p_chat_msg_save_num')) or \
               (server_sender_id not in self.doc.msg_dict and len(self.doc.msg_dict) >=
                master_constants_inst.get_int('aofei_p2p_chat_max_num_per_user'))
