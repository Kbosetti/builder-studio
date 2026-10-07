// GET /api/book?d=<division>&l=<land_status>
//
// The "Visit a Design Studio" and "Schedule my visit" buttons on the quiz and
// the full portrait come here. If the division's Design Studio Visit calendar
// in Builder Studio is switched on and has open times in the next 30 days, the
// buyer goes straight to its booking page. Otherwise they go to that studio's
// page on mitchellhomesinc.com (address, phone, and Mitchell's own contact and
// scheduling form), or the Contact page for undecided buyers, so a calendar
// that is off or has no hours never shows a buyer an error. Turning a
// calendar on in Builder Studio is all it takes for booking to start working;
// no redeploy.
//
// This is the only place the calendar IDs live. Uses HBS_PIT from Vercel env.
const BASE = "https://services.leadconnectorhq.com";
const WIDGET = "https://api.leadconnectorhq.com/widget/booking/";
const SITE = "https://mitchellhomesinc.com";
// Fallbacks when a calendar is not bookable. Checked live October 7, 2026.
const STUDIO_PAGE = {
  "Richmond, VA":       SITE + "/design-center/richmond-va/",
  "Fredericksburg, VA": SITE + "/design-center/fredericksburg-va/",
  "Newport News, VA":   SITE + "/design-center/newport-news-va/",
  "Raleigh, NC":        SITE + "/design-center/raleigh-nc/",
  "Wilmington, NC":     SITE + "/design-center/wilmington-nc/"
};
const CONTACT_PAGE = SITE + "/contact/";

// Design Studio Visit calendars per division: with land / no land.
const BOOKING = {
  "Richmond, VA":       { land: "lefHeBcANsbjZf5IhZGw", noland: "LSDaGxShOPqb9J1t4SCO" },
  "Fredericksburg, VA": { land: "46oGCWfZJoFwbuub1wtV", noland: "fkAfa07N4rovoVR0iZMt" },
  "Newport News, VA":   { land: "4bOw8XC3FS9aBi1lxCaJ", noland: "yHaSZPNP24gcGJkY6MoP" },
  "Raleigh, NC":        { land: "e7IJYU4ZVbxtsf3RZpbP", noland: "ET1aeQY6CmEOXUEZEMZa" },
  "Wilmington, NC":     { land: "dEtDNPpoKNnBTY7Sw2Y9", noland: "nf3cLjxsG069HUeNCWkU" }
};
// Buyers who chose "Somewhere else, or still deciding": Fredericksburg Phone Consultation.
const UNDECIDED = "izsSdkJpFJbCdMsOdFcf";

function calendarFor(division, land) {
  const b = BOOKING[division];
  if (!b) return UNDECIDED;
  return (land === "owned" || land === "family") ? b.land : b.noland;
}

// True when the calendar is active and has at least one open slot in the next 30 days.
// An inactive calendar answers 400 "Calendar is inactive"; any failure counts as not bookable.
async function bookable(id) {
  if (!process.env.HBS_PIT) return false;
  const start = Date.now();
  const end = start + 30 * 24 * 60 * 60 * 1000;
  const r = await fetch(
    `${BASE}/calendars/${id}/free-slots?startDate=${start}&endDate=${end}&timezone=America/New_York`,
    {
      headers: {
        Authorization: `Bearer ${process.env.HBS_PIT}`,
        Version: "2021-04-15",
        Accept: "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; HomePortraitBooking/1.0)"
      },
      signal: AbortSignal.timeout(4000)
    }
  );
  if (!r.ok) return false;
  const data = await r.json().catch(() => ({}));
  return Object.values(data).some(v => v && Array.isArray(v.slots) && v.slots.length > 0);
}

module.exports = async (req, res) => {
  const q = req.query || {};
  const division = String(q.d || "");
  const id = calendarFor(division, String(q.l || ""));
  let target = STUDIO_PAGE[division] || CONTACT_PAGE;
  try { if (await bookable(id)) target = WIDGET + id; } catch (e) { /* fall back */ }
  res.statusCode = 302;
  res.setHeader("Location", target);
  res.setHeader("Cache-Control", "no-store");
  res.end();
};
