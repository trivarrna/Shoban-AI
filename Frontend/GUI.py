# import sys
# import time
# import random
# import datetime
# import pyttsx3
# import speech_recognition as sr
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QTextEdit, QLineEdit, QPushButton
# )
# from PyQt5.QtGui import QMovie, QFont
#
# # Initialize TTS engine
# engine = pyttsx3.init()
#
# def generate_response(user_input):
#     user_input = user_input.lower()
#     if "hello" in user_input:
#         return "Hello! I am Jarvis. How can I help you today?"
#     elif "time" in user_input:
#         now = datetime.datetime.now()
#         return f"The current time is {now.strftime('%I:%M %p')}."
#     elif "date" in user_input:
#         return f"Today's date is {datetime.date.today()}."
#     elif "your name" in user_input:
#         return "I am Jarvis, your AI assistant."
#     elif "bye" in user_input or "exit" in user_input:
#         return "Goodbye! Have a great day!"
#     else:
#         return random.choice([
#             "I'm not sure how to respond to that.",
#             "Can you please rephrase?",
#             "That's interesting!",
#             "Let me look into that for you."
#         ])
#
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()
#
# class JarvisWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Shoban - AI Advancebot")
#         self.setGeometry(100, 100, 1000, 600)
#
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#
#         # Main layout
#         self.main_layout = QVBoxLayout(self.central_widget)
#
#         # Full-screen GIF background
#         self.bg_label = QLabel(self)
#         self.bg_movie = QMovie("gif.gif")
#         self.bg_label.setMovie(self.bg_movie)
#         self.bg_movie.start()
#         self.bg_label.setScaledContents(True)
#         self.bg_label.setGeometry(0, 0, self.width(), self.height())
#         self.bg_label.lower()
#
#         # Resize event override to adjust background dynamically
#         self.installEventFilter(self)
#
#         # Overlay layout (holds all UI elements)
#         self.overlay_layout = QHBoxLayout()
#         self.main_layout.addLayout(self.overlay_layout)
#
#         # Left column for chat + input
#         self.left_column = QVBoxLayout()
#         self.overlay_layout.addLayout(self.left_column)
#         self.overlay_layout.addStretch()
#
#         # Header
#         self.header = QLabel("Shoban AI Assistant")
#         self.header.setStyleSheet("color: #00ffcc; background: transparent;")
#         self.header.setFont(QFont("Helvetica", 14, QFont.Bold))
#         self.header.setAlignment(Qt.AlignCenter)
#         self.left_column.addWidget(self.header)
#
#         # Chat display
#         self.chat_area = QTextEdit()
#         self.chat_area.setFixedSize(400, 150)
#         self.chat_area.setReadOnly(True)
#         self.chat_area.setStyleSheet(
#             "background : transparent; color: white; border: 1px #00c3ff;"
#         )
#         self.left_column.addWidget(self.chat_area)
#
#         # Input field
#         self.entry = QLineEdit()
#         self.entry.setFixedWidth(400)
#         self.entry.setStyleSheet(
#             "background-color: #1a1a1a; color: white; border: 2px solid #00c3ff;"
#         )
#         self.entry.returnPressed.connect(self.send_text_response)
#         self.left_column.addWidget(self.entry)
#
#         # Buttons stacked vertically
#         self.button_column = QVBoxLayout()
#         self.left_column.addLayout(self.button_column)
#
#         self.send_button = QPushButton("Send")
#         self.send_button.setStyleSheet("background-color: #00ffcc; color: black; font-weight: bold;")
#         self.send_button.clicked.connect(self.send_text_response)
#         self.button_column.addWidget(self.send_button)
#
#         self.voice_button = QPushButton("Chat")
#         self.voice_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
#         self.voice_button.clicked.connect(self.toggle_chat_mode)
#         self.button_column.addWidget(self.voice_button)
#
#         self.clear_button = QPushButton("Clear")
#         self.clear_button.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold;")
#         self.clear_button.clicked.connect(self.clear_chat)
#         self.button_column.addWidget(self.clear_button)
#
#         self.speak_mode = False
#
#     def eventFilter(self, source, event):
#         # Resize background to match window
#         if event.type() == event.Resize:
#             self.bg_label.setGeometry(0, 0, self.width(), self.height())
#         return super().eventFilter(source, event)
#
#     def toggle_chat_mode(self):
#         if self.voice_button.text() == "Chat":
#             self.voice_button.setText("Audio")
#             self.speak_mode = False
#         else:
#             self.voice_button.setText("Chat")
#             self.speak_mode = True
#         self.send_text_response()
#
#     def send_text_response(self):
#         user_input = self.entry.text().strip()
#         if not user_input:
#             return
#         self.chat_area.append(f"You: {user_input}")
#         self.entry.clear()
#         response = generate_response(user_input)
#         self.chat_area.append(f"Jarvis: {response}\n")
#         if self.speak_mode:
#             speak(response)
#
#     def clear_chat(self):
#         self.chat_area.clear()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = JarvisWindow()
#     window.show()
#     sys.exit(app.exec_())

