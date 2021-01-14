# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from selenium.webdriver import Chrome
from middleware.handler import Handler
from middleware.pages.page_login import PageLogin


@pytest.fixture(scope='class')
def driver():
    driver = Chrome()
    driver.implicitly_wait(Handler.yaml_conf['implicitly_wait'])
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='class')
def login(driver):
    """登录后返回首页对象"""
    index_page = PageLogin(driver).login_success(Handler.yaml_conf['tester']['mobile_phone'], Handler.yaml_conf['tester']['pwd'])
    yield index_page
