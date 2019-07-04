# -*- coding: utf-8 -*-
# __author__ = 'Yoray'

import msgpack
import socket
import sys
sys.path.append("../..")
import script.common.config.topoconfig as ModTopo
from script.common.gm_define import ALL_GM_CMD_LIST, FINISH_FLAG_STR

HEADER_LENGTH = 5


def make_socket_send_data(str_data):
    data_len = len(str_data)
    header = chr(1) + chr(data_len & 255) + chr((data_len >> 8) & 255) + chr((data_len >> 16) & 255) + chr(data_len >> 24)
    return header + str_data


def receive_msg_handler(sock):
    while 1:
        header = sock.recv(HEADER_LENGTH)
        if not header:
            # 数据为空，对端关闭
            print 'receive data is None, server may be closed'
            return
        data_len = (ord(header[4]) << 24) + (ord(header[3]) << 16) + (ord(header[2]) << 8) + ord(header[1])
        if data_len == 0:
            print 'return data len is zero, close socket'
            sock.close()
            return
        ret_data = sock.recv(data_len)
        if ret_data == FINISH_FLAG_STR:
            print 'receive finish flag, close socket'
            sock.close()
            return
        print ret_data


def run():
    if len(sys.argv) == 6:
        monitor_addr = sys.argv[1]
        monitor_port = sys.argv[2]
        node_type = sys.argv[3]
        gm_cmd = sys.argv[4]
        param_str = sys.argv[5]
        if int(node_type) in ModTopo.NODE_TYPE.__dict__.values():
            if gm_cmd in ALL_GM_CMD_LIST:
                sock = socket.socket(proto=socket.IPPROTO_TCP)
                sock.connect((monitor_addr, int(monitor_port)))
                proto_data = {'gm_cmd': gm_cmd, 'node_type': int(node_type), 'params': param_str}
                send_data = make_socket_send_data(msgpack.packb(proto_data))
                sock.sendall(send_data)
                receive_msg_handler(sock)
            else:
                print 'Unsupported GM command : %s' % gm_cmd
        else:
            print 'NodeType is wrong'
    else:
        print "Usage:"
        print "\t%s MonitorAddr MonitorPort NodeType Cmd Params" % sys.argv[0]
        print "\tNodeType :"
        print "\t\tMONITOR = 100\n\t\tGATEWAY = 200\n\t\tDB_PROXY = 300\n\t\tCHAT_PROXY = 400\n\t\tCHAT = 500\n\t\tTEAM_PROXY = 600"
        print "\t\tTEAM = 700\n\t\tFIGHT_PROXY = 800\n\t\tFIGHT = 900\n\t\tSCENE_PROXY = 1000\n\t\tSCENE = 1100"
        print "\tCmd : "
        print "\t\tupdate_data | reload_script"
        print "\tParams:"
        print "\t\tif cmd is update_data : all | inst names with comma separated , e.g. master_constants_inst,master_equipment_inst"
        print "\t\tif cmd is reload_script: full import paths with comma separated, e.g. script.common.utils.utils,script.common.protocol_def"
        sys.exit(1)

if __name__ == '__main__':
    run()