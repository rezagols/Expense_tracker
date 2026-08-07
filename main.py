from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import sqlite3
import tkinter.ttk as ttk

root = ctk.CTk()

root.title("Expense Tracker")

root.geometry("400x600")


#Project_Funcions

def add_expense():
    if title_entry.get() == "" and amount_entry.get() == "" and date_entry.get() == "" and category_combobox.get() == "Select Category":
            CTkMessagebox(
                title = "Error"
                ,message = "Please fill in all fields"
                ,icon = "Cancel"
            )
            return
    if title_entry.get() == "":
        CTkMessagebox(
            title = "Error"
            ,message = "Please fill the title!"
            ,icon = "Cancel"
        )
        return
    if amount_entry.get() == "":
            CTkMessagebox(
                title = "Error"
                ,message = "Please fill the amount!"
                ,icon = "Cancel"
            )
            return
    if category_combobox.get() == "Select category":
            CTkMessagebox(
                title = "Error"
                ,message = "Please select the category!"
                ,icon = "Cancel"
            )
            return
    if date_entry.get() == "":
            CTkMessagebox(
                title = "Error"
                ,message = "Please fill the date!"
                ,icon = "Cancel"
            )
            return

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





root.mainloop()