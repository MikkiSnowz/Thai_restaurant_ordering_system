#Main Ordering page

#Importing libraries
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
import subprocess


#Importing XML library
import xml.etree.ElementTree as ET
tree = ET.parse("Customer.xml")
rootx = tree.getroot()

root = Tk()

#Configuring the screen
root.configure(bg="grey")
root.geometry("1300x800")
root.title("Ordering Page / Menu")


#Total and checkes
current_total = 0
count = 0


#ORDER DETAILS
DATA = []


#Frames Section
#------------------------------------------------------

#Ordering Frame
OrderFrame = Frame(root, width=250, height= 450)
OrderFrame.place(x=20,y=100)


#Menu Frame
MenuFrame = Frame(root,width=650, height=550)
MenuFrame.place(x=600,y=100)

#------------------------------------------------------


#Method

#Function: writing the customer's information including firstname,lastname, order details and total price to an XML file
#Input: (String) firstname, lastname, total price and order details
#Output: (String) firstname, lastname, total price and order details written to an XML file and saved onto the file

def Write_XML ():
    global current_total
    global DATA
    global ent_firstname
    global ent_lastname

    if ent_firstname.get() == "" and ent_lastname.get() == "":
        messagebox.showwarning(message="Please enter your first name and last name")
    elif ent_firstname.get() == "":
        messagebox.showwarning(message="Please enter your first name")
    elif ent_lastname.get() == "":
        messagebox.showwarning(message="Please enter your last name")
    else:

        first_name = ent_firstname.get()

        last_name = ent_lastname.get()


        #writing to XML file 
        newrecords = ET.SubElement(rootx,"detail")

        F_name = ET.SubElement(newrecords,"firstname")
        F_name.text = first_name
        
        L_name = ET.SubElement(newrecords,"lastname")
        L_name.text = last_name

        data = ET.SubElement(newrecords,"order")
        data.text = str(DATA)

        total = ET.SubElement(newrecords,"total")
        total.text = str(current_total)

        ET.indent(tree,space="\t",level=0)

        tree.write("Customer.xml")

        messagebox.showinfo(message="Your order has been saved!")
        root.destroy()
        subprocess.Popen('Main menu.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)




def delete_order():
    messagebox.showinfo(message="The order has been deleted")
    root.destroy()
    subprocess.Popen('Main menu.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)

def send_order():
    messagebox.showinfo(message="The order has been sent to the kitchen!")

#Function: Calculating the total price of the order 
#Input: A current total (float)
#Output: Displaying the current total in a string on the root window
def calculate_total():
    global current_total
    global lbl_total
    current_total_dp = Label(root,text=f"Total: {current_total}$", font=("Arial", 20), bg="grey")
    current_total_dp.place(x=20, y=600)

#Function: Displaying the items on the order frame to indicate that an order has been selected
#Input: A click on the appropriate button for a specific item
#Output: A label will pop up on the order frame indicating the selected items
     
def display_panang():
    global DATA
    global count
    global current_total
    count = count + 1
    if count <= 15:
        lbl_panang = Label(OrderFrame, text="21.00$ Panang curry",font=("Arial Bold",16))
        lbl_panang.pack()
        current_total = current_total + 21.00
        DATA.append("21.00$ Panang curry")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_massaman():
    global DATA
    global count
    global current_total
    count = count + 1
    if count <= 15:
        lbl_massaman = Label(OrderFrame, text="27.00$ Gang Massaman",font=("Arial Bold",16))
        lbl_massaman.pack()
        current_total = current_total + 27.00
        DATA.append("27.00$ Gang Massaman")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_padthai():
    global DATA
    global count
    global current_total
    count = count + 1
    if count <= 15:
        lbl_padthai = Label(OrderFrame, text="23.00$ Pad Thai",font=("Arial Bold",16))
        lbl_padthai.pack()
        current_total = current_total + 23.00
        DATA.append("23.00$ Pad Thai")

    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass
    
def display_green_curry():
    global current_total
    global count
    count = count + 1
    if count <= 15:
        lbl_green_curry = Label(OrderFrame, text="23.00$ Green Curry",font=("Arial Bold",16))
        lbl_green_curry.pack()
        current_total = current_total + 23.00
        DATA.append("23.00$ Green Curry")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_padseew():
    global count
    global current_total
    count = count + 1
    if count <= 15:
        lbl_padseew = Label(OrderFrame, text="20.00$ Pad-Se-Ew",font=("Arial Bold",16))
        lbl_padseew.pack()
        current_total = current_total + 23.00
        DATA.append()
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_fried_rice():
    global count
    global current_total 
    count = count + 1
    if count <= 15:    
        lbl_thai_fried_rice = Label(OrderFrame, text="20.00$ Thai Fried Rice",font=("Arial Bold",16))
        lbl_thai_fried_rice.pack()
        current_total = current_total + 23.00
        DATA.append("20.00$ Pad-Se-Ew")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_Tom_Yum():
    global count
    global current_total 
    count = count + 1
    if count <= 15:
        lbl_tom_yum = Label(OrderFrame, text="18.00$ Tom-Yum-Soup",font=("Arial Bold",16))
        lbl_tom_yum.pack()
        current_total = current_total + 18.00
        DATA.append("18.00$ Tom-Yum-Soup")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_gapow():
    global current_total
    global count
    count = count + 1
    if count <= 15:
        lbl_gapow = Label(OrderFrame, text="21.00$ Pad-Gapow",font=("Arial Bold",16))
        lbl_gapow.pack()
        current_total = current_total + 21.00
        DATA.append("21.00$ Pad-Gapow")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_padkeemao():
    global count
    global current_total 
    count = count + 1
    if count <= 15:
        lbl_padkeemao = Label(OrderFrame, text="24.00$ Pad-Kee-Mao",font=("Arial Bold",16))
        lbl_padkeemao.pack()
        current_total = current_total + 21.00
        DATA.append("24.00$ Pad-Kee-Mao")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass
def display_coke():
    global count
    global current_total 
    count = count + 1
    if count <= 15:
        lbl_coke = Label(OrderFrame, text="4.00$ Coca-Cola",font=("Arial Bold",16))
        lbl_coke.pack()
        current_total = current_total + 4.00
        DATA.append("4.00$ Coca-Cola")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_kaitao():
    global count
    global current_total 
    count = count + 1
    if count <= 15:
        lbl_kaitao = Label(OrderFrame, text="15.00$ Kaitao",font=("Arial Bold",16))
        lbl_kaitao.pack()
        current_total = current_total + 15.00
        DATA.append("15.00$ Kaitao")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def display_temveg():
    global count
    global current_total 
    count = count + 1
    if count <= 15:
        lbl_tem_veg = Label(OrderFrame, text="20.00$ Tempura Vegetables",font=("Arial Bold",16))
        lbl_tem_veg.pack()
        current_total = current_total + 15.00
        DATA.append("20.00$ Yempura Vegetables")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass
    
    

    
def apply_discount():
    global current_total
    global count
    if count <= 15:
        count = count + 1
        lbl_discount = Label(OrderFrame, text="10% discount",font=("Arial Bold",16))
        lbl_discount.pack()
        percent_off = current_total*0.1
        current_total = round(current_total - percent_off,3)
        DATA.append("10% discount")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass

def apply_surcharge():
    global current_total
    global count
    if count <= 15:
        count = count + 1
        lbl_surcharge = Label(OrderFrame, text="2% surcharge",font=("Arial Bold",16))
        lbl_surcharge.pack(fill="both", expand=True)
        charge = current_total*0.02
        current_total = round(current_total + charge,3)
        DATA.append("2% surcharge")
    else:
        messagebox.showinfo(message="You have reached the maximum amount of items per order")
        pass
 

        
    



#Labels
lbl_customer_detail = Label(root, text="Customer:\n Details", font=("Arial Bold",20), bg="grey")
lbl_customer_firstname = Label(root, text="First name:", font=("Arial",16), bg="grey")
lbl_customer_lastname = Label(root, text="Last name:", font=("Arial",16), bg="grey")
lbl_menu = Label(root, text="Menu", font=("Arial Black",26), bg='grey')
lbl_tbl_tk2 = Label(root, text="TK-2:", font=("Arial Black",24), bg='grey')

#Buttons
btn_save = Button(root, text="SAVE ORDER", font=("Arial", 16), bg="#00ff00",relief=SUNKEN, height=1, width=12, command=Write_XML)
btn_delete = Button(root, text="DELETE ORDER",font=("Arial", 16), bg="Red",relief=SUNKEN,  height=1, width=14, command=delete_order)
btn_discount = Button(root, text="APPLY\nDISCOUNT", font=("Arial", 16), bg="#00ff00",relief=SUNKEN,width=12, command=apply_discount)
btn_surcharge = Button(root, text="APPLY\nSURCHARGE",font=("Arial", 16), bg="Red",relief=SUNKEN,width=14, height=2, command= apply_surcharge)
btn_send = Button(root, text="SEND",font=("Arial", 16), bg="Yellow",relief=SUNKEN,width=14, height=3, command=send_order)

#Entries
ent_firstname = Entry(root)
ent_lastname = Entry(root)



#Total section
lbl_total = Label(root,text=f"Total: {current_total}$", font=("Arial", 20), bg="grey")
lbl_total.place(x=20,y=600)
btn_cal_total = Button(root, text="Calculate the total", width=14, height=2,command=calculate_total,font=("Arial", 14))
btn_cal_total.place(x=230, y=590)







#Menu Frame section (Button)
btn_panang = Button(MenuFrame, text="Gang Panang",font=("Arial", 16),command=display_panang,bg="light green", height=3,width=13)
btn_panang.place(x=25, y=50)
btn_massaman = Button(MenuFrame, text="Gang Massaman",font=("Arial", 16),command=display_massaman,bg="light green", height=3,width=13)
btn_massaman.place(x=240, y=50)
btn_green_curry = Button(MenuFrame, text="Green curry",font=("Arial", 16),command=display_green_curry,bg="light green", height=3,width=13)
btn_green_curry.place(x=25, y=180)
btn_padthai = Button(MenuFrame, text="Pad Thai",font=("Arial", 16),command=display_padthai,bg="light green", height=3,width=13)
btn_padthai.place(x=240, y=180)
btn_padseew = Button(MenuFrame, text="Pad-Se-Ew",font=("Arial", 16),command=display_padseew,bg="light green", height=3,width=13)
btn_padseew.place(x=465, y=50)
btn_thai_fried_rice = Button(MenuFrame, text="Thai Fried Rice",font=("Arial", 16),command=display_fried_rice,bg="light green", height=3,width=13)
btn_thai_fried_rice.place(x=465, y=180)
btn_tomyum = Button(MenuFrame, text="Tom-Yum-Soup",font=("Arial", 16),command=display_Tom_Yum,bg="light green", height=3,width=13)
btn_tomyum.place(x=465, y=310)
btn_gapow = Button(MenuFrame, text="Pad-Gapow",font=("Arial", 16),command=display_gapow,bg="light green", height=3,width=13)
btn_gapow.place(x=240, y=310)
btn_padkeemao = Button(MenuFrame, text="Pad-Kee-Mao",font=("Arial", 16),command=display_padkeemao,bg="light green", height=3,width=13)
btn_padkeemao.place(x=25, y=310)
btn_coke = Button(MenuFrame, text="Coca-cola",font=("Arial", 16),command=display_coke,bg="light green", height=3,width=13)
btn_coke.place(x=25, y=440)
btn_kaitao = Button(MenuFrame, text="Kaitao",font=("Arial", 16),command=display_kaitao,bg="light green", height=3,width=13)
btn_kaitao.place(x=240, y=440)
btn_tem_veg = Button(MenuFrame, text="Tempura Veg",font=("Arial", 16),command=display_temveg,bg="light green", height=3,width=13)
btn_tem_veg.place(x=465, y=440)





#Dislay section
lbl_customer_detail.place(x=0,y=15)
lbl_customer_firstname.place(x=150,y=20)
lbl_customer_lastname.place(x=150,y=50)
lbl_menu.place(x=880,y=40)
ent_firstname.place(x=270,y=25)
ent_lastname.place(x=270,y=60)
btn_save.place(x=20,y=675)
btn_delete.place(x=190,y=675)
btn_discount.place(x=20,y=725)
btn_surcharge.place(x=190,y=725)
btn_send.place(x=1073, y=675)
lbl_tbl_tk2.place(x=1140,y=45)







root.mainloop()
