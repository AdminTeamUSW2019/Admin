import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
import webbrowser
import urllib.request

from datetime import datetime

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
PIN = StringVar()
FNAME = StringVar()

def ShowPolicy():
    webbrowser.open_new(r"https://github.com/AdminTeamUSW2019/Admin---GUI/blob/master/PolicyV1.md")

##UNUSED
def Database():
    global conn, cursor
    conn = sqlite3.connect("GUITest.db")
    cursor = conn.cursor()
    now = datetime.now()
    now = now.isoformat()
    cursor.execute("CREATE TABLE IF NOT EXISTS `newloggedin` (username VARCHAR(30), password VARCHAR(30), activity STRING)")
    ##Current Progress
    cursor.execute("SELECT * FROM `users` WHERE `username` = 'users' AND `password` = 'users' AND 'activity' = ?", (now))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `loggedin` (username, password) VALUES('users', 'users')")
        conn.commit()
##UNUSED

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Account Login")
    loginform.configure(bg='grey')
    width = 1000
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()

def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=1)
    lbl_text = Label(TopLoginForm, text="System Support Login", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    MidLoginForm.configure(bg='grey')
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_username.configure(bg='grey')
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_password.configure(bg='grey')
    lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    lbl_result.configure(bg='grey')
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=10, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)

def Login(event=None):
    ##Database()
    global conn, cursor, cursor2, lname, username
    conn = sqlite3.connect("GUITest.db")
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `registeredIP` WHERE `username` = ? AND `IPaddress` = ?", (USERNAME.get(), external_ip))
            if cursor.fetchone() is None:
                ShowPINInput()
            else:
                cursor2.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ? AND 'accesslevel' > 0", (USERNAME.get(), PASSWORD.get()))
                if cursor2.fetchmany() is not None:
                    data = cursor2.fetchmany()
                    for rows in data:
                        username = rows[0]
                        FNAME.set(rows[3])
                        lname = rows[4]
                    USERNAME.set("")
                    PASSWORD.set("")
                    lbl_result.config(text="")
                    ShowAdminForm()
                else:
                    data = cursor.fetchone()
                    USERNAME.set("")
                    PASSWORD.set("")
                    lbl_result.config(text="")
                    ShowPolicy()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
    ##cursor.close()
    ##conn.close()

def PINCheck():
    global conn, cursor
    conn = sqlite3.connect("GUITest.db")
    cursor = conn.cursor()
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    if PIN.get == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ? AND `pin` = ?", (USERNAME.get(), PIN.get()))
        if cursor.fetchone() is not None:
            cursor.execute("INSERT INTO `registeredIP` VALUES (?, ?)", (USERNAME.get(), external_ip))
            cursor2.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ? AND 'accesslevel' > 0", (USERNAME.get(), PASSWORD.get()))
            if cursor2.fetchmany() is not None:
                data = cursor2.fetchmany()
                for rows in data:
                    username = rows[0]
                    FNAME.set(rows[3])
                    lname = rows[4]
                USERNAME.set("")
                PASSWORD.set("")
                PIN.set("")
                lbl_result.config(text="")
                ShowAdminForm()
            else:
                data = cursor.fetchone()
                USERNAME.set("")
                PASSWORD.set("")
                PIN.set("")
                lbl_result.config(text="")
                ShowPolicy()
        else:
            lbl_result.config(text="Invalid PIN", fg="red")
    conn.commit()
    conn.close()

def ShowPINInput():
    global PINform
    PINform = Toplevel()
    PINform.title("Please input 4 digit PIN")
    width = 500
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    PINform.resizable(0, 0)
    PINform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    InputPINform()

def InputPINform():
    global lbl_result
    TopPForm = Frame(PINform, width=500, height=50, bd=1, relief=SOLID)
    TopPForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopPForm, text="Please input 4 digit PIN", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidPForm = Frame(PINform, width=300)
    MidPForm.pack(side=TOP, pady=50)
    lbl_pin = Label(MidPForm, text="PIN:", font=('arial', 25), bd=18)
    lbl_pin.grid(row=0)
    lbl_result = Label(MidPForm, text="", font=('arial', 18))
    lbl_result.grid(row=2, columnspan=2)
    pin = Entry(MidPForm, textvariable=PIN, font=('arial', 25), width=15)
    pin.grid(row=0, column=1)
    btn_pin = Button(MidPForm, text="Confirm", font=('arial', 18), width=30, command=PINCheck)
    btn_pin.grid(row=1, columnspan=2, pady=20)
    btn_pin.bind('<Return>', PINCheck)


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
    adminform.title("Admin Menu")
    width = 1000
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    adminform.resizable(0, 0)
    adminform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    NewAdminForm()

def NewAdminForm():
    lbl_message = 'Welcome ' + FNAME.get()
    TopAForm = Frame(adminform, width=600, height=100, bd=0, relief=SOLID)
    TopAForm.pack(side=TOP)
    lbl_text = Label(TopAForm, text="Admin", font=('arial', 18), width=600, bg='grey', fg='white')
    lbl_text.pack(fill=X)

    style = ttk.Style(adminform)
    style.configure('lefttab.TNotebook', tabposition='wn', background='grey')
    notebook = ttk.Notebook(adminform, style='lefttab.TNotebook')
    
    f1 = tk.Frame(notebook, bg='white', width=1000, height=500)
    lbl_dash = Label(f1, text=lbl_message, font=('arial', 25), bg='white')
    lbl_dash.pack(fill=X)
    
    f2 = tk.Frame(notebook, bg='white', width=1000, height=500)
    sb = Scrollbar(f2)
    sb.pack(side = RIGHT, fill=Y)
    mylist = Listbox(f2, yscrollcommand = sb.set)
    for line in range(30):  
        mylist.insert(END, "Number " + str(line))  
    mylist.pack( fill=BOTH )  
    sb.config( command = mylist.yview )  

    f3 = tk.Frame(notebook, bg='green', width=1000, height=500)
    notebook.add(f1, text=f'{"Dashboard": ^20s}')
    notebook.add(f3, text=f'{"Queries": ^24s}')
    notebook.add(f2, text=f'{"User Log": ^23s}')
    notebook.pack(side=TOP)

##Old
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
##Old

def DatabaseTest():
    conn = sqlite3.connect("GUITest.db")
    crsr = conn.cursor()
    sql_command = """CREATE TABLE users (
    username VARCHAR(30) PRIMARY KEY, 
    password VARCHAR(30),
    accesslevel INT, 
    pin VARCHAR(4),
    fname VARCHAR(20),  
    lname VARCHAR(30));"""

    crsr.execute(sql_command)

    sql_command = """CREATE TABLE registeredIP (username VARCHAR(30), IPaddress VARCHAR(20));"""
    crsr.execute(sql_command)

    sql_command = """INSERT INTO users VALUES ("UserOne", "password", 1, 1234, "Bob", "Jones");"""
    crsr.execute(sql_command)
    sql_command = """INSERT INTO users VALUES ("UserTwo", "passwordTwo", 0, 0987, "Bill", "Gates");"""
    crsr.execute(sql_command)
    conn.commit()
    conn.close()

def ShowHome():
    root.show()
    loginform.destroy()

nextmenu.add_command(label='Log In', command=ShowLoginForm)
nextmenu.add_command(label='Query', command=ShowQueryForm)
nextmenu.add_command(label='Admin', command=ShowAdminForm)
nextmenu.add_command(label='Policy', command=ShowPolicy)
nextmenu.add_command(label='Create Test Database', command=DatabaseTest)
nextmenu.add_separator()
nextmenu.add_command(label='Exit', command=root.quit)

mainloop()