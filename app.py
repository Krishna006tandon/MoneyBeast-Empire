import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkfont
from ttkthemes import ThemedTk
from datetime import datetime
import pickle
import os
import csv

class FinanceManager(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           # --- Modern Light Theme Colors ---
        self.bg_color = "#fafafa"
        self.card_bg = "#ffffff"
        self.text_color = "#1a1a1a"
        self.accent_color = "#4a90e2"
        self.button_bg = "#d9e7ff"
        self.button_hover = "#bcd6ff"
        self.border_color = "#e0e0e0"
        self.success_color = "#2ecc71"
        self.warning_color = "#f39c12"
        self.error_color = "#e74c3c"
        self.primary_color = self.bg_color
        self.secondary_color = self.card_bg
        self.success_color = "#2ecc71"
        self.warning_color = "#f39c12"
        self.error_color = "#e74c3c"
        
        self.title("Finance Manager")
        self.state('zoomed')  # Start maximized
        self.minsize(1000, 700)
        
        # Set theme to clam for better theming control
        self.style = ttk.Style(self)
        
     
        
        # Configure base styles
        self.style.theme_use('clam')
        self.configure(bg=self.bg_color)
        
        # Configure default styles
        self.style.configure('.',
                           background=self.bg_color,
                           foreground=self.text_color,
                           font=('Segoe UI', 10))
        
        # Configure frame styles
        self.style.configure('Card.TFrame',
                           background=self.card_bg,
                           borderwidth=1,
                           relief='solid',
                           borderradius=10)
        
        # Configure button styles
        self.style.configure('TButton',
                           background=self.button_bg,
                           foreground=self.text_color,
                           font=('Segoe UI', 10, 'normal'),
                           borderwidth=1,
                           relief='solid',
                           padding=8)
        self.style.map('TButton',
                      background=[('active', self.button_hover)],
                      relief=[('pressed', 'sunken'), ('!pressed', 'solid')])
        
        # Configure label styles
        self.style.configure('Header.TLabel',
                           font=('Segoe UI', 20, 'bold'),
                           foreground=self.accent_color,
                           background=self.bg_color)
        self.style.configure('Subheader.TLabel',
                           font=('Segoe UI', 14, 'bold'),
                           foreground=self.text_color,
                           background=self.bg_color)
        
        # Configure entry styles
        self.style.configure('TEntry',
                           fieldbackground='white',
                           foreground=self.text_color,
                           borderwidth=1,
                           relief='solid',
                           padding=5)
        
        # Configure Treeview styles
        self.style.configure('Treeview',
                           background='white',
                           fieldbackground='white',
                           foreground=self.text_color,
                           borderwidth=0,
                           rowheight=30)
        self.style.map('Treeview',
                      background=[('selected', self.accent_color)],
                      foreground=[('selected', 'white')])
        self.style.configure('Treeview.Heading',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.bg_color,
                           foreground=self.text_color,
                           borderwidth=0,
                           padding=5)
        
        # Configure side menu styles
        self.style.configure('SideMenu.TFrame',
                           background=self.card_bg,
                           borderwidth=1,
                           relief='solid',
                           borderradius=0)
        self.style.configure('SideMenu.TButton',
                           font=('Segoe UI', 11),
                           background=self.card_bg,
                           foreground=self.text_color,
                           anchor='w',
                           padding=(20, 10))
        self.style.map('SideMenu.TButton',
                      background=[('active', self.button_hover)])
        
        # Add rounded button style
        self.style.configure('Rounded.TButton',
                           background=self.button_bg,
                           foreground=self.text_color,
                           font=('Segoe UI', 10, 'normal'),
                           borderwidth=0,
                           padding=10,
                           relief='flat')
        self.style.map('Rounded.TButton',
                      background=[('active', self.button_hover)])
        
        # Add padding to all widgets
        self.option_add('*TButton*Padding', 8)
        self.option_add('*TEntry*Padding', 6)
        self.option_add('*TCombobox*Padding', 6)

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
        # Create login frame
        self.login_frame_obj = ttk.Frame(self)
        
        # Set background color for the login frame
        self.login_frame_obj.configure(style='Card.TFrame')
        
        # Create a frame for the background
        bg_frame = ttk.Frame(self.login_frame_obj, style='TFrame')
        bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Configure the frame to use the background color
        bg_frame.configure(style='TFrame')
        self.style.configure('TFrame', background=self.bg_color)
        
        # Make sure the background frame stays at the back
        bg_frame.lower()
        
        # Create login screen
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
        # Main container with background
        container = ttk.Frame(self.login_frame_obj, style='TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center', width=400)
        
        # Card frame for the login form
        form_card = ttk.Frame(container, style='Card.TFrame', padding=(40, 40, 40, 30))
        form_card.pack(fill=tk.BOTH, expand=True)
        
        # App title
        ttk.Label(form_card, text="💼 Finance Manager", style='Header.TLabel').pack(pady=(0, 30))
        
        # Username field
        username_frame = ttk.Frame(form_card)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(username_frame, text="Username", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.username_entry = ttk.Entry(username_frame, font=('Segoe UI', 11))
        self.username_entry.pack(fill=tk.X, pady=0)
        
        # Password field
        password_frame = ttk.Frame(form_card)
        password_frame.pack(fill=tk.X, pady=(0, 25))
        ttk.Label(password_frame, text="Password", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.password_entry = ttk.Entry(password_frame, show="•", font=('Segoe UI', 11))
        self.password_entry.pack(fill=tk.X, pady=0)
        
        # Login button
        btn_login = ttk.Button(form_card, text="Sign In", command=self.login, style='Rounded.TButton')
        btn_login.pack(fill=tk.X, pady=(10, 20))
        
        # Signup link
        signup_frame = ttk.Frame(form_card)
        signup_frame.pack(fill=tk.X)
        ttk.Label(signup_frame, text="Don't have an account?").pack(side=tk.LEFT)
        signup_btn = ttk.Button(signup_frame, 
                              text="Create account", 
                              command=self.show_signup_screen,
                              style='TButton')
        signup_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus the username field by default
        self.username_entry.focus_set()

    def show_login_screen(self):
        self.show_frame(self.login_frame_obj)

    def create_signup_screen(self):
        # Main container with background
        container = ttk.Frame(self.signup_frame_obj, style='TFrame')
        container.place(relx=0.5, rely=0.5, anchor='center', width=400)
        
        # Card frame for the signup form
        form_card = ttk.Frame(container, style='Card.TFrame', padding=(40, 40, 40, 30))
        form_card.pack(fill=tk.BOTH, expand=True)
        
        # App title
        ttk.Label(form_card, text="📝 Create Account", style='Header.TLabel').pack(pady=(0, 30))
        
        # Full Name field
        fullname_frame = ttk.Frame(form_card)
        fullname_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(fullname_frame, text="Full Name", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.full_name_entry = ttk.Entry(fullname_frame, font=('Segoe UI', 11))
        self.full_name_entry.pack(fill=tk.X, pady=0)
        
        # Username field
        username_frame = ttk.Frame(form_card)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(username_frame, text="Username", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.new_username_entry = ttk.Entry(username_frame, font=('Segoe UI', 11))
        self.new_username_entry.pack(fill=tk.X, pady=0)
        
        # Password field
        password_frame = ttk.Frame(form_card)
        password_frame.pack(fill=tk.X, pady=(0, 25))
        ttk.Label(password_frame, text="Password", font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.new_password_entry = ttk.Entry(password_frame, show="•", font=('Segoe UI', 11))
        self.new_password_entry.pack(fill=tk.X, pady=0)
        
        # Signup button
        btn_signup = ttk.Button(form_card, text="Create Account", command=self.signup, style='Rounded.TButton')
        btn_signup.pack(fill=tk.X, pady=(10, 20))
        
        # Login link
        login_frame = ttk.Frame(form_card)
        login_frame.pack(fill=tk.X)
        ttk.Label(login_frame, text="Already have an account?").pack(side=tk.LEFT)
        login_btn = ttk.Button(login_frame, 
                             text="Sign in", 
                             command=self.show_login_screen,
                             style='TButton')
        login_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to signup
        self.new_password_entry.bind('<Return>', lambda e: self.signup())
        
        # Focus the full name field by default
        self.full_name_entry.focus_set()

    def show_signup_screen(self):
        self.show_frame(self.signup_frame_obj)

    def create_dashboard_screen(self):
        # Configure grid layout
        self.dashboard_frame_obj.grid_rowconfigure(0, weight=1)
        self.dashboard_frame_obj.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        sidebar = ttk.Frame(self.dashboard_frame_obj, width=280, style='SideMenu.TFrame')
        sidebar.grid(row=0, column=0, sticky="nsew", ipadx=10, ipady=20)
        sidebar.grid_propagate(False)
        
        # App logo and user info
        header_frame = ttk.Frame(sidebar, style='SideMenu.TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # App title
        ttk.Label(header_frame, 
                 text="💼 Finance", 
                 font=('Segoe UI', 18, 'bold'),
                 foreground=self.accent_color,
                 background=self.card_bg).pack(anchor='w')
        
        # User welcome and balance
        self.welcome_label = ttk.Label(header_frame, 
                                     text="", 
                                     font=('Segoe UI', 12, 'bold'),
                                     style='TLabel')
        self.welcome_label.pack(anchor='w', pady=(15, 5))
        
        self.total_balance_label = ttk.Label(header_frame,
                                           text="",
                                           font=('Segoe UI', 10),
                                           style='TLabel')
        self.total_balance_label.pack(anchor='w', pady=(0, 20))
        
        # Navigation menu
        nav_frame = ttk.Frame(sidebar, style='SideMenu.TFrame')
        nav_frame.pack(fill=tk.X, padx=10)
        
        # Navigation buttons
        nav_items = [
            ("📝 Add Expense", self.show_add_expense_screen),
            ("💰 Monthly Income", self.show_monthly_income_screen),
            ("📊 Reports", self.show_check_report_screen),
            ("👤 Profile", self.show_profile_screen),
        ]
        
        for text, command in nav_items:
            btn = ttk.Button(nav_frame,
                           text=text,
                           command=command,
                           style='SideMenu.TButton')
            btn.pack(fill=tk.X, pady=4, padx=10)
        
        # Logout button at bottom
        ttk.Frame(sidebar, height=20, style='SideMenu.TFrame').pack(fill=tk.X)  # Spacer
        
        logout_btn = ttk.Button(sidebar,
                              text="🚪 Logout",
                              command=self.logout,
                              style='SideMenu.TButton')
        logout_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Main content area
        self.main_content_frame = ttk.Frame(self.dashboard_frame_obj, style='TFrame')
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Add some padding to the main content
        self.main_content_frame.columnconfigure(0, weight=1)
        self.main_content_frame.rowconfigure(0, weight=1)

    def update_dashboard_summary(self):
        """Update the dashboard summary with current financial data"""
        if not hasattr(self, 'welcome_label') or not hasattr(self, 'total_balance_label'):
            return
            
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = float(user_data.get('monthly_income', 0))
        expenses = user_data.get('expenses', [])
        
        # Calculate total expenses and remaining balance
        total_expenses = sum(float(expense.get('amount', 0)) for expense in expenses)
        remaining_balance = monthly_income - total_expenses
        
        # Update the welcome label with user's name
        if self.logged_in_user:
            full_name = user_data.get('full_name', self.logged_in_user)
            self.welcome_label.config(text=f"Hello, {full_name.split()[0]}!")
        
        # Update the total balance label
        if hasattr(self, 'total_balance_label') and self.total_balance_label.winfo_exists():
            self.total_balance_label.config(
                text=f"Current Balance: ₹{remaining_balance:,.2f}",
                foreground="green" if remaining_balance >= 0 else "red"
            )
        
        # If there are expense summary labels, update them too
        if hasattr(self, 'expense_summary_frame') and self.expense_summary_frame.winfo_exists():
            for widget in self.expense_summary_frame.winfo_children():
                widget.destroy()
                
            # Create summary cards
            cards = [
                ("💰 Monthly Income", f"₹{monthly_income:,.2f}", self.accent_color),
                ("💸 Total Expenses", f"₹{total_expenses:,.2f}", self.warning_color),
                ("💵 Remaining", f"₹{remaining_balance:,.2f}", 
                 self.success_color if remaining_balance >= 0 else self.error_color)
            ]
            
            for i, (title, value, color) in enumerate(cards):
                card = ttk.Frame(self.expense_summary_frame, style='Card.TFrame', padding=10)
                card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
                self.expense_summary_frame.columnconfigure(i, weight=1)
                
                ttk.Label(card, text=title, font=('Segoe UI', 10), style='TLabel').pack()
                ttk.Label(card, text=value, font=('Segoe UI', 14, 'bold'), 
                         foreground=color, style='TLabel').pack(pady=(5, 0))

    def show_dashboard_screen(self):
        if self.logged_in_user:
            # Update welcome message with user's name if available
            users = self.load_users()
            user_data = users.get(self.logged_in_user, {})
            full_name = user_data.get('full_name', self.logged_in_user)
            self.welcome_label.config(text=f"Hello, {full_name.split()[0]}!")

        # Show the dashboard frame
        self.show_frame(self.dashboard_frame_obj)
        
        # Clear main content and add a summary frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
            
        # Create a container for the dashboard content
        content_container = ttk.Frame(self.main_content_frame, padding=20)
        content_container.pack(expand=True, fill='both')
        
        # Add a summary section
        summary_frame = ttk.LabelFrame(content_container, text="Financial Summary", padding=10)
        summary_frame.pack(fill='x', pady=(0, 20))
        
        # Add a frame for the summary cards
        self.expense_summary_frame = ttk.Frame(summary_frame)
        self.expense_summary_frame.pack(fill='x', pady=10)
        
        # Add a welcome message
        welcome_msg = """
        Welcome to MoneyBeast Empire!
        
        Get started by adding your expenses, setting your monthly income, 
        or checking your financial reports using the menu on the left.
        """
        
        ttk.Label(
            content_container, 
            text=welcome_msg.strip(),
            justify='center',
            font=('Segoe UI', 12),
            style='TLabel'
        ).pack(pady=20)
        
        # Update the dashboard summary
        self.update_dashboard_summary()
        
        # Clear the main content area
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
        
        # Create a welcome card
        welcome_card = ttk.Frame(self.main_content_frame, style='Card.TFrame', padding=30)
        welcome_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Welcome message
        ttk.Label(welcome_card,
                 text="👋 Welcome to Finance Manager",
                 style='Header.TLabel').pack(anchor='w', pady=(0, 15))
        
        # Quick stats
        stats_frame = ttk.Frame(welcome_card)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Get user data
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = user_data.get('monthly_income', 0)
        expenses = user_data.get('expenses', [])
        
        # Calculate total expenses
        total_expenses = sum(float(expense['amount']) for expense in expenses)
        remaining_balance = float(monthly_income) - total_expenses if monthly_income else 0
        
        # Stats cards
        stats = [
            (f"₹{float(monthly_income):,.2f}", "Monthly Income", self.accent_color),
            (f"₹{total_expenses:,.2f}", "Total Expenses", self.warning_color),
            (f"₹{remaining_balance:,.2f}", "Remaining Balance", 
             self.success_color if remaining_balance >= 0 else self.error_color)
        ]
        
        for value, label, color in stats:
            card = ttk.Frame(stats_frame, style='Card.TFrame', padding=15)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            ttk.Label(card, 
                     text=value,
                     font=('Segoe UI', 16, 'bold'),
                     foreground=color).pack(anchor='w')
            
            ttk.Label(card,
                     text=label,
                     font=('Segoe UI', 9),
                     foreground='#666').pack(anchor='w')
        
        # Recent transactions
        if expenses:
            ttk.Label(welcome_card, 
                     text="Recent Transactions",
                     font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(30, 10))
            
            # Create a frame for the transactions table
            table_frame = ttk.Frame(welcome_card, style='Card.TFrame')
            table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Create a treeview with scrollbars
            columns = ("Date", "Description", "Category", "Amount")
            tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Treeview')
            
            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=tk.W)
            
            # Add recent transactions (last 5)
            for expense in expenses[-5:][::-1]:  # Show most recent first
                tree.insert('', 'end', values=(
                    expense['date'],
                    expense['description'][:30] + '...' if len(expense['description']) > 30 else expense['description'],
                    expense['category'],
                    f"${float(expense['amount']):,.2f}"
                ))
            
            # Add scrollbars
            vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            
            # Grid the tree and scrollbars
            tree.grid(row=0, column=0, sticky='nsew')
            vsb.grid(row=0, column=1, sticky='ns')
            hsb.grid(row=1, column=0, sticky='ew')
            
            # Configure grid weights
            table_frame.grid_rowconfigure(0, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)
            
            # Add a view all button
            view_all_btn = ttk.Button(welcome_card,
                                    text="View All Transactions",
                                    command=self.show_check_report_screen,
                                    style='TButton')
            view_all_btn.pack(anchor='e', pady=(10, 0))

    def create_add_expense_screen(self):
        # Configure the main container
        self.add_expense_frame_obj.columnconfigure(0, weight=1)
        self.add_expense_frame_obj.rowconfigure(0, weight=1)
        
        # Create a card for the form
        form_card = ttk.Frame(self.add_expense_frame_obj, style='Card.TFrame', padding=30)
        form_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_card.columnconfigure(1, weight=1)
        
        # Title
        ttk.Label(form_card, 
                 text="➕ Add New Expense", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")
        
        # Description Field
        desc_frame = ttk.Frame(form_card)
        desc_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        ttk.Label(desc_frame, 
                 text="Description", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.expense_desc_entry = ttk.Entry(desc_frame, font=('Segoe UI', 11))
        self.expense_desc_entry.pack(fill=tk.X, pady=0)
        
        # Amount and Category in a row
        input_row = ttk.Frame(form_card)
        input_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Amount Field
        amount_frame = ttk.Frame(input_row)
        amount_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Label(amount_frame, 
                 text="Amount", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        amount_container = ttk.Frame(amount_frame)
        amount_container.pack(fill=tk.X)
        
        # Add dollar sign prefix to amount
        ttk.Label(amount_container, 
                 text="$", 
                 font=('Segoe UI', 12, 'bold'),
                 foreground='#666').pack(side=tk.LEFT, padx=(5, 0))
        
        self.expense_amount_entry = ttk.Entry(amount_container, 
                                           font=('Segoe UI', 11),
                                           justify=tk.RIGHT)
        self.expense_amount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Category Field
        category_frame = ttk.Frame(input_row)
        category_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        ttk.Label(category_frame, 
                 text="Category", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        # Common expense categories
        categories = ["Food & Dining", "Shopping", "Transportation", "Bills & Utilities", 
                     "Entertainment", "Travel", "Healthcare", "Education", "Gifts & Donations", "Other"]
        
        self.expense_category_entry = ttk.Combobox(category_frame, 
                                                 values=categories,
                                                 font=('Segoe UI', 11),
                                                 state='normal')
        self.expense_category_entry.pack(fill=tk.X, pady=0)
        self.expense_category_entry.set("Select a category")
        
        # Buttons
        button_frame = ttk.Frame(form_card)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=(10, 0))
        
        ttk.Button(button_frame, 
                  text="← Back to Dashboard", 
                  command=self.show_dashboard_screen,
                  style='TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="💾 Save Expense", 
                  command=self.save_expense,
                  style='Rounded.TButton').pack(side=tk.LEFT)
        
        # Focus the description field by default
        self.expense_desc_entry.focus_set()

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
        # Configure the main container
        self.monthly_income_frame_obj.columnconfigure(0, weight=1)
        self.monthly_income_frame_obj.rowconfigure(0, weight=1)
        
        # Create a card for the form
        form_card = ttk.Frame(self.monthly_income_frame_obj, style='Card.TFrame', padding=30)
        form_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_card.columnconfigure(1, weight=1)
        
        # Title
        ttk.Label(form_card, 
                 text="💰 Monthly Income", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")
        
        # Current Income Display
        current_income_frame = ttk.Frame(form_card, style='Card.TFrame', padding=15)
        current_income_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 30))
        
        ttk.Label(current_income_frame, 
                 text="Current Monthly Income",
                 font=('Segoe UI', 10, 'bold'),
                 foreground='#666').pack(anchor='w')
        
        self.current_income_display = ttk.Label(current_income_frame,
                                              text="Not set",
                                              font=('Segoe UI', 18, 'bold'),
                                              foreground=self.accent_color)
        self.current_income_display.pack(anchor='w', pady=(5, 0))
        
        # Income Input
        input_frame = ttk.Frame(form_card)
        input_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 30))
        
        ttk.Label(input_frame,
                 text="Update Monthly Income",
                 font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 15))
        
        # Amount input with dollar sign
        amount_frame = ttk.Frame(input_frame)
        amount_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(amount_frame, 
                 text="Amount", 
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        amount_container = ttk.Frame(amount_frame)
        amount_container.pack(fill=tk.X)
        
        # Add dollar sign prefix to amount
        ttk.Label(amount_container, 
                 text="$", 
                 font=('Segoe UI', 14, 'bold'),
                 foreground='#666').pack(side=tk.LEFT, padx=(5, 0))
        
        self.income_entry = ttk.Entry(amount_container, 
                                    font=('Segoe UI', 14),
                                    justify=tk.LEFT)
        self.income_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.income_entry.insert(0, "0.00")
        
        # Add note
        ttk.Label(input_frame,
                 text="This will be used to calculate your monthly budget and spending limits.",
                 font=('Segoe UI', 9),
                 foreground='#666').pack(anchor='w', pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(form_card)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=(10, 0))
        
        ttk.Button(button_frame, 
                  text="← Back to Dashboard", 
                  command=self.show_dashboard_screen,
                  style='TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="💾 Save Income", 
                  command=self.save_income,
                  style='Rounded.TButton').pack(side=tk.LEFT)
        
        # Focus the income entry field by default
        self.income_entry.focus_set()
        self.income_entry.select_range(0, tk.END)

    def show_monthly_income_screen(self):
        self.show_content_frame("monthly_income")
        self.load_and_display_income()
        self.income_entry.focus_set()
        self.income_entry.select_range(0, tk.END)
        
    def show_check_report_screen(self):
        self.show_content_frame("check_report")
        self.update_report()

    def create_check_report_screen(self):
        self.check_report_frame_obj.grid_columnconfigure(0, weight=1)
        self.check_report_frame_obj.grid_rowconfigure(5, weight=1)

        # Header
        ttk.Label(self.check_report_frame_obj, text="Financial Report", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")
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

        # Update label with better visibility
        ttk.Label(progress_frame, 
                 text="Budget Utilization:", 
                 font=("Arial", 11, "bold"),
                 foreground=self.text_color).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Update canvas with better contrast
        self.progress_canvas = tk.Canvas(progress_frame, height=40, bg='#f0f0f0', highlightthickness=1, highlightbackground='#d0d0d0')
        self.progress_canvas.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        # Update percentage label with better styling
        self.progress_percentage_label = ttk.Label(
            progress_frame, 
            text="", 
            font=("Arial", 10, "italic"),
            foreground=self.text_color
        )
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

        # Buttons
        button_frame = ttk.Frame(self.check_report_frame_obj)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        ttk.Button(button_frame, 
                  text="← Back to Dashboard", 
                  command=self.show_dashboard_screen,
                  style='TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, 
                  text="🔄 Refresh", 
                  command=self.update_report,
                  style='TButton').pack(side=tk.LEFT)
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
        progress_frame = ttk.Frame(self.check_report_frame_obj)
        progress_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        # Use accent_color instead of primary_color
        self.progress_canvas = tk.Canvas(progress_frame, height=40, bg=self.accent_color, highlightthickness=0)
        self.progress_canvas.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.progress_percentage_label = ttk.Label(progress_frame, text="", font=("Arial", 10, "italic"))
        self.progress_percentage_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)

        # Expense Breakdown Section
        ttk.Label(self.check_report_frame_obj, text="📋 Expense Breakdown by Category", style='Subheader.TLabel').grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        # Category Details Frame with Canvas for visual bars
        category_frame = ttk.Frame(self.check_report_frame_obj)
        category_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        category_frame.grid_columnconfigure(0, weight=1)

        self.category_canvas = tk.Canvas(category_frame, bg=self.accent_color, highlightthickness=0, height=200)
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
        
        # Get user data and calculate financials
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = float(user_data.get('monthly_income', 0.0))
        expenses = user_data.get('expenses', [])
        total_expenses = sum(float(expense.get('amount', 0.0)) for expense in expenses)
        remaining_balance = monthly_income - total_expenses
        
        # Update income and balance labels
        if hasattr(self, 'current_income_label') and self.current_income_label is not None:
            self.current_income_label.config(text=f"₹{monthly_income:,.2f}")
        if hasattr(self, 'total_balance_label') and self.total_balance_label is not None:
            self.total_balance_label.config(
                text=f"₹{remaining_balance:,.2f}",
                foreground=self.success_color if remaining_balance >= 0 else self.error_color
            )

    def update_report(self):
        # Update the report content with current data
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = float(user_data.get('monthly_income', 0.0))
        expenses = user_data.get('expenses', [])
        
        # Calculate totals
        total_expenses = sum(float(expense.get('amount', 0.0)) for expense in expenses)
        remaining_balance = monthly_income - total_expenses
        
        # Update the summary cards
        if hasattr(self, 'report_income_label') and self.report_income_label.winfo_exists():
            self.report_income_label.config(text=f"₹{monthly_income:,.2f}")
        
        if hasattr(self, 'report_expenses_label') and hasattr(self.report_expenses_label, 'winfo_exists') and self.report_expenses_label.winfo_exists():
            self.report_expenses_label.config(text=f"₹{total_expenses:,.2f}")
        
        if hasattr(self, 'report_balance_label') and hasattr(self.report_balance_label, 'winfo_exists') and self.report_balance_label.winfo_exists():
            self.report_balance_label.config(
                text=f"₹{remaining_balance:,.2f}",
                foreground=self.success_color if remaining_balance >= 0 else self.error_color
            )
        
        # Update the detailed content
        self.update_report_content()
    
    def update_report_content(self):
        # Fetch data
        users = self.load_users()
        user_data = users.get(self.logged_in_user, {})
        monthly_income = float(user_data.get('monthly_income', 0.0))
        expenses = user_data.get('expenses', [])
        
        # Calculate totals
        total_expenses = sum(float(expense.get('amount', 0.0)) for expense in expenses)
        remaining_balance = monthly_income - total_expenses
        
        # Update progress bar
        self.progress_canvas.delete("all")
        canvas_width = self.progress_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 600  # Default width

        if monthly_income > 0:
            utilization_percentage = min((total_expenses / monthly_income) * 100, 100)
            bar_width = (canvas_width - 20) * (utilization_percentage / 100)

            # Background bar
            self.progress_canvas.create_rectangle(10, 10, canvas_width - 10, 30,
                                                fill="#e0e0e0", outline="")

            # Progress bar with color based on utilization
            if utilization_percentage <= 50:
                bar_color = self.success_color
            elif utilization_percentage <= 80:
                bar_color = self.warning_color
            else:
                bar_color = self.error_color

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
            
        # Update category breakdown
        self.update_category_breakdown(expenses, total_expenses)
        
        # Update detailed report
        self.update_detailed_report(monthly_income, total_expenses, remaining_balance, expenses)
            
        # Update category breakdown
        self.update_category_breakdown(expenses, total_expenses)
        
        # Update detailed text report
        self.update_detailed_report(monthly_income, total_expenses, remaining_balance, expenses)
    
    def update_category_breakdown(self, expenses, total_expenses):
        # Calculate expenses by category
        expenses_by_category = {}
        for expense in expenses:
            category = expense.get('category', 'Uncategorized')
            amount = float(expense.get('amount', 0.0))
            if category in expenses_by_category:
                expenses_by_category[category] += amount
            else:
                expenses_by_category[category] = amount
        
        # Clear previous content
        self.category_canvas.delete("all")
        canvas_width = self.category_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 600  # Default width
            
        if not expenses_by_category:
            self.category_canvas.create_text(canvas_width // 2, 100,
                                          text="No expenses recorded yet",
                                          fill=self.text_color, font=("Arial", 12))
            return
            
        # Sort categories by amount (descending)
        sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
        
        # Draw category bars
        bar_height = 30
        spacing = 10
        y_offset = 10
        colors = ["#4a90e2", "#e74c3c", "#f39c12", "#2ecc71", "#9b59b6", "#1abc9c", "#e67e22"]
        max_amount = max(expenses_by_category.values()) if expenses_by_category else 1
        
        for idx, (category, amount) in enumerate(sorted_categories):
            if idx >= 7:  # Limit to top 7 categories
                break
                
            # Calculate bar width
            bar_width = (canvas_width - 200) * (amount / max_amount) if max_amount > 0 else 0
            
            # Draw category name
            self.category_canvas.create_text(10, y_offset + bar_height // 2,
                                          text=category,
                                          anchor=tk.W,
                                          fill=self.text_color,
                                          font=("Arial", 10))
            
            # Draw bar
            color = colors[idx % len(colors)]
            self.category_canvas.create_rectangle(150, y_offset,
                                               150 + bar_width, y_offset + bar_height - 5,
                                               fill=color, outline="")
            
            # Draw amount and percentage
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            amount_text = f"₹{amount:,.2f} ({percentage:.1f}%)"
            self.category_canvas.create_text(160 + bar_width, y_offset + bar_height // 2,
                                          text=amount_text,
                                          anchor=tk.W,
                                          fill=self.text_color,
                                          font=("Arial", 9))
            
            y_offset += bar_height + spacing
    
    def update_detailed_report(self, monthly_income, total_expenses, remaining_balance, expenses):
        # Clear previous content
        self.report_text_widget.config(state=tk.NORMAL)
        self.report_text_widget.delete(1.0, tk.END)
        
        # Add header
        self.report_text_widget.insert(tk.END, "Financial Summary\n", "header")
        self.report_text_widget.insert(tk.END, "="*50 + "\n\n")
        
        # Add summary section
        self.report_text_widget.insert(tk.END, "• Monthly Income: ", "bold")
        self.report_text_widget.insert(tk.END, f"₹{monthly_income:,.2f}\n")
        
        self.report_text_widget.insert(tk.END, "• Total Expenses: ", "bold")
        self.report_text_widget.insert(tk.END, f"₹{total_expenses:,.2f}\n")
        
        self.report_text_widget.insert(tk.END, "• Remaining Balance: ", "bold")
        balance_tag = "ok" if remaining_balance >= 0 else "bad"
        self.report_text_widget.insert(tk.END, f"₹{remaining_balance:,.2f}\n\n", balance_tag)
        
        # Add recent transactions
        if expenses:
            self.report_text_widget.insert(tk.END, "Recent Transactions\n", "header")
            self.report_text_widget.insert(tk.END, "-"*50 + "\n")
            
            # Sort by date (newest first)
            sorted_expenses = sorted(expenses, 
                                  key=lambda x: x.get('date', ''), 
                                  reverse=True)[:10]  # Show last 10 transactions
            
            for expense in sorted_expenses:
                date = expense.get('date', 'No Date')
                desc = expense.get('description', 'No Description')
                amount = float(expense.get('amount', 0))
                category = expense.get('category', 'Uncategorized')
                
                self.report_text_widget.insert(tk.END, f"• {date} - {desc[:30]}", "bold")
                self.report_text_widget.insert(tk.END, f" (₹{amount:,.2f})\n", "mono")
        else:
            self.report_text_widget.insert(tk.END, "No transactions recorded yet.\n")
        
        # Add financial health status
        if monthly_income > 0:
            self.report_text_widget.insert(tk.END, "\nFinancial Health\n", "header")
            self.report_text_widget.insert(tk.END, "-"*50 + "\n")
            
            savings_ratio = (remaining_balance / monthly_income) * 100
            if savings_ratio >= 20:
                status = "Excellent"
                status_tag = "ok"
            elif savings_ratio >= 10:
                status = "Good"
                status_tag = "ok"
            elif savings_ratio >= 0:
                status = "Needs Improvement"
                status_tag = "warn"
            else:
                status = "Critical (Overspending)"
                status_tag = "bad"
            
            self.report_text_widget.insert(tk.END, f"Status: ", "bold")
            self.report_text_widget.insert(tk.END, f"{status}\n", status_tag)
            
            if savings_ratio >= 0:
                self.report_text_widget.insert(tk.END, f"You're saving ", "label")
                self.report_text_widget.insert(tk.END, f"{savings_ratio:.1f}%", status_tag)
                self.report_text_widget.insert(tk.END, " of your income\n")
            else:
                overspend = abs(savings_ratio)
                self.report_text_widget.insert(tk.END, f"You're overspending by ", "label")
                self.report_text_widget.insert(tk.END, f"{overspend:.1f}%", status_tag)
                self.report_text_widget.insert(tk.END, " of your income\n")
        
        # Disable editing
        self.report_text_widget.config(state=tk.DISABLED)

        # Calculate expenses by category
        expenses_by_category = {}
        for expense in expenses:
            category = expense.get('category', 'Uncategorized')
            amount = float(expense.get('amount', 0.0))
            expenses_by_category[category] = expenses_by_category.get(category, 0) + amount

        # Draw category breakdown bars
        self.category_canvas.delete("all")
        canvas_width = self.category_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 600

        if expenses_by_category:
            sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
            max_amount = max(expenses_by_category.values()) if expenses_by_category else 1
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
                                              text=f"₹{amount:,.2f} ({percentage:.1f}%)",
                                              anchor="w", fill=self.text_color, font=("Arial", 9))

                y_offset += bar_height + 10
        else:
            self.category_canvas.create_text(canvas_width // 2, 100,
                                          text="No expenses recorded yet",
                                          fill=self.text_color, font=("Arial", 12))

        # Configure text widget colors for better visibility
        self.report_text_widget.config(
            state=tk.NORMAL,
            background='white',  # Set background to white
            foreground='#333333',  # Dark gray for better readability
            font=('Segoe UI', 10),  # Clean, readable font
            padx=10,  # Add some padding
            pady=10,
            wrap=tk.WORD  # Wrap text at word boundaries
        )
        
        # Configure text tags for styling
        self.report_text_widget.tag_configure('header', font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.report_text_widget.tag_configure('bold', font=('Segoe UI', 10, 'bold'))
        self.report_text_widget.tag_configure('ok', foreground='#27ae60')  # Green for positive
        self.report_text_widget.tag_configure('warn', foreground='#f39c12')  # Orange for warning
        self.report_text_widget.tag_configure('bad', foreground='#e74c3c')  # Red for negative
        self.report_text_widget.tag_configure('label', foreground='#7f8c8d')
        self.report_text_widget.tag_configure('mono', font=('Consolas', 10))
        
        # Clear existing content
        self.report_text_widget.delete(1.0, tk.END)

        # Header
        self.report_text_widget.insert(tk.END, "MONTHLY FINANCIAL ANALYTICS\n", "header")
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
        monthly_income = user_data.get('monthly_income', 0)
        if monthly_income:
            formatted_income = f"${float(monthly_income):,.2f}"
            self.current_income_display.config(text=formatted_income)
            self.income_entry.delete(0, tk.END)
            self.income_entry.insert(0, monthly_income)
        else:
            self.current_income_display.config(text="Not set", foreground='#999')
            self.income_entry.delete(0, tk.END)
            self.income_entry.insert(0, "0.00")

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