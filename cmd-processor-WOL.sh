#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 HTPC"
    exit 1
fi

python ./wol.py $1

if [[ $? == 0 ]] ; then
    echo "ok"
fi
