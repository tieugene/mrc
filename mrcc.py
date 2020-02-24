#!/usr/bin/env python3
# -*- utf-8 -*-
# Tool to explore Mail.ru Cloud API (requests version)
# cmdline: ls, cd, get, pwd[, get, put, rm, mkdir, rmdir]
# Powered by:
# - https://gitlab.com/Kanedias/MARC-FS - working prototype
# - https://github.com/mad-gooze/PyMailCloud - python tricks
# TODO: pub:
#  - collapse 5 to 1 (pub <resource> on/off/info/ro/rw)
#  - handle as weblink as path

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
WEBLINK_ACCESS = {
    'r': 'R',
    'rw': 'W'
}
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
    intro = 'Welcome to Cloud@Mail.Ru. Type `help` or `?` to list commands.\n'
    __cpath = None
    __mrc = None

    def __init__(self, mrc):
        super().__init__()
        self.__mrc = mrc
        self.__cpath = '/'
        self.__update_prompt()

    def __ut2dt(self, ut, m):
        """Converts unixtime into datetime"""
        return datetime.datetime.fromtimestamp(ut).strftime(m)

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

    def do_quit(self, args):
        """Quit"""
        return True

    def do_pwd(self, args):
        """Print current remote path (ftp PWD)"""
        print(self.__cpath)

    def do_login(self, args):
        """Log in to server.\nUsage: login [username password]\nsusername and password can be stored in ~/.config/marcfs/config.json"""
        # TODO: handle args
        # TODO: check login twice
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
        """List folder (ftp LIST)\nUsage: ls [-l] [folder]\nOutput:
        - P (published): W - rw (folder only), R - r/o[, ! - weblink w/o weblink_access-right or vice versa]
        - M (message): * - exists and not empty
        - S (share; folder only): S - shared, M - mounted rw, m - mounted r/o
        - T(folder)/V(file): ! - tree is not equal to parent, +/x/? - virus_scan=pass/fail/not_yet
        """
        # Common(17): size(13), ... published+access(1), >message(1)
        # Folder(27): rev(5), grev(5), dirs(5), files(5), sharing+mount access(1), tree(1)
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
                line = 42 * '-'
                # 1. head
                print(line)
                print('PMST dirs files rev   grev  {:13} Name'.format('Size'))
                print('   V date       time')
                print(line)
                # 2. body
                for f in i['list']:
                    #print(f)
                    flags = [' ', ' ', ' ', ' ']
                    if 'weblink' in f:
                        flags[0] = WEBLINK_ACCESS[f['weblink_access_rights']]
                        if f['message']:
                            flag[1] = '*'
                    if f['type'] == 'folder':
                        if f['kind'] == 'shared':
                            flags[2] = 'S'
                        elif f['kind'] == 'mounted':
                            flags[2] = 'm' if 'readonly' in f else 'M'
                        if f['tree'] != __tree:
                            flags[3] = '!'
                        print('{:4} {:4d} {:5d} {:5d} {:5d} {:13d} {}/'.format(
                            ''.join(flags), f['count']['folders'], f['count']['files'], f['rev'], f['grev'], f['size'], f['name']
                        ))
                    else:   # file
                        flags[3] = VIRUS_TEST[f['virus_scan']]
                        print('{:4} {:22} {:13d} {}'.format(
                            ''.join(flags), datetime.datetime.fromtimestamp(f['mtime']).strftime('%Y.%m.%d    %H:%M:%S'),
                            f['size'], f['name']
                        ))
                # 3. bottom
                print('{}\n     {:4d} {:5d} {:5d} {:5d} {:13d} {}'.format(
                    line, i['count']['folders'], i['count']['files'], i['rev'], i['grev'], i['size'], i['home']
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
        #if self.__mrc.exists(path) == 200:      # 4. path exists
        #    _dprint(f"`{path}` already exists")
        #    return
        rsp = self.__wrap(self.__mrc.folder_add(path))
        if (rsp):
            print(rsp)

    def do_get(self, arg):
        """Download file (ftp GET)\nUsage:
        get <path> [<localfile> (default - same as src *Name*]"""
        path = self.__norm_path(arg)
        rsp = self.__wrap(self.__mrc.entry_info(path))
        if rsp:
            assert rsp['type'] == 'file'
            self.__mrc._file_get(path, rsp['name'])

    def _do_put(self, args):
        """Upload file (ftp PUT)"""
        self.__not_implemented()

    def do_cp(self, arg):
        """Copy folder/file into folder\nUsage:
        cp <src> <folder>"""
        # TODO: check arg
        # TODO: check folder on invalid chars
        # TODO: rename mode
        args = arg.split(' ', 2)
        rsp = self.__wrap(self.__mrc.entry_copy(self.__norm_path(args[0]), self.__norm_path(args[1])))
        if (rsp):
            print(rsp)

    def do_mv(self, arg):
        """Move folder/file into folder\nUsage:
        mv <src> <folder>"""
        # TODO: check arg
        # TODO: check folder on invalid chars
        # TODO: rename mode
        args = arg.split(' ', 2)
        rsp = self.__wrap(self.__mrc.entry_move(self.__norm_path(args[0]), self.__norm_path(args[1])))
        if (rsp):
            print(rsp)

    def do_rn(self, arg):
        """Rename entry inplace\nUsage:
        rn <path> <name>"""
        """Move folder/file into folder\nUsage:
        mv <src> <folder>"""
        # TODO: check arg
        # TODO: check new name on invalid chars
        # TODO: rename mode
        args = arg.split(' ', 2)
        rsp = self.__wrap(self.__mrc.entry_rename(self.__norm_path(args[0]), args[1]))
        if rsp:
            print(rsp)

    def do_rm(self, arg):
        """Remove entry to trash (ftp DELE[TE])\nUsage:
        rm <path>"""
        # TODO: check arg exists
        # TODO: check entry exists
        rsp = self.__wrap(self.__mrc.entry_remove(self.__norm_path(arg)))
        if rsp:
            print(rsp)

    def do_trash(self, arg):
        """List trash content\nUsage:
        trash"""
        # TODO: check entries keys (e.g. mounts or shares)
        rsp = self.__wrap(self.__mrc.trash_list())
        if rsp and rsp['list']:
            # 1. head
            # line = 42 * '-'
            line = '-----+-----------------+-------------+----'
            print(line)
            print('{:5} {:17} {:13} Name [deleted from]'.format('Rev', 'Deleted', 'Size'))
            print(line)
            # 2. body
            for f in rsp['list']:
                assert f['type'] == f['kind']
                assert f['type'] in set(('folder', 'file'))
                name = f['name']
                if f['type'] == 'folder':
                    name += '/'
                print('{:5d} {:17} {:13d} {} [{}]'.format(
                    f['rev'], self.__ut2dt(f['deleted_at'], '%y.%m.%d %H:%M:%S'), f['size'], name, f['deleted_from']
                ))
            print(line)

    def do_purge(self, arg):
        """Empty trash.\nUsage:
        purge"""
        # TODO: chech arg
        rsp = self.__wrap(self.__mrc.trash_empty())
        print(rsp)

    def do_restore(self, arg):
        """Restore entry from trash.\nUsage:
        restore <rev> <new_path> [rename]"""
        # TODO: chech arg
        # TODO: check target folder exists
        # TODO: rename option
        args = arg.split()
        rsp = self.__wrap(self.__mrc.trash_restore(int(args[0]), self.__norm_path(args[1])))

    def do_pub(self, arg):
        """Publish entry.\nUsage:
        pub <path>"""
        rsp = self.__wrap(self.__mrc.entry_publish(self.__norm_path(arg)))
        print(rsp)

    def do_unpub(self, arg):
        """Unpublish entry.\nUsage:
        unpub <path>"""
        rsp = self.__wrap(self.__mrc.pub_close(arg))

    def do_pub_info(self, arg):
        """Get public info.\nUsage:
        pub <path>"""
        rsp = self.__wrap(self.__mrc.pub_info(arg))
        if rsp:
            print("Long={}, Short={}".format(rsp['long'], rsp['short']))

    def do_pub_ro(self, arg):
        """Set public ro.\nUsage:
        pub_ro <path>"""
        rsp = self.__wrap(self.__mrc.pub_ro(arg))

    def do_pub_rw(self, arg):
        """Set public rw.\nUsage:
        pub_ro <path>"""
        rsp = self.__wrap(self.__mrc.pub_rw(arg))

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
        # TODO: optional payload
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

    def do_test(self, args):
        """Just for tests"""
        self.__mrc._test_exists(args)

def main():
    t = Terminal(MailRuCloudClient()).cmdloop()
    # print(json.dumps(mrc.ls('/8'), sort_keys=True, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
