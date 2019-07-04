# coding=utf8

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Integer, Float
from script.dbproxy.do.master_util import new_master_do_class


class MasterEquipmentStrengthenSetRow(ClassObject):
    key = String(desc='key')
    type = String(desc="类型")
    strengthen = Integer(desc='强化等级')
    set_option = String(desc='属性类型')
    option_value = Float(desc='属性值')
    res_id = String(desc="特效id")
    owner_class = String(desc="所属英雄")

    def get_index_meta(self):
        return {
            'get_by_type': (self.type, self.owner_class,)
        }

MasterEquipmentStrengthenSetDo = new_master_do_class(MasterEquipmentStrengthenSetRow, 'MST_EquipmentStrengthenSet')
