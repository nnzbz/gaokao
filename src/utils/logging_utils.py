import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from logging import info, basicConfig, error


class LoggingUtils:
    """日志工具"""

    @staticmethod
    def init():
        """初始化日志"""
        # 读取配置
        logging_level = os.getenv("LOGGING_LEVEL", "INFO")
        """日志级别"""
        logging_file_name = os.getenv("LOGGING_FILE_NAME", "current.log")
        """日志文件名"""

        # 按文件大小轮转 (最大5MB，保留3个备份)
        rotating_handler = RotatingFileHandler(
            logging_file_name, maxBytes=5 * 1024 * 1024, backupCount=3
        )

        # 按时间轮转 (每天午夜创建一个新文件，保留7天)
        timed_handler = TimedRotatingFileHandler(
            logging_file_name, when='midnight', interval=1, backupCount=7
        )

        basicConfig(
            level=logging_level,
            filename=logging_file_name,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s[%(levelname)s] - %(message)s',
            handlers=[rotating_handler, timed_handler]
        )
