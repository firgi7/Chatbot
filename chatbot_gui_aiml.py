import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
import aiml
import os
import subprocess
import threading
import math
import time
from PIL import Image, ImageTk

# === AIML Setup ===
bot = aiml.Kernel()
if os.path.isfile("standard.brn"):
    bot.loadBrain("standard.brn")
else:
    bot.bootstrap(learnFiles="tes.aiml", commands="LOAD AIML B")
    bot.saveBrain("standard.brn")

# === TTS ===
def find_espeak():
    paths = [
        r"C:\\Program Files\\eSpeak\\command_line\\espeak.exe",
        r"C:\\Program Files (x86)\\eSpeak\\command_line\\espeak.exe"
    ]
    for p in paths:
        if os.path.isfile(p):
            return p
    return None

def speak(text):
    espeak = find_espeak()
    if espeak:
        subprocess.call([espeak, text])
    else:
        print("eSpeak tidak ditemukan.")

def speak_async(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()

# === GUI Setup ===
root = tk.Tk()
root.title("JARVIS AI")
root.geometry("700x600")
root.configure(bg="#0d0d0d")

# === Canvas Hologram Topeng Iron Man ===
canvas = tk.Canvas(root, width=360, height=360, bg="#0d0d0d", highlightthickness=0)
canvas.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

# Gambar topeng Iron Man/JARVIS
try:
    image = Image.open("ironman_mask.png")  # pastikan file ada di direktori yang sama
    image = image.resize((360, 360), Image.Resampling.LANCZOS)  # Resize gambar sesuai dengan ukuran canvas
    mask_photo = ImageTk.PhotoImage(image)
    canvas.create_image(180, 180, image=mask_photo)  # Menempatkan gambar di tengah canvas
except Exception as e:
    print("Gagal memuat gambar topeng:", e)

# === Tampilan Chat ===
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED,
    bg="#1a1a1a", fg="#00ffe1", font=("Consolas", 12), insertbackground="white")
chat_window.pack(padx=10, pady=(180,10), fill=tk.BOTH, expand=True)

# === Input Frame ===
input_frame = tk.Frame(root, bg="#0d0d0d")
input_frame.pack(padx=10, pady=10, fill=tk.X)

input_field = tk.Entry(input_frame, bg="#333333", fg="#00ffcc", font=("Consolas", 12),
                       insertbackground="white")
input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
input_field.bind("<Return>", lambda event: send_message())

def send_message():
    user_input = input_field.get()
    if user_input.strip():
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, f"KAMU: {user_input}\n", "user")
        response = bot.respond(user_input)
        chat_window.insert(tk.END, f"JARVIS: {response}\n\n", "bot")
        chat_window.config(state=tk.DISABLED)
        chat_window.see(tk.END)
        speak_async(response)
        input_field.delete(0, tk.END)

send_button = tk.Button(input_frame, text="SEND", bg="#00b3b3", fg="white",
                        activebackground="#009999", command=send_message,
                        font=("Consolas", 12, "bold"))
send_button.pack(side=tk.RIGHT)

# === Tombol Voice Note ===
def listen_and_process():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "🔊 Mendengarkan...\n", "bot")
        chat_window.config(state=tk.DISABLED)
        chat_window.see(tk.END)
        try:
            audio = r.listen(source, timeout=5)
            user_input = r.recognize_google(audio, language="id-ID")
            input_field.delete(0, tk.END)
            input_field.insert(0, user_input)
            send_message()
        except sr.WaitTimeoutError:
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, "⚠ Waktu habis. Tidak ada suara.\n", "bot")
            chat_window.config(state=tk.DISABLED)
        except sr.UnknownValueError:
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, "⚠ Maaf, tidak bisa mengenali suara.\n", "bot")
            chat_window.config(state=tk.DISABLED)

voice_button = tk.Button(input_frame, text="🎤 Voice", bg="#006666", fg="white",
                         activebackground="#004c4c", command=listen_and_process,
                         font=("Consolas", 12, "bold"))
voice_button.pack(side=tk.RIGHT, padx=(10, 0))

# === Gaya Chat ===
chat_window.tag_config("user", foreground="#66ffcc")
chat_window.tag_config("bot", foreground="#00ffe1")

# === Suara Startup ===
def startup_voice():
    speak("Hello, Sir. Systems are now online.")

root.after(500, startup_voice)

# === Jalankan GUI ===
root.mainloop()
