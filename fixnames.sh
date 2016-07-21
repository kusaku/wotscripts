#!/bin/bash

# bash script for filename case conversion
# decompiled files have prefix:
# Embedded file name: [type]/scripts/[original_pathname_here]
#
# it tries to extract original names and rename
# files moved from in~/[type]/script_in
# to [type]/script directory
# extensions are changed to .py also


fixname ()
{
    local TYPE=$1
    local OLDFILE=$2

    # make new filename
    local NEWFILE=$(head -n 1 $OLDFILE | sed -e "s/# Embedded file name: /$TYPE\//g")

    # detect if it is correct
    if [[ ! $NEWFILE =~ ^$TYPE/scripts/ ]];
    then
        # fallback to default, just move in~/ -> .
        NEWFILE=$(echo "${OLDFILE%.*}.py" | sed -e "s/in~\///g")
        echo "Bad header in $OLDFILE, using $NEWFILE"
    fi

    if [[ $NEWFILE != $OLDFILE ]];
    then
        echo "$OLDFILE -> $NEWFILE"
        DIR=$(dirname $NEWFILE)
        # make proper dir if necessary
        [ -d $DIR ] || mkdir -p $DIR
        mv $OLDFILE $NEWFILE
    else
        echo "$OLDFILE -> no change"
    fi
}


find in~/ -name '*.pyc' -delete

find in~/res -name '*.pyc_dis*' | while IFS=$'\n' read -r FILE;
do
    fixname res $FILE
done

find in~/res_bw -name '*.pyc_dis*' | while IFS=$'\n' read -r FILE;
do
    fixname res_bw $FILE
done

# wow!

