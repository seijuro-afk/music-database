import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Function to handle the signup
def signup(db, username, email, password):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Accounts (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        messagebox.showinfo("Signup", "Account created successfully!")
    except mysql.connector.Error as e:
        messagebox.showerror("Signup Error", f"Error: {e}")
    finally:
        cursor.close()

# Function to handle login
def authenticate(db, email, password):
    cursor = db.cursor()
    cursor.execute("SELECT username FROM Accounts WHERE email = %s AND password = %s", (email, password))
    account = cursor.fetchone()
    cursor.close()
    return account[0] if account else None

# Function to show the login screen
def login_screen(db, start_main_app_callback):
    login_root = tk.Tk()
    login_root.title("Signup/ Login Frame")
    login_root.geometry("400x300")
    login_root.configure(bg="#1a1a1a")
    
    # Dark theme setup
    label_font = ("Arial", 12)
    entry_bg = "#333333"
    entry_fg = "#ffffff"

    # Username entry for signup
    tk.Label(login_root, text="Username", font=label_font, fg=entry_fg, bg="#1a1a1a").grid(row=0, column=0, pady=10, padx=10)
    entry_username = tk.Entry(login_root, font=label_font, bg=entry_bg, fg=entry_fg)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    # Email entry for login/signup
    tk.Label(login_root, text="Email", font=label_font, fg=entry_fg, bg="#1a1a1a").grid(row=1, column=0, pady=10, padx=10)
    entry_email = tk.Entry(login_root, font=label_font, bg=entry_bg, fg=entry_fg)
    entry_email.grid(row=1, column=1, padx=10, pady=10)

    # Password entry
    tk.Label(login_root, text="Password", font=label_font, fg=entry_fg, bg="#1a1a1a").grid(row=2, column=0, pady=10, padx=10)
    entry_password = tk.Entry(login_root, show="*", font=label_font, bg=entry_bg, fg=entry_fg)
    entry_password.grid(row=2, column=1, padx=10, pady=10)

    # Signup and Login buttons
    def on_signup():
        signup(db, entry_username.get(), entry_email.get(), entry_password.get())

    def on_login():
        username = authenticate(db, entry_email.get(), entry_password.get())
        if username:
            messagebox.showinfo("Login", "Login successful!")
            login_root.destroy()  # Close login window
            start_main_app_callback(username)  # Start the main app with the username
        else:
            messagebox.showerror("Login", "Invalid email or password.")

    tk.Button(login_root, text="Sign Up", command=on_signup, bg="#555555", fg=entry_fg, font=label_font).grid(row=3, column=0, pady=20)
    tk.Button(login_root, text="Login", command=on_login, bg="#555555", fg=entry_fg, font=label_font).grid(row=3, column=1, pady=20)

    login_root.mainloop()
