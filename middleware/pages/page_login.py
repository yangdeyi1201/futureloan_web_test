# author:CC
# email:yangdeyi1201@foxmail.com

from common.handler_selenium import BasePage
from selenium.webdriver.common.by import By
from middleware.handler import Handler
from middleware.pages.page_index import PageIndex


class PageLogin(BasePage):
    # 登录页手机号输入框
    login_phone_locator = (By.NAME, 'phone')
    # 登录页密码输入框
    login_pwd_locator = (By.NAME, 'password')
    # 登录按钮
    login_button_locator = (By.CLASS_NAME, 'btn-special')

    msg_incorrect_phone_locator = (By.XPATH, '//div[text()="请输入正确的手机号"]')
    msg_none_phone_locator = (By.XPATH, '//div[text()="请输入手机号"]')
    msg_none_pwd_locator = (By.XPATH, '//div[text()="请输入密码"]')
    msg_error_locator = (By.CLASS_NAME, 'layui-layer-content')

    def __init__(self, driver, timeout=20):
        super().__init__(driver=driver, timeout=timeout)

    def get(self):
        """访问登录页"""
        self.driver.get(Handler.yaml_conf['host']+'/Index/login.html')

    def login_fail(self, mobile_phone, pwd):
        """异常登录"""
        self.get()
        self.find_elem(self.login_phone_locator).send_keys(mobile_phone)
        self.find_elem(self.login_pwd_locator).send_keys(pwd)
        self.click_elem(self.login_button_locator)
        return self

    def login_success(self, mobile_phone, pwd):
        """
        正常登录
        返回首页页面对象
        """
        self.get()
        self.find_elem(self.login_phone_locator).send_keys(mobile_phone)
        self.find_elem(self.login_pwd_locator).send_keys(pwd)
        self.click_elem(self.login_button_locator)
        return PageIndex(self.driver)

    def get_msg_incorrect_phone(self):
        """请输入正确的手机号"""
        return self.get_text_of_visitable_elem(self.msg_incorrect_phone_locator)

    def get_msg_none_phone(self):
        """请输入手机号"""
        return self.get_text_of_visitable_elem(self.msg_none_phone_locator)

    def get_msg_none_pwd(self):
        """请输入密码"""
        return self.get_text_of_visitable_elem(self.msg_none_pwd_locator)

    def get_msg_error(self):
        """帐号或密码错误"""
        return self.get_text_of_visitable_elem(self.msg_error_locator)




