import aiml
import os
import subprocess

# Hapus file brain untuk load ulang AIML saat debug
if os.path.isfile("standard.brn"):
    print("Menghapus brain file lama...")
    os.remove("standard.brn")

# Inisialisasi bot
bot = aiml.Kernel()

# Load file .AIML
print("Memuat file AIML...")
bot.bootstrap(learnFiles="tes.aiml", commands="LOAD AIML B")
bot.saveBrain("standard.brn")
print("AIML berhasil dimuat.")

# Fungsi untuk mencari espeak.exe secara otomatis
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
        try:
            subprocess.call([espeak_path, text])
        except Exception as e:
            print(f"[Peringatan] Terjadi kesalahan saat menjalankan espeak: {e}")
    else:
        print("[Peringatan] espeak.exe tidak ditemukan. Tidak dapat menggunakan TTS.")

# Loop percakapan
print('Ketik "exit" untuk keluar.')
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Keluar dari percakapan...")
        break
    response = bot.respond(user_input)
    print("Bot:", response)
    speak(response)
