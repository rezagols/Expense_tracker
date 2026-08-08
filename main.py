from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import sqlite3
import tkinter.ttk as ttk

root = ctk.CTk()

root.title("Expense Tracker")

root.geometry("400x600")

#Project_database

conn = sqlite3.connect("expense.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
id INTEGER PRIMARY KEY AUTOINCREMENT ,
title TEXT,
amount REAL,
category TEXT,
date TEXT
)
""")

conn.commit()

#Project_Funcions

def add_expense():
    if title_entry.get() == "" or amount_entry.get() == "" or date_entry.get() == "" :
            CTkMessagebox(
                title = "Missing information"
                , message = "Please fill in all fields"
                , icon = "cancel"
                , justify = "center"
            )
            return

    if category_combobox.get() == "Select category":
            CTkMessagebox(
                title = "Missing information"
                , message = "Please select the category!"
                , icon = "cancel"
                , justify = "center"
            )
            return

    title = title_entry.get()
    amount = amount_entry.get()
    category = category_combobox.get()
    date = date_entry.get()

    cursor.execute("""
INSERT INTO expenses (title , amount , category , date)
values(? , ? , ? , ?)
""" , (title , amount , category , date))

    conn.commit()

    expense_tree.insert("" , "end" , values = (cursor.lastrowid , title , amount , category , date))

    CTkMessagebox(
        title = "Success" ,
        message = "Expense added successfully!" ,
        justify = "center"
    )

    title_entry.delete(0 , "end")
    amount_entry.delete(0, "end")
    date_entry.delete(0 , "end")
    category_combobox.set("Select category")

def show_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    for expense in expenses :
        expense_tree.insert("" , "end" , values = expense)


#Project_widgets

title_label = ctk.CTkLabel(root , text = "Enter a title : " , width = 20)
title_entry = ctk.CTkEntry(root)
title_label.grid(row = 0 , column = 0  , padx = 10 , pady = 10 )
title_entry.grid(row = 0 , column = 1 , padx = 10 , pady = 10 )


amount_label = ctk.CTkLabel(root , text = "Enter amount : " , width =20)
amount_entry = ctk.CTkEntry(root)
amount_label.grid(row = 1 , column = 0 , padx = 10 , pady = 10 )
amount_entry.grid(row = 1 , column = 1 , padx = 10 , pady = 10 )

category_label = ctk.CTkLabel(root , text = "Choose category : " , width = 20)
category_combobox = ctk.CTkComboBox(root , values = [
    "Food" 
    , "Transport"
    , "Shopping"
    , "Entertainment"
    , "Other"]
)
category_label.grid(row = 2 , column = 0 , padx =10 , pady = 10)
category_combobox.grid(row = 2 , column = 1 , padx = 10 , pady = 10 )
category_combobox.set("Select category")


date_label = ctk.CTkLabel(root , text = "Enter a date : " , width = 20)
date_entry = ctk.CTkEntry(root)
date_label.grid(row = 3 , column = 0 , padx = 10 , pady = 10 )
date_entry.grid(row = 3 , column = 1 , padx = 10 , pady = 10 )


add_button = ctk.CTkButton(root , text = "Add expense" , command = add_expense)
add_button.grid(row = 4 , column = 1 , padx = 10 , pady = 10 )

#Treeview
columns = ("ID" , "Title" , "Amount" , "Category" , "Date")

expense_tree = ttk.Treeview(root , columns = columns , show = "headings")
expense_tree.heading("ID" , text = "ID")
expense_tree.heading("Title" , text = "Title")
expense_tree.heading("Amount" , text = "Amount")
expense_tree.heading("Category" , text = "Category")
expense_tree.heading("Date" , text = "Date")

expense_tree.column("ID" , width = 40)
expense_tree.column("Title" , width = 90)
expense_tree.column("Amount" , width =70)
expense_tree.column("Category" , width = 100)
expense_tree.column("Date" , width = 90)

expense_tree.grid(row = 5 , columnspan = 2 ,  padx = 10 , pady = 20 , sticky = "W")

show_expenses()

root.mainloop()