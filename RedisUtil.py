import redis    # 导入redis模块，通过python操作redis 也可以直接在redis主机的服务端操作缓存数据库

class RedisUtil:
    @staticmethod
    def getRedis():
        pool = redis.ConnectionPool(host='redis_server', port=6379,
                                    decode_responses=True)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
        r = redis.Redis(connection_pool=pool)
        return  r




