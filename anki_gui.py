import tkinter as tk
from tkinter import messagebox

import anki_generator

def submit_to_anki():
    kanji = entry_kanji.get()
    reading = entry_reading.get()
    meaning = entry_meaning.get()
    sentence = entry_sentence.get()
    translation = entry_translation.get()

    result = anki_generator.create_anki_card(kanji, reading, meaning, sentence, sentence_trans=translation)

    if result.get("error") is None:
        label_last_card_val.config(text=f"Last added: {kanji}")

        for e in [entry_kanji, entry_reading, entry_meaning, entry_sentence, entry_translation]:
            e.delete(0, tk.END)
        
        entry_kanji.focus()
    
    else:
        messagebox.showerror("ERROR", f"Anki error: {result['error']}")

def auto_fill_reading(event):
    word = entry_kanji.get()
    if word:
        suggested = anki_generator.get_jisho_reading(word)
        entry_reading.delete(0, tk.END)
        entry_reading.insert(0, suggested)

root = tk.Tk()
root.title("JP Miner GUI")
root.geometry("400x520")
root.configure(bg="#1e1e1e")

label_cfg = {"bg": "#1e1e1e", "fg": "#f0f0f0", "font": ("Arial", 10)}
entry_cfg = {"bg": "#2c313a", "fg": "white", "insertbackground": "white", "relief": "flat"}

tk.Label(root, text="Kanji", **label_cfg).pack(pady=(10,0))
entry_kanji = tk.Entry(root, **entry_cfg, width=35)
entry_kanji.pack(pady=5)
entry_kanji.bind("<FocusOut>", auto_fill_reading)

tk.Label(root, text="Reading", **label_cfg).pack()
entry_reading = tk.Entry(root, **entry_cfg, width=35)
entry_reading.pack(pady=5)

tk.Label(root, text="Meaning", **label_cfg).pack()
entry_meaning = tk.Entry(root, **entry_cfg, width=35)
entry_meaning.pack(pady=5)

tk.Label(root, text="Sentence (japanese)", **label_cfg).pack()
entry_sentence = tk.Entry(root, **entry_cfg, width=35)
entry_sentence.pack(pady=5)

tk.Label(root, text="Sentence translation", **label_cfg).pack()
entry_translation = tk.Entry(root, **entry_cfg, width=35)
entry_translation.pack(pady=5)

btn = tk.Button(root, text="Create card", command=submit_to_anki, bg="#61afef", fg="#1e1e1e", font=("Arial", 10, "bold"))
btn.pack(pady=20)

tk.Frame(root, height=1, width=300, bg="#3e4451").pack(pady=10)
label_last_card_val = tk.Label(root, text="No card added", bg="#1e1e1e", fg="#abb2bf", font=("Arial", 9, "italic"))
label_last_card_val.pack()

root.mainloop()