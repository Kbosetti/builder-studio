#!/usr/bin/env python3
"""The fall events in one place: each event's write-up and every piece of its copy, plus My Mitchell Story.

usage: python3 campaigns/events/build_events_page.py      writes campaigns/events/out/index.html and out/img/*.jpg
Reads campaigns/events/events.json, campaigns/homeowners/contest.json, the plain-text email renders in
campaigns/email/out/ and the email previews in campaigns/email/previews/. Rerun after make_events.py,
make_contest.py or build.py so the page matches the sources.
"""
import html, json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
OUT = f"{HERE}/out"
E = html.escape

ev = json.load(open(f"{HERE}/events.json"))
ct = json.load(open(f"{C}/homeowners/contest.json"))
emails = {e["id"]: e for e in json.load(open(f"{C}/email/out/emails.json"))["emails"]}
EVENTS = {e["id"]: e for e in ev["events"]}
FALL = ["e2", "e1", "e7", "e6"]          # in date order
WINTER = ["e3", "e4", "e5"]
os.makedirs(f"{OUT}/img", exist_ok=True)
files = []


def clean(text):
    """Drop internal file references so the page reads cleanly for Mitchell."""
    text = re.sub(r"\s*\([^()]*(campaigns/|\.json|\.md)[^()]*\)", "", text or "")
    text = re.sub(r"[^.]*(campaigns/|\.json\b|events\.md)[^.]*\.\s*", "", text)
    return text.strip()


def para(text):
    return "".join(f"<p>{E(clean(p))}</p>" for p in (text or "").split("\n\n") if p.strip())


def ul(items):
    items = [clean(i) for i in items if i and clean(i)]
    return "<ul>" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>" if items else ""


def copyblock(label, meta, body, notes=""):
    body = clean(body)
    if not body:
        return ""
    return (f'<div class="piece"><div class="ph"><div><b>{E(label)}</b>{f"<span>{E(clean(meta))}</span>" if meta else ""}</div>'
            f'<button type="button" class="cp">Copy</button></div><pre>{E(body)}</pre>'
            + (f'<p class="pn">{E(clean(notes))}</p>' if notes and clean(notes) else "") + "</div>")


def preview(eid, caption):
    src = f"{C}/email/previews/{eid}.jpg"
    if not os.path.exists(src):
        return ""
    shutil.copy(src, f"{OUT}/img/{eid}.jpg")
    files.append(f"img/{eid}.jpg")
    return f'<figure class="shot"><img src="img/{eid}.jpg" alt="{E(caption)}" loading="lazy"><figcaption>{E(caption)}</figcaption></figure>'


def block_text(b):
    parts = [b.get("head", ""), b.get("text", "")]
    if b.get("cta"):
        parts.append(f"Button: {b['cta']} ({b.get('link', '')})")
    if b.get("fine"):
        parts.append(b["fine"])
    return "\n\n".join(p for p in parts if p)


