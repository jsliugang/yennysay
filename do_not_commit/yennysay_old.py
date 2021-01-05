import pyperclip
import time
import functions_voice

old_value = "Default_value"
engine, voices = functions_voice.get_engine()

while True:

    time.sleep(1)

functions_voice.stop_engine(engine)


