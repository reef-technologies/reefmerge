#!/bin/bash

function validate()
{
    DIRECTORY=$1
    if [ -z $DIRECTORY ]
    then
        echo "Please provide directory, cannot make it here"
        exit 2
    fi

    DIRECTORY=$(readlink -m $DIRECTORY)
    TEMP_DIR=$(mktemp -d)

    START_DIR=$(pwd)
    cd $TEMP_DIR

    git init

    echo "step 1: creating ancestor"
    cp $DIRECTORY/ancestor.py main.py
    git add main.py
    git commit -am "Ancestor commit"

    echo "step 2: creating my branch"
    git checkout -b mine
    cp $DIRECTORY/mine.py main.py
    git commit -am "Mine commit"

    echo "step 3: commiting your version of file on master"
    git checkout master
    cp $DIRECTORY/yours.py main.py
    git commit -am "Your commit"

    echo "step 4: again on my branch, trying to merge"
    git checkout mine
    git merge master

    echo "step 5: checking if a conflict occurs"
    git status | grep -q "fix conflicts"
    RETVAL=$(echo $?)

    cd $START_DIR
    rm -rf $TEMP_DIR

    return $RETVAL
}
