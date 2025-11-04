# the bore calendar

Create a mobile widget to display biblical dates on your device, with all days of the year including festivals, new moons, and special events, inspired by the works of Michael Rood, Adam Drissel, Deborah Gordon, and Mark Harris.

## data
- [When Is The New Moon](https://whenisthenewmoon.com)
- [El Cuerpo del Mesías](https://elcuerpodelmesias.com)
- [Michael Rood](https://www.michaelrood.com)

## generate the calendar in your machine
*clone this repo into your machine or even faster --> just copy paste `scriptable.js` into your iOS app (I always try to keep this up-to-date since I use it myself*

1. **Update dates** in `json_maker.py` based on current new moon sightings from [whenisthenewmoon.com](https://whenisthenewmoon.com)
2. **Run**: `python json_maker.py`
3. **Output**: Creates `6025.json` with biblical calendar data

## iphone setup

### 1. Install Scriptable
Download **Scriptable** from the App Store.

### 2. Add Script
- Open Scriptable → Tap **+** → Create new script
- Copy `scriptable.js` content → Paste into script
- Name it the way you want, I just go by "bore"

### 3. Configure
Update `jsonUrl` in the script to point to your JSON file location.

### 4. Add Widget
- Long-press home screen → Edit → Add widget → **Scriptable**
- Select your script → Choose Medium size → **Add Widget**

### 5. Done!
Widget shows biblical date, Gregorian date, and special events.

## key events
*always try as much as possible to observe them according to the Torah*

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

**shalom**
