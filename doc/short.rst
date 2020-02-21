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
