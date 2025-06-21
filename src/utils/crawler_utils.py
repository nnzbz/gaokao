CLICK_OPEN_PAGE_WAIT_FOR_TIMEOUT = 500
"""点击打开页面等待超时时间"""
LOADING_PAGE_WAIT_FOR_TIMEOUT = 15000
"""加载页面等待超时时间"""


class CrawlerUtils:
    """爬取工具"""

    @staticmethod
    def click_open_page(context, home_page, click_locator, wait_for_selector):
        """
        点击打开页面
        :param context: 上下文
        :param home_page: 点击的主页面
        :param click_locator: 点击的定位器
        :param wait_for_selector: 等待的选择器
        :return: 打开的新页面
        """
        try:
            click_locator.click()
            home_page.wait_for_timeout(CLICK_OPEN_PAGE_WAIT_FOR_TIMEOUT)
            # home_page.wait_for_load_state("networkidle")
            opened_page = context.pages[len(context.pages) - 1]
            # opened_page.wait_for_load_state("networkidle")
            opened_page.wait_for_selector(wait_for_selector, timeout=LOADING_PAGE_WAIT_FOR_TIMEOUT)
            return opened_page
        except Exception as e:
            print(e)
            return None
