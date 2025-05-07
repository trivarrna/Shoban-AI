from groq import Groq
from json import load, dump
import datetime
import os
from dotenv import dotenv_values

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the API key.
client = Groq(api_key=GroqAPIKey)

# Path to the chat log
chat_log_path = "Data/ChatLog.json"

# Ensure the data directory exists
os.makedirs("Data", exist_ok=True)

# Initialize chat log
messages = []
if os.path.exists(chat_log_path) and os.path.getsize(chat_log_path) > 0:
    try:
        with open(chat_log_path, "r") as f:
            messages = load(f)
    except Exception:
        messages = []
else:
    with open(chat_log_path, "w") as f:
        dump([], f)

# System message with chatbot rules
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [{"role": "system", "content": System}]

# Function to get current date and time
def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed,\n"
        f"Day: {now.strftime('%A')}\nDate: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\nYear: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours : {now.strftime('%M')} minutes : {now.strftime('%S')} seconds.\n"
    )

# Clean and format the AI's response
def AnswerModifier(answer):
    return "\n".join([line for line in answer.split("\n") if line.strip()])

# Main chatbot function
def ChatBot(query):
    try:
        # Load existing messages
        with open(chat_log_path, "r") as f:
            messages = load(f)

        # Add system prompt only if it's a new session
        if not any(m["role"] == "system" for m in messages):
            messages.insert(0, {"role": "system", "content": System})

        # Append user's query
        messages.append({"role": "user", "content": query})

        # Call Groq API with streaming
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        # Collect streamed answer
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})

        # Save updated messages
        with open(chat_log_path, "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(answer)

    except Exception as e:
        print(f"Error: {e}")
        # Optionally reset the chat log on failure
        with open(chat_log_path, "w") as f:
            dump([], f, indent=4)
        return "Something went wrong. Please try again."

# Entry point
if __name__ == "__main__":
    print(f"🤖 {Assistantname} is ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("Enter Your Question: ").strip()
        if not user_input:
            print("⚠️ Please enter a valid question.")
            continue
        if user_input.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break
        print(ChatBot(user_input))
