#!/bin/bash

if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 command"
    exit 1
fi

function get_status {
  sudo screen -S cec-client -p 0 -X stuff "pow 0
" > /home/osmc/flask/result.log
  #echo "1"
  #cat result.log
  #local result=`cat /home/osmc/flask/result.log`
  #echo "2" $result
}

get_status
res=`cat /home/osmc/flask/result.log`
#echo 1 $res
if [[ "$res" =~ "No screen session found" ]]; then
  sudo /etc/init.d/cec-client-runner restart
  get_status
  res=`cat /home/osmc/flask/result.log`
  #echo 2 $res
fi

if [[ "$res" =~ "No screen session found" ]]; then
  echo CEC server restart failed - no CEC communication - quitting!
  exit 1
fi

res=`tail -n 1 /var/log/cec-client-console.log | awk '{print $3}'`

if [[ $1 == "on" ]] ; then
    /home/osmc/flask/turn-tv-on.sh
fi

if [[ $1 == "off" ]] ; then
    /home/osmc/flask/turn-tv-off.sh
fi

if [[ $1 == "power" ]] ; then
  #res=`sudo /home/osmc/flask/get-tv-status.sh`
  if [[ ${res} == "" ]] ; then
    echo "tv power status unknown"
    exit 1
  elif [[ ${res} =~ "on" ]] ; then
    sudo /home/osmc/flask/turn-tv-off.sh
  elif [[ ${res} =~ "standby" ]] ; then
    sudo /home/osmc/flask/turn-tv-on.sh
  fi
fi

if [[ $1 == "status" ]] ; then
    #sudo /home/osmc/flask/get-tv-status.sh
    echo $res
    exit
fi

if [[ $1 == "HDMI1" ]] ; then
    sudo /home/osmc/flask/switch-to-hdmiN.sh 1
fi

if [[ $1 == "HDMI2" ]] ; then
    sudo /home/osmc/flask/switch-to-hdmiN.sh 2
fi
if [[ $1 == "HDMI3" ]] ; then
    sudo /home/osmc/flask/switch-to-hdmiN.sh 3
fi

if [[ $? == 0 ]] ; then
    echo "ok"
fi


