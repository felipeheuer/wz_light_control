from json import encoder
import os
import time
import json
from time import sleep

import win32file
import win32event
import win32con

def checkIfExists(filePath):
    return os.path.exists(filePath) and os.path.isfile(filePath)


class wzHighlightsMonitor:
    def __init__(self, path, file) -> None:
        self.debug = False
        self.lastEvent = ''
        self.jsonData = None
        self.file = file
        self.folder = path
        self.filePath = path + file
        self.fileType = ''
        self.__dbgPrint (self.filePath)
        self.status = checkIfExists(self.filePath)
        if self.status:
            self.__dbgPrint("File exists!")
            self.changeHandle = win32file.FindFirstChangeNotification (self.folder,
            0,
            win32con.FILE_NOTIFY_CHANGE_SIZE|
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME|
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME|
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES|
            win32con.FILE_NOTIFY_CHANGE_SIZE|
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE|
            win32con.FILE_NOTIFY_CHANGE_SECURITY)
            self.lastModDate = os.stat(self.filePath)[8]
            self.__dbgPrint ("Initial file datime is " + time.ctime(self.lastModDate))
            self.__getFileContents()
        else:
            self.__dbgPrint("Could not find Highlights file")


    def __dbgPrint(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)


    def __monitorFile(self):
        if not self.status:
            return None

        try:
            while 1:
                result = win32event.WaitForSingleObject (self.changeHandle, 500)
                if result == win32con.WAIT_OBJECT_0:
                    moddate = os.stat(self.filePath)[8] # there are 10 attributes this call returns and you want the next to last
                    if moddate > self.lastModDate:
                        self.__dbgPrint ("File Updated at " + time.ctime(moddate))
                        self.lastEvent = self.__getLastEvent()
                        if self.lastEvent is not None:
                            print(self.lastEvent)
                        self.lastModDate = moddate
                    else:
                        self.__dbgPrint ("No timestamp change on file")
                    win32file.FindNextChangeNotification (self.changeHandle)
        except:
            self.__dbgPrint ("Drop", result)
        finally:
            self.__dbgPrint ("Exit", result)
            win32file.FindCloseChangeNotification (self.changeHandle)


    def __readFile(self, encoding='utf-8'):
        with open(self.filePath, encoding=encoding) as file:
            strData = file.read().encode('utf-8')
            file.close()
        return strData


    def __getFileContents(self):
        if self.fileType == '':
            try:
                self.jsonData = json.loads(self.__readFile())
                self.fileType = 'utf-8'
            except:
                try:
                    self.jsonData = json.loads(self.__readFile(encoding='utf-16-le'))
                    self.fileType = 'utf-16-le'
                except:
                    self.__dbgPrint("Could not open NVidia Highlights File. Exiting...")
                    exit(-1)
            self.__dbgPrint("File type is ", self.fileType)
        else:
            self.jsonData = json.loads(self.__readFile(encoding=self.fileType))


    def __getLastEventId(self):
        try:
            self.__getFileContents()
            return self.jsonData['info']['lastHighlightIdUsed']
        except:
            return None


    def __getLastEvent(self):
        retries = 100

        while retries:
            retries -= 1
            lastHighlight = self.__getLastEventId()
            if lastHighlight is None:
                continue
            self.__dbgPrint("Last Highlight: ", lastHighlight)

            try:
                for highlight in self.jsonData['highlights']:
                    if highlight['id'] == lastHighlight:
                        self.__dbgPrint("Retries:", retries)
                        return highlight['highlightDefinitionId']
            except:
                None
            finally:
                None
            sleep(0.1)

        return None

    def run(self):
        try:
            self.__monitorFile()
        except:
            self.__dbgPrint("Quit")
