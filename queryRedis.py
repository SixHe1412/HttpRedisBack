import os
import toTimeStamp
import connRedisCluster
import time
# -*- coding: utf-8 -*-

#file to output
def outToFile(l):
    for val in l:
        if val:
            file.write(''.join(val))
    return


def query(qs):
    minlon = ''.join(qs.get('minlon', None))
    minlat = ''.join(qs.get('minlat', None))
    maxlon = ''.join(qs.get('maxlon', None))
    maxlat = ''.join(qs.get('maxlat', None))
    #d_minlon = ''.join(qs.get('d_minlon', None))
    #d_minlat = ''.join(qs.get('d_minlat', None))
    #d_maxlon = ''.join(qs.get('d_maxlon', None))
    #d_maxlat = ''.join(qs.get('d_maxlat', None))
    time_from = qs.get('time_from', None)
    time_to = qs.get('time_to', None)

    nt_from = toTimeStamp.transToStamp(time_from[0])
    nt_to = toTimeStamp.transToStamp(time_to[0])

    redis = connRedisCluster.redis_cluster()
    pl = redis.pipeline()

    tStart = time.time()
    result = os.popen(r'D:/VSProgram/SFCLib-master1/Release/sfcquery.exe -i '
                      + nt_from + '/' + nt_to + '/' + minlon + '/' + maxlon + '/'
                      + minlat + '/' + maxlat + '-s 1 -e 0 -t cttaxi.txt -n 5000 -k 12 -p 1')

    file = open('out18.txt', 'w')

    count = 0
    while 1:
        line = result.readline()
        if not line:
            break
        if line.decode('gbk').find(". . .") != -1:
            break
        pl.zrangebyscore('18level', int(line.split(',')[0]), int(line.split(',')[1]))
        count += 1
        if count >= 500:
            count = 0
            queryRes = pl.execute()
            outToFile(queryRes)
    queryRes = pl.execute()
    outToFile(queryRes)
    file.close()

    decodeRes = os.popen(r'D:\VSProgram\SFCLib-master\Release\sfcdecode.exe -i out18.txt -s 1 -e 0 -t cttaxi.txt -p 1')

    list = []
    while 1:
        res = decodeRes.readline()
        if not res:
            break
        list.append({"x":res.split(',')[2],"y":res.split(',')[3].split('\n')[0],"v":res.split(',')[0]})

    tEnd = time.time()

    print 'time use: '+ ''.join(tEnd-tStart)
    return list


#print(redis.llen("5l"))
#reslist = redis.lrange("5l",1,10)
#for val in reslist:
#    print val