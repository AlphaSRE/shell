#!/usr/bin/env python
#coding:utf-8

"""
moni-flume-job.py
~~~~~~~~~~~~~~

check the channel of flume job status

Usage:python2.7 ./moni-storm-job.py 'url' 'channelname' 'json.key'
python moni-flume-job.py http://10.16.10.54:34545/metrics ctestfk ChannelFillPercentage

"""

import os
import sys
import json
import pickle
import socket
import urllib2
import subprocess
import re
import time


def html_extension(baseurl,channel):        #for flume1.5
    html = urllib2.urlopen(baseurl).read()
    data = json.loads(html)
    checkchannel = 'CHANNEL'+'.'+channel
    d = {}
    for (k, v) in data[checkchannel].items():
        if (k == 'ChannelFillPercentage' or k == 'EventPutSuccessCount' or k == 'EventTakeSuccessCount'):
            d[k] = v
    return d


def result_cmp(now,previous,checkitem):
    flag = 1
    for k1, v1 in previous.items():
        if k1 == checkitem:
            old = v1
    for k2, v2 in now.items():
        if k2 == checkitem:
            new = v2
    if checkitem == 'ChannelFillPercentage':
        if float(new) > 3:flag = 0;
    else:
        if old == new:flag = 0
    return flag


def get_file(checkfile):
    if os.path.exists(checkfile) is False:     #如果没有检测文件,则返回错误值,主函数判断后将结果写入
        print 'file not frond && mkdir'
        return 65

    with open(checkfile, 'r') as fr:            #文件存在,获取结果发报警
        return pickle.load(fr)


def sync_file(checkfile,newresult):
    if os.path.exists(checkfile) is False:     #如果没有检测文件,则写入结果后直接退出
        fw = open(checkfile, 'w')
        pickle.dump(newresult, fw)
        fw.close()
        sys.exit()

    with open(checkfile, 'w') as fw:            #文件存在,获取结果发报警
        pickle.dump(newresult, fw)
        fw.close()


if __name__ == '__main__':

    baseurl = sys.argv[1]
    channel = sys.argv[2]
    checkitem = sys.argv[3]
    checkip = re.match(r'http://(.*)\:', baseurl).group(1)
    checkfile = '/opt/monitor/flume/check-flumejob-'+channel+'-'+checkitem+'-'+checkip+'.log'

    oldresult = get_file(checkfile)

    try:
        newresult = html_extension(baseurl, channel)
    except IndexError, e:
        print e
        print 'Enter job or json.key does not exist !!!'
        command = '/opt/zabbix/bin/zabbix_sender -z "zabbix.adrd.sohuno.com" -s "adrd-'+checkip+'" -k flume2kafka.'+channel+' -o 0'
        print command
        subprocess.call(command, shell=True)
        sys.exit()
    except urllib2.URLError, e:
        print e
        print 'Enter the URL is incorrect !!!'
        command = '/opt/zabbix/bin/zabbix_sender -z "zabbix.adrd.sohuno.com" -s "adrd-'+checkip+'" -k flume2kafka.'+channel+' -o 0'
        subprocess.call(command, shell=True)
        sys.exit()

    sync_file(checkfile, newresult)

    if oldresult == 65:sys.exit()

    try:
        flag = result_cmp(newresult, oldresult, checkitem)
    except UnboundLocalError, e:
        print e
        print 'Enter job or json.key does not exist !!!'
        sys.exit()

    command = '/opt/zabbix/bin/zabbix_sender -z "zabbix.adrd.sohuno.com" -s "adrd-'+checkip+'" -k flume2kafka.'+channel+' -o '+str(flag)
    print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
    print command
    print newresult
    print "=================================================================="
    subprocess.call(command, shell=True)
    status_command = '/opt/zabbix/bin/zabbix_sender -z "zabbix.adrd.sohuno.com" -s "adrd-'+checkip+'" -k flume2kafka.'+channel+' -o 1'
    subprocess.call(status_command, shell=True)
