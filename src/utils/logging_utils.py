import os
from logging import basicConfig, StreamHandler, DEBUG, WARNING
from logging.handlers import TimedRotatingFileHandler

from src.utils.file_utils import FileUtils


class LoggingUtils:
    """日志工具"""

    @staticmethod
    def init(output_path):
        """初始化日志
        :param output_path: 输出路径
        """
        # 读取配置
        logging_level = os.getenv("LOGGING_LEVEL") or "INFO"
        """日志级别"""
        logging_backup_when = os.getenv("LOGGING_BACKUP_WHEN") or "midnight"
        """日志备份时间"""
        logging_backup_interval = os.getenv("LOGGING_BACKUP_INTERVAL") or 1
        """日志备份间隔(默认为1)"""
        logging_backup_retention_days = os.getenv("LOGGING_BACKUP_RETENTION_DAYS") or 7
        """备份保留天数"""
        logging_file_name = os.getenv("LOGGING_FILE_NAME") or "log/current.log"
        """正常日志文件名"""
        logging_error_file_name = os.getenv("LOGGING_ERROR_FILE_NAME") or "log/error.log"
        """错误日志文件名"""

        # 控制台
        console_handler = StreamHandler()
        console_handler.setLevel(logging_level)  # 控制台可以设置不同的日志级别

        # 日志
        logging_file_path = os.path.join(output_path, logging_file_name)
        FileUtils.create_directory(logging_file_path)
        file_handler = TimedRotatingFileHandler(
            filename=logging_file_path, when=logging_backup_when, interval=logging_backup_interval, backupCount=logging_backup_retention_days
        )
        """日志按时间备份"""
        file_handler.setLevel(logging_level)

        # 错误日志
        logging_error_file_path = os.path.join(output_path, logging_error_file_name)
        FileUtils.create_directory(logging_error_file_path)
        error_file_handler = TimedRotatingFileHandler(
            filename=logging_error_file_path, when=logging_backup_when, interval=logging_backup_interval, backupCount=logging_backup_retention_days
        )
        """错误日志按时间备份"""
        error_file_handler.setLevel(WARNING)

        # 配置日志
        basicConfig(
            level=DEBUG,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s[%(levelname)s] - %(message)s',
            handlers=[console_handler, file_handler, error_file_handler]
        )
