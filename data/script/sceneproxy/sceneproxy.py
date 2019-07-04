# -*- coding: utf-8 -*-

# Author : Yoray
# Created: 2018-07-09 15:48

from __future__ import unicode_literals

import game

import random
import script.common.config.topoconfig as ModTopo
import script.common.log as logger
import script.common.gm_define as gm_def
import script.common.utils.utils as utils
from script.common.nodebase.appbase import CAppBase
from script.common.game_define.scene_def import SCENE_USER_MAX_NUM_PER_CHANNEL, CHANNEL_ID_MAX, LEAVE_SCENE_REASON_LOGOUT, LEAVE_SCENE_REASON_CREATE_TEAM, \
    LEAVE_SCENE_REASON_JOIN_TEAM, LEAVE_SCENE_REASON_MANUAL


class CSceneProxy(CAppBase):
    def __init__(self):
        CAppBase.__init__(self)
        self.scene_msg_count = 0
        self.channel_id_counter = {}        # channel计数器, server_group_id => channel id counter
        self.user_map_channel = {}          # 玩家所在场景, server_user_id => (server group id, channel id）
        self.channel_user_list = {}         # 场景玩家数量统计, server group id => channel id => [server_user_id, ...]
        self.team_bind_channel = {}         # 队伍绑定的场景, team id => (server group id, channel id)
        self.channel_bind_team = {}         # 场景所属的队伍, server group id => channel id => team id
        self.channel_map_node = {}          # 场景对应的场景服务器, server group id => channel id => scene node id

    # ========== child class must override functions ==========
    def get_node_type(self):
        return ModTopo.NODE_TYPE.SCENE_PROXY

    def send_msg_to_server_node(self, client_type, msg_str, *args):
        # scene proxy的服务器节点: monitor、gateway
        server_node_type = self.get_node_type_by_client_type(client_type)
        if server_node_type == ModTopo.NODE_TYPE.MONITOR:
            game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.COMMON, msg_str)
        elif server_node_type == ModTopo.NODE_TYPE.GATEWAY:
            if server_node_type in self.connect_server_dict:
                if client_type == server_node_type:
                    # 广播给所有的gateway
                    for real_client_type in self.connect_server_dict[server_node_type].keys():
                        game.SendMsgToServer(real_client_type, ModTopo.PROTO_TYPE.SCENE, msg_str)
                else:
                    game.SendMsgToServer(client_type, ModTopo.PROTO_TYPE.SCENE, msg_str)
            else:
                logger.GetLog().warn('no gateway connect')
        else:
            logger.GetLog().error('send msg to an unexpected server node : %s, %s, %s' % (client_type, msg_str, args))

    def send_msg_to_client_node(self, client_node_type, msg_str, *args):
        # scene proxy的客户端节点: scene、team(可能还有其他逻辑节点)
        if client_node_type in [ModTopo.NODE_TYPE.SCENE, ModTopo.NODE_TYPE.TEAM]:
            if args:
                self._send_msg_to_client_node(msg_str, client_node_type, args[0])
            else:
                self._send_msg_to_client_node(msg_str, client_node_type)
        else:
            logger.GetLog().error('send msg to an unexpected client node : %s, %s, %s' % (client_node_type, msg_str, args))

    # ========== C++ API ==========
    # None

    # ========== public functions ==========
    def get_scene_proxy_2_scene_rpc(self, scene_node_id=None):
        if scene_node_id:
            return self.get_server_rpc_handler(ModTopo.NODE_TYPE.SCENE, scene_node_id)
        return self.get_server_rpc_handler(ModTopo.NODE_TYPE.SCENE)

    def get_scene_proxy_2_gateway_rpc(self, client_type=None):
        if client_type is not None:
            return self.get_client_rpc_handler(client_type)
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.GATEWAY)

    def get_scene_proxy_to_monitor_rpc(self):
        return self.get_client_rpc_handler(ModTopo.NODE_TYPE.MONITOR)

    def get_scene_node_id_list(self):
        if ModTopo.NODE_TYPE.SCENE in self.connect_client_dict:
            return self.connect_client_dict[ModTopo.NODE_TYPE.SCENE].keys()
        logger.GetLog().info('no scene node connected')
        return []

    # ========== private functions ==========
    def _send_msg_to_client_node(self, msg_str, client_node_type, client_node_id=None):
        if client_node_type in self.connect_client_dict:
            if client_node_type == ModTopo.NODE_TYPE.SCENE:
                proto_type = ModTopo.PROTO_TYPE.SCENE
            elif client_node_type == ModTopo.NODE_TYPE.TEAM:
                proto_type = ModTopo.PROTO_TYPE.TEAM
            else:
                logger.GetLog().error('_send_msg_to_client_node input an unexpected node type : %s' % client_node_type)
                return

            if client_node_id:
                if client_node_id in self.connect_client_dict[client_node_type]:
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, self.connect_client_dict[client_node_type][client_node_id], proto_type, msg_str)
                else:
                    logger.GetLog().warn('client node %s %s not connected' % (client_node_type, client_node_id))
            else:
                for client_node_conn_id in self.connect_client_dict[client_node_type].values():
                    game.SendMsgToClient(ModTopo.SERVICE_TYPE.FOR_NODE, client_node_conn_id,proto_type, msg_str)
        else:
            logger.GetLog().warn('no scene node in connect_client_dict')

    def _get_user_map_channel_id(self, server_user_id):
        if server_user_id in self.user_map_channel:
            server_group_id, channel_id = self.user_map_channel[server_user_id]
            if server_group_id in self.channel_map_node and channel_id in self.channel_map_node[server_group_id]:
                return channel_id
            logger.GetLog().warn('user has map channel but data not in channel_map_node : %s, %s' % (server_group_id, channel_id))
        return None

    def _get_channel_map_node_id(self, server_group_id, channel_id):
        if channel_id:
            # 此处不做过多额外检查
            return self.channel_map_node[server_group_id][channel_id]
        # 没有映射的场景服务器, 随机一个
        scene_node_id_list = self.get_scene_node_id_list()
        scene_node_id = scene_node_id_list[self.scene_msg_count % len(scene_node_id_list)]
        self.scene_msg_count += 1
        return scene_node_id

    def _find_target_scene(self, server_group_id, team_id):
        target_channel_id = 0
        if team_id:
            # 有队伍id, 查找是否有队伍对应的场景
            if team_id in self.team_bind_channel:
                _, target_channel_id = self.team_bind_channel[team_id]
            else:
                # 队伍还没有绑定的场景, 找一个人多适合未绑定过的场景
                if server_group_id in self.channel_user_list:
                    max_flag = SCENE_USER_MAX_NUM_PER_CHANNEL - 5  # 场景最大人数减去队伍最大人数
                    temp_num = -1
                    # 找到现存场景中满足人数要求中人数最多的场景
                    for cid, user_list in self.channel_user_list[server_group_id].iteritems():
                        if server_group_id not in self.channel_bind_team or cid not in self.channel_bind_team[server_group_id]:
                            # 场景还未绑定队伍
                            num = len(user_list)
                            if max_flag >= num > temp_num:
                                # 人数符合, 检查是否已绑定
                                temp_num = num
                                target_channel_id = cid
                                if temp_num == max_flag:
                                    break
                if not target_channel_id:
                    # 还未找到场景, 新建一个
                    target_channel_id = self._create_scene_channel(server_group_id, team_id)
                else:
                    # 找到一个场景, 绑定给组队
                    self.team_bind_channel[team_id] = (server_group_id, target_channel_id)
                    if server_group_id not in self.channel_bind_team:
                        self.channel_bind_team[server_group_id] = {}
                    self.channel_bind_team[server_group_id][target_channel_id] = team_id
        else:
            # 没有队伍, 找一个人多且未满的场景(此处不检查场景是否绑定队伍, 所以场景可能最大人数会到25)
            if server_group_id in self.channel_user_list:
                max_flag = SCENE_USER_MAX_NUM_PER_CHANNEL - 1
                temp_num = -1
                for cid, user_list in self.channel_user_list[server_group_id].iteritems():
                    num = len(user_list)
                    if max_flag >= num > temp_num:
                        # 人数符合, 检查是否已绑定
                        temp_num = num
                        target_channel_id = cid
                        if temp_num == max_flag:
                            break
            if not target_channel_id:
                # 还未找到场景, 新建一个
                target_channel_id = self._create_scene_channel(server_group_id, team_id)

        return target_channel_id

    def _create_scene_channel(self, server_group_id, team_id):
        # 先随机一个场景服务器
        scene_node_id_list = self.get_scene_node_id_list()
        scene_node_id = random.choice(scene_node_id_list)
        # 查找一个新的channel id
        if server_group_id not in self.channel_id_counter:
            self.channel_id_counter[server_group_id] = 0
        target_channel_id = 1 if self.channel_id_counter[server_group_id] == CHANNEL_ID_MAX else self.channel_id_counter[server_group_id] + 1
        # 更新counter
        self.channel_id_counter[server_group_id] = target_channel_id
        # 更新team bind channel 和 channel bind team
        if team_id:
            self.team_bind_channel[team_id] = (server_group_id, target_channel_id)
            if server_group_id not in self.channel_bind_team:
                self.channel_bind_team[server_group_id] = {}
            self.channel_bind_team[server_group_id][target_channel_id] = team_id
        # 更新channel map server
        if server_group_id not in self.channel_map_node:
            self.channel_map_node[server_group_id] = {}
        self.channel_map_node[server_group_id][target_channel_id] = scene_node_id
        return target_channel_id

    def _add_channel_user(self, server_group_id, channel_id, server_user_id):
        if server_group_id not in self.channel_user_list:
            self.channel_user_list[server_group_id] = {}
        if channel_id not in self.channel_user_list[server_group_id]:
            self.channel_user_list[server_group_id][channel_id] = []
        if server_user_id not in self.channel_user_list[server_group_id][channel_id]:
            self.channel_user_list[server_group_id][channel_id].append(server_user_id)

    def _remove_scene_user(self, server_user_id):
        server_group_id, channel_id = self.user_map_channel.pop(server_user_id, (None, None))
        if server_group_id in self.channel_user_list and channel_id in self.channel_user_list[server_group_id] and \
           server_user_id in self.channel_user_list[server_group_id][channel_id]:
            self.channel_user_list[server_group_id][channel_id].remove(server_user_id)

    # ========== rpc 相关 ==========
    # gateway to proxy >>>
    def OnSceneMsg(self, server_group_id, server_user_id, msg_str):
        """
         收到网关转发过来的聊天消息
        """
        # 拿到玩家对应的场景channel
        channel_id = self._get_user_map_channel_id(server_user_id)
        scene_node_id = self._get_channel_map_node_id(server_group_id, channel_id)
        self.get_scene_proxy_2_scene_rpc(scene_node_id).OnSceneMsg(server_group_id, server_user_id, msg_str, channel_id)

    def OnUserLogout(self, server_group_id, server_user_id):
        """
        玩家状态改变,广播到所有server
        """
        logger.GetLog().debug('on user logout : %s, %s' % (server_group_id, server_user_id))
        # 玩家下线, 移除玩家信息, 通知场景其他成员下线
        channel_id = self._get_user_map_channel_id(server_user_id)
        if channel_id:
            scene_node_id = self._get_channel_map_node_id(server_group_id, channel_id)
            # 删除玩家相关数据
            self._remove_scene_user(server_user_id)
            # 通知业务节点处理玩家离开场景
            self.get_scene_proxy_2_scene_rpc(scene_node_id).OnUserLeaveScene(server_group_id, server_user_id, channel_id, LEAVE_SCENE_REASON_LOGOUT)
    # gateway to proxy <<<

    # scene to proxy >>>
    def OnUserEnterSceneSelectChannel(self, server_group_id, server_user_id, scene_user, team_id, leader_id, member_id_list):
        """
        进入场景选择channel
        """
        channel_id = self._find_target_scene(server_group_id, team_id)
        # 更新玩家场景映射数据
        self.user_map_channel[server_user_id] = (server_group_id, channel_id)
        # 更新场景玩家数据
        self._add_channel_user(server_group_id, channel_id, server_user_id)
        scene_node_id = self.channel_map_node[server_group_id][channel_id]
        self.get_scene_proxy_2_scene_rpc(scene_node_id).OnUseEnterSelectChannelCallback(server_group_id, server_user_id, channel_id, scene_user, team_id, leader_id, member_id_list)

    def OnUserLeaveSceneManual(self, server_group_id, server_user_id):
        logger.GetLog().debug('on user leave scene manual : %s, %s' % (server_group_id, server_user_id))
        channel_id = self._get_user_map_channel_id(server_user_id)
        if channel_id:
            scene_node_id = self._get_channel_map_node_id(server_group_id, channel_id)
            # 删除玩家相关数据
            self._remove_scene_user(server_user_id)
            # 通知业务节点处理玩家离开场景
            self.get_scene_proxy_2_scene_rpc(scene_node_id).OnUserLeaveScene(server_group_id, server_user_id, channel_id, LEAVE_SCENE_REASON_MANUAL)

    def OnSceneMsgFromScene(self, server_group_id, msg, receiver_id_list=None, exclude_id_list=None):
        """
        收到场景消息，转发下去
        """
        self.get_scene_proxy_2_gateway_rpc().OnSceneMsgFromScene(server_group_id, msg, receiver_id_list, exclude_id_list)
    # scene to proxy <<<

    # team to proxy >>>
    def OnUserCreateTeam(self, server_user_id, team_id, scene_user_info):
        if server_user_id in self.user_map_channel:
            server_group_id, cur_channel_id = self.user_map_channel[server_user_id]
            if server_group_id not in self.channel_bind_team:
                self.channel_bind_team[server_group_id] = {}

            if cur_channel_id in self.channel_bind_team[server_group_id]:
                # 当前场景已有队伍,需要切换场景
                # 拿到旧场景对应的场景逻辑服id
                cur_scene_node_id = self._get_channel_map_node_id(server_group_id, cur_channel_id)
                # 找到一个新场景绑定给队伍
                new_channel_id = self._find_target_scene(server_group_id, team_id)
                new_scene_node_id = self.channel_map_node[server_group_id][new_channel_id]
                # 旧场景删除玩家数据
                self._remove_scene_user(server_user_id)
                # 更新玩家场景映射数据
                self.user_map_channel[server_user_id] = (server_group_id, new_channel_id)
                # 更新场景玩家数据
                self._add_channel_user(server_group_id, new_channel_id, server_user_id)
                # 通知旧场景玩家离开场景
                self.get_scene_proxy_2_scene_rpc(cur_scene_node_id).OnUserLeaveScene(server_group_id, server_user_id, cur_channel_id, LEAVE_SCENE_REASON_CREATE_TEAM)
                # 通知新场景该玩家进入
                self.get_scene_proxy_2_scene_rpc(new_scene_node_id).OnUseEnterSelectChannelCallback(server_group_id, server_user_id, new_channel_id, scene_user_info,
                                                                                                    team_id, server_user_id, [server_user_id])
            else:
                # 当前场景还未绑定, 直接绑定给队伍
                self.channel_bind_team[server_group_id][cur_channel_id] = team_id
                self.team_bind_channel[team_id] = (server_group_id, cur_channel_id)
                cur_scene_node_id = self._get_channel_map_node_id(server_group_id, cur_channel_id)
                self.get_scene_proxy_2_scene_rpc(cur_scene_node_id).OnSyncUserCreateTeamInScene(server_group_id, server_user_id, cur_channel_id, team_id)

        else:
            logger.GetLog().warn('user create team but user has no match channel : %s, %s' % (server_user_id, team_id))

    def OnTeamDisband(self, team_id):
        if team_id in self.team_bind_channel:
            server_group_id, channel_id = self.team_bind_channel[team_id]
            self.team_bind_channel.pop(team_id)
            if server_group_id in self.channel_bind_team:
                self.channel_bind_team[server_group_id].pop(channel_id, None)
            scene_node_id = self.channel_map_node[server_group_id][channel_id]
            self.get_scene_proxy_2_scene_rpc(scene_node_id).OnTeamDisband(server_group_id, channel_id, team_id)

    def OnUserLeaveTeam(self, server_user_id, team_id):
        if server_user_id in self.user_map_channel:
            server_group_id, channel_id = self.user_map_channel[server_user_id]
            scene_node_id = self.channel_map_node[server_group_id][channel_id]
            self.get_scene_proxy_2_scene_rpc(scene_node_id).OnUserLeaveTeam(server_group_id, channel_id, server_user_id, team_id)

    def OnUserJoinTeam(self, server_user_id, scene_user_info, team_id, leader_id, member_id_list):
        if server_user_id in self.user_map_channel:
            server_group_id, cur_channel_id = self.user_map_channel[server_user_id]
            if team_id in self.team_bind_channel:
                _, team_channel_id = self.team_bind_channel[team_id]
                if cur_channel_id == team_channel_id:
                    # 场景没变化, 只更新玩家状态信息
                    scene_node_id = self._get_channel_map_node_id(server_group_id, cur_channel_id)
                    self.get_scene_proxy_2_scene_rpc(scene_node_id).OnUserJoinTeam(server_group_id, server_user_id, cur_channel_id, team_id, leader_id)
                else:
                    # 场景有变化, 处理数据
                    cur_scene_node_id = self._get_channel_map_node_id(server_group_id, cur_channel_id)
                    new_scene_node_id = self._get_channel_map_node_id(server_group_id, team_channel_id)
                    # 旧场景删除玩家数据
                    self._remove_scene_user(server_user_id)
                    # 更新玩家场景映射数据
                    self.user_map_channel[server_user_id] = (server_group_id, team_channel_id)
                    # 更新场景玩家数据
                    self._add_channel_user(server_group_id, team_channel_id, server_user_id)
                    # 通知旧场景玩家离开场景
                    self.get_scene_proxy_2_scene_rpc(cur_scene_node_id).OnUserLeaveScene(server_group_id, server_user_id, cur_channel_id, LEAVE_SCENE_REASON_JOIN_TEAM)
                    # 通知新场景该玩家进入
                    self.get_scene_proxy_2_scene_rpc(new_scene_node_id).OnUseEnterSelectChannelCallback(server_group_id, server_user_id, team_channel_id, scene_user_info,
                                                                                                        team_id, leader_id, member_id_list)
                    # 通知玩家加入队伍
                    self.get_scene_proxy_2_scene_rpc(new_scene_node_id).OnUserJoinTeam(server_group_id, server_user_id, team_channel_id, team_id, leader_id)

    # team to proxy <<<

    # monitor to proxy >>>
    # ====================================================================================
    # ================================ gm command handler ================================
    # ====================================================================================
    def OnGMMsg(self, gm_cmd, params_str):
        logger.GetLog().debug('scene proxy on gm msg, gm_cmd : %s, params_str: %s' % (gm_cmd, params_str))
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.get_scene_proxy_to_monitor_rpc().OnGMMsgResponse('scene proxy executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.get_scene_proxy_to_monitor_rpc().OnGMMsgResponse('scene proxy executed gm command %s success' % gm_cmd)
        else:
            # 参数不对或者不支持的
            return_msg = 'scene proxy unsupported gm command or param unexpected : %s' % gm_cmd
            logger.GetLog().warn(return_msg)
            self.get_scene_proxy_to_monitor_rpc().OnGMMsgResponse(return_msg)
    # monitor to proxy <<<

    # ========== internal function ==========

