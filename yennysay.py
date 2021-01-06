import os
import threading
import time
import copy
import pyperclip
import requests
import trafilatura
from tkinter import *
import functions_voice
import subprocess

def button_press(event):
    global global_parameters

    if global_parameters['play_button']['text'].get() == "Read Aloud":
        global_parameters['command']['name'] = "Read Aloud"
        global_parameters['command']['param'] = textbox.get('1.0', 'end')
        global_parameters['play_button']['text'].set("Stop") # Next available action
        global_parameters['textbox'].configure(state='disabled')
    elif global_parameters['play_button']['text'].get() == "Stop":
        # print("Stopping the engine...")
        # functions_voice.stop_engine(global_parameters['engine'])
        # global_parameters['engine_status'] = "Stopped"
        global_parameters['command']['name'] = "Idle"
        global_parameters['command']['param'] = ""
        global_parameters['play_button']['text'].set("Waiting...") # Waiting for speaking engine to stop

def get_blocks(text):
    global global_parameters
    n_line = 1
    blocks = list()
    current_value = global_parameters['textbox'].index('insert')
    current_line = int(current_value.split(".")[0])
    current_col = int(current_value.split(".")[1])
    first_block_num = 0
    for line in text.split("\n"):
        line = re.sub("\.", ".|", line)
        line = re.sub("\?", "?|", line)
        previous_block_end = 0
        for block in line.split("|"):
            if len(block) > 0:
                block_description = {'start':str(n_line) + "." + str(previous_block_end),
                                     'end': str(n_line) + "." + str(previous_block_end + len(block)),
                                     'text':block}
                if n_line == current_line and current_col >= previous_block_end and current_col < previous_block_end + len(block):
                    first_block_num = len(blocks)
                previous_block_end = previous_block_end + len(block)
                blocks.append(block_description)
        n_line += 1
    return(blocks, first_block_num)

def highlight_block(start,end,color):
    global global_parameters
    global_parameters['textbox'].tag_add('highlightline', start, end)
    global_parameters['textbox'].tag_configure('highlightline', background=color)
    return True

def remove_highlight():
    global global_parameters
    global_parameters['textbox'].tag_delete('highlightline')

