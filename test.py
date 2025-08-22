import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk 
from collections import deque
import sqlite3

class Profile:
    def __init__(self, user_data):
        (self.user_id, self.name, self.profile_picture, self.subjects, 
         self.hourly_rate, self.qualifications, self.school, self.email) = user_data

    def update_profile(self, new_data):
        try:
            conn = sqlite3.connect("teacher_data.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_profiles 
                SET name=?, school=?, qualifications=?, hourly_rate=?, subjects=?, profile_picture_path=?, email=? 
                WHERE id=?
            ''', new_data)
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def refresh_profile(self):
        try:
            conn = sqlite3.connect("teacher_data.db")
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_profiles WHERE id=?', (self.user_id,))
            user_data = cursor.fetchone()
            conn.close()
            if user_data:
                (self.user_id, self.name, self.profile_picture, self.subjects, 
                 self.hourly_rate, self.qualifications, self.school, self.email) = user_data
                return True
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False


class EditProfileScreen(tk.Frame):
    def __init__(self, container, user_data):
        super().__init__(container, bg="white")
        self.container = container
        self.profile = Profile(user_data)
        self.undo_queue = deque(maxlen=10) 

        initial_state = (
            self.profile.name,
            self.profile.school,
            self.profile.qualifications,
            str(self.profile.hourly_rate),
            self.profile.subjects,
            self.profile.profile_picture
        )
        self.undo_queue.append(initial_state)

        self.font_title = tkfont.Font(family="Inter 18pt", size=20, weight="bold")
        self.font_subtitle = tkfont.Font(family="Inter 18pt", size=12)
        self.font_button = tkfont.Font(family="Inter 18pt", size=12, weight="bold")
        self.font_text = tkfont.Font(family="Inter 18pt", size=12)

        self.back_button = tk.Button(self, text="← Back to login", command=self.go_back, bg="white", fg="black", font=self.font_text, bd=0, cursor="hand2")
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.title_label = tk.Label(self, text="Edit Profile", font=self.font_title, bg="white", fg="white")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

        self.profile_pic_label = tk.Label(self, bg="white")
        self.profile_pic_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.load_profile_picture(self.profile.profile_picture)
        
        upload_img = Image.open("config/images/UploadProfile.png")
        upload_img = upload_img.resize((150, 35), Image.LANCZOS)
        self.upload_icon = ImageTk.PhotoImage(upload_img)

        self.upload_button = tk.Button(
            self, image=self.upload_icon, command=self.upload_profile_picture, bg="white", bd=0, cursor="hand2"
        )
        self.upload_button.grid(row=2, column=0, padx=10, sticky="w", pady=(0, 5))

        self.entries = {}
        self.create_form_fields()

        self.save_button = tk.Button(self, text="Save profile", command=self.save_changes, bg="white", fg="#9344ec", font=self.font_button, bd=0, cursor="hand2")
        self.save_button.grid(row=10, column=0, padx=20, pady=10, sticky="w")

        self.undo_button = tk.Button(self, text="Undo changes", command=self.undo_changes, bg="white", fg="#9344ec", font=self.font_button, bd=0, cursor="hand2")
        self.undo_button.grid(row=10, column=2, padx=20, pady=10, sticky="e")

        self.pack(expand=True, fill="both")

    def create_form_fields(self):
        self.back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.title_label.grid(row=0, column=1, columnspan=2, pady=5, sticky="n")

        self.profile_pic_label.grid(row=1, column=0, rowspan=3, padx=10, pady=5, sticky="w")
        self.upload_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        fields = [
            ("Name", "name", self.profile.name),
            ("School / University", "school", self.profile.school),
            ("Hourly Rate", "hourly_rate", self.profile.hourly_rate),
        ]

        row_index = 1 
        for label_text, key, value in fields:
            tk.Label(self, text=label_text, font=self.font_subtitle, bg="white", fg="#5b6779").grid(
                row=row_index, column=1, columnspan=2, sticky="w", pady=(2, 0)
            )

            entry = tk.Entry(self, width=40, font=self.font_text, bd=1, relief="solid")
            entry.grid(row=row_index + 1, column=1, columnspan=2, pady=(0, 2), sticky="we")
            entry.insert(0, value if value is not None else "")
            self.entries[key] = entry

            row_index += 1

        row_index = 5 

        subjects_label = tk.Label(self, text="Subjects Teaching", font=self.font_subtitle, bg="white", fg="#5b6779")
        subjects_label.grid(row=row_index, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 0))

        options_frame = tk.Frame(self, bg="white", relief="solid", bd=2)
        options_frame.grid(row=row_index + 1, column=0, columnspan=3, padx=10, pady=(0, 0), sticky="we")

        canvas = tk.Canvas(options_frame, bg="white", height=80, bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(options_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        checkbox_container = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=checkbox_container, anchor="nw")

        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        checkbox_container.bind("<Configure>", update_scroll_region)

        self.selected_subjects = self.profile.subjects.split(',') if self.profile.subjects else []

        subjects = ["Maths", "English", "Spanish", "Biology", "Chemistry", "Physics", "Computer Science"]
        self.subject_vars = {}
        
        for subject in subjects:
            var = tk.BooleanVar(value=subject in self.selected_subjects)
            self.subject_vars[subject] = var
            chk = tk.Checkbutton(
                checkbox_container,
                text=subject,
                variable=var,
                bg="white",
                fg="#333",
                font=self.font_text,
                anchor="w",
                selectcolor="#c499f8",
                relief="flat",
                padx=5,
                pady=2
            )
            chk.pack(fill=tk.X, anchor="w", pady=2)

        canvas.configure(yscrollcommand=scrollbar.set)

        row_index += 2

        qualifications_label = tk.Label(self, text="Expertise & Qualifications", font=self.font_subtitle, bg="white", fg="#5b6779")
        qualifications_label.grid(row=row_index, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 0))

        self.qualifications_text = tk.Text(self, width=50, height=3, font=self.font_text, bd=1, relief="solid", wrap="word")
        self.qualifications_text.grid(row=row_index + 1, column=0, columnspan=3, padx=10, pady=(0, 0), sticky="we")
        self.qualifications_text.insert("1.0", self.profile.qualifications)

    def load_profile_picture(self, image_path):
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((150, 150), Image.LANCZOS)
                self.profile_pic = ImageTk.PhotoImage(img)
                self.profile_pic_label.config(image=self.profile_pic)
            except Exception:
                self.profile_pic_label.config(text="No Image")

    def upload_profile_picture(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.profile.profile_picture = file_path
            self.load_profile_picture(file_path)
            messagebox.showinfo("Success", "Profile picture updated successfully!")

    def save_changes(self):
        selected_subjects = [subject for subject, var in self.subject_vars.items() if var.get()]
        
        new_data = (
            self.entries["name"].get().strip(),
            self.entries["school"].get().strip(),
            self.qualifications_text.get("1.0", tk.END).strip(),
            self.entries["hourly_rate"].get().strip(),
            ','.join(selected_subjects),

            self.profile.profile_picture,
            self.profile.email,
            self.profile.user_id
        )
        if self.profile.update_profile(new_data):
            if self.profile.refresh_profile():
                self.load_profile_picture(self.profile.profile_picture)
                messagebox.showinfo("Success", "Profile updated successfully!")
            else:
                messagebox.showerror("Error", "Profile updated but failed to refresh data.")
        else:
            messagebox.showerror("Error", "Failed to update profile. Please try again.")


    def undo_changes(self):
        if self.undo_queue:
            last_state = self.undo_queue.pop()
            self.entries["name"].delete(0, tk.END)
            self.entries["name"].insert(0, last_state[0])
            
            self.entries["school"].delete(0, tk.END)
            self.entries["school"].insert(0, last_state[1])
            
            self.entries["hourly_rate"].delete(0, tk.END)
            self.entries["hourly_rate"].insert(0, last_state[3])
            
            self.selected_subjects = last_state[4].split(',') if last_state[4] else []
            for subject, var in self.subject_vars.items():
                var.set(subject in self.selected_subjects)

            
            self.qualifications_text.delete("1.0", tk.END)
            self.qualifications_text.insert("1.0", last_state[2])
            
            self.load_profile_picture(last_state[5])

    def go_back(self):
        self.pack_forget()
        from Login import LoginScreen
        LoginScreen(self.container).pack()