import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Text, Tk
import sqlite3
import webbrowser
import urllib.request
import csv
import sys

from datetime import datetime, date, timedelta

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

##
global userQuery
userQuery = ""
global queries
queries = []
##

def ShowPolicy():
    webbrowser.open_new(r"https://github.com/AdminTeamUSW2019/Admin---GUI/blob/master/PolicyV1.md")

def updateLog():
    now = datetime.now()
    now = now.strftime("%m/%d/%Y, %H:%M:%S")
    with open("Userlog.txt", "a") as txtUserlog:
            txtUserlog.write("User: " + USERNAME.get() + "\n")
            txtUserlog.write(now)
            txtUserlog.write("**********")
            txtUserlog.write("\n")
            txtUserlog.close()

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
                updateLog()
                cursor2.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ? AND Accesslevel <> 1", (USERNAME.get(), PASSWORD.get()))
                if cursor2.fetchone() is not None:
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
                    new_query_menu()
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
            updateLog()
            cursor2.execute("SELECT * FROM `users` WHERE `username` = ? AND `password` = ? AND Accesslevel <> 1", (USERNAME.get(), PASSWORD.get()))
            if cursor2.fetchone() is not None:
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
                new_query_menu()
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

def new_query_menu():
    global new_query_screen
    global new_explanation_textbox
    global new_query_combobox

    new_query_screen = Tk()
    new_query_screen.title("Submit New Query")
    new_query_screen.geometry("800x600")
    new_query_screen.configure(background="grey")
    new_query_screen.resizable(0, 0)

    # new_query_screen.grid_rowconfigure(0, weight = 1)
    # new_query_screen.grid_rowconfigure(1, weight=1)
    # new_query_screen.grid_rowconfigure(2, weight=1)
    new_query_screen.grid_columnconfigure(0, weight=1)
    new_query_screen.grid_columnconfigure(1, weight=1)
    new_query_screen.grid_columnconfigure(2, weight=1)

    ##the query
    new_query_label = Label(new_query_screen, text="Type of query: ", font=("Helvetica", 16), bg="white",
                                    fg="black")
    new_query_label.grid(row=0, column=1)

    new_query_combobox = ttk.Combobox(new_query_screen,
                                      values=["Technical", "Software", "Hardware", "Request technical support"])
    new_query_combobox.grid(row=0, column=2, pady=20, padx=5)
    new_query_combobox.config(width=30)
    new_query_combobox.current(1)

    new_explanation_label = Label(new_query_screen, text="Describe the query: ", font=("Helvetica", 16))
    new_explanation_label.grid(row=2, column=1)

    new_explanation_textbox = Text(new_query_screen, height=20, width=60)
    new_explanation_textbox.grid(row=3, column=2, pady=10, padx=5)

    new_query_exit = Button(new_query_screen, text="Close", bg="white", fg="black", command=closeQueryScreen)
    new_query_exit.grid(row=5, column=1, pady=5, padx=5)
    new_query_exit.config(height=2, width=10)

    new_query_submit = Button(new_query_screen, text="Submit", bg="white", fg="black", command=writeQueryToFile)
    new_query_submit.grid(row=5, column=3)
    new_query_submit.bind("<Return>", writeQueryToFile)

    button_save_toTextFile = Button(new_query_screen, text="Read&Save", bg="white", fg="black",
                                    command=readFromFileAndSaveToList)
    button_save_toTextFile.grid(row=5, column=2)
    new_query_submit.bind("<Return>", readFromFileAndSaveToList)

    printStudd = Button(new_query_screen, text="PrintStuff", bg="white", fg="black", command=printAllListItems)
    printStudd.grid(row=6, column=2)
    new_query_screen.mainloop()


# def character_limit(entry_text):
#     if len(entry_text.get()) >
# query form commands

def closeQueryScreen():
    new_query_screen.quit()
    new_query_screen.destroy()


def databaseConnect():
    conn = sqlite3.connect("queries.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `query` (query_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT FULL, \
                         username TEXT, submitted_Query TEXT)")
    cursor.execute("SELECT * FROM `query` WHERE `username` = 'user' AND `submitted_Query` = 'query'")

    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `query` (username, submitted_Query) VALUES('user', 'query')")
        cursor.commit()


