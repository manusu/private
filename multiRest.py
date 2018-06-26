import datetime
import requests
import random
import time
import sys
loopsum = int(sys.argv[1])
limit = int(sys.argv[2])
print loopsum,limit
dis = {0:"content",1:"mediafile"}
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
    code = requests.get("http://10.199.8.59:80/staticdata/%s/%d/%d/%d.json"%(v4,v1,v2,v3)).status_code
    newtime=datetime.datetime.now()
    if code!=404:
        count2+=1
    ms = (newtime-oldtime).microseconds
    if ms>maxtime:
        maxtime = ms
    if ms>limit:
        print '%s'%(newtime-oldtime)
        uptimes+=1
        #print 'start:%s,end:%s'%(oldtime,newtime)
        #print "http://10.199.8.186:80/staticdata/%s/%d/%d/%d.json"%(v4,v1,v2,v3)

    #print '%s'%(newtime-oldtime)
    #print 'us %s'%(newtime-oldtime).microseconds
    #time.sleep(0.1)
    if count>loopsum:
        print 'total %d'%loopsum
        print 'maxtime %d'%maxtime
        print count2
        print 'more than 100ms %d'%uptimes
        break
