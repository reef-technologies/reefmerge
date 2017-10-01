#!/bin/bash

function write()
{
#    echo $1
    return 0
}

function checkForConflict()
{
    COMMIT=$1
    A=($(git rev-list --parents -n 1 $COMMIT))
	mergeCommit=${A[0]}
	write "Parents of commit $mergeCommit:"
	A=("${A[@]:1}")
	for hash in ${A[@]}; do
		write "    $hash"
	done

    if (( ${#A[@]} > 2 ))
    then
        write "Harder case, not implemented yet"
    else
        ancestor=$(git merge-base ${A[0]} ${A[1]}) # works only for 2 parents of commit
        git merge-tree $ancestor ${A[0]} ${A[1]} | grep -q ">>>>>>>" # FIXME this grepping may not be sufficient
        RES=$(echo $?)
        if (( $RES == 0 ))
        then
            echo "!!!!!!!!! Conflict detected, conflicts = $COUNT, all = $ALL !!!!!!!!"
            return 0
        fi
    fi
    return 1
}

function countOneRepo()
{
    COUNT=0
    ALL=0
    for commit in $(git rev-list --merges HEAD)
    do
        let ALL+=1
        if checkForConflict $commit
        then
            let COUNT+=1
        fi
    done

    echo "all merges: $ALL"
    echo "conflicts: $COUNT"
}
