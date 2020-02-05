# -*- utf-8 -*-
# Library to handle Cloud@Mail.ru

from utils import *
import requests
import os, json, pprint

class MarcRestClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': '*/*',
            'Origin': CLOUD_DOMAIN,
            'User-Agent': SAFE_USER_AGENT,
        })
        self.token = None
        self.login = None
        self.password = None

    def __performAction(self, url, data = None):
        response = self.session.post(url, data = data)
        if (response.status_code not in set((200, 201, 302))):
            print("Bad code: %d" % response.status_code)
            exit(1)
        # print("Final url:", response.url)
        return response

    def __authenticate(self):
        # Login={0}&Domain={1}&Password={2}
        print("Auth...")
        self.__performAction(
            url=AUTH_ENDPOINT,                  # https://auth.mail.ru/cgi-bin/auth
            data={
                'Login': self.login,
                'Password': self.password,
                'Domain': 'mail.ru',
                'new_auth_form': '1',
        })
        if (not self.session.cookies):
            print("Failed to auth % " % self.login)
            exit(1)

    def __obtainCloudCookie(self):
        print("Cloud cookie...")
        cookiesSize = len(self.session.cookies)
        self.__performAction(
            url=SCLD_COOKIE_ENDPOINT,           # https://auth.mail.ru/sdc
            data={
                'from': CLOUD_DOMAIN + "/home", # https://cloud.mail.ru
        })
        if (len(self.session.cookies) <= cookiesSize):
            print('Failed to obtain cloud cookie, did you sign up to the cloud?')
            exit(1)

    def __obtainAuthToken(self):
        print("Token...")
        response = self.__performAction(
            url=SCLD_TOKEN_ENDPOINT,            # https://cloud.mail.ru/api/v2/tokens/csrf
        )
        try:
            js = json.loads(response.content.decode("utf-8"))
        except:
            print('Response is not json')
            exit(1)
        if ('body' not in js) or ('token' not in js['body']):
            print('Not body or token: ' + js)
            exit(1)
        self.token = js['body']['token']
        #print('I have the token: %s' % self.token)
        #print(response.text)

    def log_in(self, l, p):
        self.login = l
        self.password = p
        self.__authenticate()
        self.__obtainCloudCookie()
        self.__obtainAuthToken()

    def ls(self, folder):
        response = self.session.get(SCLD_FOLDER_ENDPOINT,
            params={
                "home": folder,
                "token": self.token
            },
        )
        if response.status_code == 200:
            print('==== Headers ====')
            hdrs = response.headers # CaseInsensitiveDict
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
