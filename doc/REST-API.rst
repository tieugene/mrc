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


Terms
`````

:Path:
    Full entry path (e.g. `/dir1/dir2/file3.txt`)
:Name:
    Entry name (e.g. `file3.txt`)
:WebLink:
    %4w/%9w after https://cloud.mail.ru/public/ (e.g. `EDAS/ZegcnyJrJ`)
:Token:
    %32w (e.g. `...`) - 24-byte B64 ?
:Tree:
    %24d (e.g. `643031373030323930303030`) - 18-byte B64 ?
:Hash:
    %40X (e.g. `...`) - 20-byte
:Conflict:
    - rename - target stay `path (1)` if target path occupied
    - rewrite -
    - strict -

Entry info
``````````

:kind:
    `file`|`folder`
:type:
    `file`|`folder`|`shared`
:home:
    <Path>
:name:
    str
:tree:
    <Tree>
:[weblink]:
    <Weblink> - for published
:[weblink_access_rights]:
    `r`|`rw` - for published (files - r only)
:[message]:
    `` - for published

File info
`````````

:kind:
    `file`
:type:
    `file`
:mtime:
    int - unixtime
:size:
    int
:hash:
    *Hash*
:virus_scan:
    `pass`|`fail`|`in_progress`

Folder info (short)
```````````````````

:kind:
    `folder`
:type:
    - `folder` - simply folder
    - `shared` - my shared folder
    - `mounted` - foreign shared; cannot be shared; published inside rights (can't publish as rw for ro mounts)
:count:
    {'folders': 0, 'files': 0}
:rev:
    int
:grev:
    int
:[size]:
    int - in list[] only
:[rrev]:
    int - for mounted only
:[readonly]:
    `true`, for RO mounted only

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
    :status:
        ...
    :time:
        ...
    :body:
        ...
:Error Codes:
    :200:
        OK
    :400:
        Bad Request (e.g. required params absent)
    :401 ?:
        Unauthorized
    :403:
        Forbidden (not logged in)
    :404:
        Not Found (e.g. object really not exists)
    :406:
        Not Acceptable (e.g. /file/history for folder)

Entry (5)
~~~~~~~~~

+Info
````

:Resource: /file
:Method: GET
:Description: Get folder/file metainfo
:Parameters:
    :home: *Path*
:Response:
:Error Codes:
    :404: Entry not exists

Copy
````

:Resource: /file/copy
:Method: POST
:Description: Copy *Entry* into other folder
:Parameters:
    :home: *Path* - entry to copy
    :folder: *Path* - folder copy to
    :conflict: `rename|rewrite|strict`
:Response: new path
:Error Codes:
    :404: Src Entry not exists
    :...: dst folder not exists
    :...: dst is file
    :...: new name is path

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
:Error Codes:
    :404: Src Entry not exists
    :...: dst folder not exists
    :...: dst is file
    :...: new name is path

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
:Error Codes:
    :404: Src Entry not exists
    :...: dst exists
    :...: dst is file against src is folder

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
:Error Codes:
    :404: Src Entry not exists
    :...: dst exists

File
~~~~

File Upload
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

...Folder List
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

+Folder New
``````````

:Resource: /folder/add
:Method: POST
:Description: Create new folder
:Parameters:
    :home: *Path*
    :[conflict]: `rename|rewrite|strict`
:Response:
    :200: str - new folder path
    :400: json if *not* `rename` (e.g. {'home': {'error': 'exists', 'value': 'Path'}})

Trashbin
~~~~~~~~

Trashbin List
`````````````

:Resource: /trashbin
:Method: GET
:Description: List *Trashbin* content
:Parameters:
:Response:

Trashbin Empty
``````````````

:Resource: /trashbin/empty
:Method: POST
:Description: Empty Trashbin
:Parameters:
:Response:

File Restore
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
:Description: Unmount foreign share
:Parameters:
    :home: *Path*
    :clone_copy: `true|false`
:Response:

???
```

:Resource: /folder/shared
:Method: GET?
:Description: ???
:Parameters: ???
:Response:
    :403: user

List invites (?)
````````````````

:Resource: /folder/shared/incoming
:Method: GET
:Description: List incoming invites (?)
:Parameters:
:Response:

Published info (?)
``````````````````

:Resource: /folder/shared/info
:Method: GET
:Description: Get published entry info
:Parameters:
:Response:

List ...
````````

:Resource: /folder/shared/links
:Method: GET
:Description: List ...
:Parameters:
    :home: *Path*
:Response:

List invites
````````````

:Resource: /folder/invites
:Method: GET
:Description: List incoming invites
:Parameters:
:Response:

Invite info
```````````

:Resource: /folder/invites/info
:Method: GET
:Description: Get invite info
:Parameters:
    :invite_token: ...
:Response:

Reject invite
`````````````

:Resource: /folder/invites/reject
:Method: POST
:Description: Reject invite
:Parameters:
    :invite_token: ...
:Response:

Get share info
````````````````

:Resource: /weblinks
:Method: GET
:Description: Get share (?) info
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
