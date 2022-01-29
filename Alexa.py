import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import webbrowser


speech_engine = sr.Recognizer()
talk_engine = pyttsx3.init()
voices = talk_engine.getProperty('voices')
talk_engine.setProperty("voice", voices[1].id)
talk_engine.setProperty("rate", 135)


def music(songOrArtist):
    
    pywhatkit.playonyt(songOrArtist)


def talk(text):

    talk_engine.say(text)
    talk_engine.runAndWait()


def hear_activation_voice():

    try:
        with sr.Microphone() as source:
            print("say alexa to activate")
            print('listening...')
            speech_engine.adjust_for_ambient_noise(source, duration=0.2)
            voice = speech_engine.listen(source)
            command = speech_engine.recognize_google(voice)
            command = command.lower()
            if command != None:
                if "alexa" in command:
                    alexa_activate()

    except:
        pass


def hear():
    try:
        with sr.Microphone() as source:
            print("say what you want")
            print('listening...')
            speech_engine.adjust_for_ambient_noise(source, duration=0.2)
            voice = speech_engine.listen(source)
            command = speech_engine.recognize_google(voice)
            command = command.lower()
            if command != None:
               return command

    except:
        pass


def alexa_activate():

    talk('Tell me what you want')
    run_alexa(hear())


def run_alexa(command):

    if 'play' in command:
        songOrArtist = command.replace('play', '')
        talk('playing' + songOrArtist)
        music(songOrArtist)

    elif 'google' in command:
        webbrowser.open('www.google.com')

    elif 'stackoverflow' in command:
        webbrowser.open('www.stackoverflow.com')

    elif 'wiki' in command:
        try:
            command = command.replace('wiki', '')
            talk("searching wikipedia")
            results = wikipedia.summary(command, sentences=2)
            talk("According to wikipedia" + results)
        except Exception as e:
            talk('sorry I could not find any results')

    elif 'wikipedia' in command:
        try:
            command = command.replace('wikipedia', '')
            talk("searching wikipedia")
            results = wikipedia.summary(command, sentences=2)
            talk("According to wikipedia" + results)
        except Exception as e:
            talk('sorry I could not find any results')

    elif 'who is' in command:
        try:
            command = command.replace('who is', '')
            talk("searching wikipedia")
            results = wikipedia.summary(command, sentences=2)
            talk("According to wikipedia" + results)
        except Exception as e:
            talk('sorry I could not find any results')

    elif 'what is' in command:
        try:
            command = command.replace('what is', '')
            talk("searching wikipedia")
            results = wikipedia.summary(command, sentences=2)
            talk("According to wikipedia" + results)
        except Exception as e:
            talk('sorry I could not find any results')

    elif 'who the heck is' in command:
        try:
            command = command.replace('who the heck is', '')
            talk("searching wikipedia")
            results = wikipedia.summary(command, sentences=2)
            talk("According to wikipedia" + results)
        except Exception as e:
            talk('sorry I could not find any results')

    elif 'what the heck is' in command:
        try:
            command = command.replace('what the heck is', '')
            talk("searching wikipedia")
            results = wikipedia.summary(command, sentences=2)
            talk("According to wikipedia" + results)
        except Exception as e:
            talk('sorry I could not find any results')

    elif 'who are you' in command:
        talk('I am alexa a virtual assistant who can help you with your daily needs')

    elif 'who am i' in command:
        talk('Swarnava Bose')

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif 'time' in command:
        strtime = datetime.datetime.now().strftime("%I:%M:%p")
        talk("The time is %s" % strtime)

    elif 'date' in command:
        strdate = datetime.datetime.today().strftime("%D %m %y")
        talk("The date is %s" % strdate)


def main():
    hear_activation_voice()


if __name__ == "__main__":
    
    while True:
        main()