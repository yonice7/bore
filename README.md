# Biblical Hebrew Calendar Generator

A Python-based tool to generate a biblical Hebrew calendar (Bore calendar) based on new moon sightings in Israel. This calendar follows the Creator's calendar as observed by dedicated watchmen, inspired by the works of Michael Rood, Adam Drissel, Deborah Gordon and Mark Harris

## References

- [When Is The New Moon](https://whenisthenewmoon.com) - Primary source for new moon sighting reports from Israel
- [El Cuerpo del Mesías](https://elcuerpodelmesias.com) - Spanish resource for biblical calendar information
- Works by Michael Rood, Adam Drissel, and Deborah Gordon

## Project Structure

- `json_maker.py` - Python script that generates the calendar JSON file
- `6025.json` - Generated calendar data for biblical year 6025 (Gregorian 2025)
- `scriptable.js` - iOS Scriptable widget for displaying biblical dates
- `LICENSE` - MIT License

## How It Works

The calendar is based on visual sightings of the new moon crescent in Israel. Unlike the modern Jewish calendar (which uses mathematical calculations), this follows the biblical commandment to observe the moon and determine festival dates accordingly.

### Key Principles

- **New Moon Sighting**: Each month begins when the new moon crescent is first visible from Jerusalem
- **Biblical Year**: Starts in Aviv (March/April) with the spring barley harvest
- **Festival Dates**: Determined by counting from the new moon, not fixed Gregorian dates
- **Witness Verification**: Requires multiple witnesses for validity

## Generating the Calendar

### Usage

1. **Update Configuration**: Edit the dates in `json_maker.py` based on current year new moon sightings:

```python
# Configuration for the current year
current_year = 2025      # Gregorian year
bore_year = 6025         # Biblical year (Aviv to Aviv)
yehudim_year = 5785      # Traditional Jewish year (Tishrei to Tishrei)

# Update base_months with actual sighting dates
base_months = [
    {"name": "Aviv", "month": 3, "day": 31, "days": 29, "bore_month": 1, "yehudim_month": "Nisán"},
    # ... update each month's start date based on sightings
]
```

2. **Update Festival Dates**: Modify the first Omer day date (16th of Aviv/Nisan):

```python
first_omer_day = date(current_year, 4, 21)  # Adjust based on actual Aviv 16
```

3. **Run the Generator**:

```bash
python json_maker.py
```

This creates a JSON file (e.g., `6025.json`) with the complete biblical calendar.

### JSON Structure

Each date entry contains:

```json
{
  "2025-03-31": {
    "bore": "1 Aviv 6025",
    "yehudim": "1 Nisán 5785",
    "note": "Beginning of the Biblical year",
    "moon": "visible",
    "aviv": "confirmed",
    "event": "Rosh Hashanah"
  }
}
```

## iOS Setup with Scriptable

Scriptable is an iOS automation app that allows JavaScript-based widgets. Use the provided `scriptable.js` to display biblical dates on your iPhone.

### Step-by-Step iPhone Setup

#### 1. Install Scriptable App
- Download **Scriptable** from the App Store
- Open the app and grant necessary permissions

#### 2. Add the Biblical Calendar Script
- In Scriptable, tap the **+** button to create a new script
- Copy the entire contents of `scriptable.js`
- Paste it into the new script
- Name it "Biblical Calendar" or similar

#### 3. Configure the Script
- **Update JSON URL**: If hosting the JSON elsewhere, modify `jsonUrl`:
  ```javascript
  const jsonUrl = "https://your-host.com/6025.json";
  ```
- **Adjust Sunset Time**: Modify `sunsetHour` if needed (default: 18:00):
  ```javascript
  const sunsetHour = 18; // Biblical day changes at sunset
  ```

#### 4. Add to Home Screen Widget
- Long-press on your iPhone home screen
- Tap the **+** button in the top-left corner
- Scroll down and select **Scriptable**
- Choose your script ("Biblical Calendar")
- Select widget size (Medium recommended)
- Tap **Add Widget**

#### 5. Grant Permissions
- The first time you run the widget, Scriptable may request network access
- Allow access to load the JSON calendar data

#### 6. Test the Widget
- The widget should now display:
  - Large biblical day number
  - Biblical month and year
  - Current Gregorian date
  - Traditional Hebrew date
  - Any special notes or events

### Widget Features

- **Real-time Updates**: Automatically shows the correct biblical day
- **Sunset Logic**: Biblical day changes at sunset (configurable)
- **Event Highlights**: Special biblical events appear in red
- **Fallback Handling**: Gracefully handles missing data

### Troubleshooting iOS Setup

**Widget not updating:**
- Force-refresh by tapping the widget
- Check internet connection for JSON loading

**Script errors:**
- Verify JSON URL is accessible
- Ensure JSON format matches expected structure

**Date showing incorrectly:**
- Confirm your timezone settings
- Adjust `sunsetHour` if needed for your location

## Biblical Calendar Events

The calendar includes these key biblical events:

### Spring Festivals (Aviv)
- **Rosh Hashanah**: New Year (Aviv 1)
- **Pesach**: Passover (Aviv 14)
- **Hag Ha'Matzot**: Unleavened Bread (Aviv 15-21)
- **Bikurim**: Firstfruits (Aviv 16, start of Omer count)
- **Shavuot**: Pentecost (50 days after Firstfruits)

### Fall Festivals (Etanim/Tishrei)
- **Yom Terua**: Feast of Trumpets (Etanim 1)
- **Yom Ha'Kipurim**: Day of Atonement (Etanim 10)
- **Sucot**: Tabernacles (Etanim 15-21)

## Disclaimer

This calendar is based on visual new moon sightings and represents one interpretation of biblical calendar principles. Always verify dates with multiple reliable sources and consult with qualified teachers.
