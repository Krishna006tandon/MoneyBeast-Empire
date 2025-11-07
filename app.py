
import tkinter as tk
from tkinter import messagebox
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
        tk.Button(self.dashboard_frame, text="Logout", command=self.logout).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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

        users[username] = {"password": password, "full_name": full_name}

        with open("user_data.pkl", "wb") as f:
            pickle.dump(users, f)

        messagebox.showinfo("Success", "Signup successful! Please login.")
        self.show_login_screen()

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
