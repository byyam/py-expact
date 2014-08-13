#author: yanzhang.scut@gmail.com

#common functions which used by ssh controllor
import pexpect
import re, sys, time, os

__all__ = [
    'check_file_exist',
    'check_local_file_exist',
    'do_scp',
    'sleep_rate'
    ]

def check_file_exist(conn_handle, path):
    conn_handle.send_command('file ' + path)
    str_buf = conn_handle.ssh_handle.before
    str_pattern = "No such file or directory"
    match_result = re.search(str_pattern, str_buf)
    if match_result:
        return False
    else:
        return str_buf

def check_local_file_exist(path):
    return os.path.exists(path)

def sleep_rate(seconds):
    for i in range(0, 10):
        print str(i*10) + '%...'
        time.sleep(seconds/10)
    print '100%'

def do_scp(host, user, pwd, file_name, target_path):
    print 'scp ' + file_name + ' ' + user + '@' + host + ':' + target_path
    child = pexpect.spawn('scp ' + file_name + ' ' + user + '@' + host + ':' + target_path)
    for loop in range(1, 8):
        exp_index = child.expect(['assword:', r'yes/no', pexpect.TIMEOUT, pexpect.EOF], timeout=30)
        if exp_index == 0:
            print "input pwd..."
            child.sendline(pwd)
            child.read()
            break
        elif exp_index == 1:
            child.sendline("yes")
            data = child.read()
            print data
            child.close()
        elif exp_index == 2:
            print "timeout waiting..."
        elif exp_index == 3:
            print "EOF error, exit"
            sys.exit()
        