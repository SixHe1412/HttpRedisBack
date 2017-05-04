import os
import toTimeStamp
import connRedisCluster

def query(qs):
    o_minlon = ''.join(qs.get('o_minlon', None))
    o_minlat = ''.join(qs.get('o_minlat', None))
    o_maxlon = ''.join(qs.get('o_maxlon', None))
    o_maxlat = ''.join(qs.get('o_maxlat', None))
    d_minlon = ''.join(qs.get('d_minlon', None))
    d_minlat = ''.join(qs.get('d_minlat', None))
    d_maxlon = ''.join(qs.get('d_maxlon', None))
    d_maxlat = ''.join(qs.get('d_maxlat', None))
    time_from = qs.get('time_from', None)
    time_to = qs.get('time_to', None)

    nt_from = toTimeStamp.transToStamp(time_from[0])
    nt_to = toTimeStamp.transToStamp(time_to[0])

    redis = connRedisCluster.redis_cluster()





#print(redis.llen("5l"))
#reslist = redis.lrange("5l",1,10)
#for val in reslist:
#    print val