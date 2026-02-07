from telegram import Bot
import os
import datetime
import pytz

print("=== BOT STARTED ===")

# 🔧 Force trigger switch (TURN OFF AFTER TESTING)
FORCE_TRIGGER = True

# Secrets
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

print("BOT_TOKEN present:", bool(BOT_TOKEN))
print("CHAT_ID present:", bool(CHAT_ID))
print("CHAT_ID value:", CHAT_ID)

if not BOT_TOKEN or not CHAT_ID:
    print("Missing secrets, exiting.")
    exit(1)

# Init bot
bot = Bot(token=BOT_TOKEN)
print("Bot initialized")

# Time info
IST = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(IST)

print("Current IST time:", now)
print("FORCE_TRIGGER:", FORCE_TRIGGER)

try:
    if FORCE_TRIGGER:
        print("Force trigger enabled → sending message")
        bot.send_message(
            chat_id=CHAT_ID,
            text="🧪 FORCE TEST: Telegram bot is working"
        )
    else:
        print("Force trigger disabled → normal flow (not implemented here)")
except Exception as e:
    print("ERROR while sending message:")
    print(e)

print("=== BOT FINISHED ===")
