import os
import time
import webbrowser
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import requests
import re
import json

OPENROUTER_API_KEY = "Your api key here" #inside quotes duh
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Whisper for speech-to-text
try:
    import whisper
    whisper_available = True
    whisper_model = whisper.load_model("tiny")   # "tiny" is fast, "small" more accurate
except Exception as e:
    print(f"[Aura Notice] Whisper not available: {e}")
    whisper_available = False


class AuraAssistant:
    def __init__(self):
        self.is_listening = False
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1.0)
        self.wake_words = ["hi", "hey", "hello"]
        self.model = "mistralai/mistral-7b-instruct:free"
        self.activated = False
        self.startup_hello()

    def speak(self, text: str):
        """Speak and print text using pyttsx3"""
        print(f"Aura: {text}")
        try:
            self.engine.stop()           # clear past buffer
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[TTS error] {e}")

    def startup_hello(self):
        hour = datetime.now().hour
        if hour < 12:
            msg = "Good morning. I am Aura, ready to assist you with Mistral."
        elif hour < 17:
            msg = "Good afternoon. Aura is online, powered by Mistral."
        else:
            msg = "Good evening. Aura is standing by with Mistral."
        self.speak(msg)

    def transcribe(self) -> str:
        if not whisper_available:
            self.speak("Whisper is not installed. I cannot process speech.")
            return ""
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            wav_file = "temp.wav"
            with open(wav_file, "wb") as f:
                f.write(audio.get_wav_data())
            result = whisper_model.transcribe(wav_file)
            return result.get("text", "")
        except Exception as e:
            print(f"[Whisper error] {e}")
            self.speak("There was an error processing the audio.")
            return ""

    def ask_openrouter(self, prompt: str) -> str:
        """Send query to Mistral via OpenRouter and return full reply"""
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are Aura, a helpful, friendly AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                self.speak(reply)
                return reply
            else:
                error_msg = f"OpenRouter API error: {response.text}"
                self.speak(error_msg)
                return error_msg
        except Exception as e:
            msg = f"Communication with OpenRouter failed: {str(e)}"
            self.speak(msg)
            return msg

    def clean_command(self, text: str):
        lowered = text.lower()
        for ww in self.wake_words:
            lowered = lowered.replace(ww, "")
        cleaned = re.sub(r"^[\s,\.]+", "", lowered)
        return cleaned.strip()

    def execute_command(self, command: str):
        command = command.lower().strip()
        print(f"Command received: {command}")

        if "time" in command:
            now = datetime.now().strftime("%I:%M %p").lstrip("0")
            self.speak(f"The current time is {now}.")
            return

        if "date" in command:
            today = datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {today}.")
            return

        if "open youtube" in command or "youtube" in command:
            self.speak("Opening YouTube in your browser.")
            webbrowser.open("https://youtube.com")
            return

        if "stop" in command or "bye" in command:
            self.speak("Goodbye. Aura is shutting down.")
            self.is_listening = False
            return

        self.ask_openrouter(command)

    def listen(self):
        self.is_listening = True
        self.speak("Say Hi, Hey, or Hello once to activate me.")
        try:
            while self.is_listening:
                text = self.transcribe()
                if not text:
                    continue
                print("Heard:", text)

                if not self.activated:
                    if any(w in text.lower() for w in self.wake_words):
                        self.activated = True
                        command = self.clean_command(text)
                        if command:
                            self.execute_command(command)
                        else:
                            self.speak("Yes. What would you like me to do?")
                else:
                    command = self.clean_command(text)
                    if command:
                        self.execute_command(command)
        except KeyboardInterrupt:
            self.speak("Manual shutdown requested. Goodbye.")
            self.is_listening = False
        except Exception as e:
            print("Error:", e)
            self.speak("Unexpected error, shutting down.")
            self.is_listening = False


def main():
    assistant = AuraAssistant()
    assistant.listen()


if __name__ == "__main__":
    main()
