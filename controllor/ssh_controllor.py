#author: yanzhang.scut@gmail.com

import  pexpect, log

import time, sys, re, datetime

__all__ = [
    'ssh_connection'
    ]

"""
integrate the class spawn and functions above for ssh connection and control. 
log_mode:
1. print input and output
2. print output
3. write input and output
4. write output

other: no log
"""
class ssh_connection(object):
    def __init__(self, host, username, password, log_mode=2):
        self.set_prompt('\# ')
        self.ssh_handle = pexpect.spawn('ssh ' + username + '@' + host)
        for loop in range(1,8):
            exp_index = self.ssh_handle.expect ([
            self.str_prompt,                         # 0  expect prompt
            pexpect.TIMEOUT,                         # 1
            pexpect.EOF,                             # 2
            'yes/no',                                # 3  If added new line here, please notice
            'password',                              # 4  the index is used in the if elif lines.
            'password: ',                            # 5  ubuntu ssh
            'Permission denied, please try again.',  # 6
            'Connection closed by UNKNOWN'           # 7
            ], timeout=6)
            
            if 0 == exp_index:
                if 1 == log_mode:
                    self.ssh_handle.logfile = sys.stdout
                elif 2 == log_mode:
                    self.ssh_handle.logfile_read = sys.stdout
                elif 3 == log_mode:
                    fout = file('mylog.txt','w')
                    self.ssh_handle.logfile = fout
                elif 4 == log_mode:
                    fout = file('mylog.txt','w')
                    self.ssh_handle.logfile_read = fout
                self.clean_buff()
                log.log_info('ssh connect successfully.')
                break    
            elif 1 == exp_index:
                pass
            elif 3 == exp_index:
                self.ssh_handle.sendline('yes')
            elif 4 == exp_index or 5 == exp_index:
                self.ssh_handle.sendline(password)
            elif 6 == exp_index:
                pass
            else:   #EOF or others
                log.log_info('ssh connect failed.', 'ERROR')
                self.ssh_handle.close(force=True)
                
    def disconnect(self):
        self.ssh_handle.close(force=True)            
    
    def set_prompt(self, str_prompt):
        self.str_prompt = str_prompt

    def clean_buff(self):
        for loop in range(1,3):
            exp_index = self.ssh_handle.expect([self.str_prompt, pexpect.TIMEOUT, pexpect.EOF], 0.01)
        if 2 == exp_index:
            log.log_info('expect EOF. what happened?', 'ERROR')
            self.ssh_handle.close(force = True)

    def send_command(self, cmd, timeout=6, ignore_fail = 0, retry_on = 0):
        buff = ''
        result = 1
        self.ssh_handle.sendline(cmd)
        for count in range(1, 10):
            if retry_on == 1 and count > 1:
                self.ssh_handle.sendline(cmd)
            exp_index = self.ssh_handle.expect([
            self.str_prompt,             #0
            pexpect.EOF,                 #1
            pexpect.TIMEOUT              #2
            ], timeout)
            buff += self.ssh_handle.before
            self.clean_buff()
            if exp_index == 0:
                result = 0
                break
            elif exp_index == 1:
                 log.log_info('command: %s failed. (EOF)' %(cmd), 'ERROR')
                 break
            elif exp_index == 2:
                log.log_info('command: %s failed, wait: %s. (TIMEOUT)' %(cmd, count), 'WARNING')
                time.sleep(timeout)
        if result == 1:
            log.log_info('Send %s failed, resend times %d(timeout=%d)' %(cmd, count, timeout), 'ERROR')
            if ignore_fail == 0:
                self.ssh_handle.close(force = True)
                sys.exit()
            else:
                return False
        if not buff:
            log.log_info('command: %s [NO BUFF]' %(cmd), 'WARNING') #still return, handled by users
            return False
        log.log_info('Send [%s] command ok' %(cmd), 'DUBUG')
        return buff

    def send_commands(self, cmds, timeout = 6, interval = 0.01, ignore_fail = 0, retry_on = 0):
        buff = ''
        for cmd in cmds.split('\n'):
            if not cmd:
                continue
            cmd = cmd.strip('\t')
            buff += self.send_command(cmd, timeout, ignore_fail, retry_on)
            time.sleep(interval)
        if not buff:
            log.log_info('command: %s [NO BUFF]' %(cmds), 'WARNING') #still return, handled by users
            return False
        return buff
