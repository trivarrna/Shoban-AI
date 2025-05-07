from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from dotenv import load_dotenv
import mtranslate as mt

# Load environment variables from the .env file.
load_dotenv(".env")

# Get the input language setting from the environment variable.
InputLanguage = os.getenv("InputLanguage", "en")  # Default to 'en' if not set

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new recognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from InputLanguage.
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Ensure that the 'Data' directory exists
os.makedirs("Data", exist_ok=True)

# Write the modified HTML code to a file.
with open("Data/Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the current working directory.
current_dir = os.getcwd()

# Generate the file path for the HTML file.
Link = f"{current_dir}/Data/Voice.html"

# Set Chrome options for the WebDriver.
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow media stream access
chrome_options.add_argument("--disable-notifications")  # Disable notifications
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration to avoid errors
chrome_options.add_argument("--no-sandbox")  # Disable sandbox for security
chrome_options.add_argument("--disable-dev-shm-usage")  # Fix for Docker/low-resource environments

# Initialize the Chrome WebDriver using the ChromeDriverManager.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary Files
TempDirPath = rf"{current_dir}/Files"

# Ensure the 'Files' directory exists
os.makedirs("Files", exist_ok=True)

# Function to set the assistant's status by writing to a file.
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's"]

    # Check if the query is a question and add a question mark if necessary.
    if any(word in [w.lower() for w in question_words] for word in query_words[:1]):
        new_query = new_query[:-1] + "? " if new_query[-1] not in ["?", "."] else new_query
    else:
        new_query += "?"

    # Add a period if the query is not a question.
    if query_words[-1][-1] in [".", "?"]:
        new_query = new_query[:-1] + ". "
    else:
        new_query += "."

    return new_query.capitalize()

# Function to translate text into English using the mtranslate library.
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, 'en', 'auto')
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver.
def SpeechRecognition():
    # Open the HTML file in the browser.
    driver.get(Link)

    # Wait until the start button is clickable
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "start"))).click()

    while True:
        try:
            # Get the recognized text from the HTML output element.
            Text = driver.find_element(by=By.ID, value="output").text
            if Text:
                # Stop recognition by clicking the stop button.
                driver.find_element(by=By.ID, value="end").click()

                # If the input language is English, return the modified query.
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    # If the input language is not English, translate the text and return QueryModifier(UniversalTranslator(Text))
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception as e:
            pass

# Main execution block.
if __name__ == "__main__":
    while True:
        # Continuously perform speech recognition and print the recognized text.
        Text = SpeechRecognition()
        print(Text)
