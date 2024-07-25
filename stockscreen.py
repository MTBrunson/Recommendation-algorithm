import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import datetime
from datetime import date, timedelta
import pandas as pd

###reads csv files###
stock = pd.read_csv(r'D:\Computer science\Project\final code and csv files\stock levels.csv')
date_column = ['date']
rcdpq = pd.read_csv(r'D:\Computer science\Project\final code and csv files\rcdpq.csv', parse_dates=date_column, dayfirst=True)

'''
###start and end dates related to current date###
end_date = str(date.today())
start_date = datetime.datetime.now() - datetime.timedelta(30)
'''

###sets start and end dates###
start_date = '2021-06-14'
end_date = '2021-07-14'


###creates a list of all products###
product_list = rcdpq['productID'].tolist()
product_list = list(dict.fromkeys(product_list))
    
stock_level_prediction = pd.DataFrame(columns = ['productID', 'outofstockdate'])
    
###loops for every product###
for product_id in product_list:
    product_df = rcdpq[rcdpq['productID']==product_id]
    
    ###extracts rows between start and end date###
    thirty_days = product_df.loc[product_df['date'].between(start_date, end_date)]

    ###calculating how many were bought in the last 30 days###
    bought_list = thirty_days['quantityBought'].tolist()
    quantity_bought = sum(bought_list)

    if quantity_bought > 0:
        ###average sold per day###
        average_30_days = quantity_bought / 30

        ###number currently in stock###
        in_stock_df = stock[stock['productID']==product_id]
        in_stock = in_stock_df['inStock'].tolist()
        in_stock = sum(in_stock)

        ###calculating the days until product runs out###
        days_left = in_stock / average_30_days
        days_left = int(days_left)

        ###date product will run out on###
        out_of_stock_date = datetime.datetime.now() + datetime.timedelta(days_left)
        out_of_stock_date = out_of_stock_date.strftime('%d-%m-%Y')

        ###adding the product ID and out of stock date to the sotck_level_prediction dataframe###

        pred_new_row = pd.DataFrame({'productID':[product_id], 'outofstockdate':[out_of_stock_date]})
        stock_level_prediction = pd.concat([stock_level_prediction, pred_new_row])

    
###list of all product IDs##                                                   
pi_list = []
pi_list.extend(stock_level_prediction['productID'].tolist())

###list of all dates###
date_list = []
date_list.extend(stock_level_prediction['outofstockdate'].tolist())

    
swindow = tk.Tk() 

stexist = swindow.winfo_exists()
if stexist == False:
    swindow = tk.Tk() 

def closestock():
    swindow.destroy()

def closehome(): 
    hwindow.destroy()

def homescreen():
    import homescreen as hosc

def stockscreen():

    swindow.configure(bg="#95baf7") 
    swindow.title("Stock")

    ###creates 4 rows and 2 columns###
    for i in range(0, 3): 
        swindow.columnconfigure(i, weight=1, minsize=10) 
        swindow.rowconfigure(i, weight=1, minsize=10) 
        for j in range(2): 
            sframe = tk.Frame( 
                master=swindow, 
                relief=tk.RAISED, 
                borderwidth=1 
            ) 
            sframe.grid(row=i, column=j) 

            ###creates and displays the title###
            title = tk.Label( 
                master=swindow, 
                text="STOCK", 
                fg="white", 
                bg="#95baf7", 
                width=17, 
                height=2, 
                font=('Arial',17, 'bold') 
            ) 
            title.grid(row=0, column=0, sticky="nw") 

            ###creates and displays the back button and gives it functionality###
            back_btn = tk.Button( 
                master=swindow, 
                text="Back", 
                fg="white", 
                bg="#5f8bd5", 
                width=30, 
                height=1,
                command=lambda: [homescreen(), closestock()]
                ) 
            back_btn.grid(row=1, column=1, sticky="ns") 
            
            ###creates the header product ID to go above the list of product IDs###
            PID_header = tk.Label( 
                master=swindow, 
                text="Product ID", 
                fg="white", 
                bg="#95baf7", 
                width=30, 
                height=1 
            ) 
            PID_header.grid(row=2, column=0, sticky="nw")

            ###creates a scroll bar to allow the product ID list to be scrolled throught###
            yscrollbar1 = Scrollbar(swindow)
            yscrollbar1.grid(row=3, column=0, sticky='nse')

            ###uses listbox widget to display the list items###
            PID_list = Listbox(
                master = swindow,
                yscrollcommand = yscrollbar1.set
            )
            PID_list.grid(row=3, column=0, sticky='nw')

            ###iterates throught the pi_list to display each item###
            for x in range(len(pi_list)):
                PID_list.insert(END, pi_list[x])
                PID_list.itemconfig(x, bg = '#95baf7', fg='white')
            PID_list.grid(row=3, column=0, sticky='nw')

            yscrollbar1.config(command = PID_list.yview)
                
            ###creates the header for the list of dates###
            date_header = tk.Label( 
                master=swindow, 
                text="Date", 
                fg="white", 
                bg="#95baf7", 
                width=30, 
                height=2 
            ) 
            date_header.grid(row=2, column=1, stick="ne")

            ###creates a scroll bar to allow the dates list to be scrolled throught##
            yscrollbar2 = Scrollbar(swindow)
            yscrollbar2.grid(row=3, column=1, sticky='nse')

            ###uses the listbox widget to display the list items###
            dates_list = Listbox(
                master = swindow,
                yscrollcommand = yscrollbar2.set
            )
            dates_list.grid(row=3, column=1, sticky='nw')

            ####iterates through the dates_list to display each item###
            for x in range(len(date_list)):
                dates_list.insert(END, date_list[x])
                dates_list.itemconfig(x, bg = '#95baf7', fg='white')
            dates_list.grid(row=3, column=1, sticky='nw')

            yscrollbar2.config(command = dates_list.yview)




stockscreen()
