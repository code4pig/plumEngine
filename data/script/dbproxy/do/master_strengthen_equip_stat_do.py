# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Dict, Class
from script.common.db.database import db_game
from script.common.db.base_do import MasterDoBase


class MasterStrengthenEquipmentStat(ClassObject):
    key = String(desc='Master StrengthenEquipmentStat 의 키값')

    group_id = String(desc='Items StrengthenValue 의 값')
    strengthen = Integer(desc='아이템의 강화도')

    up_value = Integer(desc='장비에 붙은 속성이 올라가는 확률 ')


class MasterStrengthenEquipmentsStat(ClassObject):
    version = String(desc='마스터 버전')
    items = Dict(Class(MasterStrengthenEquipmentStat), desc='마스터 StrengthenEquipmentStat 의 row')


class MasterStrengthenEquipmentStatDo(MasterDoBase):
    def __init__(self, context):
        super(MasterStrengthenEquipmentStatDo, self).__init__(context)

        self.pk = {}
        for row in self.doc.items.itervalues():
            pk = (row.group_id, row.strengthen)
            self.pk[pk] = row.up_value

    @classmethod
    def cls(cls):
        return MasterStrengthenEquipmentsStat

    @classmethod
    def get_prefix(cls):
        return 'MST_StrengthenEquipmentStat'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_by_pk(self, group, strengthen):
        """

        :rtype: MasterStrengthenEquipmentStat
        """
        return self.pk.get((group, strengthen))
