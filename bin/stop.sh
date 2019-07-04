#!/bin/bash

APPNAME=$1
IDS=$(pgrep -l $APPNAME -u $USER | awk '{print $1}')

if [ -n "$IDS" ];then
	echo try to kill $IDS
	kill -TERM $IDS
	times=0
	while [ "$times" -lt 10 ]; do
		times=$[$times+1]
		LASTIDS=$(pgrep -l $APPNAME -u $USER | awk '{print $1}')
		if [ -z "$LASTIDS" ];then
			echo kill $APPNAME with pid:$IDS successful
			exit 0
		else
			sleep 1
		fi
	done
	echo kill $LASTIDS failed
else
	echo no process for $APPNAME to kill
fi
