import RedisUtil
# import LogUtil
import LogUtil
import tasks


class RedisSub:
    def __init__(self,channel='CRAWLER_CHANNEL'):
        self.channel = channel
        self.log = LogUtil.LogUtil.get_logger()
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
        self.log.info('监听消息中...')
        while True:
            full_msg = pub.get_message(timeout=86400)
            msg = full_msg['data']
            self.log.info("收到订阅消息 %s" , msg)
            tasks.Task().runJob(msg)

if __name__ == '__main__':
    RedisSub().listen()
