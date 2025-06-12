from PyQt5.QtCore import pyqtSignal, QObject
from flask import signals


class GUISignals(QObject):
    status_updated = pyqtSignal(str)
    text_to_display = pyqtSignal(str)
    mic_state_changed = pyqtSignal(bool)

# Shared functions
def speak(text):
    """Centralized TTS function"""
    ...

def SetAssistantStatus(text):
    """Update status bar"""
    signals.status_updated.emit(text)

def ShowTextToScreen(text):
    """Display formatted text"""
    signals.text_to_display.emit(text)

def GetAssistantStatus(text):
    signals.status_updated.emit(text)

def SetMicrophoneStatus(text):
    signals.status_updated.emit(text)

def GetMicrophoneStatus(text):
    signals.status_updated.emit(text)