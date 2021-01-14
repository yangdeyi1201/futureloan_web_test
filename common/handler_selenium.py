# author:CC
# email:yangdeyi1201@foxmail.com

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from middleware.handler import Handler
import allure
from functools import wraps


def log(func):
    """元素找不到时截图并输出日志"""
    @wraps(func)
    def inner(self, locator):
        try:
            return func(self, locator)
        except:
            self.screenshot()
            Handler.logger.error(f'元素 {locator} 找不到')
    return inner


class BasePage:
    def __init__(self, driver, timeout):
        self.wait = WebDriverWait(driver=driver, timeout=timeout)
        self.driver = driver
        return

    @log
    def find_elem(self, locator):
        """查找元素(加入异常处理)"""
        elem = self.driver.find_element(*locator)
        return elem

    @log
    def wait_presence_elem(self, locator):
        """显示等待元素被加载"""
        elem = self.wait.until(expected_conditions.presence_of_element_located(locator=locator))
        return elem

    @log
    def wait_visitable_elem(self, locator):
        """显示等待元素可见"""
        elem = self.wait.until(expected_conditions.visibility_of_element_located(locator=locator))
        return elem

    @log
    def wait_clickable_elem(self, locator):
        """显示等待元素可点击"""
        elem = self.wait.until(expected_conditions.element_to_be_clickable(locator=locator))
        return elem

    def get_text_of_visitable_elem(self, locator):
        """获取可见元素 text 文本，text 文本可用于断言"""
        return self.wait_visitable_elem(locator=locator).text

    def get_text_of_clickable_elem(self, locator):
        """获取可点击元素 text 文本，text 文本可用于断言"""
        return self.wait_clickable_elem(locator=locator).text

    def click_elem(self, locator):
        """点击某个元素"""
        self.wait_clickable_elem(locator=locator).click()

    def switch_into_frame(self, locator):
        """ iframe 等待切换"""
        self.wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(locator=locator))
        return self

    def switch_into_alert(self, locator):
        """ alert 等待切换"""
        alert = self.wait.until(expected_conditions.alert_is_present())
        return alert

    def switch_to_window(self):
        """切换至最新标签页"""
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def screenshot(self):
        """页面截图"""
        from config.path import screenshot_path
        from datetime import datetime
        ts = datetime.now().strftime(Handler.yaml_conf['fmt'])
        filename = str(screenshot_path/f'screenshot-{ts}.png')
        self.driver.save_screenshot(filename=filename)
        with open(file=filename, mode='rb') as f:
            file = f.read()
            allure.attach(file, name='异常截图', attachment_type=allure.attachment_type.PNG)