# -*- coding: utf-8 -*-
# __author__ = 'Yoray'

import msgpack
import script.monitor.object_factory as ModFac
import script.common.config.topoconfig as ModTopo
import script.common.log as logger
import script.common.gm_define as gm_def
import script.common.utils.utils as utils
from script.common.gm_define import ALL_GM_CMD_LIST


class GMMsgHandler(object):
    def __init__(self):
        self.cur_client_connect_id = None
        self.cur_gm_msg = None

    def handle_gm_msg(self, connect_id, proto_type, msg_str):
        logger.GetLog().info('receive gm msg from connect_id = %s, proto_type = %s, msg_str = %s' % (connect_id, proto_type, msg_str))
        if self.cur_client_connect_id is not None:
            ret_msg = 'other gm command is in processing: %s, %s' % (self.cur_client_connect_id, self.cur_gm_msg)
            logger.GetLog().warn(ret_msg)
            ModFac.CreateApp().send_msg_to_client(connect_id, ret_msg)
            ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)      # tell client connect close
            return
        if proto_type == ModTopo.PROTO_TYPE.COMMON:
            try:
                msg_obj = msgpack.unpackb(msg_str)
                gm_cmd = msg_obj.get('gm_cmd', None)
                if gm_cmd in ALL_GM_CMD_LIST:
                    param_str = msg_obj.get('params', None)
                    if param_str and param_str.strip():
                        node_type = msg_obj.get('node_type', None)
                        if node_type == ModTopo.NODE_TYPE.MONITOR:
                            # 本节点
                            # 特殊处理,不设置更新当前连接和gm命令信息,不启动超时定时器，执行完成直接告诉客户端断开连接
                            self.OnGMMsg(gm_cmd, param_str)
                            ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)  # tell client connect close
                        else:
                            if ModTopo.NODE_TYPE.has_value(node_type):
                                ModFac.CreateApp().get_monitor_2_node_rpc(node_type).OnGMMsg(gm_cmd, param_str)
                            else:
                                ret_msg = 'gm command node type invalid : %s' % node_type
                                logger.GetLog().warn(ret_msg)
                                ModFac.CreateApp().send_msg_to_client(connect_id, ret_msg)
                                ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)  # tell client connect close
                                return
                            # 更新当前连接和gm命令信息
                            self.cur_client_connect_id = connect_id
                            self.cur_gm_msg = msg_str
                            # 启动一个定时器,指定时间内给客户端发一个信息
                            ModFac.CreateApp().RegTick(self.handle_timeout_timer, None, 5000)
                    else:
                        ret_msg = 'gm command params invalid : %s' % param_str
                        logger.GetLog().warn(ret_msg)
                        ModFac.CreateApp().send_msg_to_client(connect_id, ret_msg)
                        ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)  # tell client connect close
                else:
                    ret_msg = 'Unsupported gm command : %s' % gm_cmd
                    logger.GetLog().warn(ret_msg)
                    ModFac.CreateApp().send_msg_to_client(connect_id, ret_msg)
                    ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)  # tell client connect close
            except Exception as e:
                ret_msg = 'gm command error : %s, %s' % (msg_str, e.message)
                logger.GetLog().warn(ret_msg)
                ModFac.CreateApp().send_msg_to_client(connect_id, ret_msg)
                ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)  # tell client connect close
        else:
            ret_msg = 'gm command proto type error'
            logger.GetLog().warn(ret_msg)
            ModFac.CreateApp().send_msg_to_client(connect_id, ret_msg)
            ModFac.CreateApp().send_msg_to_client(connect_id, gm_def.FINISH_FLAG_STR)  # tell client connect close

    def OnGMMsg(self, gm_cmd, params_str):
        if gm_cmd == gm_def.gm_cmd_reload_script:
            fail_file_list = utils.execute_reload_files_command(params_str)
            if fail_file_list:  # 有失败的文件
                self.OnGMMsgHandleResponse('monitor executed gm command %s fail, fail files : %s' % (gm_cmd, fail_file_list))
            else:  # 所有文件重load成功
                self.OnGMMsgHandleResponse('monitor executed gm command %s success' % gm_cmd)
        else:
            return_msg = 'monitor unsupported gm command or param unexpected : %s, %s' % (gm_cmd, params_str)
            logger.GetLog().warn(return_msg)
            self.OnGMMsgHandleResponse(return_msg)

    def OnGMMsgHandleResponse(self, ret_msg):
        logger.GetLog().debug("execute gm command result : %s" % ret_msg)
        if self.cur_client_connect_id:
            ModFac.CreateApp().send_msg_to_client(self.cur_client_connect_id, ret_msg)

    def handle_timeout_timer(self, msg):
        if self.cur_client_connect_id:
            ModFac.CreateApp().send_msg_to_client(self.cur_client_connect_id, gm_def.FINISH_FLAG_STR)      # tell client connect close
            ModFac.CreateApp().DelTick(self.handle_timeout_timer)
            self.cur_client_connect_id = None
            self.cur_gm_msg = None