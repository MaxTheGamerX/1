import tkinter as tk
from voice import speak, start_listening_for_commands
from database import save_emergency_code
from gui import HelpMenu, MedicalEmergencyMenu
from utils import trigger_emergency, open_google_maps

class DisasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disaster Management System")
        self.root.geometry("400x400")

        tk.Label(root, text="Enter User Name:", font=("Arial", 12)).pack(pady=5)
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()

        tk.Label(root, text="Set Emergency Code:", font=("Arial", 12)).pack(pady=5)
        self.code_entry = tk.Entry(root, show="*")
        self.code_entry.pack()

        tk.Button(root, text="Save Code", command=self.save_code, bg="green", fg="white").pack(pady=5)
        tk.Button(root, text="Help Menu", command=self.open_help_menu, bg="blue", fg="white").pack(pady=5)
        tk.Button(root, text="Trigger Emergency", command=trigger_emergency, bg="red", fg="white").pack(pady=5)

        speak("System initialized. Voice commands are active.")
        start_listening_for_commands()

    def save_code(self):
        user = self.user_entry.get()
        code = self.code_entry.get()
        if user and code:
            save_emergency_code(user, code)
        else:
            speak("Please enter a valid user name and emergency code.")
            tk.messagebox.showerror("Error", "Please enter a valid user name and emergency code.")

    def open_help_menu(self):
        HelpMenu()

if __name__ == "__main__":
    root = tk.Tk()
    app = DisasterApp(root)
    root.mainloop()
