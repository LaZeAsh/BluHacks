from tkinter import filedialog
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
import cv2
import time
import random


analysing = False 
totalAccuracy = 100
totalTime = 1





def LiveAnalyse():
    if analysing: return
    print("we analyse")
    analysing = True

    
    return

    







def main():
    print("MEOWW! i am main")
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Label(frm, text="Your overall workout efficiency: ").grid(column = 0, row=0)
    ttk.Label(frm, text="Enable live tracking ").grid(column=0, row=1)
    ttk.Button(frm, text="Open Camera", command=LiveAnalyse).grid(column=1, row=1)
    
    root.mainloop()


main()