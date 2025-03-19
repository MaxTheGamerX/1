import tkinter as tk
from tkinter import messagebox
import sqlite3
import speech_recognition as sr
import pyttsx3
import threading
import webbrowser

engine = pyttsx3.init()
engine_lock = threading.Lock()

MOCK_LOCATION = "Vijaywada"
MOCK_SHELTER = "VIT AP University"

def speak(text):
    def run():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()
    
    threading.Thread(target=run, daemon=True).start()

def open_google_maps():
    url = f"https://www.google.com/maps/dir/?api=1&origin={MOCK_LOCATION}&destination={MOCK_SHELTER}&travelmode=driving"
    speak("Opening Google Maps for navigation.")
    webbrowser.open(url)

def setup_database():
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

setup_database()

def save_emergency_code(user, code):
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE name = ?", (user,))
    cursor.execute("INSERT INTO users (name, code) VALUES (?, ?)", (user, code))
    conn.commit()
    conn.close()
    speak("Emergency code saved successfully.")
    auto_close_message("Success", "Emergency code saved successfully!")

def get_emergency_codes():
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM users")
    result = cursor.fetchall()
    conn.close()
    return [r[0].lower() for r in result]

def auto_close_message(title, message, duration=3000):
    popup = tk.Toplevel()
    popup.title(title)
    tk.Label(popup, text=message, font=("Arial", 12)).pack(padx=20, pady=20)
    popup.after(duration, popup.destroy)

def request_rescue():
    speak("Rescue request submitted. Authorities have been notified.")
    speak(f"Your current location is {MOCK_LOCATION}. Food and ration will be transported to your location shortly.")
    ourl = f"https://sites.google.com/view/eqw1254625/home"
    webbrowser.open(ourl)

def trigger_emergency():
    speak("Emergency detected. Authorities have been notified.")
    auto_close_message("ALERT", "Emergency Code Triggered! Authorities have been notified.")
    speak(f"Your current location is {MOCK_LOCATION}. The nearest shelter is at {MOCK_SHELTER}.")
    open_google_maps()

def handle_medical_emergency():
    speak("Opening medical emergency menu.")
    MedicalEmergencyMenu()

def request_food():
    speak("The location was shared, the food and ration will be on their way shortly, please stay safe.")
    ourl = f"https://sites.google.com/view/f00d123/home"
    webbrowser.open(ourl)

def get_medical_response(issue):
    medical_advice = {
        "1": "Do not remove it. Cover with a clean cloth and seek medical help.",
        "wood stuck": "Do not remove it. Cover with a clean cloth and seek medical help.",
        "2": "Do not pull out deeply embedded glass. Wash with water and bandage it.",
        "glass shard": "Do not pull out deeply embedded glass. Wash with water and bandage it.",
        "3": "Immobilize the limb and seek medical help.",
        "fracture": "Immobilize the limb and seek medical help.",
        "4": "Place hands in the center of the chest, push hard and fast, 100-120 times per minute.",
        "cpr": "Place hands in the center of the chest, push hard and fast, 100-120 times per minute.",
        "5": "Run cool water over the area for 10 minutes. Do not apply ice.",
        "burn": "Run cool water over the area for 10 minutes. Do not apply ice.",
        "6": "Apply firm pressure with a clean cloth.",
        "bleeding": "Apply firm pressure with a clean cloth.",
        "7": "Perform the Heimlich maneuver with upward thrusts above the navel.",
        "choking": "Perform the Heimlich maneuver with upward thrusts above the navel."
    }
    return medical_advice.get(issue, None)

def listen_for_commands():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                spoken_command = recognizer.recognize_google(audio).strip().lower()
                print("You said:", spoken_command)

                emergency_codes = get_emergency_codes()

                if spoken_command in emergency_codes:
                    trigger_emergency()
                elif spoken_command == "help":
                    HelpMenu()
                elif spoken_command == "medical":
                    handle_medical_emergency()
                elif spoken_command in ["navigate", "shelter"]:
                    open_google_maps()
                else:
                    advice = get_medical_response(spoken_command)
                    if advice:
                        auto_close_message("Medical Advice", advice)
                        speak(advice)
            except sr.UnknownValueError:
                pass
            except sr.WaitTimeoutError:
                pass
            except sr.RequestError:
                pass

def start_listening_for_commands():
    listener_thread = threading.Thread(target=listen_for_commands, daemon=True)
    listener_thread.start()

class DisasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disaster Management System")
        self.root.geometry("420x500")
        self.root.configure(bg="#1E1E1E")
        
        frame = tk.Frame(root, bg="#1E1E1E")
        frame.pack(pady=20)

        tk.Label(frame, text="Enter User Name:", font=("Arial", 12),fg="white", bg="#1E1E1E").pack(pady=5)
        self.user_entry = tk.Entry(frame)
        self.user_entry.pack(pady=5)

        tk.Label(frame, text="Set Emergency Code:", font=("Arial", 12),fg="white", bg="#1E1E1E").pack(pady=5)
        self.code_entry = tk.Entry(frame, show="*")
        self.code_entry.pack(pady=5)

        tk.Button(frame, text="Save Code", command=self.save_code, bg="green", fg="white").pack(pady=5)
        tk.Button(frame, text="Help Menu", command=HelpMenu, bg="blue", fg="white").pack(pady=5)
        tk.Button(frame, text="Trigger Emergency", command=trigger_emergency, bg="red", fg="white").pack(pady=5)
        tk.Button(frame, text="Rescue Request", command=request_rescue, bg="red", fg="white").pack(pady=5)
        tk.Button(frame, text="Food Request", command=request_food, bg="red", fg="white").pack(pady=5)

        speak("System initialized. Voice commands are active.")
        start_listening_for_commands()

    def save_code(self):
        user = self.user_entry.get()
        code = self.code_entry.get()
        if user and code:
            save_emergency_code(user, code)
        else:
            speak("Please enter a valid user name and emergency code.")
            auto_close_message("Error", "Please enter a valid user name and emergency code.")

class HelpMenu:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Help Menu")
        self.window.geometry("300x300")
        self.window.configure(bg="#1E1E1E")

        tk.Label(self.window, text="Select an Option:", font=("Arial", 14), bg="#1E1E1E").pack(pady=10)

        tk.Button(self.window, text="1. Medical Emergency", command=handle_medical_emergency, bg="lightblue").pack(pady=5)
        tk.Button(self.window, text="2. Navigate to Safe Location", command=open_google_maps, bg="lightgreen").pack(pady=5)
        tk.Button(self.window, text="3. Trigger Emergency", command=trigger_emergency, bg="red", fg="white").pack(pady=5)

        speak("Help menu opened. Speak a number or an option.")

class MedicalEmergencyMenu:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Medical Assistance")
        self.window.geometry("300x350")
        self.window.configure(bg="#1E1E1E")

        tk.Label(self.window, text="Select Your Medical Emergency:", font=("Arial", 12), bg="#1E1E1E").pack(pady=10)

        issues = ["Wood Stuck", "Glass Shard", "Fracture", "CPR", "Burn", "Bleeding", "Choking"]
        for index, issue in enumerate(issues, 1):
            tk.Button(self.window, text=f"{index}. {issue}", command=lambda i=index: self.provide_advice(i), bg="lightgray").pack(pady=3)

        speak("Medical menu opened. Speak a number or a condition.")

    def provide_advice(self, index):
        advice = get_medical_response(str(index))
        if advice:
            auto_close_message("Medical Advice", advice)
            speak(advice)

root = tk.Tk()
app = DisasterApp(root)
root.mainloop()