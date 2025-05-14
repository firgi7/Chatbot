import os
import subprocess

def find_espeak():
    possible_paths = [
        r"C:\Program Files\eSpeak\command_line\espeak.exe",
        r"C:\Program Files (x86)\eSpeak\command_line\espeak.exe"
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    return None

def speak(text):
    espeak_path = find_espeak()
    if espeak_path:
        subprocess.call([espeak_path, text])
    else:
        print("❌ eSpeak tidak ditemukan. Pastikan sudah terinstal dan arahkan ke lokasi yang benar.")

# Tes
speak("Tes suara berhasil")
