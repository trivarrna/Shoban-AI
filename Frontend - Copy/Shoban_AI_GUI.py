
import customtkinter as ctk
import threading
import os
from Automation import handle_command
from Groq_chatbot import get_chat_response

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ShobanAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shoban AI - Jarvis Interface")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_widgets()
        self.chat_history = []

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.chat_box = ctk.CTkTextbox(self.frame, width=600, height=300, corner_radius=10)
        self.chat_box.configure(state="disabled")
        self.chat_box.pack(padx=10, pady=(10, 5))

        self.entry = ctk.CTkEntry(self.frame, width=500, placeholder_text="Type your message...")
        self.entry.pack(side="left", padx=(10, 5), pady=10)
        self.entry.bind("<Return>", lambda event: self.send_text_command())

        self.send_button = ctk.CTkButton(self.frame, text="Send", command=self.send_text_command)
        self.send_button.pack(side="left", padx=5, pady=10)

        self.mic_button = ctk.CTkButton(self.frame, text="🎙️", command=self.listen_command)
        self.mic_button.pack(side="left", padx=5, pady=10)

        self.command_frame = ctk.CTkFrame(self)
        self.command_frame.pack(pady=(0, 20))

        self.create_command_buttons()

    def create_command_buttons(self):
        buttons = [
            ("Open Browser", "open browser"),
            ("Weather", "what's the weather"),
            ("Play Music", "play music"),
            ("Open YouTube", "open YouTube"),
            ("News", "get latest news")
        ]

        for label, command in buttons:
            btn = ctk.CTkButton(self.command_frame, text=label,
                                command=lambda c=command: self.send_text_command(cmd=c))
            btn.pack(side="left", padx=10)

    def send_text_command(self, event=None, cmd=None):
        user_input = cmd if cmd else self.entry.get().strip()
        if user_input == "":
            return

        self.entry.delete(0, "end")
        self.display_chat("You", user_input)

        thread = threading.Thread(target=self.process_response, args=(user_input,))
        thread.start()

    def process_response(self, command):
        if command.startswith(("open", "play", "search", "launch")):
            response = handle_command(command)
        else:
            response = get_chat_response(command)

        self.display_chat("Shoban", response)

    def display_chat(self, sender, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{sender}: {message}
")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def listen_command(self):
        self.display_chat("Shoban", "Listening... (voice input logic goes here)")

if __name__ == "__main__":
    app = ShobanAIApp()
    app.mainloop()
