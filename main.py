import speech_recognition as sr
import pyttsx3
import subprocess
import platform
import webbrowser
import requests

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    
def listen():
    # Intialize recognizer
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # Represents the minimum length of silence (in seconds) that will register as the end of a phrase.
    # Smaller values result in the recognition completing more quickly, but might result in slower speakers being cut off.
    recognizer.pause_threshold = 0.5
    
    recognizer.energy_threshold = 0
    
    while True:
        with mic as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                # print("Audio captured. Length:", len(audio.frame_data))
                
            except sr.WaitTimeoutError:
                print("Timeout: No audio detected.")
                continue
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Please try again.")
        except sr.RequestError:
            print("Sorry, I'm having trouble connecting to the internet. Please try again.")
 
def greet():
    speak("Hello!")

def open_google():
    system = platform.system()
    if system == 'Windows':
        try:
            # For Windows, use the default browser command to open Google Chrome
            webbrowser.open('https://www.google.com', new=2)
            print("Google Chrome opened.")
        except Exception as e:
            print(f"Error opening Google Chrome: {e}")
    elif system == 'Darwin':  # macOS
        try:
            # For macOS, use 'open' command to open Google Chrome
            subprocess.run(['open', '-a', 'Google Chrome'])
            print("Google Chrome opened.")
        except Exception as e:
            print(f"Error opening Google Chrome: {e}")
    elif system == 'Linux':
        try:
            # For Linux, use the 'google-chrome' command to open Google Chrome
            subprocess.run(['google-chrome'])
            print("Google Chrome opened.")
        except Exception as e:
            print(f"Error opening Google Chrome: {e}")
    else:
        print("Sorry, I couldn't determine your operating system. Opening Google Chrome manually is not supported.")

def search_wiki(query):
    search_url = f"https://en.wikipedia.org/wiki/{query}"
    system = platform.system()

    if system == 'Windows':
        try:
            webbrowser.open(search_url, new=2)
            print(f"Searching Wikipedia for: {query}")
        except Exception as e:
            print(f"Error opening web browser: {e}")
    elif system == 'Darwin':  # macOS
        try:
            subprocess.run(['open', search_url])
            print(f"Searching Wikipedia for: {query}")
        except Exception as e:
            print(f"Error opening web browser: {e}")
    elif system == 'Linux':
        try:
            subprocess.run(['xdg-open', search_url])
            print(f"Searching Wikipedia for: {query}")
        except Exception as e:
            print(f"Error opening web browser: {e}")
    else:
        print("Sorry, I couldn't determine your operating system. Opening a web browser manually is not supported.")
    
def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    system = platform.system()
    
    if system == 'Windows':
        try:
            webbrowser.open(search_url, new=2)
            print(f"Searching Google for: {query}")
        except Exception as e:
            print(f"Error opening web browser: {e}")
    elif system == 'Darwin':  # macOS
        try:
            subprocess.run(['open', search_url])
            print(f"Searching Google for: {query}")
        except Exception as e:
            print(f"Error opening web browser: {e}")
    elif system == 'Linux':
        try:
            subprocess.run(['xdg-open', search_url])
            print(f"Searching Google for: {query}")
        except Exception as e:
            print(f"Error opening web browser: {e}")
    else:
        print("Sorry, I couldn't determine your operating system. Opening a web browser manually is not supported.")

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if weather_data["cod"] == 200:
        main_weather = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        weather_info = f"The weather in {location} is {main_weather} ({description}). " \
                       f"The temperature is {temperature:.1f}°C and the humidity is {humidity}%."
        return weather_info
    else:
        return "Sorry, I couldn't retrieve the weather information for the provided location."

def play_music():
    music_url = "https://music.youtube.com/"
    webbrowser.open(music_url, new=2)
    print("Opening YouTube Music. You can now play music from the website.")

if __name__ == "__main__":
    weather_api_key = 'YOUR API KEY'
    greet()
    while True:
        command = listen()
        if "open google" in command:
            open_google()
            speak("opened google")
        elif "search wikipedia" in command:
            search_query = command.replace("wikipedia", "").strip()
            search_query = search_query.replace("search", "").strip()
            speak(f"searching {search_query} on wikipedia")
            search_query = search_query.title()
            search_query = search_query.replace(" ", "_").strip()
            print(search_query)
            if search_query:
                search_wiki(search_query)
        elif "search" in command:
            search_query = command.replace("search", "").strip()
            speak(f"searching {search_query}")
            if search_query:
                search_google(search_query)
        elif "play music" in command:
            play_music()
        elif "weather" in command:
            location = "Taipei"
            weather_info = get_weather(weather_api_key, location)
            speak(weather_info)
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I can't handle that request.")