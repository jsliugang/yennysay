Windows tts python API. Ведь в винде есть собственный достаточно качественный tts. Глупо его не использовать.

I downloaded python-3.7.3-amd64.exe from https://www.python.org/downloads/ 
By default python will be installed at C:\Users\Alexander\AppData\Local\Programs\Python\Python37\python.exe and pip will be installed at C:\Users\Alexander\AppData\Local\Programs\Python\Python37\Scripts\pip3.7.exe
You can add this directories to path by selecting this option in installer or search for ‘edit environment variables’.

python -m pip install --upgrade pip
pip install pypiwin32 pyttsx3

# Tutorial: https://www.devdungeon.com/content/text-speech-python-pyttsx3#change_voice_language
# Desciption of the module: https://pypi.org/project/pyttsx3/

cd C:\Users\Alexander\Desktop\tts

> python get_voices.py
Voice:
 - ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0
 - Name: Microsoft Irina Desktop - Russian
 - Languages: []
 - Gender: None
 - Age: None
Voice:
 - ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0
 - Name: Microsoft Zira Desktop - English (United States)
 - Languages: []
 - Gender: None
 - Age: None
Voice:
 - ID: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0
 - Name: Microsoft David Desktop - English (United States)
 - Languages: []
 - Gender: None
 - Age: None

> python test_voice.py
