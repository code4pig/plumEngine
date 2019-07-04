# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.dbproxy.do.masters_global import master_constants_inst
from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.alpha_fort_war_def import AlphaFortWarUserInfo, ALPHA_FORT_WAR_STEP2_POINT_ID_LIST


class AlphaFortWarUserDo(BaseDo):
    """
    每日战斗的阶段信息
    """

    def __init__(self, context, user_id, server_id=None):
        self.server_id = server_id
        super(AlphaFortWarUserDo, self).__init__(context, user_id)
        self.context = context

    @classmethod
    def cls(cls):
        return AlphaFortWarUserInfo

    @classmethod
    def get_prefix(cls):
        return 'ALPHAFORTWARUSER'

    @classmethod
    def get_db(cls):
        return db_game()

    def get_server_dependant_id(self):
        return self.server_id

    def is_in_frozen_time(self, current_time, point_id):
        is_same_step_point = (point_id == self.doc.last_attack_point_id) or (point_id in ALPHA_FORT_WAR_STEP2_POINT_ID_LIST and
                                                                             self.doc.last_attack_point_id in ALPHA_FORT_WAR_STEP2_POINT_ID_LIST)
        return is_same_step_point and (current_time - self.doc.last_attack_time < master_constants_inst.get_number('aofei_fort_war_user_attack_interval'))

    def update_attack_data(self, attack_time, point_id):
        self.doc.last_attack_point_id = point_id
        self.doc.last_attack_time = attack_time
        self.update()

    def update_attack_time_only(self, attack_time):
        self.doc.last_attack_time = attack_time
        self.update()
