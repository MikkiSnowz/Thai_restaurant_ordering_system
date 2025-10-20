#Functionality page

#Importing libraries 
from tkinter import *
import subprocess
from tkinter import messagebox

root=Tk()


#Cofiguring the screen
root.configure(bg="grey")
root.title("Functionality Page")
root.geometry("1380x800")
root.state("zoomed")

#Importing xml libraries
import xml.etree.ElementTree as ET
tree = ET.parse("Customer.xml")
rootx = tree.getroot()

data = []

ent_search = Entry(root)

count = 0

def reset():
    root.destroy()
    subprocess.Popen('Functionality Page.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)

#Function: Calculate the total amount of the money that orders made on that day
#input: (Float) The amount of each orders that was processed on one day
#Output: (Float) All of the orders' total is added up into one total for that one day, it should be display at the bottom
def daily_total():
    Cusrow = 4
    global data 
    global count
    ordernum = 1
    if count == 0:

        for t in rootx.findall("detail"):
            total = float(t.find("total").text)
            data.append(total)

            lbl_headorder = Label(root, text="Order:", font=("Arial Black",16),bg="grey",fg="white")
            lbl_headorder.grid(row=3,column=0)

            lbl_headtotal = Label(root, text="Total:", font=("Arial Black",16),bg="grey",fg="white")
            lbl_headtotal.grid(row=3,column=1)

            lbl_ordernum = Label(root, text=str(ordernum) + ".)", font=("Arial",14),bg="grey",fg="white")
            lbl_ordernum.grid(row=Cusrow,column=0)

            lbl_total = Label(root, text=str(total) + "$", font=("Arial",14),bg="grey",fg="white")
            lbl_total.grid(row=Cusrow,column=1)

            Cusrow = Cusrow + 1
            ordernum = ordernum + 1 


        daily_total = round(sum(data),3)
        lbl_display_income = Label(root, text=f"Overall daily total income for today is\n {daily_total}" + "$", bg="grey", font=("Arial Black",16),fg="white")
        lbl_display_income.grid(row=Cusrow, column=1)
        count = count + 1
    else:
        messagebox.showinfo(message="Please hit the reset button!")
        pass
      



#Function: This function reads from an XML file and display all of the order details from the customer
#Input: Customer information including firstname, lastname, order details and total (String) from XML file
#Output: Display all of the orders in the XML file in each columns and rows
def show_allorder():
    Cusrow= 5
    global data
    global count
    if count == 0:

        for i in rootx.findall("detail"):
            
            f_name = i.find("firstname").text
            l_name = i.find("lastname").text
            order = i.find("order").text
            total_2 = i.find("total").text
            
            lbl_Head = Label(root, text="Customer Order", font=("Arial",20),bg='grey',fg="white")
            lbl_Head.grid(row=3,column=0)

            lbl_Head_2 = Label(root, text="Firstname:", font=("Arial Black",14),bg='grey',fg="white")
            lbl_Head_2.grid(row=4,column=0)

            lbl_Head_3 = Label(root, text="Lastname:", font=("Arial Black",14),bg="grey",fg="white")
            lbl_Head_3.grid(row=4,column=1)

            lbl_Head_4 = Label(root, text="Order:", font=("Arial Black",14),bg="grey",fg="white")
            lbl_Head_4.grid(row=4,column=2)

            lbl_Head_5 = Label(root, text="Total:", font=("Arial Black",14),bg="grey",fg="white")
            lbl_Head_5.grid(row=4,column=3)


            lbl_fname = Label(root, text=f_name, font=("Arial",12),bg="grey",fg="white")
            lbl_fname.grid(row=Cusrow,column=0)

            lbl_lname = Label(root, text=l_name, font=("Arial",12),bg="grey",fg="white")
            lbl_lname.grid(row=Cusrow,column=1)

            lbl_order = Label(root, text=order, font=("Arial",7),bg="grey",fg="white")
            lbl_order.grid(row=Cusrow,column=2)

            lbl_total_2 = Label(root, text=str(total_2) + "$", font=("Arial",12),bg="grey",fg="white")
            lbl_total_2.grid(row=Cusrow,column=3)

            Cusrow = Cusrow + 1

        count = count + 1
    else:
        messagebox.showinfo(message="Please hit the reset button")
        pass

#Function : Creates a sorted two dimensional array with customer information from the XML files and display on the graphical user interface 
#Input: Multi-dimensional array, (customer information)
#Output: Return a sorted multi-dimensional array and display on the graphical user interface 
def sort_total():
    global data
    global count
    if count == 0:
            
        Cusrow=5
        list = []
        for i in rootx.findall("detail"):
            list.append([i.find("firstname").text, i.find("lastname").text, i.find("order").text, i.find("total").text])
        #Selection sort
            for x in range(0, len(list)-1):
                smallest = x

                for j in range(x+1,int(len(list))):
                    if float(list[j][3])< float(list[smallest][3]):
                        smallest = j
                if smallest != x:
                    list[x],list[smallest]= list[smallest],list[x]

        for x in list:
            f_name = x[0]
            l_name = x[1]
            order = x[2]
            total_2 = x[3]
            
            lbl_Head = Label(root, text="Customer Order", font=("Arial",20),bg='grey',fg="white")
            lbl_Head.grid(row=3,column=0)

            lbl_Head_2 = Label(root, text="Firstname:", font=("Arial Black",14),bg='grey',fg="white")
            lbl_Head_2.grid(row=4,column=0)

            lbl_Head_3 = Label(root, text="Lastname:", font=("Arial Black",14),bg="grey",fg="white")
            lbl_Head_3.grid(row=4,column=1)

            lbl_Head_4 = Label(root, text="Order:", font=("Arial Black",14),bg="grey",fg="white")
            lbl_Head_4.grid(row=4,column=2)

            lbl_Head_5 = Label(root, text="Total:", font=("Arial Black",14),bg="grey",fg="white")
            lbl_Head_5.grid(row=4,column=3)


            lbl_fname = Label(root, text=f_name, font=("Arial",12),bg="grey",fg="white")
            lbl_fname.grid(row=Cusrow,column=0)

            lbl_lname = Label(root, text=l_name, font=("Arial",12),bg="grey",fg="white")
            lbl_lname.grid(row=Cusrow,column=1)

            lbl_order = Label(root, text=order, font=("Arial",7),bg="grey",fg="white")
            lbl_order.grid(row=Cusrow,column=2)

            lbl_total_2 = Label(root, text=str(total_2) + "$", font=("Arial",12),bg="grey",fg="white")
            lbl_total_2.grid(row=Cusrow,column=3)

            Cusrow = Cusrow + 1
        count = count + 1
    else:
        messagebox.showinfo(message="Please hit the reset button!")
        pass

count1 = 0

#Function: Search for an order of the customer based on their lastname
#Input: A string of the customer's lastname
#Output: The firstname, lastname, order and total price of an customer's order
def search_lastname():
        global ent_search
        global count1
        list_search = []
        if count1 == 0:
                
            for i in rootx.findall("detail"):
                list_search.append([i.find("firstname").text, i.find("lastname").text, i.find("order").text, i.find("total").text])
            check = False
            for x in list_search:
                if ent_search.get() == x[1]:
                    
                    lbl_Head = Label(root, text="Customer Order", font=("Arial",20),bg='grey',fg="white")
                    lbl_Head.grid(row=4,column=0)

                    lbl_Head_2 = Label(root, text="Firstname:", font=("Arial Black",14),bg='grey',fg="white")
                    lbl_Head_2.grid(row=5,column=0)

                    lbl_Head_3 = Label(root, text="Lastname:", font=("Arial Black",14),bg="grey",fg="white")
                    lbl_Head_3.grid(row=5,column=1)

                    lbl_Head_4 = Label(root, text="Order:", font=("Arial Black",14),bg="grey",fg="white")
                    lbl_Head_4.grid(row=5,column=2)

                    lbl_Head_5 = Label(root, text="Total:", font=("Arial Black",14),bg="grey",fg="white")
                    lbl_Head_5.grid(row=5,column=3)
                    
                    lbl_fname = Label(root, text=x[0], font=("Arial",12),bg="grey",fg="white")
                    lbl_fname.grid(row=6,column=0)

                    lbl_lname = Label(root, text=x[1], font=("Arial",12),bg="grey",fg="white")
                    lbl_lname.grid(row=6,column=1)

                    lbl_order = Label(root, text=x[2], font=("Arial",7),bg="grey",fg="white")
                    lbl_order.grid(row=6,column=2)

                    lbl_total_2 = Label(root, text=str(x[3]) + "$", font=("Arial",12),bg="grey",fg="white")
                    lbl_total_2.grid(row=6,column=3)

                    check = True
                    count1 = count1 + 1
                    break
        
                    
                
            if check == False:
                lbl_notfound = Label(root, text="The order is not found",bg="grey",fg="white")
                lbl_notfound.grid(row=4,column=1)
                count = count + 1
                    
        else:
            messagebox.showinfo(message="Please hit the reset button")
            pass
#Function: Displaying the search box and the button for searching 
#Input: Clicking the search for an order function
#Output: Displaying the search entry box and the search button onto the root window
def display_search():
    global count
    global ent_search
    if count == 0:
        lbl_searchbar = Label(root, text="Search bar : ", font=("Arial Black",18),bg="grey",fg='white')
        lbl_searchbar.grid(row=3,column=0)
        lbl_lnamedes = Label(root, text="(Based on customer's lastname)", font=("Arial Black",14),bg="grey",fg='white')
        lbl_lnamedes.grid(row=3,column=3,padx=(10,0))
        ent_search.grid(row=3,column=1)
        btn_search = Button(root, text="Search",font=("Arial",16),command=search_lastname)
        btn_search.grid(row=3,column=2, padx=(10,0))

        count = count + 1
    else:
        messagebox.showinfo(message="Please hit the reset button!")
        pass
        
def page_change():
    root.destroy()
    subprocess.Popen('Main menu.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)

            
            




    


#Labels
lbl_functionality = Label(root, text="Functionality : ", font=("Arial Black", 20),bg='grey',fg="white")
lbl_description = Label(root, text="(This page allows for functions to be perform on customer data)", font=("Arial Black", 16),bg='grey',fg="white")
lbl_display = Label(root, text="Display: ", font=("Arial Black", 20), bg='grey',fg="white")
#Buttons
btn_showorder = Button(root, text="Show all of the order",bg='light green',command=show_allorder,width=20,height=4,font=("Arial",14))
btn_daily_total = Button(root, text="Calculate daily income",bg='light green', command=daily_total,width=20,height=4,font=("Arial",14))
btn_sorttotal = Button(root, text="Sorting based on total",bg='light green', command=sort_total,width=20,height=4,font=("Arial",14))
btn_search = Button(root, text="Search for customer order",bg='light green', command=display_search,width=20,height=4,font=("Arial",14))
btn_reset = Button(root, text="Reset button",bg='light green', width=15,command=reset,height=3,font=("Arial",14))
btn_previous =  Button(root, text="Previous Page",bg='red', width=15,command=page_change,height=3,font=("Arial",14))
#Displaying objects
lbl_functionality.grid(row=0,column=0)
lbl_description.place(x=230,y=5)
lbl_display.grid(row=2,column=0,pady=(120,15))
btn_showorder.place(x=0,y=50)
btn_daily_total.place(x=250,y=50)
btn_sorttotal.place(x=500,y=50)
btn_search.place(x=750,y=50)
btn_reset.place(x=20,y=1000)
btn_previous.place(x=200,y=1000)

root.mainloop()
