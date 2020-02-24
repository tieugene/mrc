Response
````````
:email:
    email - auth login
:time:
    int - unixtime
:status:
    int - HTTP response code
:body:
    json - Payload

Entry info
``````````

:kind:
    enum [file, folder]
:type:
    enum [file, folder, shared, mounted]
:home:
    Path
:name:
    str
:tree:
    Tree
:[weblink]:
    Weblink - for published
:[weblink_access_rights]:
    enum [r, rw] - for published (files - r only)
:[message]:
    str('') - for published

File info
`````````

:kind:
    'file'
:type:
    'file'
:mtime:
    unixtime
:size:
    int
:hash:
    *Hash*
:virus_scan:
    enum [pass, fail, not_yet]

Folder info (short)
```````````````````

:kind:
    'folder'
:type: enum -
    - 'folder' - simply folder
    - 'shared' - my shared folder
    - 'mounted' - foreign shared; cannot be shared; published inside rights (can't publish as rw for ro mounts)
:count:
    {'folders': 0, 'files': 0}
:rev:
    int
:grev:
    int
:[rrev]:
    int - for mounted only
:[readonly]:
    'True', for RO mounted only
:[size]:
    int - in /folder request only
:[list]:
    [] - for /folder request only

Folder list
```````````

Trasbin
```````
Returned by /trashbin requiest

:kind:
    'folder'
:type:
    'folder'
:name:
    '/'
:next_chunk_rev:
    int = 0 ?
:list:
    [] of trashentries

TrashEntry
``````````

:deleted_at:
    *unixtime*
:deleted_by:
    2449502477
:deleted_from:
    *Path* - folder where removed from
:name:
    *Name* - folder/file name
:size:
    int - folder/file size
:rev:
    int - ?
:kind:
    enum [folder, file]
:type:
    enum [folder, file]

TrashFolder
```````````

:kind:
    'folder'
:type:
    'folder'
:count:
    :files:
        int
    :folders:
        int

TrashFile
`````````

:kind:
    'file'
:type:
    'file'
:hash:
    *Hash*
