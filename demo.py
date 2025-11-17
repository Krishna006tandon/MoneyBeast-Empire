import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# =============================
# Apply Light Modern Theme
# =============================
def apply_modern_theme(root):
    root.configure(bg="#fafafa")

    root.option_add("*Background", "#fafafa")
    root.option_add("*Foreground", "#1a1a1a")
    root.option_add("*Font", ("Segoe UI", 10))

    root.option_add("*Entry.Background", "#ffffff")
    root.option_add("*Entry.Foreground", "#1a1a1a")

    root.option_add("*Button.Background", "#d9e7ff")
    root.option_add("*Button.Foreground", "#000000")
    root.option_add("*Button.ActiveBackground", "#bcd6ff")

    root.option_add("*Listbox.Background", "#ffffff")
    root.option_add("*Listbox.Foreground", "#000000")

# =============================
# Main Application Window
# =============================
def open_finance_manager():
    file_name = "Finance_Data.xlsx"

    if not os.path.isfile(file_name):
        df = pd.DataFrame(columns=["Date", "Category", "Amount"])
        df.to_excel(file_name, index=False)

    root = tk.Tk()
    root.title("Finance Manager")

    apply_modern_theme(root)

    # =============================
    # Input Fields
    # =============================
    tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=5)
    entry_date = tk.Entry(root)
    entry_date.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Category").grid(row=1, column=0, padx=10, pady=5)
    entry_category = tk.Entry(root)
    entry_category.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Amount").grid(row=2, column=0, padx=10, pady=5)
    entry_amount = tk.Entry(root)
    entry_amount.grid(row=2, column=1, padx=10, pady=5)

    # =============================
    # Function to Add Entry
    # =============================
    def add_entry():
        date = entry_date.get()
        category = entry_category.get()
        amount = entry_amount.get()

        if not date or not category or not amount:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number.")
            return

        df = pd.read_excel(file_name)
        new_data = pd.DataFrame([[date, category, amount]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(file_name, index=False)

        messagebox.showinfo("Success", "Entry added!")

        entry_date.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_amount.delete(0, tk.END)

        load_data()

    tk.Button(root, text="Add Entry", command=add_entry).grid(row=3, column=0, columnspan=2, pady=10)

    # =============================
    # Listbox to Display Entries
    # =============================
    listbox = tk.Listbox(root, width=50)
    listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # =============================
    # Load and Refresh Data
    # =============================
    def load_data():
        listbox.delete(0, tk.END)

        if os.path.isfile(file_name):
            df = pd.read_excel(file_name)
            for index, row in df.iterrows():
                listbox.insert(
                    tk.END,
                    f"{row['Date']} | {row['Category']} | {row['Amount']}"
                )

    load_data()

    root.mainloop()

# Start App
open_finance_manager()