import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time
import os
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

adc_dataA1=0.0
adc_dataA2=0.0
indicador = 0
valuesA1 = [0]
valuesA2 = [0]
board = Arduino ('COM3')
it = util.Iterator(board)
it.start()
time.sleep(1)
a_A1 = board.get_pin('a:1:i')
a_A2 = board.get_pin('a:2:i')
led1 = board.get_pin('d:9:p')
led2 = board.get_pin('d:10:p')

def onReturnKey(event):
    global adc_dataA1, adc_dataA2, indicador
    if(v.get() == "i"):
        indicador = 1
    if(v.get() == "p"):
        indicador = 2
    if(v.get() == "g"):
        indicador = 3
    if(v.get() == "d"):
       indicador = 4
def getData():
    global adc_dataA1, adc_dataA2, indicador
    ref = db.reference("ADC")
    adc_dataA1 = a_A1.read()
    ADC_A1['text'] = str(adc_dataA1)
    adc_dataA2 = a_A2.read()
    ADC_A2['text'] = str(adc_dataA2)
    valuesA1.append(adc_dataA1)
    valuesA2.append(adc_dataA2)
    if (len(valuesA1) == 11):
        del valuesA1[0]
    if (len(valuesA1) == 11):
        del valuesA2[0]

    if(indicador == 1):
        led1.write(adc_dataA1)
        led2.write(adc_dataA2)
    if(indicador == 2):
        print("Datos A1: "+str(valuesA1))
        print("promedio: "+str(sum(valuesA1)/10))
        print("Datos A2: "+str(valuesA1))
        print("promedio: "+str(sum(valuesA1)/10))
        indicador = 0
    if(indicador == 3):
        ref.update({
                'ADC A1': {
                     'valor': adc_dataA1,
                },
                 'ADC A2': {
                     'valor': adc_dataA2,
                }
         })
        print("Publicando datos")
    if(indicador == 4):
        graphic()
    root.after(250, getData)

def graphic():
    fig = Figure(figsize=(5, 2), dpi= 100, facecolor= "white")
    fig.add_subplot(111).plot(np.arange(1,len(valuesA1)+1,1), valuesA1, color = "white", linewidth = 1)
    canvas = FigureCanvasTkAgg(fig, master=graphicFrame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side = TOP, fill= BOTH, expand=1)
    

root = Tk()
root.title("Parcial Final Herramientas")
root.geometry ("500x300")
print(os.getcwd().replace('\\','/')+'/Parcial Final/key.json')
cred = credentials.Certificate(os.getcwd().replace('\\','/')+'/Parcial Final/key.json')

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
v = StringVar()
entry = Entry(root, textvariable = v)
entry.place(x = 10, y = 60)
entry.bind('<Return>',onReturnKey)
#Graphic
graphicFrame = Frame(root, width = 500, height = 200, bg = "white")
graphicFrame.place(y = 100)
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