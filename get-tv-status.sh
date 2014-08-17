#!/bin/bash
screen -S cec-client -p 0 -X stuff "pow 0^M"
tail -n5 /var/log/cec-client-console.log | grep 'power' | tail -n1 | awk '{print $3}'