def writeQueryToFile(event=None):
    userQuery = new_explanation_textbox.get('1.0', END)
    messagebox.showinfo("Title", userQuery)
    print(userQuery)
    if userQuery == "\n":
        new_query_result = Label(new_query_screen, text="", font=("Helvetica", 16))
        new_query_result.grid(row=5, column=2)
        new_query_result.config(text="Please enter a query!")
    else:
        with open("userQueries.txt", "a") as txtUserQuery:
            txtUserQuery.write("Type of issue: {} \n".format(new_query_combobox.get()))
            txtUserQuery.write(userQuery)
            txtUserQuery.write("**********")
            txtUserQuery.write("\n")
            txtUserQuery.close()

def readFromFileAndSaveToList():
    listQuery = ""
    with open("userQueries.txt", "r") as txtUserQuery:
        # queries = txtUserQuery.readlines()
        for returnedLine in txtUserQuery:
            ##print(returnedLine)
            mylist.insert(returnedLine)
            if returnedLine == "**********\n":
                listQuery += returnedLine
                queries.append(listQuery)
                listQuery = ""
            else:
                listQuery += returnedLine
        txtUserQuery.close()

        # try:
        #     while True:
        #         returnedLine = txtUserQuery.readline()
        #         while returnedLine != "**********":
        #             listQuery += returnedLine
        #             returnedLine = txtUserQuery.readline()
        #         queries.append(listQuery)


def printAllListItems():
    # with open("Testing.txt", "a") as txtUserQuery:
        for query in queries:
            print(query)
            print("hello world")
        #
        #     print(query)
        # txtUserQuery.close()

##new_query_menu()

# def submitQueryToSQL():
#     global query_id
#     databaseConnect()
#
#     if len(userQuery) <= 50:
#         new_query_result.config(text="Please write at least 50 characters for your query!", fg="red")
#     else:
#         cursor.execute("S")

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
    global mylist
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
    listQuery = ""
    with open("userQueries.txt", "r") as txtUserQuery:
        # queries = txtUserQuery.readlines()
        for returnedLine in txtUserQuery:
            ##print(returnedLine)
            mylist.insert(END, returnedLine)
            if returnedLine == "**********\n":
                listQuery += returnedLine
                queries.append(listQuery)
                listQuery = ""
            else:
                listQuery += returnedLine
        txtUserQuery.close()
    ##for line in range(30):  
    ##    mylist.insert(END, "Number " + str(line))  
    mylist.pack( fill=BOTH )  
    sb.config( command = mylist.yview )  

    f3 = tk.Frame(notebook, bg='green', width=1000, height=500)
    notebook.add(f1, text=f'{"Dashboard": ^20s}')
    notebook.add(f2, text=f'{"Queries": ^24s}')
    notebook.add(f3, text=f'{"User Log": ^23s}')
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
    accesslevel VARCHAR(5), 
    pin INT,
    fname VARCHAR(20),  
    lname VARCHAR(30));"""

    crsr.execute(sql_command)

    sql_command = """CREATE TABLE registeredIP (username VARCHAR(30), IPaddress VARCHAR(20));"""
    crsr.execute(sql_command)

    sql_command = """INSERT INTO users VALUES ("UserOne", "password", 2, 1234, "Bob", "Jones");"""
    crsr.execute(sql_command)
    sql_command = """INSERT INTO users VALUES ("UserTwo", "passwordTwo", 1, 0987, "Bill", "Gates");"""
    crsr.execute(sql_command)
    conn.commit()
    conn.close()

def ShowHome():
    root.show()
    loginform.destroy()

nextmenu.add_command(label='Log In', command=ShowLoginForm)
nextmenu.add_command(label='Query', command=new_query_menu)
nextmenu.add_command(label='Admin', command=ShowAdminForm)
nextmenu.add_command(label='Policy', command=ShowPolicy)
nextmenu.add_command(label='Create Test Database', command=DatabaseTest)
nextmenu.add_separator()
nextmenu.add_command(label='Exit', command=root.quit)

mainloop()