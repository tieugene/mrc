#!/usr/bin/env python3
# -*- utf-8 -*-
# Tool to explore Mail.ru Cloud API (requests version)
# cmdline: ls, cd, get, pwd[, get, put, rm, mkdir, rmdir]
# Powered by:
# - https://gitlab.com/Kanedias/MARC-FS - working prototype
# - https://github.com/mad-gooze/PyMailCloud - python tricks

import json
import os
import sys
import re
import datetime
import pprint
import warnings
import cmd
from mrc import MailRuCloudClient
from oops import MailRuCloudError

INVALID_FOLDER_CHARS = "\"*:<>?\\|"
INVALID_FOLDER_MASK = re.compile('["*:<>?\\\|]')
VIRUS_TEST = {
    'pass': '+',
    'fail': 'x',
    'not_yet': '?'
}
CFG_PATH = '.config/mrc/config.json'
DEBUG = True


def _dprint(s: str, end: str = '\n') -> None:
    """
    Prints debug info
    :param s: to print
    :param end: EOL separator
    :return: None
    """
    if DEBUG:
        print(s, file=sys.stderr, end=end, flush=True)


def _load_account():
    def __load_str(d, s):
        if s not in d:
            print('Not found: ' + s)
            exit(1)
        return d[s]

    CFG = os.path.join(os.path.expanduser('~'), CFG_PATH)
    if not os.path.exists(CFG):
        print('Please fill out ' + CFG)
        exit(1)
    with open(CFG, "r") as cfg:
        data = json.load(cfg)
    return __load_str(data, 'username'), __load_str(data, 'password')


class Terminal(cmd.Cmd):
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

    def __not_implemented(self):
        print('Command not implemented yet.')

    def __update_prompt(self):
        """Updates command prompt"""
        self.prompt = self.__cpath + '> '

    def __norm_path(self, path: str) -> str:
        """Normalize path"""
        if path.startswith('/'):
            retvalue = path
        elif self.__cpath == '/':
            retvalue = os.path.normpath(self.__cpath + path)
        else:
            retvalue = os.path.normpath(self.__cpath + '/' + path)
        return retvalue

    def do_EOF(self, args):
        """"""
        print()
        return True

    def do_exit(self, args):
        """Exit"""
        return True

    def do_quit(args):
        """Quit"""
        return True

    def do_pwd(self, args):
        """Print current remote path (ftp PWD)"""
        print(self.__cpath)

    def do_login(self, args):
        """Log in to server.\nUsage: login [username password]\nsusername and password can be stored in ~/.config/marcfs/config.json"""
        # TODO: handle args
        l, p = _load_account()
        self.__mrc.login(l, p)

    def __wrap(self, r):
        """
        Wrap response.
        :param r - Response object
        TODO: exception handling
        """
        if r:
            return r.json()['body']
        else:
            _dprint("Error {} ({}): {}".format(r.status_code, r.reason, r.json()['body']))

    def __get_info(self, path: str, isfolder: bool = None):
        """
        Get/test entry info.
        :param path: entry to get/test
        :param isfolder: None - get info, True - folder, False - file
        :return: dict (entry info) or bool (is folder/file)
        """
        i = self.__wrap(self.__mrc.entry_info(path))
        if i:
            if (isfolder is None):  # get info
                return i
            else:                   # test on is folder or file
                return (i['kind'] == 'folder') == isfolder

    def do_info(self, args):
        """Print entry info.\nUsage: info [folder/file]\nDefault - current folder"""
        path = self.__norm_path(args or '.')  # current path default
        i = self.__get_info(path)
        if i:
            for k, v in i.items():
                print(f'{k}: {v}')

    def do_cd(self, args):
        """Change current folder (ftp C[W]D)\nUsage: cd [folder] (default /)"""
        path = self.__norm_path(args or '/')
        r = self.__get_info(path, True)
        if r:
            self.__cpath = path
            self.__update_prompt()
        elif r is False:
            _dprint(f'`{path}` is not folder')

    def do_ls(self, args):
        """List folder (ftp LIST)\nUsage: ls [-l] [folder]"""
        # Common(17): size(13), ... published+access(1), >message(1)
        # Folder(23): rev(5), grev(5), dirs(3), files(3), sharing+mount access(1), tree(1)
        # Files(21): mtime(19), virus(1)
        # TODO: check isfile
        # TODO: check logged in
        # TODO: list template
        # TODO: cache
        __long = False
        if (args == '-l') or args.startswith('-l'):  # long style
            __long = True
            args = args[2:].lstrip()
        path = self.__norm_path(args or '.')
        #if not self.__get_info(path, True):
        #    _dprint(f'"{path}" is not folder')
        #    return
        i = self.__wrap(self.__mrc.folder_list(path))
        if i:
            if __long:
                __tree = i['tree']
                line = 40 * '-'
                # 1. head
                print('{} (rev {}, grev {}):'.format(i['home'], i['rev'], i['grev']))
                print(line)
                print('{:<13} {:<5} {:<5} dirs  files T Name'.format(
                    'Size', 'rev', 'grev'
                ))
                print('{:<13} {:<17} V M A W Name'.format('', 'mtime'))
                print(line)
                # 2. body
                for f in i['list']:
                    #print(f)
                    if f['type'] == 'folder':
                        print('{:13d} {:5d} {:5d} {:5d} {:5d} {} {}/'.format(
                            f['size'], f['rev'], f['grev'], f['count']['folders'], f['count']['files'],
                            ' ' if f['tree'] == __tree else '!', f['name']
                        ))
                    else:  # skip hash; +5 spaces; virus: pass, fail, not_yet
                        vir = f['virus_scan']
                        print('{:13d} {:17} {} {:1} {:1} {:1} {}'.format(
                            f['size'], datetime.datetime.fromtimestamp(f['mtime']).strftime('%Y.%m.%d %H:%M:%S'),
                            VIRUS_TEST.get(vir, vir), f.get('message', '-'), f.get('weblink_access_rights', '-'),
                            '+' if 'weblink' in f else '-', f['name']
                        ))
                # 3. bottom
                print('{}\n{:13d} {:17d} {:5d}'.format(
                    line, i['size'], i['count']['folders'], i['count']['files']
                ))
            else:
                for f in i['list']:
                    print('{}{}'.format(f['name'], '/' if f['type'] == 'folder' else ''))

    def do_mkdir(self, path):
        """Create new folder (ftp MKD[IR])\nUSage:
        mkdir <path>"""
        # TODO: rename mode
        if not path:                            # 1. args is empty
            _dprint('Empty path')
            return
        if path in set(('.', '..', '/')):       # 2. special name
            _dprint("Folder name cannot be `.` or `..` or `/`")
            return
        if INVALID_FOLDER_MASK.search(path):    # 3. invalid chars
            _dprint("Folder name cannot contents `{}`".format(INVALID_FOLDER_CHARS))
            return
        path = self.__norm_path(path.rstrip('/'))
        if self.__mrc.exists(path) == 200:      # 4. path exists
            _dprint(f"`{path}` already exists")
            return
        self.__wrap(self.__mrc.folder_add(path))

    def _do_rd(self, args):
        """Delete folder (ftp RMD[IR])"""
        self.__not_implemented()

    def _do_get(self, args):
        """Download file (ftp GET)"""
        self.__not_implemented()

    def _do_put(self, args):
        """Upload file (ftp PUT)"""
        self.__not_implemented()

    def _do_rm(self, args):
        """Delete file (ftp DELE[TE])"""
        self.__not_implemented()

    def _do_cp(self, args):
        """Copy file (ftp ???)"""
        self.__not_implemented()

    def _do_mv(self, args):
        """Rename/move file/folder (ftp ?)"""
        self.__not_implemented()

    def _do_mget(self, args):
        """Multiple get (ftp MGET)"""
        self.__not_implemented()

    def _do_mput(self, args):
        """Multiple put (ftp MPUT)"""
        self.__not_implemented()

    def do_df(self, args):
        """Display free disk space"""
        rsp = self.__wrap(self.__mrc.user_space())
        print('{:,} / {:,} bytes used'.format(rsp['bytes_used'], rsp['bytes_total']).replace(',', ' '))

    def do_cmd(self, arg):
        """
        Perform command to MRC API\nUsage: cmd <method> <url> <payload>
        - method:str get/post/head
        - url:str tail after (e.g. /file/add)
        - payload:dict - params/data
        :return status_code, content[:json]
        example: cmd get /file {"home":"/tmp"}
        """
        args = arg.split(' ', 2)
        if len(args) != 3:
            print('Wrong args number')
            return
        if args[0] not in set(('get', 'post', 'head')):
            print('Bad method')
            return
        if not args[1].startswith('/'):
            print('Bad url')
            return
        try:
            payload = json.loads(args[2])
        except:
            print('Bad payload')
            return
        else:
            res = self.__mrc.any(args[0], args[1], payload)
            print(f'Code: {res.status_code}')
            # if res.content:
            # json.dumps(res.json(), indent=1)
            pprint.pprint(res.json()['body'])

    def do_test(self, args):
        """Just for tests"""
        self.__mrc._test_exists(args)

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


def main():
    t = Terminal(MailRuCloudClient()).cmdloop()
    # print(json.dumps(mrc.ls('/8'), sort_keys=True, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
