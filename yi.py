import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

# Function to process user queries
def process_query(query):
    response = ""
    if "hello" in query:
        response = greet()
    elif "what is your name" in query:
        response = "My name is Laptop."
    elif "how are you" in query:
        response = "I'm fine, thank you!"
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."
    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        response = "Opening Google."
    elif "play music" in query:
        music_dir = "C:/Users/YourUsername/Music"  # Update this path
        try:
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                response = "Playing music."
            else:
                response = "No music files found in the directory."
        except Exception as e:
            response = f"Error: {e}"
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {current_time}"
    elif "goodbye" in query:
        response = "Goodbye!"
    else:
        response = "I'm sorry, I didn't understand that."
    
    return response

# Streamlit application
st.title("Voice Assistant")

if st.button("Start Listening"):
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            st.write("Recognizing...")
            query = recognizer.recognize_google(audio)
            st.write(f"User said: {query}")
            response = process_query(query.lower())
            st.write(f"Response: {response}")
            speak(response)
        except sr.UnknownValueError:
            response = "Sorry, I didn't hear that."
            st.write(response)
            speak(response)
        except sr.RequestError as e:
            response = f"Could not request results; {e}"
            st.write(response)
            speak(response)
