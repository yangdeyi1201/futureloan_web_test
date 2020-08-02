from config import paths
from common.handler_yaml import read_yaml
from common.handler_log import get_logger
from common.handler_excel import ExcelHandler


class Handler:
    yaml_conf = read_yaml(paths.CONFIG_PATH/'config.yaml')

    __log_config = yaml_conf['log']
    logger = get_logger(logger_level=__log_config['logger_level'],
                        console_level=__log_config['console_level'],
                        file_level=__log_config['file_level'],
                        file_path=paths.LOGS_PATH/__log_config['filename'])

    excel = ExcelHandler(paths.DATA_PATH / yaml_conf['excel']['filename'])

    tester = yaml_conf['tester']


if __name__ == '__main__':
    pass
