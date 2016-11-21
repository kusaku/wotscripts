#!/bin/bash

# bash script for filename case conversion
# decompiled files have prefix:
# Embedded file name: scripts/[original_pathname_here]
#
# it tries to extract original names and rename
# files moved from in~ to /script directory
# extensions are changed to .py also


fixname ()
{
    local OUTDIR=$1
    local OLDFILE=$2

    # make new filename
    local NEWFILE=$OUTDIR/$(head -n 1 $OLDFILE | sed -e "s/# Embedded file name: //g")

    # detect if it is correct
    if [[ ! $NEWFILE =~ ^$OUTDIR/scripts/ ]];
    then
        # fallback to default, just move in~/ -> .
        NEWFILE=$OUTDIR$(echo "${OLDFILE%.*}.py" | sed -e "s/in~\///g")
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


find in~ -name '*.pyc' -delete

find in~ -name '*.pyc_dis*' | while IFS=$'\n' read -r FILE;
do
    fixname . $FILE
done

# wow!

