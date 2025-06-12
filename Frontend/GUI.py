import sys
import random
import datetime
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import Qt, QEvent, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton, QFrame, QSizePolicy
)
from PyQt5.QtGui import QMovie, QFont, QIcon, QColor, QTextCursor, QPalette
from PyQt5.QtCore import pyqtProperty
from backend.RealtimeSearchEngine import RealtimeSearchEngine

# Initialize TTS engine with better voice settings
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for different voices
engine.setProperty('rate', 150)  # Slower speech rate


# Response generator with enhanced responses
def generate_response(user_input):
    user_input = user_input.lower()
    greetings = ["Hello!", "Hi there!", "Greetings!", "Nice to see you!"]

    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return random.choice(greetings) + " I am Shoban. How can I assist you today?"
    elif "time" in user_input:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."
    elif "date" in user_input:
        return f"Today is {datetime.date.today().strftime('%A, %B %d, %Y')}."
    elif "your name" in user_input:
        return "I am Shoban, your advanced AI assistant."
    elif "bye" in user_input or "exit" in user_input:
        farewells = ["Goodbye!", "See you later!", "Have a great day!", "Until next time!"]
        return random.choice(farewells)
    else:
        return RealtimeSearchEngine(user_input)


# Speak function with error handling
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")


class AnimatedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._opacity = 1.0

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, value):
        self._opacity = value
        self.setStyleSheet(f"color: rgba(0, 255, 204, {value});")

    opacity = pyqtProperty(float, getOpacity, setOpacity)


