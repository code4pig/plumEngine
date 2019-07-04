# coding=utf8

from __future__ import unicode_literals

from script.common.db.base_do import MasterDoBase
from script.common.db.class_obj import ClassObject, String, Dict, Class, Number
from script.common.db.database import db_game


class MasterConstantRow(ClassObject):
    key = String(desc='상수명')
    value = Number(desc='값. 수.')
    s_value = String(desc='값. 스트링.')


class MasterConstant(ClassObject):
    version = String(desc='마스터 버전')
    items = Dict(Class(MasterConstantRow), desc='마스터. row')


class MasterConstantDo(MasterDoBase):
    def __init__(self, context):
        super(MasterConstantDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return MasterConstant

    @classmethod
    def get_prefix(cls):
        return 'MST_Constants'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_number(self, key):
        return self.doc.items[key].value

    def get_string(self, key):
        return self.doc.items[key].s_value

    def get_int(self, key):
        return int(self.get_number(key))
