import json
import datetime
import pytz
from telegram import Bot
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

FORCE_TEST = True  # set False after testing

bot = Bot(token=BOT_TOKEN)
IST = pytz.timezone("Asia/Kolkata")

now = datetime.datetime.now(IST)
# today = now.strftime("%A")
# current_time = now.strftime("%H:%M")

today = "Wednesday" if FORCE_TEST else now.strftime("%A")


with open("timetable.json") as f:
    timetable = json.load(f)

if today in timetable:
    for p in timetable[today]:
        class_time = datetime.datetime.strptime(p["start"], "%H:%M").time()
        class_dt = IST.localize(datetime.datetime.combine(now.date(), class_time))

        diff = (class_dt - now).total_seconds() / 60

        if 4 <= diff <= 5:
            msg = (
                f"📚 {p['subject']}\n"
                f"⏰ {p['start']} - {p['end']}\n"
                f"📍 {p['block']} | {p['room']}"
            )
            bot.send_message(chat_id=CHAT_ID, text=msg)
