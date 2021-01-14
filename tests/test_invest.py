# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler

cases = Handler.excel.read_sheet('invest')


class TestInvest:
    @pytest.mark.parametrize('case_info', cases[:2])
    def test_invest(self, case_info, login):
        actual = login.into_invest_list().invest(eval(case_info['data'])['amount']).get_msg_success_invest()

        try:
            assert actual == eval(case_info['expected_resp'])
            Handler.success_case('invest', len(case_info), case_info['case_id'], __name__)
        except:
            Handler.fail_case('invest', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main(['--reruns', '3', '--reruns-delay', '5', '-s'])
