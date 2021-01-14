# author:CC
# email:yangdeyi1201@foxmail.com

from common.handler_excel import ExcelHandler
from common.handler_yaml import read_yaml
from common.handler_log import my_logger
from config.path import data_path, config_path, log_path


class Handler(object):
    yaml_conf = read_yaml(yaml_path=config_path/'config.yaml')

    excel = ExcelHandler(excel_path=data_path/yaml_conf['excel']['name'])

    logger = my_logger(file_path=log_path/'log.log')

    investor_id = yaml_conf['investor_id']
    tester_id = yaml_conf['tester_id']
    administrator_id = yaml_conf['administrator_id']

    @property
    def randomphone(self):
        """随机生成手机号用于正常注册"""
        from random import randint
        return '138'+str(randint(10000000, 99999999))

    def regular_replace(self, string, pattern=r'#(.*?)#'):
        """正则替换"""
        import re
        while re.search(pattern=pattern, string=string):
            key = re.search(pattern=pattern, string=string).group(1)
            value = getattr(self, key, '')
            string = re.sub(pattern=pattern, repl=str(value), string=string, count=1)
        return string

    @staticmethod
    def success_case(sheet_name, column, case_id, module_name):
        """用例通过：excel回写测试结果+输出日志"""
        Handler.excel.write(sheet_name=sheet_name, row=case_id+1, column=column, data='pass')
        Handler.logger.info('{}--第{}条测试用例通过'.format(module_name, case_id))

    @staticmethod
    def fail_case(sheet_name, column, case_id, module_name):
        """用例失败：excel回写测试结果+输出日志"""
        Handler.excel.write(sheet_name=sheet_name, row=case_id+1, column=column, data='fail')
        Handler.logger.error('{}--第{}条测试用例不通过'.format(module_name, case_id))


if __name__ == '__main__':
    pass
