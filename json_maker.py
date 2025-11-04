import json
from datetime import date, timedelta

# Configuration year - UPDATE THESE VALUES FOR NEW YEAR
# current_year: Gregorian year when the biblical year begins
# bore_year: Biblical year (Aviv to Aviv)
# yehudim_year: Jewish calendar year (Tishrei to Tishrei)
current_year = 2025
bore_year = 6025
yehudim_year = 5785

# Example for next year (uncomment and update when ready):
# current_year = 2026
# bore_year = 6026
# yehudim_year = 5786

# Base dates for the year (UPDATE THESE DATES ANNUALLY based on new moon sightings)
base_months = [
    {"name": "Aviv", "month": 3, "day": 31, "days": 29, "bore_month": 1, "yehudim_month": "Nisán"},
    {"name": "Ziv",  "month": 4, "day": 28, "days": 30, "bore_month": 2, "yehudim_month": "Iyyar"},
    {"name": "3rd month","month": 5, "day": 27, "days": 29, "bore_month": 3, "yehudim_month": "Sivan"},
    {"name": "4th month","month": 6, "day": 27, "days": 30, "bore_month": 4, "yehudim_month": "Tamuz"},
    {"name": "5th month","month": 7, "day": 27, "days": 29, "bore_month": 5, "yehudim_month": "Av"},
    {"name": "6th month","month": 8, "day": 24, "days": 30, "bore_month": 6, "yehudim_month": "Elul"},
    {"name": "Etanim","month": 9, "day": 24, "days": 29, "bore_month": 7, "yehudim_month": "Tishrei"},
    {"name": "Bul","month": 10, "day": 24, "days": 30, "bore_month": 8, "yehudim_month": "Cheshvan"}
]

# Generate months with actual dates
months = []
for base_month in base_months:
    months.append({
        "name": base_month["name"],
        "start": date(current_year, base_month["month"], base_month["day"]),
        "days": base_month["days"],
        "bore_month": base_month["bore_month"],
        "yehudim_month": base_month["yehudim_month"]
    })

# First day of the Omer count (UPDATE THIS DATE ANNUALLY - 16th of Aviv/Nisan)
first_omer_day = date(current_year, 4, 21)
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
        
        # bore month name (usando el nombre definido en la configuración)
        bore_month_name = month["name"]

        bore = f"{bore_day} {bore_month_name} {bore_year}"
        yehudim = f"{bore_day} {month['yehudim_month']} {yehudim_year}"

        note = ""
        event = ""

        # Events for Aviv
        if month["name"] == "Aviv":
            if bore_day == 1:
                note = "Beginning of the Biblical year"
                event = "Rosh Hashanah"
            if bore_day == 14:
                note = "Pesach begins at sunset"
                event = "Pesach"
            if bore_day == 15:
                note = "Start of Hag Ha'Matzot"
                event = "Hag Ha'Matzot"
            if bore_day == 21:
                note = "Bikurim (Firstfruits) and first day of the Omer"
                event = "Bikurim and Omer"

        # Events for Etanim (Fall Festivals)
        if month["name"] == "Etanim":
            if bore_day == 1:
                note = "Yom Terua (Rosh Hashana)"
                event = "Yom Terua"
            if bore_day == 10:
                note = "Yom Ha'Kipurim (Day of Atonement)"
                event = "Yom Ha'Kipurim"
            if bore_day == 15:
                note = "Sucot begins"
                event = "Sucot"

        # Omer count
        if iso_date in omer_count:
            note += f" | Omer day {omer_count[iso_date]}"
            event = "Omer"

        # Shavuot on day 50 of the Omer
        if iso_date in omer_count and omer_count[iso_date] == 50:
            note += " | Shavuot"
            event = "Shavuot"

        # New month markers
        if bore_day == 1 and month["bore_month"] != 1 and not event:
            note = f"Beginning of month {bore_month_name}"
            event = "New month"

        calendar[iso_date] = {
            "bore": bore,
            "yehudim": yehudim,
            "note": note.strip(" |"),
            "moon": "visible" if bore_day == 1 else "",
            "aviv": "confirmed" if month["name"] == "Aviv" and bore_day == 1 else "",
            "event": event
        }

# Save to JSON
filename = f"{bore_year}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(calendar, f, ensure_ascii=False, indent=2)

print(f"✅ Calendar successfully generated: {filename}")