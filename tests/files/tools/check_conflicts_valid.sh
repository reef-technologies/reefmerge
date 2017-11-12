#!/bin/bash

source ./impls/validate_conflict.sh

FAILS=0

SINGLE_TESTS=../single
for testdir in $(ls -1 $SINGLE_TESTS)
do
    validate "$SINGLE_TESTS/$testdir" 2>&1 >/dev/null
    if [ $(echo $?) ]
    then
        echo "  check for $testdir ok"
    else
        echo "  FAIL FOR $testdir"
        let FAILS += 1
    fi
done

if [ "$FAILS" ]
then
    exit 0
else
    echo "Some checks failed"
    exit 1
fi
