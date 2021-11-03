import logging
from datetime import datetime
import threading
import readConfig
import os


class Log:
    def __init__(self):
        global log_path, result_path, absolute_path  # 日志路径， 默认路径， 绝对路径
        absolute_path = readConfig.absolute_path
        result_path = os.path.join(absolute_path, "result")

        if not os.path.exists(result_path):
            os.mkdir(result_path)

        log_path = os.path.join(result_path, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # 第一步，创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # 第二步，创建一个handler，用于写入日志文件
        handler = logging.FileHandler(os.path.join(log_path, "output.log"))
        handler.setLevel(logging.DEBUG)
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - 【%(filename)s - %(lineno)d】- %(message)s')
        handler.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name + " - Code:" + str(code) + " - msg:" + msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(log_path, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return log_path

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(log_path, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.logger.error(str(ex))  # 与原文不同


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod  # 静态方法，无须实例化调用
    def get_log():
        if MyLog.log is None:
            # 先要获取锁
            MyLog.mutex.acquire()
            # 调用上面的 log
            MyLog.log = Log()
            # 最后释放锁
            MyLog.mutex.release()
        return MyLog.log


if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")