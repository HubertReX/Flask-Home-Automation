#!/bin/bash

if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 command"
    exit 1
fi

if [[ $1 == "on" ]] ; then
    /home/pi/flask/turn-tv-on.sh
fi
if [[ $1 == "off" ]] ; then
    /home/pi/flask/turn-tv-off.sh
fi

if [[ $1 == "power" ]] ; then
  res=`/home/pi/flask/get-tv-status.sh`
  if [ -z "${res}" ]; then
    echo "tv power status unknown"
    exit 1
  elif [ "x${res}" = "xon" ]; then
    /home/pi/flask/turn-tv-off.sh
  else
    /home/pi/flask/turn-tv-on.sh
  fi
fi

if [[ $1 == "status" ]] ; then
    /home/pi/flask/get-tv-status.sh
fi

if [[ $1 == "HDMI1" ]] ; then
    /home/pi/flask/switch-to-hdmiN.sh 1
fi
if [[ $1 == "HDMI2" ]] ; then
    /home/pi/flask/switch-to-hdmiN.sh 2
fi
if [[ $1 == "HDMI3" ]] ; then
    /home/pi/flask/switch-to-hdmiN.sh 3
fi

if [[ $? == 0 ]] ; then
    echo "ok"
fi



