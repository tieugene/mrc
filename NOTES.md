note: don't forget xdg for md: text/markdown

17 sec to 1st response

Interestings:
[Cmd](https://docs.python.org/3.7/library/cmd.html)
[MRC Total Plugin](https://github.com/pozitronik/CloudMailRu)
[All API](https://www.pvsm.ru/php-2/114459)
[.Net client](https://github.com/erastmorgan/Mail.Ru-.net-cloud-client) - [rich client](https://habr.com/ru/post/281360/)
[C@MR downloader PHP](https://github.com/Geograph-us/Cloud-Mail.Ru-Downloader)

Note:
В названии папок нельзя использовать символы «" * / : < > ? \ |». Также название не может состоять только из точки «.» или из двух точек «..»
"ITEM_NAME_INVALID_CHARACTERS": "\"*/:\x3c>?\\|",
"ITEM_PATH_INVALID_CHARACTERS": "\"*:\x3c>?\\|",

To find:
- ask for folder/file stat ([g]rev | mtime|hash):
 - folder - file?home=<folder> 
 - file - file?home=<folder> [Referer=<file>]
 - HEAD?
 - OPTIONS?
- Cache (header) https://html5.by/blog/cache/:
  - ~~etag~~
  - ~~Last-Modified~~
  - ~~Expired~~: <Date>
  - ~~Cache-Control~~: no-store, no-cache, must-revalidate
  - Date
- short query

Note response:
- status_code
- headers (dict)
- cookies (dict?)
- text

Commands:
- pwd   PWD
- ls    LIST
- cd    C[W]D
- get   GET
- put   PUT
- rm    DELE[TE]
- md    MKD[IR]
- rd    RMD[IR]
- lpwd  <local pwd>
- lls   <local ls>
- lcd   <local cd>
- quit  QUIT
- ?     FEAT/HELP
- mget
- mput

ls:
Folder ... (x folders, y files, ...):
==========================
Type Size (<=2G) grev_rev_tree / mtime_hash
= ====
T 

Response:
...
entity:
    kind:str
    type:str
    home:str - full path (/...)
    name:str - folder/file name
    size:int
Folder(entity):
    kind:str=folder
    type:str=folder
    count:{files:int, folders:int}
    grev:int
    rev:int
    tree:int?
File(entity):
    kind:str=file
    type:str=file
    hash:hex(40X) - ?SHA-1
    mtime:int - ?unixtime
    virus_scan:str = "pass"
    [message:str = ""]
    ["weblink:str - after ("EDAS/ZegcnyJrJ")]
    ["weblink_access_rights:str = "r"]

GET folder?home=/tmp/Digma_e65g
[Referer: https://cloud.mail.ru/home/tmp/]
home: Digma_65e
sort: {"type":"name","order":"asc"}
offset: 0
limit: 500
api: 2
Прилетает весь folder json

GET file?
home: /tmp/Digma_e65g
api: 2
[Referer: https://cloud.mail.ru/home/tmp/Digma_e65g/e65g_20170130.7z]
Прилетает краткий folder json:
{"email":"ti.eugene@mail.ru","body":{"count":{"folders":1,"files":2},"tree":"356165343634623030303030","name":"Digma_e65g","grev":13683,"kind":"folder","rev":13628,"type":"folder","home":"/tmp/Digma_e65g"},"time":1580943818684,"status":200}

Сначала идет:
1. space
2. file?home=folder (referer=file)

Try D/F? X home=D/F X Referer = D/F/-