# author:CC
# email:yangdeyi1201@foxmail.com

from selenium.webdriver import Chrome
import pytest


@pytest.fixture(scope='class', autouse=False)
def driver():
    driver = Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()
