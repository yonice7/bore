# Biblical Hebrew Calendar

Python tool to generate a biblical Hebrew calendar based on new moon sightings in Israel. Create a mobile widget to display biblical dates on your device, with all days of the year including festivals, new moons, and special events, inspired by the works of Michael Rood, Adam Drissel, Deborah Gordon, and Mark Harris.

## References
- [When Is The New Moon](https://whenisthenewmoon.com)
- [El Cuerpo del Mesías](https://elcuerpodelmesias.com)
- [Michael Rood](https://www.michaelrood.com)

## Generate Calendar

1. **Update dates** in `json_maker.py` based on current new moon sightings from [whenisthenewmoon.com](https://whenisthenewmoon.com)
2. **Run**: `python json_maker.py`
3. **Output**: Creates `6025.json` with biblical calendar data

## iPhone Setup

### 1. Install Scriptable
Download **Scriptable** from the App Store.

### 2. Add Script
- Open Scriptable → Tap **+** → Create new script
- Copy `scriptable.js` content → Paste into script
- Name it "Biblical Calendar"

### 3. Configure
Update `jsonUrl` in the script to point to your JSON file location.

### 4. Add Widget
- Long-press home screen → **+** → **Scriptable**
- Select your script → Choose Medium size → **Add Widget**

### 5. Done!
Widget shows biblical date, Gregorian date, and special events.

## Key Events

### Spring Festivals (Aviv)
- **Aviv 1**: Rosh Hashanah (Biblical New Year)
- **Aviv 10**: Day of Preparation
- **Aviv 14**: Pesach (Passover) - Evening begins
- **Aviv 15**: Hag Ha'Matzot (Unleavened Bread) begins
- **Aviv 16**: Bikurim (Firstfruits) & Omer count begins
- **Aviv 21**: Last Day of Unleavened Bread
- **Aviv +50**: Shavuot (Pentecost/Weeks)

### Fall Festivals (Etanim)
- **Etanim 1**: Yom Terua (Feast of Trumpets)
- **Etanim 10**: Yom Ha'Kipurim (Day of Atonement)
- **Etanim 15**: Sukkot (Tabernacles) begins
- **Etanim 21**: Last Day of Tabernacles
- **Etanim 22**: Shemini Atzeret (Eighth Day)

### New Moon Days
- **1st of every month**: New Moon (Rosh Chodesh) - Work prohibited
- **30th of every month**: Last day of month

### Omer Count
- **Daily from Aviv 16 to Aviv +49**: Count of Omer (49 days)
- **Aviv +50**: Shavuot (completion of 50 days)

### Special Days
- **Weekly**: Shabbat (Sabbath) - From Friday sunset to Saturday sunset

## Disclaimer
Based on visual new moon sightings.
