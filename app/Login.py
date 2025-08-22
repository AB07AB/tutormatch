import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, auth
import sqlite3
from EditProfile import EditProfileScreen

if not firebase_admin._apps:
    cred = credentials.Certificate("config/firebase_config.json")
    firebase_admin.initialize_app(cred)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def authenticate(self):
        try:
            user = auth.get_user_by_email(self.email)
            return user is not None
        except Exception:
            return False

class UserDatabase:
    def __init__(self, db_path="teacher_data.db"):
        self.db_path = db_path

    def get_user_by_name(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE name=?", (name,))
        user_data = cursor.fetchone()
        conn.close()
        return user_data

class LoginScreen(tk.Frame):
    def __init__(self, container):
        super().__init__(container, bg="white")
        self.container = container
        self.user_db = UserDatabase()

        self.font_title = tkfont.Font(family="Inter 18pt", size=20, weight="bold")
        self.font_subtitle = tkfont.Font(family="Inter 18pt", size=14, weight="bold")
        self.register_text = tkfont.Font(family="Inter 18pt", size=14)

        content_frame = tk.Frame(self, bg="white")
        content_frame.pack(expand=True)

        entry_frame = tk.Frame(content_frame, bg="white")
        entry_frame.pack()

        tk.Label(entry_frame, text="Welcome back teacher, Login!", bg="white", font=self.font_title, fg="black").grid(row=0, column=0, sticky="w", padx=5, pady=(10, 10))

        tk.Label(entry_frame, text="Full Name", bg="white", font=self.font_subtitle, fg="black").grid(row=1, column=0, sticky="w", padx=5, pady=(5, 2))
        self.name_entry = tk.Entry(entry_frame, width=37, font=('Inter', 17))
        self.name_entry.grid(row=2, column=0, padx=5, pady=(0, 15))

        tk.Label(entry_frame, text="Email", bg="white", font=self.font_subtitle, fg="black").grid(row=3, column=0, sticky="w", padx=5, pady=(5, 2))
        self.email_entry = tk.Entry(entry_frame, width=37, font=('Inter', 17))
        self.email_entry.grid(row=4, column=0, padx=5, pady=(5, 15))

        tk.Label(entry_frame, text="Password", bg="white", font=self.font_subtitle, fg="black").grid(row=5, column=0, sticky="w", padx=5, pady=(5, 2))
        self.password_entry = tk.Entry(entry_frame, width=37, show="*", font=('Inter', 17))
        self.password_entry.grid(row=6, column=0, padx=5, pady=(5, 30))

        login_image = Image.open("config/images/LoginButton.png")
        login_image = login_image.resize((450, 60))
        login_photo = ImageTk.PhotoImage(login_image)

        login_button = tk.Button(content_frame, image=login_photo, command=self.login, borderwidth=0, relief="flat", bg="white")
        login_button.image = login_photo 
        login_button.pack(pady=(20, 15))

        bottom_frame = tk.Frame(content_frame, bg="white")
        bottom_frame.pack(pady=(10, 20))

        register_label = tk.Label(bottom_frame, text="Haven't registered yet?", font=self.register_text, bg="white", fg="#606060")
        register_label.pack(side=tk.LEFT, padx=(0, 3))

        register_button = tk.Button(bottom_frame, text="Register", font=self.register_text, bg="white", fg="#9344ec", activebackground="white", activeforeground="#9344ec", bd=0, cursor="hand2", command=self.go_back)
        register_button.pack(side=tk.LEFT)

        self.pack(expand=True)

    def login(self):
        full_name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not full_name or not email or not password:
            messagebox.showerror("Error", "Please enter your full name, email, and password")
            return

        user = User(full_name, email, password)

        if not user.authenticate():
            messagebox.showerror("Login Failed", "Invalid email or password")
            return

        user_data = self.user_db.get_user_by_name(full_name)

        if user_data:
            self.navigate_to_edit_profile(user_data)
        else:
            messagebox.showerror("Error", "User not found in the database")

    def navigate_to_edit_profile(self, user_data):
        self.pack_forget()
        EditProfileScreen(self.container, user_data).pack()

    def go_back(self):
        self.pack_forget()
        self.container.winfo_toplevel().app.back_to_welcome()