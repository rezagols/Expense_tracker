from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import sqlite3
import tkinter.ttk as ttk

root = ctk.CTk()

root.title("Expense Tracker")

root.geometry("400x770")

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

editing_expense_id = None
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

    try :
        amount = float(amount)
    except ValueError :
        CTkMessagebox(title = "Invalid amount"
            , message = "Please enter a valid number for the amount!"
            , icon = "cancel")
        return
    if amount <= 0 :
            CTkMessagebox(title = "Invalid amount" 
                        , message = "Amount must be greater than zero!"
                        , icon = "cancel")
            return

    cursor.execute("""
INSERT INTO expenses (title , amount , category , date)
values(? , ? , ? , ?)
""" , (title , amount , category , date))

    conn.commit()

    expense_tree.insert("" 
                        , "end" 
                        ,iid = str(cursor.lastrowid)
                        , values = (len(expense_tree.get_children()) + 1 
                        , title , amount , category , date))

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

    for number , expense in enumerate(expenses , start = 1):
        expense_id , title , amount , category , date = expense
        expense_tree.insert("" 
                            , "end" 
                            ,iid = str(expense_id) 
                            , values = [number , title , amount , category , date] )

def update_row_numbers():
    items = expense_tree.get_children()

    for number , item in enumerate(items , start = 1) :
        values = list(expense_tree.item(item , "values"))
        values[0] = number

        expense_tree.item(item , values = values)

def select_expense(event):
    selected_item = expense_tree.selection()

    if selected_item :
        item = selected_item[0]

        values = expense_tree.item(item , "values")

        row_number = values[0]

        selected_row_label.configure(text = str(row_number))

def cancel_selection():
    selected_item = expense_tree.selection()

    if not selected_item :
        CTkMessagebox(title = "Missing selection" ,
                message = "No expense is selected!" ,
                icon = "cancel" ,
                justify = "center")
        return

    expense_tree.selection_remove(expense_tree.selection())
    selected_row_label.configure(text = "-")

def edit_expense():
    global editing_expense_id

    selected_item = expense_tree.selection()

    if not selected_item :
        CTkMessagebox(title = "Missing selection" 
                    , message = "Please select an expense to edit!"
                    , icon = "cancel")
        return

    editing_expense_id = int(selected_item[0])

    cursor.execute("SELECT title , amount , category , date FROM expenses WHERE id = ?" , (editing_expense_id,))

    expense = cursor.fetchone()

    title , amount , category , date = expense

    title_entry.delete(0 , "end")
    title_entry.insert(0 , title)

    amount_entry.delete(0 , "end")
    amount_entry.insert(0 , amount)

    category_combobox.set(category)

    date_entry.delete(0 , "end")
    date_entry.insert(0 , date)

    edit_status_label.configure(text = "Editing expense ...")

def update_expense():
        global editing_expense_id

        if editing_expense_id is None :
            CTkMessagebox(
                title = "Missing selection"
                , text = "Please select an expense to edit!"
                , icon = "cancel"
            )
            return
        title = title_entry.get()
        amount = amount_entry.get()
        category = category_combobox.get()
        date = date_entry.get()

        try :
                amount = float(amount)
        except ValueError :
            CTkMessagebox(title = "Invalid amount"
                        , message = "Pleasr enter a valid number for the amount!"
                        , icon = "cancel")
            return
        if amount <= 0 :
            CTkMessagebox(title = "Invalid amount" 
                        , message = "Amount must be greater than zero!"
                        , icon = "cancel")
            return


        if title == "" or amount == "" or date == "" :
            CTkMessagebox(title = "Missing information" 
                        , text = "Please fill in all fields!" 
                        , icon = "cancel" , justify = "center")
            return

        if category == "select category" :
            CTkMessagebox(title = "Missing information" 
                        , text = "Please select the category!" 
                        , icon = "cancel" , justify = "center")
            return

        cursor.execute("""UPDATE expenses SET title = ?
        , amount = ? , category = ? , date = ? 
        WHERE id = ?""" , (title , amount , category , date , editing_expense_id))

        conn.commit()

        current_values = expense_tree.item(str(editing_expense_id) , "values")

        expense_tree.item(str(editing_expense_id) , values = (current_values[0] , title , amount , category , date))
        
        CTkMessagebox(
            title = "Success" , message = "Expense updated successfully!",
            justify = "center"
        )

        edit_status_label.configure(text = "")

        title_entry.delete(0 , "end")
        amount_entry.delete(0 , "end")
        category_combobox.set("Select category")
        date_entry.delete(0 , "end")
        
        expense_tree.selection_remove(expense_tree.selection())

        editing_expense_id = None

