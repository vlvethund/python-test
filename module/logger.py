from datetime import datetime
from module.timeutil import get_edt_timezone

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def warn(*args):
    log(WARNING, '[WARNING]:', ENDC, *args)


def info(*args):
    log(OKCYAN, '[INFO]:', ENDC, *args)


def debug(*args):
    log(OKGREEN, '[DEBUG]:', ENDC, *args)


def error(*args):
    log(FAIL, '[ERROR]:', ENDC, *args)


def log(*args):
    now = datetime.now(get_edt_timezone()).strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{now}]', *args)


if __name__ == '__main__':
    warn('hi', 'hello')
    info('hi', 'hello')
    debug('hi', 'hello')
    error('hi', 'hello')
