import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from datetime import datetime
import pickle
import os
import csv

class FinanceManager(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_theme("arc")
        self.title("Finance Manager")
        self.attributes('-fullscreen', True)
        self.bind('<Escape>', self.exit_fullscreen)

        self.style = ttk.Style(self)
        
        # --- Color Scheme ---
        self.primary_color = "#2c3e50"
        self.secondary_color = "#ecf0f1"
        self.accent_color = "#3498db"
        self.text_color = "#ffffff"

        self.set_theme("clam")
        
        self.style.configure('.', background=self.primary_color, foreground=self.text_color)
        self.style.configure('TLabel', background=self.primary_color, foreground=self.text_color, font=('Arial', 11))
        self.style.configure('TButton', background=self.accent_color, foreground=self.primary_color, font=('Arial', 10, 'bold'))
        self.style.map('TButton', background=[('active', self.secondary_color)])
        self.style.configure('TFrame', background=self.primary_color)
        self.style.configure('TEntry', foreground='black')
        
        self.style.configure('Header.TLabel', font=("Arial", 18, "bold"), foreground=self.accent_color)
        self.style.configure('Subheader.TLabel', font=("Arial", 12, "bold"), foreground=self.secondary_color)

        self.style.configure('SideMenu.TFrame', background=self.primary_color)
        self.style.configure('SideMenu.TButton', font=('Arial', 11), background=self.primary_color, foreground=self.text_color, anchor='w')
        self.style.map('SideMenu.TButton', background=[('active', self.accent_color)])

        # --- Treeview Style ---
        self.style.configure("Treeview", background=self.primary_color, 
                             fieldbackground=self.primary_color, foreground=self.text_color)
        self.style.map('Treeview', background=[('selected', self.accent_color)])
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background=self.primary_color, foreground=self.text_color)
        self.style.map("Treeview.Heading", background=[('active', self.secondary_color)])

        # --- Instance Variables ---
        self.logged_in_user = None
        self.login_frame_obj = None
        self.signup_frame_obj = None
        self.dashboard_frame_obj = None
        self.add_expense_frame_obj = None
        self.monthly_income_frame_obj = None
        self.check_report_frame_obj = None
        self.username_entry = None
        self.password_entry = None
        self.full_name_entry = None
        self.new_username_entry = None
        self.new_password_entry = None
        self.expense_desc_entry = None
        self.expense_amount_entry = None
        self.expense_category_entry = None
        self.expense_table = None
        self.income_entry = None
        self.current_income_label = None
        self.report_text_widget = None
        self.total_balance_label = None

        self.create_all_frames()
        self.check_session()

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

    def create_all_frames(self):
        self.login_frame_obj = ttk.Frame(self, padding="15 15 15 15")
        self.create_login_screen()
        self.signup_frame_obj = ttk.Frame(self, padding="15 15 15 15")
        self.create_signup_screen()
        
        self.dashboard_frame_obj = ttk.Frame(self, padding="0 0 0 0")
        self.create_dashboard_screen()

    def show_frame(self, frame_to_show):
        for frame in [self.login_frame_obj, self.signup_frame_obj, self.dashboard_frame_obj]:
            if frame and frame.winfo_exists():
                frame.pack_forget()
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def show_content_frame(self, frame_name):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        if frame_name == "add_expense":
            self.add_expense_frame_obj = ttk.Frame(self.main_content_frame, padding="10 10 10 10")
            self.create_add_expense_screen()
            self.add_expense_frame_obj.pack(expand=True, fill=tk.BOTH)
        elif frame_name == "monthly_income":
            self.monthly_income_frame_obj = ttk.Frame(self.main_content_frame, padding="10 10 10 10")
            self.create_monthly_income_screen()
            self.monthly_income_frame_obj.pack(expand=True, fill=tk.BOTH)
        elif frame_name == "check_report":
            self.check_report_frame_obj = ttk.Frame(self.main_content_frame, padding="10 10 10 10")
            self.create_check_report_screen()
            self.check_report_frame_obj.pack(expand=True, fill=tk.BOTH)

    def create_login_screen(self):
        ttk.Label(self.login_frame_obj, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self.login_frame_obj)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.login_frame_obj, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame_obj, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(self.login_frame_obj, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.login_frame_obj, text="Signup", command=self.show_signup_screen).grid(row=3, column=0, columnspan=2)

    def show_login_screen(self):
        self.show_frame(self.login_frame_obj)

    def create_signup_screen(self):
        ttk.Label(self.signup_frame_obj, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.full_name_entry = ttk.Entry(self.signup_frame_obj)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.signup_frame_obj, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_username_entry = ttk.Entry(self.signup_frame_obj)
        self.new_username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.signup_frame_obj, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.new_password_entry = ttk.Entry(self.signup_frame_obj, show="*")
        self.new_password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(self.signup_frame_obj, text="Signup", command=self.signup).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.signup_frame_obj, text="Back to Login", command=self.show_login_screen).grid(row=4, column=0, columnspan=2)

    def show_signup_screen(self):
        self.show_frame(self.signup_frame_obj)

    def create_dashboard_screen(self):
        self.dashboard_frame_obj.grid_rowconfigure(0, weight=1)
        self.dashboard_frame_obj.grid_columnconfigure(1, weight=1)

        side_menu_frame = ttk.Frame(self.dashboard_frame_obj, width=250, style='SideMenu.TFrame')
        side_menu_frame.grid(row=0, column=0, sticky="ns")
        side_menu_frame.grid_propagate(False)

        self.main_content_frame = ttk.Frame(self.dashboard_frame_obj, style='TFrame')
        self.main_content_frame.grid(row=0, column=1, sticky="nsew")

        # This label will be updated in show_dashboard_screen
        self.welcome_label = ttk.Label(side_menu_frame, text="", style='Header.TLabel')
        self.welcome_label.pack(pady=20, padx=20, anchor='w')
        
        self.total_balance_label = ttk.Label(side_menu_frame, text="", style='Subheader.TLabel')
        self.total_balance_label.pack(pady=10, padx=20, anchor='w')

        ttk.Button(side_menu_frame, text="➕ Add Expense", command=self.show_add_expense_screen, style='SideMenu.TButton').pack(fill=tk.X, pady=5, padx=20)
        ttk.Button(side_menu_frame, text="💰 Monthly Income", command=self.show_monthly_income_screen, style='SideMenu.TButton').pack(fill=tk.X, pady=5, padx=20)
        ttk.Button(side_menu_frame, text="📄 Generate CSV", command=self.generate_csv, style='SideMenu.TButton').pack(fill=tk.X, pady=5, padx=20)
        ttk.Button(side_menu_frame, text="📊 Check Report", command=self.show_check_report_screen, style='SideMenu.TButton').pack(fill=tk.X, pady=5, padx=20)
        ttk.Button(side_menu_frame, text="🚪 Logout", command=self.logout, style='SideMenu.TButton').pack(fill=tk.X, side=tk.BOTTOM, pady=15, padx=20)

    def show_dashboard_screen(self):
        if self.logged_in_user:
            self.welcome_label.config(text=f"Welcome, {self.logged_in_user}!")

        self.show_frame(self.dashboard_frame_obj)
        self.update_dashboard_summary()
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.main_content_frame, text="Select an option from the menu.", font=("Arial", 16)).pack(expand=True)

    def create_add_expense_screen(self):
        self.add_expense_frame_obj.grid_columnconfigure(1, weight=1)

        ttk.Label(self.add_expense_frame_obj, text="Add New Expense", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")

        ttk.Label(self.add_expense_frame_obj, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.expense_desc_entry = ttk.Entry(self.add_expense_frame_obj, width=40)
        self.expense_desc_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.add_expense_frame_obj, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.expense_amount_entry = ttk.Entry(self.add_expense_frame_obj)
        self.expense_amount_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.add_expense_frame_obj, text="Category:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.expense_category_entry = ttk.Entry(self.add_expense_frame_obj)
        self.expense_category_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(self.add_expense_frame_obj, text="Save Expense", command=self.save_expense).grid(row=4, column=1, padx=10, pady=15, sticky="e")
        ttk.Button(self.add_expense_frame_obj, text="Back to Dashboard", command=self.show_dashboard_screen).grid(row=4, column=0, padx=10, pady=15, sticky="w")

        # --- Past Expenses Table ---
        table_frame = ttk.Frame(self.add_expense_frame_obj)
        table_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        self.add_expense_frame_obj.grid_rowconfigure(5, weight=1)

        cols = ("Date", "Description", "Category", "Amount")
        self.expense_table = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.expense_table.heading(col, text=col)
        self.expense_table.column("Date", width=150, anchor=tk.W)
        self.expense_table.column("Description", width=200, anchor=tk.W)
        self.expense_table.column("Category", width=100, anchor=tk.W)
        self.expense_table.column("Amount", width=80, anchor=tk.E)

        self.expense_table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.expense_table.yview)
        self.expense_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def show_add_expense_screen(self):
        self.show_content_frame("add_expense")
        self.populate_expense_table()

    def populate_expense_table(self):
        for i in self.expense_table.get_children():
            self.expense_table.delete(i)
        users = self.load_users()
        user_expenses = users.get(self.logged_in_user, {}).get('expenses', [])
        for expense in reversed(user_expenses): # Show most recent first
            self.expense_table.insert("", "end", values=(expense['date'], expense['description'], expense['category'], f"${expense['amount']:,.2f}"))

    def create_monthly_income_screen(self):
        self.monthly_income_frame_obj.grid_columnconfigure(1, weight=1)

        ttk.Label(self.monthly_income_frame_obj, text="Set Monthly Income", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")

        ttk.Label(self.monthly_income_frame_obj, text="Monthly Income:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.income_entry = ttk.Entry(self.monthly_income_frame_obj, width=40)
        self.income_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.current_income_label = ttk.Label(self.monthly_income_frame_obj, text="", font=("Arial", 10, "italic"))
        self.current_income_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(self.monthly_income_frame_obj, text="Save Income", command=self.save_income).grid(row=3, column=1, padx=10, pady=20, sticky="e")
        ttk.Button(self.monthly_income_frame_obj, text="Back to Dashboard", command=self.show_dashboard_screen).grid(row=3, column=0, padx=10, pady=20, sticky="w")

    def show_monthly_income_screen(self):
        self.show_content_frame("monthly_income")
        self.load_and_display_income()

    def create_check_report_screen(self):
        self.check_report_frame_obj.grid_columnconfigure(0, weight=1)

        ttk.Label(self.check_report_frame_obj, text="Financial Report", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")

        summary_frame = ttk.Frame(self.check_report_frame_obj, style='TFrame')
        summary_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        summary_frame.grid_columnconfigure(1, weight=1)

        self.report_income_label = ttk.Label(summary_frame, text="", font=("Arial", 11, "bold"))
        self.report_income_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.report_expenses_label = ttk.Label(summary_frame, text="", font=("Arial", 11, "bold"))
        self.report_expenses_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.report_balance_label = ttk.Label(summary_frame, text="", font=("Arial", 11, "bold"))
        self.report_balance_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        ttk.Label(self.check_report_frame_obj, text="--- Expenses by Category ---", style='Subheader.TLabel').grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        text_frame = ttk.Frame(self.check_report_frame_obj)
        text_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.check_report_frame_obj.grid_rowconfigure(3, weight=1)

        self.report_text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15, width=40, font=("Arial", 10),
                                          background=self.primary_color, foreground=self.text_color,
                                          highlightthickness=0, borderwidth=0)
        self.report_text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.report_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text_widget.config(yscrollcommand=scrollbar.set)
        self.report_text_widget.config(state=tk.DISABLED)

        ttk.Button(self.check_report_frame_obj, text="Back to Dashboard", command=self.show_dashboard_screen).grid(row=4, column=0, padx=10, pady=20, sticky="w")

    def show_check_report_screen(self):
        self.show_content_frame("check_report")
        self.update_report_content()

    def update_dashboard_summary(self):
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = user_data.get('monthly_income', 0.0)
        expenses = user_data.get('expenses', [])
        total_expenses = sum(expense.get('amount', 0.0) for expense in expenses)
        remaining_balance = monthly_income - total_expenses
        if self.current_income_label and self.current_income_label.winfo_exists():
            self.current_income_label.config(text=f"Current Monthly Income: ${monthly_income:,.2f}")
        if self.total_balance_label and self.total_balance_label.winfo_exists():
            self.total_balance_label.config(text=f"Current Balance: ${remaining_balance:,.2f}",
                                       foreground="green" if remaining_balance >= 0 else "red")

    def update_report_content(self):
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = user_data.get('monthly_income', 0.0)
        expenses = user_data.get('expenses', [])
        total_expenses = sum(expense.get('amount', 0.0) for expense in expenses)
        remaining_balance = monthly_income - total_expenses
        self.report_income_label.config(text=f"Monthly Income: ${monthly_income:,.2f}")
        self.report_expenses_label.config(text=f"Total Expenses: ${total_expenses:,.2f}")
        self.report_balance_label.config(text=f"Remaining Balance: ${remaining_balance:,.2f}",
                                                                           foreground="green" if remaining_balance >= 0 else "red")
        self.report_text_widget.config(state=tk.NORMAL)
        self.report_text_widget.delete(1.0, tk.END)
        expenses_by_category = {}
        for expense in expenses:
            amount = expense.get('amount', 0.0)
            category = expense.get('category', 'Uncategorized')
            expenses_by_category[category] = expenses_by_category.get(category, 0.0) + amount
        if expenses_by_category:
            for category, amount in expenses_by_category.items():
                self.report_text_widget.insert(tk.END, f"{category}: ${amount:,.2f}\n")
        else:
            self.report_text_widget.insert(tk.END, "No expenses recorded yet.\n")
        self.report_text_widget.config(state=tk.DISABLED)

    def generate_csv(self):
        users = self.load_users()
        user_data = users.get(self.logged_in_user)
        if not user_data or not user_data.get("expenses"):
            messagebox.showinfo("Info", "No expenses to export.")
            return
        if not os.path.exists("data"):
            os.makedirs("data")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join("data", f"expenses_{self.logged_in_user}_{timestamp}.csv")
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'Description', 'Category', 'Amount'])
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

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return
        users = self.load_users()
        if username in users and users[username]["password"] == password:
            self.logged_in_user = username
            with open("session.pkl", "wb") as f:
                pickle.dump(self.logged_in_user, f)
            self.show_dashboard_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def signup(self):
        full_name = self.full_name_entry.get().strip()
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        if not full_name.replace(' ', '').isalpha() or not username or not password:
            messagebox.showerror("Error", "Invalid input. Please check your details.")
            return
        users = self.load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return
        users[username] = {"password": password, "full_name": full_name, "expenses": [], "monthly_income": 0.0}
        self.save_users(users)
        messagebox.showinfo("Success", "Signup successful! Please login.")
        self.show_login_screen()

    def save_expense(self):
        description = self.expense_desc_entry.get().strip()
        amount_str = self.expense_amount_entry.get().strip()
        category = self.expense_category_entry.get().strip()
        if not description or not amount_str or not category:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
            return
        users = self.load_users()
        if 'expenses' not in users[self.logged_in_user]:
            users[self.logged_in_user]['expenses'] = []
        new_expense = {
            "description": description,
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        users[self.logged_in_user]["expenses"].append(new_expense)
        self.save_users(users)
        self.expense_desc_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)
        self.expense_category_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Expense added successfully!")
        self.populate_expense_table()
        self.update_dashboard_summary()

    def save_income(self):
        income_str = self.income_entry.get().strip()
        if not income_str:
            messagebox.showerror("Error", "Please enter an income amount.")
            return
        try:
            income = float(income_str)
        except ValueError:
            messagebox.showerror("Error", "Income must be a valid number.")
            return
        users = self.load_users()
        users[self.logged_in_user]['monthly_income'] = income
        self.save_users(users)
        messagebox.showinfo("Success", "Monthly income saved successfully!")
        self.show_dashboard_screen()
        self.update_dashboard_summary()

    def load_and_display_income(self):
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = user_data.get('monthly_income', 0.0)
        self.current_income_label.config(text=f"Current Monthly Income: ${monthly_income:,.2f}")

    def logout(self):
        self.logged_in_user = None
        if os.path.exists("session.pkl"):
            os.remove("session.pkl")
        self.show_login_screen()

    def load_users(self):
        if os.path.exists("user_data.pkl"):
            with open("user_data.pkl", "rb") as f:
                try:
                    return pickle.load(f)
                except (pickle.UnpicklingError, EOFError):
                    return {}
        return {}

    def save_users(self, users):
        with open("user_data.pkl", "wb") as f:
            pickle.dump(users, f)

    def check_session(self):
        if os.path.exists("session.pkl"):
            with open("session.pkl", "rb") as f:
                try:
                    self.logged_in_user = pickle.load(f)
                except (pickle.UnpicklingError, EOFError):
                    self.logged_in_user = None
        if self.logged_in_user:
            self.show_dashboard_screen()
        else:
            self.show_login_screen()

if __name__ == "__main__":
    app = FinanceManager()
    app.mainloop()