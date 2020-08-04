# author:CC
# email:yangdeyi1201@foxmail.com

from selenium.webdriver.common.by import By
from middleware.handler import Handler
from common.basepage import BasePage
from selenium.webdriver.support import expected_conditions


class PageAccount(BasePage):
    account_leave_amount_locator = (By.CSS_SELECTOR, '.per_list_right>.color_sub')

    def __init__(self, driver, timeout=30, poll_frequency=0.5):
        super().__init__(driver, timeout, poll_frequency)
        self.wait.until(expected_conditions.title_contains(title='个人中心'))
        return

    @property
    def get_account_leave_amount(self):
        """获取个人帐户余额"""
        amount_with_unit = self.get_visitable_elem_text(locator=self.account_leave_amount_locator)
        account_leave_amount = amount_with_unit.replace(amount_with_unit[-1], '')
        return eval(account_leave_amount)
