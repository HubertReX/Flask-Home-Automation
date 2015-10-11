#!/bin/bash

tmux send-keys -t jasper "$1
"

if [[ $? == 0 ]] ; then
    echo "ok"
else
    echo "nok"
fi

