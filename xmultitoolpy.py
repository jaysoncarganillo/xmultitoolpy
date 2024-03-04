import time
import sys
import os
import re
import threading
import tkinter as tk
from tkinter import scrolledtext
sys.path.append(os.path.abspath("SO_site-packages"))

import pyperclip

def twitter_script(flag, text_widget, transform_to):
    recent_value = ""
    regex = "^https?:\/\/(?:x\.com|twitter\.com)\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)"

    while flag[0]:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            if re.search(regex, recent_value):
                newurl = re.sub('(?:x\.com|twitter\.com)', transform_to, recent_value)
                pyperclip.copy(newurl)
                text_widget.insert(tk.END, newurl + " converted to " + transform_to + " and copied to clipboard\n")
            else:
                text_widget.insert(tk.END, "not a twitter or x.com link\n")
        time.sleep(0.1)

def extract_numbers(flag, text_widget):
    recent_value = ""
    pattern = r'\d{19}'

    while flag[0]:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            result = re.findall(pattern, recent_value)
            if result:
                pyperclip.copy(''.join(result))
                text_widget.insert(tk.END, ''.join(result) + " copied to clipboard\n")
            else:
                text_widget.insert(tk.END, "No 19-digit numbers found in the input.\n")
        time.sleep(0.1)

def main():
    flag = [False]  # Mutable flag to control the script execution
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    text_area = scrolledtext.ScrolledText(frame)
    text_area.pack()

    def toggle(script, transform_to=None):
        if not flag[0]:
            flag[0] = True
            if transform_to:
                threading.Thread(target=script, args=(flag, text_area, transform_to)).start()
            else:
                threading.Thread(target=script, args=(flag, text_area)).start()
            button_vx.config(text='Stop')
            button_tw.config(text='Stop')
            button_num.config(text='Stop')
        else:
            flag[0] = False
            button_vx.config(text='Start vxTwitter')
            button_tw.config(text='Start Twitter')
            button_num.config(text='Start Number Extraction')

    button_vx = tk.Button(frame, text="Start vxTwitter", command=lambda: toggle(twitter_script, 'vxtwitter.com'))
    button_vx.pack()

    button_tw = tk.Button(frame, text="Start Twitter", command=lambda: toggle(twitter_script, 'twitter.com'))
    button_tw.pack()

    button_num = tk.Button(frame, text="Start Number Extraction", command=lambda: toggle(extract_numbers))
    button_num.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
