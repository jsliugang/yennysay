import functions_voice
import time
import re

engine, voices = functions_voice.get_engine()

#To do make a list

phrases = '''
Add yesterday tasks. Local admin ignore _Disabled
'''

def get_last_phrase(phrases):
    phrases = phrases.split("\n")
    for temp_phrase in phrases: #Take last line that is not empty
        if not re.findall("^[ \t]*$",temp_phrase):
            phrase = temp_phrase
    return(phrase)

def get_first_uncommented_phrase(phrases):
    phrases = phrases.split("\n")
    for temp_phrase in phrases: #Take First line that is not empty and commented
        if not re.findall("^[ \t]*#",temp_phrase) and not re.findall("^[ \t]*$",temp_phrase):
            return(temp_phrase)

#phrase = get_last_phrase(phrases)
phrase = get_first_uncommented_phrase(phrases)

t = 0
step = 15
while True:
    functions_voice.say_phrase(phrase, engine, voices)
    functions_voice.say_phrase(str(t) + " seconds", engine, voices)
    time.sleep(step)
    t += step

functions_voice.stop_engine(engine)