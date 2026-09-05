import sys
import time
import speech_recognition as sr
import win32com.client


class VoiceAssistant:
    def __init__(self):
        print("[System] Initializing Windows SAPI Voice Engine...")
        try:
            # Native Windows SAPI Voice Engine (Bypasses pyttsx3 freezing issues)
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        except Exception as e:
            print(f"[Error] Failed to initialize Windows voice engine: {e}")
            sys.exit(1)

        print("[System] Initializing Speech Recognizer...")
        self.recognizer = sr.Recognizer()

        # Microphones can pick up background static; adjust threshold
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    def speak(self, text: str):
        """Speaks text out loud and prints it to the console."""
        print(f"\n🤖 Assistant: {text}")
        # 0 = Synchronous speech (waits until finished speaking before continuing)
        self.speaker.Speak(text, 0)

    def listen(self) -> str:
        """Captures audio from microphone and returns recognized text."""
        with sr.Microphone() as source:
            print("\n🎙️ Listening... (Speak into your microphone)")

            # Calibrate for room noise (short 0.5 sec calibration)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                # Listen with a 5-second timeout if no speech starts
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                print("[System] Processing speech recognition...")

                # Convert speech to text via Google Speech Recognition API
                query = self.recognizer.recognize_google(audio)
                print(f"👤 You said: '{query}'")
                return query.lower()

            except sr.WaitTimeoutError:
                print("[Warning] Listening timed out (No speech detected).")
                return ""
            except sr.UnknownValueError:
                print("[Warning] Could not understand the spoken audio.")
                return ""
            except sr.RequestError as e:
                print(f"[Error] Could not connect to Speech Recognition service: {e}")
                return ""

    def process_command(self, command: str) -> bool:
        """Processes the recognized command. Returns False to exit app."""
        if not command:
            return True

        # Custom Commands Logic
        if "hello" in command or "hi" in command:
            self.speak("Hello! How can I help you today?")

        elif "your name" in command:
            self.speak("I am your Python voice assistant.")

        elif "time" in command:
            current_time = time.strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}.")

        elif "date" in command:
            current_date = time.strftime("%A, %B %d, %Y")
            self.speak(f"Today is {current_date}.")

        elif "stop" in command or "exit" in command or "bye" in command:
            self.speak("Goodbye! Have a great day.")
            return False

        else:
            self.speak(f"I heard you say: {command}. I don't have a command set up for that yet.")

        return True

    def run(self):
        """Main Loop"""
        self.speak("System online. How can I help you?")
        running = True

        while running:
            command = self.listen()
            running = self.process_command(command)


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()