from flask import Flask, render_template, jsonify,request
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import numpy as np
import sounddevice as sd
from scipy.signal import chirp
import time
import webbrowser
from gtts import gTTS
from twilio.rest import Client
import sqlite3
from sqlite3 import Error


# Global state to keep track of what the assistant is doing



app = Flask(__name__)

running = False
engine = pyttsx3.init()

loaded = True
command_count = 0



# Connect to SQLite database (or create it if it doesn't exist)
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('assistant_interactions.db')
        print("Connection established")
    except Error as e:
        print(e)
    return conn

# Create the interactions table
def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );'''
        cursor = conn.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

# Insert prompt and response into the database
def insert_interaction(conn, prompt, response):
    sql = '''INSERT INTO interactions(prompt, response)
             VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, (prompt, response))
    conn.commit()
    return cur.lastrowid


def speak(message):
    tts = gTTS(text=message, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")

   
def detect_speech():
    """
    Capture audio from the microphone and recognize speech using Google's API.
    Retries up to three times if an error occurs.
    
    Returns:
        str: The recognized speech as text, or an error message after three failed attempts.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Speech Recognition
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            # Speak the error message if speech is not understood
            error_message = "Sorry, I did not understand that. Please try again"
            speak(error_message)
            return error_message
        except sr.RequestError:
            # Speak the error message if there is a connection issue
            error_message = "Sorry, I'm having trouble connecting to the service. Please try again"
            speak(error_message)
            return error_message
                

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    global command_count
    if command_count == 0:
        introduce()
        time.sleep(2)
    command = detect_speech()
    command_count += 1
    if "exit" in command:
        speak("Exiting application.")
        return jsonify({'status': 'Assistant stopped'})
    else:
        handle_command(command)
        return jsonify({'status': f'Processed command: {command}'})
   
    


def open_email(recipient, subject='', body=''):
    mailto_url = f"mailto:{recipient}?subject={subject}&body={body}"
    webbrowser.open(mailto_url)

def ask_gemini(prompt):
    # Load environment variables from .env file
    load_dotenv()

    # Configure the Generative AI library with the API key
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Initialize the GenerativeModel
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Generate content using the model
    response = model.generate_content(prompt)
    
    # Extract text from the response
    response_text = response.text  # Adjust this line based on how `response` provides its content

    # Remove asterisks and newlines using regex
    text = re.sub(r"[*#]", "", response_text)
    return text


def generate_water_wave_sound(duration=5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate a chirp signal which can mimic water waves
    signal = chirp(t, f0=20, f1=2000, t1=duration, method='quadratic')
    return signal


def play_sound(duration=15):
   sample_rate = 44100  # Sample rate in Hz
   wave_sound = generate_water_wave_sound(duration, sample_rate)
    # Play the generated sound
   sd.play(wave_sound, samplerate=sample_rate)
   sd.wait()  # Wait until the sound finishes playing


def get_top_news(query):
    api_key = os.getenv('NEWS_API')
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&pageSize=1"
    response = requests.get(url)
    data = response.json()
    
    if data.get('articles'):
        article = data['articles'][0]
        title = article.get('title', 'No title available')
        description = article.get('description', 'No description available')
        url = article.get('url', '')
        content = article.get('content', 'No content available')

        return {
            'title': title,
            'description': description,
            'url': url,
            'content': content
        }
    else:
        return None
             

def get_weather(city):
    app_id = os.getenv('WEATHER_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app_id}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data.get('main'):
        temperature = data['main']['temp']
        weather = data['weather'][0]['description']
        return f'Temperature in {city} is : {temperature}°C, and the Weather is : {weather}'
    else:
        return 'Weather data not available.'
    
def get_location():
    token = os.getenv('LOCATION_TOKEN')
    url = f'https://ipinfo.io/108.48.7.184?token={token}'
    response = requests.get(url)
    data = response.json()
    city = data.get('city')
    return f'{city}'

def send_message(recipient_phone, text):
    account_sid =os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    # removes spaces and -
    text = re.sub(r'[ \-]', '', text)
    try:
        message = client.messages.create(
        from_='+18667023406',
        body=text,
        to=f"{recipient_phone}"
        )
        return f"Message {message.id} sent to {recipient_phone}"
    except:
        return f"Message sent to {recipient_phone}"

# Function to handle the recognized commands and execute appropriate responses
def handle_command(command):
    """
    Process the recognized speech command and respond accordingly.

    Args:
        command (str): The recognized speech command.
    """
    command = command.lower()
    response = ""
    # Define sets of keywords for different commands
    greeting_keywords = {'hi', 'hello', 'hey', 'greetings'}
    goodbye_keywords = {'goodbye', 'bye', 'see you later'}
    weather_keywords = {'weather', 'forecast', 'temperature'}
    location_keywords = {'location', 'where am i', 'my location'}
    time_keywords = {'time', 'what time is it', 'current time'}
    music_words ={'music', "sound", 'song', 'sing'}
    news_keywords = {'news', 'headline', 'top news'}
    text_message_keywords = {'send text', 'text message', 'sms', 'send message','send a message', 'text message'}

    if any(keyword in command for keyword in greeting_keywords):
        speak("Hello! How can I assist you today?")
        response = "Hello! How can I assist you today?"
    elif any(keyword in command for keyword in goodbye_keywords):
        speak("Goodbye! Have a great day!")
        response="Goodbye! Have a great day!"
    elif any(keyword in command for keyword in weather_keywords):
        speak("Let me check the weather for you.")
        city = get_location()
        time.sleep(2)
        if city != "":
            weather = get_weather(city)
            speak(weather)
            response = weather
        else:
            speak("Sorry I am unable to get the weather")
            response = "Sorry I am unable to get the weather"
    elif any(keyword in command for keyword in location_keywords):
        speak("Checking your location")
        time.sleep(2)
        response = f"You are located in {get_location()}"
        speak(response)
        
    elif any(keyword in command for keyword in time_keywords):
        speak("Checking the time.")
        time.sleep(2)
        # Get the current time
        now = datetime.now()
       
        response = f"The current time is {now.strftime('%I:%M %p')}"
        speak(response)
    elif'email' in command:
        speak('who is the recipient of the email?')
        recipient = detect_speech()
        speak('what is the subject of the email?')
        subject = detect_speech()
        speak('what is the message?')
        body = detect_speech()
        speak('Opening email client...')
        open_email(recipient, subject, body)
        response = "Opening email client>>>"
    elif any(keyword in command for keyword in music_words):
        speak('Playing sound')
        play_sound()
        response = "Playing sound"
    elif 'name' in command:
        speak("My name is Fanny. Your ai voice assistant")
        response = "My name is Fanny. Your ai voice assistant"
    elif any(keyword in command for keyword in news_keywords):
        speak("Searching for top news")
        time.sleep(2)
        article = get_top_news(command)
        if article and article['content']:
            response = f"Here is the top news article about {command}: {article['title']}. {article['content']}"
            speak(response)
        else:
            response = "Sorry, I couldn't find any news articles."
            speak(response)
    elif any(keyword in command for keyword in text_message_keywords):
        speak("What is the recipient's phone number?")
        recipient = detect_speech()
        speak('What is the message you want to send?')
        message = detect_speech()
        speak('Sending text message...')
        response = send_message(recipient, message)
        speak(response)
    else:
        speak('Searching for results')
        response = ask_gemini(command)
        speak(response)

    conn = create_connection()
    if conn is not None:
        create_table(conn)

        # Insert data
        interaction_id = insert_interaction(conn, command, response)
        print(f"Interaction stored with ID: {interaction_id}")

        # Close the connection
        conn.close()

def introduce():
    speak("Hello! I'm Fanny. Your AI voice command assistant. Please click on the button to speak and I will be ready to help you")



# Entry point of the application
if __name__ == '__main__':
    app.run()
    
   
