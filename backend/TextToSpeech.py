import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(".env")
AssistantVoice = os.getenv("AssistantVoice", "en-CA-LiamNeural")
 
# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text: str) -> None:
    file_path = "Data/speech.mp3"
    if os.path.exists(file_path):
        os.remove(file_path)

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
    await communicate.save(file_path)

# Function to manage Text-to-Speech functionality and audio playback
def TTS(text: str, func=lambda r=None: True) -> bool:
    try:
        asyncio.run(TextToAudioFile(text))

        pygame.mixer.init()
        pygame.mixer.music.load("Data/speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() is False:
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")
        return False

    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in finally block: {e}")

# Function to manage long text with additional assistant-style responses
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(Data) > 4 and len(Text) >= 250:
        short_text = ".".join(Data[:2]) + "..." + random.choice(responses)
        TTS(short_text, func)
    else:
        TTS(Text, func)

# Ensure the Data folder exists
os.makedirs("Data", exist_ok=True)

# Main loop
if __name__ == "__main__":
    print("Text-to-Speech Assistant (type 'exit' to quit)\n")
    while True:
        user_input = input("Enter the text: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        TextToSpeech(user_input)
