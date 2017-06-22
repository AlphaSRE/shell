#!/bin/bash


for i in `cat $1`
do
	ssh $i 'echo "ssh-rsa " >> /root/.ssh/authorized_keys'
done
