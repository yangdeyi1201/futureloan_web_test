# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.pages.page_login import PageLogin
from middleware.handler import Handler

cases = Handler.excel.read_sheet('login')


class TestLogin:
    @pytest.mark.parametrize('case_info', cases)
    def test_login(self, case_info, driver):
        login_page = PageLogin(driver)

        if 1 <= case_info['case_id'] <= 11:
            after_login = login_page.login_fail(eval(case_info['data'])['mobile_phone'], eval(case_info['data'])['pwd'])
        elif case_info['case_id'] == 12:
            after_login = login_page.login_success(eval(case_info['data'])['mobile_phone'], eval(case_info['data'])['pwd'])

        try:
            if 1 <= case_info['case_id'] <= 7:
                assert after_login.get_msg_incorrect_phone() == case_info['expected_resp']
            elif case_info['case_id'] == 8:
                assert after_login.get_msg_none_phone() == case_info['expected_resp']
            elif case_info['case_id'] in (9, 10):
                assert after_login.get_msg_error() == case_info['expected_resp']
            elif case_info['case_id'] == 11:
                assert after_login.get_msg_none_pwd() == case_info['expected_resp']
            elif case_info['case_id'] == 12:
                assert after_login.get_msg_account() == case_info['expected_resp']
            Handler.success_case('login', len(case_info), case_info['case_id'], __name__)
        except:
            Handler.fail_case('login', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main(["--reruns", "3", "--reruns-delay", "5", "-s"])
