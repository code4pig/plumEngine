# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-09 14:52

from __future__ import unicode_literals

import game

import msgpack
import random
import script.common.exception_def as excp
import script.common.config.topoconfig as ModTopo
import script.common.log as logger
import script.common.protocol_def as proto_def
import script.common.gm_define as gm_def
import script.common.utils.utils as utils
from script.common.game_define.scene_def import SceneTeamInfo, SceneMemberInfo
from script.common.nodebase.appbase import CAppBase
from script.common.protocol_def import SCSyncSceneUsers, SCEnterSceneResponse


class CScene(CAppBase):

    def __init__(self):
        CAppBase.__init__(self)
        self.scene_channel_info = {}        # 场景信息, server group id => channel id => server user id => scene user info
        self.scene_team_info = {}           # 场景队伍信息, team id => SceneTeamInfo  注: 成员列表表示在线成员

    # child class must override functions >>>
    def get_node_type(self):
        return ModTopo.NODE_TYPE.SCENE

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # scene的服务器节点: monitor、scene proxy、db
        logger.GetLog().debug('send_msg_to_server_node : %s, %s' % (client_type, args))
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type in self.connect_server_dict and self.connect_server_dict[server_node_type]:
            if server_node_type == ModTopo.NODE_TYPE.MONITOR:
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.SCENE_PROXY:
                if client_type == server_node_type:
                    # 需要查找一个实际的node
                    client_type = self.connect_server_dict[server_node_type].keys()[0]     # 因为proxy只有1个, 所以直接取
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.SCENE, msg_str)
            elif server_node_type == ModTopo.NODE_TYPE.DB_PROXY:
                if client_type == server_node_type:
                    # 随机一个db节点处理即可
                    client_type = random.choice(self.connect_server_dict[server_node_type].keys())
                game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.SCENE, msg_str)
            else:
                logger.GetLog().error('send msg to an unsupported server node : %s, %s, %s' % (client_type, msg_str, args))
        else:
            logger.GetLog().error('send msg to server node %s but there is no one in connect_server_dict' % server_node_type)

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # scene 节点没有客户端
        logger.GetLog().warn('scene has no client node, please check the code: %s, %s, %s' % (client_node_type, msg_str, args))

    # child class must override functions <<<

    # C++ API >>>
    # None
    # C++ API <<<

    # public functions >>>
    def get_scene_2_scene_proxy_rpc(self, client_type=None):
        if client_type:
            return self.get_client_rpc_handler(client_type)
        # 没有传参数,则传入node type, 在send_msg_to_server_node处再做判断
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.SCENE_PROXY)

    def get_scene_2_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_scene_2_db_rpc(self):
        return self.get_send_query_rpc_handler(ModTopo.NODE_TYPE.DB_PROXY)

    # public functions <<<

    # private functions >>>
    def _handle_user_enter_scene(self, server_group_id, server_user_id, msg):
        logger.GetLog().debug('scene handle user enter: %s, %s, %s' % (server_group_id, server_user_id, msg))
        msg_obj = proto_def.SCEnterSceneRequest.new_from_data(msg)
        if msg_obj.scene == 'scLobby':
            # 进入场景, 到db构造自己的数据并发送给所有玩家
            self.get_scene_2_db_rpc().HandleUserEnterScene(server_group_id, server_user_id)
        else:
            # 离开场景
            self.get_scene_2_scene_proxy_rpc().OnUserLeaveSceneManual(server_group_id, server_user_id)

    def _handler_user_move(self, server_group_id, server_user_id, channel_id, msg):
        logger.GetLog().debug('scene user move: %s, %s, %s, %s' % (server_group_id, server_user_id, channel_id, msg))
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id]:
            scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
            if server_user_id in scene_user_id_list:
                # 更新玩家位置信息
                msg_obj = proto_def.SCPlayerMoveRequest.new_from_data(msg)
                self.scene_channel_info[server_group_id][channel_id][server_user_id].position_info = msg_obj.position_info
                # 同步位置给场景其他玩家
                scene_user_id_list.remove(server_user_id)
                if scene_user_id_list:
                    sync_to_scene = proto_def.SCSyncPlayerMove()
                    sync_to_scene.server_user_id = server_user_id
                    sync_to_scene.position_info = msg_obj.position_info
                    self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_to_scene.dump()), scene_user_id_list)

    def _handler_user_update_follow_leader(self, server_group_id, server_user_id, channel_id, msg):
        logger.GetLog().debug('scene user change follow leader: %s, %s, %s, %s' % (server_group_id, server_user_id, channel_id, msg))
        ret_to_client = proto_def.SCUpdateFollowLeaderResponse()
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id] and \
                        server_user_id in self.scene_channel_info[server_group_id][channel_id]:
            team_id = self.scene_channel_info[server_group_id][channel_id][server_user_id].team_id
            if team_id and team_id in self.scene_team_info and server_user_id in self.scene_team_info[team_id].member_dict:
                if self.scene_team_info[team_id].leader_server_user_id == server_user_id:
                    ret_to_client.return_code = excp.ExceptionTeamLeaderCanNotChange.code
                else:
                    msg_obj = proto_def.SCUpdateFollowLeaderRequest.new_from_data(msg)
                    self.scene_team_info[team_id].member_dict[server_user_id].follow_leader = msg_obj.follow_leader
                    other_member_list = self.scene_team_info[team_id].member_dict.keys()
                    other_member_list.remove(server_user_id)
                    if other_member_list:
                        sync_to_mem = proto_def.SCSyncMemFollowLeader()
                        sync_to_mem.server_user_id = server_user_id
                        sync_to_mem.follow_leader = msg_obj.follow_leader
                        self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_to_mem.dump()), other_member_list)
                    ret_to_client.return_code = excp.ExceptionSuccess.code
            else:
                ret_to_client.return_code = excp.ExceptionHasNoTeam.code
        else:
            ret_to_client.return_code = excp.ExceptionUnknown.code
        self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])

    # private functions <<<

    # rpc 相关 >>>
    # from scene proxy >>>
    def OnSceneMsg(self, server_group_id, server_user_id, str_msg, channel_id):
        msg = msgpack.unpackb(str_msg)
        logger.GetLog().debug('scene server receive msg: %s, %s, %s' % (server_group_id, server_user_id, msg))
        cmd = msg.get(proto_def.field_name_cmd, None)
        if cmd is None:
            logger.GetLog().warn('format of this scene msg is unexpected : %s' % msg)
        elif cmd == proto_def.sc_enter_scene:
            self._handle_user_enter_scene(server_group_id, server_user_id, msg)
        elif cmd == proto_def.sc_player_move:
            self._handler_user_move(server_group_id, server_user_id, channel_id, msg)
        elif cmd == proto_def.sc_update_follow_leader:
            self._handler_user_update_follow_leader(server_group_id, server_user_id, channel_id, msg)
        else:
            logger.GetLog().warn('scene server receive unexpected cmd msg : %s' % msg)

    def OnUserLeaveScene(self, server_group_id, server_user_id, channel_id, reason):
        """
        玩家离开场景,移除玩家,并推送给场景其他玩家
        """
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id]:
            # 下线的玩家, 从场景中删除
            scene_user_info = self.scene_channel_info[server_group_id][channel_id].pop(server_user_id, None)

            # 通知其他场景玩家该玩家离开
            scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
            if scene_user_id_list:
                sync_to_scene = SCSyncSceneUsers()
                sync_to_scene.leave_users.append(server_user_id)
                self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_to_scene.dump()), scene_user_id_list)

            # 删除玩家在队伍中数据
            if scene_user_info and scene_user_info.team_id in self.scene_team_info:
                if server_user_id in self.scene_team_info[scene_user_info.team_id].member_dict:
                    self.scene_team_info[scene_user_info.team_id].member_dict.pop(server_user_id)

    def OnSyncUserCreateTeamInScene(self, server_group_id, server_user_id, channel_id, team_id):
        # 更新玩家队伍信息
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id] and \
           server_user_id in self.scene_channel_info[server_group_id][channel_id]:
            self.scene_channel_info[server_group_id][channel_id][server_user_id].team_id = team_id

            # 增加队伍信息
            self.scene_team_info[team_id] = SceneTeamInfo()
            self.scene_team_info[team_id].leader_server_user_id = server_user_id
            self.scene_team_info[team_id].member_dict[server_user_id] = SceneMemberInfo()
            self.scene_team_info[team_id].member_dict[server_user_id].server_user_id = server_user_id
            self.scene_team_info[team_id].member_dict[server_user_id].follow_leader = True
            # 同步队伍创建队伍信息给全场景
            sync_create_team = proto_def.SCSyncCreateTeam()
            sync_create_team.team_info = self.scene_team_info[team_id]
            scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
            self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_create_team.dump()), scene_user_id_list)
        else:
            logger.GetLog().warn('server user id create team but not in scene: %s, %s, %s, %s' % (server_group_id, server_user_id, channel_id, team_id))

    def OnTeamDisband(self, server_group_id, channel_id, team_id):
        # 队伍解散, 直接删除队伍数据, 并更新场景玩家队伍数据
        team_info = self.scene_team_info.pop(team_id, None)
        scene_user_id_list = None
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id]:
            scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
            for scene_user in self.scene_channel_info[server_group_id][channel_id].itervalues():
                if scene_user.team_id == team_id:
                    scene_user.team_id = None
        # 推送队伍解散信息给场景
        if team_info is not None and scene_user_id_list:
            sync_team_disband = proto_def.SCSyncDisbandTeam()
            self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_team_disband.dump()), scene_user_id_list)

    def OnUserLeaveTeam(self, server_group_id, channel_id, server_user_id, team_id):
        # 玩家从队伍数据中删除
        if team_id in self.scene_team_info:
            self.scene_team_info[team_id].member_dict.pop(server_user_id, None)

        # 更新场景玩家数据
        scene_user_id_list = None
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id] and \
           server_user_id in self.scene_channel_info[server_group_id][channel_id]:
            scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
            self.scene_channel_info[server_group_id][channel_id][server_user_id].team_id = None

        # 同步玩家退出队伍
        if scene_user_id_list:
            sync_member_leave = proto_def.SCSyncLeaveTeam()
            sync_member_leave.server_user_id = server_user_id
            self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_member_leave.dump()), scene_user_id_list)

    def OnUserJoinTeam(self, server_group_id, server_user_id, channel_id, team_id):
        if team_id not in self.scene_team_info:
            logger.GetLog().error('user join team but team not in dict : %s, %s, %s, %s' % (server_group_id, server_user_id, channel_id, team_id))
            return
        self.scene_team_info[team_id].member_dict[server_user_id] = SceneMemberInfo()
        self.scene_team_info[team_id].member_dict[server_user_id].server_user_id = server_user_id
        self.scene_team_info[team_id].member_dict[server_user_id].follow_leader = True
        # 更新场景玩家数据
        scene_user_id_list = None
        if server_group_id in self.scene_channel_info and channel_id in self.scene_channel_info[server_group_id] and \
           server_user_id in self.scene_channel_info[server_group_id][channel_id]:
            scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
            self.scene_channel_info[server_group_id][channel_id][server_user_id].team_id = team_id
        # 同步玩家加入队伍
        if scene_user_id_list:
            sync_member_join = proto_def.SCSyncJoinTeam()
            sync_member_join.member = self.scene_team_info[team_id].member_dict[server_user_id]
            self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_member_join.dump()), scene_user_id_list)

    def OnUseEnterSelectChannelCallback(self, server_group_id, server_user_id, channel_id, scene_user, team_id, leader_id, member_id_list):
        # 检查是否有数据
        if server_group_id not in self.scene_channel_info:
            self.scene_channel_info[server_group_id] = {}
        if channel_id not in self.scene_channel_info[server_group_id]:
            self.scene_channel_info[server_group_id][channel_id] = {}
        self.scene_channel_info[server_group_id][channel_id].pop(server_user_id, None)     # 保险起见, 先把自己给pop掉
        # 拿到当前场景中玩家信息
        scene_user_id_list = self.scene_channel_info[server_group_id][channel_id].keys()
        # 将玩家添加到字典中
        self.scene_channel_info[server_group_id][channel_id][server_user_id] = scene_user
        scene_user_info_list = self.scene_channel_info[server_group_id][channel_id].values()
        # 更新队伍数据
        team_info = None
        if team_id:
            if team_id not in self.scene_team_info:
                self.scene_team_info[team_id] = SceneTeamInfo()
                self.scene_team_info[team_id].leader_server_user_id = leader_id
            self.scene_team_info[team_id].member_dict[server_user_id] = SceneMemberInfo()
            self.scene_team_info[team_id].member_dict[server_user_id].server_user_id = server_user_id
            self.scene_team_info[team_id].member_dict[server_user_id].follow_leader = True
            team_info = SceneTeamInfo()
            team_info.leader_server_user_id = leader_id
            for mem_id in member_id_list:
                team_info.member_dict[mem_id] = SceneMemberInfo()
                team_info.member_dict[mem_id].server_user_id = mem_id
                if mem_id in self.scene_team_info[team_id].member_dict:
                    team_info.member_dict[mem_id].follow_leader = self.scene_team_info[team_id].member_dict[mem_id].follow_leader
            # 将自己的同步状态推送给队员
            member_id_list.remove(server_user_id)
            if member_id_list:
                sync_to_mem = proto_def.SCSyncMemFollowLeader()
                sync_to_mem.server_user_id = server_user_id
                sync_to_mem.follow_leader = self.scene_team_info[team_id].member_dict[server_user_id].follow_leader
                self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_to_mem.dump()), member_id_list)
        # 返回信息给客户端
        ret_to_client = SCEnterSceneResponse()
        ret_to_client.scene_user_list = scene_user_info_list
        ret_to_client.team_info = team_info
        self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(ret_to_client.dump()), [server_user_id])
        # 将自己的信息, 广播给场景其他人
        if scene_user_id_list:
            sync_to_scene = SCSyncSceneUsers()
            sync_to_scene.enter_users.append(scene_user)
            self.get_scene_2_scene_proxy_rpc().OnSceneMsgFromScene(server_group_id, msgpack.packb(sync_to_scene.dump()), scene_user_id_list)
    # from scene proxy <<<

    # from db >>>
    def OnHandleUserEnterScene(self, result):
        # 先传给scene proxy, 找到目标channel,并进入
        self.get_scene_2_scene_proxy_rpc().OnUserEnterSceneSelectChannel(*result)

    # from db <<<

    # from monitor >>>
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('scene on gm msg, gm_cmd : %s, params : %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_scene_2_monitor_rpc().OnGMMsgResponse('scene executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_scene_2_monitor_rpc().OnGMMsgResponse('scene executed gm command %s success' % gm_cmd)
        else:
            # 参数不对或者不支持的
            return_msg = 'scene unsupported gm command or param unexpected : %s' % gm_cmd
            logger.GetLog().warn(return_msg)
            self.get_scene_2_monitor_rpc().OnGMMsgResponse(return_msg)

    # # from monitor <<<

    # rpc 相关 <<<

