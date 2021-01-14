# author:CC
# email:yangdeyi1201@foxmail.com

from common.handler_selenium import BasePage
from selenium.webdriver.common.by import By
from middleware.pages.page_invest import PageInvest


class PageIndex(BasePage):
    msg_account_locator = (By.LINK_TEXT, '我的帐户[小蜜蜂146177499]')
    invest_list_locator = (By.LINK_TEXT, '投标')

    def __init__(self, driver, timeout=20):
        super().__init__(driver=driver, timeout=timeout)

    def get_msg_account(self):
        """成功登录后首页我的账户元素"""
        return self.get_text_of_clickable_elem(self.msg_account_locator)

    def into_invest_list(self):
        """切换至投标列表页"""
        self.click_elem(self.invest_list_locator)
        return PageInvest(self.driver)
