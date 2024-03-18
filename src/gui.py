import threading
import tkinter as tk
from ttkthemes import ThemedStyle
from tkinter import filedialog, ttk, messagebox
import tkinter.scrolledtext as ScrolledText
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import sys

import remove 
import transcribe
import censor

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated AI Audio Censoring")
        self.geometry('800x600')
        
        style = ThemedStyle(self)
        style.set_theme("ubuntu")
        
        self.drop_screen = DropScreen(self, self.show_options_screen)
        self.drop_screen.pack(fill=tk.BOTH, expand=True)
    
    def show_options_screen(self, filepath):
        self.drop_screen.pack_forget()  # Hide the drop screen
        self.options_screen = OptionsScreen(self, filepath)
        self.options_screen.pack(fill=tk.BOTH, expand=True)
        
    def show_drop_screen(self):
            if hasattr(self, 'options_screen'):
                self.options_screen.pack_forget()  # Hide the options screen
            self.drop_screen.pack(fill=tk.BOTH, expand=True)  # Show the drop screen

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert('end', str, (self.tag,))
        self.widget.configure(state='disabled')
        self.widget.see('end')

    def flush(self):
        pass

class DropScreen(tk.Frame):
    def __init__(self, master, on_file_drop):
        super().__init__(master, bg='darkorange', bd=2)
        self.on_file_drop = on_file_drop
        drop_label = tk.Label(self, text="Drop video or audio files here ['.mp3', '.wav', '.mp4', '.avi', .mkv]", bg='lightgrey')
        drop_label.pack(expand=True, fill=tk.BOTH)
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        file_types = ['.mp3', '.wav', '.mp4', '.avi', '.mkv']  # Expanded list of file types
        valid_files = [f for f in self.master.tk.splitlist(event.data) if any(f.endswith(ft) for ft in file_types)]
        if not valid_files:
            messagebox.showerror("Error", "Please drop only supported audio/video files.")
            return
        for f in valid_files:
            self.on_file_drop(f)

class OptionsScreen(tk.Frame):
    def __init__(self, master, filepath):
        super().__init__(master)
        self.filepath = filepath  # Store the full path
        self.directory_var = tk.StringVar(value=os.getcwd())
        
        self.status_var = tk.StringVar()
        
        base_filename = os.path.splitext(os.path.basename(filepath))[0]
        file_extension = os.path.splitext(filepath)[1]

        default_output_filename = f"{base_filename}_censored{file_extension}"
        self.filename_var = tk.StringVar(value=default_output_filename)  # Use the new default file name

        filename = os.path.basename(filepath)  # Extract filename for display
        
        filename_label = tk.Label(self, text=filename)
        filename_label.pack(pady=10)

        self.status_label = tk.Label(self, textvariable=self.status_var)
        self.status_label.pack(pady=10)
        
        # Model size label and dropdown
        model_size_frame = tk.Frame(self)  # Create a frame to hold the label and dropdown together
        model_size_frame.pack(fill=tk.X, padx=10, pady=10)

        model_size_label = tk.Label(model_size_frame, text="Model Size:")
        model_size_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some padding to the right of the label for spacing

        options = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
        self.size_var = tk.StringVar()
        size_dropdown = ttk.Combobox(model_size_frame, textvariable=self.size_var, values=options, state="readonly")
        size_dropdown.set("medium")  # Set default model size
        size_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
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
        
         # Checkbox variables
        self.save_transcription_var = tk.IntVar()
        self.save_muted_timestamps_var = tk.IntVar()

        # Save Transcription checkbox
        self.save_transcription_checkbox = tk.Checkbutton(self, text="Save Transcription", variable=self.save_transcription_var)
        self.save_transcription_checkbox.pack()

        # Save Muted Timestamps checkbox
        self.save_muted_timestamps_checkbox = tk.Checkbutton(self, text="Save Muted Timestamps", variable=self.save_muted_timestamps_var)
        self.save_muted_timestamps_checkbox.pack()

        
        # Create a scrolled text widget for output logs
        self.log_text = ScrolledText.ScrolledText(self, state='disabled', height=10)
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Add the 'Process Another File' button
        process_another_button = tk.Button(self, text="Process Another File", command=self.process_another)
        process_another_button.pack(pady=10)
        
        # Start button at the bottom
        start_button = tk.Button(self, text="Start", command=self.start_process)
        start_button.pack(pady=10)
        
    def select_output_directory(self):
        dirname = filedialog.askdirectory(parent=self, initialdir="/", title='Please select a directory')
        if dirname:
            self.directory_var.set(dirname)

    def start_process(self):
        output_redirector = TextRedirector(self.log_text)
        sys.stdout = output_redirector
        sys.stderr = output_redirector


        # Start the processing in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.process_audio, daemon=True).start()
        
    def process_another(self):
        self.master.show_drop_screen()  

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
        transcribed_data = transcribe.transcribe(self.filepath, model_type=chosen_model_size)
        
        transcribed_text = '\n'.join([chunk['text'] for chunk in transcribed_data])  
        # Determine the output base file name without the extension
        base_output_filename = os.path.splitext(self.filename_var.get())[0]
    
        if self.save_transcription_var.get() == 1:
            transcription_path = os.path.join(self.directory_var.get(), f"{base_output_filename}_transcription.txt")
            with open(transcription_path, "w") as file:
                file.write(f"Transcription for {base_output_filename}:\n\n{transcribed_text}")
            print(f"Transcription saved to: {transcription_path}")


        matches = remove.find_profanities(transcribed_data)
        self.status_var.set(f"Found {len(matches)} profanities. Muting sections...")
        
        if len(matches) == 0:
            print(f"No Profanity was found!")
            print(f"If there was a mistake, check the transcribed output and check if the profanity your looking for is in the profanity list.")
            print(f"There are also limitations with the AI Model, its not perfect especially with smaller models. Possibly use a larger model.")
            
        else:
            timestamps = [match['timestamp'] for match in matches]
        
            if self.save_muted_timestamps_var.get() == 1:
                # Save timestamps using the correct structure
                timestamps_path = os.path.join(self.directory_var.get(), f"{base_output_filename}_muted_timestamps.txt")
                with open(timestamps_path, "w") as file:
                    file.write(f"Muted Timestamps for {base_output_filename}:\n\n")
                    for timestamp in timestamps:
                        file.write(f"{timestamp}\n")
                print(f"Muted timestamps saved to: {timestamps_path}")
            
            output_path = os.path.join(self.directory_var.get(), self.filename_var.get())
            censor.mute_sections(self.filepath, timestamps, output_path)
            self.status_var.set(f"Process complete. Processed audio saved to: {output_path}")

