# author:CC
# email:yangdeyi1201@foxmail.com
import pytest
from middleware.handler import Handler
from middleware.pages.index import PageIndex

excel = Handler.excel
cases = excel.read_sheet('invest')
logger = Handler.logger


class TestInvest:
    @pytest.mark.parametrize('case_info', cases[11:12])
    def test_invest_without_login(self, case_info, driver):
        """未登录进行投资"""
        actual = PageIndex(driver).get_homepage().get_invest_list().invest_input_money(eval(case_info['data'])['amount']).get_msg_please_login()
        try:
            assert actual == eval(case_info['expected_resp'])
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[10:11])
    def test_invest_no_input(self, case_info, login):
        """不输入投资金额"""
        actual = login.get_invest_list().invest_no_input(eval(case_info['data'])['amount']).get_msg_no_input()
        try:
            assert actual == case_info['expected_resp']
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id']+1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[6:10])
    def test_invest_incorrect_money(self, case_info, login):
        """投资金额输入 0、-100、-200 元 / 全空格"""
        warning = login.get_invest_list().invest_input_money(eval(case_info['data'])['amount'])
        actual = warning.get_msg_incorrect_money()
        warning.confirm_warning()
        try:
            assert actual == eval(case_info['expected_resp'])
            excel.write_data('invest', case_info['case_id']+1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[:2])
    def test_invest_not_100_times(self, case_info, login):
        """投资金额输入非 100 整数倍：90 元 / 110 元"""
        warning = login.get_invest_list().invest_input_money(eval(case_info['data'])['amount'])
        actual = warning.get_msg_not_100_times()
        warning.confirm_warning()
        try:
            assert actual == eval(case_info['expected_resp'])
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[3:4])
    def test_invest_more_than_bid_amount(self, case_info, login):
        """标剩余可投金额 ＜ 投资金额（100 正整数倍） ≤ 投资账户余额"""
        invest_page = login.get_invest_list()
        more_than_bid_leave_amount = invest_page.generate_more_than_bid_leave_amount
        warning = invest_page.invest_input_money(str(more_than_bid_leave_amount))
        actual = warning.get_msg_not_more_than_bid_amount()
        warning.confirm_warning()
        try:
            assert actual == eval(case_info['expected_resp'])
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[2:3])
    def test_invest_more_than_account_amount(self, case_info, login):
        """投资账户余额 ＜ 投资金额（100 正整数倍） ≤ 标剩余可投金额"""
        account_leave_amount = login.into_my_account().get_account_leave_amount
        invest_page = login.get_invest_list()
        more_than_account_leave_amount = invest_page.generate_more_than_account_leave_amount(account_leave_amount)
        warning = invest_page.invest_input_money(str(more_than_account_leave_amount))
        actual = warning.get_msg_not_more_than_account_leave_amount()
        warning.confirm_warning()
        try:
            assert actual == eval(case_info['expected_resp'])
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[14:16])
    def test_invest_success(self, case_info, login):
        """投资成功"""
        from decimal import Decimal
        # 正常投资的金额
        invest_money = eval(case_info['data'])['amount']
        # 正常投资前先查询可用余额
        account_leave_amount_before = login.into_my_account().get_account_leave_amount
        warning = login.get_invest_list().invest_input_money(invest_money)
        actual = warning.get_msg_success()
        # 投资成功后再查询可用余额
        account_leave_amount_after = warning.confirm_activate().get_account_leave_amount
        try:
            assert actual == eval(case_info['expected_resp'])
            # 投资成功：投资前可用余额 - 投资金额 = 投资后可用余额
            assert Decimal(str(account_leave_amount_before))-Decimal(str(invest_money)) == Decimal(str(account_leave_amount_after))
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise

    @pytest.mark.parametrize('case_info', cases[13:14])
    @pytest.mark.expired
    def test_invest_bid_expired(self, case_info, login):
        """ 竞标到期"""
        warning = login.get_invest_list().invest_input_money(eval(case_info['data'])['amount'])
        actual = warning.get_msg_bid_expired()
        warning.confirm_warning()
        try:
            assert actual == eval(case_info['expected_resp'])
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '通过')
            logger.info(f'第{case_info["case_id"]}条测试用例通过')
        except AssertionError:
            excel.write_data('invest', case_info['case_id'] + 1, len(case_info), '不通过')
            logger.error(f'第{case_info["case_id"]}条测试用例不通过')
            raise
