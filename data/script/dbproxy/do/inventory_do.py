# coding=utf8

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.item_def import Inventory
from script.common.game_define.global_def import make_server_user_id


class InventoryDo(BaseDo):
    def __init__(self, context, user_id, server_id=None):
        self.user_id = user_id
        self.server_id = server_id

        super(InventoryDo, self).__init__(context, user_id)

    @classmethod
    def cls(cls):
        return Inventory

    @classmethod
    def get_prefix(cls):
        return 'USRINVEN'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def get_default_doc(self):
        return Inventory(user_id=self.user_id)

    def get_equipment(self, instance_key, raise_exception=True):
        """
        장비 인스턴스 키에 부합하는 장비를 조회한다.

        :param instance_key: 장비의 instance key
        :param raise_exception: 존재하지 않을 경우 예외 발생시킬지 여부
        :rtype: Equipment
        """
        return self.doc.get_equipment(instance_key, raise_exception)

