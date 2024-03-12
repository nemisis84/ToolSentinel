import speech_recognition as sr
import pyttsx3

def recognize_voice():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_vosk(audio)
        print("You said:", text)

    except sr.UnknownValueError:
        print("Couldn't understand what you said")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    print("Done")

def speak(message):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-100)
    engine.say('{}'.format(message))
    engine.runAndWait()

#spoken_text = recognize_voice()
speak('throughout heaven and earth, i alone, am the honored one')
