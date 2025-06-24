import os
from logging import info, error

from dotenv import load_dotenv

from src.crawler import Crawler
from src.utils.logging_utils import LoggingUtils
from src.utils.neo4j_utils import Neo4jUtils


def main():
    # 加载 .env 文件
    load_dotenv()  # 默认加载当前目录下的 .env 文件

    output_path = os.getenv("output_path") or "out"

    # 初始化 logging
    LoggingUtils.init(output_path)
    info("程序开始运行...")
    neo4j_utils = Neo4jUtils()
    try:
        crawler = Crawler(is_trace=True, output_path=output_path, neo4j_utils=neo4j_utils)
        crawler.sync_crawl()
    except KeyboardInterrupt:
        info("用户中断程序的执行")
    except Exception as e:
        error(e)
        print(e)
    finally:
        neo4j_utils.close()
        info("程序结束运行")


if __name__ == '__main__':
    main()
