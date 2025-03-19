import webbrowser
import tkinter as tk
from voice import speak

MOCK_LOCATION = "Vijaywada"
MOCK_SHELTER = "VIT AP University"

def open_google_maps():
    url = f"https://www.google.com/maps/dir/?api=1&origin={MOCK_LOCATION}&destination={MOCK_SHELTER}&travelmode=driving"
    speak("Opening Google Maps for navigation.")
    webbrowser.open(url)

def trigger_emergency():
    speak("Emergency detected. Authorities have been notified.")
    tk.messagebox.showinfo("ALERT", "Emergency Code Triggered! Authorities have been notified.")
    speak(f"Your current location is {MOCK_LOCATION}. The nearest shelter is at {MOCK_SHELTER}.")
    open_google_maps()

def get_medical_response(issue):
    medical_advice = {
        "wood stuck": "Do not remove it. Cover with a clean cloth and seek medical help.",
        "glass shard": "Do not pull out deeply embedded glass. Wash with water and bandage it.",
        "fracture": "Immobilize the limb and seek medical help.",
        "cpr": "Place hands in the center of the chest, push hard and fast, 100-120 times per minute.",
        "burn": "Run cool water over the area for 10 minutes. Do not apply ice.",
        "bleeding": "Apply firm pressure with a clean cloth.",
        "choking": "Perform the Heimlich maneuver with upward thrusts above the navel."
    }
    return medical_advice.get(issue.lower(), "No advice available for this condition.")
