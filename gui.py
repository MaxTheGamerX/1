import tkinter as tk
from voice import speak
from utils import get_medical_response, open_google_maps, trigger_emergency

class HelpMenu:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Help Menu")
        self.window.geometry("300x300")

        tk.Label(self.window, text="Select an Option:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.window, text="1. Medical Emergency", command=self.open_medical_menu, bg="lightblue").pack(pady=5)
        tk.Button(self.window, text="2. Navigate to Safe Location", command=open_google_maps, bg="lightgreen").pack(pady=5)
        tk.Button(self.window, text="3. Trigger Emergency", command=trigger_emergency, bg="red", fg="white").pack(pady=5)

        speak("Help menu opened. Speak a number or an option.")

    def open_medical_menu(self):
        MedicalEmergencyMenu()

class MedicalEmergencyMenu:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Medical Assistance")
        self.window.geometry("300x350")

        tk.Label(self.window, text="Select Your Medical Emergency:", font=("Arial", 12)).pack(pady=10)

        issues = ["Wood Stuck", "Glass Shard", "Fracture", "CPR", "Burn", "Bleeding", "Choking"]
        for index, issue in enumerate(issues, 1):
            tk.Button(self.window, text=f"{index}. {issue}", command=lambda i=issue: speak(get_medical_response(i)), bg="lightgray").pack(pady=3)

        speak("Medical menu opened. Speak a number or a condition.")
