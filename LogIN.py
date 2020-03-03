import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import webbrowser

root = Tk()
menu = Menu(root)

root.config(menu=menu)
nextmenu = Menu(menu)
menu.add_cascade(label="Menus",menu=nextmenu)

pw = PanedWindow(orient = 'vertical')
title = Label(root, text="Main Menu")
title.pack(side = TOP)
pw.add(title)
pw.add(title)
pw.pack(fill = BOTH, expand = True)

USERNAME = StringVar()
PASSWORD = StringVar()

def ShowPolicy():
    webbrowser.open_new(r"https://github.com/AdminTeamUSW2019/Admin---GUI/blob/master/PolicyV1.md")

def Database():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_name TEXT, product_qty TEXT, product_price TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Account Login")
    loginform.configure(bg='grey')
    width = 2000
    height = 1000
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()

def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=10, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)

def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()

##Nick's Part

def ShowQueryForm():
    global queryform
    queryform = Toplevel()
    queryform.title("Query Submission")
    width = 2000
    height = 1000
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    queryform.resizable(0, 0)
    queryform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    QueryForm()

def QueryForm():
    global lbl_result
    TopQForm = Frame(queryform, width=600, height=100, bd=1, relief=SOLID)
    TopQForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopQForm, text="Query Submission", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidQForm = Frame(queryform, width=600)
    MidQForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidQForm, text="Type of Problem:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidQForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result = Label(MidQForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    problembox = ttk.Combobox(MidQForm, values=["Issue with Software", "Hardware Issue", "Request Technical Support", "Other"], font=('arial', 25), width=25)
    problembox.grid(row=0, column=1)
    problembox.current(1)
    password = Entry(MidQForm, textvariable=PASSWORD, font=('arial', 25), width=15)
    password.grid(row=1, column=1)
    btn_login = Button(MidQForm, text="Login", font=('arial', 18), width=30, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)

##Nick's Part

def ShowAdminForm():
    global adminform
    adminform = Toplevel()
    adminform.title("Query Submission")
    width = 2000
    height = 1000
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    adminform.resizable(0, 0)
    adminform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    AdminForm()

def AdminForm():
    global lbl_result
    TopAForm = Frame(adminform, width=600, height=100, bd=0, relief=SOLID)
    TopAForm.pack(side=TOP)
    lbl_text = Label(TopAForm, text="Admin", font=('arial', 18), width=600, bg='grey', fg='white')
    lbl_text.pack(fill=X)

    SideAForm = Frame(adminform, width=150, height=1000, bd=0, relief=SOLID, bg='grey')
    SideAForm.pack(side=LEFT)
    btn_dash = Button(SideAForm, text="Dashboard", font=('arial', 18), command=Login)
    ##btn_dash.pack(fill=Y)
    btn_dash.grid(row=1000, column=0)
    SideAForm.grid_rowconfigure(0, weight=1)
    SideAForm.grid_columnconfigure(0, weight=1)

    MidQForm = Frame(adminform, width=600)
    MidQForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidQForm, text="Type of Problem:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidQForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result = Label(MidQForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    problembox = ttk.Combobox(MidQForm, values=["Issue with Software", "Hardware Issue", "Request Technical Support", "Other"], font=('arial', 25), width=25)
    problembox.grid(row=0, column=1)
    problembox.current(1)
    password = Entry(MidQForm, textvariable=PASSWORD, font=('arial', 25), width=15)
    password.grid(row=1, column=1)
    btn_login = Button(MidQForm, text="Login", font=('arial', 18), width=30, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)

def ShowHome():
    root.show()
    loginform.destroy()

nextmenu.add_command(label='Log In', command=ShowLoginForm)
nextmenu.add_command(label='Query', command=ShowQueryForm)
nextmenu.add_command(label='Admin', command=ShowAdminForm)
nextmenu.add_command(label='Policy', command=ShowPolicy)
nextmenu.add_separator()
nextmenu.add_command(label='Exit', command=root.quit)

mainloop()