import speech_recognition as sr
import pyttsx3
import threading
import time
from database import get_emergency_codes
from utils import trigger_emergency, open_google_maps, get_medical_response
from gui import HelpMenu, MedicalEmergencyMenu

engine = pyttsx3.init()
engine.setProperty('rate', 180)  
engine_lock = threading.Lock()

def speak(text):
    """Speak function with threading to prevent lag."""
    def run():
        with engine_lock:
            engine.say(text)
            engine.runAndWait()
    
    threading.Thread(target=run, daemon=True).start()

def listen_for_commands():
    """Continuously listens for voice commands and responds immediately."""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False  
    recognizer.energy_threshold = 300  

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("Voice assistant is active and always listening.")

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)  # Low-latency listening
                spoken_command = recognizer.recognize_google(audio).strip().lower()
                print(f"You said: {spoken_command}")

                emergency_codes = get_emergency_codes()

                # **Immediate Response Handling**
                if spoken_command in emergency_codes:
                    trigger_emergency()
                elif "help" in spoken_command:
                    HelpMenu()
                elif "medical" in spoken_command:
                    MedicalEmergencyMenu()
                elif "navigate" in spoken_command or "shelter" in spoken_command:
                    open_google_maps()
                else:
                    advice = get_medical_response(spoken_command)
                    if advice:
                        speak(advice)

            except sr.UnknownValueError:
                continue 
            except sr.WaitTimeoutError:
                continue  
            except sr.RequestError:
                speak("Internet issue detected, check your connection.")
            except Exception as e:
                print(f"Error: {e}")

def start_listening_for_commands():
    """Starts the background voice listener thread."""
    listener_thread = threading.Thread(target=listen_for_commands, daemon=True)
    listener_thread.start()
