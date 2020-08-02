# author:CC
# email:yangdeyi1201@foxmail.com


from common.basepage import BasePage
from selenium.webdriver.common.by import By
from middleware.handler import Handler
from middleware.pages.index import PageIndex


class PageLogin(BasePage):
    login_url = Handler.yaml_conf['host']+'/Index/login.html'

    def __init__(self, driver, timeout=10, poll_frequency=0.5):
        super().__init__(driver, timeout, poll_frequency)
        return

    # 将要定位的元素抽离出测试代码，统一存放便于维护
    username_locator = (By.NAME, 'phone')
    pwd_locator = (By.NAME, 'password')
    login_btn_locator = (By.CLASS_NAME, 'btn')

    error_msg_locator = (By.CLASS_NAME, 'layui-layer-content')
    fail_msg_error = (By.CLASS_NAME, 'form-error-info')

    def login_exception(self, username, password):
        """
        异常登录步骤
        username 登录用户名
        password 登录密码
        返回 self 链式调用：调用登录后继续调用获取预期结果
        """
        self.driver.get(self.login_url)
        self.write(locator=self.username_locator, value=username)
        self.write(locator=self.pwd_locator, value=password)
        self.click(locator=self.login_btn_locator)
        return self

    def login_success(self, username, password):
        """
        正常登录步骤
        username 登录用户名
        password 登录密码
        返回首页页面
        """
        self.driver.get(self.login_url)
        self.write(locator=self.username_locator, value=username)
        self.write(locator=self.pwd_locator, value=password)
        self.click(locator=self.login_btn_locator)
        return PageIndex(self.driver)

    def get_error_msg(self):
        """获取密码错误预期结果"""
        return self.get_visitable_elem_text(locator=self.error_msg_locator)

    def get_fail_msg(self):
        """获取手机号错误、密码或手机为空预期结果"""
        return self.get_visitable_elem_text(locator=self.fail_msg_error)


if __name__ == '__main__':
    pass
