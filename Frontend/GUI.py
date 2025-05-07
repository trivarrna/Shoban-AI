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

# Configure logging with both file and console output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler(sys.stdout)  # Output to console for debugging
    ]
)

# Directory setup
current_dir = os.getcwd()
TempDirPath = rf"{current_dir}\Temp"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

try:
    os.makedirs(TempDirPath, exist_ok=True)
    os.makedirs(GraphicsDirPath, exist_ok=True)
    logging.info("Directories created successfully")
except Exception as e:
    logging.error(f"Failed to create directories: {e}")
    sys.exit(1)

# File I/O utilities
def ShowTextToScreen(Text):
    try:
        with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
            file.write(Text)
        logging.info("Text shown to screen")
    except Exception as e:
        logging.error(f"Error writing Responses.data: {e}")

def GetMicrophoneStatus():
    try:
        with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
            status = file.read()
        logging.info("Microphone status retrieved")
        return status
    except FileNotFoundError:
        logging.warning("Mic.data not found, initializing with default")
        SetMicrophoneStatus("False")
        return "False"
    except Exception as e:
        logging.error(f"Error reading Mic.data: {e}")
        return "False"

def SetMicrophoneStatus(Status):
    try:
        with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
            file.write(Status)
        logging.info(f"Microphone status set to: {Status}")
    except Exception as e:
        logging.error(f"Error writing Mic.data: {e}")

# Holographic Orb Widget
class HolographicOrb(QWidget):
    def _init_(self, parent=None):
        super(HolographicOrb, self)._init_(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        self.setMinimumSize(300, 300)
        logging.info("HolographicOrb initialized")

    def update_animation(self):
        self.angle += 1
        if self.angle >= 360:
            self.angle = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center_x, center_y = self.width() // 2, self.height() // 2
        radius = min(self.width(), self.height()) // 3

        # Draw glowing orb with gradient
        gradient = QRadialGradient(center_x, center_y, radius)
        gradient.setColorAt(0, QColor(0, 255, 255, 255))
        gradient.setColorAt(1, QColor(0, 128, 255, 50))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        # Draw animated rings
        for i in range(4):
            r = radius + (i * 20)
            pen = QPen(QColor(0, 255, 255, 150 - i * 30), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(center_x - r, center_y - r, r * 2, r * 2)

        # Draw rotating particles
        for i in range(12):
            particle_angle = radians(self.angle + i * 30)
            particle_radius = radius + 40
            x = center_x + particle_radius * cos(particle_angle)
            y = center_y + particle_radius * sin(particle_angle)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 255, 200))
            painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))

# Globe Placeholder (2D for now)
class GlobePlaceholder(QLabel):
    def _init_(self, parent=None):
        super(GlobePlaceholder, self)._init_(parent)
        self.setStyleSheet("background-color: blue; border-radius: 100px;")
        self.setMinimumSize(200, 200)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(50)
        logging.info("GlobePlaceholder initialized")

    def update_rotation(self):
        self.update()

# System Stats Widget
class SystemStats(QWidget):
    def _init_(self):
        super(SystemStats, self)._init_()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.stats_label = QLabel("SYSTEM STATS\nCPU: 37%\nMemory: 61%\nNetwork: 3.1 MB/s")
        self.stats_label.setStyleSheet("color: cyan; background-color: rgba(0, 0, 0, 0.8); border: 2px solid cyan; padding: 10px;")
        self.layout.addWidget(self.stats_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)
        logging.info("SystemStats initialized")

    def update_stats(self):
        try:
            cpu = random.randint(20, 80)
            memory = random.randint(40, 90)
            network = round(random.uniform(0.5, 5.0), 1)
            self.stats_label.setText(f"SYSTEM STATS\nCPU: {cpu}%\nMemory: {memory}%\nNetwork: {network} MB/s")
            logging.info("System stats updated")
        except Exception as e:
            logging.error(f"Error updating stats: {e}")

