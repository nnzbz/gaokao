import os
from logging import debug


class FileUtils:
    """文件工具"""

    @staticmethod
    def write_file(output_path, file_name, content):
        """
        输出文件
        :param output_path: 输出路径
        :param file_name: 文件名称
        :param content: 文件内容
        """
        full_path = os.path.join(output_path, file_name)
        debug(f"输出文件：{full_path}")
        os.makedirs(output_path, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def create_directory(file_path):
        """
        创建目录
        :param file_path: 文件路径
        """
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
