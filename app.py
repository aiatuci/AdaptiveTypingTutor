"""
Entry point for desktop app
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog

import time, random, string
import pandas as pd

from ui_tools.app_config import ALLOWED_CHARS, KEYSYM_TRANSLATION_TABLE
from ui_tools.utils import replace_words


# Time that the app was started (in Unix ms)
# It's added to event.time to get the unix ms time of the event
START_TIME = round(time.time()*1e3)
print('START_TIME:', START_TIME)

class KeyEvent():
    """
    Dataclass for storing key event data.

    Attributes:
        name (str): The character or keysym of key that was pressed.
        type (str): The type of event that occurred ('up' or 'down').
        timestamp (int): The time the event occurred in milliseconds since start of app or epoch time.
    """
    def __init__(self, name: str, event_type: str, timestamp: int):
        """
        See class docstring for attributes.
        """
        self.name = name
        self.type = event_type
        self.timestamp = timestamp
    

    def __repr__(self) -> str:
        return f'<KeyEvent Dataclass: {self.name} {self.type} {self.timestamp}>'


class PromptFrame(tk.Frame):
    """
    Frame which prompts the user on what to type
    """
    def __init__(self, root, prompt: str):
        super().__init__(root)

        # Create the label and pack it to the top of the prompt frame
        self.label = tk.Label(self, text=f'Please type the following:', font=('Helvetica', 16))
        self.label.pack(side='top')

        # Text box for prompt text
        self.prompt_frame = tk.Label(self, font=('Helvetica', 14), text=prompt)
        self.prompt_frame.pack(side='top', anchor='nw')
    

    def update_prompt(self, prompt: str):
        """
        Update the prompt text
        """
        self.prompt_frame.config(text=prompt)


class InputFrame(tk.Frame):
    """
    Frame which contains the input box
    """
    def __init__(self, root):
        super().__init__(root)

        # Create the input box and pack it to the bottom of the input frame
        self.input_box = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.input_box.pack(side='bottom')


class Body(tk.Frame):
    """
    Frame which contains the prompt and input box
    """
    def __init__(self, root, prompt: str):
        super().__init__(root)

        self.prompt = prompt

        # Create the prompt frame
        self.prompt_frame = PromptFrame(self, self.prompt)
        self.prompt_frame.pack(side='top', anchor='nw', fill='x')

        # Create the input frame
        self.input_frame = InputFrame(self)
        self.input_frame.pack(side='top')



class SettingsFrame(tk.Frame):
    """
    Settings panel
    """
    def __init__(self, root: 'App'):
        super().__init__(root)
        self.root = root

        # Create the label and pack it to the top of the settings frame
        self.label = tk.Label(self, text='Settings', font=('Helvetica', 16))
        self.label.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Create the checkbox and pack it to the bottom of the settings frame
        self.log_keyup_button = tk.Checkbutton(self, text='Log keyup events', variable=root.options['log_keyup'])
        self.log_keyup_button.grid(row=1, column=0, sticky='nsew')
        
        # Button to upload results
        self.upload_button = tk.Button(self, text='Upload results', command=self.upload_callback)
        self.upload_button.grid(row=2, column=1, sticky='s')
    

    def upload_callback(self):
        self.root.upload_results()
        self.root.reload_test()
    

class App(tk.Frame):
    """
    Main application window
    """
    def __init__(self, root=None):
        super().__init__(root)

        self.options = {
            # To store the option of whether to log the keyup events
            'log_keyup': tk.BooleanVar(value=True),
        }

        # Listener for keystrokes
        self.bind_all('<KeyPress>', self.record_keystroke)
        self.bind_all('<KeyRelease>', self.record_keystroke)
        
        # List to store keystroke data
        self.keypresses: list[KeyEvent] = []

        # Placeholder for the prompt. This will probably be replaced with a server query.
        self.prompt = self.get_prompt()

        self.create_widgets()

        # pack() loads and positions the frame in the window
        self.pack()


    def create_widgets(self):
        """
        Creates the widgets for the application, including the prompt, input box, and export button.
        """
        # Create the menu bar
        self.menu_bar = tk.Menu(self)
        self.menu_bar.add_command(label='Export', command=self.export_button_callback)
        self.master.config(menu=self.menu_bar)

        # Create the body frame
        self.body = Body(self, self.prompt)
        self.body.pack(side='left', fill='y', expand=True)

        # Create the settings frame
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.pack(side='right', anchor='ne')
    

    def export_button_callback(self):
        """
        Callback for the export button
        """
        # Get the file path from the user
        file_path = filedialog.asksaveasfilename(
            defaultextension=('.csv', 'Comma Separated Values'),
            filetypes=[('Comma Separated Values', '*.csv')]
        )

        # If the user canceled the file selection, return
        if file_path == '' or file_path is None:
            return
        
        # Export the data
        self.export_data(file_path)


    def record_keystroke(self, event: tk.Event):
        """
        Callback used in the input box to record the keystroke.
        """
        # If the input box is not focused, don't record the keystroke
        if self.focus_get() is not self.body.input_frame.input_box:
            return

        # Filter out unwanted events
        if event.type not in {'2', '3'} or (event.char not in ALLOWED_CHARS and event.keysym not in ALLOWED_CHARS):  
            return

        # Create the KeystrokeEvent object
        # The conditional for the name is for special characters like 'space'
        # The timestamp is the time since the app started in ms
        keypress = KeyEvent(
            name = event.char if event.char in ALLOWED_CHARS else event.keysym, 
            event_type = 'down' if event.type == '2' else 'up',
            timestamp = event.time
            )

        print(keypress)
        self.keypresses.append(keypress)

    
    def export_data(self, file_path: str = None, return_format: str = 'df'):
        """
        Outputs the key events data to a file and returns the processed data.
        Data is processed here to not slow down the app and key recording.

        Processing steps:
            1. Replace special characters with KEYSYM_TRANSLATION_TABLE
            2. Change timestamp from relative to absolute (Unix ms)
            3. Add data into list of tuples
            4. Convert list of tuples to dataframe and save to file (if file_path is not None)

        Params:
            file_path (str): The path to the file to export to.
            return_format (str): 'df' to return a pandas dataframe, 'list' to return a list of KeyEvent objects.
        """
        if not return_format in {'df', 'list'}:
            raise ValueError(f'Invalid return_format: {return_format}')

        # Process the data and convert the keypresses to tuples
        # Ex : [] -> [('a', 'up', 16397865510847932)]
        translated_events: list[tuple[str, str, int]] = []

        for key_event in self.keypresses:
            translated_events.append((
                # Change special keys (enter, space, backspace, etc.) to their key names
                # with the dict in the config file
                replace_words(key_event.name, KEYSYM_TRANSLATION_TABLE),
                key_event.type, 
                # Change the timestamp from relative to absolute (Unix ms)
                key_event.timestamp + START_TIME
                ))
        
        # Convert the list of keypress tuples to a pandas dataframe
        # Output the dataframe to a csv file
        if file_path is not None:
            # Create the dataframe
            df = pd.DataFrame(translated_events, columns=('key', 'type', 'timestamp'))
            
            # If not logging keyup events, remove the keyup events and remove the event type column
            if not self.options['log_keyup'].get():
                # Filter for only keydown events
                df = df[df['type'] == 'down']
                # Remove the event type column
                df = df.drop(columns=['type'])
                
            # Save the dataframe to a csv file
            df.to_csv(file_path, index=False)

        if return_format == 'df':
            return df
        elif return_format == 'list':
            # Return the list of KeyEvent objects with the renamed keys and absolute timestamps
            return [KeyEvent(name, type, timestamp) for name, type, timestamp in translated_events]
        
        # This should not be accessible
        raise Exception('I don\'t know how we got here')


    def reload_test(self):
        """
        Reloads the test data from the server and updates the prompt.
        """
        # Get the new prompt
        self.prompt = self.get_prompt()

        # Update the prompt
        self.body.prompt_frame.update_prompt(self.prompt)

    @staticmethod
    def get_prompt() -> str:
        """
        Retrieves a prompt for the user to type.
        Currently a placeholder the returns a random string of length 10.
        """
        return ''.join(random.choices(string.ascii_letters, k=10))

    
    def upload_results(self):
        """
        Uploads the results to the server.
        Currently a placeholder that prints the results to the console.
        """
        print(self.keypresses[-10:])
    


if __name__ == '__main__':
    # Create the root window with some settings
    root = tk.Tk()
    root.title("Hello World!")
    root.geometry('1080x720')
    root.minsize('480','360')

    # Don't worry about this. It prevents some legacy bugs.
    root.option_add('*tearOff', False)

    # Create the application
    app = App(root)

    # Run the app
    root.mainloop()
