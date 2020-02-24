# Notes
- teach https://cloud.mail.ru/trashbin/ (move to, ls, delete)
- teach https://cloud.mail.ru/favorites/
- try http delete, /folder/remove/

## Interestings:
- [Cmd](https://docs.python.org/3.7/library/cmd.html)
- [MRC Total Plugin](https://github.com/pozitronik/CloudMailRu)
- [All API](https://www.pvsm.ru/php-2/114459)
- [.Net client](https://github.com/erastmorgan/Mail.Ru-.net-cloud-client) - [rich client](https://habr.com/ru/post/281360/)
- [C@MR downloader PHP](https://github.com/Geograph-us/Cloud-Mail.Ru-Downloader)

## Idea:
- cache entries metainfo into key-value file:
  - [Redis](https://redislabs.com/lp/python-redis/) ([tour](https://python-scripts.com/redis))
  - Memcached
  - [Tokyo cabinet](https://pythonhosted.org/tokyocabinet-python/)
  - [BDB](https://docs.python.org/2/library/bsddb.html)
  - [UniQLite](http://charlesleifer.com/blog/introduction-to-the-fast-new-unqlite-python-bindings/)
  - Sqlite
- rsync-like utility specially for mrc (sha1-based)

## Note:

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
- [Cache](https://html5.by/blog/cache/):
  - ~~etag~~
  - ~~Last-Modified~~
  - ~~Expired~~: <Date>
  - ~~Cache-Control~~: no-store, no-cache, must-revalidate
  - Date

Guess:
rev: изменился _состав_ и/или _размер_ _этой_ папки
grev: ... подчиненной ...
rrev: ?

==== Download ====
1. https://cloud.mail.ru/public/31Zh/4bBd2Ujau - получаем печеньки
~~GET https://cloud.mail.ru/api/v2/dispatcher =>~~ 
2. POST: https://cloud.mail.ru/api/v2/tokens/download => token	37448c4f5478e0386594e9a3efbd845d3323e52a + file?
~~GET https://cloclo10.cldmail.ru/2xiL6QhmiaWNT2EUhRnk/G/31Zh/4bBd2Ujau?key=37448c4f5478e0386594e9a3efbd845d3323e52a~~
