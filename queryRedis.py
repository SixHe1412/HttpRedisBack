import os
import toTimeStamp
import connRedisCluster
import time
import pandas as pd
# -*- coding: utf-8 -*-

#file to output
def outToFile(l,file):
    for val in l:
        if val:
            file.write(''.join(val))
    return


def query(qs):
    tStart = time.time()
    minlon = qs.get('minlon', None)[0]
    minlat = qs.get('minlat', None)[0]
    maxlon = qs.get('maxlon', None)[0]
    maxlat = qs.get('maxlat', None)[0]
    #d_minlon = ''.join(qs.get('d_minlon', None))
    #d_minlat = ''.join(qs.get('d_minlat', None))
    #d_maxlon = ''.join(qs.get('d_maxlon', None))
    #d_maxlat = ''.join(qs.get('d_maxlat', None))
    #time_from = qs.get('time_from', None)
    #time_to = qs.get('time_to', None)
    time_from = ''.join(qs.get('time_from', None))
    time_to = ''.join(qs.get('time_to', None))

    #nt_from = toTimeStamp.transToStamp(time_from[0])
    #nt_to = toTimeStamp.transToStamp(time_to[0])

    redis = connRedisCluster.redis_cluster()
    pl = redis.pipeline()

    file = open('out1612.txt', 'w')
    para = time_from + '/' + time_to + '/' + minlon + '/' + maxlon + '/' + minlat + '/' + maxlat
    result = os.popen(r'D:/VSProgram/SFCLib-master1/Release/sfcquery.exe -i '+ para
                      + ' -s 1 -e 0 -t cttaxi.txt -n 5000 -k 12 -p 1')

    tEnd = time.time()
    print tEnd - tStart


    count = 0
    while 1:
        line = result.readline()
        if not line:
            break
        if line.decode('gbk').find(". . .") != -1:
            break
        pl.zrangebyscore('1612sumlvl', int(line.split(',')[0]), int(line.split(',')[1]))
        count += 1
        if count >= 500:
            count = 0
            queryRes = pl.execute()
            outToFile(queryRes,file)
    queryRes = pl.execute()
    outToFile(queryRes,file)
    file.close()

    tEnd = time.time()
    print tEnd - tStart

    #decodeRes = os.popen(r'D:\VSProgram\SFCLib-master\Release\sfcdecode.exe -i out1612.txt -s 1 -e 0 -t cttaxi.txt -p 1')
    os.popen(r'D:\VSProgram\SFCLib-master\Release\sfcdecode.exe -i out1612.txt -o decode.txt -s 1 -e 0 -t cttaxi.txt -p 1')

    tEnd = time.time()
    print tEnd - tStart

    #tempdict = {}
    #list = []
    #while 1:
    #    res = decodeRes.readline()
    #    if not res:
    #        break
    #    list.append({"x":float(res.split(',')[3].split('\n')[0]),"y":float(res.split(',')[2]),"v":int(res.split(',')[0])})

    #while 1:
    #    res = decodeRes.readline()
    #    if not res:
    #        break
    #    x = res.split(',')[3].split('\n')[0]
    #    y = res.split(',')[2]
    #    v = int(res.split(',')[0])
    #    k = x + ',' + y
    #    if tempdict.has_key(k):
    #        tempdict[k] += v
    #    else:
    #        tempdict[k] = v
    #for val in tempdict:
    #     list.append({"x":float(str(val).split(',')[0]),"y":float(str(val).split(',')[1]),"v":int(tempdict.get(val))})


    df = pd.read_table('decode.txt', sep=',', index_col=False, na_filter=False)
    df = df.groupby(['x','y'],as_index=False)['v'].sum()

    list = df.to_json(orient='records')

    tEnd = time.time()
    print tEnd-tStart

    return list
