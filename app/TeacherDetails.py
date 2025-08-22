import tkinter as tk
from PIL import Image, ImageTk
import sqlite3  

class TeacherDetailsScreen(tk.Frame):
    def __init__(self, container, teacher_data):
        super().__init__(container, bg="white")
        self.container = container
        self.teacher_data = teacher_data

        self.teacher_details = [
            ["ID", teacher_data[0]],
            ["Name", teacher_data[1]],
            ["Profile Picture", teacher_data[2]],
            ["Subjects", teacher_data[3]],
            ["Hourly Rate", teacher_data[4]],
            ["Qualifications", teacher_data[5]],
            ["School", teacher_data[6]],
            ["Email", teacher_data[7]]
        ]

        (self.teacher_id, self.name, self.profile_picture, self.subjects, 
         self.hourly_rate, self.qualifications, self.school, self.email) = teacher_data

        self.create_widgets()
        self.pack(expand=True, fill="both", padx=20, pady=20)

    def create_widgets(self):
        back_button = tk.Button(self, text="← Back to dashboard", font=("Inter 18pt", 12), fg="black", bg="white", 
                                bd=0, highlightthickness=0, command=self.go_back)
        back_button.pack(anchor="w", pady=(0, 10))

        profile_frame = tk.Frame(self, bg="white")
        profile_frame.pack(fill="x", pady=10)

        self.display_profile_picture(profile_frame)

        text_frame = tk.Frame(profile_frame, bg="white")
        text_frame.pack(side="left", padx=(10, 0), anchor="w")

        name_label = tk.Label(text_frame, text=self.name, font=("Inter 18pt", 20, "bold"), bg="white")
        name_label.pack(anchor="w")  

        school_label = tk.Label(text_frame, text=self.school, font=("Inter 18pt", 16), fg="#7d7d7d", bg="white")
        school_label.pack(anchor="w") 

        rate_label = tk.Label(profile_frame, text=f"${self.hourly_rate}/hr", font=("Inter 18pt", 14), fg="#8854d0", bg="white")
        rate_label.pack(side="right")

        tk.Label(self, text="Expertise & Qualifications", font=("Inter 18pt", 15, "bold"), bg="white").pack(anchor="w", pady=(10, 0))

        tk.Label(
            self, 
            text=self.qualifications, 
            font=("Inter 18pt", 12), 
            bg="#ffffff", 
            wraplength=520, 
            anchor="w",
            justify="left" 
        ).pack(fill="x", anchor="w")

        tk.Label(self, text="Subjects teaching", font=("Inter 18pt", 15, "bold"), bg="white").pack(anchor="w", pady=(15, 0))
        tk.Label(self, text=self.subjects, font=("Inter 18pt", 12), fg="black", bg="white", wraplength=520).pack(anchor="w")

        tk.Label(self, text="Contact Details", font=("Inter 18pt", 15, "bold"), bg="white").pack(anchor="w", pady=(15, 0))
        tk.Label(self, text=self.email, font=("Inter 18pt", 12), fg="black", bg="#ffffff", anchor="w").pack(fill="x", padx=5, pady=5)

    def display_profile_picture(self, frame):
        if self.profile_picture:
            try:
                image = Image.open(self.profile_picture).resize((120, 135))
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(frame, image=photo, bg="white")
                label.image = photo
                label.pack(side="left")
            except Exception:
                tk.Label(frame, text="No Image", bg="white", fg="red").pack(side="left")

    def go_back(self):
        self.pack_forget()
        from StudentDashboard import StudentDashboardScreen
        StudentDashboardScreen(self.container).pack()
