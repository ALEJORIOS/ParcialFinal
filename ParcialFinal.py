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

def onReturnKey(event):
    ADC_A1label['text'] = "hola"

def getData():
    global adc_dataA1, adc_dataA2
    adc_dataA1 = a_A1.read()
    ADC_A1['text'] = str(adc_dataA1)
    adc_dataA2 = a_A2.read()
    ADC_A2['text'] = str(adc_dataA2)
    root.after(250, getData)

root = Tk()
root.title("Parcial Final Herramientas")
root.geometry ("500x200")
print(os.getcwd().replace('\\','/')+'Parcial Final/key.json')
cred = credentials.Certificate(os.getcwd().replace('\\','/')+'/Parcial Final/key.json') # cambiar

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parcialfinal-b8888.firebaseio.com/'
})

ADC_A1label = Label(root, text = "ADC A1")
ADC_A1label.place(x=10,y=40)
ADC_A1 = Label(root, text = "0")
ADC_A1.place(x=10,y=10)
ADC_A2label = Label(root, text = "ADC A2")
ADC_A2label.place(x=70,y=40)
ADC_A2 = Label(root, text = "0")
ADC_A2.place(x=70,y=10)
entry = Entry(root)
entry.place(x = 10, y = 60)
entry.bind('<Return>',onReturnKey)

#Logus
b=Label(root,text="")
img = Image.open("C:/Users/luisr/Desktop/Herramientas/logousa.png")
img = img.resize((80,50))
photoImg=  ImageTk.PhotoImage(img)
b.configure(image=photoImg)
b.place(x = 400,y = 20)
#end logus
getData()
root.mainloop()