# -*- coding:utf-8 -*-


from __future__ import unicode_literals

from script.common.db.class_obj import ClassObject, Integer, List, Dict, Class, String
from script.common.db.database import db_clan
from script.common.game_define.global_def import get_clan_server_id
from script.common.game_define.time_util import is_same_date
from script.common.db.base_do import BaseDo

CLAN_DUNGEON_WAREHOUSE_DIST_LOG_EXPIRE_TIME = 604800


class ClanDungeonWarehouseDistLog(ClassObject):
    dist_time = Integer(default=0, desc='分配时间')
    item_id = String(desc='道具id')
    item_num = Integer(desc='道具数量')
    op_user_name = String(desc='分配者名字')
    gain_user_name = String(desc='得到的玩家名字')


class ClanDungeonWarehouseInfo(ClassObject):
    item_dict = Dict(Integer(), desc='当前仓库道具列表')
    log_list = List(Class(ClanDungeonWarehouseDistLog), desc='分配日志列表')
    log_check_time = Integer(desc='日志检查时间,处理过期日志')


class ClanDungeonWarehouseDo(BaseDo):
    def __init__(self, data_context, clan_id):
        self.server_id = get_clan_server_id(clan_id)
        super(ClanDungeonWarehouseDo, self).__init__(data_context, clan_id)
        self.clan_id = clan_id

    @classmethod
    def cls(cls):
        return ClanDungeonWarehouseInfo

    @classmethod
    def get_prefix(cls):
        return 'CLANDUNGEONWAREHOUSE'

    @classmethod
    def get_db(cls):
        return db_clan()

    def get_server_dependant_id(self):
        return self.server_id

    def get_log_list(self, flag_time):
        return [log_item for log_item in self.doc.log_list if log_item.dist_time > flag_time]

    def add_dist_log(self, log):
        if not self.doc.log_check_time:
            self.doc.log_check_time = log.dist_time
        if not is_same_date(self.doc.log_check_time, log.dist_time):
            self.doc.log_list = [log_item for log_item in self.doc.log_list if log_item.dist_time + CLAN_DUNGEON_WAREHOUSE_DIST_LOG_EXPIRE_TIME > log.dist_time]
        self.doc.log_list.append(log)
        self.update()

    def do_dist_item(self, item_id, item_num):
        self.doc.item_dict[item_id] -= item_num
        self.update()
        if self.doc.item_dict[item_id] <= 0:
            self.doc.item_dict.pop(item_id)
            return 0
        return self.doc.item_dict[item_id]

    def add_warehouse_items(self, add_item_dict):
        for item_id, item_num in add_item_dict.iteritems():
            if item_id not in self.doc.item_dict:
                self.doc.item_dict[item_id] = 0
            self.doc.item_dict[item_id] += item_num
        self.update()

    def empty_warehouse_items(self):
        if self.doc.item_dict:
            self.doc.item_dict.clear()
            self.update()
