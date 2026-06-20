from http.client import responses

import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import json
import os
import threading

DICTIONARY_FILE = "dictionary.json"
_dict = {}
_dict_lock = threading.Lock()

def load_dicrionary():
    global _dict
    if os.path.exists(DICTIONARY_FILE):
        try:
            with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
                _dict = json.load(f)
            print(f"Dictionary loaded: {len(_dict)} words.")
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            _dict = {}
    else:
        save_dictionary()
        print("New dictionary created")

def save_dictionary():
    with _dict_lock:
        try:
            with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
                json.dump(_dict, f, ensure_ascii=False, indent=2)
            print(f"Dictionary saved: {len(_dict)} words.")
        except Exception as e:
            print(f"Error saving dictionary: {e}")

def get_dicitonary():
    return dict(_dict)

def add_word(word, url):
    word_lower = word.lower()
    with _dict_lock:
        _dict[word_lower] = url
        save_dictionary()
    return True

def delete_word(word):
    word_lower = word.lower()
    with _dict_lock:
        if word_lower in _dict:
            del _dict[word_lower]
            save_dictionary()
            return True
    return False

def import_dictionary(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            new_dict = json.load(f)
        if not isinstance(new_dict, dict):
            raise ValueError("The file doesn't contain a valid dictionary.")
        with _dict_lock:
            _dict.clear()
            _dict.update(new_dict)
            save_dictionary()
        return True
    except Exception as e:
        print(f"Error during import: {e}")
        return False

def export_dictionary(file_path):
    try:
        with open(file_path, 'w', encodicng='utf-8') as f:
            json.dump(_dict, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error during export: {e}")
        return False

def merge_dictionary(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            external_dict = json.load(f)
        if not isinstance(external_dict, dict):
            raise ValueError("The file doesn't contain a valid dictionary.")
        added = 0
        with _dict_lock:
            for word, url in external_dict.items():
                if word not in _dict:
                    _dict[word] = url
                    added += 1
            if added > 0:
                save_dictionary()
        return added
    except Exception as e:
        print(f"Error during merging: {e}")
        return -1

def search(word):
    word_lower = word.lower()
    if word_lower in _dict:
        url = _dict[word_lower]
        if url is None:
            return None
        try:
            img_response = requests.get(url)
            img_response.raise_for_status()
            img = Image.open(BytesIO(img_response.content))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            print("Word found")
            return img
        except Exception as e:
            print(f"Error loading image: {e}")
            with _dict_lock:
                if word_lower in _dict:
                    del _dict[word_lower]
                    save_dictionary()
            return _search_arasaac(word, word_lower)
    return _search_arasaac(word, word_lower)

def _search_arasaac(word, word_lower):
    print(f"searching {word}...")
    url = f"https://api.arasaac.org/api/pictograms/it/search/{word}"
    try:
        response = responses.get(url)
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

                with _dict_lock:
                    _dict[word_lower] = url_img
                    save_dictionary()
                print(f"{word} found and added.")
                return img

        with _dict_lock:
            _dict[word_lower] = None
            save_dictionary()
        print(f"{word} not found")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
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

load_dicrionary()