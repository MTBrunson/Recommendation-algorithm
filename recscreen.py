import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import numpy as np
import pandas as pd

###linking csv file###
rcdpq = pd.read_csv(r'D:\Computer science\Project\databases\films\ratings.csv')

###creating dataframe to store recmmendations###
recommendations = pd.DataFrame(columns = ['customerID', 'productID', 'predicted rating'])

###creating dataframe that only contains productID, customerID and ratings for products with >25 ratings###
grouped_rcdpq = rcdpq.groupby('productID').agg(num_ratings = ('rating','count')).reset_index()
grouped_rcdpq_25 = grouped_rcdpq[grouped_rcdpq['num_ratings']>25]
rcdpq_25 = pd.merge(rcdpq, grouped_rcdpq_25[['productID']], on='productID', how='inner')

#creates a list of customer and product IDs with no repeated values
customer_id_list = rcdpq_25['customerID'].tolist()
customer_id_list = list(dict.fromkeys(customer_id_list))

p25_list = rcdpq_25['productID'].tolist()
p25_list = list(dict.fromkeys(p25_list))

pc_matrix = rcdpq_25.pivot_table(index='productID', columns='customerID', values='rating')

ps_matrix = pc_matrix.T.corr()

###loops for every customer###
for count in range (0,len(customer_id_list)):
    customer_id = customer_id_list[count]

    ###creates a dataframe containg every product a customer has bought###
    customer_bought = pd.DataFrame(pc_matrix[customer_id].dropna(axis=0, how='all'))
    customer_bought.rename(columns={customer_id:'rating'}, inplace = True)
    customer_bought = customer_bought.reset_index()

    ###creates a dataframe and list containing every item a customer hasn't bought###
    customer_nb = pd.DataFrame(pc_matrix[customer_id].isna())
    customer_nb = customer_nb.reset_index()
    customer_nb_list = customer_nb[customer_nb[customer_id]==True]['productID'].values.tolist()

    ###loops for every item that a customer hasn't bought###
    for product_id in customer_nb_list:
        
        ###comparing each product to every other product and calculating similarity based on ratings###
        product_similarity = pd.DataFrame(ps_matrix[product_id].copy())
        product_similarity = product_similarity.reset_index()
        product_similarity.rename(columns={product_id:'similarity'}, inplace=True)

        customer_bought_sim = pd.merge(left=customer_bought, right = product_similarity, on = 'productID', how = 'inner')
        customer_bought_sim.sort_values('similarity')

        ###predicting a customers rating of a product, more similar products are weighted more###
        pred_rating = np.average(customer_bought_sim['rating'], weights=customer_bought_sim['similarity'])

        ###add the customer ID, product ID and predicted rating to a dataframe###
        rec_new_row = pd.DataFrame({'customerID':[customer_id], 'productID': [product_id], 'predicted rating':[pred_rating]})
        recommendations = pd.concat([recommendations, rec_new_row])

###removing records where the predicted rating is less than 3.5###
recommendations = recommendations[recommendations['predicted rating'] > 3.5]
 
###creates custostomer ID list and adds every customer ID from the column customerID in the recommendation data frame###
ci_list = []
ci_list.extend(recommendations['customerID'].tolist())
ci_list = map(str, ci_list)
ci_list = list(ci_list)

###creates a product recommendations list and adds every product ID from the column productID in the recommendations data frame###
pr_recs_list = []
pr_recs_list.extend(recommendations['productID'].tolist())
 

rwindow = tk.Tk() 

reexist = rwindow.winfo_exists()
if reexist == False:
    rwindow = tk.Tk()


def closerec():
    rwindow.destroy()

def homescreen():
    import homescreen as hosc

def recscreen():

    rwindow.title("Recommendations") 
    rwindow.configure(bg="#95baf7")

    ###creates 4 rows and 2 columns###
    for i in range(0,3):
        rwindow.columnconfigure(i, weight=1, minsize=10) 
        rwindow.rowconfigure(i, weight=1, minsize=10) 
        for j in range(2): 
            rframe = tk.Frame( 
                master=rwindow 
            ) 
            rframe.grid(row=i, column=j) 

            ###creates and displayes the title###
            title = tk.Label( 
                master=rwindow, 
                text="RECOMMENDATIONS", 
                fg="white", 
                bg="#95baf7", 
                width=17, 
                height=2, 
                font=('Arial',17, 'bold') 
            ) 
            title.grid(row=0, column=0, sticky="nw")

            ###creates and displayes the back button and gives it functionality###
            back_btn = tk.Button( 
                master=rwindow, 
                text="Back", 
                fg="white", 
                bg="#5f8bd5", 
                width=30, 
                height=1,
                command=lambda: [homescreen(), closerec()]
                ) 
            back_btn.grid(row=1,column=1,sticky="ne") 

            ###creates the header customer ID to go above the list of customer IDs###
            CID_header = tk.Label( 
                master=rwindow, 
                text="Customer ID", 
                fg="white", 
                bg="#95baf7", 
                width=30, 
                height=1 
            )
            CID_header.grid(row=2, column=0, sticky="nw")

            ###creates a scroll bar to allow the customer ID list to be scrolled through###
            yscrollbar1 = Scrollbar(rwindow)
            yscrollbar1.grid(row=3, column=0, sticky='nse')

            ###uses listbox widget to display list items###
            CID_list = Listbox(
                master=rwindow,
                yscrollcommand = yscrollbar1.set
            )
            CID_list.grid(row=3, column=0, sticky='nw')

            ###iterates through the ci_list to display all items in the list###
            for x in range(len(ci_list)):
                CID_list.insert(END, ci_list[x])
                CID_list.itemconfig(x, bg = '#95baf7', fg='white')
            CID_list.grid(row=3, column=0, sticky='nw')

            yscrollbar1.config(command = CID_list.yview)

            ###creates the header for the list of product IDs###
            PID_header = tk.Label( 
                master=rwindow, 
                text="Product ID", 
                fg="white", 
                bg="#95baf7", 
                width=30, 
                height=2 
            ) 
            PID_header.grid(row=2, column=1, stick="ne")

            ###creates a scroll bar to allow the product ID list to be scrolled throught###
            yscrollbar2 = Scrollbar(rwindow)
            yscrollbar2.grid(row=3, column=1, sticky= 'nse')

            ###uses list box widget to display list items###
            PID_list = Listbox(
                master=rwindow,
                yscrollcommand = yscrollbar2.set
            )
            PID_list.grid(row=3, column=1, sticky='nw')

            ###iterates throught the pr_recs_list to display all items in the list###
            for x in range (len(pr_recs_list)):
                PID_list.insert(END, pr_recs_list[x])
                PID_list.itemconfig(x, bg='#95baf7', fg='white')
            PID_list.grid(row=3, column=1, sticky='nw')

            yscrollbar2.config(command = PID_list.yview)



recscreen()
