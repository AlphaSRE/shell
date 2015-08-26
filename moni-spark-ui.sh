#!/bin/bash
now=`date +%s`
flag=0
wget http://10.10.88.64:8080/ -O /opt/work/spark/index/index-$now
if [ $? = 0 ];then
	flag=1
fi
if [ $flag = 1 ];then
	work=`sed -n '20p' /opt/work/spark/index/index-$now |awk '{print $2}'|awk -F'<' '{print $1}'`
	if [ "$work" != "15"  ];then
		flag=0
	fi
fi
/opt/zabbix/bin/zabbix_sender -z "zabbix.adrd.sohuno.com" -s "adrd-10.16.10.190" -k spark.ui -o "${flag}"

if [[ $work -lt 10 ]];then
	bash /opt/zabbix/script/restart-spark.sh
fi
