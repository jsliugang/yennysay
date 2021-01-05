import pyttsx3
import regex
import json

def get_voices_report(engine):
    voices = engine.getProperty('voices')
    for voice in voices:
        print("Voice:")
        print(" - ID: %s" % voice.id)
        print(" - Name: %s" % voice.name)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)

def get_engine():
    engine = pyttsx3.init()
    return engine

def get_voices():
    # Voice IDs pulled from engine.getProperty('voices')
    # These will be system specific
    f = open("config.txt","r")
    config = json.loads(f.read())
    f.close()
    voices = config['voices']
    return voices

def say_phrase(phrase, engine, voices):
    # Use female English voice
    if regex.search(r'\p{IsCyrillic}', phrase):
        engine.setProperty('voice', voices["ru_voice"]['id'])
        engine.setProperty('rate', voices["ru_voice"]['rate'])
    else:
        engine.setProperty('voice', voices["en_voice"]['id'])
        engine.setProperty('rate', voices["en_voice"]['rate'])
    engine.say(phrase)
    engine.runAndWait()

def stop_engine(engine):
    engine.stop()