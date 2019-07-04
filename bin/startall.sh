#!/bin/bash

set -e
set -u

export LD_LIBRARY_PATH=../libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
echo "LD_LIBRARY_PATH : " $LD_LIBRARY_PATH

echo "start monitor"
./plum monitor conf/config_monitor &
sleep 1

echo "start gateway"
./plum gateway conf/config_gateway &
sleep 1

echo "start db"
./mtplum dbproxy conf/config_db &
sleep 1

echo "start chatproxy"
./plum chatproxy conf/config_chatproxy &
sleep 1
echo "start teamproxy"
./plum teamproxy conf/config_teamproxy &
sleep 1
echo "start fightproxy"
./plum fightproxy conf/config_fightproxy &
sleep 1
echo "start sceneproxy"
./plum sceneproxy conf/config_sceneproxy &
sleep 1

echo "start chat"
./plum chat conf/config_chat &
sleep 1
echo "start team"
./plum team conf/config_team &
sleep 1
echo "start fight"
./plum fight conf/config_fight &
sleep 1
echo "start scene"
./plum scene conf/config_scene &
sleep 1

echo "start all end"
