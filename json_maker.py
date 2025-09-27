import json
from datetime import date, timedelta

# Configuration of the 4 months
months = [
    {"name": "Aviv", "start": date(2025, 3, 31), "days": 29, "bore_month": 1, "hebrew_month": "Nisán"},
    {"name": "Ziv",  "start": date(2025, 4, 28), "days": 30, "bore_month": 2, "hebrew_month": "Iyyar"},
    {"name": "Sivan","start": date(2025, 5, 27), "days": 29, "bore_month": 3, "hebrew_month": "Sivan"},
    {"name": "Tammuz","start": date(2025, 6, 27), "days": 30, "bore_month": 4, "hebrew_month": "Tamuz"},
    {"name": "Av","start": date(2025, 7, 27), "days": 29, "bore_month": 5, "hebrew_month": "Av"},
    {"name": "Elul","start": date(2025, 8, 24), "days": 30, "bore_month": 6, "hebrew_month": "Elul"},
    {"name": "Tishrei","start": date(2025, 9, 24), "days": 29, "bore_month": 7, "hebrew_month": "Tishrei"},
]

# First day of the Omer count
first_omer_day = date(2025, 4, 21)
omer_count = {}

# Generate omer count for 50 days
for i in range(50):
    day = first_omer_day + timedelta(days=i)
    omer_count[day.isoformat()] = i + 1

# Final JSON dictionary
calendar = {}

for month in months:
    start_date = month["start"]
    for d in range(month["days"]):
        current = start_date + timedelta(days=d)
        iso_date = current.isoformat()
        bore_day = d + 1
        
        # bore month name
        if month["bore_month"] == 1:
            bore_month_name = "Aviv"
        elif month["bore_month"] == 2:
            bore_month_name = "Ziv"
        elif month["bore_month"] == 7:
            bore_month_name = "Etanim"
        elif month["bore_month"] == 8:
            bore_month_name = "Bul"
        else:
            # para los no-bíblicos (en este caso 3 y 4)
            bore_month_name = f"{month['bore_month']}° mes"

        bore = f"{bore_day} {bore_month_name} 6025"
        hebrew = f"{bore_day} {month['hebrew_month']} 5785"

        note = ""
        event = ""

        # Events for Aviv
        if month["name"] == "Aviv":
            if bore_day == 1:
                note = "Beginning of the Biblical year"
                event = "Rosh Hashanah"
            if bore_day == 10:
                note = "Selection of the Pesach lamb"
                event = "Pesach lamb selection"
            if bore_day == 14:
                note = "Pesach begins at sunset"
                event = "Pesach"
            if bore_day == 15:
                note = "Start of Unleavened Bread (High Shabbat)"
                event = "Unleavened Bread"
            if bore_day == 21:
                note = "Firstfruits and first day of the Omer"
                event = "Firstfruits and Omer"

        # Omer count
        if iso_date in omer_count:
            note += f" | Omer day {omer_count[iso_date]}"
            event = "Omer"

        # Shavuot on day 50 of the Omer
        if iso_date in omer_count and omer_count[iso_date] == 50:
            note += " | Shavuot"
            event = "Shavuot"

        # New month markers
        if bore_day == 1 and month["bore_month"] != 1:
            note = f"Beginning of month {bore_month_name}"
            event = "New month"

        calendar[iso_date] = {
            "bore": bore,
            "hebrew": hebrew,
            "note": note.strip(" |"),
            "moon": "visible" if bore_day == 1 else "",
            "aviv": "confirmed" if month["name"] == "Aviv" and bore_day == 1 else "",
            "event": event
        }

# Save to JSON
with open("6025.json", "w", encoding="utf-8") as f:
    json.dump(calendar, f, ensure_ascii=False, indent=2)

print("✅ Calendar successfully generated: 6025.json")