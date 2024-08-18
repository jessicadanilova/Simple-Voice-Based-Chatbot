import tkinter as tk
from tkinter import scrolledtext, simpledialog
import nltk
from nltk.stem import PorterStemmer
import tensorflow as tf
import numpy as np
import random
import json
import pickle
import pyttsx3
import speech_recognition as sr
from selenium import webdriver
import re

# Download NLTK data
nltk.download('punkt')

# Load intents
with open('intents.json') as json_data:
    intents = json.load(json_data)

# Initialize stemmer
stemmer = PorterStemmer()

# Load training data
data = pickle.load(open("training_data", "rb"))
words = data['words']
classes = data['classes']

# Load model
model = tf.keras.models.load_model("model.h5")

# Create Tkinter window
window = tk.Tk()
window.title("CuBot Assistant")
window.geometry("600x700")
window.configure(bg="light blue")
window.resizable(False, False)

# Function to classify user input
def classify(sentence):
    bag = bow(sentence, words)
    results = model.predict(np.array([bag]))
    results = [[i, r] for i, r in enumerate(results[0])]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    return return_list

# Function to clean up sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# Function to create bag of words
def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

# Function to speak the response
def assistant_speaks(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to add a chat message to the conversation window
def add_chat_message(sender, message, side):
    frame = tk.Frame(conversation_text, bg="light blue", padx=5, pady=5)
    if side == "right":
        frame.pack(anchor="e", padx=5, pady=5)
    else:
        frame.pack(anchor="w", padx=5, pady=5)

    label_sender = tk.Label(frame, text=sender, bg="#D4FFF9")
    label_sender.pack(side=tk.TOP)
    
    label_message = tk.Label(frame, text=message, bg="light blue")
    label_message.pack(side=tk.BOTTOM)

# Function to initiate conversation and prompt user for response
def initiate_conversation():
    user_name = simpledialog.askstring("CuBot", "Hello! What's your name?")
    if user_name:
        assistant_speaks("Hello, " + user_name + "! I'm CuBot. How can I assist you today?")
        add_chat_message("CuBot", "Hello, " + user_name + "! I'm CuBot. How can I assist you today?", "left")
    else:
        assistant_speaks("Hello! I'm CuBot. How can I assist you today?")
        add_chat_message("CuBot", "Hello! I'm CuBot. How can I assist you today?", "left")


# Function to get audio input from user
def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        process_user_input(user_input)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        assistant_speaks("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Error: {e}")
        assistant_speaks("Error occurred. Please try again.")


# Initialize global WebDriver instance
driver = None

def initialize_driver():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()

def process_user_input(user_input):
    global driver

    if user_input.lower() == "exit":
        if driver:
            driver.quit()
        window.destroy()
    elif "google" in user_input.lower():
        if not driver:
            initialize_driver()
        query = user_input.lower().split('google')[1].strip()
        driver.get("https://www.google.com/search?q=" + "+".join(query.split()))
    elif "youtube" in user_input.lower():
        if not driver:
            initialize_driver()
        query = user_input.lower().split('youtube')[1].strip()
        driver.get("https://www.youtube.com/results?search_query=" + "+".join(query.split()))
    elif "open maps" in user_input.lower():
        if not driver:
            initialize_driver()
        assistant_speaks("Please specify your destination or location.")
    elif "directions" in user_input.lower():
        if not driver:
            initialize_driver()
        assistant_speaks("Please specify your starting point and destination.")
    elif re.match(r'^[0-9+\-*/(). ]+$', user_input):
        try:
            result = eval(user_input)
            add_chat_message("You", user_input, "right")
            assistant_speaks(str(result))
            add_chat_message("CuBot", str(result), "left")
        except Exception as e:
            error_message = "Error: " + str(e)
            assistant_speaks(error_message)
            add_chat_message("CuBot", error_message, "left")
    else:
        add_chat_message("You", user_input, "right")
        results = classify(user_input)
        if results:
            for i in intents['intents']:
                if results[0][0] == i['tag']:
                    response = random.choice(i['responses'])
                    assistant_speaks(response)
                    add_chat_message("CuBot", response, "left")
                    break
        else:
            assistant_speaks("I'm sorry, I didn't understand that.")
            add_chat_message("CuBot", "I'm sorry, I didn't understand that.", "left")





# Create button to initiate conversation with blue-ish color
initiate_button = tk.Button(window, text="Initiate Conversation", command=initiate_conversation, bg="#4a90e2", fg="white", relief=tk.RAISED, font=("Arial", 12, "bold"))
initiate_button.pack(pady=10)

# Create button to trigger voice input with blue-ish color
voice_button = tk.Button(window, text="Speak", command=get_audio, bg="#4a90e2", fg="white", relief=tk.RAISED, font=("Arial", 12, "bold"))
voice_button.pack(pady=10)

# Create padding frame
padding_frame = tk.Frame(window, height=20, bg="light blue")
padding_frame.pack()

# Create scrolled text widget to display conversation history
conversation_text = scrolledtext.ScrolledText(window, width=50, height=20)
conversation_text.pack()

# Run the Tkinter event loop
window.mainloop()