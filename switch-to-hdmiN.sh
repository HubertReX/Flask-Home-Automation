#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameter: hdmi source number"
    exit 1
fi

screen -S cec-client -p 0 -X stuff "as
"
screen -S cec-client -p 0 -X stuff "p 0 $1
"

#if [[ $? == 0 ]] ; then
#    echo "ok"
#fi



