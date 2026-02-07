import json
import os
import asyncio
import datetime
import pytz
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

IST = pytz.timezone("Asia/Kolkata")
bot = Bot(token=BOT_TOKEN)

LAST_SENT_FILE = "last_sent.json"


def load_last_sent():
    if not os.path.exists(LAST_SENT_FILE):
        return {}
    with open(LAST_SENT_FILE, "r") as f:
        return json.load(f)


def save_last_sent(data):
    with open(LAST_SENT_FILE, "w") as f:
        json.dump(data, f)


def get_next_class(timetable, now):
    today = now.strftime("%A")
    if today not in timetable:
        return None

    upcoming = []

    for cls in timetable[today]:
        start_time = datetime.datetime.strptime(cls["start"], "%H:%M").time()
        class_dt = IST.localize(
            datetime.datetime.combine(now.date(), start_time)
        )

        diff = (class_dt - now).total_seconds() / 60
        if diff >= 0:
            upcoming.append((diff, cls))

    if not upcoming:
        return None

    upcoming.sort(key=lambda x: x[0])
    return upcoming[0]   # nearest class


async def main():
    print("=== BOT RUNNING (EC2 MODE) ===")

    with open("timetable.json") as f:
        timetable = json.load(f)

    while True:
        now = datetime.datetime.now(IST)
        next_class = get_next_class(timetable, now)

        if next_class:
            diff, cls = next_class
            print(f"[DEBUG] Next class {cls['subject']} in {diff:.2f} mins")

            if diff <= 5:
                last_sent = load_last_sent()
                key = f"{now.strftime('%A')}_{cls['subject']}_{cls['start']}"

                if last_sent.get("key") != key:
                    msg = (
                        f"📚 {cls['subject']}\n"
                        f"⏰ {cls['start']} - {cls['end']}\n"
                        f"📍 {cls['block']} | {cls['room']}\n\n"
                        f"🚨 Class starts in {int(diff)} minutes!"
                    )

                    await bot.send_message(chat_id=CHAT_ID, text=msg)
                    save_last_sent({"key": key})
                    print("✅ Message sent")
                else:
                    print("⏭ Duplicate prevented")

        await asyncio.sleep(60)   # check every 1 minute


if __name__ == "__main__":
    asyncio.run(main())
