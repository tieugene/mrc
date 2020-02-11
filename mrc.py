# -*- utf-8 -*-
# Library to handle Cloud@Mail.ru

import os, sys, time, json, requests
import pprint
from const import *

DEBUG = True
GOOD_RESPONSE = set((200, 201, 302))    # OK, Created, Found (temporary moved)
start = None

def getcsec():
    '''
    Get current seconds
    :return: current unixtime in seconds
    '''
    return int(time.time())

# = Debug functions
def dprint(s, end='\n'):
    '''
    prints debug info
    :param s: to print
    :param end: EOL separator
    :return: None
    '''
    if (DEBUG):
        print(s, file=sys.stderr, end=end, flush=True)

class MailRuCloudClient:
    '''
    Manipulate Cloud@Mail.Ru storage
    '''

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
        self.__dURL = None      # like https://cloclo4.cloud.mail.ru/attach/
        self.__uURL = None      # like https://cld-upload4.cloud.mail.ru/upload-web/

    def __debug_response(self, response):
        dprint('= Response: =')
        dprint('Code: {}'.format(response.status_code))
        dprint('-- Cookies: --')
        #if (self.__session.cookies.multiple_domains()):
        for d in self.__session.cookies.list_domains():
            print('Domain: {}, cookies: {}'.format(d, self.__session.cookies.get_dict(domain=d)))
        #else:
        #for k, v in self.__session.cookies.iteritems():
        #    dprint('{}: {}'.format(k, v))
        dprint('= /Response =')
        #print("Final url:", response.url)

    def __performAction(self, url, data=None):
        '''
        POST something
        :param url:
        :param data:dict Payload
        :return: Response() object
        '''
        response = self.__session.post(
            url,
            header = {
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

    def __authenticate(self, l, p):
        '''
        Authorize (10 sec)
        :param l - login
        :param p - password
        :return: True if ok
        '''
        dprint("Auth...", end='')
        self.__login = l
        self.__password = p
        response = self.__session.post(
            url=AUTH_ENDPOINT,  # https://auth.mail.ru/cgi-bin/auth
            data={
                'Login': self.__login,
                'Password': self.__password,
                'Domain': 'mail.ru',
                'new_auth_form': '1',
            })
        #self.__debug_response(response)
        if ((response) and (self.__session.cookies) and (self.__session.cookies.multiple_domains())):
            return True
        dprint("Failed to auth {}".format(self.__login))
        return False

    def __obtainCloudCookie(self):
        '''
        Get Cloud cookie for authorized user (6 sec).
        :return: True if ok
        '''
        dprint("Cloud cookie...", end='')
        # TODO: check cookies on .auth.mail.ru entries B4
        response = self.__session.get(url=SCLD_COOKIE_ENDPOINT, params={'from': CLOUD_DOMAIN})
        if ((response) and (self.__session.cookies) and (self.__session.cookies.get('sdcs', domain='.cloud.mail.ru'))):
            return True
        dprint('Seems you are not logged in')
        return False

    def __obtainAuthToken(self):
        '''
        Get token.
        TODO: check result
        :return:
        '''
        dprint("Token...", end='')
        response = self.__session.get(url = SCLD_TOKEN_ENDPOINT)
        #self.__debug_response(response)
        if (response):
            try:
                js = json.loads(response.content.decode("utf-8"))
            except:
                dprint('Response is not json')
                return False
            if ('body' in js) and ('token' in js['body']):
                self.__token = js['body']['token']
                dprint(self.__token)
                return True
            dprint('Not `body` or `token` keys: {}'.format(js))
        else:
            dprint('Bad response: {}'.format(response.status_code))
        return False

    def __get_download_source(self):
        '''
        Fill out download and upload direct endpoints
        :return:
        '''
        dprint("Down-/upload URLs...", end='')
        response = self.__session.get(url = SCLD_SHARD_ENDPOINT, params = {"token": self.__token})
        if (response):
            self.__dURL = json.loads(response.content.decode("utf-8"))['body']['get'][0]['url']
            self.__uURL = json.loads(response.content.decode("utf-8"))['body']['upload'][0]['url']
            dprint('D: {}, U: {}'.format(self.__dURL, self.__uURL))
            return True
        return False

    def login(self, l, p):
        '''
        Log in
        :param l: login 
        :param p: password
        :return: OK
        '''
        return (
            self.__authenticate(l, p) and
            self.__obtainCloudCookie() and
            self.__obtainAuthToken() and
            self.__get_download_source()
        )

    def __do_get(self, endpoint, params):
        '''
        Do get request. Handle token[, 404]
        :param endpoint: path after CLOUD_DOMAIN
        :param params: payload
        :return:
        '''
        # TODO: retry token
        response = self.__session.get(
            url = endpoint,
            params = {
                "token": self.__token
            },
        )

    def ask(self, path):
        '''
        Check entry. Do get file?home=path.
        TODO: cache folder content
        :param path:
        :return: ?/403/404
        '''
        self.__do_get(SCLD_FILE_ENDPOINT)

    def folder_add(self, path, resolve):
        '''
        Create new folder
        :param path:
        :param resolve How to solve conflict - ignore (replace)/new name/reject
        :return:
        '''
        pass

    def folder_read(self, path):
        '''
        Get folder content.
        TODO: get cached
        :param path:
        :return: folder/403/404/is file
        '''
        response = self.__session.get(
            url = SCLD_FOLDER_ENDPOINT,
            params={
                "home": folder,
                "token": self.__token
            },
        )
        if response.status_code == 200:
            print('==== Headers ====')
            hdrs = response.headers  # CaseInsensitiveDict
            pprint.pprint(hdrs)
            print('==== Headers ====')
            return response.json()
        elif response.status_code == 403:
            # tokens seem to expire
            print("Got HTTP 403 on listing folder contents, retrying...")
            self.__obtainAuthToken()
            return self.get_folder_contents(folder)
        elif response.status_code == (400 or 404):
            print("File or folder not found: %s" % folder)
        else:
            # wtf?
            print('Error: [%d] %s' % (response.status_code, response.text))
            exit(1)

    def folder_rename(self, path, new_name):
        '''
        ???
        Rename folder inplace
        :param path:
        :param new_name:
        :return:
        '''
        pass

    def folder_move(self, path, new_folder):
        '''
        ???
        Move folder into new place.
        :param path:
        :param new_folder:
        :return:
        '''
        pass

    def folder_del(self, path):
        '''
        Delete folder
        :param path: folder to del
        :return:
        '''
        pass

    def file_add(self, path, src_path, resolve):
        '''
        Create (upload) new file
        :param path:
        :param src_path:
        :param resolve How to solve conflict - ignore (replace)/new name/reject
        :return:
        '''
        pass

    def file_read(self, path, dst_path):
        '''
        Read (download) file
        :param path:
        :param dst_path:
        :return: Ok/403/404
        '''

    def file_rename(self, path, new_name, resolve):
        '''
        Rename file inplace
        :param path:
        :param new_name:
        :param resolve How to solve conflict - ignore (replace)/new name/reject
        :return:
        '''
        pass

    def file_move(self, path, new_path, resolve):
        '''
        Move file into new place
        :param path:
        :param new_path:
        :param resolve How to solve conflict - ignore (replace)/new name/reject
        :return:
        '''
        pass

    def file_del(self, path):
        '''
        Delete file
        :param path:
        :return: ok/403/404
        '''
        pass

    def _test1(self):
        '''
        Test combinations of folder/file?home=folder/file with misc Referers
        :return: None
        '''
        for e in ('file', 'folder'):                # endpoint
            for h in ('/1', '1/2.txt'):             # ?home=
                dprint('{} {}:'.format(e, h))
                response = self.__session.get(
                    url = CLOUD_DOMAIN + '/api/v2/' + e,
                    params={
                        "home": h,
                        "token": self.__token,
                    }
                )
                if (response):
                    pprint.pprint(response.text)
