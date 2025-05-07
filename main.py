# Importing required modules
from Frontend.GUI import GraphicalUserInterface, SetAssistantStatus, ShowTextToScreen, TempDirectoryPath
from GraphicalInterface import SetAssistantStatus, ShowTextToScreen
from TempDirectoryPath import TempDirectoryPath
from ShowTextToScreen import ShowTextToScreen
from SetMicrophoneStatus import SetMicrophoneStatus, GetMicrophoneStatus
from TempDirectoryPath import TempDirectoryPath
from AnswerModifier import AnswerModifier, QueryModifier
from QueryModifier import QueryModifier
from GetMicrophoneStatus import GetMicrophoneStatus
from GetAssistantStatus import GetAssistantStatus
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.ChatBot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import json
import os
import threading

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f"{{'Username'}}: Hello {Assistantname}, How are you? {{Assistantname}}: Welcome {Username}. I am doing well. How may I help you? ..."
subprocesses = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Chat log management functions
def ShowDefaultChatIfNoChats():
    """Initialize default chat if ChatLog.json is empty."""
    with open(r"Data\ChatLog.json", "r", encoding="utf-8") as File:
        if len(File.read()) < 5:
            with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
                file.write("")
            with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as file:
                file.write(DefaultMessage)

def ReadChatLogJson():
    """Read and return the JSON content of ChatLog.json."""
    with open(r"Data\ChatLog.json", "r", encoding="utf-8") as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    """Format chat log by replacing 'User' and 'Assistant' with actual names."""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username)
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")
    with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    """Display formatted chat data on the GUI."""
    with open(TempDirectoryPath("Database.data"), "r", encoding="utf-8") as Data:
        if len(str(Data.read())) > 0:
            lines = Data.read().split('\n')
            result = '\n'.join(lines)
    with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as File:
        File.write(result)

# Initial setup function
def InitialExecution():
    """Perform initial setup for the assistant."""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

# Main execution logic
def MainExecution():
    """Process user queries and handle assistant responses."""
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    
    SetAssistantStatus("Listening ...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking ...")
    Decision = FirstLayerDMM(Query)
    print("")
    print(f"Decision : {Decision}")
    print("")
    
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    Merged_query = ' and '.join([''.join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")])
    
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
    
    if ImageExecution:
        with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery}, True")
        try:
            p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=False)
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")
    
    if G and R or R:
        SetAssistantStatus("Searching ...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking ...")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searching ...")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                os._exit(1)

# Thread functions
def FirstThread():
    """Continuously monitor microphone status and execute main logic."""
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available ...")

def SecondThread():
    """Initialize and run the graphical user interface."""
    GraphicalUserInterface()

# Main execution block
if _name_ == "_main_":
    InitialExecution()
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()