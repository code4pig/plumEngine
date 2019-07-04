# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-10 21:05

import random
import time
import script.common.log as logger
from script.common.game_define.global_def import get_server_and_user_id
from script.common.game_define.hero_def import HeroSnap
from script.common.game_define.scene_def import SceneUserInfo, PositionItem
from script.dbproxy.do.hero_do import HeroDo
from script.dbproxy.do.heroes_do import HeroesDo
from script.dbproxy.do.inventory_do import InventoryDo
from script.dbproxy.do.user_do import UserDo
from script.dbproxy.do.user_mastery_do import UserMasteryDo
from script.dbproxy.do.user_team_do import UserTeamDo
from script.dbproxy.do.team_do import TeamDo
from script.dbproxy.rpc.irpctarget import IDbsRpcTarget
from script.dbproxy.do.user_summary_do import UserSummaryDo
from script.common.db.data_context import DataContext
from script.common.db.instant_box import instant_box


class Scene2DbRpcHandler(IDbsRpcTarget):
    def __init__(self):
        pass

    def Reload(self, modname):
        import script.common.utils.utils as utils
        utils.Reload(modname)

    def HandleUserEnterScene(self, server_group_id, server_user_id):
        logger.GetLog().debug('handle user enter scene : %s, %s' % (server_group_id, server_user_id))
        server_id, user_id = get_server_and_user_id(server_user_id)
        instant_box.server_group = server_group_id
        instant_box.server_selected = server_id
        instant_box.time_current = time.time()
        data_context = DataContext()
        instant_box.data_context = data_context
        user_info = self.make_scene_user_info(data_context, server_user_id)
        leader_id = None
        team_member_list = None
        if user_info.team_id:
            team_doc = TeamDo.Reader()(data_context, user_info.team_id).doc
            leader_id = team_doc.server_leader_id
            team_member_list = team_doc.member_id_list
        # 构造公会
        return server_group_id, server_user_id, user_info, user_info.team_id, leader_id, team_member_list

    @staticmethod
    def make_scene_user_info(data_context, server_user_id):
        scene_user_info = SceneUserInfo()
        server_id, user_id = get_server_and_user_id(server_user_id)
        scene_user_info.server_user_id = server_user_id
        user_reader_do = UserDo.Reader()(data_context, user_id, server_id)
        scene_user_info.name = user_reader_do.name
        scene_user_info.level = user_reader_do.level
        scene_user_info.hero_snap = HeroSnap()
        active_hero_key = HeroesDo.Reader()(data_context, user_id, server_id).doc.active
        hero_doc = HeroDo.Reader()(data_context, user_id, active_hero_key, server_id).doc
        inventory_doc = InventoryDo.Reader()(data_context, user_id, server_id).doc
        mastery_doc = UserMasteryDo.Reader()(data_context, user_id, server_id).doc
        scene_user_info.hero_snap.load_from_hero(hero_doc, inventory_doc, mastery_doc)
        user_summary_doc = UserSummaryDo(data_context, user_id, server_id).doc
        scene_user_info.clan_id = user_summary_doc.clan_id
        scene_user_info.clan_name = user_summary_doc.clan_name
        scene_user_info.team_id = UserTeamDo.Reader()(data_context, user_id, server_id).doc.team_id
        pos_item = PositionItem()
        pos_item.x, pos_item.y, pos_item.z, pos_item.rotation = Scene2DbRpcHandler.get_lobby_init_position()
        scene_user_info.position_info = pos_item
        return scene_user_info

    @staticmethod
    def get_lobby_init_position():
        return random.choice([(7.54, -4.818467, 3.56, 0), (66.29, -1.935134, 22.83, 0), (5.14, -4.818467, 11.77, 0),
                              (67.96, -1.927896, 9.41, 0), (30.44, -1.851801, 3.2, 0), (40.04, -1.935134, 16.8, 0)])