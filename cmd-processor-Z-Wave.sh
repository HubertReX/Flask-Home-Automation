#!/bin/bash
if [[ $1 == "" ]] ; then
    echo "missing parameter: $0 speakers on"
    exit 1
fi


if [[ $1 == "speakers" ]] ; then
  if [[ $2 == "" ]] ; then
      echo "missing second parameter: $0 speakers on"
      exit 1
  fi
  
  if [[ $2 == "on" ]] ; then
      ../azw/turn_on.sh
  fi
  if [[ $2 == "off" ]] ; then
      ../azw/turn_off.sh
  fi
fi

if [[ $? == 0 ]] ; then
    echo "ok"
fi

