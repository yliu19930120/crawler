
import logging

class LogUtil():

    @staticmethod
    def get_logger():
        logger_obj = logging.getLogger()  # 创建一个logger对象，它提供了应用程序可以直接使用的接口，其类型为“<class 'logging.RootLogger'>”；
        logger_obj.setLevel(logging.DEBUG)
        fh = logging.FileHandler("../logs/crawler.log")  # 创建一个文件输出流；
        fh.setLevel(logging.DEBUG)  # 定义文件输出流的告警级别；

        ch = logging.StreamHandler()  # 创建一个屏幕输出流；
        ch.setLevel(logging.DEBUG)  # 定义屏幕输出流的告警级别；

        formater = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 自定义日志的输出格式，这个格式可以被文件输出流和屏幕输出流调用；
        fh.setFormatter(formater)  # 添加格式花输出，即调用我们上面所定义的格式，换句话说就是给这个handler选择一个格式；
        ch.setFormatter(formater)

        logger_obj.addHandler(fh)  # logger对象可以创建多个文件输出流（fh）和屏幕输出流（ch）哟
        logger_obj.addHandler(ch)

        return logger_obj

if __name__ == '__main__':
    logger_obj = LogUtil.get_logger()
    logger_obj.info("asd")
    logger_obj.info("info")
    logger_obj.error("error")
    logger_obj.warning("warning")
    logger_obj.debug("debug")

