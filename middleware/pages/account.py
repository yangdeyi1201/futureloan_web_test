# author:CC
# email:yangdeyi1201@foxmail.com

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from middleware.handler import Handler
from common.basepage import BasePage


class PageAccount(BasePage):
    account_leave_amount_locator = (By.CLASS_NAME, 'color_sub')

    def __init__(self, driver, timeout=10, poll_frequency=0.5):
        super().__init__(driver, timeout, poll_frequency)
        return

    @property
    def get_account_leave_amount(self):
        """获取个人帐户余额"""
        m_str = self.get_visitable_elem_text(locator=self.account_leave_amount_locator)
        from decimal import Decimal
        account_amount = Decimal(m_str.replace(m_str[-1], ''))
        return account_amount
