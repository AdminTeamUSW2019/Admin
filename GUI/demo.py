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

##testing
global typeOfQuery
typeOfQuery = []
global descriptionOfQuery
descriptionOfQuery = []

##testing

##
global userQuery
userQuery = ""
global queries
queries = []
##
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
            typeOfQuery.append(new_query_combobox.get())
            descriptionOfQuery.append(userQuery)
            txtUserQuery.write(userQuery)
            txtUserQuery.write("**********")
            txtUserQuery.write("\n")
            txtUserQuery.close()

def readFromFileAndSaveToList():
    listQuery = ""
    with open("userQueries.txt", "r") as txtUserQuery:
        # queries = txtUserQuery.readlines()
        for returnedLine in txtUserQuery:
            # print(returnedLine)
            # mylist.insert(returnedLine)
            if returnedLine == "**********\n":
                listQuery += returnedLine
                queries.append(listQuery)
                listQuery = ""
            else:
                listQuery += returnedLine
        txtUserQuery.close()

##testing adding to multiple lists




def printAllListItems():
    # with open("Testing.txt", "a") as txtUserQuery:
        for query in queries:
            print(query)
            print("hello world")

        with open("testing.csv", "w") as test_file:
            writ = csv.writer(test_file)
            writ.writerows(zip(typeOfQuery, descriptionOfQuery))


new_query_menu()
##Nick's Part
