
import tkinter as tk

from tkinter import messagebox

from tkinter import ttk # Import ttk for themed widgets

from datetime import datetime

import pickle

import os

import csv



# --- Global Variables ---

root = tk.Tk()

logged_in_user = None



# Main frames for single-window design

login_frame_obj = None

signup_frame_obj = None

dashboard_frame_obj = None

add_expense_frame_obj = None

monthly_income_frame_obj = None

check_report_frame_obj = None



# Widgets that need to be accessed globally

username_entry = None

password_entry = None

full_name_entry = None

new_username_entry = None

new_password_entry = None

expense_desc_entry = None

expense_amount_entry = None

expense_category_entry = None

income_entry = None

current_income_label = None # Now part of monthly_income_frame_obj

report_text_widget = None # Now part of check_report_frame_obj

total_balance_label = None # Now part of dashboard_frame_obj



# --- Helper Functions ---

def show_frame(frame_to_show):

    for frame in [login_frame_obj, signup_frame_obj, dashboard_frame_obj,

                  add_expense_frame_obj, monthly_income_frame_obj, check_report_frame_obj]:

        if frame: # Check if frame object has been created

            frame.pack_forget()

    frame_to_show.pack(expand=True, fill=tk.BOTH)



def update_dashboard_summary():

    global logged_in_user, current_income_label, total_balance_label

    users = {}

    if os.path.exists("user_data.pkl"):

        with open("user_data.pkl", "rb") as f:

            users = pickle.load(f)



    user_data = users.get(logged_in_user, {})

    monthly_income = user_data.get('monthly_income', 0.0)

    expenses = user_data.get('expenses', [])



    total_expenses = sum(expense.get('amount', 0.0) for expense in expenses)

    remaining_balance = monthly_income - total_expenses



    # Update current_income_label if it exists and is part of the current view

    if current_income_label and current_income_label.winfo_exists():

        current_income_label.config(text=f"Current Monthly Income: ${monthly_income:,.2f}")

    

    # Update total_balance_label if it exists and is part of the current view

    if total_balance_label and total_balance_label.winfo_exists():

        total_balance_label.config(text=f"Current Balance: ${remaining_balance:,.2f}",

                                   foreground="green" if remaining_balance >= 0 else "red")



# --- Screen Management Functions ---



