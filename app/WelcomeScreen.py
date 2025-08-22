import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk

from StudentDashboard import StudentDashboardScreen
from SignUpTeacher import SignUpTeacherScreen
from Login import LoginScreen 

class WelcomeScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TutorMatch")
        self.root.geometry("600x550")
        self.root.configure(bg="white")

        self.font_title = tkfont.Font(family="Inter 18pt", size=20, weight="bold")
        self.font_subtitle = tkfont.Font(family="Inter 18pt", size=14)
        self.font_button = tkfont.Font(family="Inter 18pt", size=17, weight="bold")

        self.container = tk.Frame(self.root, bg="white")
        self.container.pack(fill="both", expand=True)

        root.app = self
        self.create_widgets()

    def create_widgets(self):
        title1 = tk.Label(self.container, text="Welcome to TutorMatch!", font=self.font_title, bg="white", fg="black")
        title1.pack(pady=(35, 0))

        title2 = tk.Label(self.container, text="How would you like to join us?", font=self.font_title, bg="white", fg="black")
        title2.pack(pady=(0, 1))

        subtitle = tk.Label(self.container, text="Select an option from below", font=self.font_subtitle, bg="white", fg="#969696")
        subtitle.pack(pady=(14, 70))

        teacher_image = Image.open("C:/Users/bache/OneDrive/Escritorio/TutorMatch/config/images/AsATeacherButton.png")
        teacher_image = teacher_image.resize((300, 60))
        teacher_photo = ImageTk.PhotoImage(teacher_image)

        teacher_button = tk.Button(self.container, image=teacher_photo, command=self.join_as_teacher, borderwidth=0, relief="flat")
        teacher_button.image = teacher_photo
        teacher_button.pack(pady=8)

        student_image = Image.open("C:/Users/bache/OneDrive/Escritorio/TutorMatch/config/images/AsAStudentButton.png")
        student_image = student_image.resize((300, 60))
        student_photo = ImageTk.PhotoImage(student_image)

        student_button = tk.Button(self.container, image=student_photo, command=self.join_as_student, borderwidth=0, relief="flat")
        student_button.image = student_photo
        student_button.pack(pady=(8, 15))

        login_frame = tk.Frame(self.container, bg="white")
        login_frame.pack(pady=(65, 0))

        login_label = tk.Label(login_frame, text="Already have an account?", font=self.font_subtitle, bg="white", fg="#606060")
        login_label.pack(side=tk.LEFT, padx=(0, 0))

        login_button = tk.Button(login_frame, text="Login", font=self.font_subtitle, bg="white", fg="#9344ec", activebackground="white", activeforeground="#9344ec", bd=0, cursor="hand2", command=self.login)
        login_button.pack(side=tk.LEFT, padx=(0, 0))

    def clear_widgets(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def join_as_teacher(self):
        self.clear_widgets()
        self.teacher_sign_up_screen()

    def join_as_student(self):
        self.clear_widgets()
        app = StudentDashboardScreen(self.container)
        app.pack(fill="both", expand=True)

    def login(self):
        self.clear_widgets()
        self.login_screen()

    def teacher_sign_up_screen(self):
        app = SignUpTeacherScreen(self.container)
        app.pack(fill="both", expand=True)

    def student_sign_up_screen(self):
        app = StudentDashboardScreen(self.container)
        app.pack(fill="both", expand=True)

    def login_screen(self):
        app = LoginScreen(self.container)
        app.pack(fill="both", expand=True)

    def back_to_welcome(self):
        self.clear_widgets()
        self.create_widgets()

if __name__ == "__main__":
    root = tk.Tk()
    root.app = WelcomeScreenApp(root)
    root.mainloop()
