#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 pr_p"
    exit 1
fi

python ./send_x10_to_htpc.py $1

if [[ $? == 0 ]] ; then
    echo "ok"
fi
