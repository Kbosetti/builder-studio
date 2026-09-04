# Builder Studio / Mitchell Homes working notes

Operating notes for Claude sessions in this repo. Keep this current when IDs or hosting change.

## Accounts and IDs

- **Builder Studio (HighLevel) sub-account:** Mitchell Homes, location `5o5zLlUPPizy6Ajp61oF`. API base `https://services.leadconnectorhq.com`, header `Version: 2021-07-28`. Cloudflare rejects Python's default user agent (error 1010); always send a browser `User-Agent`.
- **Vercel:** team CEA Marketing `team_ruPVbZ5by79KqyoOnsn9JUZ8`.
  - Home Portrait quiz: project `mitchell-home-portrait-quiz` (`prj_TC3OD5qViQK3BPO6pn9lEPvUNre0`), custom domain **https://mitchellhomesliving.com** (www redirects to apex; `SITE_URL` env var set to it so emails link there), also https://mitchell-home-portrait-quiz-cea-marketing.vercel.app. Source in `home-portrait/`.
  - Design Dollars landing page: project `mitchell-design-dollars` (`prj_saPsC5WIH6Sc7f88JM4lzvmnnpfK`), live at https://mitchell-design-dollars.vercel.app/nhi-index. Source in `design-dollars/` (pulled from the deployment on September 4, 2026). Its own intake reads `GHL_PRIVATE_TOKEN` and `GHL_LOCATION_ID`.
  - Neither project is linked to git. Deploy with the CLI from the source folder; each folder has a `.vercel/project.json` (gitignored) pointing at the right project. If it is missing, write it by hand rather than running `vercel link`, which creates a new project named after the folder.
- **GHL media CDN:** `https://assets.cdn.filesafe.space/5o5zLlUPPizy6Ajp61oF/media/...`. URL maps in `assets/mitchell-home-portrait-image-urls.json`, `assets/portraits/uploaded.json`, `assets/portrait-boards/uploaded.json`.

## Credentials

Never commit tokens. Look for them in this order:

1. Environment variables `VERCEL_TOKEN`, `GHL_PIT` (set in the Claude Code environment settings so every session has them).
2. `/root/.config/cea/credentials.env` (local only, gitignored, disappears when the sandbox is reclaimed).
3. Ask the user. The GHL private integration token also lives in the Vercel project env var `HBS_PIT`.

## Common tasks

- **Deploy the Home Portrait site:** `cd home-portrait && vercel deploy --prod --yes --no-wait --scope team_ruPVbZ5by79KqyoOnsn9JUZ8 --token $VERCEL_TOKEN`. Use `--no-wait`; the sandbox proxy drops connections held open longer than about nine seconds, which also breaks `vercel login` (use a token instead). Verify by comparing MD5 of each served page with the source.
- **Upload to the GHL media library:** `scripts/upload_to_ghl.py <folder>` with `GHL_PIT` and `GHL_LOCATION_ID` set; reads `manifest.json`, writes `uploaded.json`.
- **Test the intake:** POST a quiz payload to `/api/lead` on the live site. Expect `contactId`, `noteAdded`, `emailQueued`, and `opportunityId` in the response.

## Home Portrait wiring (see home-portrait/SETUP-NOTES.md for field IDs and calendars)

- Quiz `portrait.html` posts to `api/lead.js`, which upserts the contact, writes 17 custom fields and tags, adds a note, sends the portrait email with the persona PDF from `home-portrait/pdf/`, and creates or updates the opportunity in the division pipeline (pipelines are named exactly like the divisions).
- Workflows are manual in HighLevel; triggers are the `home portrait quiz` tag plus `contact.nurture_track`, and `qualified lead` for the fast track.

## Git

Work on `claude/research-ghl-hbs-i8YQV` unless told otherwise. Commit with the user's identity (`Kelly Bosetti <kelly@ceamarketing.com>`).
