#!/bin/bash

function write()
{
    # echo $1
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
        DIFF=$(git merge-tree $ancestor ${A[0]} ${A[1]})
        echo $DIFF | grep -q ">>>>>>>" # FIXME this grepping may not be sufficient
        RES=$(echo $?)
        if (( $RES == 0 ))
        then
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

function countAllRepos()
{
    COUNT=0
    ALL=0
    for repo in $(ls -1d */)
    do
        cd $repo
        echo "Processing $repo"
        RESULTS=$(countOneRepo)
        cd ..
        ADD_COUNT=$(echo "$RESULTS" | grep "conflicts" | cut -f2 -d" ")
        ADD_ALL=$(echo "$RESULTS" | grep "all merges" | cut -f3 -d" ")
        let COUNT+=$ADD_COUNT
        let ALL+=$ADD_ALL
        echo "$repo processed, count = $ADD_COUNT, all = $ADD_ALL"
    done

    echo "all merges: $ALL"
    echo "conflicts: $COUNT"
}

function countInQuarters()
{
    YEAR=`date +"%Y"`
    DAYS_IN_MONTH=(31 28 31 30 31 30 31 31 30 31 30 31)
    START_YEAR=$(git log $(git log --pretty=format:%H|tail -1) | grep Date | cut -f4 -d":" | cut -f2 -d" ")
    for yr in `seq $START_YEAR $YEAR`
    do
        for month in `seq 0 3`
        do
            let IN_MONTH=0
            let ALL_IN_MONTH=0
            let START=$month*3+1
            let STOP=$START+2
            for commit in $(git rev-list --merges --after=$yr-$START-01 --before=$yr-$STOP-${A[$STOP]} HEAD)
            do
                let ALL_IN_MONTH+=1
                if checkForConflict $commit
                then
                    let IN_MONTH+=1
                fi
            done
            if (( $START < 10 ))
            then
              START="0$START"
            fi
            if (( $ALL_IN_MONTH > 0 ))
            then
                PERCENTAGE=`bc <<< "scale=2; 100*$IN_MONTH/$ALL_IN_MONTH"`
                csv="yes"
                if [ -z "$csv" ]
                then
                  echo "In quarter $month in year $yr: conflicts/merges: $IN_MONTH / $ALL_IN_MONTH ($PERCENTAGE%)"
                else
                  echo "$yr-$START-01,$PERCENTAGE"
                fi
            else
              echo "$yr-$START-01,0"
            fi
        done
    done
}

function countInChunks()
{
    CHUNKS_NUM=$1  # TODO error handling?
    ALL_MERGES=$(git rev-list --merges HEAD)
    MERGE_COMMITS_NUM=$(echo "$ALL_MERGES" | wc -l)
    COMMITS_IN_CHUNK=$(python -c "print($MERGE_COMMITS_NUM/$CHUNKS_NUM.0)")
    echo $COMMITS_IN_CHUNK
    PREV_CHUNK=0
    CURR_CHUNK=0
    CHUNK_START=0
    CHUNK_END=$(echo "$COMMITS_IN_CHUNK" | cut -f1 -d'.')
    CHUNK_END_FL=$COMMITS_IN_CHUNK
    CURR=0
    CONFLICTS=0
    for COMMIT in `echo "$ALL_MERGES"`
    do
        if checkForConflict $COMMIT
        then
            let CONFLICTS+=1
        fi
        let CURR+=1
        if (( $CURR >= $CHUNK_END ))
        then
            echo "chunk ending with $CHUNK_END_FL got $CONFLICTS conflicts"
            CHUNK_END_FL=$(echo "$CHUNK_END_FL + $COMMITS_IN_CHUNK" | bc)
            CHUNK_END=$(echo "$CHUNK_END_FL" | cut -f1 -d'.')
            CONFLICTS=0
        fi
    done
}
