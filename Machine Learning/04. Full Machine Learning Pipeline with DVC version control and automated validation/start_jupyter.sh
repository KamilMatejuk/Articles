#!/bin/bash

# jupyter cannot be closed by CTRL-C, docker compose doesn't handle well passing SIGINT

trap 'kill -TERM $PID' TERM INT

jupyter notebook "$@" &
PID=$!
wait $PID
trap - TERM INT
wait $PID
