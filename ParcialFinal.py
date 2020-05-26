import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time
import os

adc_dataA1=0.0
adc_dataA2=0.0
board = Arduino ('COM3')
it = util.Iterator(board)
it.start()
time.sleep(1)
a_A1 = board.get_pin('a:1:i')
a_A2 = board.get_pin('a:2:i')

root = Tk()
root.title("Parcial Final Herramientas")
print(os.getcwd().replace('\\','/')+'/key.json')