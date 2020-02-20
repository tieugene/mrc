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

Entry (5)
~~~~~~~~~

Info
````

:Resource: /file
:Method: GET
:Description: Get folder/file metainfo
:Parameters:
    :home: *Path*
:Response:

Copy
````

:Resource: /file/copy
:Method: POST
:Description: Copy *Entry* into other folder
:Parameters:
    :home: *Path* - entry to copy
    :folder: *Path* - folder copy to
    :conflict: `rename|rewrite|strict` (usual rename)
:Response: new path

Move
````

:Resource: /file/move
:Method: POST
:Description: Move *Entry* into other folder
:Parameters:
    :home: *Path* - Entry to move
    :folder: *Path* - Folder move to
    :conflict: `rename|rewrite|strict` (usual rename)
:Response:

Rename
``````

:Resource: /file/rename
:Method: POST
:Description: Rename *Entry* inplace
:Parameters:
    :home: *Path* - Entry to rename
    :name: *Name* - new name
    :conflict: `rename|rewrite|strict` (usual rename)
:Response: new path

Remove
``````

:Resource: /file/remove
:Method: POST
:Description: Remove Entry into *Trashbin*
:Parameters:
    :home: *Path* - entry to remove
    :hash?: ...
    :~~conflict~~: ...
:Response: path

File
~~~~

Upload File
```````````

:Resource: /file/add
:Method: POST
:Description: Upload file
:Parameters:
:Response:

File History
````````````

:Resource: /file/history
:Method: GET
:Description: List file history
:Parameters:
    :home: *Path*
:Response:

Folder
~~~~~~

List Folder
```````````

:Resource: /folder
:Method: GET
:Description: List folder content
:Parameters:
    :home: *Path*
    :[limit]: int
    :[offset]: int
    :sort:
        :type: `name|mtime|size`
        :order: `asc|desc`
:Response: list[]

Folder Tree
```````````

:Resource: /folder/tree
:Method: GET
:Description: List folders from /
:Parameters:
    :home: *Path*
:Response: list of `List Folder`s

Create Folder
`````````````

:Resource: /folder/add
:Method: POST
:Description: Create new folder
:Parameters:
    :home: *Path*
    :conflict: `rename|rewrite|strict` (usual rename)
:Response:

Trashbin
~~~~~~~~

List Trashbin
`````````````

:Resource: /trashbin
:Method: GET
:Description: List *Trashbin* content
:Parameters:
:Response:

Empty Trashbin
``````````````

:Resource: /trashbin/empty
:Method: POST
:Description: Empty Trashbin
:Parameters:
:Response:

Restore File
````````````

:Resource: /trashbin/empty
:Method: POST
:Description: Restore *File* from Trash
:Parameters:
    :path: *Path*
    :restore_revisiion: int
    :conflict: `rename|rewrite|strict` (usual rename)
:Response:

Sharing (16)
~~~~~~~~~~~~
* Public - 2+
* Share out - 2+
* Share in (invites) - 5+

Publish
```````

:Resource: /file/publish
:Method: POST
:Description: Publish entry
:Parameters:
    :path: *Path*
:Response: *Weblink*

Unpublish
`````````

:Resource: /file/unpublish
:Method: POST
:Description: Unpublish entry
:Parameters:
    :weblink: *Weblink*
:Response: *Weblink*

Share folder
````````````

:Resource: /folder/share
:Method: POST
:Description: Share folder
:Parameters:
    :home: *Path*
    :invite:
        :email: guest
        :access: `read_only`
:Response:

Unshare folder
``````````````

:Resource: /folder/unshare
:Method: POST
:Description: Unshare folder
:Parameters:
    :home: *Path*
    :invite: email
:Response:

Mount shared
````````````

:Resource: /folder/mount
:Method: POST
:Description: Mount foreign share
:Parameters:
    :invite_token: ...
    :conflict: `rename|rewrite|strict` (usual rename)
:Response:

Unmount shared
``````````````

:Resource: /folder/unmount
:Method: POST
:Description:
:Parameters:
    :home: *Path*
    :clone_copy: `true|false`
:Response:

---
``````````````

:Resource: /folder/shared
:Method: GET?
:Description: ???
:Parameters: ???
:Response:
    :403: user

---
``````````````

:Resource: /folder/shared/incoming
:Method: GET
:Description:
:Parameters:
:Response:

---
``````````````

:Resource: /folder/shared/info
:Method: GET
:Description:
:Parameters:
:Response:

---
``````````````

:Resource: /folder/shared/links
:Method: GET
:Description:
:Parameters:
    :home: *Path*
:Response:

---
``````````````

:Resource: /folder/invites
:Method: GET
:Description: List incoming invites
:Parameters:
:Response:

---
``````````````

:Resource: /folder/invites/info
:Method: GET
:Description: Get invite info
:Parameters:
    :invite_token: ...
:Response:

---
``````````````

:Resource: /folder/invites/reject
:Method: POST
:Description: Reject invite
:Parameters:
    :invite_token: ...
:Response:

Get Weblink info
````````````````

:Resource: /weblinks
:Method: GET
:Description: Get *Weblink* info
:Parameters:
    :weblink: *Weblink*
:Response:

Set share RO
````````````

:Resource: /weblinks/readonly
:Method: POST
:Description: Set published RO
:Parameters:
    :weblink: *Weblink*
:Response:

Set share RW
````````````

:Resource: /weblinks/writable
:Method: POST
:Description: Set published RW
:Parameters:
    :weblink: *Weblink*
:Response:

Misc (7)
~~~~~~~~

Get Token
`````````

:Resource: /tokens/csrf
:Method: POST
:Description:
:Parameters:
:Response:
    :token: %32w

Get anon? token
```````````````

:Resource: /tokens/download
:Method: POST
:Description:
:Parameters:
:Response:
    :token: %40x

Dispatcher
``````````

:Resource: /dispatcher
:Method: GET
:Description: List usual urls
:Parameters:
:Response:

User info
`````````

:Resource: /user
:Method: GET
:Description: Get all user's info
:Parameters:
:Response:


User edit
`````````

:Resource: /user/edit
:Method: POST
:Description: Update user UI settings
:Parameters:
:Response:

Used space
``````````

:Resource: /user/space
:Method: GET
:Description: Get used/available space
:Parameters:
:Response:

Zip
```

:Resource: /zip
:Method: GET
:Description: Get ziped entries
:Parameters:
:Response:
