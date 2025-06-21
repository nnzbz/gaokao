import os
from logging import info, basicConfig, error

from dotenv import load_dotenv

from src.crawler import Crawler
from src.utils.logging_utils import LoggingUtils


def main():
    # 加载 .env 文件
    load_dotenv()  # 默认加载当前目录下的 .env 文件

    output_path = os.getenv("output_path", "./out")

    # 初始化 logging
    LoggingUtils.init()
    info("程序开始运行...")
    try:
        # 开始同步爬取数据
        crawler = Crawler(is_trace=True, output_path=output_path)
        crawler.sync_crawl()
    except KeyboardInterrupt:
        info("用户中断程序的执行")
    except Exception as e:
        error(e)
    finally:
        info("程序结束运行")


if __name__ == '__main__':
    main()
