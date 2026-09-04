# Mitchell Home Portrait, September 2026 deploy notes

Source of the production deployment on Vercel, project `mitchell-home-portrait-quiz`, team `cea-marketing`.
Live at https://mitchellhomesliving.com (custom domain assigned September 4, 2026; www redirects to the apex; `SITE_URL` env var points emails there). Vercel address https://mitchell-home-portrait-quiz-cea-marketing.vercel.app still works.

## Done on September 4, 2026

- 24 new images hosted in the Mitchell Homes media library (location `5o5zLlUPPizy6Ajp61oF`). Full map in `../assets/mitchell-home-portrait-image-urls.json`.
- `fullportrait.html`: lake region set uses the new lake painting. Each of the five persona boards now has its own photo set. Closing slide has a real "Schedule my Design Studio visit" button.
- `portrait.html`: lake painting on the result card for lake regions. "Visit a Design Studio" opens the division's Design Studio Visit calendar (With Land or No Land, chosen from the land answer). Pitch room panel and prototype footer removed.
- `api/lead.js`: the four September opportunity fields are wired. Hosted PDF map added (`PDF_URLS`).
- Builder Studio custom fields created:

| Model | Field | ID | Key |
|---|---|---|---|
| contact | Region | ah2CksVDEm8TzQzudEdS | contact.region |
| contact | Home Intent | DG3I7dBZIc8ZKkpmhrZk | contact.home_intent |
| contact | Selection Appetite | W7TwHOJi6GwmV6evGERl | contact.selection_appetite |
| contact | Portrait Name | ApGe8rxF3tu4VJ5AW58T | contact.portrait_name |
| contact | Design Dollars Focus | UkkJOBxiJk3DpZHralBW | contact.design_dollars_focus |
| opportunity | Region | uSnPQrmupBeVotpCqdOQ | opportunity.region |
| opportunity | Home Intent | xGOnZobp613pvo4aOLZc | opportunity.home_intent |
| opportunity | Selection Appetite | 4CrQDEDiUxNrcLR6n4Ic | opportunity.selection_appetite |
| opportunity | Portrait Name | FbKWoNRebNSVYAEPtkKp | opportunity.portrait_name |

## Scheduling calendars used

Booking URL pattern: `https://api.leadconnectorhq.com/widget/booking/<calendarId>`

| Division | Design Studio Visit With Land | Design Studio Visit No Land |
|---|---|---|
| Richmond, VA | lefHeBcANsbjZf5IhZGw | LSDaGxShOPqb9J1t4SCO |
| Fredericksburg, VA | 46oGCWfZJoFwbuub1wtV | fkAfa07N4rovoVR0iZMt |
| Newport News, VA | 4bOw8XC3FS9aBi1lxCaJ | yHaSZPNP24gcGJkY6MoP |
| Raleigh, NC | e7IJYU4ZVbxtsf3RZpbP | ET1aeQY6CmEOXUEZEMZa |
| Wilmington, NC | dEtDNPpoKNnBTY7Sw2Y9 | nf3cLjxsG069HUeNCWkU |

## Deploying

`vercel deploy --prod --yes --no-wait` from this folder, with `VERCEL_TOKEN` set. `.vercel/project.json` (gitignored) must point at project `prj_TC3OD5qViQK3BPO6pn9lEPvUNre0`; write it by hand if missing. Verify by comparing the MD5 of each served page with the source.

## Done later on September 4

- `HBS_PIT`, `HBS_LOCATION_ID`, and `SITE_URL` are set on the Vercel project. Leads flow into Builder Studio and the portrait email sends through the platform (verified: contact, note, opportunity, delivered email with the PDF attached).
- All nine portrait PDFs are hosted at `/pdf/<shell>.pdf` on the site. `PDF_URLS` in `api/lead.js` stays empty; the fallback path serves them.
- Simply Mitchell wordmark replaces the script label on the quiz card and portrait slide; PDFs carry it inline.
- Montserrat and Charlotte are self-hosted under `/fonts/`; PDF script lines were reset in Charlotte.
- Custom domain `mitchellhomesliving.com` assigned (www redirects to apex).

## Still manual

### Workflows (no API for these, build in Automation)

Every quiz contact arrives with tag `home portrait quiz`, a persona tag, and `contact.nurture_track` set to one of:

- `the_planner_sequence`
- `the_transitioner_sequence`
- `the_value_unlocker_sequence`
- `the_grounded_dreamer_sequence`
- `the_gathering_place_sequence`

Build one workflow per value, trigger: Contact Tag Added `home portrait quiz` with filter `nurture_track` equals the value.

Qualified lead fast track: trigger on tag `qualified lead` (set when the buyer owns or has family land and the timeline is 0 to 12 months). `contact.qualified_lead_signal` is also `true`. Route to the division pipeline owner, SMS the OSC, and move the opportunity to Contacted once the call is logged.

Useful fields for merge and filters: `contact.portrait_name`, `contact.division`, `contact.region`, `contact.home_intent`, `contact.design_dollars_focus`, `contact.selection_appetite`.

### Sending domain

Portrait emails currently go out from HighLevel's default `reply@ec1.msgsndr.org`. Add a dedicated sending domain under Settings, Email Services in the Mitchell sub-account so they come from a Mitchell address.
