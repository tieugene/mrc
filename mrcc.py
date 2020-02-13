#!/usr/bin/env python3
# -*- utf-8 -*-
# Tool to explore Mail.ru Cloud API (requests version)
# cmdline: ls, cd, get, pwd[, get, put, rm, mkdir, rmdir]
# Powered by:
# - https://gitlab.com/Kanedias/MARC-FS - working prototype
# - https://github.com/mad-gooze/PyMailCloud - python tricks

import json
import os
import pprint
from cmd import Cmd
from mrc import MailRuCloudClient


def load_account():
    def __load_str(d, s):
        if s not in d:
            print('Not found: ' + s)
            exit(1)
        return d[s]

    CFG = os.path.join(os.path.expanduser('~'), '.config/marcfs/config.json')
    if not os.path.exists(CFG):
        print('Please fill out ' + CFG)
        exit(1)
    with open(CFG, "r") as cfg:
        data = json.load(cfg)
    return __load_str(data, 'username'), __load_str(data, 'password')


class Terminal(Cmd):
    """
    https://docs.python.org/3.6/library/cmd.html
    https://stackoverflow.com/questions/9340391/python-interactive-shell-type-application
    """
    prompt = '> '
    intro = 'Welcome to Cloud@Mail.Ru. Type help or ? to list commands.\n'
    __cpath = None
    __mrc = None

    def __init__(self, mrc):
        super().__init__()
        self.__mrc = mrc
        self.__cpath = '/'
        self.__update_prompt()

    def __update_prompt(self):
        self.prompt = self.__cpath + '> '

    def __normpath(self, path: str) -> str:
        if path.startswith('/'):
            retvalue = path
        elif self.__cpath == '/':
            retvalue = os.path.normpath(self.__cpath + path)
        else:
            retvalue = os.path.normpath(self.__cpath + '/' + path)
        return retvalue

    def do_EOF(self, args):
        """Exit"""
        print()
        return True

    def do_exit(self, args):
        """Exit"""
        return True

    def do_quit(args):
        """Quit"""
        return True

    def do_login(self, args):
        """Log in to server.\nUsage: login [username password]\nsusername and password can be stored in ~/.config/marcfs/config.json"""
        # TODO: handle args
        l, p = load_account()
        self.__mrc.login(l, p)

    def do_info(self, args):
        """Print entry info.\nUsage: info [folder/file]\nDefault - current folder"""
        #print(f'Args = "{args}": {type(args)}')
        path = self.__normpath(args or '.' )    # current path default
        #print(f'New path: {path}')
        #pprint.pprint(self.__mrc.info())
        i = self.__mrc.info(path)
        if i:
            for k, v in i.items():
                print(f'{k}: {v}')

    def do_pwd(self, args):
        """Print current remote path (ftp PWD)"""
        print(self.__cpath)

    def do_ls(self, args):
        """List folder (ftp LIST)\nUsage: ls [-l] [folder]"""
        # TODO: check path is existent folder
        # TODO: handle -l option (size; folders: grev, rev; file: mtime, hash, virus, urls, msg)
        path = self.__normpath(args or '.')
        i = self.__mrc.folder_read(path)
        if i:
            print('{} (rev {}, grev {}, {} bytes, {} folders, {} files):\n------------------'.format(
                i['home'], i['rev'], i['grev'], i['size'], i['count']['folders'], i['count']['files']))
            print('Size          Name\n------------------')
            for f in i['list']:
                print('{:13d} {}{}'.format(f['size'], f['name'], '/' if f['type'] == 'folder' else ''))
            print('------------------')

    def do_cd(self, args):
        """Change current folder (ftp C[W]D)\nUsage: cd [folder] (default - /)"""
        # construct new path (os.path.abspath())
        # check if exists => download
        # cwd
        # TODO: chg prompt
        # TODO: check path is existent folder
        path = self.__normpath(args or '/')
        self.__cpath = path
        self.__update_prompt()

    def do_md(self, args):
        """Make folder (ftp MKD[IR])"""
        # TODO: check available chars
        pass

    def do_rd(self, args):
        """Delete folder (ftp RMD[IR])"""
        pass

    def do_get(self, args):
        """Download file (ftp GET)"""
        pass

    def do_put(self, args):
        """Upload file (ftp PUT)"""
        pass

    def do_rm(self, args):
        """Delete file (ftp DELE[TE])"""
        pass

    def do_mv(self, args):
        """Rename/move file/folder (ftp ?)"""
        pass

    def do_lpwd(self, args):
        """Print current local folder"""
        print(os.getcwd())

    def do_lls(self, args):
        """List [current] local folder"""
        for i in os.listdir():
            print(i)

    def do_lcd(self, args):
        """Change current local folder"""
        npath = os.path.abspath(args[0])
        if (os.path.isdir(npath)):
            os.chdir(npath)
        else:
            print('Folder `%s` does not exists' % npath)

    def do_mget(self, args):
        """Multiple get (ftp MGET)"""
        pass

    def do_mput(self, args):
        """Multiple put (ftp MPUT)"""
        pass

    def do_test(self, args):
        """Just for tests"""
        self.__mrc.test()


def main():
    t = Terminal(MailRuCloudClient()).cmdloop()
    # print(json.dumps(mrc.ls('/8'), sort_keys=True, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
