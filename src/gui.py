import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

from remove import find_profanities
from transcribe import transcribe
from censor import mute_sections

        
class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated AI Censoring")
        self.geometry('800x600')
        self.drop_screen = DropScreen(self, self.show_options_screen)
        self.drop_screen.pack(fill=tk.BOTH, expand=True)
    
    def show_options_screen(self, filepath):
        self.drop_screen.pack_forget()  # Hide the drop screen
        self.options_screen = OptionsScreen(self, filepath)
        self.options_screen.pack(fill=tk.BOTH, expand=True)


class DropScreen(tk.Frame):
    def __init__(self, master, on_file_drop):
        super().__init__(master, bg='lightgrey', bd=2, relief='sunken')
        self.on_file_drop = on_file_drop
        drop_label = tk.Label(self, text="Drop MP3 file here", bg='lightgrey')
        drop_label.pack(expand=True, fill=tk.BOTH)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        file_types = ['.mp3']
        valid_files = [f for f in self.master.tk.splitlist(event.data) if any(f.endswith(ft) for ft in file_types)]
        if not valid_files:
            messagebox.showerror("Error", "Please drop only MP3 files.")
            return
        for f in valid_files:
            self.on_file_drop(f)

class OptionsScreen(tk.Frame):
    def __init__(self, master, filepath):
        super().__init__(master)
        self.filepath = filepath  # Store the full path
        self.directory_var = tk.StringVar(value=os.getcwd())
        self.filename_var = tk.StringVar(value="censored_output.mp3")  # Default file name
        self.status_var = tk.StringVar()
        filename = os.path.basename(filepath)  # Extract filename for display
        
        filename_label = tk.Label(self, text=filename)
        filename_label.pack(pady=10)

        self.status_label = tk.Label(self, textvariable=self.status_var)
        self.status_label.pack(pady=10)
        
        options = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
        self.size_var = tk.StringVar()
        size_dropdown = ttk.Combobox(self, textvariable=self.size_var, values=options, state="readonly")
        size_dropdown.pack(fill=tk.X, padx=10, pady=10)
        size_dropdown.set("Select size")
        size_dropdown.set("medium")  
        
        dir_frame = tk.Frame(self)
        dir_frame.pack(fill=tk.X, padx=10, pady=10)
        dir_label = tk.Label(dir_frame, text="Output Directory:")
        dir_label.pack(side=tk.LEFT)
        dir_button = tk.Button(dir_frame, text="Choose", command=self.select_output_directory)
        dir_button.pack(side=tk.RIGHT)
        dir_entry = tk.Entry(dir_frame, textvariable=self.directory_var, state='readonly')
        dir_entry.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        # File name entry
        file_frame = tk.Frame(self)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        file_label = tk.Label(file_frame, text="Output File Name:")
        file_label.pack(side=tk.LEFT)
        file_entry = tk.Entry(file_frame, textvariable=self.filename_var)
        file_entry.pack(fill=tk.X, expand=True, side=tk.RIGHT)
        
        # Start button at the bottom
        start_button = tk.Button(self, text="Start", command=self.start_process)
        start_button.pack(pady=10)
        



    def select_output_directory(self):
        dirname = filedialog.askdirectory(parent=self, initialdir="/", title='Please select a directory')
        if dirname:
            self.directory_var.set(dirname)

    def start_process(self):
        # Start the processing in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        
            chosen_model_size = self.size_var.get()
            valid_sizes = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
            if chosen_model_size not in valid_sizes:
                messagebox.showerror("Error", "Please select a valid model size.")
                return  # Do not proceed further

        
            self.status_var.set("Starting process...")
            chosen_model_size = self.size_var.get() 
            print(f"Chosen model size: {chosen_model_size}")  # For debugging purposes

            # Assuming the transcribe function accepts a model_type parameter
            transcribed_data = transcribe(self.filepath, model_type=chosen_model_size)

            matches = find_profanities(transcribed_data)
            self.status_var.set(f"Found {len(matches)} profanities. Muting sections...")

            timestamps = [match['timestamp'] for match in matches]
            
            output_path = os.path.join(self.directory_var.get(), self.filename_var.get())
            mute_sections(self.filepath, timestamps, output_path)
            self.status_var.set(f"Process complete. Processed audio saved to: {output_path}")

