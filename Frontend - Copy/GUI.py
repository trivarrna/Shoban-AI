import sys
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QTextEdit, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtCore import Qt
# import os

class ShobanAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S H O B A N A I ")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("background-color: red;")
        self.initUI()

    def initUI(self):
        # Background HUD animation
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, 900, 650)
        self.movie = QMovie("jarvis_hud_gif.gif")  
        # print(os.path.abspath("jarvis_hud.gif"))
        # Make sure this file exists

        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Title
        self.title_label = QLabel("♦ S H O B A N A I   ♦", self)
        self.title_label.setGeometry(0, 10, 900, 40)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: cyan; font-size: 26px; font-weight: bold;")

        # Chatbox (conversation display)
        self.chatbox = QTextEdit(self)
        self.chatbox.setGeometry(50, 60, 800, 400)
        self.chatbox.setReadOnly(True)
        self.chatbox.setStyleSheet("""
            QTextEdit {
                color: #00ffff;
                background-color: rgba(0,0,0,0.6);
                font-size: 16px;
                border: 2px solid cyan;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Mic button
        self.mic_button = QPushButton("🎤", self)
        self.mic_button.setGeometry(400, 470, 100, 50)
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: cyan;
                color: black;
                font-size: 22px;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #00cccc;
            }
        """)
        self.mic_button.clicked.connect(self.listen_to_user)

        # Command Buttons
        self.browser_btn = QPushButton("🌐 Open Browser", self)
        self.browser_btn.setGeometry(100, 540, 180, 40)
        self.browser_btn.setStyleSheet(self.button_style())
        self.browser_btn.clicked.connect(lambda: self.run_command("open browser"))

        self.weather_btn = QPushButton("☀️ Weather Info", self)
        self.weather_btn.setGeometry(360, 540, 180, 40)
        self.weather_btn.setStyleSheet(self.button_style())
        self.weather_btn.clicked.connect(lambda: self.run_command("weather"))

        self.clear_btn = QPushButton("🧹 Clear Chat", self)
        self.clear_btn.setGeometry(620, 540, 180, 40)
        self.clear_btn.setStyleSheet(self.button_style())
        self.clear_btn.clicked.connect(lambda: self.chatbox.clear())

    def button_style(self):
        return """
            QPushButton {
                background-color: #00ffff;
                color: black;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00cccc;
            }
        """

    def speak(self, message):
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

    def listen_to_user(self):
        threading.Thread(target=self.capture_voice, daemon=True).start()

    def capture_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.append_chat("🔊 Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.append_chat(f"🗣️ You: {text}")
                self.respond(text)
            except sr.UnknownValueError:
                self.append_chat("❗ Sorry, I didn't catch that.")
                self.speak("Sorry, I didn't catch that.")
            except sr.RequestError:
                self.append_chat("❌ API unavailable.")
                self.speak("Speech service is unavailable.")
            except Exception as e:
                self.append_chat(f"⚠️ Error: {str(e)}")
                self.speak("An error occurred.")

    def append_chat(self, message):
        self.chatbox.append(message)

    def respond(self, command):
        command = command.lower()
        if "open browser" in command:
            self.run_command("open browser")
        elif "weather" in command:
            self.run_command("weather")
        else:
            response = "I'm not sure how to help with that yet."
            self.append_chat(f"🤖 Shoban AI: {response}")
            self.speak(response)

    def run_command(self, command):
        if command == "open browser":
            self.append_chat("🌐 Opening browser...")
            webbrowser.open("https://www.google.com")
            self.speak("Opening browser")
        elif command == "weather":
            self.append_chat("☀️ Weather info: 27°C, clear sky (demo)")
            self.speak("The weather is clear with 27 degrees Celsius.")
        else:
            self.append_chat("❓ Unknown command")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShobanAI()
    window.show()
    sys.exit(app.exec_())
