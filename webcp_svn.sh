#!/usr/bin/env bash

set -x # echo on

rsync -avz /dev/shm/www/ ~/svn_users/mbsullivan
