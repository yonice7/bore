# The Bore Calendar

Create a mobile widget to display biblical dates on your device, with all days of the year including festivals, new moons, and special events, inspired by the works of Michael Rood, Adam Drissel, Deborah Gordon, and Mark Harris.

## Data Sources
- [When Is The New Moon](https://whenisthenewmoon.com)
- [El Cuerpo del Mesías](https://elcuerpodelmesias.com)
- [Michael Rood](https://www.michaelrood.com)
- [NASA Daily Moon Guide](https://moon.nasa.gov/moon-observation/daily-moon-guide/?intent=021#1763721791380::0::) ← super handy to eyeball real-time moon visibility straight from the source

## Generate Calendar Locally
*Clone this repo or copy `scriptable.js` into Scriptable app (kept up-to-date)*

1. **Update dates** in `json_maker.py` using [whenisthenewmoon.com](https://whenisthenewmoon.com) + [NASA moon guide](https://moon.nasa.gov/moon-observation/daily-moon-guide/?intent=021#1763721791380::0::)
2. **Run**: `python json_maker.py`
3. **Output**: Creates `6025.json` with biblical calendar data

## Setup

### iPhone Setup

1. **Install Scriptable**: Download **Scriptable** from the App Store
2. **Add Script**: Open Scriptable → Tap **+** → Create new script → Copy `scriptable.js` content → Paste into script → Name it "bore"
3. **Configure**: Update `jsonUrl` in script to point to your JSON file location
4. **Add Widget**: Long-press home screen → Edit → Add widget → **Scriptable** → Select script → Choose Medium size → Add Widget
5. **Done!**: Widget shows biblical date, Gregorian date, and special events

### Android Setup
- WIP

### Terminal Setup

1. **Clone repo**: `git clone <repository-url> && cd bore`
2. **Make executable**: `chmod +x bore`
3. **Run command**: `./bore` to see today's date
4. **Add alias** (optional): Run this command from the bore directory to add `bore-today` alias to your `.zshrc`:

   ```bash
   echo -e "\n# bore\nalias bore-today='$(pwd)/bore'" >> ~/.zshrc && source ~/.zshrc
   ```

5. **Use alias**: Now you can run `bore-today` from any directory to see today's date

## Key Events
*Always observe according to the Torah*

| Event | Date | Description |
|-------|------|-------------|
| **Spring Festivals (Aviv)** | | |
| Rosh Hashanah | Aviv 1 | Biblical New Year |
| Day of Preparation | Aviv 10 | Preparation for Passover |
| Pesach (Passover) | Aviv 14 | Evening begins |
| Hag Ha'Matzot | Aviv 15 | Unleavened Bread begins |
| Bikurim & Omer | Aviv 16 | Firstfruits & Omer count begins |
| Last Day Unleavened Bread | Aviv 21 | End of Unleavened Bread |
| Shavuot | Aviv +50 | Pentecost/Weeks |
| **Fall Festivals (Etanim)** | | |
| Yom Teruah | Etanim 1 | Feast of Trumpets |
| Yom Ha'Kipurim | Etanim 10 | Day of Atonement |
| Sukkot | Etanim 15 | Tabernacles begins |
| Last Day Tabernacles | Etanim 21 | End of Tabernacles |
| Shemini Atzeret | Etanim 22 | Eighth Day |
| **New Moon Days** | | |
| New Moon (Rosh Hodesh) | 1st of every month | Work prohibited |
| **Omer Count** | | |
| Count of Omer | Daily Aviv 16 to Aviv +49 | 49 days |
| Shavuot | Aviv +50 | Completion of 50 days |
| **Special Days** | | |
| Shabbat (Sabbath) | Weekly | Friday sunset to Saturday sunset |

## Disclaimer
Based on visual new moon sightings.

**shalom**
