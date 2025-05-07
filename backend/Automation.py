# Import required libraries
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables from the .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define CSS classes for parsing specific elements in HTML content
classes = ["zCubwf", "hgKElc", "LtkOO sy7ric", "zOLcW", "gsrt"]

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Async function to open an app
async def OpenApp(command):
    if "open it" in command or "open file" == command:
        print("[yellow]Ignored unrecognized open command[/yellow]")
        return
    await asyncio.to_thread(appopen, command.removeprefix("open "))

# Async function to close an app
async def CloseApp(command):
    await asyncio.to_thread(close, command)

# Async function to perform Google search
async def GoogleSearch(command):
    await asyncio.to_thread(search, command)

# Async function to perform YouTube search
async def YouTubeSearch(command):
    await asyncio.to_thread(playonyt, command)

# Async function to execute a system command
async def System(command):
    await asyncio.to_thread(subprocess.run, command, shell=True)

# Translate and execute a list of commands asynchronously
async def TranslateAndExecute(commands: list[str]):
    tasks = []
    for command in commands:
        if command.startswith("open "):
            tasks.append(OpenApp(command))
        elif command.startswith("close "):
            tasks.append(CloseApp(command.removeprefix("close ")))
        elif command.startswith("google search "):
            tasks.append(GoogleSearch(command.removeprefix("google search ")))
        elif command.startswith("youtube search "):
            tasks.append(YouTubeSearch(command.removeprefix("youtube search ")))
        elif command.startswith("system "):
            tasks.append(System(command.removeprefix("system ")))
        elif command.startswith("general "):
            print("[yellow]General command recognized (not implemented yet).[/yellow]")
        elif command.startswith("realtime "):
            print("[yellow]Realtime command recognized (not implemented yet).[/yellow]")
        else:
            print(f"[red]No Function Found for: {command}[/red]")

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        yield result

# Wrapper to start the automation from a list of commands
async def Automation(commands: list[str]):
    async for _ in TranslateAndExecute(commands):
        pass  # Processed

# Extra async utilities
async def VoiceCommand(command):
    print(f"Processing voice command: {command}")
    return True

async def WebScrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for class_name in classes:
        elements = soup.find_all(class_=class_name)
        for element in elements:
            print(element.text)
    return True

async def KeyboardAction(key):
    keyboard.press(key)
    keyboard.release(key)
    return True

async def FileManager(action, file_path):
    if action == "open":
        os.startfile(file_path)
    elif action == "delete":
        os.remove(file_path)
    return True

async def ScheduleTask(task, time):
    print(f"Scheduling {task} at {time}")
    return True

async def EmailSender(to, subject, body):
    print(f"Sending email to {to} with subject '{subject}'")
    return True

async def CalendarEvent(event, date):
    print(f"Adding event '{event}' on {date}")
    return True

async def MusicPlayer(action, song=None):
    if action == "play":
        print(f"Playing {song}")
    elif action == "pause":
        print("Pausing music")
    return True

async def WeatherUpdate(location):
    print(f"Getting weather for {location}")
    return True

async def NewsFeed(category):
    print(f"Fetching news for {category}")
    return True

# End of script
if __name__ == "__main__":
    print("[green]Automation module is ready. Run your async logic from here if needed.[/green]")
    import asyncio

    while True:
        user_input = input("Enter your command (or type 'exit' to quit): ").strip().lower()
        if user_input == "exit":
            break
        asyncio.run(Automation([user_input]))

