import json
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Alarm
import os

YEAR = datetime.now().year

EMOJI = {
    "funding": "💰",
    "digital": "💻",
    "visual": "🖼️",
    "residency": "🏠",
    "mobility": "🌍"
}

REGION_FILES = {
    "SI": "output/01_slovenija.ics",
    "EU": "output/02_eu.ics",
    "GLOBAL": "output/03_global.ics"
}

def create_alarm(days):
    alarm = Alarm()
    alarm.add("action", "DISPLAY")
    alarm.add("trigger", timedelta(days=-days))
    alarm.add("description", f"Deadline čez {days} dni")
    return alarm

def build():
    os.makedirs("output", exist_ok=True)

    with open("data/opencalls.json") as f:
        data = json.load(f)

    calendars = {k: Calendar() for k in REGION_FILES}

    for item in data:
        real_deadline = datetime(YEAR, item["month"], item["day"])
        notify_date = real_deadline - timedelta(days=14)

        emojis = "".join([EMOJI.get(tag, "") for tag in item["tags"]])
        summary = f"🔴 {emojis} {item['name']}"

        event = Event()
        event.add("summary", summary)
        event.add("dtstart", notify_date)
        event.add("dtend", notify_date + timedelta(days=1))
        event.add("url", item["url"])

        event.add("description", f"Deadline: {real_deadline}\nApply: {item['url']}")

        for d in [30,14,7,1]:
            event.add_component(create_alarm(d))

        calendars[item["region"]].add_component(event)

    for region, cal in calendars.items():
        with open(REGION_FILES[region], "wb") as f:
            f.write(cal.to_ical())

if __name__ == "__main__":
    build()