import sys
import random
import datetime
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton
)
from PyQt5.QtGui import QMovie, QFont, QIcon

# Initialize TTS engine
engine = pyttsx3.init()

# Response generator
def generate_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hello! I am Jarvis. How can I help you today?"
    elif "time" in user_input:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."
    elif "date" in user_input:
        return f"Today's date is {datetime.date.today()}."
    elif "your name" in user_input:
        return "I am Jarvis, your AI assistant."
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return random.choice([
            "I'm not sure how to respond to that.",
            "Can you please rephrase?",
            "That's interesting!",
            "Let me look into that for you."
        ])

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main GUI class
class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shoban - AI Advancebot")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Background GIF
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie("gif.gif")
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.setScaledContents(True)
        self.bg_movie.start()
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()
        self.installEventFilter(self)

        # Overlay Layout
        self.overlay_layout = QHBoxLayout()
        self.main_layout.addLayout(self.overlay_layout)

        # Left-side UI Column
        self.left_column = QVBoxLayout()
        self.overlay_layout.addLayout(self.left_column)
        self.overlay_layout.addStretch()

        # Header
        self.header = QLabel("Shoban AI Assistant")
        self.header.setStyleSheet("color: #00ffcc; background: transparent;")
        self.header.setFont(QFont("Helvetica", 16, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.left_column.addWidget(self.header)

        # Chat Area
        self.chat_area = QTextEdit()
        self.chat_area.setFixedSize(400, 250)
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background-color: #1a1a1a; color: white; border: 2px solid #00c3ff;")
        self.left_column.addWidget(self.chat_area)

        # Input Field
        self.entry = QLineEdit()
        self.entry.setFixedWidth(400)
        self.entry.setStyleSheet("background-color: #1a1a1a; color: white; border: 2px solid #00c3ff;")
        self.entry.returnPressed.connect(self.send_text_response)
        self.left_column.addWidget(self.entry)

        # Buttons Column
        self.button_column = QVBoxLayout()
        self.left_column.addLayout(self.button_column)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: #00ffcc; color: black; font-weight: bold;")
        self.send_button.clicked.connect(self.send_text_response)
        self.button_column.addWidget(self.send_button)

        # Mic Button with Icon
        self.mic_button = QPushButton("Speak")
        self.mic_button.setIcon(QIcon.fromTheme("microphone"))
        self.mic_button.setIconSize(self.send_button.sizeHint())
        self.mic_button.setStyleSheet("background-color: blue; color: white; font-weight: bold;")
        self.mic_button.clicked.connect(self.listen_and_respond)
        self.button_column.addWidget(self.mic_button)

        # Clear Button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet("background-color: #ff4d4d; color: white; font-weight: bold;")
        self.clear_button.clicked.connect(self.clear_chat)
        self.button_column.addWidget(self.clear_button)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        return super().eventFilter(source, event)

    def send_text_response(self):
        user_input = self.entry.text().strip()
        if not user_input:
            return
        self.chat_area.append(f"You: {user_input}")
        self.entry.clear()
        self.respond_to_input(user_input)

    def listen_and_respond(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.chat_area.append("🎙️ Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                self.chat_area.append(f"You (via mic): {user_input}")
                self.respond_to_input(user_input)
            except sr.WaitTimeoutError:
                self.chat_area.append("⏳ Listening timed out. Please try again.")
            except sr.UnknownValueError:
                self.chat_area.append("⚠️ Sorry, I couldn't understand that.")
            except sr.RequestError:
                self.chat_area.append("❌ Speech service is unavailable.")

    def respond_to_input(self, user_input):
        response = generate_response(user_input)
        self.chat_area.append(f"Jarvis: {response}\n")
        speak(response)

    def clear_chat(self):
        self.chat_area.clear()

# Run App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisWindow()
    window.show()
    sys.exit(app.exec_())
