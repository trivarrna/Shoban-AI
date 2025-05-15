from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QEvent, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat, QRadialGradient, QPen, QBrush
import speech_recognition as sr
import logging
import os
import sys
import time
import random
from math import sin, cos, radians

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('jarvis.log'), logging.StreamHandler(sys.stdout)]
)

# Directory setup
current_dir = os.getcwd()
TempDirPath = rf"{current_dir}\Temp"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"
os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(GraphicsDirPath, exist_ok=True)

# File I/O
def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

def GetMicrophoneStatus():
    try:
        with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        SetMicrophoneStatus("False")
        return "False"

def SetMicrophoneStatus(Status):
    with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
        file.write(Status)

# HolographicOrb
class HolographicOrb(QWidget):
    def __init__(self, parent=None):
        super(HolographicOrb, self).__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        self.setMinimumSize(300, 300)

    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center_x, center_y = self.width() // 2, self.height() // 2
        radius = min(self.width(), self.height()) // 3

        gradient = QRadialGradient(center_x, center_y, radius)
        gradient.setColorAt(0, QColor(0, 255, 255, 255))
        gradient.setColorAt(1, QColor(0, 128, 255, 50))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        for i in range(4):
            r = radius + (i * 20)
            pen = QPen(QColor(0, 255, 255, 150 - i * 30), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(center_x - r, center_y - r, r * 2, r * 2)

        for i in range(12):
            angle = radians(self.angle + i * 30)
            particle_radius = radius + 40
            x = center_x + particle_radius * cos(angle)
            y = center_y + particle_radius * sin(angle)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 255, 200))
            painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))

# Globe Placeholder
class GlobePlaceholder(QLabel):
    def __init__(self, parent=None):
        super(GlobePlaceholder, self).__init__(parent)
        self.setStyleSheet("background-color: blue; border-radius: 100px;")
        self.setMinimumSize(200, 200)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(50)

    def update_rotation(self):
        self.update()

# System Stats
class SystemStats(QWidget):
    def __init__(self):
        super(SystemStats, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: cyan; background-color: rgba(0, 0, 0, 0.8); border: 2px solid cyan; padding: 10px;")
        self.layout.addWidget(self.stats_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)
        self.update_stats()

    def update_stats(self):
        cpu = random.randint(20, 80)
        memory = random.randint(40, 90)
        network = round(random.uniform(0.5, 5.0), 1)
        self.stats_label.setText(f"SYSTEM STATS\nCPU: {cpu}%\nMemory: {memory}%\nNetwork: {network} MB/s")

# Clock
class ClockWidget(QWidget):
    def __init__(self):
        super(ClockWidget, self).__init__()
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: cyan; font-size: 16px; background-color: transparent;")
        layout = QHBoxLayout(self)
        layout.addWidget(self.time_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)

# Chat Section
class ChatSection(QWidget):
    message_sent = pyqtSignal(str)

    def __init__(self):
        super(ChatSection, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); color: cyan; border: 2px solid cyan; padding: 5px;")
        self.layout.addWidget(self.chat_text_edit)

        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); color: cyan; border: 2px solid cyan; padding: 5px;")
        self.input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: cyan; color: black; border: none; padding: 5px 15px; border-radius: 5px;")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        self.mic_button = QPushButton("Mic")
        self.mic_button.setStyleSheet("background-color: cyan; color: black; border: none; padding: 5px 15px; border-radius: 5px;")
        self.mic_button.clicked.connect(self.toggle_mic)
        self.input_layout.addWidget(self.mic_button)

        self.layout.addLayout(self.input_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chat)
        self.timer.start(500)

    def update_chat(self):
        try:
            with open(rf"{TempDirPath}\Responses.data", "r", encoding="utf-8") as file:
                self.chat_text_edit.setText(file.read())
        except FileNotFoundError:
            pass

    def add_message(self, message, sender="You"):
        self.chat_text_edit.append(f"{sender}: {message}")

    def toggle_mic(self):
        status = GetMicrophoneStatus()
        if status == "False":
            SetMicrophoneStatus("True")
            self.start_listening()
        else:
            SetMicrophoneStatus("False")
            self.stop_listening()

    def start_listening(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.add_message("Listening...", "JARVIS")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                self.add_message(command, "You")
                response = self.process_command(command)
                ShowTextToScreen(response)
                self.add_message(response, "Shoban")
            except:
                self.add_message("Could not process audio", "JARVIS")

    def stop_listening(self):
        self.add_message("Microphone off", "JARVIS")

    def send_message(self):
        message = self.input_field.text()
        if message:
            self.add_message(message, "You")
            response = self.process_command(message.lower())
            ShowTextToScreen(response)
            self.add_message(response, "Shoban")
            self.input_field.clear()

    def process_command(self, command):
        commands = {
            "hello": "Hello! How can I assist you today?",
            "time": f"The current time is {time.strftime('%H:%M:%S')}",
            "date": f"Today is {time.strftime('%Y-%m-%d')}",
            "status": "System is operational.",
            "help": "Commands: hello, time, date, status, shutdown, weather, news, joke",
            "shutdown": "Shutting down... (simulated)",
            "weather": "Weather data not available.",
            "news": "News not available.",
            "joke": "Why did the computer go to school? To become a bit smarter!"
        }
        return commands.get(command, "Unknown command. Try 'help'.")

# Main Interface
class JarvisInterface(QMainWindow):
    def __init__(self):
        super(JarvisInterface, self).__init__()
        self.setWindowTitle("JARVIS Interface")
        self.setStyleSheet("background-color: #1a1a1a;")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        self.holographic_orb = HolographicOrb()
        main_layout.addWidget(self.holographic_orb, 0, 1, 3, 3)

        self.globe_placeholder = GlobePlaceholder()
        main_layout.addWidget(self.globe_placeholder, 0, 4)

        self.chat_section = ChatSection()
        main_layout.addWidget(self.chat_section, 3, 0, 1, 2)

        self.system_stats = SystemStats()
        main_layout.addWidget(self.system_stats, 0, 0)

        self.clock_widget = ClockWidget()
        main_layout.addWidget(self.clock_widget, 3, 4)

        self.protocol_label = QLabel("VIOLENCE PROTOCOL")
        self.protocol_label.setStyleSheet("color: cyan; font-size: 20px; background-color: rgba(0, 0, 0, 0.8); border: 2px solid cyan; padding: 10px;")
        main_layout.addWidget(self.protocol_label, 1, 4)

        SetMicrophoneStatus("False")
        self.resize(1200, 800)

# Launch
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisInterface()
    window.show()
    sys.exit(app.exec_())
