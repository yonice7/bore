// CONFIG -------------------------------------------------------------
// URL del JSON con llaves por fecha civil (yyyy-mm-dd)
const jsonUrl = "https://raw.githubusercontent.com/yonice7/bore/main/6025.json";

// Hora fija de “puesta del sol” (heurística). Si >= 18, cambia el día bíblico.
const sunsetHour = 18;

// UI colors
const BG_COLOR = "#fefefe";
const ACCENT_RED = "#d9534f";

// -------------------------------------------------------------------
// Fetch JSON (raw GitHub)
const req = new Request(jsonUrl);
const jsonData = await req.loadJSON();

// === Keep two timelines ============================================
// civilNow: real local civil time (no sunset shift)
// boreNow : “biblical day” time (shifted after sunset ONLY for lookup)
const now = new Date();
const civilNow = new Date(
  now.getFullYear(), now.getMonth(), now.getDate(),
  now.getHours(), now.getMinutes(), now.getSeconds()
);

const boreNow = new Date(civilNow);
if (boreNow.getHours() >= sunsetHour) {
  console.log(`✅ Después de las ${sunsetHour}h, sumando +1 día SOLO para el lookup bore`);
  boreNow.setDate(boreNow.getDate() + 1);
}

// === Helpers ========================================================
function toISODate(d) {
  // Local ISO date without UTC shifts
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

const civilISO = toISODate(civilNow); // for gregorian display
const lookupISO = toISODate(boreNow); // for JSON lookup

console.log(`📌 Fecha civil (gregoriano): ${civilISO}`);
console.log(`📌 Fecha usada para lookup JSON (bore): ${lookupISO}`);

// === Lookup JSON by bore “biblical day” key =========================
let entry = jsonData[lookupISO];

// Optional graceful fallback: if not found, fall back to civilISO
if (!entry) {
  console.log("⚠️ No encontré entrada para el día bore. Probando con la fecha civil…");
  entry = jsonData[civilISO];
}

if (!entry) {
  console.log("❌ No hay entrada ni para bore ni para civil. Usando valores por defecto.");
  entry = {
    bore: "Unknown",
    hebrew: "Unknown",
    note: "",
    moon: "",
    aviv: "",
    event: ""
  };
}

// === Extract bore parts =============================================
const boreParts = (entry.bore || "").split(" ");
const boreDay   = boreParts[0] || "";
const boreYear  = boreParts[boreParts.length - 1] || "";
const boreMonth = boreParts.slice(1, boreParts.length - 1).join(" ");

// === Build widget ===================================================
const w = new ListWidget();
w.setPadding(12, 12, 12, 12);
w.backgroundColor = new Color(BG_COLOR);

// Main bore day (big & bold)
const dayText = w.addText(boreDay);
dayText.font = Font.boldSystemFont(48);
dayText.textColor = Color.black();
dayText.centerAlignText();

// Month and year (bore)
const monthYearText = w.addText(`${boreMonth} ${boreYear}`);
monthYearText.font = Font.systemFont(16);
monthYearText.textColor = Color.gray();
monthYearText.centerAlignText();

w.addSpacer(8);

// Gregorian date: ALWAYS from civilNow (no sunset shift)
const gregorian = civilNow.toLocaleDateString("es-CO", {
  weekday: "short",
  day: "numeric",
  month: "short",
  year: "numeric"
});
const gregText = w.addText(`${gregorian}`);
gregText.font = Font.systemFont(14);
gregText.textColor = Color.lightGray();
gregText.centerAlignText();

// Hebrew date (from JSON entry)
const hebrewText = w.addText(`${entry.hebrew}`);
hebrewText.font = Font.systemFont(14);
hebrewText.textColor = Color.lightGray();
hebrewText.centerAlignText();

w.addSpacer(4);

// Note (optional)
if (entry.note) {
  const note = w.addText(entry.note);
  note.font = Font.systemFont(14);
  note.textColor = Color.darkGray();
  note.centerAlignText();
}

// Event (optional, highlighted)
if (entry.event) {
  const ev = w.addText(entry.event);
  ev.font = Font.boldSystemFont(14);
  ev.textColor = new Color(ACCENT_RED);
  ev.centerAlignText();
}

// === Finalize =======================================================
if (config.runsInWidget) {
  Script.setWidget(w);
} else {
  w.presentMedium();
}
Script.complete();