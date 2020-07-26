# author:CC
# email:yangdeyi1201@foxmail.com

from middleware.handler import Handler
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


class PageLogin:
    login_url = Handler.yaml_conf['host']+'/Index/login.html'

    # 将要定位的元素抽离出测试代码，统一存放便于维护
    username_locator = ('name', 'phone')
    pwd_locator = ('name', 'password')
    login_btn_locator = ('class name', 'btn')

    error_msg_locator = ('class name', 'layui-layer-content')
    fail_msg_error = ('class name', 'form-error-info')
    success_msg_error = ('xpath', '//a[text()="我的帐户[小蜜蜂146177499]"]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Handler.yaml_conf['webdriverwait']['timeout'])
        return

    def login(self, username, password):
        """
        username 登录用户名
        password 登录密码
        返回 self 链式调用：调用登录后继续调用获取预期结果
        """
        self.driver.get(self.login_url)
        self.driver.find_element(*self.username_locator).send_keys(username)
        self.driver.find_element(*self.pwd_locator).send_keys(password)
        self.driver.find_element(*self.login_btn_locator).click()
        return self

    def get_error_msg(self):
        """获取密码错误预期结果"""
        return self.wait.until(expected_conditions.visibility_of_element_located(self.error_msg_locator)).text

    def get_fail_msg(self):
        """获取手机号错误、密码或手机为空预期结果"""
        return self.driver.find_element(*self.fail_msg_error).text

    def get_success_msg(self):
        """获取成功登录预期结果"""
        return self.driver.find_element(*self.success_msg_error).text
