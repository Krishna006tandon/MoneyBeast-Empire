
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pickle
import os

# --- Global Variables ---
root = tk.Tk()
logged_in_user = None

# Widgets that need to be accessed globally
username_entry = None
password_entry = None
full_name_entry = None
new_username_entry = None
new_password_entry = None
expense_window = None
expense_desc_entry = None
expense_amount_entry = None
expense_category_entry = None

# --- Screen Management Functions ---

def show_login_screen():
    global username_entry, password_entry
    clear_screen()

    login_frame = tk.Frame(root)
    login_frame.pack(pady=20)

    tk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(login_frame, text="Signup", command=show_signup_screen).grid(row=3, column=0, columnspan=2)

def show_signup_screen():
    global full_name_entry, new_username_entry, new_password_entry
    clear_screen()

    signup_frame = tk.Frame(root)
    signup_frame.pack(pady=20)

    tk.Label(signup_frame, text="Full Name:").grid(row=0, column=0, padx=10, pady=5)
    full_name_entry = tk.Entry(signup_frame)
    full_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(signup_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
    new_username_entry = tk.Entry(signup_frame)
    new_username_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(signup_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
    new_password_entry = tk.Entry(signup_frame, show="*")
    new_password_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(signup_frame, text="Signup", command=signup).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(signup_frame, text="Back to Login", command=show_login_screen).grid(row=4, column=0, columnspan=2)

def show_dashboard():
    clear_screen()

    dashboard_frame = tk.Frame(root)
    dashboard_frame.pack(pady=20)

    tk.Label(dashboard_frame, text=f"Welcome, {logged_in_user}!").pack(pady=10)
    tk.Button(dashboard_frame, text="Add Expense", command=add_expense).pack(fill=tk.X, pady=2)
    tk.Button(dashboard_frame, text="Monthly Income", command=monthly_income).pack(fill=tk.X, pady=2)
    tk.Button(dashboard_frame, text="Generate CSV", command=generate_csv).pack(fill=tk.X, pady=2)
    tk.Button(dashboard_frame, text="Check Report", command=check_report).pack(fill=tk.X, pady=2)
    tk.Button(dashboard_frame, text="Logout", command=logout).pack(pady=10)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# --- Functionality Functions ---

def add_expense():
    global expense_window, expense_desc_entry, expense_amount_entry, expense_category_entry
    expense_window = tk.Toplevel(root)
    expense_window.title("Add Expense")
    expense_window.geometry("350x200")

    frame = tk.Frame(expense_window, padx=10, pady=10)
    frame.pack(expand=True)

    tk.Label(frame, text="Description:").grid(row=0, column=0, sticky="w", pady=2)
    expense_desc_entry = tk.Entry(frame)
    expense_desc_entry.grid(row=0, column=1, pady=2)

    tk.Label(frame, text="Amount:").grid(row=1, column=0, sticky="w", pady=2)
    expense_amount_entry = tk.Entry(frame)
    expense_amount_entry.grid(row=1, column=1, pady=2)

    tk.Label(frame, text="Category:").grid(row=2, column=0, sticky="w", pady=2)
    expense_category_entry = tk.Entry(frame)
    expense_category_entry.grid(row=2, column=1, pady=2)

    tk.Button(frame, text="Save Expense", command=save_expense).grid(row=3, columnspan=2, pady=10)

def monthly_income():
    messagebox.showinfo("Info", "Monthly Income functionality not implemented yet.")

def generate_csv():
    messagebox.showinfo("Info", "Generate CSV functionality not implemented yet.")

def check_report():
    messagebox.showinfo("Info", "Check Report functionality not implemented yet.")

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
        show_dashboard()
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

    users[username] = {"password": password, "full_name": full_name, "expenses": []}

    with open("user_data.pkl", "wb") as f:
        pickle.dump(users, f)

    messagebox.showinfo("Success", "Signup successful! Please login.")
    show_login_screen()

def save_expense():
    description = expense_desc_entry.get().strip()
    amount_str = expense_amount_entry.get().strip()
    category = expense_category_entry.get().strip()

    if not description or not amount_str or not category:
        messagebox.showerror("Error", "All fields are required.", parent=expense_window)
        return

    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number.", parent=expense_window)
        return

    users = {}
    if os.path.exists("user_data.pkl"):
        with open("user_data.pkl", "rb") as f:
            users = pickle.load(f)

    new_expense = {
        "description": description,
        "amount": amount,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users[logged_in_user]["expenses"].append(new_expense)

    with open("user_data.pkl", "wb") as f:
        pickle.dump(users, f)

    messagebox.showinfo("Success", "Expense added successfully!", parent=expense_window)
    expense_window.destroy()

def logout():
    global logged_in_user
    logged_in_user = None
    if os.path.exists("session.pkl"):
        os.remove("session.pkl")
    show_login_screen()

def create_dummy_data():
    users = {
        "testuser": {"password": "testpassword", "full_name": "Test User"},
        "john": {"password": "doe", "full_name": "John Doe"}
    }
    with open("user_data.pkl", "wb") as f:
        pickle.dump(users, f)

# --- Main Application Logic ---

if __name__ == "__main__":
    # create_dummy_data() # Uncomment to create dummy data
    root.title("Finance Manager")
    root.geometry("400x300")

    # Check for a saved session
    if os.path.exists("session.pkl"):
        with open("session.pkl", "rb") as f:
            logged_in_user = pickle.load(f)
    
    if logged_in_user:
        show_dashboard()
    else:
        show_login_screen()

    root.mainloop()
