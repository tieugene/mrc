#!/usr/bin/python3
# -*- coding: utf-8 -*-

############################################
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## made by Axel Schneider * https://github.com/Axel-Erfurt/
## August 2019
############################################
# 1. stdlib
import sys
import os
import errno
import getpass
import socket
import shutil
import subprocess
import stat
from zipfile import ZipFile
from enum import Enum
import time
# 2. PyQt
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QIcon, QPixmap, QKeySequence, QCursor, QDesktopServices
#from PySide2 import QKeySequence, QCursor, QDesktopServices

TREEVIEW = True

def dprint(s):
    print(s, file=sys.stderr)


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()

        self.setWindowTitle("Filemanager")
        self.setWindowIcon(QIcon.fromTheme("system- file-manager"))
        self.process = QProcess()
        self.clip = QApplication.clipboard()

        self.settings = QSettings("QFileManager", "QFileManager")
        self.isInEditMode = False
        self.cut = False
        self.hiddenEnabled = False
        self.folder_copied = ""
        self.copyPath = ""
        self.copyList = []
        self.copyListNew = ""
        path = QDir.rootPath()

        # GUI
        self.treeview = QTreeView()
        if TREEVIEW:
            self.listview = QTreeView()
        else:
            self.listview = QListView()
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.listview)
        self.splitter.setSizes([20, 160])
        hlay = QHBoxLayout()
        hlay.addWidget(self.splitter)
        wid = QWidget()
        wid.setLayout(hlay)
        self.createStatusBar()
        self.setCentralWidget(wid)
        self.setGeometry(0, 26, 900, 500)

        self.createActions()

        # main menu
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.actionFolderNew)
        fileMenu.addAction(self.actionFolderRename)
        fileMenu.addAction(self.actionFolderDel)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actionFileRename)
        fileMenu.addAction(self.actionFileDel)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actionExit)
        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction(self.actionFolderCopy)
        editMenu.addAction(self.actionFolderPaste)
        editMenu.addSeparator()
        editMenu.addAction(self.actionFileCut)
        editMenu.addAction(self.actionFileCopy)
        editMenu.addAction(self.actionFilePaste)
        viewMenu = menuBar.addMenu('&View')
        viewMenu.addAction(self.actionSwitchHide)
        viewMenu.addAction(self.actionRefresh)
        goMenu = menuBar.addMenu('&Navigate')
        goMenu.addAction(self.actionGoBack)
        goMenu.addAction(self.actionGoUp)
        goMenu.addAction(self.actionGoHome)
        goMenu.addAction(self.actionGoDocuments)
        goMenu.addAction(self.actionGoDownloads)
        goMenu.addAction(self.actionGoMusic)
        goMenu.addAction(self.actionGoVideo)
        menuHelp = menuBar.addMenu('&Help')
        menuHelp.addAction(self.actionHelp)

        # toolbar
        self.tBar = self.addToolBar("Tools")
        self.tBar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.tBar.setMovable(False)
        self.tBar.setIconSize(QSize(16, 16))
        self.tBar.addAction(self.actionFolderNew)
        self.tBar.addAction(self.actionFolderCopy)
        self.tBar.addAction(self.actionFolderPaste)
        self.tBar.addSeparator()
        self.tBar.addAction(self.actionFileCopy)
        self.tBar.addAction(self.actionFileCut)
        self.tBar.addAction(self.actionFilePaste)
        self.tBar.addAction(self.actionFileDel)
        self.tBar.addSeparator()
        self.tBar.addAction(self.actionGoHome)
        self.tBar.addAction(self.actionGoBack)
        self.tBar.addAction(self.actionGoUp)
        self.tBar.addAction(self.actionGoDocuments)
        self.tBar.addAction(self.actionGoDownloads)
        # /toolbar

        # tree panel
        # - model
        self.dirModel = QFileSystemModel()
        self.dirModel.setReadOnly(False)
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Drives)
        self.dirModel.setRootPath(QDir.rootPath())
        # - view
        self.treeview.setModel(self.dirModel)
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        self.treeview.setRootIsDecorated(True)
        self.treeview.setSortingEnabled(True)
        self.treeview.setRootIndex(self.dirModel.index(path))
        #        self.treeview.clicked.connect(self.on_clicked)
        self.treeview.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        #        self.treeview.expand(self.treeview.currentIndex())
        self.treeview.setTreePosition(0)
        self.treeview.setUniformRowHeights(True)
        self.treeview.setExpandsOnDoubleClick(True)
        self.treeview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeview.setIndentation(12)
        self.treeview.setDragDropMode(QAbstractItemView.DragDrop)
        self.treeview.setDragEnabled(True)
        self.treeview.setAcceptDrops(True)
        self.treeview.setDropIndicatorShown(True)
        self.treeview.sortByColumn(0, Qt.AscendingOrder)
        # files panel
        # - model
        self.fileModel = QFileSystemModel()
        self.fileModel.setReadOnly(False)
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.fileModel.setResolveSymlinks(True)
        # - view
        self.listview.setModel(self.fileModel)
        if TREEVIEW:
            self.listview.header().resizeSection(0, 320)
            self.listview.header().resizeSection(1, 80)
            self.listview.header().resizeSection(2, 80)
            self.listview.setSortingEnabled(True)
            self.listview.doubleClicked.connect(self.list_doubleClicked)
        else:   # QListView
            # alternatingRowColors=true, , showDropIndicator=false
            self.listview.setWrapping(True)
            self.listview.setResizeMode(QListView.Adjust)
            self.listview.setModelColumn(0)
            self.listview.activated.connect(self.list_doubleClicked)
        self.listview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listview.setDragDropMode(QAbstractItemView.DragDrop)
        self.listview.setDragEnabled(True)
        self.listview.setAcceptDrops(True)
        self.listview.setDropIndicatorShown(True)
        self.listview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.listview.setIndentation(10)
        #self.listview.sortByColumn(0, Qt.AscendingOrder)
        # setup panels
        docs = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))

        dprint("Welcome to QFileManager")
        self.readSettings()
        self.enableHidden()
        self.getRowCount()

    def closeEvent(self, e):
        dprint("writing settings ...\nGoodbye ...")
        self.writeSettings()

    ### utilities
    def readSettings(self):
        dprint("reading settings ...")
        if self.settings.contains("pos"):
            pos = self.settings.value("pos", QPoint(200, 200))
            self.move(pos)
        else:
            self.move(0, 26)
        if self.settings.contains("size"):
            size = self.settings.value("size", QSize(800, 600))
            self.resize(size)
        else:
            self.resize(800, 600)
        if self.settings.contains("hiddenEnabled"):
            if self.settings.value("hiddenEnabled") == "false":
                self.hiddenEnabled = True
            else:
                self.hiddenEnabled = False

    def writeSettings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("size", self.size())
        self.settings.setValue("hiddenEnabled", self.hiddenEnabled, )

    def getRowCount(self):
        count = 0
        index = self.treeview.selectionModel().currentIndex()
        path = QDir(self.dirModel.fileInfo(index).absoluteFilePath())
        count = len(path.entryList(QDir.Files))
        self.statusBar().showMessage("%s %s" % (count, "Files"), 0)
        return count

    ### actions
    def createActions(self):
        # icon, title, action
        self.actionExit = QAction(QIcon.fromTheme("quit"), "&Quit", triggered=qApp.quit)
        # go
        self.actionGoBack = QAction(QIcon.fromTheme("go-back"), "&Back", triggered=self.goBack)
        self.actionGoUp = QAction(QIcon.fromTheme("go-up"), "&Up", triggered=self.goUp)
        self.actionGoHome = QAction(QIcon.fromTheme("go-home"), "&Home", triggered=self.goHome)
        self.actionGoDocuments = QAction(QIcon.fromTheme("folder-documents"), "Documents", triggered=self.goDocuments)
        self.actionGoDownloads = QAction(QIcon.fromTheme("folder-downloads"), "Downloads", triggered=self.goDownloads)
        self.actionGoMusic = QAction(QIcon.fromTheme("folder-music"), "&Music", triggered=self.goMusic)
        self.actionGoVideo = QAction(QIcon.fromTheme("folder-video"), "&Video", triggered=self.goVideo)
        #
        # folder/file manipulations
        # - common
        # - folder
        self.actionFolderNew = QAction(QIcon.fromTheme("folder-new"), "Folder create", triggered=self.createNewFolder)
        self.actionFolderRename = QAction(QIcon.fromTheme("accessories-text-editor"), "Folder rename", triggered=self.renameFolder)
        self.actionFolderDel = QAction(QIcon.fromTheme("edit-delete"), "Folder delete", triggered=self.deleteFolder)
        self.actionFolderCopy = QAction(QIcon.fromTheme("edit-copy"), "Folder copy", triggered=self.copyFolder)
        self.actionFolderPaste = QAction(QIcon.fromTheme("edit-paste"), "Folder paste", triggered=self.pasteFolder)
        # - file
        self.actionFileRename = QAction(QIcon.fromTheme("accessories-text-editor"), "rename File", triggered=self.renameFile)
        self.actionFileDel = QAction(QIcon.fromTheme("edit-delete"), "delete File(s)", triggered=self.deleteFile)
        self.actionFileCut = QAction(QIcon.fromTheme("edit-cut"), "cut File(s)", triggered=self.cutFile)
        self.actionFileCopy = QAction(QIcon.fromTheme("edit-copy"), "copy File(s)", triggered=self.copyFile)
        self.actionFilePaste = QAction(QIcon.fromTheme("edit-paste"), "paste File(s) / Folder", triggered=self.pasteFile)
        # misc
        self.actionRefresh = QAction(QIcon.fromTheme("view-refresh"), "refresh View", triggered=self.refreshList, shortcut="F5")
        self.actionSwitchHide = QAction("show hidden Files", triggered=self.enableHidden)
        self.actionHelp = QAction(QIcon.fromTheme("help"), "About", triggered=self.showHelp)

        # shortcuts
        self.actionFileRename.setShortcut(QKeySequence(Qt.Key_F2))
        self.actionFileCopy.setShortcut(QKeySequence("Ctrl+c"))
        self.actionFileCut.setShortcut(QKeySequence("Ctrl+x"))
        self.actionFilePaste.setShortcut(QKeySequence("Ctrl+v"))
        self.actionFileDel.setShortcut(QKeySequence("Shift+Del"))
        self.actionSwitchHide.setShortcut(QKeySequence("Ctrl+h"))
        self.actionGoBack.setShortcut(QKeySequence(Qt.Key_Backspace))
        self.actionHelp.setShortcut(QKeySequence(Qt.Key_F1))
        self.actionFolderNew.setShortcut(QKeySequence("Shift+Ctrl+n"))

        # context visibility
        self.actionFileRename.setShortcutVisibleInContextMenu(True)
        self.actionFileCopy.setShortcutVisibleInContextMenu(True)
        self.actionFileCut.setShortcutVisibleInContextMenu(True)
        self.actionFilePaste.setShortcutVisibleInContextMenu(True)
        self.actionFileDel.setShortcutVisibleInContextMenu(True)
        self.actionRefresh.setShortcutVisibleInContextMenu(True)
        self.actionSwitchHide.setShortcutVisibleInContextMenu(True)
        self.actionSwitchHide.setCheckable(True)
        self.actionGoBack.setShortcutVisibleInContextMenu(True)
        self.actionHelp.setShortcutVisibleInContextMenu(True)
        self.actionFolderNew.setShortcutVisibleInContextMenu(True)

        # tree context
        self.treeview.addAction(self.actionFolderNew)
        self.treeview.addAction(self.actionFolderRename)
        self.treeview.addAction(self.actionFolderCopy)
        self.treeview.addAction(self.actionFolderPaste)
        self.treeview.addAction(self.actionFolderDel)
        self.treeview.addAction(self.actionFileRename)

        # files context
        self.listview.addAction(self.actionFileRename)
        self.listview.addAction(self.actionFileCopy)
        self.listview.addAction(self.actionFileCut)
        self.listview.addAction(self.actionFilePaste)
        self.listview.addAction(self.actionFileDel)
        self.listview.addAction(self.actionRefresh)
        self.listview.addAction(self.actionSwitchHide)
        #        self.listview.addAction(self.pasteFolderAction)

    def enableHidden(self):
        if self.hiddenEnabled == False:
            self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Hidden | QDir.AllDirs | QDir.Files)
            self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.Hidden | QDir.AllDirs)
            self.hiddenEnabled = True
            self.actionSwitchHide.setChecked(True)
            dprint("set hidden files to true")
        else:
            self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
            self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
            self.hiddenEnabled = False
            self.actionSwitchHide.setChecked(False)
            dprint("set hidden files to false")

    def refreshList(self):
        dprint("refreshing view")
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        self.treeview.setCurrentIndex(self.fileModel.index(path))
        self.treeview.setFocus()

    def showHelp(self):
        QMessageBox.about(self, "About", "This is about")

    def on_clicked(self, index):
        if self.treeview.selectionModel().hasSelection():
            index = self.treeview.selectionModel().currentIndex()
            if not (self.treeview.isExpanded(index)):
                self.treeview.setExpanded(index, True)
            else:
                self.treeview.setExpanded(index, False)

    def getFolderSize(self, path):
        size = sum(os.path.getsize(f) for f in os.listdir(folder) if os.path.isfile(f))
        return size

    def on_selectionChanged(self):
        self.treeview.selectionModel().clearSelection()
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))
        self.currentPath = path
        self.setWindowTitle(path)
        self.getRowCount()

    def list_doubleClicked(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        #        folderpath = self.fileModel.fileInfo(index).path()
        if not self.fileModel.fileInfo(index).isDir():
            if self.checkIsApplication(path) == True:
                self.process.startDetached(path)
            else:
                QDesktopServices.openUrl(QUrl(path, QUrl.TolerantMode | QUrl.EncodeUnicode))
        else:
            self.treeview.setCurrentIndex(self.dirModel.index(path))
            self.treeview.setFocus()
            #            self.listview.setRootIndex(self.fileModel.setRootPath(path))
            self.setWindowTitle(path)

    def goBack(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).path()
        self.treeview.setCurrentIndex(self.dirModel.index(path))

    def goUp(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).path()
        dprint(path)
        self.treeview.setCurrentIndex(self.dirModel.index(path))

    def goHome(self):
        docs = QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goMusic(self):
        docs = QStandardPaths.standardLocations(QStandardPaths.MusicLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goVideo(self):
        docs = QStandardPaths.standardLocations(QStandardPaths.MoviesLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goDocuments(self):
        docs = QStandardPaths.standardLocations(QStandardPaths.DocumentsLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def goDownloads(self):
        docs = QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)[0]
        self.treeview.setCurrentIndex(self.dirModel.index(docs))
        self.treeview.setFocus()

    def infobox(self, message):
        title = "QFilemanager"
        QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                    Qt.Dialog | Qt.NoDropShadowWindowHint).show()

    def contextMenuEvent(self, event):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        self.menu = QMenu(self.listview)
        if self.listview.hasFocus():
            self.menu.addAction(self.actionFolderNew)
            self.menu.addSeparator()
            self.menu.addAction(self.actionFileRename)
            self.menu.addSeparator()
            self.menu.addAction(self.actionFileCopy)
            self.menu.addAction(self.actionFileCut)
            self.menu.addAction(self.actionFilePaste)
            #            self.menu.addAction(self.pasteFolderAction)
            self.menu.addSeparator()
            self.menu.addAction(self.actionFileDel)
            self.menu.addSeparator()
            self.menu.addAction(self.actionRefresh)
            self.menu.addAction(self.actionSwitchHide)
            self.menu.addSeparator()
            self.menu.addAction(self.actionHelp)
            self.menu.popup(QCursor.pos())
        else:
            index = self.treeview.selectionModel().currentIndex()
            path = self.dirModel.fileInfo(index).absoluteFilePath()
            dprint("current path is: %s" % path)
            self.menu = QMenu(self.treeview)
            if os.path.isdir(path):
                self.menu.addAction(self.actionFolderNew)
                self.menu.addAction(self.actionFolderRename)
                self.menu.addAction(self.actionFolderCopy)
                self.menu.addAction(self.actionFolderPaste)
                self.menu.addAction(self.actionFolderDel)
            self.menu.popup(QCursor.pos())

    def createNewFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        dlg = QInputDialog(self)
        foldername, ok = dlg.getText(self, 'Folder Name', "Folder Name:", QLineEdit.Normal, "", Qt.Dialog)
        if ok:
            success = QDir(path).mkdir(foldername)

    def renameFile(self):
        if self.listview.hasFocus():
            if self.listview.selectionModel().hasSelection():
                index = self.listview.selectionModel().currentIndex()
                path = self.fileModel.fileInfo(index).absoluteFilePath()
                basepath = self.fileModel.fileInfo(index).path()
                dprint(basepath)
                oldName = self.fileModel.fileInfo(index).fileName()
                dlg = QInputDialog()
                newName, ok = dlg.getText(self, 'new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
                if ok:
                    newpath = basepath + "/" + newName
                    QFile.rename(path, newpath)
        elif self.treeview.hasFocus():
            self.renameFolder()

    def renameFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        basepath = self.dirModel.fileInfo(index).path()
        dprint("pasepath: %s" % basepath)
        oldName = self.dirModel.fileInfo(index).fileName()
        dlg = QInputDialog()
        newName, ok = dlg.getText(self, 'new Name:', path, QLineEdit.Normal, oldName, Qt.Dialog)
        if ok:
            newpath = basepath + "/" + newName
            dprint(newpath)
            nd = QDir(path)
            check = nd.rename(path, newpath)

    def copyFile(self):
        self.copyList = []
        selected = self.listview.selectionModel().selectedRows()
        count = len(selected)
        for index in selected:
            path = self.currentPath + "/" + self.fileModel.data(index, self.fileModel.FileNameRole)
            dprint(path + " copied to clipboard")
            self.copyList.append(path)
            self.clip.setText('\n'.join(self.copyList))
        dprint("%s\n%s" % ("filepath(s) copied:", '\n'.join(self.copyList)))

    def copyFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        folderpath = self.dirModel.fileInfo(index).absoluteFilePath()
        dprint("%s\n%s" % ("folderpath copied:", folderpath))
        self.folder_copied = folderpath
        self.copyList = []

    def pasteFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        target = self.folder_copied
        destination = self.dirModel.fileInfo(index).absoluteFilePath() + "/" + QFileInfo(self.folder_copied).fileName()
        dprint("%s %s %s" % (target, "will be pasted to", destination))
        try:
            shutil.copytree(target, destination)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(target, destination)
            else:
                self.infobox('Error', 'Directory not copied. Error: %s' % e)

    def pasteFile(self):
        if len(self.copyList) > 0:
            index = self.treeview.selectionModel().currentIndex()
            file_index = self.listview.selectionModel().currentIndex()
            for target in self.copyList:
                dprint(target)
                destination = self.dirModel.fileInfo(index).absoluteFilePath() + "/" + QFileInfo(target).fileName()
                dprint("%s %s" % ("pasted File to", destination))
                QFile.copy(target, destination)
                if self.cut == True:
                    QFile.remove(target)
                self.cut == False
        else:
            index = self.treeview.selectionModel().currentIndex()
            target = self.folder_copied
            destination = self.dirModel.fileInfo(index).absoluteFilePath() + "/" + QFileInfo(
                self.folder_copied).fileName()
            try:
                shutil.copytree(target, destination)
            except OSError as e:
                # If the error was caused because the source wasn't a directory
                if e.errno == errno.ENOTDIR:
                    shutil.copy(target, destination)
                else:
                    dprint('Directory not copied. Error: %s' % e)

    def cutFile(self):
        self.cut = True
        self.copyFile()

    def deleteFolder(self):
        index = self.treeview.selectionModel().currentIndex()
        delFolder = self.dirModel.fileInfo(index).absoluteFilePath()
        msg = QMessageBox.question(self, "Info", "Caution!\nReally delete this Folder?\n" + delFolder,
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            dprint('Deletion confirmed.')
            self.statusBar().showMessage("%s %s" % ("folder deleted", delFolder), 0)
            self.fileModel.remove(index)
            dprint("%s %s" % ("folder deleted", delFolder))
        else:
            dprint('No clicked.')

    def deleteFile(self):
        self.copyFile()
        msg = QMessageBox.question(self, "Info", "Caution!\nReally delete this Files?\n" + '\n'.join(self.copyList),
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            dprint('Deletion confirmed.')
            index = self.listview.selectionModel().currentIndex()
            self.copyPath = self.fileModel.fileInfo(index).absoluteFilePath()
            dprint("%s %s" % ("file deleted", self.copyPath))
            self.statusBar().showMessage("%s %s" % ("file deleted", self.copyPath), 0)
            for delFile in self.listview.selectionModel().selectedIndexes():
                self.fileModel.remove(delFile)
        else:
            dprint('No clicked.')

    def createStatusBar(self):
        sysinfo = QSysInfo()
        myMachine = "current CPU Architecture: " + sysinfo.currentCpuArchitecture() + " *** " + sysinfo.prettyProductName() + " *** " + sysinfo.kernelType() + " " + sysinfo.kernelVersion()
        self.statusBar().showMessage(myMachine, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        dprint(path)
        w.listview.setRootIndex(w.fileModel.setRootPath(path))
        w.treeview.setRootIndex(w.dirModel.setRootPath(path))
        w.setWindowTitle(path)
    sys.exit(app.exec_())
