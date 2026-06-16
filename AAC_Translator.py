import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext

def search(word):
    url = f"https://api.arasaac.org/api/pictograms/it/search/{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data:
            id_img = data[0].get('_id')
            if id_img:
                url_img = f"https://static.arasaac.org/pictograms/{id_img}/{id_img}_500.png"
                img_response = requests.get(url_img)
                img_response.raise_for_status()
                img = Image.open(BytesIO(img_response.content))
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                return img
    except requests.exceptions.RequestException as e:
        print(f"Error in searching '{word}': {e}")
    return None

def translate(text, frame_container):
    for widget in frame_container.winfo_children():
        widget.destroy()

    words = text.split()
    for word in words:
        img_pil = search(word)
        if img_pil:
            img_tk = ImageTk.PhotoImage(img_pil)
            label_img = tk.Label(frame_container, image=img_tk)
            label_img.image = img_tk
            label_img.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            label_text = tk.Label(frame_container, text=word, font=("Arial", 14))
            label_text.pack(side=tk.LEFT, padx=5, pady=5)