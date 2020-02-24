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

Common
~~~~~~

:Resource: https://cloud.mail.ru/api/v2/
:Parameters:
    :token:
        *Token*
    :[api]:
        2
:Response: *Response*
:Error Codes:
    :200:
        OK
    :400:
        Bad Request (e.g. required params absent)
    :401?:
        Unauthorized
    :403:
        Forbidden (not logged in)
    :404:
        Not Found (e.g. entry really not exists)
    :406:
        Not Acceptable (e.g. /file/history for folder)
    :507:
        Writing into R/O mounted foreign share

+Entry (5)
~~~~~~~~~~

+Info
`````

:Resource: /file
:Method: GET
:Description: Get folder/file metainfo
:Parameters:
    :home: *Path*
:Response:
:Error Codes:
    :404: Entry not exists

+Copy
`````

Creates parents if not exist

:Resource: /file/copy
:Method: POST
:Description: Copy *Entry* into folder
:Parameters:
    :home: *Path* - entry to copy
    :folder: *Path* - folder copy to
    :[conflict]: *Conflict*
:Response: new path
:Error Codes:
    :400: target exists (w/o conflict=rename); dst is not folder
    :404: src not exists
    :507: dst is r/o mounted

+Move
`````

:Resource: /file/move
:Method: POST
:Description: Move *Entry* into folder
:Parameters:
    :home: *Path* - Entry to move
    :folder: *Path* - Folder move to
    :conflict: `rename|rewrite|strict`
:Response: new path
:Error Codes:
    :400: target exists (w/o conflict=rename); dst is not folder
    :404: src not exists
    :507: dst is r/o mounted

+Rename
```````

:Resource: /file/rename
:Method: POST
:Description: Rename *Entry* inplace
:Parameters:
    :home: *Path* - Entry to rename
    :name: *Name* - new name
    :[conflict]: `rename|rewrite|strict`
:Response: new path
:Error Codes:
    :400: name is occupied (w/o rename); name is path
    :404: Src not exists
    :507?: src folder is r/o mounted

+Remove
```````

:Resource: /file/remove
:Method: POST
:Description: Remove Entry into *Trashbin*
:Parameters:
    :home: *Path* - entry to remove
    :[hash]: anything
:Response:
    *Path* - removed entry
:Error Codes:
    :200: Everywhere
    :507?:

File (2)
~~~~~~~~

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

Folder (3)
~~~~~~~~~~

+Folder List
````````````

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
:Response:
    <Folder> + list[]

Folder Tree
```````````

:Resource: /folder/tree
:Method: GET
:Description: List folders from /
:Parameters:
    :home: *Path*
:Response:
    list of 'List Folder's

+Folder New
```````````

Create parents if not exist

:Resource: /folder/add
:Method: POST
:Description: Create new folder
:Parameters:
    :home: *Path*
    :[conflict]: `rename|rewrite|strict`
:Response:
:Error Codes:
    :200: str - new folder path
    :400: json if *not* `rename` (e.g. {'home': {'error': 'exists', 'value': 'Path'}})

+Trashbin (3)
~~~~~~~~~~~~~

+Trashbin List
```````````````

:Resource: /trashbin
:Method: GET
:Description: List *Trashbin* content
:Parameters:
    *None*
:Response:
    *TrashList*

+Trashbin Empty
```````````````

:Resource: /trashbin/empty
:Method: POST
:Description: Empty Trashbin
:Parameters: None
:Response: {}

+Restore
````````
Target folder must exist.
- Mount become simple folder
- Share become simple folder
- published stay published

:Resource: /trashbin/restore
:Method: POST
:Description: Restore *Entry* from Trash
:Parameters:
    :path: *Path* - target path restore to (or *Name* if to /}
    :restore_revision: int - unique id of trash entry
    :[conflict]: *Conflict*
:Response:
    :rev:
        - *Tree* - ?
        - int - new rev of tree restored to (?)
    :[name]:
        Restored *Name* when set conflict=rename
:Error Codes:
    :400:
        - target path is occupied (w/o conflict=rename)
        - restore_revision not exists in trash
    :507: target folder is mounted r/o

+Public (5)
~~~~~~~~~~~

+Publish
````````

Return same weblink on each publishing.

:Resource: /file/publish
:Method: POST
:Description: Make public
:Parameters:
    :path: *Path* - entry to publish
:Response: *Weblink* (e.g. '3Na6/w7WhtLcTs')
:Error Codes:
    :404: entry not exists

+Unpublish
``````````

Returns OK on any .+/.+

:Resource: /file/unpublish
:Method: POST
:Description: Remove public
:Parameters:
    :weblink: *Weblink* - to unpublish
:Response: *Weblink* - same as input parameters
:Error Codes: None

+Public info
````````````

:Resource: /weblinks
:Method: GET
:Description: Get public info
:Parameters:
    :weblink: *Weblink*
:Response:
    :long: %12w<path> (e.g. 4CwiqLNTUjPS/2/) - seems 9-bytes B64 + path
    :short: *Weblink* as is
:Error Codes:
    :404: weblink not exists

+Set public RO
``````````````

Not produces error on repeated action.

:Resource: /weblinks/readonly
:Method: POST
:Description: Set published RO
:Parameters:
    :weblink: *Weblink*
:Response: *Weblink* as is
:Error Codes:
    :404: weblink not exists

+Set public RW
``````````````

Not produces error on repeated action.
Works for file (!).

:Resource: /weblinks/writable
:Method: POST
:Description: Set published RW
:Parameters:
    :weblink: *Weblink*
:Response: *Weblink* as is
:Error Codes: weblink is ro mounted
    :404: weblink not exists

Share (8)
~~~~~~~~~

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
    :conflict: *Conflict* (usual rename)
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

List invites (?)
````````````````

:Resource: /folder/shared/incoming
:Method: GET
:Description: List incoming invites (?)
:Parameters:
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

Unsorted (3)
~~~~~~~~~~~~

???
```

:Resource: /folder/shared
:Method: GET?
:Description: ???
:Parameters: ???
:Response:
    :403: user

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

Misc (7)
~~~~~~~~

Get ? Token
```````````

:Resource: /tokens
:Method: POST
:Description:
:Parameters:
:Response:
    :token: %40d

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

+Used space
```````````

:Resource: /user/space
:Method: GET
:Description: Get used/available space
:Parameters: None
:Response:
    :bytes_used: int
    :bytes_total: int

Zip
```

:Resource: /zip
:Method: GET
:Description: Get zipped entries
:Parameters:
:Response:
