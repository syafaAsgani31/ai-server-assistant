# AI ChatBot Assistant untuk Admin Server via Telegram Menggunakan OpenRouter AI

Bot Telegram ini memudahkan server admin untuk:
- 🔍 Mengecek log
- 📊 Menampilkan resource usage (CPU, RAM, Disk)
- 🔒 Menganalisis serangan via Fail2Ban
- 💬 Konsultasi otomatis dengan AI via OpenRouter API

## Fitur :

| Perintah     | Fungsi                                                             |
|--------------|------------------------------------------------------------------  |
| `/ask` pertanyaan      | Konsultasi ke AI                                         |
| `/log`       | Menampilkan syslog terbaru                                         |
| `/resource`  | Tampilkan CPU, RAM, Disk                                           |
| `/fail2ban`  | Analisis log Fail2Ban + AI                                         |
| 🔔 Otomatis  | Alert CPU > 90% + AI bantu deteksi penyebab                        


## 🛠️ Instalasi

# 1. Clone repository :
git clone https://github.com/USERNAME/ai-assistant-server.git
cd ai-assistant-server

# 2. Install dependency :
pip install -r requirements.txt

# 3. Edit ai_assistant_bot.py
Isi token bot dan Chat ID Telegram dan API key OpenRouter

# 4. Run :
python3 ai_assistant_bot.py


