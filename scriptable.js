// CONFIG
const jsonUrl = "https://raw.githubusercontent.com/yonice7/bore/main/6025.json";

// get JSON from GitHub raw
let req = new Request(jsonUrl);
let jsonData = await req.loadJSON();

// get today's date (Scriptable local timezone)
let now = new Date();

// day change after sunset
let sunsetHour = 18;
// if (now.getHours() >= sunsetHour) {
//  now.setDate(now.getDate() + 1);
// }

let todayISO = now.toISOString().slice(0,10);

// lookup
let entry = jsonData[todayISO] || {
  bore: "Unknown",
  hebrew: "Unknown",
  note: "",
  moon: "",
  aviv: "",
  event: ""
};

// extract bore parts
let boreParts = entry.bore.split(" ");
let boreDay = boreParts[0] || "";
let boreMonth = boreParts[1] || "";
let boreYear = boreParts[2] || "";

// build widget
let w = new ListWidget();
w.setPadding(12, 12, 12, 12);
w.backgroundColor = new Color("#fefefe");

// main bore day (big & bold)
let dayText = w.addText(boreDay);
dayText.font = Font.boldSystemFont(48);
dayText.textColor = Color.black();
dayText.centerAlignText();

// month and year (larger)
let monthYearText = w.addText(`${boreMonth} ${boreYear}`);
monthYearText.font = Font.systemFont(16);
monthYearText.textColor = Color.gray();
monthYearText.centerAlignText();

w.addSpacer(8);

// gregorian date (larger light gray)
let gregorian = now.toLocaleDateString("es-CO", { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
let gregText = w.addText(`${gregorian}`);
gregText.font = Font.systemFont(14);
gregText.textColor = Color.lightGray();
gregText.centerAlignText();

// hebrew date (larger light gray)
let hebrewText = w.addText(`${entry.hebrew}`);
hebrewText.font = Font.systemFont(14);
hebrewText.textColor = Color.lightGray();
hebrewText.centerAlignText();

w.addSpacer(4);

// note or event
if (entry.note) {
  let note = w.addText(entry.note);
  note.font = Font.systemFont(14);
  note.textColor = Color.darkGray();
  note.centerAlignText();
}

if (entry.event) {
  let ev = w.addText(entry.event);
  ev.font = Font.boldSystemFont(14);
  ev.textColor = new Color("#d9534f"); // subtle red
  ev.centerAlignText();
}

// finalize
if (config.runsInWidget) {
  Script.setWidget(w);
} else {
  w.presentMedium();
}
Script.complete();