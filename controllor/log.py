#author: yanzhang.scut@gmail.com

import datetime, sys

__all__ = [
    'log_info',
    'logger'
    ]

GREEN = '\033[32m'
YELLOW = '\033[33m' 
RED = '\033[31m'
LIGHT_BLUE = '\033[36m'
BLUE = '\033[34m'
RED_BLACK = '\033[41m'

COLOR_END = '\033[0m'

# directly use to print log
def log_info(str_trace, level='DEFAULT'):
    LOG_LEVEL = GREEN
    LOG_END = COLOR_END
    if level == 'WARNING':
        LOG_LEVEL = YELLOW
    elif level == 'ERROR':
        LOG_LEVEL = RED
    elif level == 'DEBUG':
        LOG_LEVEL = LIGHT_BLUE
    elif level == 'HIGHLIGHT':
        LOG_LEVEL = RED_BLACK
    print (LOG_LEVEL + r"%s%20s:%03d %s" + LOG_END) %(datetime.datetime.now().strftime('%m%d-%H:%M:%S'),
        sys._getframe().f_back.f_code.co_name,
        sys._getframe().f_back.f_lineno,
        str_trace);

# use a object handle to print log
class logger(object):
    def __init__(self):
        self.LOG_LEVEL = GREEN
        self.LOG_END = COLOR_END
        
    def print_log(self, str_trace):
        print (self.LOG_LEVEL + "%s%20s:%03d %s" + self.LOG_END) %(datetime.datetime.now().strftime('%m%d-%H:%M:%S'),
            sys._getframe().f_back.f_code.co_name,
            sys._getframe().f_back.f_lineno,
            str_trace)
            
    def debug(self, str_trace):
        self.LOG_LEVEL = LIGHT_BLUE
        self.print_log(str_trace)
    
    def highlight(self, str_trace):
        self.LOG_LEVEL = RED_BLACK
        self.print_log(str_trace)
        
    def warning(self, str_trace):
        self.LOG_LEVEL = YELLOW
        self.print_log(str_trace)
        
    def error(self, str_trace):
        self.LOG_LEVEL = RED
        self.print_log(str_trace)

    def log_info(self, str_trace, level):
        if level == 'WARNING':
            self.warning(str_trace)
        elif level == 'ERROR':
            self.error(str_trace) 
        elif level == 'DEBUG':
            self.debug(str_trace)
        elif level == 'HIGHLIGHT':
            self.light(str_trace)