import datetime
import requests
import random
import time
import sys
import threading
import logging
iplist = [
'10.199.8.2',
'10.199.8.59',
'10.199.8.105',
'10.199.8.95',
'10.199.8.99',
'10.199.8.242',
'10.199.8.36',
'10.199.8.158',
'10.199.8.27',
'10.199.8.137',
'10.199.8.186',
'10.199.8.30',
'10.199.8.154',
'10.199.8.39',
'10.199.8.236'
]
logging.basicConfig(filename='./restmul.log',format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level = logging.WARN,filemode='w',datefmt='%Y-%m-%d%I:%M:%S %p')
dis = {0:"content",1:"mediafile"}

def sendrest(ip,loopsum,limit):
    print ip
    time.sleep(5)
    count = 0
    count2 = 0
    maxtime = 0
    uptimes = 0
    while True:
        count+=1
        v1=random.uniform(600, 641)
        v2=random.uniform(100, 999)
        v3=random.uniform(100, 999)
        v4=dis[count%2]
        oldtime=datetime.datetime.now()
        code = requests.get("http://%s:80/staticdata/%s/%d/%d/%d.json"%(ip,v4,v1,v2,v3)).status_code
        newtime=datetime.datetime.now()
        if code!=404:
            count2+=1
        ms = (newtime-oldtime).microseconds
        if ms>maxtime:
            maxtime = ms
        if ms>limit:
            strinfo = '%s'%(newtime-oldtime) + 'start:%s,end:%s'%(oldtime,newtime) + "http://%s:80/staticdata/%s/%d/%d/%d.json"%(ip,v4,v1,v2,v3)
            logging.error(strinfo)
            uptimes+=1
        if count>loopsum:
            logging.warn('total %d,maxtime %d,suc %d,more than limit sum%d'%(loopsum,maxtime,count2,uptimes))
            break

if __name__=='__main__':
    loopsum = int(sys.argv[1])
    #limit = int(sys.argv[2])
    limit = 100000
    threads = []
    for i in range(0,8):
        t1 = threading.Thread(target=sendrest,args=(iplist[i],loopsum,limit))
        threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
