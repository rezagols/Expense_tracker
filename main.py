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


#Project_widgets

title_label = ctk.CTkLabel(root , text = "Enter a title : ")
title_entry = ctk.CTkEntry(root)
title_label.grid(row = 0 , column = 0  , padx = 10 , pady = 10)
title_entry.grid(row = 0 , column = 1 , padx = 10 , pady = 10)


amount_label = ctk.CTkLabel(root , text = "Enter amount : ")
amount_entry = ctk.CTkEntry(root)
amount_label.grid(row = 1 , column = 0 , padx = 10 , pady = 10)
amount_entry.grid(row = 1 , column = 1 , padx = 10 , pady = 10)

category_label = ctk.CTkLabel(root , text = "Choose category : ")
category_combobox = ctk.CTkComboBox(root , values = [
    "Food" 
    , "Transport"
    , "Shopping"
    , "Entertainment"
    , "Other"]
)
category_combobox.grid(row = 2 , column = 1 , padx = 10 , pady = 10 )
category_combobox.set("Select category")


date_label = ctk.CTkLabel(root , text = "Enter a date : ")
date_entry = ctk.CTkEntry(root)
date_label.grid(row = 3 , column = 0 , padx = 10 , pady = 10)
date_entry.grid(row = 3 , column = 1 , padx = 10 , pady = 10)


add_button = ctk.CTkButton(root , text = "Add expense" , command = add_expense)
add_button.grid(row = 4 , column = 1 , padx = 10 , pady = 10)


root.mainloop()