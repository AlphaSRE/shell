#!/bin/sh

hosts=`cat $1`;
CMD=$2;

for i in ${hosts}; do
	echo ${i};
	ssh ${i} "$CMD";
	while [ 1 -eq 1 ]
	do
	  read -p "y or n?" OPTION
	  case "$OPTION" in
	  y)
	    echo "go on!"
	    break
	    ;;
	  n)
	    exit 1
	    ;;
	  *)
	    continue
	  esac
	done
done

