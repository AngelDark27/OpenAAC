import tkinter as tk
from tkinter import Menu, messagebox, filedialog, simpledialog
from AAC_Translator import (get_dicitonary, add_word, delete_word, import_dictionary, export_dictionary, merge_dictionary)

def menu(root, text_widget, output_frame, translate_callback):
    def new_file():
        text_widget.delete("1.0",tk.END)
        for widget in output_frame.winfo_children():
            widget.destroy()

    def open_file():
        file_path = filedialog.askopenfilename(title="Open text file", filetypes=[("Text file", "*.txt"), ("All files", "*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    text_widget.delete("1.0", tk.END)
                    text_widget.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"The file can't be opened:\n{e}")

    def save_file():
        content = text_widget.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("No text", "The text box is empty")
            return
        file_path = filedialog.asksaveasfilename(title="Save text file", defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Saved", "File saved properly")
            except Exception as e:
                messagebox.showerror("Error", f"The file can't be saved:\n{e}")

    def show_dictionary():
        d = get_dicitonary()
        if not d:
            messagebox.showinfo("Dictionary", "Dictionary empty")
            return

        text = ""
        for word, url in sorted(d.items()):
            if url is None:
                status = "Not found"
            else:
                staus = url[:50] + "..." if len(url) > 50 else url
            text += f"{word}: {status}\n"

        dialog = tk.Toplevel(root)
        dialog.title("Dictionary Content")
        dialog.geometry("600x400")

        label = tk.Label(dialog, text="Word in the dictionary:", font=("Arial", 12))
        label.pack(pady=5)

        text_area = tk.Text(dialog, wrap=tk.WORD, font=("Courier", 10))
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert("1.0", text)
        text_area.config(state=tk.DISABLED)

        btn_close = tk.Button(dialog, text="Close", command=dialog.destroy)
        btn_close.pack(pady=5)

    def add_word_dialog():
        word = simpledialog.askstring("Add/Change Word", "Enter word:")
        if not word:
            return
        word_lower = word.lower()

        d = get_dicitonary()
        current_url = d.get(word_lower, "")
        url = simpledialog.askstring("Add/Change Word", "Enter URL:", initialvalue=current_url if current_url else"")
        if url is None:
            return
        if url.strip() == "":
            url = None

        if add_word(word_lower, url):
            messagebox.showinfo("Success", "Word added/modified")
        else:
            messagebox.showerror("Error", "The word can't be added/changed")

    def delete_word_dialog():
        word = simpledialog.askstring("Delete word", "Enter word:")
        if not word:
            return
        if delete_word(word.lower()):
            messagebox.showinfo("Success", "Word deleted")
        else:
            messagebox.showerror("Error", "Word not found")

    def import_dictionary_dialog():
        file_path = filedialog.askopenfilename(title="Import Dictionary", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not file_path:
            return

        if not messagebox.askyesno("Confirm Import", "You're going to delete the current dictionary to use another\n Continue?"):
            return

        if import_dictionary(file_path):
            messagebox.showinfo("Success", "Dictionary imported")
        else:
            messagebox.showerror("Error", "Dictionary not imported")

    def export_dictionary_dialog():
        file_path = filedialog.asksaveasfilename(title="Export Dictionary", defaultextension=".json", filetypes=[("JSON file", "*.json"), ("All files", "*.*")])
        if not file_path:
            return
        if export_dictionary(file_path):
            messagebox.showinfo("Success", "Dictionary exported")
        else:
            messagebox.showerror("Error", "Dictionary not exported")

    def merge_dictionary_dialog():
        file_path = filedialog.askopenfilename(title="Merge Dictionary", filetypes=[("JSON file", "*.json"), ("All file", "*.*")])
        if not file_path:
            return
        added = merge_dictionary(file_path)
        if added < 0:
            messagebox.showerror("Error", "Error merging the dictionaries")
        elif added == 0:
            messagebox.showinfo("Merge", "No word added")
        else:
            messagebox.showinfo("Merge", f"{added} word(s) added")

    def about():
        messagebox.showinfo("Informations about OpenAAC","OpenACC - ACC open source translator\n\nVersion 1.0\nDeveloped with Python and Tkinter\nPittograms: ARASAAC (CC BY-NC-SA)")

    def commands():
        messagebox.showinfo("Commands", "File\nNew: Ctrl+N\nOpen: Ctrl+O\nSave: Ctrl+S\nExit: Ctrl+Q\n\n\nText\nTranslate: Ctrl+T\nCopy: Ctrl+C\nPaste: Ctrl+V\nCut: Ctrl+X")

    def clear_all():
        text_widget.delete("1.0", tk.END)
        for widget in output_frame.winfo_children():
            widget.destroy()


    menu_bar = Menu(root)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Cut", command=lambda: root.focus_get().event_generate("<<Cut>>"))
    edit_menu.add_command(label="Copy", command=lambda: root.focus_get().event_generate("<<Copy>>"))
    edit_menu.add_command(label="Paste", command=lambda: root.focus_get().event_generate("<<Paste>>"))
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    dict_menu = Menu(menu_bar, tearoff=0)
    dict_menu.add_command(label="Show", command=show_dictionary)
    dict_menu.add_separator()
    dict_menu.add_command(label="Add/Change", command=add_word_dialog)
    dict_menu.add_command(label="Delete", command=delete_word_dialog)
    dict_menu.add_separator()
    dict_menu.add_command(label="Import", command=import_dictionary_dialog)
    dict_menu.add_command(label="Export", command=export_dictionary_dialog)
    dict_menu.add_command(label="Merge", command=merge_dictionary_dialog)
    menu_bar.add_cascade(label="Dictionary", menu=dict_menu)


    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Informations", command=about)
    help_menu.add_command(label="Commands", command=commands)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

    root.bind("<Control-n>", lambda e: new_file())
    root.bind("<Control-o>", lambda e: open_file())
    root.bind("<Control-s>", lambda e: save_file())
    root.bind("<Control-q>", lambda e: root.quit())

    return menu_bar