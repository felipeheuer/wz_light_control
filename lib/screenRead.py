import numpy as nm
import pytesseract
from time import sleep
import paho.mqtt.client as mqtt
# importing OpenCV
import cv2
import re

from PIL import ImageGrab

eventsToWatch=["Warzone Death","Warzone Double Kill","Warzone Down","Warzone Elimination","Warzone Revenge","Warzone Triple Kill","Warzone Win"]

broker = '192.168.0.200'
state_topic = 'wz/commands/action'
delay = 2.5
client = mqtt.Client("ha-client")
client.connect(broker, port=1893)
client.loop_start()


# area = (70, 950, 900, 1500)
# area_left  = (100, 775, 460, 1600)
# area_right = (460, 775, 830, 1600)
# area_left  = (70, 950, 900, 1250)
# area_right = (70, 1250, 900, 1550)


area_top = (3650, 0, 3850, 250)

def publish():
        client.publish(state_topic, 'Warzone Death')
        sleep(0.2)
        client.publish(state_topic, 'Alive')


def imToString():
    # Path of tesseract executable
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    while(True):
        # ImageGrab-To capture the screen image in a loop.
        # Bbox used to capture a specific area.
        cap_left  = ImageGrab.grab(bbox = area_left)
        cap_right = ImageGrab.grab(bbox = area_right)

        # Converted the image to monochrome for it to be easily
        # read by the OCR and obtained the output String.
        tesstr = pytesseract.image_to_string(
                cv2.cvtColor(nm.array(cap_left), cv2.COLOR_BGR2GRAY),
                lang ='eng')
        if 'DrHouse' in tesstr:
                print("Dr. House Killed someone, maybe")
                publish()
        else:
                tesstr = pytesseract.image_to_string(
                        cv2.cvtColor(nm.array(cap_right), cv2.COLOR_BGR2GRAY),
                        lang ='eng')
                if 'DrHouse' in tesstr:
                        print("Dr. House was shot")
                        publish()
        sleep(2)


def test():
    kills = 0
    temp_kills = 0
    pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    cap_top = ImageGrab.grab(bbox = area_top)
    file = open('bla.jpg', 'w+')
    cap_top.save(file)
    tesstr = pytesseract.image_to_string(
                cv2.cvtColor(nm.array(cap_top), cv2.COLOR_BGR2BGRA),
                lang ='eng')
    print(tesstr)
#     print("-----")
#     print(re.findall(r'\d+', tesstr))
#     print("=====")
#     [int(temp_kills) for temp_kills in tesstr.split() if temp_kills.isdigit()]
#     print("+++++")
#     print(temp_kills)



# Calling the function
test()