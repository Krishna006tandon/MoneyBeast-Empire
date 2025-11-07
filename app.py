
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pickle
import os

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager")
        self.root.geometry("400x300")

        self.logged_in_user = None

        if os.path.exists("session.pkl"):
            with open("session.pkl", "rb") as f:
                self.logged_in_user = pickle.load(f)
        
        if self.logged_in_user:
            self.show_dashboard()
        else:
            self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Signup", command=self.show_signup_screen).grid(row=3, column=0, columnspan=2)

    def show_signup_screen(self):
        self.clear_screen()

        self.signup_frame = tk.Frame(self.root)
        self.signup_frame.pack(pady=20)

        tk.Label(self.signup_frame, text="Full Name:").grid(row=0, column=0, padx=10, pady=5)
        self.full_name_entry = tk.Entry(self.signup_frame)
        self.full_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.signup_frame, text="Username:").grid(row=1, column=0, padx=10, pady=5)
        self.new_username_entry = tk.Entry(self.signup_frame)
        self.new_username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.signup_frame, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        self.new_password_entry = tk.Entry(self.signup_frame, show="*")
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.signup_frame, text="Signup", command=self.signup).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.signup_frame, text="Back to Login", command=self.show_login_screen).grid(row=4, column=0, columnspan=2)

    def show_dashboard(self):
        self.clear_screen()

        self.dashboard_frame = tk.Frame(self.root)
        self.dashboard_frame.pack(pady=20)

        tk.Label(self.dashboard_frame, text=f"Welcome, {self.logged_in_user}!").pack(pady=10)
        tk.Button(self.dashboard_frame, text="Add Expense", command=self.add_expense).pack(fill=tk.X, pady=2)
        tk.Button(self.dashboard_frame, text="Monthly Income", command=self.monthly_income).pack(fill=tk.X, pady=2)
        tk.Button(self.dashboard_frame, text="Generate CSV", command=self.generate_csv).pack(fill=tk.X, pady=2)
        tk.Button(self.dashboard_frame, text="Check Report", command=self.check_report).pack(fill=tk.X, pady=2)
        tk.Button(self.dashboard_frame, text="Logout", command=self.logout).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_expense(self):
        self.expense_window = tk.Toplevel(self.root)
        self.expense_window.title("Add Expense")
        self.expense_window.geometry("350x200")

        frame = tk.Frame(self.expense_window, padx=10, pady=10)
        frame.pack(expand=True)

        tk.Label(frame, text="Description:").grid(row=0, column=0, sticky="w", pady=2)
        self.expense_desc_entry = tk.Entry(frame)
        self.expense_desc_entry.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="Amount:").grid(row=1, column=0, sticky="w", pady=2)
        self.expense_amount_entry = tk.Entry(frame)
        self.expense_amount_entry.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Category:").grid(row=2, column=0, sticky="w", pady=2)
        self.expense_category_entry = tk.Entry(frame)
        self.expense_category_entry.grid(row=2, column=1, pady=2)

        tk.Button(frame, text="Save Expense", command=self.save_expense).grid(row=3, columnspan=2, pady=10)

    def monthly_income(self):
        messagebox.showinfo("Info", "Monthly Income functionality not implemented yet.")

    def generate_csv(self):
        messagebox.showinfo("Info", "Generate CSV functionality not implemented yet.")

    def check_report(self):
        messagebox.showinfo("Info", "Check Report functionality not implemented yet.")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        users = {}
        if os.path.exists("user_data.pkl"):
            with open("user_data.pkl", "rb") as f:
                users = pickle.load(f)

        if username in users and users[username]["password"] == password:
            self.logged_in_user = username
            with open("session.pkl", "wb") as f:
                pickle.dump(self.logged_in_user, f)
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        full_name = self.full_name_entry.get().strip()
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()

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
        self.show_login_screen()

    def save_expense(self):
        description = self.expense_desc_entry.get().strip()
        amount_str = self.expense_amount_entry.get().strip()
        category = self.expense_category_entry.get().strip()

        if not description or not amount_str or not category:
            messagebox.showerror("Error", "All fields are required.", parent=self.expense_window)
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.", parent=self.expense_window)
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
        users[self.logged_in_user]["expenses"].append(new_expense)

        with open("user_data.pkl", "wb") as f:
            pickle.dump(users, f)

        messagebox.showinfo("Success", "Expense added successfully!", parent=self.expense_window)
        self.expense_window.destroy()

    def logout(self):
        self.logged_in_user = None
        if os.path.exists("session.pkl"):
            os.remove("session.pkl")
        self.show_login_screen()

def create_dummy_data():
    users = {
        "testuser": {"password": "testpassword", "full_name": "Test User"},
        "john": {"password": "doe", "full_name": "John Doe"}
    }
    with open("user_data.pkl", "wb") as f:
        pickle.dump(users, f)

if __name__ == "__main__":
    # create_dummy_data() # Uncomment to create dummy data
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
