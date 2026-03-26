
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
    alarm.add("description", f"Deadline čez {days} dni")
    alarm.add("trigger", timedelta(days=-days))
    return alarm


def build():
    os.makedirs("output", exist_ok=True)

    with open("data/opencalls.json", encoding="utf-8") as f:
        data = json.load(f)

    calendars = {k: Calendar() for k in REGION_FILES}

    for item in data:
        real_deadline = datetime(YEAR, item["month"], item["day"])

        emojis = "".join([EMOJI.get(tag, "") for tag in item.get("tags", [])])
        summary = f"🔴 {emojis} {item['name']}"

        event = Event()
        event.add("summary", summary)

        # ✅ EVENT JE SAMO NA DEADLINE DAN
        event.add("dtstart", real_deadline)
        event.add("dtend", real_deadline + timedelta(days=1))

        # ✅ pomembno za update (brez podvajanja)
        uid = f"{item['name']}-{real_deadline.date()}"
        event.add("uid", uid)

        event.add("url", item["url"])

        # ✅ lepši description
        event.add(
            "description",
            f"Deadline: {real_deadline.strftime('%d.%m.%Y')}\nApply: {item['url']}"
        )

        # ✅ alarmi
        for d in [30, 14, 7, 1]:
            event.add_component(create_alarm(d))

        # dodaj v pravilen koledar
        region = item["region"]
        if region in calendars:
            calendars[region].add_component(event)

    # shrani vse koledarje
    for region, cal in calendars.items():
        with open(REGION_FILES[region], "wb") as f:
            f.write(cal.to_ical())


if __name__ == "__main__":
    build()
