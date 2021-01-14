# author:CC
# email:yangdeyi1201@foxmail.com

from common.handler_selenium import BasePage
from selenium.webdriver.common.by import By


class PageInvest(BasePage):
    # 投标成功
    invest_success_locator = (By.XPATH, '//div[text()="投标成功！"]')
    # 查看并激活
    check_and_confirm_locator = (By.XPATH, '//div[@class="layui-layer-content"]//button[text()="查看并激活"]')
    # 投资金额输入框
    invest_input_locator = (By.CSS_SELECTOR, '.invest-unit-investinput')
    # 投标按钮
    invest_button_locator = (By.XPATH, '//button[contains(@class, "btn btn-special")]')
    # 请正确填写投标金额
    msg_incorrect_money_locator = (By.XPATH, '//*[text()="请正确填写投标金额"]')
    # 请输入10的整数倍
    msg_not_ten_times_locator = (By.XPATH, '//*[text()="请输入10的整数倍" and @disabled]')
    # 投标金额大于可用金额
    msg_more_than_account_leaveamount_locator = (By.XPATH, '//*[text()="投标金额大于可用金额"]')
    # 投标金额大于标剩余金额
    msg_more_than_bid_leaveamount_locator = (By.XPATH, '//*[text()="购买标的金额不能大于标剩余金额"]')
    # 投标金额大于标总金额
    msg_more_than_bid_total_amount_locator = (By.XPATH, '//*[text()="购买标的金额不能大于标总金额"]')
    # 投资金额为空投标按钮置灰
    msg_disabled_invest_locator = (By.XPATH, '//*[text()="投标" and @disabled]')
    # 请输入手机号
    msg_please_input_phone_locator = (By.XPATH, '//*[@name="phone" and @placeholder]')
    # 请输入密码
    msg_please_input_pwd_locator = (By.XPATH, '//*[@name="password" and @placeholder]')
    # 登录按钮
    msg_login_locator = (By.XPATH, '//*[@_lpchecked]//*[text()="登录"]')

    def __init__(self, driver, timeout=20):
        super().__init__(driver=driver, timeout=timeout)

    def invest(self, amount):
        """
        1、输入投资金额
        2、点击投标按钮
        """
        self.find_elem(self.invest_input_locator).send_keys(amount)
        self.click_elem(self.invest_button_locator)
        return self

    def get_msg_success_invest(self):
        """获取投标成功的断言元素"""
        invest_success = self.get_text_of_visitable_elem(self.invest_success_locator)
        check_and_confirm = self.get_text_of_clickable_elem(self.check_and_confirm_locator)
        return invest_success, check_and_confirm
