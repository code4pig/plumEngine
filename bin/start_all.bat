echo "start monitor"
start "monitor" plum.exe monitor conf/config_monitor

ping 127.0.0.1 -n 1 > nul

echo "start gateway"
start "gate0" plum.exe gateway conf/config_gateway
start "gate1" plum.exe gateway conf/config_gateway1

ping 127.0.0.1 -n 1 > nul

echo "start db"
start "db0" mtplum.exe dbproxy conf/config_db

ping 127.0.0.1 -n 1 > nul

echo "start chat proxy"
start "chatproxy0" plum.exe chatproxy conf/config_chatproxy

ping 127.0.0.1 -n 1 > nul

echo "start chat"
start "chat0" plum.exe chat conf/config_chat

ping 127.0.0.1 -n 1 > nul

echo "start team proxy"
start "teamproxy0" plum.exe teamproxy conf/config_teamproxy

ping 127.0.0.1 -n 1 > nul

echo "start team"
start "team0" plum.exe team conf/config_team

ping 127.0.0.1 -n 1 > nul

echo "start battle proxy"
start "fightproxy0" plum.exe fightproxy conf/config_fightproxy

ping 127.0.0.1 -n 1 > nul

echo "start battle"
start "fight0" plum.exe fight conf/config_fight

ping 127.0.0.1 -n 1 > nul

echo "start scene proxy"
start "sceneproxy0" plum.exe sceneproxy conf/config_sceneproxy

ping 127.0.0.1 -n 1 > nul

echo "start scene"
start "scene0" plum.exe scene conf/config_scene

ping 127.0.0.1 -n 1 > nul

rem start "testclient0" test.exe conf/config_testclient

echo "start all finish"