#!/bin/bash


for i in `cat $1`
do
	ssh $i 'echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA2/zrurPaT0dyqcTY5aT2/ZvIQfHTHVXz3XDaFHkrF2BbEvC3e4OvWbLhf+BC8+pXYw7ev6cYQBmr/tgFWvT/ory2YVlGP6N+2HqD04W8I94fJ0Tfj9AlyoXr8od8wv2WtwACDRXYja1Z9fHejhy6YBjfwEUSPhF7QWqik0qNO6alMXZ1NmgGccfIuJexBNquqb7tyCfXKvqzvQd2xNHPdAlpBi06qq6mFFtNGa9nE2+RiKg3HmGEV3blmIfjcBjaIymUjKy0GrZpy1fpXhaMtpNBS+Aaqj5UgS/lowYor4MBEyMLfT01yNVXVRQZJFJSJtHm5PXtw/XMWgnPuSnjIw== root@bx_10_190" >> /root/.ssh/authorized_keys'
done
