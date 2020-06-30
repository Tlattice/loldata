#!/bin/bash

server_ip=192.168.0.10
server_path=/home/pi/Documents/server
mount_path=src/server
sshfs -o allow_other butter@${server_ip}:${server_path} ${mount_path}

