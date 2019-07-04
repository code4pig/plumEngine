#!/bin/bash

export LD_LIBRARY_PATH=../libs:$LD_LIBRARY_PATH

# ./mtplum {node_flag} {config_path} {prof_path} {log_path} &
# node_flag: required, is one of : dbproxy
# config_path: required, path of config file, e.g. conf/config_db
# prof_path: optional, path of profile output file, e.g. ../profile/db.prof
# log_path: optional, path of log output directory, e.g. ../log 

./plum dbproxy conf/config_db &
