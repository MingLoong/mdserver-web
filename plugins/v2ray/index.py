# coding:utf-8

import sys
import io
import os
import time
import shutil

sys.path.append(os.getcwd() + "/class/core")
import public

app_debug = False
if public.isAppleSystem():
    app_debug = True


def getPluginName():
    return 'v2ray'


def getPluginDir():
    return public.getPluginDir() + '/' + getPluginName()


def getServerDir():
    return public.getServerDir() + '/' + getPluginName()


def getArgs():
    args = sys.argv[2:]
    tmp = {}
    args_len = len(args)

    if args_len == 1:
        t = args[0].strip('{').strip('}')
        t = t.split(':')
        tmp[t[0]] = t[1]
    elif args_len > 1:
        for i in range(len(args)):
            t = args[i].split(':')
            tmp[t[0]] = t[1]

    return tmp


def checkArgs(data, ck=[]):
    for i in range(len(ck)):
        if not ck[i] in data:
            return (False, public.returnJson(False, '参数:(' + ck[i] + ')没有!'))
    return (True, public.returnJson(True, 'ok'))


def status():
    cmd = "ps -ef|grep ssserver |grep -v grep | awk '{print $2}'"
    data = public.execShell(cmd)
    if data[0] == '':
        return 'stop'
    return 'start'


def start():

    shell_cmd = 'service  ' + getPluginName() + ' start'
    data = public.execShell(shell_cmd)

    if data[0] == '':
        return 'ok'
    return data[1]


def stop():
    shell_cmd = 'service  ' + getPluginName() + ' stop'

    data = public.execShell(shell_cmd)
    if data[0] == '':
        return 'ok'
    return data[1]


def restart():
    shell_cmd = 'service  ' + getPluginName() + ' restart'
    data = public.execShell(shell_cmd)
    if data[0] == '':
        return 'ok'
    return data[1]


def reload():
    shell_cmd = 'service  ' + getPluginName() + ' reload'
    data = public.execShell(shell_cmd)
    if data[0] == '':
        return 'ok'
    return data[1]


def getPathFile():
    if public.isAppleSystem():
        return getServerDir() + '/config.json'
    return '/etc/v2ray/config.json'


def getInitDFile():
    if app_debug:
        return '/tmp/' + getPluginName()
    return '/etc/init.d/' + getPluginName()


def initdStatus():
    if not app_debug:
        if public.isAppleSystem():
            return "Apple Computer does not support"
    initd_bin = getInitDFile()
    if os.path.exists(initd_bin):
        return 'ok'
    return 'fail'


def initdInstall():
    import shutil
    if not app_debug:
        if public.isAppleSystem():
            return "Apple Computer does not support"

    public.execShell('chmod +x ' + initd_bin)
    public.execShell('chkconfig --add ' + getPluginName())
    return 'ok'


def initdUinstall():
    if not app_debug:
        if public.isAppleSystem():
            return "Apple Computer does not support"

    public.execShell('chkconfig --del ' + getPluginName())
    return 'ok'


def getLog():
    return '/var/log/shadowsocks.log'

if __name__ == "__main__":
    func = sys.argv[1]
    if func == 'status':
        print status()
    elif func == 'start':
        print start()
    elif func == 'stop':
        print stop()
    elif func == 'restart':
        print restart()
    elif func == 'reload':
        print reload()
    elif func == 'conf':
        print getPathFile()
    elif func == 'initd_status':
        print initdStatus()
    elif func == 'initd_install':
        print initdInstall()
    elif func == 'initd_uninstall':
        print initdUinstall()
    elif func == 'run_log':
        print getLog()
    else:
        print 'error'