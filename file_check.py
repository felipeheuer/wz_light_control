import os
import time

import win32file
import win32event
import win32con

cod_nvidia_highlights_path="./"
cod_nvidia_highlights_file="test.txt"
file_path=cod_nvidia_highlights_path + cod_nvidia_highlights_file

def checkIfExists(filePath):
  return os.path.exists(filePath) and os.path.isfile(filePath)

def monitorFile(filePath):
  try:
    moddate = os.stat(filePath)[8] # there are 10 attributes this call returns and you want the next to last
    changeHandle = win32file.FindFirstChangeNotification ( \
    cod_nvidia_highlights_path, 0, win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_SIZE)
    while 1:
      result = win32event.WaitForSingleObject (changeHandle, 500)

      if result == win32con.WAIT_OBJECT_0:
        new_moddate = os.stat(file_path)[8] # there are 10 attributes this call returns and you want the next to last
        if new_moddate > moddate: print ("File Updated at " + time.ctime(new_moddate))
        new_moddate = moddate
        win32file.FindNextChangeNotification (changeHandle)
  finally:
    win32file.FindCloseChangeNotification (changeHandle)

def run(filePath):
  if not checkIfExists(filePath): return False

  # changeHandle = win32file.FindFirstChangeNotification ( \
  #   cod_nvidia_highlights_path, 0, win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_SIZE)

  try:
    monitorFile(filePath)
  except:
    print("Quit")


# def mixed_solution():
#   if not os.path.exists(file_path):
#     return False

#   if not os.path.isfile(file_path):
#     return False

#   #
#   # FindFirstChangeNotification sets up a handle for watching
#   #  file changes. The first parameter is the path to be
#   #  watched; the second is a boolean indicating whether the
#   #  directories underneath the one specified are to be watched;
#   #  the third is a list of flags as to what kind of changes to
#   #  watch for. We're just looking at file additions / deletions.
#   #
#   change_handle = win32file.FindFirstChangeNotification (
#     cod_nvidia_highlights_path,
#     0,
#     win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
#     win32con.FILE_NOTIFY_CHANGE_SIZE
#   )

#   #
#   # Loop forever, listing any file changes. The WaitFor... will
#   #  time out every half a second allowing for keyboard interrupts
#   #  to terminate the loop.
#   #
#   try:
#     moddate = os.stat(file_path)[8] # there are 10 attributes this call returns and you want the next to last
   
#     while 1:
#       result = win32event.WaitForSingleObject (change_handle, 500)

#       #
#       # If the WaitFor... returned because of a notification (as
#       #  opposed to timing out or some error) then look for the
#       #  changes in the directory contents.
#       #
#       if result == win32con.WAIT_OBJECT_0:
#         new_moddate = os.stat(file_path)[8] # there are 10 attributes this call returns and you want the next to last
#         if new_moddate > moddate: print ("File Updated at " + time.ctime(new_moddate))
#         new_moddate = moddate
#         win32file.FindNextChangeNotification (change_handle)
#   finally:
#     win32file.FindCloseChangeNotification (change_handle)


run(file_path)
# mixed_solution()