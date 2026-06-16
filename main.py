import tkinter as tk
from tkinter import scrolledtext, Frame
from AAC_Translator import translate

root = tk.Tk()
root.title("OpenAAC")
root.geometry("800x600")

label_input = tk.Label(root, text="Write here:", font=("Arial", 12))
label_input.pack(pady=5)

text_input = scrolledtext.ScrolledText(root, height=5, font=("Arial", 12))
text_input.pack(padx=10, pady=5, fill=tk.X)

def translate_on_click():
    text = text_input.get("1.0", tk.END).strip()
    if text:
        translate(text, frame_output)

button_translate = tk.Button(root, text="Translate to AAC", command=translate_on_click, font=("Arial", 12), bg="lightblue")
button_translate.pack(pady=10)

frame_output = Frame(root)
frame_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()