# Main GUI class with enhanced design
class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shoban - Advanced AI Assistant")
        self.setGeometry(100, 100, 1400, 800)  # Wider window
        self.setMinimumSize(1200, 700)  # Adjusted minimum size

        # Set window icon
        self.setWindowIcon(QIcon("ai_icon.png"))  # Replace with your icon

        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Added margins

        # Create glass panel effect
        self.glass_panel = QFrame()
        self.glass_panel.setStyleSheet("""
            background-color: rgba(10, 20, 30, 0.7);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        """)
        self.glass_panel.setFixedWidth(700)  # Wider panel

        # Glass panel layout
        self.panel_layout = QVBoxLayout(self.glass_panel)
        self.panel_layout.setContentsMargins(20, 20, 20, 20)
        self.panel_layout.setSpacing(15)

        # Header with animation
        self.header = AnimatedLabel("SHOBAN AI")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("Arial", 24, QFont.Bold))

        # Add opacity animation to header
        self.header_anim = QPropertyAnimation(self.header, b"opacity")
        self.header_anim.setDuration(2000)
        self.header_anim.setStartValue(0.3)
        self.header_anim.setEndValue(1.0)
        self.header_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.header_anim.setLoopCount(-1)  # Infinite loop
        self.header_anim.start()

        self.panel_layout.addWidget(self.header)

        # Divider line
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine)
        self.divider.setStyleSheet("border: 1px solid rgba(0, 255, 204, 0.3);")
        self.panel_layout.addWidget(self.divider)

        # Chat area with modern styling and constrained height
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(15, 25, 35, 0.8);
                color: #e0e0e0;
                border: 1px solid rgba(0, 255, 204, 0.2);
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                min-height: 450px;
                max-height: 550px;
            }
        """)
        self.chat_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.panel_layout.addWidget(self.chat_area)

        # Input area
        self.input_frame = QFrame()
        self.input_frame.setStyleSheet("background: transparent;")
        self.input_layout = QHBoxLayout(self.input_frame)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setSpacing(10)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Type your message or click mic to speak...")
        self.entry.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 30, 40, 0.8);
                color: white;
                border: 1px solid rgba(0, 255, 204, 0.3);
                border-radius: 15px;
                padding: 12px 20px;
                font-size: 14px;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(0, 255, 204, 0.6);
                background-color: rgba(25, 35, 45, 0.9);
            }
        """)
        self.entry.returnPressed.connect(self.send_text_response)

        # Buttons with modern styling
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon("send_icon.svg"))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setToolTip("Send message")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 180, 150, 0.7);
                border-radius: 15px;
                padding: 10px;
                min-width: 50px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: rgba(0, 200, 170, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(0, 160, 130, 0.7);
            }
        """)
        self.send_button.clicked.connect(self.send_text_response)

        self.mic_button = QPushButton()
        self.mic_button.setIcon(QIcon("mic_icon.svg"))
        self.mic_button.setIconSize(QSize(24, 24))
        self.mic_button.setToolTip("Voice command")
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 100, 200, 0.7);
                border-radius: 15px;
                padding: 10px;
                min-width: 50px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 220, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(0, 80, 180, 0.7);
            }
        """)
        self.mic_button.clicked.connect(self.listen_and_respond)

        self.input_layout.addWidget(self.entry, 5)  # Higher stretch factor for input
        self.input_layout.addWidget(self.send_button, 1)
        self.input_layout.addWidget(self.mic_button, 1)
        self.panel_layout.addWidget(self.input_frame)

        # Add glass panel to main layout
        self.main_layout.addWidget(self.glass_panel)

        # Background with animated holographic effect
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie("gif.gif")  # Replace with your background
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.setScaledContents(True)
        self.bg_movie.start()
        self.bg_label.lower()

        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: rgba(10, 20, 30, 0.7);
                color: #00ffcc;
                border-top: 1px solid rgba(0, 255, 204, 0.2);
                font-size: 12px;
                padding: 5px;
            }
        """)
        self.status_label = QLabel("System ready")
        self.status_bar.addPermanentWidget(self.status_label)

        # Typing indicator
        self.typing_indicator = QLabel()
        self.typing_indicator.setAlignment(Qt.AlignRight)
        self.typing_indicator.setStyleSheet("""
            color: rgba(0, 255, 204, 0.7);
            font-style: italic;
            font-size: 12px;
            padding-right: 10px;
        """)
        self.typing_indicator.hide()

        # Install event filter for dynamic resizing
        self.installEventFilter(self)

        # Initial greeting
        QTimer.singleShot(1000, lambda: self.show_welcome_message())

    def show_welcome_message(self):
        welcome_msg = "Initializing Shoban AI...\nSystem ready.\nHow may I assist you today?"
        self.animate_text(welcome_msg, "Shoban:")
        speak("Shoban AI initialized and ready to assist you.")

    def animate_text(self, text, prefix=""):
        self.typing_indicator.show()
        self.chat_area.moveCursor(QTextCursor.End)

        # Split text into words for typing animation
        words = text.split()
        self.current_word = 0
        self.typing_text = ""

        def type_next_word():
            if self.current_word < len(words):
                self.typing_text += words[self.current_word] + " "
                self.chat_area.textCursor().insertText(f"{prefix} {self.typing_text}\n")
                self.chat_area.moveCursor(QTextCursor.End)
                self.current_word += 1
                QTimer.singleShot(100, type_next_word)
            else:
                self.typing_indicator.hide()
                speak(text)

        type_next_word()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        return super().eventFilter(source, event)

    def send_text_response(self):
        user_input = self.entry.text().strip()
        if not user_input:
            return

        # Add user message with different styling
        self.chat_area.moveCursor(QTextCursor.End)
        self.chat_area.textCursor().insertHtml(
            f'<p style="color: #00ffcc; margin-bottom: 10px;"><b>You:</b> {user_input}</p>'
        )
        self.entry.clear()

        # Show typing indicator
        self.typing_indicator.setText("Shoban is typing...")
        self.typing_indicator.show()
        QTimer.singleShot(1500, lambda: self.respond_to_input(user_input))

    def listen_and_respond(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            # Visual feedback for listening
            old_style = self.mic_button.styleSheet()
            self.mic_button.setStyleSheet(old_style + "background-color: rgba(200, 0, 0, 0.7);")
            self.status_label.setText("Listening...")

            try:
                self.chat_area.append("<i style='color: #ff9900;'>Listening...</i>")
                QApplication.processEvents()  # Update UI immediately

                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

                user_input = recognizer.recognize_google(audio)
                self.chat_area.append(f"<p style='color: #00ffcc; margin-bottom: 10px;'><b>You (voice):</b> {user_input}</p>")
                self.respond_to_input(user_input)

            except sr.WaitTimeoutError:
                self.chat_area.append("<i style='color: #ff3300;'>Listening timed out. Please try again.</i>")
            except sr.UnknownValueError:
                self.chat_area.append("<i style='color: #ff3300;'>Sorry, I couldn't understand that.</i>")
            except sr.RequestError as e:
                self.chat_area.append(f"<i style='color: #ff3300;'>Error: {str(e)}</i>")
            finally:
                self.mic_button.setStyleSheet(old_style)
                self.status_label.setText("Ready")

    def respond_to_input(self, user_input):
        self.typing_indicator.hide()
        response = generate_response(user_input)

        # Format response with HTML for better appearance
        formatted_response = response.replace('\n', '<br>')
        formatted_response = f"""<div style="
            background-color: rgba(0, 50, 70, 0.3);
            border-left: 3px solid #00ffcc;
            padding: 12px;
            margin: 10px 0;
            border-radius: 0 8px 8px 0;
        "><b>Shoban:</b><br>{formatted_response}</div>"""

        self.chat_area.moveCursor(QTextCursor.End)
        self.chat_area.textCursor().insertHtml(formatted_response)
        self.chat_area.append("")  # Add empty line

        # Auto-scroll to bottom
        self.chat_area.ensureCursorVisible()

        # Speak the response
        speak(response)

    def clear_chat(self):
        self.chat_area.clear()
        self.chat_area.append("<i style='color: #666;'>Chat history cleared</i>")


# Run App
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application style and palette
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(10, 20, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 25, 35))
    palette.setColor(QPalette.AlternateBase, QColor(20, 30, 40))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(20, 30, 40))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(0, 150, 150))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = JarvisWindow()
    window.show()
    sys.exit(app.exec_())
