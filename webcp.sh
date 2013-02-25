#!/bin/bash

#
# Copy without extranous files to a new folder
#
# Usage: >webch.sh (copies to default directory) OR >webch.sh [directory name]
#

set -x # echo on

# set default directory, if none is given
if [ -z "$1" ]
then
    DIR="/dev/shm/www/"
else
    DIR=$1
fi

rsync -av   --exclude "webcp.sh" \
            --exclude "README.txt" \
            --exclude "*~" \
            --exclude ".hg/" \
            --exclude '*/.hg/' ./ $DIR
