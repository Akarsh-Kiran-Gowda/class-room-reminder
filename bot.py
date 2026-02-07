import json
import os
import datetime
import pytz
from telegram import Bot

# ========== FORCE TEST CONFIG ==========
FORCE_TEST = True
FORCE_DAY = "Wednesday"   # Change to any weekday
# ======================================

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=BOT_TOKEN)

IST = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(IST)

real_today = now.strftime("%A")
today = FORCE_DAY if FORCE_TEST else real_today

print("=== BOT STARTED ===")
print("Real day:", real_today)
print("Effective day:", today)
print("Current IST time:", now.strftime("%Y-%m-%d %H:%M"))

with open("timetable.json") as f:
    timetable = json.load(f)

if today not in timetable:
    print("No classes for", today)
    exit()

for p in timetable[today]:
    class_time = datetime.datetime.strptime(p["start"], "%H:%M").time()
    class_dt = IST.localize(
        datetime.datetime.combine(now.date(), class_time)
    )

    diff_minutes = (class_dt - now).total_seconds() / 60

    print(
        f"[DEBUG] {p['subject']} starts in "
        f"{diff_minutes:.2f} minutes"
    )

    # ⏰ alert window
    if 0 <= diff_minutes <= 10 or FORCE_TEST:
        msg = (
            f"🧪 FORCE TEST\n"
            f"📅 Acting as: {today}\n\n"
            f"📚 {p['subject']}\n"
            f"⏰ {p['start']} - {p['end']}\n"
            f"📍 {p['block']} | {p['room']}"
        )
        bot.send_message(chat_id=CHAT_ID, text=msg)

print("=== BOT FINISHED ===")
