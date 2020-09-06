# author:CC
# email:yangdeyi1201@foxmail.com
import pytest
import allure
from middleware.handler import Handler
from middleware.pages.login import PageLogin

excel = Handler.excel
cases = excel.read_sheet('login')
logger = Handler.logger


@allure.feature('登录模块')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.login
class TestLogin:
    """登录功能测试类"""
    @pytest.mark.parametrize('case_info', cases[:2])
    def test_login_error(self, case_info, driver):
        """密码错误的用例"""
        # 初始化页面，测试用到的页面
        login_page = PageLogin(driver)
        # 测试步骤：页面的行为，PO 中的方法
        actual = login_page.login_exception(eval(case_info['data'])['mobile_phone'], eval(case_info['data'])['pwd']).get_error_msg()
        # 实际结果、预期结果比对
        # 异常处理：日志记录/测试结果回写
        try:
            assert actual == case_info['expected_resp']
            excel.write_data('login', case_info['case_id']+1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('login', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[2:8])
    def test_login_fail(self, case_info, driver):
        """手机号错误、密码或手机号为空的用例"""
        login_page = PageLogin(driver)
        actual = login_page.login_exception(eval(case_info['data'])['mobile_phone'], eval(case_info['data'])['pwd']).get_fail_msg()
        try:
            assert actual == case_info['expected_resp']
            excel.write_data('login', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('login', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[8:])
    def test_login_success(self, case_info, driver):
        """正常登录的用例"""
        login_page = PageLogin(driver)
        actual = login_page.login_success(eval(case_info['data'])['mobile_phone'], eval(case_info['data'])['pwd']).get_success_msg()
        try:
            assert actual == case_info['expected_resp']
            excel.write_data('login', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('login', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise
