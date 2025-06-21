import os
from logging import info, debug, warn, error

from html2text import HTML2Text
from playwright.sync_api import sync_playwright, Locator

from src.utils.crawler_utils import CrawlerUtils
from src.utils.file_utils import FileUtils


class Crawler:
    """
    爬虫类
    """
    html2text: HTML2Text
    """Html转Markdown工具"""
    is_trace: bool
    """是否启动跟踪功能"""
    output_path: str
    """输出路径"""

    def __init__(self, is_trace: bool, output_path: str):
        """
        初始化
        :param is_trace: 是否启动跟踪功能
        :param output_path: 输出路径
        """
        self.is_trace = is_trace
        self.output_path = output_path
        # 创建 html2text 对象
        self.html2text = HTML2Text()

    def sync_crawl(self):
        """
        同步爬取数据
        """
        p = sync_playwright().start()
        browser = p.firefox.launch(headless=True)

        # 创建 BrowserContext对象
        context = browser.new_context()
        # 是否启动跟踪功能
        if self.is_trace:
            context.tracing.start(snapshots=True, sources=True, screenshots=True)

        try:
            # 打开页面
            page = context.new_page()
            # page.goto("https://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerifedZszc--method-index,lb-1.dhtml")
            page.goto("https://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerifedZszc--method-index,ssdm-,yxls-,xlcc-,zgsx-,yxjbz-,start-2900.dhtml")
            page.wait_for_selector(".sch-list-container")
            info(f'标题: {page.title()}')

            # 遍历学校的招生章程
            while True:
                self.loop_zszc(context, page)
                next_a = page.locator(".ivu-page-next")
                class_attr = next_a.get_attribute("class")
                if "ivu-page-disabled" in class_attr:
                    break
                next_a.click()
                page.wait_for_load_state("networkidle")
        finally:
            # 如果启动了跟踪功能，则结束跟踪
            if self.is_trace:
                context.tracing.stop(path="trace.zip")

            browser.close()
            p.stop()

    def loop_zszc(self, context, page):
        zch_item_list = page.locator(".sch-list-container .sch-item").all()
        for zszc_item in zch_item_list:
            college_name = zszc_item.locator(".name").inner_text().strip()
            """学校名称"""
            # 判断是否有数据
            if zszc_item.locator(".no-info").count() > 0:
                warn(f"警告: {college_name}没有招生章程的页面")
                continue

            new_page1 = CrawlerUtils.click_open_page(context, page, zszc_item.locator(".zszc-link"), ".zszcdel")
            if new_page1 is None:
                error(f"错误: 打开{college_name}招生章程报错")
                continue

            title = new_page1.locator(".gk-mdgs-title").text_content().strip()
            # 判断是否有数据
            if new_page1.locator("noInfoTxt").count() > 0:
                warn(f"警告: {college_name}没有招生章程")
                continue

            yz_zszc_list = new_page1.locator(".zszc-zc-title").all()
            yz_zszc_count = len(yz_zszc_list)
            """院校招生章程列表"""
            for yz_zszc in yz_zszc_list:
                new_page2 = CrawlerUtils.click_open_page(context, page, yz_zszc, ".zszc-content")
                if yz_zszc_count > 1:
                    title = new_page2.locator(".zszc-content-title").text_content().strip()
                self.save_page_content(title, new_page2.locator(".zszc-content"))
                new_page2.close()

            new_page1.close()

    def save_page_content(self, title, locator: Locator):
        """
        保存页面内容
        :param title: 标题
        :param locator: 定位器
        """
        markdown_file_name = f"{title}.md"
        markdown_file_full_path = os.path.join(self.output_path, markdown_file_name)
        png_file_name = f"{title}.png"
        png_file_full_path = os.path.join(self.output_path, png_file_name)
        page_content = self.html2text.handle(locator.inner_html())

        if os.path.exists(markdown_file_full_path):
            warn(f"文件已存在：{markdown_file_full_path}")
            return
        info(f"保存网页内容：{title}")

        debug(f"保存快照: {png_file_full_path}")
        locator.screenshot(path=png_file_full_path)
        debug(f"保存文本: {markdown_file_full_path}")
        FileUtils.write_file(self.output_path, markdown_file_name, page_content)
