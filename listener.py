import speech_recognition as sr
from ui import show_user

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        show_user(command)
        return command.lower()

    except sr.UnknownValueError:
        return "i didn't catch that"

    except sr.RequestError:
        return "speech error"