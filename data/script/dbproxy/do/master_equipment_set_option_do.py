# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, String, Float, Integer
from script.dbproxy.do.master_util import new_master_do_class


class MasterEquipmentSetOptionRow(ClassObject):
    key = String(desc='마스터 시트 Equipment Set Option 의 키')
    set_id = String(desc='세트 key')
    set_count = Integer(desc='세트 개수')
    set_option = String(desc='세트 옵션')
    option_value = Float(desc='옵션 값')
    skin_id = String(desc="皮肤key")   #add by ZHM, JoyGames, ALPHA GROUP CO.,LTD, at 2017-07-11 for 英雄装备服装

    def get_index_meta(self):
        return {
            'get_set_options': (self.set_id,)
        }

MasterEquipmentSetOptionDo = new_master_do_class(MasterEquipmentSetOptionRow, 'MST_EquipmentSetOption')
