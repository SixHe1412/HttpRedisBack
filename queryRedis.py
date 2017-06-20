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
    tStart1 = time.time()
    minlon = qs.get('minlon', None)[0]
    minlat = qs.get('minlat', None)[0]
    maxlon = qs.get('maxlon', None)[0]
    maxlat = qs.get('maxlat', None)[0]

    time_from = qs.get('time_from', None)[0]
    time_to = qs.get('time_to', None)[0]
    #print time_from+' '+ time_to
    nt_from = toTimeStamp.transToStamp(time_from)
    nt_to = toTimeStamp.transToStamp(time_to)

    lvl = qs.get('level', None)[0]
    print lvl
    lvlcommand = lvl + '.exe -i '
    lvlquery = lvl + 'lvl'

    redis = connRedisCluster.redis_cluster()
    pl = redis.pipeline()

    file = open('out16.txt', 'w')
    para = nt_from + '/' + nt_to + '/' + minlon + '/' + maxlon + '/' + minlat + '/' + maxlat
    #print para
    result = os.popen(r'D:/VSProgram/SFCLib-master1/Release/sfcquery' + lvlcommand + para
                      + ' -s 1 -e 0 -t cttaxi.txt -n 5000 -k 12 -p 1')

    tStart2 = time.time()
    print tStart2 - tStart1

    count = 0
    while 1:
        line = result.readline()
        if not line:
            break
        if line.decode('gbk').find(". . .") != -1:
            break
        pl.zrangebyscore(lvlquery, int(line.split(',')[0]), int(line.split(',')[1]))
        count += 1
        if count >= 1000:
            count = 0
            queryRes = pl.execute()
            outToFile(queryRes,file)
    queryRes = pl.execute()
    outToFile(queryRes,file)
    file.close()

    tStart3 = time.time()
    print tStart3 - tStart2

    #decodeRes = os.popen(r'D:\VSProgram\SFCLib-master\Release\sfcdecode.exe -i out1612.txt -s 1 -e 0 -t cttaxi.txt -p 1')
    os.popen(r'D:\VSProgram\SFCLib-master\Release\sfcdecode' + lvlcommand + 'out16.txt -o decode.txt -s 1 -e 0 -t cttaxi.txt -p 1')

    tStart4 = time.time()
    print tStart4 - tStart3

    df = pd.read_table('decode.txt', sep=',', index_col=False, na_filter=False)
    print len(df)
    df = df.groupby(['x','y'],as_index=False)['v'].sum()

    list = df.to_json(orient='records')

    tEnd = time.time()
    print tEnd-tStart4
    print tEnd - tStart1

    return list
