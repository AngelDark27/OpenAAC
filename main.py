import tkinter as tk
from tkinter import scrolledtext, Frame
from AAC_Translator import translate
from spinner import Spinner
import threading

root = tk.Tk()
root.title("OpenAAC")
root.geometry("800x600")

label_input = tk.Label(root, text="Write here:", font=("Arial", 12))
label_input.pack(pady=5)

text_input = scrolledtext.ScrolledText(root, height=5, font=("Arial", 12))
text_input.pack(padx=10, pady=5, fill=tk.X)

spinner = Spinner(root, text="Translating", size=16)

frame_output = Frame(root)
frame_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def translate_thread(text):
    try:
        translate(text, frame_output)
    except Exception as e:
        print(f"Error during the translation: {e}")
    finally:
        root.after(0, spinner.stop)

def translate_on_click():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        return

    for widget in frame_output.winfo_children():
        widget.destroy()

    spinner.start()

    thread = threading.Thread(target=translate_thread, args=(text,))
    thread.deamon = True
    thread.start()

button_translate = tk.Button(root, text="Translate to AAC", command=translate_on_click, font=("Arial", 12), bg="lightblue")
button_translate.pack(pady=10)



root.mainloop()