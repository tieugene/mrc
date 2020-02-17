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

Common
~~~~~~

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

Entry
~~~~~

Info
````

:Resource: /file
:Method: GET
:Description: Get folder/file metainfo
:Parameters:
    :home: Path.
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Copy
````

:Resource: /file/copy
:Method: POST
:Description: Copy folder/file into other folder
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Move
````

:Resource: /file/move
:Method: POST
:Description: Move folder/file into other folder
:Parameters:
    :home: Path.
    :folder: Path of folder move to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Rename
``````

:Resource: /file/rename
:Method: POST
:Description: Rename folder/file inplace (?)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Delete
``````

:Resource: /file/remove
:Method: POST
:Description: Delete folder/file (into Trashbin)
:Parameters:
    :home: Path.
    :folder: Path of folder copy to
    :conflict: rename/.../... Usual rename
:Response:
:Error Codes:
        :401: If the user is not authorized to list bookmarks

Files
~~~~~

Upload
``````

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

History
```````

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

Folders
~~~~~~~

List
````

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

Tree
````

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

Create
``````

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

Trashbin
~~~~~~~~

List
````

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

Clear
`````

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
