#!/bin/bash

# Command to show today's date according to the bore calendar
# Usage: ./bore

# JSON file with bore dates
JSON_FILE="$(dirname "$0")/6025.json"

# Verify the file exists
if [[ ! -f "$JSON_FILE" ]]; then
    echo "❌ Error: 6025.json file not found"
    exit 1
fi

# Get current date and time
NOW=$(date +"%Y-%m-%d %H:%M:%S")
ISO_DATE=$(date +"%Y-%m-%d")
CURRENT_HOUR=$(date +"%H")

# Calculate date for bore lookup (after 18h = next day)
if [[ $CURRENT_HOUR -ge 18 ]]; then
    LOOKUP_DATE=$(date -v+1d +"%Y-%m-%d")
    echo "Today is:"
else
    LOOKUP_DATE=$ISO_DATE
    echo "Today is:"
fi

# Search for calendar entry
ENTRY=$(jq -r --arg date "$LOOKUP_DATE" '.[$date] // empty' "$JSON_FILE" 2>/dev/null || echo "")

if [[ -z "$ENTRY" || "$ENTRY" == "null" ]]; then
    # If bore date not found, try civil date
    ENTRY=$(jq -r --arg date "$ISO_DATE" '.[$date] // empty' "$JSON_FILE" 2>/dev/null || echo "")
    if [[ -z "$ENTRY" || "$ENTRY" == "null" ]]; then
        echo "❌ No information found for date $LOOKUP_DATE (bore) or $ISO_DATE (civil)"
        exit 1
    fi
fi

# Extract fields from JSON
BORE=$(echo "$ENTRY" | jq -r '.bore // "Unknown"' 2>/dev/null || echo "Unknown")
YEHUDIM=$(echo "$ENTRY" | jq -r '.yehudim // "Unknown"' 2>/dev/null || echo "Unknown")
EVENT=$(echo "$ENTRY" | jq -r '.event // empty' 2>/dev/null || echo "")
NOTE=$(echo "$ENTRY" | jq -r '.note // empty' 2>/dev/null || echo "")
MOON=$(echo "$ENTRY" | jq -r '.moon // empty' 2>/dev/null || echo "")
AVIV=$(echo "$ENTRY" | jq -r '.aviv // empty' 2>/dev/null || echo "")

# Display information
echo "   Bore: $BORE"
echo "   Yehudim: $YEHUDIM"
echo "   Gregorian: $(date +"%A %d %B %Y")"

# Optional fields
[[ -n "$EVENT" ]] && echo "   🎉 Event: $EVENT"
[[ -n "$NOTE" ]] && echo "   📝 Note: $NOTE"
[[ -n "$MOON" ]] && echo "   🌙 Moon: $MOON"
[[ -n "$AVIV" ]] && echo "   🌾 Aviv: $AVIV"

exit 0