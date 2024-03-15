import tkinter as tk
from tkinter import ttk, font, messagebox
import requests
import openai
import multiprocessing
from playsound import playsound
import os
import time

class QuranReaderApp(tk.Tk):
    def setup_action_buttons(self):
        # Frame for action buttons
        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)

        # Highlight button
        highlight_button = tk.Button(action_frame, text="Highlight", command=self.highlight_selected_text,
                                     font=self.headingFont)
        highlight_button.pack(side=tk.LEFT, padx=10)

        # Simplify button
        simplify_button = tk.Button(action_frame, text="Simplify", command=self.simplify_selected_text,
                                    font=self.headingFont)
        simplify_button.pack(side=tk.LEFT, padx=10)

        # Undo Highlight button
        undo_highlight_button = tk.Button(action_frame, text="Remove Highlights", command=self.undo_highlight,
                                          font=self.headingFont)
        undo_highlight_button.pack(side=tk.LEFT, padx=10)

        # Play Audio button
        play_audio_button = tk.Button(action_frame, text="Play Audio", command=self.play_audio,
                                          font=self.headingFont)
        play_audio_button.pack(side=tk.LEFT, padx=10)

        #music button
        music_button = tk.Button(action_frame, text="Play Music", command=self.play_music,
                                            font=self.headingFont)
        music_button.pack(side=tk.LEFT, padx=10)

        #stop music button
        stop_music_button = tk.Button(action_frame, text="Stop Music", command=self.stop_music ,
                                            font=self.headingFont)
        stop_music_button.pack(side=tk.LEFT, padx=10)

        # Stop Audio button
        stop_audio_button = tk.Button(action_frame, text="Stop Audio", command=self.stop_audio,
                                            font=self.headingFont)
        stop_audio_button.pack(side=tk.LEFT, padx=10)


    def play_music(self):
        self.playmusic = multiprocessing.Process(target=playsound, args=("islamsong.mp3",))
        self.playmusic.start()
        return "amogus"

    def stop_music(self):
        self.playmusic.terminate()
        return "amogus"

    def highlight_selected_text(self):
        """Highlight selected text."""
        try:
            self.verse_text.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)
            self.verse_text.tag_configure("highlight", background="yellow")
        except tk.TclError:
            print("No text selected for highlighting.")  # Replace with your choice of notification

    def undo_highlight(self):
        """Undo the most recent highlight."""
        self.verse_text.tag_remove("highlight", "1.0", tk.END)

    def play_audio(self):
        try:
            selected_text = self.verse_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.get_audio(selected_text, self.voice_dropdown.get().lower())
        except tk.TclError:
            messagebox.showerror("Error", "No text selected for audio.")

    def is_api_key_valid(self):
        client = openai.OpenAI(
            api_key=self.api_key_entry.get(),
        )
        try:
            response = client.completions.create(
                model="davinci-002",
                prompt="This is a test.",
                max_tokens=5
            )
        except:
            return False
        else:
            return True


    def get_audio(self, text, selected_voice):
        if len(self.api_key_entry.get()) == 0:
            messagebox.showerror("Error", "Please enter your OpenAI API Key.")
            return
        if not self.is_api_key_valid():
            messagebox.showerror("Error", "Invalid API Key.")
            return

        if os.path.isfile("output.mp3"):
            os.remove("output.mp3") #clears the file
        else:
            pass

        if text.__len__() > 4000:
            messagebox.showerror("Error", "Text Too Long")
            return
        client = openai.OpenAI(
            api_key=self.api_key_entry.get(),
        )
        response = client.audio.speech.create(
            model="tts-1",
            voice=selected_voice,
            input=text,
        )
        response.stream_to_file("output.mp3")
        while not os.path.exists("output.mp3"):
            time.sleep(1)
        if os.path.isfile("output.mp3"):
            self.playaudio = multiprocessing.Process(target=playsound, args=("output.mp3",))
            self.playaudio.start()

        return "amogus"

    def stop_audio(self):
        self.playaudio.terminate()
        os.remove("output.mp3")
        return "amogus"

    def simplify_selected_text(self):
        try:
            selected_text = self.verse_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            simplified_text = self.get_simplified_text(selected_text)

            # Create a new Toplevel window
            simplified_text_window = tk.Toplevel(self)
            simplified_text_window.title("Simplified Text")
            simplified_text_window.geometry("400x200")  # Adjust size as needed

            # Add a Text widget to display the simplified text
            simplified_text_display = tk.Text(simplified_text_window, wrap=tk.WORD, font=self.textFont)
            simplified_text_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            simplified_text_display.insert(tk.END, simplified_text)

            # Make the Text widget read-only
            simplified_text_display.configure(state=tk.DISABLED)
        except tk.TclError:
            messagebox.showerror("Error", "No text selected for simplification.")

    def get_simplified_text(self, text):
        if len(self.api_key_entry.get()) == 0:
            messagebox.showerror("Error", "Please enter your OpenAI API Key.")
            return
        if not self.is_api_key_valid():
            messagebox.showerror("Error", "Invalid API Key.")
            return
        client = openai.OpenAI(
            api_key=self.api_key_entry.get(),
        )
        res = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {
                'role': 'user',
                'content': f"Can you simplify this text in the given language? it is from the quran and sometimes it may have complex sentences: {text}"
            }
        ]
    )
        simplified_text = res.choices[0].message.content
        return simplified_text
    def __init__(self):
        super().__init__()

        self.title("Quran Reader Pro - Multi-Lingual Quran Navigator, Simplifier, Reader with Search Functionality Free")
        self.geometry("800x600")

        self.app_title = tk.Label(self, text="Quran Reader Pro",
                                  font=font.Font(family="Papyrus", size=38, weight="bold", slant="italic"),
                                  foreground="gold", anchor="w")
        self.app_title.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(10, 0))

        self.headingFont = font.Font(family="Georgia", size=14, weight="bold")
        self.textFont = font.Font(family="Georgia", size=12)




        settings_frame = tk.Frame(self)
        settings_frame.pack(pady=20)

        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, font=self.textFont, width=30)
        self.search_entry.grid(row=0, column=0, padx=(10, 5))
        self.search_entry.bind("<Return>", self.search_verses)

        search_button = tk.Button(search_frame, text="Search", command=self.search_verses, font=self.headingFont)
        search_button.grid(row=0, column=1, padx=5)
        self.setup_action_buttons()
        # openai api key input
        self.api_key_label = tk.Label(settings_frame, text="OpenAI API Key:", font=self.headingFont)
        self.api_key_entry = tk.Entry(settings_frame, font=self.textFont, width=10)
        self.api_key_label.grid(row=1, column=3, padx=10)
        self.api_key_entry.grid(row=1, column=4, padx=10)


        self.language_label = tk.Label(settings_frame, text="Language:", font=self.headingFont)
        self.language_label.grid(row=0, column=0, padx=10)

        self.languages = {'English': 'en.asad', 'Turkish': 'tr.yildirim', 'Chinese': 'zh.jian', 'German': 'de.aymanswoaid', 'Arabic': 'ar.alafasy'}
        self.language_var = tk.StringVar(value='Arabic')
        self.language_dropdown = ttk.Combobox(settings_frame, textvariable=self.language_var,
                                              values=list(self.languages.keys()), width=10, font=self.headingFont)
        self.language_dropdown.grid(row=0, column=1, padx=10)
        self.language_dropdown.bind("<<ComboboxSelected>>", self.load_surah)

        self.voices = {'Onyx': 'onyx', 'Alloy': 'alloy', 'Fable': 'fable', 'Echo': 'echo', 'Nova': 'nova', 'Shimmer': 'shimmer'}
        self.voice_var = tk.StringVar(value='Onyx')
        self.voice_dropdown = ttk.Combobox(settings_frame, textvariable=self.voice_var,
                                                values=list(self.voices.keys()), width=10, font=self.headingFont)
        self.voice_dropdown.grid(row=0, column=4, padx=10)

        self.surah_label = tk.Label(settings_frame, text="Surah:", font=self.headingFont)
        self.surah_label.grid(row=0, column=2, padx=10)

        self.surah_var = tk.StringVar(value="1")
        self.surah_dropdown = ttk.Combobox(settings_frame, textvariable=self.surah_var,
                                           values=[str(i) for i in range(1, 115)], width=10, font=self.headingFont)
        self.surah_dropdown.grid(row=0, column=3, padx=10)
        self.surah_dropdown.bind("<<ComboboxSelected>>", self.load_surah)

        prev_button = tk.Button(settings_frame, text="Previous", command=self.prev_surah, font=self.headingFont)
        prev_button.grid(row=1, column=1, padx=10, pady=10)

        next_button = tk.Button(settings_frame, text="Next", command=self.next_surah, font=self.headingFont)
        next_button.grid(row=1, column=2, padx=10, pady=10)

        self.text_frame = tk.Frame(self)
        self.text_frame.pack(expand=True, fill="both")

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.verse_text = tk.Text(self.text_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set,
                                  state=tk.DISABLED, font=self.textFont, relief=tk.FLAT, borderwidth=0)
        self.verse_text.pack(expand=True, fill="both", side=tk.LEFT)
        self.scrollbar.config(command=self.verse_text.yview)

        self.load_surah(None)


    def search_verses(self, event=None):
        search_term = self.search_entry.get().lower().strip()
        if not search_term:
            self.load_surah(None)
            return
        all_verses = self.get_translation(self.surah_var.get())
        if all_verses:
            search_results = [verse for verse in all_verses if search_term in verse['text'].lower()]
            self.display_verses(search_results)

    def get_translation(self, surah_number):
        lang_code = self.languages[self.language_var.get()]
        url = f"http://api.alquran.cloud/v1/surah/{surah_number}/{lang_code}"

        response = requests.get(url)
        if response.status_code == 200 and 'data' in response.json():
            verses = response.json().get('data').get('ayahs')
            return verses
        else:
            return None

    def display_verses(self, verses):
        self.verse_text.configure(state=tk.NORMAL)
        self.verse_text.delete(1.0, tk.END)
        for verse in verses:
            self.verse_text.insert(tk.END, f"{verse.get('text')} ({verse.get('numberInSurah')})\n\n")
        self.verse_text.configure(state=tk.DISABLED)

    def load_surah(self, event):
        surah_number = self.surah_var.get()
        verses = self.get_translation(surah_number)
        if verses:
            self.display_verses(verses)

    def prev_surah(self):
        current_surah = int(self.surah_var.get())
        if current_surah > 1:
            self.surah_var.set(str(current_surah - 1))
            self.load_surah(None)

    def next_surah(self):
        current_surah = int(self.surah_var.get())
        if current_surah < 114:
            self.surah_var.set(str(current_surah + 1))
            self.load_surah(None)


if __name__ == "__main__":
    app = QuranReaderApp()
    app.mainloop()