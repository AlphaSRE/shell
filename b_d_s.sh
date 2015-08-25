#!/bin/sh

hosts=`cat $1`;
CMD=$2;

for i in ${hosts}; do
	echo ${i};
	ssh ${i} "$CMD";
	sleep 2;
done

