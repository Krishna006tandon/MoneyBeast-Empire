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
        self.state('zoomed')  # Start maximized
        self.minsize(800, 600) 

        self.style = ttk.Style(self)
        
        # --- Color Scheme ---
        self.primary_color = "#1b263b"
        self.secondary_color = "#e0e1dd"
        self.accent_color = "#0d9276"
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
        self.profile_frame_obj = None
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
        elif frame_name == "profile":
            self.profile_frame_obj = ttk.Frame(self.main_content_frame, padding="10 10 10 10")
            self.create_profile_screen()
            self.profile_frame_obj.pack(expand=True, fill=tk.BOTH)

    def create_profile_screen(self):
        self.profile_frame_obj.grid_columnconfigure(1, weight=1)

        ttk.Label(self.profile_frame_obj, text="User Profile", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")

        ttk.Label(self.profile_frame_obj, text="Full Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.full_name_entry = ttk.Entry(self.profile_frame_obj, width=40)
        self.full_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.profile_frame_obj, text="New Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.new_password_entry = ttk.Entry(self.profile_frame_obj, show="*")
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(self.profile_frame_obj, text="Save Profile", command=self.update_profile).grid(row=3, column=1, padx=10, pady=20, sticky="e")

    def show_profile_screen(self):
        self.show_content_frame("profile")
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        full_name = user_data.get('full_name', '')
        self.full_name_entry.delete(0, tk.END)
        self.full_name_entry.insert(0, full_name)

    def update_profile(self):
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})

        new_full_name = self.full_name_entry.get().strip()
        new_password = self.new_password_entry.get().strip()

        if new_full_name:
            user_data['full_name'] = new_full_name

        if new_password:
            user_data['password'] = new_password

        self.save_users(users)
        messagebox.showinfo("Success", "Profile updated successfully!")
        self.show_dashboard_screen()

    def create_login_screen(self):
        self.login_frame_obj.grid_rowconfigure(0, weight=1)
        self.login_frame_obj.grid_columnconfigure(0, weight=1)

        form_frame = ttk.Frame(self.login_frame_obj, padding="20 20 20 20")
        form_frame.grid(row=0, column=0)

        ttk.Label(form_frame, text="Login", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Signup", command=self.show_signup_screen).grid(row=4, column=0, columnspan=2)

    def show_login_screen(self):
        self.show_frame(self.login_frame_obj)

    def create_signup_screen(self):
        self.signup_frame_obj.grid_rowconfigure(0, weight=1)
        self.signup_frame_obj.grid_columnconfigure(0, weight=1)

        form_frame = ttk.Frame(self.signup_frame_obj, padding="20 20 20 20")
        form_frame.grid(row=0, column=0)

        ttk.Label(form_frame, text="Signup", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Full Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.full_name_entry = ttk.Entry(form_frame)
        self.full_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(form_frame, text="Username:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.new_username_entry = ttk.Entry(form_frame)
        self.new_username_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(form_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.new_password_entry = ttk.Entry(form_frame, show="*")
        self.new_password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(form_frame, text="Signup", command=self.signup).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Back to Login", command=self.show_login_screen).grid(row=5, column=0, columnspan=2)

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
        ttk.Button(side_menu_frame, text="👤 Profile", command=self.show_profile_screen, style='SideMenu.TButton').pack(fill=tk.X, pady=5, padx=20)
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
        self.check_report_frame_obj.grid_rowconfigure(5, weight=1)

        ttk.Label(self.check_report_frame_obj, text="📊 Monthly Financial Analytics", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")

        # Summary Cards Frame
        summary_frame = ttk.Frame(self.check_report_frame_obj, style='TFrame')
        summary_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        summary_frame.grid_columnconfigure(0, weight=1)
        summary_frame.grid_columnconfigure(1, weight=1)
        summary_frame.grid_columnconfigure(2, weight=1)

        # Income Card
        income_card = ttk.Frame(summary_frame, style='TFrame', relief=tk.RAISED, borderwidth=2)
        income_card.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Label(income_card, text="💰 Monthly Salary", font=("Arial", 10, "bold"), foreground=self.accent_color).pack(pady=5, padx=10)
        self.report_income_label = ttk.Label(income_card, text="", font=("Arial", 14, "bold"), foreground="green")
        self.report_income_label.pack(pady=5, padx=10)

        # Expenses Card
        expenses_card = ttk.Frame(summary_frame, style='TFrame', relief=tk.RAISED, borderwidth=2)
        expenses_card.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(expenses_card, text="💸 Total Expenses", font=("Arial", 10, "bold"), foreground=self.accent_color).pack(pady=5, padx=10)
        self.report_expenses_label = ttk.Label(expenses_card, text="", font=("Arial", 14, "bold"), foreground="orange")
        self.report_expenses_label.pack(pady=5, padx=10)

        # Balance Card
        balance_card = ttk.Frame(summary_frame, style='TFrame', relief=tk.RAISED, borderwidth=2)
        balance_card.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Label(balance_card, text="💵 Remaining Balance", font=("Arial", 10, "bold"), foreground=self.accent_color).pack(pady=5, padx=10)
        self.report_balance_label = ttk.Label(balance_card, text="", font=("Arial", 14, "bold"))
        self.report_balance_label.pack(pady=5, padx=10)

        # Visual Progress Bar Frame
        progress_frame = ttk.Frame(self.check_report_frame_obj, style='TFrame')
        progress_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(progress_frame, text="Budget Utilization:", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.progress_canvas = tk.Canvas(progress_frame, height=40, bg=self.primary_color, highlightthickness=0)
        self.progress_canvas.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.progress_percentage_label = ttk.Label(progress_frame, text="", font=("Arial", 10, "italic"))
        self.progress_percentage_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        # Expense Breakdown Section
        ttk.Label(self.check_report_frame_obj, text="📋 Expense Breakdown by Category", style='Subheader.TLabel').grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        # Category Details Frame with Canvas for visual bars
        category_frame = ttk.Frame(self.check_report_frame_obj)
        category_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        category_frame.grid_columnconfigure(0, weight=1)

        self.category_canvas = tk.Canvas(category_frame, bg=self.primary_color, highlightthickness=0, height=200)
        self.category_canvas.pack(fill=tk.BOTH, expand=True)

        # Detailed Text Report
        ttk.Label(self.check_report_frame_obj, text="📝 Detailed Analytics", style='Subheader.TLabel').grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="nw")

        text_frame = ttk.Frame(self.check_report_frame_obj)
        text_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.check_report_frame_obj.grid_rowconfigure(6, weight=1)

        self.report_text_widget = tk.Text(text_frame, wrap=tk.WORD, height=12, width=60, font=("Arial", 10),
                                          background=self.primary_color, foreground=self.text_color,
                                          highlightthickness=0, borderwidth=0)
        self.report_text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.report_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text_widget.config(yscrollcommand=scrollbar.set)
        # Styled tags for better readability in Detailed Analytics
        self.report_text_widget.tag_config("header", font=("Arial", 11, "bold"), foreground=self.accent_color)
        self.report_text_widget.tag_config("bold", font=("Arial", 10, "bold"))
        self.report_text_widget.tag_config("ok", foreground="#2ecc71")
        self.report_text_widget.tag_config("warn", foreground="#e67e22")
        self.report_text_widget.tag_config("bad", foreground="#e74c3c")
        self.report_text_widget.tag_config("label", foreground=self.secondary_color)
        self.report_text_widget.tag_config("value", foreground="#ffffff")
        self.report_text_widget.tag_config("mono", font=("Consolas", 10))
        self.report_text_widget.config(state=tk.DISABLED)

        ttk.Button(self.check_report_frame_obj, text="Back to Dashboard", command=self.show_dashboard_screen).grid(row=7, column=0, padx=10, pady=20, sticky="w")

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
        # Fetch data from user_data.pkl
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = user_data.get('monthly_income', 0.0)
        expenses = user_data.get('expenses', [])
        total_expenses = sum(expense.get('amount', 0.0) for expense in expenses)
        remaining_balance = monthly_income - total_expenses

        # Update summary cards with formatted values
        self.report_income_label.config(text=f"${monthly_income:,.2f}")
        self.report_expenses_label.config(text=f"${total_expenses:,.2f}")
        self.report_balance_label.config(text=f"${remaining_balance:,.2f}",
                                         foreground="green" if remaining_balance >= 0 else "red")

        # Draw budget utilization progress bar
        self.progress_canvas.delete("all")
        canvas_width = self.progress_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 600  # Default width

        if monthly_income > 0:
            utilization_percentage = min((total_expenses / monthly_income) * 100, 100)
            bar_width = (canvas_width - 20) * (utilization_percentage / 100)

            # Background bar
            self.progress_canvas.create_rectangle(10, 10, canvas_width - 10, 30,
                                                  fill="#34495e", outline="")

            # Progress bar with color based on utilization
            if utilization_percentage <= 50:
                bar_color = "green"
            elif utilization_percentage <= 80:
                bar_color = "orange"
            else:
                bar_color = "red"

            self.progress_canvas.create_rectangle(10, 10, 10 + bar_width, 30,
                                                  fill=bar_color, outline="")

            # Percentage text
            self.progress_canvas.create_text(canvas_width // 2, 20,
                                            text=f"{utilization_percentage:.1f}%",
                                            fill="white", font=("Arial", 12, "bold"))

            self.progress_percentage_label.config(
                text=f"You've spent {utilization_percentage:.1f}% of your monthly income"
            )
        else:
            self.progress_canvas.create_text(canvas_width // 2, 20,
                                            text="Set monthly income to see utilization",
                                            fill=self.text_color, font=("Arial", 10))
            self.progress_percentage_label.config(text="")

        # Calculate expenses by category
        expenses_by_category = {}
        for expense in expenses:
            amount = expense.get('amount', 0.0)
            category = expense.get('category', 'Uncategorized')
            expenses_by_category[category] = expenses_by_category.get(category, 0.0) + amount

        # Draw category breakdown bars
        self.category_canvas.delete("all")
        canvas_width = self.category_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 600

        if expenses_by_category:
            sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
            max_amount = max(expenses_by_category.values())
            bar_height = 30
            y_offset = 10
            colors = ["#3498db", "#e74c3c", "#f39c12", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22"]

            for idx, (category, amount) in enumerate(sorted_categories):
                bar_width = ((canvas_width - 200) * (amount / max_amount)) if max_amount > 0 else 0
                color = colors[idx % len(colors)]

                # Category name
                self.category_canvas.create_text(10, y_offset + bar_height // 2,
                                                text=category, anchor="w",
                                                fill=self.text_color, font=("Arial", 10, "bold"))

                # Bar
                self.category_canvas.create_rectangle(150, y_offset, 150 + bar_width, y_offset + bar_height - 5,
                                                     fill=color, outline="")

                # Amount text
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                self.category_canvas.create_text(160 + bar_width, y_offset + bar_height // 2,
                                                text=f"${amount:,.2f} ({percentage:.1f}%)",
                                                anchor="w", fill=self.text_color, font=("Arial", 9))

                y_offset += bar_height + 10
        else:
            self.category_canvas.create_text(canvas_width // 2, 100,
                                            text="No expenses recorded yet",
                                            fill=self.text_color, font=("Arial", 12))

        # Update detailed text report with daily-use analytics
        self.report_text_widget.config(state=tk.NORMAL)
        self.report_text_widget.delete(1.0, tk.END)

        # Header
        self.report_text_widget.insert(tk.END, "MONTHLY FINANCIAL ANALYTICS\n", ("header",))
        self.report_text_widget.insert(tk.END, f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Compute day-based metrics
        today = datetime.now()
        first_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            next_month_first = first_of_month.replace(year=today.year + 1, month=1)
        else:
            next_month_first = first_of_month.replace(month=today.month + 1)
        days_in_month = (next_month_first - first_of_month).days or 30
        days_passed = today.day
        days_left = max(0, days_in_month - days_passed)

        spend_per_day_actual = (total_expenses / days_passed) if days_passed > 0 else 0.0
        planned_daily_budget = (monthly_income / days_in_month) if days_in_month > 0 else 0.0
        safe_daily_spend_remaining = (remaining_balance / days_left) if days_left > 0 else 0.0
        projected_month_end_balance = monthly_income - (spend_per_day_actual * days_in_month)

        # Summary blocks
        self.report_text_widget.insert(tk.END, "OVERVIEW\n", ("header",))
        self.report_text_widget.insert(tk.END, "  Income: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${monthly_income:,.2f}\n", ("value",))
        self.report_text_widget.insert(tk.END, "  Spent to date: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${total_expenses:,.2f}\n", ("value",))
        balance_tag = "ok" if remaining_balance >= 0 else "bad"
        self.report_text_widget.insert(tk.END, "  Remaining balance: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${remaining_balance:,.2f}\n", (balance_tag,))

        self.report_text_widget.insert(tk.END, "\nTHIS MONTH\n", ("header",))
        self.report_text_widget.insert(tk.END, f"  Days in month: {days_in_month}\n")
        self.report_text_widget.insert(tk.END, f"  Days passed: {days_passed}\n")
        self.report_text_widget.insert(tk.END, f"  Days left: {days_left}\n")
        
        budget_tag = "ok" if spend_per_day_actual <= planned_daily_budget else ("warn" if spend_per_day_actual <= planned_daily_budget * 1.2 else "bad")
        self.report_text_widget.insert(tk.END, "  Actual burn/day: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${spend_per_day_actual:,.2f}\n", (budget_tag,))
        self.report_text_widget.insert(tk.END, "  Planned budget/day: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${planned_daily_budget:,.2f}\n", ("value",))
        safe_tag = "ok" if safe_daily_spend_remaining >= planned_daily_budget else "warn"
        self.report_text_widget.insert(tk.END, "  Safe spend for today: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${safe_daily_spend_remaining:,.2f}\n", (safe_tag,))

        proj_tag = "ok" if projected_month_end_balance >= 0 else "bad"
        self.report_text_widget.insert(tk.END, "  Projected month-end balance: ", ("label",))
        self.report_text_widget.insert(tk.END, f"${projected_month_end_balance:,.2f}\n", (proj_tag,))

        # Category breakdown text
        if expenses_by_category:
            self.report_text_widget.insert(tk.END, "\nCATEGORY BREAKDOWN\n", ("header",))
            for category, amount in sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True):
                pct = (amount / total_expenses * 100) if total_expenses > 0 else 0
                self.report_text_widget.insert(tk.END, f"  • {category}: ", ("label",))
                self.report_text_widget.insert(tk.END, f"${amount:,.2f} ({pct:.1f}%)\n", ("value",))

        # Recent transactions
        if expenses:
            self.report_text_widget.insert(tk.END, "\nRECENT TRANSACTIONS\n", ("header",))
            for tx in list(reversed(expenses))[:5]:
                dt = tx.get('date', '')
                desc = tx.get('description', '')
                cat = tx.get('category', '')
                amt = tx.get('amount', 0.0)
                line = f"  - [{dt}] {desc} ({cat}): ${amt:,.2f}\n"
                self.report_text_widget.insert(tk.END, line, ("mono",))
        else:
            self.report_text_widget.insert(tk.END, "\nNo expenses yet. Start tracking to see insights.\n")

        # Tips
        if monthly_income > 0:
            self.report_text_widget.insert(tk.END, "\nTIPS\n", ("header",))
            if remaining_balance < 0:
                self.report_text_widget.insert(tk.END, f"  ⚠️  Over budget by ${abs(remaining_balance):,.2f}. Reduce discretionary spend this week.\n", ("bad",))
            elif spend_per_day_actual > planned_daily_budget:
                self.report_text_widget.insert(tk.END, "  💡 You're above daily budget. Try a no-spend day to catch up.\n", ("warn",))
            else:
                self.report_text_widget.insert(tk.END, "  ✓ You're on track. Consider moving surplus to savings.\n", ("ok",))

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