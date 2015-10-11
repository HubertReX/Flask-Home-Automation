#!/bin/bash
screen -S cec-client -p 0 -X stuff "poll 0
"
tail -n3 /var/log/cec-client-console.log | grep 'POLL'




