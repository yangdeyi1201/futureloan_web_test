# author:CC
# email:yangdeyi1201@foxmail.com

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from middleware.handler import Handler
import allure


class BasePage:
    def __init__(self, driver, timeout=30, poll_frequency=0.5):
        self.driver = driver
        self.wait = WebDriverWait(driver=self.driver, timeout=timeout, poll_frequency=poll_frequency)
        self.action_chains = ActionChains(driver=self.driver)
        return

    def wait_elem_clickable(self, locator):
        """显示等待元素可被点击"""
        try:
            elem = self.wait.until(expected_conditions.element_to_be_clickable(locator=locator))
            return elem
        except:
            self.screen_shoot()
            Handler.logger.error(f'元素{locator}找不到')

    def wait_elem_visitable(self, locator):
        """显示等待元素页面可见"""
        try:
            elem = self.wait.until(expected_conditions.visibility_of_element_located(locator=locator))
            return elem
        except:
            self.screen_shoot()
            Handler.logger.error(f'元素{locator}找不到')

    def wait_elem_presence(self, locator):
        """显示等待元素源码中出现"""
        try:
            elem = self.wait.until(expected_conditions.presence_of_element_located(locator=locator))
            return elem
        except:
            self.screen_shoot()
            Handler.logger.error(f'元素{locator}找不到')

    def click(self, locator):
        """点击某个元素"""
        self.wait_elem_clickable(locator=locator).click()
        return self

    def write(self, locator, value):
        """输入信息"""
        self.wait_elem_presence(locator=locator).send_keys(value)
        return self

    def get_attribute(self, locator, name):
        """获取某元素某属性"""
        attribute = self.wait_elem_presence(locator=locator).get_attribute(name=name)
        return attribute

    def get_clickable_elem_text(self, locator):
        """获取可被点击元素的文本"""
        text = self.wait_elem_clickable(locator=locator).text
        return text

    def get_visitable_elem_text(self, locator):
        """获取仅可见元素的文本"""
        text = self.wait_elem_visitable(locator=locator).text
        return text

    def switch_into_frame(self, locator):
        """切换至iframe"""
        self.wait.until(expected_conditions.frame_to_be_available_and_switch_to_it(locator=locator))
        return self

    def switch_into_alert(self):
        """切换至alert弹框"""
        alert = self.wait.until(expected_conditions.alert_is_present())
        return alert

    def screen_shoot(self):
        """截图"""
        from datetime import datetime
        from config.paths import SCREENSHOOTS_PATH
        ts = datetime.now().strftime(Handler.yaml_conf['strftime_format'])
        file_name = str(SCREENSHOOTS_PATH/f'screenshoot-{ts}.png')
        self.driver.save_screenshot(filename=file_name)
        with open(file=file_name, mode='rb') as f:
            file = f.read()
        allure.attach(body=file, name='异常截图', attachment_type=allure.attachment_type.PNG)
        Handler.logger.info(f'页面截图文件保存在{file_name}')
