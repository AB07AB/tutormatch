import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import sqlite3

import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("config/firebase_config.json")
firebase_admin.initialize_app(cred)

class SignUpTeacherScreen(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        self.container.configure(bg="white")
        self.configure(bg="white")

        self.font_title = tkfont.Font(family="Inter 18pt", size=20, weight="bold")
        self.font_subtitle = tkfont.Font(family="Inter 18pt", size=14)
        self.font_loginbutton = tkfont.Font(family="Inter 18pt", size=15)

        self.name_frame = tk.Frame(self, bg="white")
        self.email_frame = tk.Frame(self, bg="white")
        self.password_frame = tk.Frame(self, bg="white")
        self.profile_picture_frame = tk.Frame(self, bg="white")
        self.qualifications_frame = tk.Frame(self, bg="white")
        self.role_frame = tk.Frame(self, bg="white")

        self.selected_subjects = []
        self.profile_picture_path = ""

        self.create_db()
        self.create_name_frame()

    def create_db(self):
        self.conn = sqlite3.connect('teacher_data.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            profile_picture_path TEXT,
            subjects TEXT,
            hourly_rate REAL,
            qualifications TEXT,
            school TEXT,
            email TEXT
        )
        ''')

        self.conn.commit()

    def validate_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Name field cannot be empty!")
            return False
        return True
    
    def validate_email(self):
        email = self.email_entry.get().strip()
        if not email or "@" not in email or "." not in email:
            messagebox.showerror("Input Error", "Please enter a valid email address!")
            return False
        return True
    
    def validate_hourly_rate(self):
        try:
            rate = float(self.hourly_rate_entry.get().strip())
            if rate <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Hourly rate must be a positive number!")
            return False
        return True

    def create_name_frame(self):
        name_frame_left = tk.Frame(self.name_frame, bg="white")
        name_frame_left.pack(padx=0, pady=0, anchor="w")

        label = tk.Label(name_frame_left, text="What's your name?", font=self.font_title, bg="white", fg="black")
        label.pack(side=tk.TOP, pady=(40,10), anchor="w") 

        entryText = tk.Label(name_frame_left, text="Full Name", font=self.font_subtitle, bg="white", fg="black")
        entryText.pack(side=tk.TOP, pady=(10,0), anchor="w") 

        self.name_entry = tk.Entry(name_frame_left, width=30, font=('Inter', 16), bg="white", justify="left")
        self.name_entry.pack(side=tk.TOP, pady=(5,5), padx=2, anchor="w", ipadx = 30, ipady = 10)

        next_image = Image.open("config/images/ContinueButton.png")
        next_image = next_image.resize((450, 60))
        next_photo = ImageTk.PhotoImage(next_image)

        next_button = tk.Button(self.name_frame, image=next_photo, command=self.create_email_frame, borderwidth=0, 
                                relief="flat", bg="white")
        next_button.image = next_photo
        next_button.pack(pady=(140, 0))

        login_frame = tk.Frame(self.name_frame, bg="white")
        login_frame.pack(pady=(35, 0))

        login_label = tk.Label(login_frame, text="Already have an account?", font=self.font_loginbutton, bg="white", fg="#606060")
        login_label.pack(side=tk.LEFT, padx=(0, 0))

        login_button = tk.Button(login_frame, text="Login", font=self.font_loginbutton, bg="white", fg="#9344ec", 
                                activebackground="white", activeforeground="#9344ec", bd=0, cursor="hand2", command=self.login)
        login_button.pack(side=tk.LEFT, padx=(0, 0))

        self.name_frame.pack(padx=3, pady=3)

    def create_email_frame(self):
        if not self.validate_name():
            return
        self.name_frame.pack_forget()

        email_frame_left = tk.Frame(self.email_frame, bg="white")
        email_frame_left.pack(padx=0, pady=0, anchor="w")

        label = tk.Label(email_frame_left, text="What's your email?", font=self.font_title, bg="white", fg="black")
        label.pack(side=tk.TOP, pady=(40, 10), anchor="w")

        entryText = tk.Label(email_frame_left, text="Email Address", font=self.font_subtitle, bg="white", fg="black")
        entryText.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        def on_click(event):
            if self.email_entry.get() == "example@gmail.com":
                self.email_entry.delete(0, "end")
                self.email_entry.config(fg="black")

        def on_focusout(event):
            if not self.email_entry.get():
                self.email_entry.insert(0, "example@gmail.com")
                self.email_entry.config(fg="#606060")

        entry_frame = tk.Frame(self.email_frame, bg="white")
        entry_frame.pack(side=tk.TOP, pady=(5, 5), padx=2, anchor="w")

        self.email_entry = tk.Entry(entry_frame, width=30, font=("Inter", 16), fg="#606060", bg="white", justify="left")
        self.email_entry.insert(0, "example@gmail.com")
        self.email_entry.bind("<FocusIn>", on_click)
        self.email_entry.bind("<FocusOut>", on_focusout)
        self.email_entry.pack(side=tk.LEFT, ipadx=30, ipady=10)

        next_image = Image.open("config/images/ContinueButton.png")
        next_image = next_image.resize((450, 60))
        next_photo = ImageTk.PhotoImage(next_image)

        next_button = tk.Button(self.email_frame, image=next_photo, command=self.create_password_frame, borderwidth=0, 
                            relief="flat", bg="white")
        next_button.image = next_photo
        next_button.pack(pady=(140, 0))

        login_frame = tk.Frame(self.email_frame, bg="white")
        login_frame.pack(pady=(35, 0))

        login_label = tk.Label(login_frame, text="Already have an account?", font=self.font_loginbutton, bg="white", fg="#606060")
        login_label.pack(side=tk.LEFT, padx=(0, 0))

        login_button = tk.Button(login_frame, text="Login", font=self.font_loginbutton, bg="white", fg="#9344ec", 
                            activebackground="white", activeforeground="#9344ec", bd=0, cursor="hand2", command=self.login)
        login_button.pack(side=tk.LEFT, padx=(0, 0))

        self.email_frame.pack(padx=3, pady=3)

    def create_password_frame(self):
        if not self.validate_email():
            return
        self.email_frame.pack_forget()
        self.email = self.email_entry.get()

        password_frame_left = tk.Frame(self.password_frame, bg="white")
        password_frame_left.pack(padx=0, pady=0, anchor="w")

        label = tk.Label(password_frame_left, text="Create a Password", font=self.font_title, bg="white", fg="black")
        label.pack(side=tk.TOP, pady=(40, 10), anchor="w")

        password_label = tk.Label(password_frame_left, text="Password", font=self.font_subtitle, bg="white", fg="black")
        password_label.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        self.password_entry = tk.Entry(password_frame_left, width=30, font=('Inter', 16), fg="black", bg="white", show="*", justify="left")
        self.password_entry.pack(side=tk.TOP, pady=(5, 5), padx=2, anchor="w", ipadx=30, ipady=10)

        confirm_password_label = tk.Label(password_frame_left, text="Confirm Password", font=self.font_subtitle, bg="white", fg="black")
        confirm_password_label.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        self.confirm_password_entry = tk.Entry(password_frame_left, width=30, font=('Inter', 16), fg="black", bg="white", show="*", justify="left")
        self.confirm_password_entry.pack(side=tk.TOP, pady=(5, 5), padx=2, anchor="w", ipadx=30, ipady=10)

        next_image = Image.open("config/images/ContinueButton.png")
        next_image = next_image.resize((450, 60))
        next_photo = ImageTk.PhotoImage(next_image)

        next_button = tk.Button(self.password_frame, image=next_photo, command=self.create_profile_picture_frame, borderwidth=0, 
                                relief="flat", bg="white")
        next_button.image = next_photo
        next_button.pack(pady=(80, 0))

        login_frame = tk.Frame(self.password_frame, bg="white")
        login_frame.pack(pady=(35, 0))

        login_label = tk.Label(login_frame, text="Already have an account?", font=self.font_loginbutton, bg="white", fg="#606060")
        login_label.pack(side=tk.LEFT, padx=(0, 0))

        login_button = tk.Button(login_frame, text="Login", font=self.font_loginbutton, bg="white", fg="#9344ec", 
                                activebackground="white", activeforeground="#9344ec", bd=0, cursor="hand2", command=self.login)
        login_button.pack(side=tk.LEFT, padx=(0, 0))

        self.password_frame.pack(padx=3, pady=3)

    def create_profile_picture_frame(self):
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
        
        try:
            user = auth.create_user(
                email=self.email,
                password=password
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error creating account: {str(e)}")

        self.password_frame.pack_forget()

        label = tk.Label(self.profile_picture_frame, text="Upload Photo", font=self.font_title, bg="white", fg="black")
        label.pack(pady=(10,0), anchor="center")

        sub_label = tk.Label(self.profile_picture_frame, text="Complete the last step !", font=self.font_loginbutton, bg="white", fg="#606060")
        sub_label.pack(pady=(0,15), anchor="center")

        upload_image = Image.open("config/images/UploadPictureButton.png")
        upload_image = upload_image.resize((230, 300))
        upload_photo = ImageTk.PhotoImage(upload_image)

        upload_button = tk.Button(self.profile_picture_frame, image=upload_photo, command=self.upload_profile_picture, borderwidth=0, 
                                relief="flat", bg="white")
        upload_button.image = upload_photo
        upload_button.pack(pady=(0, 0))

        next_image = Image.open("config/images/ContinueButton.png")
        next_image = next_image.resize((450, 60))
        next_photo = ImageTk.PhotoImage(next_image)

        next_button = tk.Button(self.profile_picture_frame, image=next_photo, command=self.create_qualifications_frame, borderwidth=0, 
                                relief="flat", bg="white")
        next_button.image = next_photo
        next_button.pack(pady=(20, 0))

        self.profile_picture_frame.pack(padx=20, pady=20)

    def upload_profile_picture(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.profile_picture_path = file_path
        else:
            messagebox.showwarning("Warning", "No file selected!")

    def create_qualifications_frame(self):
        self.profile_picture_frame.pack_forget()

        qualifications_frame_left = tk.Frame(self.qualifications_frame, bg="white")
        qualifications_frame_left.pack(padx=0, pady=0, anchor="w")

        label = tk.Label(qualifications_frame_left, text="Your Education", font=self.font_title, bg="white", fg="black")
        label.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        sub_label = tk.Label(qualifications_frame_left, text="Provide your educational information", font=self.font_loginbutton, bg="white", fg="#606060")
        sub_label.pack(side=tk.TOP, pady=(5, 0), anchor="w")

        entryText1 = tk.Label(qualifications_frame_left, text="School / University", font=self.font_subtitle, bg="white", fg="black")
        entryText1.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        self.school_entry = tk.Entry(qualifications_frame_left, width=37, font=('Inter', 16), bg="white", justify="left")
        self.school_entry.pack(side=tk.TOP, pady=(5, 5), padx=2, anchor="w", ipadx=30, ipady=10)

        entryText2 = tk.Label(qualifications_frame_left, text="Expertise & Qualifications", font=self.font_subtitle, bg="white", fg="black")
        entryText2.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        def on_click(event):
            if self.qualifications_entry.get("1.0", "end-1c") == "Add here any additional information you would like to include...":
                self.qualifications_entry.delete("1.0", "end")
                self.qualifications_entry.config(fg="black")

        def on_focusout(event):
            if not self.qualifications_entry.get("1.0", "end-1c").strip():
                self.qualifications_entry.insert("1.0", "Add here any additional information you would like to include...")
                self.qualifications_entry.config(fg="#606060")

        def enforce_character_limit(event=None):
            text = self.qualifications_entry.get("1.0", "end-1c")

            if len(text) > 200:
                messagebox.showwarning("Character Limit Exceeded", "You have exceeded the 200-character limit!")
                self.qualifications_entry.delete("1.0", "end")
                self.qualifications_entry.insert("1.0", text[:200])
                return "break"

        entry_frame = tk.Frame(self.qualifications_frame, bg="white")
        entry_frame.pack(side=tk.TOP, pady=(5, 5), padx=2, anchor="w")

        self.qualifications_entry = tk.Text(entry_frame, width=50, height=6, font=("Inter", 12), fg="#606060", bg="white", wrap="word")
        self.qualifications_entry.insert("1.0", "Add here any additional information you would like to include...")
        self.qualifications_entry.bind("<FocusIn>", on_click)
        self.qualifications_entry.bind("<FocusOut>", on_focusout)
        self.qualifications_entry.bind("<KeyRelease>", enforce_character_limit)
        self.qualifications_entry.pack(side=tk.LEFT, ipadx=30, ipady=10)

        next_image = Image.open("config/images/ContinueButton.png")
        next_image = next_image.resize((450, 60))
        next_photo = ImageTk.PhotoImage(next_image)

        next_button = tk.Button(self.qualifications_frame, image=next_photo, command=self.create_role_frame, borderwidth=0, 
                                relief="flat", bg="white")
        next_button.image = next_photo
        next_button.pack(pady=(50, 0))

        self.qualifications_frame.pack(padx=20, pady=20)

    def create_role_frame(self):
        self.qualifications_frame.pack_forget()

        role_frame_left = tk.Frame(self.role_frame, bg="white")
        role_frame_left.pack(padx=0, pady=0, anchor="w")

        label = tk.Label(role_frame_left, text="Your role in TutorMatch", font=self.font_title, bg="white", fg="black")
        label.pack(pady=(10, 0), anchor="w")

        entryText1 = tk.Label(
            role_frame_left,
            text="What subject will you be teaching?",
            font=self.font_subtitle,
            bg="white",
            fg="black",
        )
        entryText1.pack(side=tk.TOP, pady=(10, 0), anchor="w")

        subText1 = tk.Label(role_frame_left, text="Selected all that apply", bg="white", font=("Inter", 12), fg="#555")
        subText1.pack(side=tk.TOP, pady=(3, 5), anchor="w")

        options_frame = tk.Frame(role_frame_left, bg="white", relief="solid", bd=2)
        options_frame.pack(pady=(5, 5), fill=tk.X, anchor="w")

        canvas = tk.Canvas(options_frame, bg="white", height=100, bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(options_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        checkbox_container = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=checkbox_container, anchor="nw")

        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        checkbox_container.bind("<Configure>", update_scroll_region)

        subjects = ["Maths", "English", "Spanish", "Biology", "Chemistry", "Physics", "Computer Science"]
        selected_subjects = []

        for subject in subjects:
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                checkbox_container,
                text=subject,
                variable=var,
                bg="white",
                fg="#333",
                font=("Inter", 12),
                anchor="w",
                command=lambda s=subject, v=var: self.on_check(s, v),
                selectcolor="#c499f8",
                relief="flat",
                padx=5,
                pady=2,
            )
            chk.pack(fill=tk.X, anchor="w", pady=2)

        canvas.configure(yscrollcommand=scrollbar.set)

        entryText2 = tk.Label(role_frame_left, text="Hourly rate", font=self.font_subtitle, bg="white", fg="black")
        entryText2.pack(side=tk.TOP, pady=(10,0), anchor="w") 

        subText2 = tk.Label(role_frame_left, text="Establish a standard hourly rate for your classes", bg="white", font=("Inter", 12), fg="#555")
        subText2.pack(side=tk.TOP, pady=(3, 5), anchor="w")

        self.hourly_rate_entry = tk.Entry(role_frame_left, width=37, font=('Inter', 16), bg="white", justify="left")
        self.hourly_rate_entry.pack(side=tk.TOP, pady=(5,5), padx=2, anchor="w", ipadx = 30, ipady = 10)

        finish_image = Image.open("config/images/FinishButton.png")
        finish_image = finish_image.resize((450, 60))
        finish_photo = ImageTk.PhotoImage(finish_image)

        finish_button = tk.Button(
            self.role_frame,
            image=finish_photo,
            command=self.save_selected_subjects,
            borderwidth=0,
            relief="flat",
            bg="white",
        )
        finish_button.image = finish_photo
        finish_button.pack(pady=(20, 0))

        self.role_frame.pack(padx=20, pady=20)
    
    def on_check(self, subject, var):
        if var.get():
            self.selected_subjects.append(subject)
        else:
            self.selected_subjects.remove(subject)

    def save_selected_subjects(self):
        name = self.name_entry.get()
        school = self.school_entry.get()
        qualifications = self.qualifications_entry.get("1.0", "end-1c").strip() 
        hourly_rate = self.hourly_rate_entry.get()
        profile_picture_path = self.profile_picture_path
        email = self.email_entry.get()

        subjects_string = ','.join(self.selected_subjects) 

        if not name or not school or not hourly_rate: 
            messagebox.showerror("Error", "Please complete all required fields before saving.")
            return

        self.cursor.execute('''
        INSERT INTO user_profiles (name, school, qualifications, hourly_rate, profile_picture_path, email, subjects)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, school, qualifications, hourly_rate, profile_picture_path, email, subjects_string))

        self.conn.commit()

        self.show_success_message()

        print("Saved subjects:", self.selected_subjects) 

    def show_success_message(self):
        self.role_frame.pack_forget()
        
        self.success_frame = tk.Frame(self, background="white")
        self.success_frame.pack(pady=10)

        success_image = Image.open("config/images/Success.png")
        success_image = success_image.resize((480, 450))
        success_photo = ImageTk.PhotoImage(success_image)

        success_label = tk.Label(self.success_frame, image=success_photo, bg="white")
        success_label.image = success_photo
        success_label.pack(pady=(0, 5))

        proceed_image = Image.open("config/images/EditProfileButton.png")
        proceed_image = proceed_image.resize((450, 45))
        proceed_photo = ImageTk.PhotoImage(proceed_image)

        proceed_button = tk.Button(self.success_frame, image=proceed_photo, borderwidth=0, command=self.editProfile,
                                relief="flat", bg="white")
        proceed_button.image = proceed_photo
        proceed_button.pack(pady=(5, 0))

        self.success_frame.pack(padx=20, pady=20)

    def clear_widgets(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def login(self):
        self.clear_widgets()
        self.login_screen()

    def login_screen(self):
        from Login import LoginScreen 
        app = LoginScreen(self.container)
        app.pack(fill="both", expand=True)

    def editProfile(self):
        self.clear_widgets()
        self.editProfile_screen()

    def editProfile_screen(self):
        from Login import LoginScreen
        app = LoginScreen(self.container)
        app.pack(fill="both", expand=True)

root = tk.Tk()
app = SignUpTeacherScreen(root)
root.mainloop()