def event_section(e, winter=False):
    eid = e["id"]
    head = (f'<section class="event" id="{eid}"><header class="eh"><span class="tag {"w" if winter else "f"}">{"Saved for winter" if winter else "This fall"}</span>'
            f'<h2>{E(e["name"])}</h2><dl class="facts"><div><dt>When</dt><dd>{E(e["date"])}{(", " + E(e["time"])) if e.get("time") else ""}</dd></div>'
            f'<div><dt>Where</dt><dd>{E(clean(e["where"]))}</dd></div><div><dt>Who it is for</dt><dd>{E(clean(e["audience"]))}</dd></div></dl></header>')
    write = (f'<div class="write"><div><h3>What happens</h3>{ul(e.get("what", []))}</div>'
             f'<div><h3>Why we are doing it</h3>{para(e.get("why", ""))}</div>'
             f'<div><h3>What Mitchell needs to confirm</h3>{ul(e.get("confirm", []))}</div>'
             + (f'<div><h3>Good to know</h3>{ul(e.get("notes", []))}</div>' if e.get("notes") else "") + "</div>")
    pieces = []
    shots = []
    for r in e.get("rides_in", []):
        em = emails.get(r["email"], {})
        pieces.append(copyblock(f"Invitation inside the {r['email'].upper()} email", f"{r['send']} · {em.get('subject', '')}", block_text(r["block"]), r.get("placement", "")))
        shots.append(preview(r["email"], f"{r['email'].upper()}: {em.get('subject', '')} ({r['send']})"))
    if e.get("own_email") and e["own_email"] in emails:
        o = e["own_email"]
        txt = open(f"{C}/email/out/{o}.txt").read()
        pieces.append(copyblock(f"Invitation email {o.upper()}", f"{emails[o]['send']} · Subject: {emails[o]['subject']}", txt))
        shots.append(preview(o, f"{o.upper()}: {emails[o]['subject']} ({emails[o]['send']})"))
    if e.get("invite_text"):
        pieces.append(copyblock("Consultant invitation text", e.get("invite_when", ""), e["invite_text"]))
    if e.get("invite_email"):
        pieces.append(copyblock("Consultant invitation email", f"Subject: {e['invite_email']['subject']}", e["invite_email"]["body"]))
    for i, s in enumerate(e.get("social", []), 1):
        pieces.append(copyblock(f"Social post {i}", f"{s.get('date', '')} · {s.get('channels', '')}", s["body"], s.get("notes", "")))
    if e.get("facebook_event"):
        pieces.append(copyblock("Facebook event", "One per Design Center", e["facebook_event"], e.get("facebook_event_notes", "")))
    if e.get("gbp"):
        pieces.append(copyblock("Google Business Profile event post", e["gbp"].get("title", ""), e["gbp"].get("body", ""), e["gbp"].get("notes", "")))
    if e.get("nextdoor"):
        pieces.append(copyblock("Nextdoor", e.get("nextdoor_when", ""), e["nextdoor"]))
    if e.get("reminder_text"):
        pieces.append(copyblock("RSVP reminder text", e.get("reminder_when", ""), e["reminder_text"]))
    if e.get("thanks_text"):
        pieces.append(copyblock("Same-day thank-you text", e.get("thanks_when", ""), e["thanks_text"]))
    if e.get("followup_email"):
        pieces.append(copyblock("Next-day follow-up email", f"{e.get('followup_when', '')} · Subject: {e['followup_email']['subject']}", e["followup_email"]["body"]))
    for x in e.get("extra_texts", []):
        pieces.append(copyblock("Extra text", f"{x.get('date', '')} · {x.get('audience', '')}", x["body"]))
    sched = e.get("schedule", [])
    sched_html = ("<details><summary>Every touch, by date</summary><ul class='sched'>" + "".join(
        f"<li><b>{E(s['day'])}</b> · {E(s['channel'])} · {E(clean(s['what']))}{(' · ' + E(s['who'])) if s.get('who') else ''}</li>" for s in sched) + "</ul></details>") if sched else ""
    shots = "".join(x for x in shots if x)
    return (head + write + (f'<div class="shots">{shots}</div>' if shots else "")
            + f'<details class="copy"{" open" if not winter else ""}><summary>The copy ({len([p for p in pieces if p])} pieces)</summary><div class="pieces">{"".join(pieces)}</div></details>'
            + sched_html + "</section>")


# ---------------------------------------------------------------- My Mitchell Story
def contest_section():
    ems = [e for e in ct["emails"] if e["id"] in emails]
    shots = "".join(preview(e["id"], f"{e['id'].upper()}: {emails[e['id']]['subject']} ({emails[e['id']]['send']})") for e in ems)
    how = "<ol>" + "".join(f"<li>{E(clean(h if isinstance(h, str) else h.get('text', h.get('step', ''))))}</li>" for h in ct["how_it_works"]) + "</ol>"
    prizes = "<ul>" + "".join(f"<li><b>{E(p['tier'])}:</b> {E(clean(p['what']))}</li>" for p in ct["prizes"]) + "</ul>"
    timeline = "<ul class='sched'>" + "".join(f"<li><b>{E(t['date'])}</b> · {E(clean(t['what']))}</li>" for t in ct["timeline"]) + "</ul>"
    judging = "<ul>" + "".join(f"<li><b>{E(j['criterion'])} ({E(j['weight'])}):</b> {E(j['what'])}</li>" for j in ct["judging"] if isinstance(j, dict)) + "</ul>"
    qs = "<ul>" + "".join(f"<li><b>{E(q['topic'])}:</b> {E(q['question'])}{(' <i>Our recommendation: ' + E(q['recommend']) + '</i>') if q.get('recommend') else ''}</li>" for q in ct["questions"]) + "</ul>"
    pieces = []
    for e in ems:
        o = e["id"]
        pieces.append(copyblock(f"Email {o.upper()}", f"{emails[o]['send']} · Subject: {emails[o]['subject']}", open(f"{C}/email/out/{o}.txt").read()))
    for w in ct["workflow_emails"]:
        if os.path.exists(f"{C}/email/out/{w['id']}.txt"):
            pieces.append(copyblock(f"Automatic note {w['id'].upper()}", w.get("send", ""), open(f"{C}/email/out/{w['id']}.txt").read()))
    for t in ct["texts"]:
        pieces.append(copyblock(f"Text: {t['title']}", t.get("when", "").split(". ")[0], t["body"], "To: " + t.get("to", "")))
    for s in ct["sales"]:
        pieces.append(copyblock(f"Script: {s['title']}", s.get("when", ""), s["body"]))
    for s in ct["social"]:
        pieces.append(copyblock(f"Post: {s['title']}", f"{s.get('date', '')} · {s.get('channels', '')}", s["body"], (s.get("format", "") + " " + s.get("notes", "")).strip()))
    g = ct["gbp"]
    pieces.append(copyblock(f"Google Business Profile post: {g.get('title', '')}", g.get("post_on", ""), g.get("body", ""), g.get("notes", "")))
    tips = ul(ct["filming_tips"])
    return (f'<section class="event home" id="story"><header class="eh"><span class="tag h">Brittany\'s idea · Homeowners</span><h2>My Mitchell Story</h2>'
            f'<p class="line">{E(ct["line"])} {E(ct["hashtag"])}</p>{para(" ".join(ct["summary"]) if isinstance(ct["summary"], list) else ct["summary"])}</header>'
            f'<div class="write"><div><h3>How it works</h3>{how}</div><div><h3>The four questions homeowners answer</h3>{ul(ct["prompts"])}</div>'
            f'<div><h3>What homeowners receive (proposal)</h3>{prizes}</div><div><h3>Judging</h3>{judging}</div>'
            f'<div><h3>Filming tips we give homeowners</h3>{tips}</div><div><h3>Questions for Mitchell</h3>{qs}</div></div>'
            f'<details><summary>The dates</summary>{timeline}</details>'
            f'<div class="shots">{shots}</div>'
            f'<details class="copy" open><summary>The copy ({len(pieces)} pieces)</summary><div class="pieces">{"".join(pieces)}</div></details></section>')


