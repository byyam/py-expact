#!/usr/bin/python
#author: yanzhang.scut@gmail.com

from controllor import pexpect

my_handle = pexpect.spawn('ssh yourhost')
my_handle.expect ('password: ', timeout=5)
my_handle.sendline('yourpwd')
print my_handle.before