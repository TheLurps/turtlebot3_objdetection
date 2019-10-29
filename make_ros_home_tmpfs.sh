#!/bin/bash
ME=$(echo $USERNAME)

sudo sh -c 'echo "tmpfs /home/'$ME'/.ros tmpfs rw,noexec,nodev,nosuid,uid='$ME',gid='$ME',mode=1700,size=4G 0 0" >> /etc/fstab'
