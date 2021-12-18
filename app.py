"""
Entry point for desktop app
"""

import tkinter as tk
from tkinter import scrolledtext
import time
import pandas as pd

from ui_tools.app_config import ALLOWED_CHARS, KEYSYM_TRANSLATION_TABLE


# Time that the app was started (in Unix ms)
# It's added to event.time to get the unix ms time of the event
START_TIME = int(time.time()*1e7)
print('START_TIME:', START_TIME)

class KeyEvent():
    """
    Dataclass for storing key event data.
    """
    def __init__(self, key: str, event_type: str, timestamp: int):
        """
        Params:
            key (str): The character or name of key that was pressed.
            event_type (str): The type of event that occurred ('up' or 'down').
            timestamp (int): The time the event occurred in unix epoch milliseconds.
        """
        self.key = key
        self.type = event_type
        self.timestamp = timestamp
    

    def __repr__(self) -> str:
        return f'<KeyEvent Dataclass: {self.key} {self.type} {self.timestamp}>'


class PromptFrame(tk.Frame):
    """
    Frame which prompts the user on what to type
    """
    def __init__(self, root):
        super().__init__(root)
        # Create the label and pack it to the top of the prompt frame
        self.label = tk.Label(self, text='Please type the following: "Hello World!"')
        self.label.pack(side='top')


class InputFrame(tk.Frame):
    """
    Frame which contains the input box
    """
    def __init__(self, root):
        super().__init__(root)
        # Create the input box and pack it to the bottom of the input frame
        self.input_box = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.input_box.pack(side='bottom')


class App(tk.Frame):
    """
    Main application window
    """
    def __init__(self, master=None):
        super().__init__(master)
        # pack() loads and positions the frame in the window
        self.pack()

        # Listener for keystrokes
        self.bind_all('<KeyPress>', self.record_keystroke)
        self.bind_all('<KeyRelease>', self.record_keystroke)
        
        # List to store keystroke data
        self.keypresses: list[KeyEvent] = []

        self.create_widgets()


    def create_widgets(self):
        """
        Creates the widgets for the application
        """
        # Create the prompt frame
        self.prompt_frame = PromptFrame(self)
        self.prompt_frame.pack(side='top')

        # Create the input frame
        self.input_frame = InputFrame(self)
        self.input_frame.pack(side='top')
    

    def record_keystroke(self, event: tk.Event):
        """
        Records the keystroke
        """
        # Filter out unwanted events
        if event.type not in {'2', '3'} or event.char == '':  
            return

        keypress = KeyEvent(
            key = event.keysym, 
            event_type = 'down' if event.type == '2' else 'up',
            timestamp = START_TIME + event.time
            )

        print(keypress)
        self.keypresses.append(keypress)

    
    def output_data(self, file_path: str = './data.csv'):
        """
        Outputs the key events data to a file and returns the list of data.

        Data is processed here to not slow down the app and key recording.
        """




if __name__ == '__main__':
    # Create the root window
    root = tk.Tk()
    root.title("Hello World!")
    root.geometry('1080x720')
    root.minsize('480','360')
    root.option_add('*tearOff', False)

    # Create the application
    app = App(root)

    root.mainloop()
