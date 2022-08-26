#!/usr/bin/env bash

gunicorn start:app -c gunicorn.conf.py
#while true ; do
##    sleep 43200   0.5day
#    wget localhost:8090/new
#    sleep 2
#
#done
# docker build  --network=host -t testfnd .

0 1 * * * docker exec stock2 /bin/sh -c 'wget localhost:8090/new > /dev/null 2>&1 &'
