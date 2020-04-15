#!/bin/bash
user=saular
cmd=/home/saular/Pollution-CSC4996/main.py
su -c 'nohup env -i $cmd </dev/null >/dev/null 2>&1 &' $user