import json
import os
import datetime
import pytz
import asyncio
from telegram import Bot

# ========== FORCE TEST CONFIG ==========
FORCE_TEST = False
FORCE_DAY = "Wednesday"   # Any weekday
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

next_class = None
min_diff = float("inf")

for p in timetable[today]:
    class_time = datetime.datetime.strptime(p["start"], "%H:%M").time()
    class_dt = IST.localize(
        datetime.datetime.combine(now.date(), class_time)
    )

    diff_minutes = (class_dt - now).total_seconds() / 60

    print(f"[DEBUG] {p['subject']} starts in {diff_minutes:.2f} minutes")

    if diff_minutes >= 0 and diff_minutes < min_diff:
        min_diff = diff_minutes
        next_class = p

async def send():
    if not next_class:
        print("No upcoming class")
        return

    if FORCE_TEST:
        prefix = f"🧪 FORCE TEST\n📅 Acting as: {today}\n\n"
    else:
        prefix = ""

    if FORCE_TEST or 0 <= min_diff <= 10:
        msg = (
            prefix
            + f"📚 {next_class['subject']}\n"
            + f"⏰ {next_class['start']} - {next_class['end']}\n"
            + f"📍 {next_class['block']} | {next_class['room']}"
        )

        await bot.send_message(chat_id=CHAT_ID, text=msg)
        print("Message sent")
    else:
        print("Next class not in alert window")

asyncio.run(send())

print("=== BOT FINISHED ===")