def create_login_screen():

    global login_frame_obj, username_entry, password_entry

    login_frame_obj = ttk.Frame(root, padding="15 15 15 15")



    ttk.Label(login_frame_obj, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    username_entry = ttk.Entry(login_frame_obj)

    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



    ttk.Label(login_frame_obj, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    password_entry = ttk.Entry(login_frame_obj, show="*")

    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



    ttk.Button(login_frame_obj, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

    ttk.Button(login_frame_obj, text="Signup", command=show_signup_screen).grid(row=3, column=0, columnspan=2)



def show_login_screen():

    if not login_frame_obj:

        create_login_screen()

    show_frame(login_frame_obj)



def create_signup_screen():

    global signup_frame_obj, full_name_entry, new_username_entry, new_password_entry

    signup_frame_obj = ttk.Frame(root, padding="15 15 15 15")



    ttk.Label(signup_frame_obj, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    full_name_entry = ttk.Entry(signup_frame_obj)

    full_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



    ttk.Label(signup_frame_obj, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    new_username_entry = ttk.Entry(signup_frame_obj)

    new_username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



    ttk.Label(signup_frame_obj, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")

    new_password_entry = ttk.Entry(signup_frame_obj, show="*")

    new_password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")



    ttk.Button(signup_frame_obj, text="Signup", command=signup).grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Button(signup_frame_obj, text="Back to Login", command=show_login_screen).grid(row=4, column=0, columnspan=2)

    tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)
   




def show_signup_screen():

    if not signup_frame_obj:

        create_signup_screen()

    show_frame(signup_frame_obj)



def create_dashboard_screen():

    global dashboard_frame_obj, total_balance_label

    dashboard_frame_obj = ttk.Frame(root, padding="15 15 15 15")



    ttk.Label(dashboard_frame_obj, text=f"Welcome, {logged_in_user}!", font=("Arial", 14, "bold")).pack(pady=10)

    

    total_balance_label = ttk.Label(dashboard_frame_obj, text="", font=("Arial", 12, "bold"))

    total_balance_label.pack(pady=5)



    ttk.Button(dashboard_frame_obj, text="Add Expense", command=show_add_expense_screen).pack(fill=tk.X, pady=5)

    ttk.Button(dashboard_frame_obj, text="Monthly Income", command=show_monthly_income_screen).pack(fill=tk.X, pady=5)

    ttk.Button(dashboard_frame_obj, text="Generate CSV", command=generate_csv).pack(fill=tk.X, pady=5)

    ttk.Button(dashboard_frame_obj, text="Check Report", command=show_check_report_screen).pack(fill=tk.X, pady=5)

    ttk.Button(dashboard_frame_obj, text="Logout", command=logout).pack(pady=15)



def show_dashboard_screen():

    if not dashboard_frame_obj:

        create_dashboard_screen()

    show_frame(dashboard_frame_obj)

    update_dashboard_summary() # Initial update of dashboard summary



# --- Functionality Functions (now creating/showing frames) ---



def create_add_expense_screen():

    global add_expense_frame_obj, expense_desc_entry, expense_amount_entry, expense_category_entry

    add_expense_frame_obj = ttk.Frame(root, padding="10 10 10 10")



    ttk.Label(add_expense_frame_obj, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    expense_desc_entry = ttk.Entry(add_expense_frame_obj)

    expense_desc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



    ttk.Label(add_expense_frame_obj, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    expense_amount_entry = ttk.Entry(add_expense_frame_obj)

    expense_amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")



    ttk.Label(add_expense_frame_obj, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky="w")

    expense_category_entry = ttk.Entry(add_expense_frame_obj)

    expense_category_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")



    ttk.Button(add_expense_frame_obj, text="Save Expense", command=save_expense).grid(row=3, columnspan=2, pady=15)

    ttk.Button(add_expense_frame_obj, text="Back to Dashboard", command=show_dashboard_screen).grid(row=4, columnspan=2, pady=5)



def show_add_expense_screen():

    if not add_expense_frame_obj:

        create_add_expense_screen()

    show_frame(add_expense_frame_obj)

    # Clear fields when showing

    expense_desc_entry.delete(0, tk.END)

    expense_amount_entry.delete(0, tk.END)

    expense_category_entry.delete(0, tk.END)



def create_monthly_income_screen():

    global monthly_income_frame_obj, income_entry, current_income_label

    monthly_income_frame_obj = ttk.Frame(root, padding="10 10 10 10")



    ttk.Label(monthly_income_frame_obj, text="Monthly Income:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

    income_entry = ttk.Entry(monthly_income_frame_obj)

    income_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



    ttk.Button(monthly_income_frame_obj, text="Save Income", command=save_income).grid(row=1, columnspan=2, pady=15)



    current_income_label = ttk.Label(monthly_income_frame_obj, text="", font=("Arial", 10, "italic"))

    current_income_label.grid(row=2, columnspan=2, pady=5)

    ttk.Button(monthly_income_frame_obj, text="Back to Dashboard", command=show_dashboard_screen).grid(row=3, columnspan=2, pady=5)



def show_monthly_income_screen():

    if not monthly_income_frame_obj:

        create_monthly_income_screen()

    show_frame(monthly_income_frame_obj)

    load_and_display_income() # Update income display

    income_entry.delete(0, tk.END) # Clear entry field



def create_check_report_screen():

    global check_report_frame_obj, report_text_widget

    check_report_frame_obj = ttk.Frame(root, padding="10 10 10 10")



    ttk.Label(check_report_frame_obj, text="--- Financial Summary ---", font=("Arial", 14, "bold")).pack(pady=5)

    

    # Labels for summary will be updated dynamically

    ttk.Label(check_report_frame_obj, text="", font=("Arial", 11)).pack(anchor=tk.W, name="report_income_label")

    ttk.Label(check_report_frame_obj, text="", font=("Arial", 11)).pack(anchor=tk.W, name="report_expenses_label")

    ttk.Label(check_report_frame_obj, text="", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10), name="report_balance_label")



    ttk.Label(check_report_frame_obj, text="--- Expenses by Category ---", font=("Arial", 14, "bold")).pack(pady=5)



    text_frame = ttk.Frame(check_report_frame_obj)

    text_frame.pack(expand=True, fill=tk.BOTH)



    report_text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15, width=40, font=("Arial", 10))

    report_text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    

    scrollbar = ttk.Scrollbar(text_frame, command=report_text_widget.yview)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    report_text_widget.config(yscrollcommand=scrollbar.set)

    report_text_widget.config(state=tk.DISABLED) # Make it read-only



    ttk.Button(check_report_frame_obj, text="Back to Dashboard", command=show_dashboard_screen).pack(pady=10)



def show_check_report_screen():

    if not check_report_frame_obj:

        create_check_report_screen()

    show_frame(check_report_frame_obj)

    # Update report content

    users = {}

    if os.path.exists("user_data.pkl"):

        with open("user_data.pkl", "rb") as f:

            users = pickle.load(f)



    user_data = users.get(logged_in_user, {})

    monthly_income = user_data.get('monthly_income', 0.0)

    expenses = user_data.get('expenses', [])



    total_expenses = sum(expense.get('amount', 0.0) for expense in expenses)

    remaining_balance = monthly_income - total_expenses



    # Update summary labels

    check_report_frame_obj.nametowidget("report_income_label").config(text=f"Monthly Income: ${monthly_income:,.2f}")

    check_report_frame_obj.nametowidget("report_expenses_label").config(text=f"Total Expenses: ${total_expenses:,.2f}")

    check_report_frame_obj.nametowidget("report_balance_label").config(text=f"Remaining Balance: ${remaining_balance:,.2f}",

                                                                       foreground="green" if remaining_balance >= 0 else "red")



    # Update expense breakdown

    report_text_widget.config(state=tk.NORMAL) # Enable to clear and insert

    report_text_widget.delete(1.0, tk.END)

    expenses_by_category = {}

    for expense in expenses:

        amount = expense.get('amount', 0.0)

        category = expense.get('category', 'Uncategorized')

        expenses_by_category[category] = expenses_by_category.get(category, 0.0) + amount

    

    if expenses_by_category:

        for category, amount in expenses_by_category.items():

            report_text_widget.insert(tk.END, f"{category}: ${amount:,.2f}\n")

    else:

        report_text_widget.insert(tk.END, "No expenses recorded yet.\n")

    report_text_widget.config(state=tk.DISABLED) # Make it read-only





def generate_csv():

    global logged_in_user

    users = {}

    if os.path.exists("user_data.pkl"):

        with open("user_data.pkl", "rb") as f:

            users = pickle.load(f)




def signup():
    global logged_in_user
    full_name = full_name_entry.get().strip()
    username = new_username_entry.get().strip()
    password = new_password_entry.get().strip()


    user_data = users.get(logged_in_user)

    if not user_data or not user_data.get("expenses"):

        messagebox.showinfo("Info", "No expenses to export.")

        return



    # Ensure 'data' directory exists

    if not os.path.exists("data"):


        os.makedirs("data")



    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = os.path.join("data", f"expenses_{logged_in_user}_{timestamp}.csv")

    users = {}
    if os.path.exists("user_data.pkl"):
        with open("user_data.pkl", "rb") as f:
            users = pickle.load(f)

    if username in users and users[username]["password"] == password:
        logged_in_user = username
        with open("session.pkl", "wb") as f:
            pickle.dump(logged_in_user, f)
        show_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

    messagebox.showinfo("Success", "Signup successful! ")
    
    





    try:

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:

            writer = csv.writer(csvfile)



            # Write header

            writer.writerow(['Date', 'Description', 'Category', 'Amount'])



            # Write expense data

            for expense in user_data["expenses"]:

                writer.writerow([

                    expense.get('date', 'N/A'),

                    expense.get('description', 'N/A'),

                    expense.get('category', 'N/A'),

                    expense.get('amount', 0.0)

                ])

        

        messagebox.showinfo("Success", f"CSV report generated successfully!\n\nFile saved at: {file_path}")



    except IOError as e:

        messagebox.showerror("Error", f"Could not write to file: {e}")



def login():

    global logged_in_user

    username = username_entry.get().strip()

    password = password_entry.get().strip()



    if not username or not password:

        messagebox.showerror("Error", "Please enter username and password.")

        return



    users = {}

    if os.path.exists("user_data.pkl"):

        with open("user_data.pkl", "rb") as f:

            users = pickle.load(f)



    if username in users and users[username]["password"] == password:

        logged_in_user = username

        with open("session.pkl", "wb") as f:

            pickle.dump(logged_in_user, f)

        show_dashboard_screen()

    else:

        messagebox.showerror("Error", "Invalid username or password.")



def signup():

    full_name = full_name_entry.get().strip()

    username = new_username_entry.get().strip()

    password = new_password_entry.get().strip()



    if not full_name.replace(' ', '').isalpha() or not username or not password:

        messagebox.showerror("Error", "Invalid input. Please check your details.")

        return



    users = {}

    if os.path.exists("user_data.pkl"):

        with open("user_data.pkl", "rb") as f:

            users = pickle.load(f)



    if username in users:

        messagebox.showerror("Error", "Username already exists.")

        return



    users[username] = {"password": password, "full_name": full_name, "expenses": [], "monthly_income": 0.0}



    with open("user_data.pkl", "wb") as f:

        pickle.dump(users, f)



    messagebox.showinfo("Success", "Signup successful! Please login.")

    show_login_screen()



def save_expense():

    description = expense_desc_entry.get().strip()

    amount_str = expense_amount_entry.get().strip()

    category = expense_category_entry.get().strip()



    if not description or not amount_str or not category:

        messagebox.showerror("Error", "All fields are required.") # Removed parent=expense_window

        return



    try:

        amount = float(amount_str)

    except ValueError:

        messagebox.showerror("Error", "Amount must be a valid number.") # Removed parent=expense_window

        return



    users = {}

    if os.path.exists("user_data.pkl"):

        with open("user_data.pkl", "rb") as f:

            users = pickle.load(f)



    # Ensure the user has an 'expenses' list

    if 'expenses' not in users[logged_in_user]:

        users[logged_in_user]['expenses'] = []



    new_expense = {

        "description": description,

        "amount": amount,

        "category": category,

        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }

    users[logged_in_user]["expenses"].append(new_expense)



    with open("user_data.pkl", "wb") as f:

        pickle.dump(users, f)



    messagebox.showinfo("Success", "Expense added successfully!") # Removed parent=expense_window

    show_dashboard_screen() # Return to dashboard

    update_dashboard_summary() # Update dashboard balance



def logout():

    global logged_in_user

    logged_in_user = None

    if os.path.exists("session.pkl"):

        os.remove("session.pkl")

    show_login_screen()



def create_dummy_data():

    users = {

        "testuser": {"password": "testpassword", "full_name": "Test User", "expenses": [], "monthly_income": 5000.0},

        "john": {"password": "doe", "full_name": "John Doe", "expenses": [], "monthly_income": 7500.50}

    }

    with open("user_data.pkl", "wb") as f:

        pickle.dump(users, f)



# --- Main Application Logic ---



if __name__ == "__main__":

    root.title("Finance Manager")

    root.geometry("500x600") # Adjusted main window size

    root.option_add("*Font", "Arial 10") # Set a default font for all widgets



    # Initialize all frames (but don't pack them yet)

    create_login_screen()

    create_signup_screen()

    create_dashboard_screen()

    create_add_expense_screen()

    create_monthly_income_screen()

    create_check_report_screen()



    # Check for a saved session

    if os.path.exists("session.pkl"):

        with open("session.pkl", "rb") as f:

            logged_in_user = pickle.load(f)

    

    if logged_in_user:

        show_dashboard_screen()

    else:

        show_login_screen()



    root.mainloop()


