# -*- utf-8 -*-
# Library to handle Cloud@Mail.ru

import os, sys, time, json, requests
import pprint
from requests import Response
from const import *
from oops import MailRuCloudError

DEBUG = True
GOOD_RESPONSE = set((200, 201, 302))  # OK, Created, Found (temporary moved)
start = None


def _getcsec() -> int:
    """
    Get current seconds
    :return: current unixtime in seconds
    """
    return int(time.time())


def _dprint(s: str, end: str = '\n') -> None:
    """
    Prints debug info
    :param s: to print
    :param end: EOL separator
    :return: None
    """
    if DEBUG:
        print(s, file=sys.stderr, end=end, flush=True)


class MailRuCloudClient:
    """
    Manipulate Cloud@Mail.Ru storage
    """

    def __init__(self):
        self.__session = requests.Session()
        self.__session.headers.update({
            'Accept': '*/*',
            'Origin': CLOUD_DOMAIN,
            'User-Agent': SAFE_USER_AGENT,
        })
        self.__login = None
        self.__password = None
        self.__token = None
        self.__dURL = None  # like https://cloclo4.cloud.mail.ru/attach/
        self.__uURL = None  # like https://cld-upload4.cloud.mail.ru/upload-web/

    def __debug_response(self, response: Response) -> None:
        """
        Print response details
        :param response:
        """
        _dprint('= Response: =')
        _dprint(f'Code: {response.status_code}')
        _dprint('-- Cookies: --')
        # if (self.__session.cookies.multiple_domains()):
        for d in self.__session.cookies.list_domains():
            print('Domain: {}, cookies: {}'.format(d, self.__session.cookies.get_dict(domain=d)))
        # else:
        # for k, v in self.__session.cookies.iteritems():
        #    dprint(f'{k}: {v}')
        _dprint('= /Response =')
        # print("Final url:", response.url)

    def __performAction(self, url: str, data=None):
        """
        POST something
        :param url:
        :param data:dict Payload
        :return: Response() object
        """
        response = self.__session.post(
            url,
            header={
                'Accept': '* / *',
                'Origin': CLOUD_DOMAIN,
                'User-Agent': SAFE_USER_AGENT,
            },
            data=data,
        )
        if (not response):  # if (response.status_code is not in GOOD_RESPONSE):
            print("Bad code: %d" % response.status_code)
            exit(1)
        return response

    def __authenticate(self) -> bool:
        """
        Authorize (10 sec)
        :return: True if ok
        :rtype: bool
        """
        _dprint("Auth...", end='')
        response = self.__session.post(
            url=AUTH_ENDPOINT,  # https://auth.mail.ru/cgi-bin/auth
            data={
                'Login': self.__login,
                'Password': self.__password,
                'Domain': 'mail.ru',
                'new_auth_form': '1',
            })
        # self.__debug_response(response)
        if ((response) and (self.__session.cookies) and (self.__session.cookies.multiple_domains())):
            return True
        _dprint("Failed to auth {}".format(self.__login))
        return False

    def __obtainCloudCookie(self):
        """
        Get Cloud cookie for authorized user (6 sec).
        :return: True if ok
        """
        _dprint("Cookie...", end='')
        # TODO: check cookies on .auth.mail.ru entries B4
        response = self.__session.get(url=SCLD_COOKIE_ENDPOINT, params={'from': CLOUD_DOMAIN})
        if ((response) and (self.__session.cookies) and (self.__session.cookies.get('sdcs', domain='.cloud.mail.ru'))):
            return True
        _dprint('Seems you are not logged in')
        return False

    def __obtainAuthToken(self):
        """
        Get token.
        TODO: check result
        :return:
        """
        _dprint("Token...", end='')
        response = self.__session.get(url=SCLD_TOKEN_ENDPOINT)
        # self.__debug_response(response)
        if (response):
            try:
                js = response.json()    # json.loads(response.content.decode("utf-8"))
            except:
                _dprint('Response is not json')
                return False
            if ('body' in js) and ('token' in js['body']):
                self.__token = js['body']['token']
                #dprint(self.__token)
                return True
            _dprint('Not `body` or `token` keys: {}'.format(js))
        else:
            _dprint('Bad response: {}'.format(response.status_code))
        return False

    def __get_download_source(self):
        """
        Fill out download and upload direct endpoints
        :return:
        """
        _dprint("URLs...", end='')
        response = self.__session.get(url=SCLD_SHARD_ENDPOINT, params={"token": self.__token})
        if (response):
            url = response.json()['body']
            self.__dURL = url['get'][0]['url']
            self.__uURL = url['upload'][0]['url']
            _dprint('OK')
            return True
        _dprint('oops')
        return False

    def login(self, l, p):
        """
        Log in
        :param l: login
        :param p: password
        :return: OK
        """
        self.__login = l
        self.__password = p
        return (
                self.__authenticate() and
                self.__obtainCloudCookie() and
                self.__obtainAuthToken() and
                self.__get_download_source()
        )

    def __chk_token(self):
        if not self.__token:
            raise MailRuCloudError.NotLoggedIn()

    def exists(self, path:str) -> int:
        """
        Test entry exists (B4 creating)
        :param path: entry to test
        :return: HTTP code
        """
        h = {"home": path}
        if self.__token:
            h["token"] = self.__token
        return self.__session.head(url=SCLD_FILE_ENDPOINT, params=h).status_code

    def __do_get(self, endpoint: str, payload: dict = {}) -> object:
        """
        Do get request. Handle token[, 404]
        :param endpoint: path after CLOUD_DOMAIN
        :param params: payload
        :return: response
        :exception: requests.exceptions.ReadTimeout
        """
        #if not self.__token:    # FIXME: raise NotAuth
        #    return
        h = {"token": self.__token} if self.__token else {}
        return self.__session.get(url=endpoint, params={**h, **payload})

    def __do_post(self, endpoint: str, payload: dict = {}) -> object:
        """
        Do get request. Handle token[, 404]
        :param endpoint: path after CLOUD_DOMAIN
        :param params: payload
        :return: response
        """
        h = {"token": self.__token} if self.__token else {}
        return self.__session.post(url=endpoint, data={**h, **payload})

    def entry_info(self, path: str) -> dict:
        """
        Check entry. Do get file?home=path.
        TODO: cache folder content
        :param path:
        :return: Response
        """
        #self.__chk_token()  # get out
        return self.__do_get(
            SCLD_FILE_ENDPOINT,
            {'home': path}
        )

    def entry_copy(self, path:str, folder:str, resolve:str = None) -> Response:
        """
        Copy entry into folder.
        :param path: entry to copy
        :param folder: folder copy to
        :return: Response
        """
        h = {'home': path, 'folder': folder}
        if resolve:
            h['conflict'] = resolve
        return self.__do_post(SCLD_FILECOPY_ENDPOINT, h)

    def entry_move(self, path:str, folder:str, resolve:str = None) -> Response:
        """
        Move entry into folder.
        :param path: entry to move
        :param folder: folder move to
        :return: Response
        """
        h = {'home': path, 'folder': folder}
        if resolve:
            h['conflict'] = resolve
        return self.__do_post(SCLD_FILEMOVE_ENDPOINT, h)

    def _entry_rename(self, path, new_name):
        """
        ???
        Rename folder inplace
        :param path:
        :param new_name:
        :return:
        """
        pass

    def _entry_remove(self, path):
        """
        Delete folder
        :param path: folder to del
        :return:
        """
        pass

    def _file_add(self, path, src_path, resolve):
        """
        Create (upload) new file
        :param path:
        :param src_path:
        :param resolve How to solve conflict - ignore (replace)/new name/reject
        :return:
        """
        pass

    def _file_read(self, path, dst_path):
        """
        Read (download) file
        :param path:
        :param dst_path:
        :return: Ok/403/404
        """

    def folder_add(self, path:str, resolve:str = None):
        """
        Create new folder.
        Return body: {"email":<login>>,"body":<path>>,"time":<timestamp>,"status":200}
        :param path: full path of folder to create
        :param resolve: How to solve conflict - rewrite|rename|strict (ignore (replace)/new name/reject?)
        :return:
        """
        h = {'home': path}
        if resolve:
            h['conflict'] = resolve
        return self.__do_post(SCLD_FOLDERADD_ENDPOINT, h)

    def folder_list(self, path):
        """
        Get folder content.
        TODO: get cached
        :param path:
        :return: folder/403/404/is file
        """
        return self.__do_get(
            SCLD_FOLDER_ENDPOINT,
            {'home': path}
        )

    def user_space(self) -> dict:
        """Space used"""
        if not self.__token:
            raise MailRuCloudError.NotLoggedIn()  # get out
        print("Go further")
        return self.__do_get(SCLD_SPACE_ENDPOINT)

    def any(self, method:str, url:str, payload:dict):
        """
        Fetch any request.
        :param method: get/post/head
        :type method: str
        :param url: tail of v2 api
        :type url: str
        :param payload: subj
        :return:Response
        """
        if not self.__token:    # FIXME: raise NotAuth
            return
        endpoint = CLOUD_APIv2 + url
        if method == Rq.GET.value:
            response = self.__session.get(
                url=endpoint,
                params={**{"token": self.__token}, **payload},
            )
        elif method == Rq.HEAD.value:
            response = self.__session.head(
                url=endpoint,
                params={**{"token": self.__token}, **payload},
            )
        elif method == Rq.POST.value:
            response = self.__session.post(
                url=endpoint,
                data={**{"token": self.__token}, **payload},
            )
        else:
            _dprint(f"Unknown method `{method}`")
            return
        return response

    def __test_f(self):
        """
        Test combinations of folder/file?home=folder/file with misc Referers
        :return: None
        """
        for e in ('file', 'folder'):  # endpoint
            for h in ('/1', '1/2.txt'):  # ?home=
                _dprint('{} {}:'.format(e, h))
                response: Response = self.__session.get(
                    url=CLOUD_DOMAIN + '/api/v2/' + e,
                    params={
                        "home": h,
                        "token": self.__token,
                    }
                )
                if response:
                    pprint.pprint(response.text)

    def __test_exists(self, path):
        """Test entry exists"""
        def __try(url, name):
            response: Response = self.__session.head(
                url=url,
                params={
                    "home": path,
                    "token": self.__token,
                }
            )
            print(f'{name}: {response.status_code}')
        __try(SCLD_FILE_ENDPOINT, 'File')
        __try(SCLD_FOLDER_ENDPOINT, 'Folder')