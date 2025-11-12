// ============================================================================
// CONFIGURATION
// ============================================================================
const CONFIG = {
  jsonUrl: "https://raw.githubusercontent.com/yonice7/bore/main/6025.json",
  sunsetHour: 18,
  colors: {
    background: "#fefefe",
    accentRed: "#d9534f",
    black: Color.black(),
    gray: Color.gray(),
    lightGray: Color.lightGray(),
    darkGray: Color.darkGray()
  },
  fonts: {
    day: Font.boldSystemFont(48),
    monthYear: Font.systemFont(16),
    body: Font.systemFont(14),
    event: Font.boldSystemFont(14)
  },
  spacing: {
    small: 4,
    medium: 8
  },
  locale: "es-CO"
};

const DEFAULT_ENTRY = {
  bore: "Unknown",
  yehudim: "Unknown",
  note: "",
  moon: "",
  aviv: "",
  event: ""
};

// ============================================================================
// DATA HELPERS
// ============================================================================

/**
 * Converts a Date object to ISO date string (yyyy-mm-dd) without UTC shifts
 */
function toISODate(date) {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

/**
 * Calculates the biblical day date (shifted after sunset)
 */
function getBiblicalDate(civilDate, sunsetHour) {
  const biblicalDate = new Date(civilDate);
  if (biblicalDate.getHours() >= sunsetHour) {
    console.log(`✅ Después de las ${sunsetHour}h, sumando +1 día SOLO para el lookup bore`);
    biblicalDate.setDate(biblicalDate.getDate() + 1);
  }
  return biblicalDate;
}

/**
 * Parses bore date string into day, month, and year components
 */
function parseBoreDate(boreString) {
  const parts = (boreString || "").split(" ");
  return {
    day: parts[0] || "",
    month: parts.slice(1, parts.length - 1).join(" "),
    year: parts[parts.length - 1] || ""
  };
}

/**
 * Fetches calendar data from JSON and finds entry for current date
 */
async function getCalendarEntry(jsonUrl, lookupISO, fallbackISO) {
  const req = new Request(jsonUrl);
  const jsonData = await req.loadJSON();
  
  let entry = jsonData[lookupISO];
  
  if (!entry) {
    console.log("⚠️ No encontré entrada para el día bore. Probando con la fecha civil…");
    entry = jsonData[fallbackISO];
  }
  
  if (!entry) {
    console.log("❌ No hay entrada ni para bore ni para civil. Usando valores por defecto.");
    entry = DEFAULT_ENTRY;
  }
  
  return entry;
}

// ============================================================================
// UI HELPERS
// ============================================================================

/**
 * Creates a styled text element in the widget
 */
function addStyledText(widget, text, options = {}) {
  const {
    font = CONFIG.fonts.body,
    color = CONFIG.colors.lightGray,
    align = "center"
  } = options;
  
  const textElement = widget.addText(text);
  textElement.font = font;
  textElement.textColor = color;
  
  if (align === "center") {
    textElement.centerAlignText();
  }
  
  return textElement;
}

/**
 * Creates the main widget UI
 */
function buildWidget(entry, civilDate) {
  const widget = new ListWidget();
  widget.setPadding(12, 12, 12, 12);
  widget.backgroundColor = new Color(CONFIG.colors.background);
  
  // Parse bore date
  const boreDate = parseBoreDate(entry.bore);
  
  // Main day (big & bold)
  addStyledText(widget, boreDate.day, {
    font: CONFIG.fonts.day,
    color: CONFIG.colors.black
  });
  
  // Month and year
  addStyledText(widget, `${boreDate.month} ${boreDate.year}`, {
    font: CONFIG.fonts.monthYear,
    color: CONFIG.colors.gray
  });
  
  widget.addSpacer(CONFIG.spacing.medium);
  
  // Gregorian date
  const gregorian = civilDate.toLocaleDateString(CONFIG.locale, {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric"
  });
  addStyledText(widget, gregorian);
  
  // Hebrew date (yehudim) - Rabbinic calendar
  if (entry.yehudim) {
    addStyledText(widget, entry.yehudim);
  }
  
  widget.addSpacer(CONFIG.spacing.small);
  
  // Optional note
  if (entry.note) {
    addStyledText(widget, entry.note, {
      color: CONFIG.colors.darkGray
    });
  }
  
  // Optional event (highlighted)
  if (entry.event) {
    addStyledText(widget, entry.event, {
      font: CONFIG.fonts.event,
      color: new Color(CONFIG.colors.accentRed)
    });
  }
  
  return widget;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  // Calculate dates
  const now = new Date();
  const civilNow = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    now.getHours(),
    now.getMinutes(),
    now.getSeconds()
  );
  
  const boreNow = getBiblicalDate(civilNow, CONFIG.sunsetHour);
  const civilISO = toISODate(civilNow);
  const lookupISO = toISODate(boreNow);
  
  console.log(`📌 Fecha civil (gregoriano): ${civilISO}`);
  console.log(`📌 Fecha usada para lookup JSON (bore): ${lookupISO}`);
  
  // Fetch calendar entry
  const entry = await getCalendarEntry(CONFIG.jsonUrl, lookupISO, civilISO);
  
  // Build and display widget
  const widget = buildWidget(entry, civilNow);
  
  if (config.runsInWidget) {
    Script.setWidget(widget);
  } else {
    widget.presentMedium();
  }
  
  Script.complete();
}

// Run main function
main();
