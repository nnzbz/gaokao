import os
from logging import basicConfig
from logging.handlers import TimedRotatingFileHandler


class LoggingUtils:
    """日志工具"""

    @staticmethod
    def init():
        """初始化日志"""
        # 读取配置
        logging_level = os.getenv("LOGGING_LEVEL", "INFO")
        """日志级别"""
        logging_backup_retention_days = os.getenv("LOGGING_BACKUP_RETENTION_DAYS", 7)
        """备份保留天数"""
        logging_file_name = os.getenv("LOGGING_FILE_NAME", "current.log")
        """正常日志文件名"""
        error_logging_file_name = os.getenv("ERROR_LOGGING_FILE_NAME", "error.log")
        """错误日志文件名"""

        timed_rotating_file_handler = TimedRotatingFileHandler(
            logging_file_name, when='midnight', interval=1, backupCount=logging_backup_retention_days
        )
        """正常日志按时间轮转 (每天午夜创建一个新文件，保留7天)"""

        error_timed_rotating_file_handler = TimedRotatingFileHandler(
            error_logging_file_name, when='midnight', interval=1, backupCount=logging_backup_retention_days
        )
        """错误日志按时间轮转 (每天午夜创建一个新文件，保留7天)"""

        basicConfig(
            level=logging_level,
            filename=logging_file_name,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s[%(levelname)s] - %(message)s',
            handlers=[timed_rotating_file_handler, error_timed_rotating_file_handler]
        )
