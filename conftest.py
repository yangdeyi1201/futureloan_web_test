# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from selenium.webdriver import Chrome
from middleware.pages.login import PageLogin
from middleware.handler import Handler


@pytest.fixture(scope='class', autouse=False)
def driver():
    """
    管理浏览器
    """
    driver = Chrome()
    driver.implicitly_wait(30)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='class', autouse=False)
def login(driver):
    """
    正常登录
    返回成功登录后首页
    """
    index_page = PageLogin(driver).login_success(username=Handler.tester['mobile_phone'],
                                                 password=Handler.tester['pwd'])
    yield index_page
