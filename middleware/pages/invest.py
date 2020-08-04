# author:CC
# email:yangdeyi1201@foxmail.com

from common.basepage import BasePage
from selenium.webdriver.common.by import By
from middleware.pages.account import PageAccount


class PageInvest(BasePage):
    invest_input_locator = (By.CLASS_NAME, 'invest-unit-investinput')
    invest_button_locator = (By.XPATH, '//button[text()="投标"]')

    success_msg_locator = (By.XPATH, '//a[text()="我的帐户[小蜜蜂146177499]"]')
    msg_success_invest_locator = (By.XPATH, '//div[text()="投标成功！"]')
    msg_check_and_activate_locator = (By.XPATH, '''//div[@class='layui-layer-content']//button[@onclick="location.href='/Member/index'"]''')
    msg_incorrect_money_locator = (By.XPATH, '//*[text()="请正确填写投标金额"]')
    msg_not_100_times_locator = (By.XPATH, '//div[text()="投标金额必须为100的倍数"]')
    msg_not_more_than_bid_amount_locator = (By.XPATH, '//div[text()="购买标的金额不能大于标剩余金额"]')
    msg_not_more_than_account_amount_locator = (By.XPATH, '//div[text()="投标金额大于可用金额"]')
    msg_bid_expired_locator = (By.XPATH, '//div[text()="投标期限已经过了！"]')
    bid_leave_amount_locator = (By.CLASS_NAME, 'money-left')
    confirm_warning_locator = (By.LINK_TEXT, '确认')

    def __init__(self, driver, timeout=10, poll_frequency=0.5):
        super().__init__(driver, timeout, poll_frequency)
        return

    def invest_no_input(self, money):
        """不输入投资金额"""
        self.write(locator=self.invest_input_locator, value=money)
        return self

    def invest_input_money(self, money):
        """输入投资金额并点投标按钮"""
        self.write(locator=self.invest_input_locator, value=money)
        self.click(locator=self.invest_button_locator)
        return self

    def confirm_warning(self):
        """点击确认关闭异常投资提示"""
        self.click(locator=self.confirm_warning_locator)
        return

    def confirm_activate(self):
        """
        点击确认并激活提示
        返回个人帐户页面
        """
        self.click(locator=self.msg_check_and_activate_locator)
        return PageAccount(self.driver)

    def get_msg_no_input(self):
        """不输入投资金额时，投资按钮应置灰"""
        return self.get_attribute(locator=self.invest_button_locator, name='disabled')

    def get_msg_incorrect_money(self):
        """请正确填写投标金额与确认"""
        actual_message = self.get_visitable_elem_text(locator=self.msg_incorrect_money_locator)
        actual_confirm = self.get_clickable_elem_text(locator=self.confirm_warning_locator)
        return actual_message, actual_confirm

    def get_msg_please_login(self):
        """请先登录"""
        from middleware.pages.login import PageLogin
        input_phone = self.get_attribute(locator=PageLogin.username_locator, name='placeholder')
        input_pwd = self.get_attribute(locator=PageLogin.pwd_locator, name='placeholder')
        click_login = self.get_clickable_elem_text(locator=(By.XPATH, '//button[text()="登录"]'))
        tip = self.get_visitable_elem_text(locator=(By.CLASS_NAME, 'layui-layer-title'))
        return input_phone, input_pwd, click_login, tip

    def get_msg_not_100_times(self):
        """投标金额必须为 100 正整数倍"""
        actual_message = self.get_visitable_elem_text(locator=self.msg_not_100_times_locator)
        actual_confirm = self.get_clickable_elem_text(self.confirm_warning_locator)
        return actual_message, actual_confirm

    def get_msg_not_more_than_bid_amount(self):
        """购买标的金额不能大于标剩余金额"""
        actual_message = self.get_visitable_elem_text(locator=self.msg_not_more_than_bid_amount_locator)
        actual_confirm = self.get_clickable_elem_text(locator=self.confirm_warning_locator)
        return actual_message, actual_confirm

    def get_msg_not_more_than_account_leave_amount(self):
        """投标金额大于可用金额"""
        actual_message = self.get_visitable_elem_text(locator=self.msg_not_more_than_account_amount_locator)
        actual_confirm = self.get_clickable_elem_text(locator=self.confirm_warning_locator)
        return actual_message, actual_confirm

    def get_msg_success(self):
        """获取投资成功的预期结果"""
        actual_success = self.get_visitable_elem_text(locator=self.msg_success_invest_locator)
        actual_activate = self.get_clickable_elem_text(locator=self.msg_check_and_activate_locator)
        return actual_success, actual_activate

    def get_msg_bid_expired(self):
        """
        投标期限已经过了！
        确认
        """
        actual_message = self.get_visitable_elem_text(locator=self.msg_bid_expired_locator)
        actual_confirm = self.get_clickable_elem_text(locator=self.confirm_warning_locator)
        return actual_message, actual_confirm

    @property
    def generate_more_than_bid_leave_amount(self):
        """产生投资金额：大于标剩余金额且小于等于帐户余额且为 100 正整数倍"""
        amount_with_unit = self.get_visitable_elem_text(locator=self.bid_leave_amount_locator).split('：')[1]
        from decimal import Decimal
        if amount_with_unit[-1] == '万':
            bid_leave_amount = Decimal(amount_with_unit.replace(amount_with_unit[-1], ''))*Decimal(str(10000))
            more_than_bid_leave_amount = bid_leave_amount+Decimal(str(100))
        elif amount_with_unit[-1] == '元':
            bid_leave_amount = Decimal(amount_with_unit.replace(amount_with_unit[-1], ''))
            more_than_bid_leave_amount = bid_leave_amount+Decimal(str(100))
        return more_than_bid_leave_amount

    @staticmethod
    def generate_more_than_account_leave_amount(account_leave_amount):
        """
        account_leave_amount：个人帐户余额
        产生投资金额：大于个人帐户余额且为 100 正整数倍
        """
        import math
        from random import randint
        ceil_account_leave_amount = math.ceil(account_leave_amount)
        while True:
            more_than_account_amount = randint(ceil_account_leave_amount,
                                               ceil_account_leave_amount + 10000)  # math.ceil() 向上取整
            if more_than_account_amount % 100 == 0:
                return more_than_account_amount
