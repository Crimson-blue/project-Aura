# AuraAssistant 🎙️🤖

Aura is a **voice-activated personal AI assistant** powered by **Whisper (speech-to-text)**, **Mistral via OpenRouter (chat model)**, and **pyttsx3 (text-to-speech)**.  
It can tell you the time, date, open websites, and answer general queries using an LLM.  

---

## ✨ Features
- 🎤 **Speech-to-Text**: Uses Whisper for transcribing voice input.  
- 🧠 **AI Assistant**: Connects to Mistral-7B via OpenRouter.  
- 🔊 **Text-to-Speech**: Responds with natural voice using `pyttsx3`.  
- ⏰ **Time & Date** queries.  
- 🌐 **Web Commands**: Opens YouTube or other sites.  
- 📴 **Graceful Shutdown** with "stop" or "bye".  

---

## 🛠️ Requirements

Make sure you have **Python 3.9+** installed.  

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg  
Whisper needs **FFmpeg** for audio processing.  

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) (or [gyan.dev builds](https://www.gyan.dev/ffmpeg/builds/)).  
2. Extract the zip → you’ll get a folder like `ffmpeg-2024-win64-static`.  
3. Inside, go to the `bin` folder (contains `ffmpeg.exe`).  
4. Copy the folder path (e.g., `C:\ffmpeg\bin`).  
5. Add it to **Environment Variables**:  
   - Press `Win + R`, type `sysdm.cpl`, press Enter.  
   - Go to **Advanced → Environment Variables**.  
   - Under **System Variables**, select `Path` → Edit → New → paste the path (`C:\ffmpeg\bin`).  
   - Click OK and restart your terminal.  
6. Verify installation:  
   ```bash
   ffmpeg -version
   ```

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Debian/Ubuntu)
```bash
sudo apt update && sudo apt install ffmpeg -y
```

---

## ⚙️ Setup

1. Clone or download this project.  
   ```bash
   git clone https://github.com/yourusername/aura-assistant.git
   cd aura-assistant
   ```

2. Set your **OpenRouter API key**:  
   - Get a free key from [OpenRouter](https://openrouter.ai/keys).  
   - Open the script and replace this line:  

     ```python
     OPENROUTER_API_KEY = "sk-xxxxx"
     ```

   - Or set it as an environment variable:  
     ```bash
     export OPENROUTER_API_KEY="sk-xxxxx"   # macOS/Linux
     setx OPENROUTER_API_KEY "sk-xxxxx"     # Windows
     ```

---

## 🚀 Usage

Run the assistant:

```bash
python aura.py
```

1. Aura greets you with a startup message.  
2. Say **"Hi"**, **"Hey"**, or **"Hello"** to activate.  
3. Ask questions or give commands like:  
   - "What’s the time?"  
   - "What’s today’s date?"  
   - "Open YouTube"  
   - "Tell me about space exploration."  

4. Say **"Stop"** or **"Bye"** to exit.  

---

## 🧩 Project Structure

```
aura-assistant/
│
├── aura.py            # Main assistant script
├── README.md          # Documentation
└── requirements.txt   # Dependencies
```

---

## 🔮 Future Improvements
- Add more web integrations (Google, Spotify, Wikipedia).  
- Add task management and reminders.  
- Improve wake-word detection (using VAD).  

---

## 📜 License
MIT License. Free to use and modify.  
