#!/bin/env python3
# -*- utf-8 -*-
# Tool to explore Mail.ru Cloud API (requests version)
# cmdline: ls, cd, get, pwd[, get, put, rm, mkdir, rmdir]
# Powered by:
# - https://gitlab.com/Kanedias/MARC-FS - working prototype
# - https://github.com/mad-gooze/PyMailCloud - python tricks

import os, json
from mrc import MailRuCloudClient
from cmd import Cmd

def load_account():
    def __load_str(d, s):
        if (not s in d):
            print('Not found: ' + s)
            exit(1)
        return d[s]

    CFG = os.path.join(os.path.expanduser('~'), '.config/marcfs/config.json')
    if (not os.path.exists(CFG)):
        print('Please fill out ' + CFG)
        exit(1)
    with open(CFG, "r") as cfg:
        data = json.load(cfg)
    return __load_str(data, 'username'), __load_str(data, 'password')

class   Terminal(Cmd):
    '''
    https://docs.python.org/3.6/library/cmd.html
    https://stackoverflow.com/questions/9340391/python-interactive-shell-type-application
    +'help': self.help,
    +'quit': self.quit,
    ...'pwd': self.pwd,
    ...'ls': self.ls,
    ...'cd': self.cd,
    'md': self.md,
    'rd': self.rd,
    'get': self.get,
    'put': self.put,
    'rm': self.rm,
    'lpwd': self.lpwd,
    'lls': self.lls,
    'lcd': self.lcd,
    '''
    prompt = 'mail.ru> '
    intro = 'Welcome to Cloud@Mail.Ru. Type help or ? to list commands.\n'
    cpath = []
    mrc = None

    def __init__(self, mrc):
        super().__init__()
        self.mrc = mrc

    def __scpath(self):
        return '/' + '/'.join(self.cpath)

    def do_EOF(self, args):
        'Exit'
        print()
        return True

    def do_exit(self, args):
        'Exit'
        return True

    def do_quit(self, args):
        'Quit'
        return True

    def do_pwd(self, args):
        'Print current remote path (ftp PWD)'
        print(self.__scpath())

    def do_ls(self, args):
        'List folder (ftp LIST)'
        print(json.dumps(self.mrc.ls(self.__scpath()), sort_keys=True, indent=1, ensure_ascii=False))

    def do_cd(self, args):
        'Change current folder (ftp C[W]D)'
        # construct new path (os.path.abspath())
        # check if exists => download
        # cwd
        self.cpath.append(args)

    def do_md(self, args):
        'Make folder (ftp MKD[IR])'
        # TODO: check available chars
        pass

    def do_rd(self, args):
        'Delete folder (ftp RMD[IR])'
        pass

    def do_get(self, args):
        'Download file (ftp GET)'
        pass

    def do_put(self, args):
        'Upload file (ftp PUT)'
        pass

    def do_rm(self, args):
        'Delete file (ftp DELE[TE])'
        pass

    def do_mv(self, args):
        'Rename/move file/folder (ftp ?)'
        pass

    def do_lpwd(self, args):
        'Print current local folder'
        print(os.getcwd())

    def do_lls(self, args):
        'List [current] local folder'
        for i in os.listdir():
            print(i)

    def do_lcd(self, args):
        'Change current local folder'
        npath = os.path.abspath(args[0])
        if (os.path.isdir(npath)):
            os.chdir(npath)
        else:
            print('Folder `%s` does not exists' % npath)

    def do_mget(self, args):
        'Multiple get (ftp MGET)'

    def do_mput(self, args):
        'Multiple put (ftp MPUT)'

    def do_test(self, args):
        'Just for tests'
        self.mrc.test()

def main():
    mrc = MailRuCloudClient()
    login, password = load_account()
    mrc.login(login, password)
    t = Terminal(mrc)
    t.cmdloop()
    #print(json.dumps(mrc.ls('/8'), sort_keys=True, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    main()
