#Ped Thain Cuisine Ordering system
#Login Page
#17/07/2024


#Importing libraries
from tkinter import *
import subprocess
from tkinter import messagebox
import time

#XML file
import xml.etree.ElementTree as ET
tree = ET.parse("Login_details.xml")
rootx = tree.getroot()





#Configuration
root = Tk()
root.configure(bg="Grey")
root.geometry("720x480")
root.title("Ped Thai Cuisine Ordering System Login Page")

#Methods

#Function: Showing the password once the checkbox is checked
#Input: A string in the entry box
#Output: A visible string in the entry box
def show_password():
    if ent_pass.cget('show') == "*":
        ent_pass.config(show='')
    else:
        ent_pass.config(show='*')
#Function: Logging into the software with username and password
#Input:(String) username and password
#Output: A messagebox telling the user if they have successfully log in or not
def login():
    global ent_user
    global ent_pass
    
    for i in rootx.findall("detail"):
        user = i.find("username").text
        password = i.find("password").text
    

        if ent_user.get() == user and ent_pass.get() == password:
            messagebox.showinfo(message="You have successfully logged in!")
            time.sleep(1)
            root.destroy()
            subprocess.Popen('Main menu.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
        elif ent_user.get() == "" and ent_pass.get() == "":
            messagebox.showinfo(message="Please enter your username and password")
        elif ent_user.get() == "":
            messagebox.showinfo(message="Please enter your username")
        elif ent_pass.get() == "":
            messagebox.showinfo(message="Please enter your password")
        elif ent_user.get() != user or ent_pass.get() != password:
            messagebox.showerror(message="Incorrect login details")

#Labels
lbl_pagetitle = Label(root, text="Ped Thai Cuisine\n Ordering system", font=("Arial Black", 26), bg="grey")
lbl_user = Label(root, text="Username:", font=("Arial", 18), bg="grey")
lbl_pass = Label(root, text="Password:", font=("Arial", 18), bg="grey")

#Entries
ent_user = Entry(root)
ent_pass = Entry(root, show="*")

#Button
btn_login = Button(root, text="Login",font=("Arial", 18),command=login)

#Checkbox
Chb_pass = Checkbutton(root, text="show password",font=("Arial", 12),bg="grey",command=show_password)

#Images
logoImg = PhotoImage(file="Logo.png", master=root)
lbl_logo = Label(root, image=logoImg, bg="grey")


#Placing object
lbl_logo.place(x=260,y=130)
btn_login.place(x=320, y=370)
lbl_pagetitle.place(x=200,y=0)
lbl_user.place(x=140,y=300)
lbl_pass.place(x=140,y=330)
ent_user.place(x=270,y=305, width=200)
ent_pass.place(x=270,y=335, width=200)
Chb_pass.place(x=480,y=335)

root.mainloop()
