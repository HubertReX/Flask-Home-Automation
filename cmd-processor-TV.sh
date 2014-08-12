#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 on"
    exit 1
fi

if [[ $1 == "on" ]] ; then
    ./turn-tv-on.sh
fi
if [[ $1 == "off" ]] ; then
    ./turn-tv-off.sh
fi

if [[ $1 == "HDMI1" ]] ; then
    ./switch-to-hdmiN.sh 1
fi
if [[ $1 == "HDMI2" ]] ; then
    ./switch-to-hdmiN.sh 2
fi
if [[ $1 == "HDMI3" ]] ; then
    ./switch-to-hdmiN.sh 3
fi

if [[ $? == 0 ]] ; then
    echo "ok"
fi



