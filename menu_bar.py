import tkinter as tk
from idlelib.outwin import file_line_pats
from tkinter import Menu, messagebox, filedialog

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
    menu_bar.add_cascade(label="Change", menu=edit_menu)

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