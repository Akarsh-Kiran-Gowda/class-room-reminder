from telegram import Bot
import os
import datetime
import pytz

print("=== BOT STARTED ===")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

print("BOT_TOKEN present:", bool(BOT_TOKEN))
print("CHAT_ID present:", bool(CHAT_ID))

bot = Bot(token=BOT_TOKEN)

IST = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(IST)
print("Current IST time:", now)

print("Sending test message...")
bot.send_message(
    chat_id=CHAT_ID,
    text="✅ Sync test message — bot is working"
)

print("Message sent")
print("=== BOT FINISHED ===")
