import os
import json
import queue
import pyttsx3
import pyaudio
import numpy as np
import threading as th
import webbrowser
import subprocess
from datetime import datetime
import winreg as regedit
import sys
import time
import speech_recognition as sr

def add_to_startup():
    try:
        script_path = os.path.abspath(__file__)
        python_exe = sys.executable
        key = regedit.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = regedit.OpenKey(key, key_path, 0, regedit.KEY_WRITE)
        command = f'"{python_exe}" "{script_path}"'
        regedit.SetValueEx(reg_key, "Aura", 0, regedit.REG_SZ, command)
        regedit.CloseKey(reg_key)
        print("Successfully added to startup")
    except Exception as e:
        print(f"Startup error: {str(e)}")

class AuraAssistant:
    def __init__(me):
        me.wake_word = "hello aura"
        me.is_listening = False
        me.audio_queue = queue.Queue()
        me.engine = pyttsx3.init()
        me.engine.setProperty('rate', 150)
        me.engine.setProperty('volume', 0.7)
        me.startup_hello()
        
    def startup_hello(me):
        current_hour = datetime.now().hour
        if current_hour < 12:
            hello = "Good morning I'm Aura 4.0"
        elif current_hour < 17:
            hello = "Good afternoon I'm Aura 4.0"
        else:
            hello = "Good evening I'm Aura 4.0"
        time.sleep(3)
        me.speak(hello)
        
    def speak(me, text):
        print(f"Aura: {text}")
        me.engine.say(text)
        me.engine.runAndWait()
    
    def open_application(me, app_name, possible_paths, web_fallback=None):
        opened = False
        
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    os.startfile(path)
                    me.speak(f"Opening {app_name}")
                    opened = True
                    break
            except Exception as e:
                print(f"Failed to open {path}: {e}")
                continue
        
        if not opened and web_fallback:
            me.speak(f"Opening {app_name} in browser")
            webbrowser.open(web_fallback)
            opened = True
        
        if not opened:
            me.speak(f"Sorry, I couldn't find {app_name} on your system")
    
    def execute_command(me, command):
        command = command.lower().strip()
        print(f"Executing command: {command}")
        
        if "open youtube" in command or "youtube" in command:
            me.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            
        elif "time" in command or "what time is it" in command:
            current_time = datetime.now().strftime("%I:%M %p").lstrip("0")
            time_period = "in the morning" if "AM" in current_time else "in the evening"
            me.speak(f"It's {current_time.replace('AM','').replace('PM','')} {time_period}")
            
        elif "weather" in command:
            me.speak("Checking the weather for you")
            webbrowser.open("https://weather.com")
            
        elif "open google" in command or "google" in command:
            me.speak("Opening Google")
            webbrowser.open("https://google.com")
            
        elif "music" in command or "spotify" in command or "open spotify" in command:
            spotify_paths = [
                os.path.expanduser(r"~\AppData\Roaming\Spotify\Spotify.exe"),
                os.path.expanduser(r"~\AppData\Local\Microsoft\WindowsApps\Spotify.exe"),
                r"C:\Program Files\Spotify\Spotify.exe",
                r"C:\Program Files (x86)\Spotify\Spotify.exe"
            ]
            me.open_application("Spotify", spotify_paths, "https://open.spotify.com")
            
        elif "open steam" in command or "steam" in command:
            steam_paths = [
                r"C:\Program Files (x86)\Steam\steam.exe",
                r"C:\Program Files\Steam\steam.exe",
                os.path.expanduser(r"~\Steam\steam.exe")
            ]
            me.open_application("Steam", steam_paths)
            
        elif "open discord" in command or "discord" in command:
            discord_paths = [
                os.path.expanduser(r"~\AppData\Local\Discord\Update.exe --processStart Discord.exe"),
                os.path.expanduser(r"~\AppData\Roaming\Discord\Discord.exe")
            ]
            me.open_application("Discord", discord_paths, "https://discord.com/app")
            
        elif "stop listening" in command or "goodbye" in command or "bye" in command:
            me.speak("Goodbye! Have a great day!")
            me.is_listening = False
            
        else:
            me.speak("Sorry, I didn't understand that command. Try saying 'open youtube', 'what time is it', or 'open spotify'")
    
    def process_audio(me):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 4000 
        recognizer.dynamic_energy_threshold = True
        
        with sr.Microphone() as source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                print("Processing speech...")
                
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"Recognized: '{text}'")
                    
                    if me.wake_word.lower() in text.lower():
                        command = text.lower().replace(me.wake_word.lower(), "").strip()
                        if command:
                            print(f"Command extracted: '{command}'")
                            me.execute_command(command)
                        else:
                            me.speak("Yes, how can I help you?")
                    else:
                        print(f"No wake word detected in: '{text}'")
                        
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition; {e}")
                    me.speak("Sorry, I'm having trouble with speech recognition")
                    
            except sr.WaitTimeoutError:
                print("Listening timeout - no speech detected")
            except Exception as e:
                print(f"Audio processing error: {e}")

    def listen(me):
        me.is_listening = True
        print("Aura is ready! Say 'Hello Aura' followed by your command...")
        print("Example commands:")
        print("- 'Hello Aura open youtube'")
        print("- 'Hello Aura what time is it'")
        print("- 'Hello Aura open spotify'")
        print("- 'Hello Aura stop listening'")
        
        try:
            while me.is_listening:
                me.process_audio()
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            me.speak("Shutting down")
        except Exception as e:
            print(f"Error in listen(): {str(e)}")
            me.speak("I encountered an error and need to restart")
        finally:
            me.is_listening = False

def main():
    try:
        assistant = AuraAssistant()
        assistant.listen()
    except Exception as e:
        print(f"Main error: {str(e)}")
        if 'assistant' in locals():
            assistant.speak("Sorry, I encountered a critical error and need to stop.")

if __name__ == "__main__":
    main()