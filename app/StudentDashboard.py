import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  
import sqlite3
from TeacherDetails import TeacherDetailsScreen

class StudentDashboardScreen(tk.Frame):
    def __init__(self, container):
        super().__init__(container, bg="white")
        self.container = container

        self.apply_img = self.load_resized_image("config/images/ApplyFilters.png", 90, 28)
        self.reset_img = self.load_resized_image("config/images/ResetFilters.png", 50, 28)

        title_frame = tk.Frame(self, bg="white")
        title_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            title_frame, 
            text="Student Dashboard", 
            font=("Inter 18pt", 20, "bold"), 
            bg="white", 
            fg="#8A2BE2"
        ).pack(side="left", anchor="w")

        filter_frame = tk.Frame(self, bg="white")
        filter_frame.pack(pady=5, padx=10, anchor="w") 

        tk.Label(filter_frame, text="Filter by Subject", bg="white", font=("Inter 18pt", 11)).grid(row=0, column=0, sticky="w", padx=(0,5))
        self.subject_filter = ttk.Combobox(filter_frame, values=self.get_subject_list(), state="readonly", width=28)
        self.subject_filter.grid(row=1, column=0, padx=(0,5), pady=5, sticky="w")

        tk.Label(filter_frame, text="Max Hourly Rate ($)", bg="white", font=("Inter 18pt", 11)).grid(row=0, column=1, sticky="w", padx=(10,5))
        self.hourly_rate_filter = tk.Entry(filter_frame, width=20)
        self.hourly_rate_filter.grid(row=1, column=1, padx=(10,5), pady=5, sticky="w")

        apply_button = tk.Button(
            filter_frame, image=self.apply_img, command=self.apply_filters, 
            bg="white", relief="flat", borderwidth=0
        )
        apply_button.grid(row=1, column=2, padx=5, sticky="w")

        reset_button = tk.Button(
            filter_frame, image=self.reset_img, command=self.load_data, 
            bg="white", relief="flat", borderwidth=0
        )
        reset_button.grid(row=1, column=3, padx=5, sticky="w")

        columns = ("Name", "Subjects", "Hourly Rate", "Education ")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(expand=True, fill="both", padx=10, pady=8)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.view_teacher_details)

        self.load_data()

        back_img = self.load_resized_image("config/images/BackButton2.png", 315, 40)
        back_button = tk.Button(self, image=back_img, command=self.go_back, bg="white", relief="flat", borderwidth=0)
        back_button.image = back_img
        back_button.pack(pady=5)

        self.pack(expand=True, fill="both")

    def load_resized_image(self, path, width, height):
        img = Image.open(path)
        img = img.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def get_subject_list(self):
        conn = sqlite3.connect("teacher_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT subjects FROM user_profiles")
        subjects = cursor.fetchall()
        conn.close()

        subject_set = set()
        for subject_row in subjects:
            if subject_row[0]:
                subject_list = subject_row[0].split(",")
                subject_set.update(subject_list)

        return sorted(subject_set)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())

        conn = sqlite3.connect("teacher_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, subjects, hourly_rate, school FROM user_profiles")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def apply_filters(self):
        subject = self.subject_filter.get()
        max_hourly_rate = self.hourly_rate_filter.get()

        query = "SELECT name, subjects, hourly_rate, school FROM user_profiles WHERE 1=1"
        params = []

        if subject:
            query += " AND subjects LIKE ?"
            params.append(f"%{subject}%")

        if max_hourly_rate:
            try:
                max_rate = float(max_hourly_rate)
                query += " AND hourly_rate <= ?"
                params.append(max_rate)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid hourly rate")
                return

        self.tree.delete(*self.tree.get_children())

        conn = sqlite3.connect("teacher_data.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def view_teacher_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a teacher")
            return

        teacher_data = self.tree.item(selected_item, "values")
        teacher_name = teacher_data[0]

        conn = sqlite3.connect("teacher_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE name=?", (teacher_name,))
        teacher_details = cursor.fetchone()
        conn.close()

        if teacher_details:
            self.pack_forget()
            self.container.teacher_details_screen = TeacherDetailsScreen(self.container, teacher_details)
            self.container.teacher_details_screen.pack(fill="both", expand=True)

    def go_back(self):
        self.pack_forget()
        self.container.winfo_toplevel().app.back_to_welcome()
