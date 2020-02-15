"""
Exceptions
https://pythonworld.ru/tipy-dannyx-v-python/isklyucheniya-v-python-konstrukciya-try-except-dlya-obrabotki-isklyuchenij.html
https://devarea.com/python-exceptions-and-error-handlings/
"""


class MailRuCloudError(Exception):
    pass

    class AuthError(Exception):
        def __init__(self, message="Login or password is incorrect"):
            super(MailRuCloudError.AuthError, self).__init__(message)

    class NotLoggedIn(Exception):
        def __init__(self, message="Seems you are not logged in"):
            super(MailRuCloudError.NotLoggedIn, self).__init__(message)

    class NetworkError(Exception):
        def __init__(self, message="Connection failed"):
            super(MailRuCloudError.NetworkError, self).__init__(message)

    class NotFoundError(Exception):
        def __init__(self, message="File not found"):
            super(MailRuCloudError.NotFoundError, self).__init__(message)

    class PublicLinksExceededError(Exception):
        def __init__(self, message="Public links number exceeded"):
            super(MailRuCloudError.PublicLinksExceededError, self).__init__(message)

    class UnknownError(Exception):
        def __init__(self, message="WTF is going on?"):
            super(MailRuCloudError.UnknownError, self).__init__(message)

    class NotImplementedError(Exception):
        def __init__(self, message="The developer wants to sleep"):
            super(MailRuCloudError.NotImplementedError, self).__init__(message)

    class FileSizeError(Exception):
        def __init__(self, message="The file is bigger than 2 GB"):
            super(MailRuCloudError.FileSizeError, self).__init__(message)