def get_text_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded == None:
        print("None in download results! Seems to be a robot detection. Trying with requests...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        r = requests.get(url = url, headers = headers)
        downloaded = r.text
    if "darkreading.com" in url:
        downloaded = re.sub("Bug Report</span>.*","",downloaded)
    summary = trafilatura.extract(downloaded)
    return(summary)

def runcmd(cmd):
    x = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

def process_buffer_tracker():
    global global_parameters
    global_parameters['buffer']['current_value']  = pyperclip.paste()
    if global_parameters['buffer']['current_value']  != global_parameters['buffer']['old_value'] :
        if global_parameters['buffer']['old_value'] == "Default_value":
            global_parameters['buffer']['old_value'] = global_parameters['buffer']['current_value'] #First time don't read buffer
        else:
            text_to_read = copy.deepcopy(global_parameters['buffer']['current_value'])
            # Telegram messages
            regexp_date = ", \[[0-9]+\.[0-9]+\.[0-9]+ [0-9]+:[0-9]+\]"
            if re.findall(regexp_date, text_to_read):
                # Exclude dates
                text_to_read = re.sub(regexp_date, "", text_to_read)
            ###
            regexp_youtube_only_url = '^https://www.youtube.com/[^ ]*$'
            if re.findall(regexp_youtube_only_url, text_to_read):
                runcmd('''"C:\Program Files\SMPlayer\smplayer.exe" "''' + text_to_read + '''" ''')
                text_to_read = "Opening Youtube URL in smplayer"
            ###
            regexp_only_url = '^http[^ ]*$'
            if re.findall(regexp_only_url, text_to_read):
                text_to_read = get_text_from_url(text_to_read)
            ###
            regexp_url = 'http[^ ]*'
            text_to_read = re.sub(regexp_url, ".URL value.", text_to_read)

            global_parameters['textbox'].delete(1.0, "end")
            global_parameters['textbox'].insert(1.0, text_to_read)
            global_parameters['buffer']['old_value'] = global_parameters['buffer']['current_value']
            button_press(False)

def process_read_aloud():
    global global_parameters
    # if global_parameters['engine_status'] == "Stopped":
    #     print("Starting the engine...")
    #     global_parameters['engine'] = functions_voice.get_engine()
    #     global_parameters['engine_status'] = "Started"
    if global_parameters['command']['name'] == "Read Aloud":
        text = global_parameters['command']['param']
        blocks, first_block_num = get_blocks(text)
        for block_num in range(first_block_num, len(blocks)):
            block = blocks[block_num]
            if global_parameters['command']['name'] == "Read Aloud":
                global_parameters['engine'] = functions_voice.get_engine()
                global_parameters['textbox'].see(block['end'])
                highlight_block(block['start'], block['end'], color='cyan')
                functions_voice.say_phrase(block['text'],
                                           global_parameters['engine'],
                                           global_parameters['voices'])
                remove_highlight()
            else:
                global_parameters['play_button']['text'].set("Read Aloud")  # Next available action
                global_parameters['textbox'].configure(state='normal')
                break
        global_parameters['command']['name'] = "Idle"
        global_parameters['play_button']['text'].set("Read Aloud")  # Next available action
        global_parameters['textbox'].configure(state='normal')

def operation_thread_function():
    global global_parameters
    while True:
        if int(global_parameters['track_clipboard'].get()) == 1:
            process_buffer_tracker()
        process_read_aloud()
        time.sleep(0.3)

def open_settings_in_editor():
    import subprocess
    subprocess.call([r"C:\Program Files\Notepad++\notepad++.exe", r"config.txt"])

root = Tk()
root.option_add('*tearOff', FALSE) # Menu
root.title("Yennysay")
root.iconbitmap(default='images/logo2.ico')

##### Global parameters

global_parameters = dict()
global_parameters['command'] = dict()
global_parameters['command']['name'] = "Idle"
global_parameters['command']['param'] = ""
global_parameters['engine'] = functions_voice.get_engine()
global_parameters['voices'] = functions_voice.get_voices()
global_parameters['engine_status'] = "Started"
global_parameters['play_button'] = dict()
global_parameters['play_button']['text'] = StringVar()
global_parameters['play_button']['text'].set("Read Aloud")
global_parameters['buffer'] = dict()
global_parameters['buffer']['current_value'] = ""
global_parameters['buffer']['old_value'] = "Default_value"
### Menu
menubar = Menu(root)
menubar.add_command(label="Settings", command=open_settings_in_editor)
menubar.add_command(label="Exit", command=root.quit)
# menubar.add_command(label="About", command=root.quit)
root.config(menu=menubar)

### Text
textFrame = Frame(root, height = 300, width = 600)
textFrame.pack(side = 'top', fill = 'both', expand = 1)
textbox = Text(textFrame, wrap='word')
scrollbar = Scrollbar(textFrame)
scrollbar['command'] = textbox.yview
scrollbar.pack(side = 'right', fill = 'y')
textbox['yscrollcommand'] = scrollbar.set
textbox.pack(side = 'left', fill = 'both', expand = 1)

global_parameters['textbox'] = textbox
global_parameters['textbox'].configure(state='normal')

### Panels
panelFrame = Frame(root, height = 40)
panelFrame.pack(side = 'bottom', fill = 'x')
button = Button(panelFrame, textvariable = global_parameters['play_button']['text'])
button.bind("<Button-1>", button_press)
button.place(x = 5, y = 5, width = 80, height = 30)
global_parameters['track_clipboard'] = StringVar()
checkbutton = Checkbutton(panelFrame, text="Track clipboard", variable=global_parameters['track_clipboard'])
checkbutton.place(x = 125, y = 5, width = 120, height = 30)
checkbutton.select()

##### Operation Thread

operation_tread = threading.Thread(target=operation_thread_function, daemon = True)
operation_tread.start()

root.mainloop()

