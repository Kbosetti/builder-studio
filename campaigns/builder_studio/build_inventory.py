#!/usr/bin/env python3
"""Everything CEA has put into Mitchell's Builder Studio account, on one page for Trevor.

usage: python3 campaigns/builder_studio/build_inventory.py      writes campaigns/builder_studio/out/inventory.html
Reads the records the other scripts keep: created.json (folder, templates, tags, trigger links), setup.json (what is
still to build), the email, event, sales and plan files for dates and audiences, the media maps, and
media_snapshot.json (the library files the fall work uses, listed from the account on October 9, 2026).
Rerun it after upload.py or setup.py so the page matches the account.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
ROOT = os.path.dirname(C)
OUT = f"{HERE}/out"
E = html.escape
AS_OF = "October 9, 2026"


def load(p):
    return json.load(open(p))


rec = load(f"{HERE}/created.json")
setup = load(f"{HERE}/setup.json")
emails = {e["id"].upper(): e for e in load(f"{C}/email/out/emails.json")["emails"]}
plan = {p["id"]: p for p in load(f"{C}/plan/plan.json")["pieces"]}
events = {e["id"].upper(): e for e in load(f"{C}/events/events.json")["events"]}
direct = {s["id"]: s for s in load(f"{C}/direct/direct.json")["sections"]}
sales = [f for f in direct["followups"]["items"] if f["body"].startswith("Subject:")]
snap = load(f"{HERE}/media_snapshot.json")["files"]

SERIES = {"portrait": "Home Portrait", "designdollars": "Design Dollars", "fourbuyers": "The Four Buyers",
          "partners": "Realtors and homeowners", "nurture": "Quiet-lead nurture", "homeowners": "My Mitchell Story"}


def short(text, n=150):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "..."


def batch_of(key):
    p = plan.get(key.lower())
    if p:
        return p["batch"], p["tier"]
    if key.startswith("HW"):
        return plan["hw"]["batch"], plan["hw"]["tier"]
    if key.startswith("NU"):
        return plan["nurture"]["batch"], plan["nurture"]["tier"]
    m = re.match(r"(E\d)", key)
    if m and m.group(1).lower() in plan:
        p = plan[m.group(1).lower()]
        return p["batch"], p["tier"]
    return None, None


def status_pill(batch, tier):
    if tier == "later":
        return '<span class="pill later">Saved for winter</span>'
    if batch:
        return f'<span class="pill b{batch}">Batch {batch}</span>'
    return '<span class="pill">Ready</span>'


# ---------------------------------------------------------------- email templates, grouped
groups = {}
for key, t in rec["templates"].items():
    if key in emails:
        e = emails[key]
        group = SERIES.get(e["series"], e.get("series_name", "Other"))
        when, aud = e["send"], e["segment"]
    elif key.startswith("SALES"):
        f = sales[int(key[5:]) - 1]
        group, when, aud = "Sales team follow-ups (personal)", f["meta"].split(" · ")[0], " · ".join(f["meta"].split(" · ")[1:])
    else:
        ev = events[key[:2]]
        group = "Event invitations and follow-ups (personal)"
        kind = "Invitation" if key.endswith("INVITE") else "Follow-up"
        when = (ev["invite_when"] if kind == "Invitation" else ev["followup_when"]).split(". ")[0]
        aud = f"{kind} for {ev['name']}"
    b, tier = batch_of(key)
    groups.setdefault(group, []).append((key, t, when, aud, b, tier))

ORDER = ["Design Dollars", "Home Portrait", "The Four Buyers", "Realtors and homeowners", "Quiet-lead nurture", "My Mitchell Story",
         "Sales team follow-ups (personal)", "Event invitations and follow-ups (personal)"]
tpl_html = []
for g in ORDER + [g for g in groups if g not in ORDER]:
    if g not in groups:
        continue
    rows = "".join(
        f'<tr><td class="mono">{E(k)}</td><td>{E(t["name"])}<div class="sub mono">id {E(t["id"])}</div></td>'
        f'<td>{E(short(w, 60))}</td><td>{E(short(a, 110))}</td><td>{status_pill(b, tier)}</td></tr>'
        for k, t, w, a, b, tier in groups[g])
    tpl_html.append(f'<h3>{E(g)} <span class="count">{len(groups[g])}</span></h3><div class="tw"><table><thead><tr><th>Key</th><th>Name in Builder Studio</th>'
                    f'<th>Planned send</th><th>Who gets it</th><th>Proofing</th></tr></thead><tbody>{rows}</tbody></table></div>')

# ---------------------------------------------------------------- tags
TAG_USE = {
    "fall26 quiet": "Workflow 04 adds it to leads who have not answered; it starts the 60-day quiet-lead nurture (workflow 05).",
    "fall26 engaged": "Workflow 01 adds it on any open or click and removes it after 90 days. Thursday Home Portrait emails go only to these contacts.",
    "fall26 clicked": "Workflow 02 adds it when someone clicks a Fall26 link, so a New Home Consultant follows up within one business day.",
    "fall26 nurture done": "Marks the end of the quiet-lead nurture, so nobody gets it twice.",
    "fall26 skip text this week": "Keeps the one-text-a-week rule when a lead already got a text.",
    "realtor land partner": "Agents who know land, for buyers still looking (realtor recruiting emails).",
    "realtor on your land": "Agents whose clients own land (realtor on-your-land emails).",
    "homeowner appreciation rsvp": "Workflow 00 adds it when a homeowner RSVPs to Homeowner Appreciation Night.",
    "my mitchell story entry": "Workflow 01 adds it when a contest entry arrives.",
    "my mitchell story verified": "Added by the contest coordinator after checking an entry; starts photo session booking (workflow 02).",
    "my mitchell story finalist": "Added after judging; sends the finalist note (workflow 03).",
}
tag_rows = []
for name, tid in rec["tags"].items():
    use = TAG_USE.get(name)
    if not use and name.startswith("event "):
        live = any(k for k in ("nov7", "oct29", "nov17", "nov18") if name.endswith(k))
        use = ("Workflow 06 adds it when someone RSVPs to this event." if live else "For a winter event that is banked; not used this fall.")
    tag_rows.append(f'<tr><td class="mono">{E(name)}</td><td>{E(use or "")}</td><td class="mono sub">{E(tid)}</td></tr>')

# ---------------------------------------------------------------- trigger links
link_rows = []
for name, l in rec["links"].items():
    ev = l.get("event")
    used = (f"RSVP button in the {ev.upper()} invitations" if ev else
            "the weekly text" if "SMS" in name else "the quiet-lead nurture texts" if "Nurture" in name else "")
    link_rows.append(f'<tr><td>{E(name)}</td><td class="mono">{E(l["field"])}</td><td class="url">{E(l["to"])}</td><td>{E(used)}</td></tr>')

# ---------------------------------------------------------------- custom fields (created September 4)
FIELDS = [("contact", "Region", "ah2CksVDEm8TzQzudEdS", "contact.region"), ("contact", "Home Intent", "DG3I7dBZIc8ZKkpmhrZk", "contact.home_intent"),
          ("contact", "Selection Appetite", "W7TwHOJi6GwmV6evGERl", "contact.selection_appetite"), ("contact", "Portrait Name", "ApGe8rxF3tu4VJ5AW58T", "contact.portrait_name"),
          ("contact", "Design Dollars Focus", "UkkJOBxiJk3DpZHralBW", "contact.design_dollars_focus"), ("opportunity", "Region", "uSnPQrmupBeVotpCqdOQ", "opportunity.region"),
          ("opportunity", "Home Intent", "xGOnZobp613pvo4aOLZc", "opportunity.home_intent"), ("opportunity", "Selection Appetite", "4CrQDEDiUxNrcLR6n4Ic", "opportunity.selection_appetite"),
          ("opportunity", "Portrait Name", "FbKWoNRebNSVYAEPtkKp", "opportunity.portrait_name")]
field_rows = "".join(f'<tr><td>{m}</td><td>{E(n)}</td><td class="mono">{E(k)}</td><td class="mono sub">{E(i)}</td></tr>' for m, n, i, k in FIELDS)
QUIZ_FIELDS = ["persona_segment", "portrait_name", "land_status", "division", "region", "home_intent", "style_preference", "must_have_spaces",
               "selection_appetite", "design_dollars_focus", "timeline", "qualified_lead_signal", "nurture_track", "ad_platform_event",
               "persona_scores", "quiz_submitted_at", "quiz_source", "county_of_interest"]

# ---------------------------------------------------------------- media library
ours = {}
for p, key in (("assets/portraits/uploaded.json", "Home Portrait story photos (September 3)"), ("assets/portrait-boards/uploaded.json", "Quiz paintings and portrait board photos (September 4)")):
    for f in load(f"{ROOT}/{p}"):
        ours[f["ghl_url"].rsplit("/", 1)[1]] = key
for u in load(f"{ROOT}/assets/mitchell-home-portrait-image-urls.json").values():
    ours.setdefault(u.rsplit("/", 1)[1], "Quiz paintings and portrait board photos (September 4)")
for v in load(f"{C}/email/gifs/gifs.json").values():
    if v.get("cdn"):
        ours[v["cdn"].rsplit("/", 1)[1]] = "Animated email heroes (one per designed email)"
for v in load(f"{C}/email/taglines/taglines.json").values():
    ours[v["cdn"].rsplit("/", 1)[1]] = "Email brand line, Charlotte (Yours, Dreams, Trust)"
for k, v in load(f"{C}/email/videos/videos.json").items():
    ours[v["cdn"].rsplit("/", 1)[1]] = "Video thumbnails for emails and the website"
    if v.get("poster_cdn"):
        ours[v["poster_cdn"].rsplit("/", 1)[1]] = "Reel posters and the corrected reels"
    if k.startswith("reel_"):
        ours[v["url"].rsplit("/", 1)[1]] = "Reel posters and the corrected reels"
media = {}
for f in snap:
    key = f["url"].rsplit("/", 1)[1]
    group = ours.get(key) or ("SimplyMitchell logo, hosted copy (September 30)" if f["name"].startswith("simply-mitchell") else "Other files our pages use (logos and page images)")
    media.setdefault(group, []).append(f)
MEDIA_ORDER = ["Animated email heroes (one per designed email)", "Email brand line, Charlotte (Yours, Dreams, Trust)", "Video thumbnails for emails and the website",
               "Reel posters and the corrected reels", "Quiz paintings and portrait board photos (September 4)", "Home Portrait story photos (September 3)",
               "SimplyMitchell logo, hosted copy (September 30)", "Other files our pages use (logos and page images)"]
media_html = []
for g in MEDIA_ORDER + [g for g in media if g not in MEDIA_ORDER]:
    if g not in media:
        continue
    items = "".join(f'<li><span class="mono">{E(f["name"])}</span> <span class="sub">{E(f["created"])} · {f["kb"]:,} KB</span></li>' for f in media[g])
    media_html.append(f'<details><summary>{E(g)} <span class="count">{len(media[g])}</span></summary><ul class="files">{items}</ul></details>')

# ---------------------------------------------------------------- still to build after approval
wf_rows = "".join(f'<tr><td>{E(w["name"])}</td><td>{E(short(w["trigger"], 120))}</td><td>{E(short(w["purpose"], 140))}</td></tr>' for w in setup["workflows"])
list_rows = "".join(f'<tr><td>{E(l["name"])}</td><td>{E(short("; ".join(l["filters"]), 170))}</td><td>{E(short(l.get("used_by", ""), 80))}</td></tr>' for l in setup["lists"])
send_rows = "".join(f'<tr><td>{E(s["when"])}</td><td>{E(s.get("time", ""))}</td><td>{E(s["template"])}</td><td>{E(short(s["to"], 90))}</td></tr>' for s in setup["sends"])
check_items = "".join(f"<li>{E(c)}</li>" for c in setup["checklist"])

n_media = len(snap)
counts = [("Email drafts", len(rec["templates"])), ("Tags", len(rec["tags"])), ("Trigger links", len(rec["links"])), ("Custom fields", len(FIELDS)), ("Media files in use", n_media)]
count_html = "".join(f'<div class="stat"><b>{n}</b><span>{E(l)}</span></div>' for l, n in counts)

page = open(f"{HERE}/inventory.html").read()
for k, v in {"%%ASOF%%": AS_OF, "%%COUNTS%%": count_html, "%%FOLDER%%": E(rec["folder"]["name"]), "%%TEMPLATES%%": "".join(tpl_html),
             "%%TAGS%%": "".join(tag_rows), "%%LINKS%%": "".join(link_rows), "%%FIELDS%%": field_rows,
             "%%QUIZFIELDS%%": ", ".join(f'<span class="mono">{f}</span>' for f in QUIZ_FIELDS), "%%MEDIA%%": "".join(media_html),
             "%%WORKFLOWS%%": wf_rows, "%%LISTS%%": list_rows, "%%SENDS%%": send_rows, "%%CHECK%%": check_items,
             "%%NWF%%": str(len(setup["workflows"])), "%%NLISTS%%": str(len(setup["lists"])), "%%NSENDS%%": str(len(setup["sends"])),
             "%%NTPL%%": str(len(rec["templates"])), "%%NTAGS%%": str(len(rec["tags"])), "%%NLINKS%%": str(len(rec["links"])), "%%NMEDIA%%": str(n_media)}.items():
    page = page.replace(k, v)
if re.search(r"[–—]", page):
    raise SystemExit("dash found")
for banned in ("HighLevel", "GoHighLevel", "CEA Marketing Group", "FACTS.md"):
    if banned in page:
        raise SystemExit(f"page contains {banned!r}")
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/inventory.html", "w").write(page)
print("inventory.html", len(page) // 1024, "KB;", ", ".join(f"{n} {l.lower()}" for l, n in counts))
