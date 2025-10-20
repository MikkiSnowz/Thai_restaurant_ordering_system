#Ped Thai Cuisine Ordering System
#Main Menu 
#11/06/2024





#Importing libraries
from tkinter import *
import subprocess
#from tkmacosx import Button



root = Tk()

#configuration
root.configure(bg="Grey")
root.geometry("1300x800")
root.title("Ped Thai Cuisine Ordering System")

#Methods
#Function: Transit into the next page when clicked
#Input: Clicking a button
#Output: Transition into the next intended page
def exits():
    root.destroy()
def newfile_TBL1():
    root.destroy()
    subprocess.Popen('Ordering Page.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TBL2():
    root.destroy()
    subprocess.Popen('Ordering Page_2.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TBL3():
    root.destroy()
    subprocess.Popen('Ordering Page_3.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TBL4():
    root.destroy()
    subprocess.Popen('Ordering Page_4.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TBL5():
    root.destroy()
    subprocess.Popen('Ordering Page_5.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TBL6():
    root.destroy()
    subprocess.Popen('Ordering Page_6.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TK1():
    root.destroy()
    subprocess.Popen('Ordering Page_tk1.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TK2():
    root.destroy()
    subprocess.Popen('Ordering Page_tk2.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
def newfile_TK3():
    root.destroy()
    subprocess.Popen('Ordering Page_tk3.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)
    
def newfile_functionality():
    root.destroy()
    subprocess.Popen('Functionality Page.py',shell=True,stdin=None,stdout=None, stderr=None,close_fds=True)


#Labels




#Images
logoImg = PhotoImage(file="Logo.png", master=root)
titleImg = PhotoImage(file="ResTitle.png", master=root)
tk_button = PhotoImage(file="TK-1BT.png", master=root)
tk_button_2 = PhotoImage(file="TK-2BT.png", master=root)
tk_button_3 = PhotoImage(file="TK-3BT.png", master=root)


#Placing images into the objects
btn_tk1 = Button(root, image=tk_button,bg="grey",relief=FLAT,command=newfile_TK1)
btn_tk2 = Button(root, image=tk_button_2,bg="grey",relief=FLAT,command=newfile_TK2)
btn_tk3 = Button(root, image=tk_button_3,bg="grey",relief=FLAT,command=newfile_TK3)
lbl_logo = Label(root, image=logoImg, bg="grey")
lbl_title = Label(root, image=titleImg, width=316, height=466, bg="grey")

#Buttons
btn_tbl_1 = Button(root, text="TBL-1", font=("Arial",20),height= 4, width=10, bg="#1A73FB",relief=RAISED,command=newfile_TBL1)
btn_tbl_2 = Button(root, text="TBL-2", font=("Arial",20),height= 4, width=10, bg="#1A73FB",relief=RAISED,command=newfile_TBL2)
btn_tbl_3 = Button(root, text="TBL-3", font=("Arial",20),height= 4, width=10, bg="#1A73FB",relief=RAISED,command=newfile_TBL3)
btn_tbl_4 = Button(root, text="TBL-4", font=("Arial",20),height= 4, width=10, bg="#1A73FB",relief=RAISED,command=newfile_TBL4)
btn_tbl_5 = Button(root, text="TBL-5", font=("Arial",20),height= 4, width=10, bg="#1A73FB",relief=RAISED,command=newfile_TBL5)
btn_tbl_6 = Button(root, text="TBL-6", font=("Arial",20),height= 4, width=10, bg="#1A73FB",relief=RAISED,command=newfile_TBL6)
btn_function = Button(root, text="Functionality", font=("Arial",20),height= 3, width=10, bg="Yellow",relief=RAISED,command=newfile_functionality)
btn_close_app = Button(root, text="Close app", font=("Arial",20),height= 3, width=10, bg="Red",relief=RAISED,command=exits)



#Placing the objects
#Displaying buttons
btn_tbl_1.place(x=400, y=50)
btn_tbl_2.place(x=400, y=250)
btn_tbl_3.place(x=400, y=450)
btn_tbl_4.place(x=650, y=50)
btn_tbl_5.place(x=650, y=250)
btn_tbl_6.place(x=650, y=450)
btn_function.place(x=400, y=650)
btn_close_app.place(x=650, y=650)
btn_tk1.place(x=900, y=50)
btn_tk2.place(x=900, y=250)
btn_tk3.place(x=900, y=450)





lbl_logo.grid(row=0,column=0)
lbl_title.place(x=0,y=200)


root.mainloop()
