import redis

import pickle
from DD import lib
############

useRedis = redis.Redis(
host = lib.redisHost,
port = lib.redisPort,
password = lib.redisPwd
)
####
##
##
def varPop(_key):
    #######
    Tmp = pickle.loads(useRedis.get(_key))
    Tmp.pop(list(Tmp.keys())[0])
    useRedis.set(_key, pickle.dumps(Tmp))

############3
##
##
def varSet(_key,_value):
    useRedis.set(_key, pickle.dumps(_value))

#def varGet(_key):
#    return useRedis.get(_key)
############33
##
##
def varGetsize():
    return useRedis.dbsize()

##########
##
##
def varGetbyte2dict(_key):
    return pickle.loads(useRedis.get(_key))