import os
import requests
import psutil
import asyncio
import nest_asyncio

# Pastikan sudah login dulu ke OpenRouter untuk dapat API Key
#############################################################
#############################################################

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()

TELEGRAM_TOKEN = "" # Ganti pake BOT token telegram masing-masing
OPENROUTER_API_KEY = "" # Ganti pake API Key OpenRouter masing-masing
YOUR_CHAT_ID = 1362211295  # Ganti pake Chat ID telegram masing-masing 

async def ask_gpt(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        data = response.json()

        if "choices" not in data:
            return f"[Gagal akses AI] Response: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"[Gagal akses AI] {e}"

# Untuk akses command /ask
async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Contoh: /ask kenapa server saya sering disconnect")
        return
    await update.message.reply_text("🧠 Tunggu, AI sedang menganalisis...")
    response = await ask_gpt(prompt)
    await update.message.reply_text(f" Analisis AI :\n{response}")

# Untuk akses command /log
async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log = os.popen("tail -n 20 /var/log/syslog").read()
    await update.message.reply_text(f"📜 Log Terbaru:\n\n{log}")

# Untuk akses command /resource
async def resource_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    await update.message.reply_text(
        f"💻 Penggunaan Resource:\nCPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%"
    )

# Untuk akses command /fail2ban
async def fail2ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        log = os.popen("tail -n 30 /var/log/fail2ban.log").read()
        if not log.strip():
            await update.message.reply_text("⚠️ Log fail2ban kosong.")
            return
        await update.message.reply_text(f"📜 Log Fail2ban:\n\n{log}")
        response = await ask_gpt(f"Berikut isi log fail2ban:\n{log}\n\nApa yang sedang terjadi?")
        await update.message.reply_text(f"📦 AI Analisis:\n{response}")
    except Exception as e:
        await update.message.reply_text(f"[Gagal analisis fail2ban]: {e}")

# Untuk monitoring CPU dan muncul alert apabila CPU Usage >90%
async def monitor_cpu(application):
    while True:
        cpu = psutil.cpu_percent()
        if cpu > 90:
            msg = f"🚨 ALERT: CPU Usage > 90% ({cpu}%)"
            try:
                await application.bot.send_message(chat_id=YOUR_CHAT_ID, text=msg)
                ai_analysis = await ask_gpt("Server saya CPU usage >90%. Kira-kira penyebab dan solusinya?")
                await application.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"📦 AI Analisis:\n{ai_analysis}")
            except Exception as e:
                await application.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"Gagal kirim alert: {e}")
        await asyncio.sleep(30)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("log", log_command))
    app.add_handler(CommandHandler("resource", resource_command))
    app.add_handler(CommandHandler("fail2ban", fail2ban_command))

    asyncio.create_task(monitor_cpu(app))

    print("✅ Bot AI Assistant aktif...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
