#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 power"
    exit 1
fi

python ./send_key2ncplus.py $1

if [[ $? == 0 ]] ; then
    echo "ok"
fi
