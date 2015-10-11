#!/bin/bash
#screen -S cec-client -p 0 -X stuff "pow 0^M"

function get_status {
  screen -S cec-client -p 0 -X stuff "pow 0
" > result.log
  #echo "1"
  #cat result.log
  #local result=`cat result.log`
  #echo "2" $result
}

get_status
res=`cat result.log`
#echo $res
if [[ "$res" =~ "No screen session found" ]]; then
  /etc/init.d/cec-client-runner restart
  get_status
  res=`cat result.log`
fi

if [[ "$res" =~ "No screen session found" ]]; then
  exit 1
else
  tail -n5 /var/log/cec-client-console.log | grep 'power' | tail -n1 | awk '{print $3}'
fi



