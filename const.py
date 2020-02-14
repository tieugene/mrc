SAFE_USER_AGENT         = "Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0";
AUTH_DOMAIN             = "https://auth.mail.ru";
CLOUD_DOMAIN            = "https://cloud.mail.ru";
AUTH_ENDPOINT               = AUTH_DOMAIN + "/cgi-bin/auth";
SCLD_COOKIE_ENDPOINT        = AUTH_DOMAIN + "/sdc";
SCLD_PUBLICLINK_ENDPOINT    = CLOUD_DOMAIN + "/public";
SCLD_TOKEN_ENDPOINT         = CLOUD_DOMAIN + "/api/v2/tokens/csrf";
SCLD_SHARD_ENDPOINT         = CLOUD_DOMAIN + "/api/v2/dispatcher";
SCLD_SPACE_ENDPOINT         = CLOUD_DOMAIN + "/api/v2/user/space";
SCLD_FOLDER_ENDPOINT        = CLOUD_DOMAIN + "/api/v2/folder";
SCLD_FOLDERADD_ENDPOINT     = CLOUD_DOMAIN + "/api/v2/folder/add";
SCLD_FILE_ENDPOINT          = CLOUD_DOMAIN + "/api/v2/file";
SCLD_FILEADD_ENDPOINT       = CLOUD_DOMAIN + "/api/v2/file/add";
SCLD_FILEPUBLISH_ENDPOINT   = CLOUD_DOMAIN + "/api/v2/file/publish";
SCLD_FILEREMOVE_ENDPOINT    = CLOUD_DOMAIN + "/api/v2/file/remove";
SCLD_FILERENAME_ENDPOINT    = CLOUD_DOMAIN + "/api/v2/file/rename";
SCLD_FILEMOVE_ENDPOINT      = CLOUD_DOMAIN + "/api/v2/file/move";

# text colors (https://ozzmaker.com/add-colour-to-text-in-python/)
# \033[<0..3;>m
#
class bcolors:
    NORMAL      = '\033[0m'
    BRIGHT      = '\033[1m'
    UNDERLINE   = '\033[2m'
    NEG1        = '\033[3m'
    UNKNOWN     = '\033[4m'
    NEG2        = '\033[5m'
    BLACK       = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
