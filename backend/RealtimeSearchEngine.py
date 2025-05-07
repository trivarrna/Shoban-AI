from googlesearch import search
from groq import Groq
from json import load, dump
import json
import datetime
import re
import os
from dotenv import dotenv_values

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuration
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIkey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the provided API key
client = Groq(api_key=GroqAPIkey)

# Define the system instruction
System = f"""Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide answers in a professional way. Make sure to add full stops, commas, question marks, and use proper grammar. ***
*** Just answer the question from the provided data in a professional way. ***"""

# Ensure the data folder exists
os.makedirs("Data", exist_ok=True)

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, json.JSONDecodeError):
    messages = []
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f)

# Function to perform a Google search and format the results
def GoogleSearch(query):
    results = list(search(query, num_results=5))
    Answer = f"The search results for '{query}' are:\n"
    for i, link in enumerate(results, 1):
        Answer += f"{i}. {link}\n"
    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing extra whitespace
def AnswerModifier(Answer):
    modified_answer = re.sub(r"\s+", " ", Answer).strip()
    return modified_answer

# Predefined chatbot conversation system message and an initial user message
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

# Function to get real-time information like the current date and time
def Information():
    current_date_time = datetime.datetime.now()
    data = (
        f"Use This Real-time Information if needed:\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours, "
        f"{current_date_time.strftime('%M')} minutes, "
        f"{current_date_time.strftime('%S')} seconds.\n"
    )
    return data

# Function to handle real-time search and response generation
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    # Load the latest chat log
    try:
        with open("Data/ChatLog.json", "r") as f:
            messages = load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = []

    messages.append({"role": "user", "content": prompt})

    # Add Google search results to the system chatbot messages
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Generate a response using the Groq client
    try:
        completion = client.chat.completions.create(
            model="Llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )
    except Exception as e:
        return f"Error while generating response: {e}"

    Answer = ""
    # Concatenate response chunks from the streaming output
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = AnswerModifier(Answer)
    messages.append({"role": "assistant", "content": Answer})

    # Save the updated chat log back to the JSON file
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Remove the last system message (Google search results) to reset
    SystemChatBot.pop()

    return Answer

# Main entry point of the program for interactive querying
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break
        response = RealtimeSearchEngine(prompt)
        print("\nAssistant:", response)
