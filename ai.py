# -*- coding: utf-8 -*-
"""AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bOM8CXlxbkFHISEsT34ADfCg2T8h9w0B
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install selenium

# Commented out IPython magic to ensure Python compatibility.
# %pip install distutils

# Commented out IPython magic to ensure Python compatibility.
# %pip install SpeechRecognition


import json
import speech_recognition as sr
from selenium import webdriver
import pyttsx3

def assistant_speaks(output):
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()

def get_audio():
    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")
        audio = rObject.listen(source, phrase_time_limit=5)
    print("Stop.")

    try:
        text = rObject.recognize_google(audio, language='en-US')
        print("You:", text)
        return text
    except:
        assistant_speaks("Could not understand your audio, please try again!")
        return 0

def load_intents(file_path):
    with open(file_path, 'r') as file:
        intents = json.load(file)
    return intents

def process_text(input, intents):
    try:
        for intent in intents['intents']:
            if any(word in input.lower() for word in intent['keywords']):
                if intent['action'] == 'search':
                    search_web(input)
                elif intent['action'] == 'define':
                    assistant_speaks(intent['response'])
                elif intent['action'] == 'calculate':
                    query = input.lower().split('calculate')[1].strip()
                    try:
                        result = str(eval(query))
                        assistant_speaks("The answer is " + result)
                    except Exception as e:
                        assistant_speaks("Sorry, I could not calculate that.")
                return

        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)

    except Exception as e:
        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)

def search_web(input):
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if 'youtube' in input.lower():
        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("https://www.youtube.com/results?search_query=" + '+'.join(query))
        return

    elif 'wikipedia' in input.lower():
        assistant_speaks("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

    else:
        if 'google' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        elif 'search' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        else:
            driver.get("https://www.google.com/search?q=" + '+'.join(input.split()))

        return

# Driver Code
if __name__ == "__main__":
    assistant_speaks("What's your name, Human?")
    name = 'Human'
    name = get_audio()
    assistant_speaks("Hello, " + name + '.')

    # Load intents from JSON file
    intents = load_intents('intents.json')

    while True:
        assistant_speaks("What can I do for you?")
        text = get_audio().lower()

        if text == 0:
            continue

        if "exit" in text or "bye" in text or "sleep" in text:
            assistant_speaks("Ok, bye " + name + '.')
            break

        process_text(text, intents)