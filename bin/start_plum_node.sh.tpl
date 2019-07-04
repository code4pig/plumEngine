#!/bin/bash

export LD_LIBRARY_PATH=../libs:$LD_LIBRARY_PATH

# ./plum {node_flag} {config_path} {prof_path} {log_path} &
# node_flag: required, is one of : monitor | gateway | chatproxy | teamproxy | fightproxy | sceneproxy | chat | team | fight | scene | testclient
# config_path: required, path of config file, e.g. conf/config_gateway
# prof_path: optional, path of profile output file, e.g. ../profile/gateway.prof
# log_path: optional, path of log output directory, e.g. ../log 

./plum chat conf/config_chat &
