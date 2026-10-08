# Approval page spec

`build_approval.py` reads one JSON file. Paths to images are relative to the spec file (or absolute). Every string is shown to the client as written, so write it as client-facing copy.

Copy rules: use grammatical hyphens in compound modifiers (a 90-second quiz, a follow-up email); em and en dashes stay banned, and the build stops on them.

## Top level

| Key | Required | What it is |
|---|---|---|
| `slug` | yes | Short id, used for the browser storage key, e.g. `mitchell-fall-2026` |
| `page_title` | yes | Browser tab and gallery name, e.g. `Mitchell Fall Plan Approval` |
| `client` | yes | Client name as the client writes it |
| `prepared_by` | no | Defaults to `CEA Marketing` |
| `date_line` | yes | e.g. `October 2026` |
| `brand` | yes | Colors and type, see below |
| `cover` | yes | `eyebrow`, `title_before`, `script_word` (optional), `title_after`, `intro` |
| `glance` | no | At a glance section, see below |
| `sections` | yes | Ordered list of sections, each holding approval items |
| `questions` | no | Ordered list of `{title, text}` |
| `signoff` | no | `{title, text}`; defaults to sending the summary to Kelly |
| `footer` | no | One line |
| `banned` | no | Phrases the build refuses to ship (add the client brand's banned terms) |

## brand

```json
{"primary": "#2b6d47", "deep": "#1e4f33", "accent": "#f5d053", "paper": "#faf8f3",
 "font": "Montserrat", "script_font": "fonts/charlotte.woff2", "logo_white": "img/logo-white.png"}
```
`primary` drives buttons and labels, `deep` the cover and sign-off band, `accent` the highlight (numbers, progress, the script word), `paper` the page ground. `font` must be a Google Fonts family. `script_font` (a local .woff2) is optional and styles only `cover.script_word`. Dark mode colors are derived automatically.

## glance

```json
{"eyebrow": "At a glance", "title": "Three campaigns, every channel that carries them", "lede": "...",
 "cards": [{"stage": "Decide · live now", "title": "Mitchell Design Dollars", "text": "...", "to": "Sends people to ..."}],
 "matrix": {"columns": ["Design Dollars", "Home Portrait", "Four Buyers"], "rows": [["Email", true, true, true], ["Print", true, true, false]]},
 "weeks": [{"label": "Week of October 12", "lines": ["Email: DD1 It is your land", "5 social posts"]}],
 "more": {"title": "Our recommended order", "items": [{"title": "...", "meta": "...", "text": "..."}]}}
```

## sections and items

```json
{"id": "emails", "eyebrow": "Email", "title": "Seventeen emails to the database", "lede": "...",
 "items": [
   {"title": "Design Dollars emails (4)", "when": "October 13 to 29 · full list", "why": "One sentence.",
    "blocks": [
      {"type": "gallery", "tall": true, "images": [
         {"src": "shots/dd1.jpg", "title": "It is your land. Make it your home.", "lines": ["Every Mitchell home now comes with ...", "DD1 · Tuesday, October 13 · Full list"], "waiting": 0}]},
      {"type": "posts", "show_first": 8, "posts": [
         {"title": "s01 · Reel", "meta": "Monday, October 12 · Instagram, Facebook", "body": "Exact caption", "link": "https://...", "waiting": 5}]},
      {"type": "text", "paragraphs": ["..."], "bullets": ["..."]}
    ]}
 ]}
```
Items are numbered A1, A2 ... across the whole page in order. `gallery` shows clickable images (`tall` crops the thumbnail to the top 300 px, right for emails and long pages). `posts` shows collapsible rows with the exact words; `show_first` hides the rest behind a Show all button. `waiting` is a question number (1-based) or 0.

## questions

```json
[{"title": "November reserve-by date", "text": "The reserve-by date rolls monthly. Which date should November pieces use? We suggest November 30, 2026."}]
```

## Example

The Mitchell fall plan (October 2026) is the reference build: sixteen items across email, website, social and search, texts and the sales team, print and events, and sixteen questions. Its source lives in the Mitchell repo at `campaigns/approval/`.
