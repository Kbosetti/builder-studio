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

## How the September 4 deploy was made

The Claude session could not push files straight to Vercel, so the production deployment used a small build step: `package.json` runs `node build.js`, which downloads `portrait.html`, `fullportrait.html`, and `dashboard.html` from the Mitchell media library, verifies each MD5 against the committed source, and writes them to `public/` for Vercel to serve. `api/lead.js`, `vercel.json`, and `index.html` were sent inline.

To redeploy from a machine the normal way, run `vercel --prod` from this folder. The clean source here (no `build.js`) is the right thing to deploy; Vercel will serve the files from the root as before.

## Still manual

### 1. Vercel environment variables (needed before any lead lands)

Vercel dashboard, project `mitchell-home-portrait-quiz`, Settings, Environment Variables, Production:

- `HBS_PIT` = the Mitchell Homes private integration token
- `HBS_LOCATION_ID` = `5o5zLlUPPizy6Ajp61oF`
- optional `EMAIL_PROVIDER=gmail`, `GMAIL_USER`, `GMAIL_APP_PASSWORD` to send from Gmail instead of the platform

Redeploy after saving (Deployments, latest, Redeploy). Until then `api/lead.js` returns `skipped: integration not configured`.

### 2. Portrait PDFs

`api/lead.js` expects nine shells: `landownerhasland`, `landownerneedsland`, `plannerhasland`, `plannerneedsland`, `familyhasland`, `familyneedsland`, `dreamerhasland`, `dreamerneedsland`, `gatheringplace`.
Host each in the Mitchell media library and paste the CDN URL into `PDF_URLS` in `api/lead.js`. The email links and attaches the document only when the URL answers a HEAD request.

### 3. Workflows (no API for these, build in Automation)

Every quiz contact arrives with tag `home portrait quiz`, a persona tag, and `contact.nurture_track` set to one of:

- `the_planner_sequence`
- `the_transitioner_sequence`
- `the_value_unlocker_sequence`
- `the_grounded_dreamer_sequence`
- `the_gathering_place_sequence`

Build one workflow per value, trigger: Contact Tag Added `home portrait quiz` with filter `nurture_track` equals the value.

Qualified lead fast track: trigger on tag `qualified lead` (set when the buyer owns or has family land and the timeline is 0 to 12 months). `contact.qualified_lead_signal` is also `true`. Route to the division pipeline owner, SMS the OSC, and move the opportunity to Contacted once the call is logged.

Useful fields for merge and filters: `contact.portrait_name`, `contact.division`, `contact.region`, `contact.home_intent`, `contact.design_dollars_focus`, `contact.selection_appetite`.
