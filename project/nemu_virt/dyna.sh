#!/bin/bash

DYNA=dynamips
CISCO_IMAGE=c7200-jk9s-mz.124-13b.image
IDLE_PC=0x608724c0
R1_cfg=R1_startup_config.cfg
R2_cfg=R2_startup_config.cfg

echo "lauching router 1"

$DYNA -P 7200 --idle-pc $IDLE_PC -i 1 -X -T 2001 \
 -p 1:PA-FE-TX -s 1:0:udp:10003:127.0.0.1:10002 -p 2:PA-FE-TX -s 2:0:udp:10007:127.0.0.1:10006 \
 $CISCO_IMAGE -C $R1_cfg &

echo "lauching router 2"

$DYNA -P 7200 --idle-pc $IDLE_PC -i 2 -X -T 2002 \
 -p 1:PA-FE-TX -s 1:0:udp:10005:127.0.0.1:10004 -p 2:PA-FE-TX -s 2:0:udp:10009:127.0.0.1:10008 \
 $CISCO_IMAGE -C $R2_cfg &
