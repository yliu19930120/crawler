import RedisUtil

class RedisSub:
    def __init__(self,channel='CRAWLER_CHANNEL'):
        self.channel = channel
    def psubscribe(self):
        """
        订阅方法
        """
        pub = RedisUtil.RedisUtil.getRedis().pubsub()
        pub.psubscribe(self.channel)  # 同时订阅多个频道，要用psubscribe
        pub.listen()
        return pub

    def listen(self):
        pub = self.psubscribe()
        print('监听消息中...')
        while True:
            msg = pub.get_message(timeout=86400)
            print("收到订阅消息 %s" % msg['data'])


if __name__ == '__main__':
    RedisSub().listen()
