#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameters: $0 <action> <service>"
    exit 1
fi

if [[ $1 == "RESTART" ]] ; then
  if [[ $2 == "KODI" ]] ; then
    systemctl restart mediacenter
  fi
  if [[ $2 == "AGO" ]] ; then
    /etc/init.d/agocontrol stop
    /etc/init.d/agocontrol start
  fi
fi

if [[ $? == 0 ]] ; then
    echo "ok"
fi
