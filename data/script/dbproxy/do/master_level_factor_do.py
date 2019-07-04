# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Dict, Class, Integer
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase


class MasterLevelFactorRow(ClassObject):
    key = String(desc='영향 받는 2차 스탯')

    str = Integer(desc='힘')
    dex = Integer(desc='민')
    int = Integer(desc='지')
    con = Integer(desc='체')


class MasterLevelFactor(ClassObject):
    version = String(desc='마스터 버전')
    items = Dict(Class(MasterLevelFactorRow), desc='마스터. row')


class MasterLevelFactorDo(MasterDoBase):
    def __init__(self, context):
        super(MasterLevelFactorDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return MasterLevelFactor

    @classmethod
    def get_prefix(cls):
        return 'MST_LevelFactor'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_item(self, c_class_d):
        """

        :param c_class_d:
        :return:
        :rtype: MasterLevelFactorRow
        """
        return self.doc.items[c_class_d]

    # def get_stats(self, c_class_d, level):
    #     result = Stat()
    #
    #     level -= 1
    #     if level < 0:
    #         level = 0
    #
    #     row = self.get_item(c_class_d)
    #
    #     result.add('str', row.str * level)
    #     result.add('dex', row.dex * level)
    #     result.add('int', row.int * level)
    #     result.add('con', row.con * level)
    #
    #     return result
