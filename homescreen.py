import tkinter as tk
from tkinter import *
from tkinter.ttk import *

hwindow = tk.Tk() 
hwindow.geometry("500x200")

hsexist = hwindow.winfo_exists()
if hsexist == False:
    hwindow = tk.Tk()

def closehome(): 
    hwindow.destroy() 

def recscreen():
    import recscreen as resc

def stockscreen():
    import stockscreen as stsc

def homescreen():

    hwindow.title("Home screen") 
    hwindow.configure(bg="#95baf7") 

    for i in range(0,3): 
        hwindow.columnconfigure(i, weight=1, minsize=10) 
        hwindow.rowconfigure(i, weight=1, minsize=10) 
        for j in range(2): 
            hframe = tk.Frame( 
                master=hwindow, 
                relief=tk.RAISED, 
                borderwidth=1 
            ) 
            hframe.grid(row=i, column=j) 

            title = tk.Label( 
                master=hwindow, 
                text="HOMESCREEN", 
                fg="white", 
                bg="#95baf7", 
                width=17, 
                height=2, 
                font=('Arial', 17, 'bold') 
            ) 
            title.grid(row=0, column=0) 

            btn_recs= tk.Button( 
                master=hwindow, 
                text="RECOMMENDATIONS", 
                width=17, 
                height=2, 
                bg="#5f8bd5", 
                fg="white", 
                command=lambda: [recscreen(), closehome()] 
            ) 
            btn_recs.grid(row=1, column=0, sticky="n") 

            btn_stock= tk.Button( 
                master=hwindow, 
                text="STOCK", 
                width=17, 
                height=2, 
                bg="#5f8bd5", 
                fg="white", 
                command=lambda: [stockscreen(), closehome()] 
            ) 
            btn_stock.grid(row=1, column=1, sticky="nw") 


homescreen() 
