# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from script.common.db.base_do import BaseDo
from script.common.db.database import db_game
from script.common.game_define.alpha_fort_war_def import AlphaFortWarStep


class AlphaFortWarStepDo(BaseDo):
    """
    每日战斗的阶段信息
    """

    def __init__(self, context):
        super(AlphaFortWarStepDo, self).__init__(context)

    @classmethod
    def cls(cls):
        return AlphaFortWarStep

    @classmethod
    def get_prefix(cls):
        return 'ALPHAFORTWARSTEP'

    @classmethod
    def get_db(cls):
        return db_game()

    @classmethod
    def is_server_group_do(cls):
        return True

    @property
    def step(self):
        return self.doc.step

    def set_step(self, step, current_time):
        """
        设置赛季阶段
        """
        old_step = self.doc.step
        old_set_time = self.doc.last_set_time
        self.doc.step = step
        self.doc.last_set_time = int(current_time)
        self.update()
        print '========================== alpha fort war step reset ==========================' \
              '\n\told step : {0}, old set time : {1}' \
              '\n\tnew step : {2}, new set time : {3}' \
              '\n========================== alpha fort war step reset =========================='.format(old_step, old_set_time, step, current_time)
