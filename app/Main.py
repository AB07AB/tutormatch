import tkinter as tk
from WelcomeScreen import WelcomeScreen

def main():
    root = tk.Tk()
    root.title("TutorMatch")
    app = WelcomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()