from rediscluster import StrictRedisCluster
import sys

def redis_cluster():
    redis_nodes =  [{'host':'192.168.0.20','port':7006},
                    {'host':'192.168.0.27','port':7000},
                    {'host':'192.168.0.28','port':7001},
                    {'host':'192.168.0.29','port':7002},
                    {'host':'192.168.0.31','port':7004},
                    {'host':'192.168.0.32','port':7005}
                   ]
    try:
        redis = StrictRedisCluster(startup_nodes = redis_nodes)
    except Exception,e:
        print "Connect Error!"
        sys.exit(1)
    return redis