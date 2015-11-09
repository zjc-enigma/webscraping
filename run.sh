#!/bin/bash
while(true)
do
    ./2.py 2
    if($?==0)
    then
        break;
    fi
done
