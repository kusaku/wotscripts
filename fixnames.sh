#!/bin/bash

# bash script for filename case conversion
# decompiled files have prefix:
# Embedded file name: ./scripts/[original_pathname_here]
#
# it tries to extract original names and rename
# files moved from ./script_in to ./script directory
# extensions also are changed to .py


rm -rf ./scripts_in/*.pyc
find ./scripts_in/ -name '*.py*' | while IFS=$'\n' read -r FILE; do

    # read original filename
    NEWFILE=$(head -n 1 $FILE | sed -e 's/# Embedded file name: /.\//g')

    # detect if it is correct
    if [[ ! $NEWFILE =~ ^./scripts/ ]];
    then
        # fallback to default, just move ./script_in -> ./script
        NEWFILE=$(echo "${FILE%.*}.py" | sed -e 's/\.\/scripts_in/\.\/scripts/g')
        echo "Bad header in $FILE, using $NEWFILE"
    fi

    if [[ $NEWFILE != $FILE ]];
    then
        echo "$FILE -> $NEWFILE"
        DIR=$(dirname $NEWFILE)
        # make proper dir if necessary
        [ -d $DIR ] || mkdir -p $DIR
        mv $FILE $NEWFILE
    else
        echo "$FILE -> no change"
    fi

done

# wow!

