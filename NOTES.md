# Notes

## Interestings:
- [Cmd](https://docs.python.org/3.7/library/cmd.html)
- [MRC Total Plugin](https://github.com/pozitronik/CloudMailRu)
- [All API](https://www.pvsm.ru/php-2/114459)
- [.Net client](https://github.com/erastmorgan/Mail.Ru-.net-cloud-client) - [rich client](https://habr.com/ru/post/281360/)
- [C@MR downloader PHP](https://github.com/Geograph-us/Cloud-Mail.Ru-Downloader)

## Idea:
- cache metainfo into key-value file:
  - [Redis](https://redislabs.com/lp/python-redis/) ([tour](https://python-scripts.com/redis))
  - Memcached
  - [Tokyo cabinet](https://pythonhosted.org/tokyocabinet-python/)
  - [BDB](https://docs.python.org/2/library/bsddb.html)
  - [UniQLite](http://charlesleifer.com/blog/introduction-to-the-fast-new-unqlite-python-bindings/)
  - Sqlite
- rsync-like utility specially for mrc (sha1)

## Note:
> В названии папок нельзя использовать символы «" * / : < > ? \ |». Также название не может состоять только из точки «.» или из двух точек «..»

Invalid chars: `"*:<>?\|`

## Start:
SDC - Streamset Data Collector
1. Login (POST https://auth.mail.ru/cgi-bin/auth?Login=<login>&Password=<password>&Domain=mail.ru&new_auth_form=1):
  - Code: 200 (anywhen)
  - Header: garbadge
  - Body: garbadge (html page)
  - Cookies (domain/key: value; 3 domains):
    - Err:
```
.mail.ru/act: <32x>
.mail.ru/mrcu: <28X>
.mail.ru/o: ':192:.s
```
    - OK:
```
.auth.mail.ru/GarageID: <32x>
.auth.mail.ru/ssdc: <32x>
.auth.mail.ru/ssdc_info: <4x:1:10d>
.e.mail.ru/sdcs: <16b64> (12 bytes) - 
.mail.ru/Mpop: <10d from sdcs>:<94x>:<login>:
.mail.ru/act: <32x>
.mail.ru/mrcu: <28X>
.mail.ru/o: <login>:192:.s
.mail.ru/s: 
.mail.ru/t: <88s>
```
2. Get cloud cookie (GET/POST https://auth.mail.ru/sdc?from=https://cloud.mail.ru/home):
  - Code: 200 (anywhen)
  - Header: garbadge
  - Body: garbadge (html page)
  - Cookies (4 domains):
    - Err:
    - OK: same as Login +.cloud.mail.ru/sdcs: <16b64>
3. Get token (POST https://cloud.mail.ru/api/v2/tokens/csrf):
  - Code: 200/403

## To find:
- ask for folder/file stat ([g]rev | mtime|hash):
 - folder - file?home=<folder> 
 - file - file?home=<folder>
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

ls:

Folder ... (x folders, y files, ...):
==========================
Type Size (<=2G) grev_rev_tree / mtime_hash
= ====
T 

## Response:
- status:int
- time:int
- email:<email>
- body:<entry>
### File:

- entity:
  - kind:str=folder/file
  - type:str=folder/file
  - home:str - full path (/...)
  - name:str - name
  - [size:int] - folder: in folder? request only
- Folder(entity):
  - count:{files:int, folders:int}
  - grev:int
  - rev:int
  - tree:int?
- File(entity):
  - hash:hex(40X) - ?SHA-1
  - mtime:int - ?unixtime
  - virus_scan:str = "pass"
  - [message:str = ""]
  - ["weblink:str - after ("EDAS/ZegcnyJrJ")]
  - ["weblink_access_rights:str = "r"]

## Note request file/folder? (!):
- Referer ни на что не влияет
- Code == 200
- file всегда отдает [короткие] метаданные объекта
- folder всегда отдает полные метаданные папки
- содержимое - https://cloud.mail.ru/api/v2/dispatcher['body']['get'][0]['url']

GET folder?home=/tmp/Digma_e65g
- home: /tmp/Digma_e65g
- sort: {"type":"name","order":"asc"}
- offset: 0
- limit: 500
- api: 2
Прилетает весь folder json

GET file?
- home: /tmp/Digma_e65g
- api: 2
- Прилетает краткий folder json:
```
{"email":"ti.eugene@mail.ru","body":{"count":{"folders":1,"files":2},"tree":"356165343634623030303030","name":"Digma_e65g","grev":13683,"kind":"folder","rev":13628,"type":"folder","home":"/tmp/Digma_e65g"},"time":1580943818684,"status":200}
```