def cancel_edit():
    global editing_expense_id

    if editing_expense_id is None : 
        CTkMessagebox(
            title = "No edit"
            , text = "There is no expense being edited!"
            , icon = "cancel"
        )
        return

    edit_status_label.configure(text = "")

    title_entry.delete(0 , "end")
    amount_entry.delete(0 , "end")
    category_combobox.set("Select category")
    date_entry.delete(0 , "end")

    editing_expense_id = None

def delete_expense():
    selected_item = expense_tree.selection()

    if not selected_item :
        CTkMessagebox(
            title = "Missing selection"
            , message = "Please select an expense to delete!"
            , icon = "cancel"
        )
        return

    expense_id = int(selected_item[0])

    cursor.execute("DELETE FROM expenses WHERE id = ?" , (expense_id,))

    conn.commit()

    expense_tree.delete(selected_item[0])
    update_row_numbers()
    selected_row_label.configure(text = "-")

    CTkMessagebox(title = "Success" 
                , message = "Expense deleted successfully!" 
                , justify = "center")

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


add_label = ctk.CTkLabel(root , text = "Add expense : ")
add_label.grid(row = 4 , column = 0 , padx = 10 , pady = 10)
add_button = ctk.CTkButton(root , text = "Add expense" , command = add_expense)
add_button.grid(row = 4 , column = 1 , padx = 10 , pady = 10 )


select_label = ctk.CTkLabel(root , text = "Selected row :")
select_label.grid(row = 7 , column = 0 , padx = 10 , pady = 10)
selected_row_label = ctk.CTkLabel(root , text = "-")
selected_row_label.grid(row = 7 , column = 1 , padx = 10 , pady = 10)


cancel_label = ctk.CTkLabel(root , text = "Cancel selection row : ")
cancel_label.grid(row = 8 , column = 0 , padx = 10 , pady = 10)
cancel_button = ctk.CTkButton(root , text = "Cancel selection" , command = cancel_selection)
cancel_button.grid(row = 8 , column = 1 , padx = 10 , pady = 10)


delete_label = ctk.CTkLabel(root , text = "Delete expense : ")
delete_label.grid(row = 9 , column = 0 , padx = 10 , pady = 10)
delete_button = ctk.CTkButton(root , text = "Delete expense" , command = delete_expense)
delete_button.grid(row = 9 , column = 1 , padx = 10 , pady = 10)


edit_label = ctk.CTkLabel(root , text = "Edit expense : ")
edit_label.grid(row = 10 , column = 0 , padx = 10 , pady = 10)
edit_button = ctk.CTkButton(root , text = "Edit expense" , command = edit_expense)
edit_button.grid(row = 10 , column = 1 , padx = 10 , pady = 10)


update_label = ctk.CTkLabel(root , text = "Update expense : ")
update_label.grid(row = 11 , column = 0 , padx = 10 , pady = 10)
update_button = ctk.CTkButton(root , text = "Update expense" , command = update_expense)
update_button.grid(row = 11 , column = 1 , padx = 10 , pady = 10)


cancel_edit_label = ctk.CTkLabel(root , text = "Cancel edit : ")
cancel_edit_label.grid(row = 12 , column = 0 , padx = 10 , pady = 10)
cancel_edit_button = ctk.CTkButton(root , text = "Cancel edit" , command = cancel_edit)
cancel_edit_button.grid(row = 12 , column = 1 , padx = 10 , pady = 10)


edit_status_label = ctk.CTkLabel(root , text = "")
edit_status_label.grid(row = 6 , column = 0 , columnspan = 2 , padx = 10 , pady = 5)

#Treeview
columns = ("row" , "Title" , "Amount" , "Category" , "Date")


expense_tree = ttk.Treeview(root , columns = columns , show = "headings")
expense_tree.heading("row" , text = "row")
expense_tree.heading("Title" , text = "Title")
expense_tree.heading("Amount" , text = "Amount")
expense_tree.heading("Category" , text = "Category")
expense_tree.heading("Date" , text = "Date")


expense_tree.column("row" , width = 40)
expense_tree.column("Title" , width = 90)
expense_tree.column("Amount" , width =70)
expense_tree.column("Category" , width = 100)
expense_tree.column("Date" , width = 90)


expense_tree.grid(row = 5 , columnspan = 2 ,  padx = 10 , pady = 20 , sticky = "W")
expense_tree.bind("<<TreeviewSelect>>" , select_expense)

show_expenses()

root.mainloop()