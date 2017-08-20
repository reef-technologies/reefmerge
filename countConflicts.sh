#!/bin/bash

# script should run in the repository

COUNT=0
ALL=0
for commit in $(git rev-list --merges HEAD)
do
	A=($(git rev-list --parents -n 1 $commit))
	mergeCommit=${A[0]}
	echo "Parents of commit $mergeCommit:"
	A=("${A[@]:1}")
	for hash in ${A[@]}; do
		echo "    $hash"
	done

	ancestor=$(git merge-base ${A[0]} ${A[1]})
	git merge-tree $ancestor ${A[0]} ${A[1]} | grep ">>>>>>>" # FIXME works only for 2 parents of commit
	RES=$(echo $?)
	let ALL+=1
	if (( $RES == 0 ))
	then
		let COUNT+=1
		echo "!!!!!!!!! Conflict detected, conflicts = $COUNT, all = $ALL !!!!!!!!"
	fi
done

echo "all merges: $ALL"
echo "conflicts: $COUNT"