# Clock Widget
class ClockWidget(QWidget):
    def _init_(self):
        super(ClockWidget, self)._init_()
        self.time_label = QLabel("15:25:02")
        self.time_label.setStyleSheet("color: cyan; font-size: 16px; background-color: transparent;")
        layout = QHBoxLayout(self)
        layout.addWidget(self.time_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        logging.info("ClockWidget initialized")

    def update_time(self):
        try:
            current_time = time.strftime("%H:%M:%S")
            self.time_label.setText(current_time)
        except Exception as e:
            logging.error(f"Error updating time: {e}")

# Chat Section Widget
class ChatSection(QWidget):
    message_sent = pyqtSignal(str)

    def _init_(self):
        super(ChatSection, self)._init_()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Chat text display
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); color: cyan; border: 2px solid cyan; padding: 5px;")
        self.layout.addWidget(self.chat_text_edit)

        # Input and button layout
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); color: cyan; border: 2px solid cyan; padding: 5px;")
        self.input_layout.addWidget(self.input_field)

        # Stylish Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: cyan; color: black; border: none; padding: 5px 15px; border-radius: 5px;")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        # Stylish Microphone button
        self.mic_button = QPushButton("Mic")
        self.mic_button.setStyleSheet("background-color: cyan; color: black; border: none; padding: 5px 15px; border-radius: 5px;")
        self.mic_button.clicked.connect(self.toggle_mic)
        self.input_layout.addWidget(self.mic_button)

        self.layout.addLayout(self.input_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_chat)
        self.timer.start(500)
        logging.info("ChatSection initialized")

    def update_chat(self):
        try:
            with open(rf"{TempDirPath}\Responses.data", "r", encoding="utf-8") as file:
                self.chat_text_edit.setText(file.read())
        except FileNotFoundError:
            logging.warning("Responses.data not found")
        except Exception as e:
            logging.error(f"Error updating chat: {e}")

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
            except sr.UnknownValueError:
                ShowTextToScreen("Could not understand audio")
                self.add_message("Could not understand audio", "JARVIS")
            except sr.RequestError as e:
                ShowTextToScreen(f"Error with service: {e}")
                self.add_message(f"Error with service: {e}", "JARVIS")
            except Exception as e:
                logging.error(f"Microphone error: {e}")
                self.add_message(f"Microphone error: {e}", "JARVIS")

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
            "status": "System is operational. All systems are green.",
            "help": "Available commands: hello, time, date, status, help, shutdown, weather, news, joke",
            "shutdown": "Shutting down... (simulated)",
            "weather": "Weather data not available. Please integrate an API.",
            "news": "News updates not available. Please integrate an API.",
            "joke": "Why did the computer go to school? Because it wanted to be a bit smarter!"
        }
        return commands.get(command, "Command not recognized. Say 'help' for available commands.")

# Main Interface
class JarvisInterface(QMainWindow):
    def _init_(self):
        super(JarvisInterface, self)._init_()
        self.setWindowTitle("JARVIS Interface")
        self.setStyleSheet("background-color: #1a1a1a;")

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        # Holographic orb (center)
        self.holographic_orb = HolographicOrb()
        main_layout.addWidget(self.holographic_orb, 0, 1, 3, 3)

        # Globe placeholder (top-right)
        self.globe_placeholder = GlobePlaceholder()
        main_layout.addWidget(self.globe_placeholder, 0, 4, 1, 1)

        # Chat section (bottom-left)
        self.chat_section = ChatSection()
        main_layout.addWidget(self.chat_section, 3, 0, 1, 2)

        # System stats (top-left)
        self.system_stats = SystemStats()
        main_layout.addWidget(self.system_stats, 0, 0, 1, 1)

        # Clock widget (bottom-right)
        self.clock_widget = ClockWidget()
        main_layout.addWidget(self.clock_widget, 3, 4, 1, 1)

        # Protocol label (right)
        self.protocol_label = QLabel("VIOLENCE PROTOCOL")
        self.protocol_label.setStyleSheet("color: cyan; font-size: 20px; background-color: rgba(0, 0, 0, 0.8); border: 2px solid cyan; padding: 10px;")
        main_layout.addWidget(self.protocol_label, 1, 4, 1, 1)

        # Initialize microphone status
        SetMicrophoneStatus("False")
        self.resize(1200, 800)
        logging.info("JarvisInterface initialized")

    def showEvent(self, event):
        logging.info("Window shown")
        super().showEvent(event)

    def closeEvent(self, event):
        logging.info("Application closed")
        event.accept()

# Main execution
if __name__ == "__main__":
    try:
        logging.info("Starting application")
        app = QApplication(sys.argv)
        window = JarvisInterface()
        window.show()
        logging.info("Application running")
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Fatal application error: {e}")
        sys.exit(1)