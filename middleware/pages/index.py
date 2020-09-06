# author:CC
# email:yangdeyi1201@foxmail.com

from selenium.webdriver.common.by import By
from common.basepage import BasePage
from middleware.handler import Handler
from middleware.pages.invest import PageInvest
from middleware.pages.account import PageAccount


class PageIndex(BasePage):
    index_url = Handler.yaml_conf['host']

    success_msg_locator = (By.XPATH, '//a[text()="我的帐户[小蜜蜂146177498]"]')
    invest_list_locator = (By.LINK_TEXT, '投标')

    def __init__(self, driver, timeout=30, poll_frequency=0.5):
        super().__init__(driver, timeout, poll_frequency)
        return

    def get_homepage(self):
        """登录前程贷官网首页"""
        self.driver.get(self.index_url)
        return self

    def get_success_msg(self):
        """获取正常登录的预期结果"""
        return self.get_visitable_elem_text(locator=self.success_msg_locator)

    def get_invest_list(self):
        """
        首页切换至投标列表页
        返回投标列表页面
        """
        self.click(locator=self.invest_list_locator)
        return PageInvest(self.driver)

    def into_my_account(self):
        """
        进入我的账户
        返回我的账户页面
        """
        self.click(locator=self.success_msg_locator)
        return PageAccount(self.driver)
