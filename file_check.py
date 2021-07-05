import os
import time

import win32file
import win32event
import win32con

# cod_nvidia_highlights_path="./"
# cod_nvidia_highlights_file="test.txt"
# file_path=cod_nvidia_highlights_path + cod_nvidia_highlights_file

def checkIfExists(filePath):
  return os.path.exists(filePath) and os.path.isfile(filePath)

class wzHighlightsMonitor:
  def __init__(self, path, file) -> None:
      self.file = file
      self.folder = path
      self.filePath = path + file
      print (self.filePath)
      self.status = checkIfExists(self.filePath)
      if self.status:
        print("File exists!")
        self.changeHandle = win32file.FindFirstChangeNotification (self.folder, 
        0,
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)
        self.lastModDate = os.stat(self.filePath)[8]
        print ("Initial file datime is " + time.ctime(self.lastModDate))

  def status(self):
      return self.status

  def monitorFile(self):
    try:
      while 1:
        result = win32event.WaitForSingleObject (self.changeHandle, 500)

        if result == win32con.WAIT_OBJECT_0:
          moddate = os.stat(self.filePath)[8] # there are 10 attributes this call returns and you want the next to last
          if moddate > self.lastModDate: print ("File Updated at " + time.ctime(moddate))
          self.lastModDate = moddate
          win32file.FindNextChangeNotification (self.changeHandle)
    finally:
      win32file.FindCloseChangeNotification (self.changeHandle)

  def run(self):
    try:
      self.monitorFile()
    except:
      print("Quit")

wz_mon = wzHighlightsMonitor("./", "test.txt")
wz_mon.run()
