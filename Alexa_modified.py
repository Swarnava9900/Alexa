import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyjokes
import wikipedia # to use wikipedia APi
import webbrowser
from datetime import date, timedelta, datetime
import pyowm  # used to tell the weather
from Keys import OPENWEATHER # Keys.py is where I store all my API keys SHANE will use
import operator  # used for math operations
import random  # will be used throughout for random response choices
import os  # used to interact with the computer's directory

# Speech Recognition Constants
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Python Text-to-Speech (pyttsx3) Constants
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 140)

# Wake word in Listen Function
WAKE = "Alexa"

# Used to store user commands for analysis
CONVERSATION_LOG = "Conversation Log.txt"

# Initial analysis of words that would typically require a Google search
SEARCH_WORDS = {"who": "who", "what": "what", "when": "when", "where": "where", "why": "why", "how": "how"}



class Alexa:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    # Used to hear the commands after the wake word has been said
    def hear(self, recognizer, microphone, response):
        try:
            with microphone as source:
                print("Waiting for command.")
                recognizer.adjust_for_ambient_noise(source)
                recognizer.dynamic_energy_threshold = 3000
                # May reduce the time out in the future
                audio = recognizer.listen(source, timeout=5.0)
                command = recognizer.recognize_google(audio)
                return command.lower()
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Network error.")

    # Used to speak to the user
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    #to play music on youtube
    def music(self, songOrArtist):
        pywhatkit.playonyt(songOrArtist)

    # Used to open the browser or specific folders
    def open_things(self, command):
        # Will need to expand on "open" commands
        if command == "open youtube":
            Alexa.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")
            pass

        elif command == "open facebook":
            Alexa.speak("Opening Facebook.")
            webbrowser.open("https://www.facebook.com")
            pass

        elif command == "open my documents":
            Alexa.speak("Opening My Documents.")
            os.startfile("C:/Users/Notebook/Documents")
            pass

        elif command == "open my downloads folder":
            Alexa.speak("Opening your downloads folder.")
            os.startfile("C:/Users/Notebook/Downloads")
            pass

        else:
            Alexa.speak("I don't know how to open that yet.")
            pass

    # Used to answer time/date questions
    def understand_time(self, command):
        today = date.today()
        now = datetime.now()
        if "date" in command:
            Alexa.speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))

        elif "time" in command:
            Alexa.speak("It is " + now.strftime("%I") + now.strftime("%M") + now.strftime("%p") + ".")

    #to get weather of the place
    def get_weather(self, command):
        home = 'Kolkata, West Bengal'
        owm = pyowm.OWM(OPENWEATHER)
        mgr = owm.weather_manager()

        
        observation = mgr.weather_at_place(home)
        w = observation.weather
        temp = w.temperature('celsius')
        status = w.detailed_status
        Alexa.speak("It is currently " + str(int(temp['temp'])) + " degrees celsius and " + status)

    # If we're doing math, this will return the operand to do math with
    def get_operator(self, op):
        return {
            '+': operator.add,
            '-': operator.sub,
            'x': operator.mul,
            'into' : operator.mul,
            'by': operator.__truediv__,
            'Mod': operator.mod,
            'mod': operator.mod,
            '^': operator.xor,
        }[op]

    # We'll need a list to perform the math
    def do_math(self, li):
        # passes the second item in our list to get the built-in function operand
        op = self.get_operator(li[1])
        # changes the strings in the list to integers
        int1, int2 = int(li[0]), int(li[2])
        # this uses the operand from the get_operator function against the two intengers
        result = op(int1, int2)
        Alexa.speak(str(int1) + " " + li[1] + " " + str(int2) + " equals " + str(result))

    # Checks "what is" to see if we're doing math
    def what_is_checker(self, command):
        number_list = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        # First, we'll make a list a out of the string
        li = list(command.split(" "))
        # Then we'll delete the "what" and "is" from the list
        del li[0:2]

        if li[0] in number_list:
            self.do_math(li)

        elif "date" in command:
            self.understand_time(command)

        else:
            self.use_search_words(command)

    # Checks the first word in the command to determine if it's a search word
    def use_search_words(self, command):
        try:
            Alexa.speak("searching")
            results = wikipedia.summary(command, sentences=1)
            Alexa.speak("According to wikipedia" + results)
        except Exception as e:
            Alexa.speak("Here is what I found.")
            webbrowser.open("https://www.google.com/search?q={}".format(command))

    # Analyzes the command
    def analyze(self, command):
        try:

            if command.startswith('open'):
                self.open_things(command)

            elif command.startswith('play'):
                songOrArtist = command.replace('play', '')
                Alexa.speak('playing' + songOrArtist)
                self.music(songOrArtist)

            elif command == "introduce yourself":
                Alexa.speak("I am alexa a virtual assistant who can help you with your daily needs")

            elif command == "who are you" :
                Alexa.speak('I am alexa a virtual assistant who can help you with your daily needs')

            elif 'who am i' in command:
                Alexa.speak('Swarnava Bose')

            elif 'can you do for me' in command:
                Alexa.speak('i can do multiple tasks for you')

            elif 'joke' in command:
                joke = pyjokes.get_joke()
                Alexa.speak(joke)

            elif "time" in command:
                self.understand_time(command)

            elif command == "how are you":
                current_feelings = ["I'm okay.", "I'm doing well. Thank you.", "I am doing okay."]
                # selects a random choice of greetings
                greeting = random.choice(current_feelings)
                Alexa.speak(greeting)

            elif "weather" in command:
                self.get_weather(command)

            elif "what is" in command:
                self.what_is_checker(command)

            # Keep this at the end
            elif SEARCH_WORDS.get(command.split(' ')[0]) == command.split(' ')[0]:
                self.use_search_words(command)

            else:
                Alexa.speak("I don't know how to do that yet.")

        except TypeError:
            print("Warning: You're getting a TypeError somewhere.")
            pass
        except AttributeError:
            print("Warning: You're getting an Attribute Error somewhere.")
            pass

    # Used to listen for the wake word
    def listen(self, recognizer, microphone):
        while True:
            try:
                with microphone as source:
                    print("Listening.")
                    recognizer.adjust_for_ambient_noise(source)
                    recognizer.dynamic_energy_threshold = 3000
                    audio = recognizer.listen(source, timeout=5.0)
                    response = recognizer.recognize_google(audio)

                    if response == WAKE:

                        Alexa.speak("How can I help you?")
                        return response.lower()

                    else:
                        pass
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Network error.")


Alexa = Alexa()
while True:
    response = Alexa.listen(recognizer, microphone)
    command = Alexa.hear(recognizer, microphone, response)
    Alexa.analyze(command)