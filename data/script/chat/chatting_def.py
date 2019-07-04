# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Dict, Class, List

# 聊天频道定义
CHAT_CHANNEL_TYPE_NONE = 0
CHAT_CHANNEL_TYPE_NOTICE = 1
CHAT_CHANNEL_TYPE_PUBLIC = 2
CHAT_CHANNEL_TYPE_CLAN = 3
CHAT_CHANNEL_TYPE_P2P = 4
CHAT_CHANNEL_TYPE_TEAM = 5


class ChattingMsg(ClassObject):
    msg_time = Integer(desc='消息时间')
    msg_server_sender_id = String(desc='发送者server user id', default=None)
    msg_content = Dict(String(), desc='消息内容')


class ChattingMsgList(ClassObject):
    msg_list = List(Class(ChattingMsg), desc='消息列表')


class P2PChattingMsgList(ClassObject):
    msg_dict = Dict(Class(ChattingMsgList), desc='离线消息数据,{sender_id:ChattingMsgList}')


class P2POfflineMsg(ClassObject):
    server_sender_id = String(desc='发送者server user id')
    msg_list = List(Class(ChattingMsg), desc='消息列表')
