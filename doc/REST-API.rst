=========================
Cloud@Mail.Ru REST API V2
=========================

Undocumented subj API.

.. contents:: Table of Contents

General considerations
======================

Authentication
--------------

In order to specify SiteAccess when talking to the REST API, a custom header, `X-Siteaccess`, needs to be provided.
If it isn't, the default one will be used.

Requests
--------

Overview
~~~~~~~~

.. list-table:: All API (sorted by endpoint)
   :widths: 1 10 1 30
   :header-rows: 1

   * - №
     - Endpoint
     - M
     - Description
   * - 1
     - /dispatcher
     - G
     - Get download/upload URLs
   * - 2
     - /file
     - G
     - Get entry info
   * - 3
     - /file/add
     - P
     - Upload file
   * - 4
     - /file/copy
     - P
     - Copy entry 2 folder
   * - 5
     - /file/history
     - G
     - Get file history
   * - 6
     - /file/move
     - P
     - Move entry to folder
   * - 7
     - /file/publish
     - P
     - Publish entry
   * - 8
     - /file/remove
     - P
     - Delete entry (2 Trash)
   * - 9
     - /file/rename
     - P
     - Rename entry inplace
   * - 10
     - /file/unpublish
     - P
     - Unpublish entry
   * - 11
     - /folder
     - G
     - Get folder content
   * - 12
     - /folder/add
     - P
     - Create folder
   * - 13
     - /folder/invites
     - G
     - List incoming invites
   * - 14
     - /folder/invites/info
     - G
     - Info about invite
   * - 15
     - /folder/invites/reject
     - P
     - Reject ivitate
   * - 16
     - /folder/mount
     - P
     - Подключить' invite
   * - 17
     - /folder/share
     - P
     - [Re]share folder to other (invite)
   * - 18
     - /folder/shared
     - G
     - 403: user
   * - 19
     - /folder/shared/incoming
     - G
     - List incoming invites
   * - 20
     - /folder/shared/info
     - G
     - Get published entry info
   * - 21
     - /folder/shared/links
     - G
     - List ...
   * - 22
     - /folder/tree
     - G
     - `folder` of /..<target>
   * - 23
     - /folder/unmount
     - P
     - Отключить foreign share
   * - 24
     - /folder/unshare
     - P
     - Remove share x user
   * - 25
     - /tokens/csrf
     - P
     - Get session token
   * - 26
     - /tokens/download
     - P
     - Get ? token
   * - 27
     - /trashbin
     - G
     - Get Trash content
   * - 28
     - /trashbin/empty
     - P
     - Clean Trash
   * - 29
     - /trashbin/restore
     - P
     - Restore file from Trash
   * - 30
     - /user
     - G
     - Get all user info
   * - 31
     - /user/edit
     - P
     - Update user UI
   * - 32
     - /user/space
     - G
     - Usage (used, total)
   * - 33
     - /weblinks
     - G
     - Get weblink info
   * - 34
     - /weblinks/readonly
     - P
     - Set published RO
   * - 35
     - /weblinks/writable
     - P
     - Set published RW
   * - 36
     - /zip
     - P
     - Download as zip

Terms
`````

:Path:
    Full entry path, e.g. /dir1/dir2/file3
:WebLink:
    %4w/%9w (e.g. EDAS/ZegcnyJrJ)
:Token:
    %32w (e.g. ...) - 24-byte B64 ?
:Tree:
    %24d (e.g. ...) - 18-byte B64 ?
:Hash:
    %40X (e.g. ...) - 20-byte

Common
~~~~~~

:Resource: https://cloud.mail.ru/api/v2/
:Parameters:
    :token:
        *Token*
    :[api]:
        2
:Response:
    :email:
        ...
    :body:
        ...
:Error Codes:
    :200:
        OK
    :400:
        Bad Request (e.g. required params absent)
    :403:
        Forbidden (no token?)
    :404:
        Not Found (e.g. object really not exists)
    :406:
        Not Acceptable (e.g. /file/history for folder)

Entry
~~~~~

Entry Info
``````````

:Resource: /file
:Method: GET
:Description: Get folder/file metainfo
:Parameters:
    :home: *Path*
:Response:

Copy Entry
``````````

:Resource: /file/copy
:Method: POST
:Description: Copy *Entry* into other folder
:Parameters:
    :home: *Path*
    :folder: Path of folder copy to
    :conflict: rename/.../... (Usual rename)
:Response:

Move Entry
``````````

:Resource: /file/move
:Method: POST
:Description: Move folder/file into other folder
:Parameters:
    :home: Path.
    :folder: Path of folder move to
    :conflict: rename/.../... Usual rename
:Response:

Rename Entry
````````````

:Resource: /file/rename
:Method: POST
:Description: Rename folder/file inplace (?)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:

Remove Entry
````````````

:Resource: /file/remove
:Method: POST
:Description: Remove folder/file into *Trashbin*
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:

Files
~~~~~

Upload File
```````````

:Resource: /file/add
:Method: POST
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

File History
````````````

:Resource: /file/history
:Method: GET
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Folder
~~~~~~

Create Folder
`````````````

:Resource: /folder/add
:Method: POST
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

List Folder
```````````

:Resource: /folder
:Method: GET
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Folder Tree
```````````

:Resource: /folder/tree
:Method: GET
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Trashbin
~~~~~~~~

List Trashbin
`````````````

:Resource: /trashbin
:Method: GET
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Clear Trashbin
``````````````

:Resource: /trashbin/empty
:Method: POST
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Misc
~~~~

Dispatcher
``````````

User info
`````````

User edit
`````````

Used space
``````````

Zip
```

Example
```````

:Headers:
    :Accept:
        :application/vnd.ez.api.BookmarkList+xml:  if set the list is returned in XML format
        :application/vnd.ez.api.BookmarkList+json: if set the list is returned in JSON format
:Response:

.. code:: http

    HTTP/1.1 200 OK
    Location: /bookmark
    Accept-Patch:  application/vnd.ez.api.BookmarkList+(json|xml)
    ETag: "<newEtag>"
    Content-Type: <depending on accept header>
    Content-Length: <length>

:Error Codes:
        :401: If the user is not authorized to list bookmarks
