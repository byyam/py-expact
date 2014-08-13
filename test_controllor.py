#!/usr/bin/python
#author: yanzhang.scut@gmail.com

from controllor import ssh_controllor
from controllor import log
from controllor import tools

from controllor import pexpect
from pexpect import *
#import all functions for directly using
print run('pwd')

ssh_handle = ssh_controllor.ssh_connection('tohost', 'username', 'password')
ssh_handle.send_commands('ps -ef')
ret = tools.check_file_exist(ssh_handle, 'check_file')
if ret:
    print 'exist'
else:
    print 'not exist'

tools.do_scp('tohost', 'username', 'password', 'transfer_file', 'target_dir')
ssh_handle.disconnect()
logger = log.logger()
logger.debug('msg')
log.log_info('func', 'WARNING')
