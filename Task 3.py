import tkinter as tk
from tkinter import ttk
import pyttsx3

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech Converter")

        self.engine = pyttsx3.init()

        
        self.text_to_speak = tk.StringVar()
        self.selected_language = tk.StringVar()

        
        self.create_widgets()

    def create_widgets(self):
        
        ttk.Label(self.root, text="Enter text:").grid(row=0, column=0, padx=5, pady=5)
        self.text_entry = ttk.Entry(self.root, textvariable=self.text_to_speak, width=40)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5)

       
        ttk.Label(self.root, text="Select Language:").grid(row=1, column=0, padx=5, pady=5)
        self.language_combobox = ttk.Combobox(self.root, textvariable=self.selected_language, 
                                               values=["en", "fr", "de", "es"])  
        self.language_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.language_combobox.current(0)  

        
        self.volume_label = ttk.Label(self.root, text="Volume:")
        self.volume_label.grid(row=2, column=0, padx=5, pady=5)
        self.volume_scale = ttk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL, command=self.update_volume)
        self.volume_scale.grid(row=2, column=1, padx=5, pady=5)
        self.volume_scale.set(1)  
        self.update_volume()

        
        self.speak_button = ttk.Button(self.root, text="Speak", command=self.speak_text)
        self.speak_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def speak_text(self):
        text = self.text_to_speak.get()
        lang = self.selected_language.get()
        self.engine.setProperty('voice', f'{lang}')
        self.engine.say(text)
        self.engine.runAndWait()

    def update_volume(self, event=None):
        volume = float(self.volume_scale.get())
        self.engine.setProperty('volume', volume)

def main():
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