def row(e, winter=False):
    return (f'<tr><td><a href="#{e["id"]}">{E(e["name"])}</a></td><td>{E(e["date"])}</td><td>{E(e.get("time", ""))}</td>'
            f'<td>{E(clean(e["audience"]).split(".")[0])}</td><td><span class="tag {"w" if winter else "f"}">{"Saved for winter" if winter else "This fall"}</span></td></tr>')


glance = ("<div class='tw'><table><thead><tr><th>Event</th><th>Date</th><th>Time</th><th>For</th><th>Status</th></tr></thead><tbody>"
          + "".join(row(EVENTS[i]) for i in FALL)
          + f'<tr><td><a href="#story">My Mitchell Story (homeowner contest)</a></td><td>November 17 to December 18, 2026</td><td>Kicks off at Homeowner Appreciation Night</td><td>Past Mitchell homeowners</td><td><span class="tag h">Brittany\'s idea</span></td></tr>'
          + "".join(row(EVENTS[i], True) for i in WINTER) + "</tbody></table></div>")
studios = "<ul class='studios'>" + "".join(f"<li><b>{E(s['studio'])}</b><span>{E(s['address'])}</span><span>{E(s['phone'])}</span></li>" for s in ev["studios"]) + "</ul>"
body = ("".join(event_section(EVENTS[i]) for i in FALL[:2]) + event_section(EVENTS["e7"]) + contest_section() + event_section(EVENTS["e6"])
        + '<h2 class="divider" id="winter">Saved for winter</h2><p class="lede">Finished and ready, with dates set when Mitchell schedules them.</p>'
        + "".join(event_section(EVENTS[i], True) for i in WINTER))
nav = " ".join(f'<a href="#{i}">{E(EVENTS[i]["name"].split(":")[0])}</a>' for i in FALL[:3]) + ' <a href="#story">My Mitchell Story</a> ' + f'<a href="#e6">{E(EVENTS["e6"]["name"])}</a> <a href="#winter">Saved for winter</a>'

page = open(f"{HERE}/events_page.html").read()
for k, v in {"%%GLANCE%%": glance, "%%STUDIOS%%": studios, "%%BODY%%": body, "%%NAV%%": nav}.items():
    page = page.replace(k, v)
if re.search(r"[–—]", page):
    raise SystemExit("dash found")
for banned in ("HighLevel", "CEA Marketing Group", "campaigns/", ".json", "FACTS.md"):
    if banned in page:
        raise SystemExit(f"page contains {banned!r}: ...{page[max(0, page.find(banned) - 120):page.find(banned) + 60]}")
open(f"{OUT}/index.html", "w").write(page)
json.dump(files, open(f"{OUT}/files.json", "w"), indent=0)
print("index.html", len(page) // 1024, "KB;", len(files), "email previews")
