import json
import os
from datetime import datetime, timedelta
import pytz
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

bot = Bot(token=BOT_TOKEN)
scheduler = BlockingScheduler(timezone="Asia/Kolkata")

with open("timetable.json") as f:
    timetable = json.load(f)

def send_message(text):
    bot.send_message(chat_id=CHAT_ID, text=text)

def schedule_classes():
    for day, periods in timetable.items():
        for period in periods:
            hour, minute = map(int, period["start"].split(":"))

            notify_time = datetime.now(pytz.timezone("Asia/Kolkata")).replace(
                hour=hour,
                minute=minute,
                second=0,
                microsecond=0
            ) - timedelta(minutes=5)

            scheduler.add_job(
                send_message,
                "cron",
                day_of_week=day.lower()[:3],
                hour=notify_time.hour,
                minute=notify_time.minute,
                args=[f"""
📚 {period['subject']}
⏰ {period['start']} - {period['end']}
📍 {period['block']} | {period['room']}
"""]
            )

schedule_classes()
scheduler.start()
