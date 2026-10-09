#!/usr/bin/env python3
"""Build the fall cadence page: every email, text, post, profile post and sales touch on one calendar.

usage: python3 campaigns/kit/build_kit.py && python3 campaigns/cadence/build_cadence.py
Reads the same sources as the kit (email/out/emails.json, direct/direct.json, traffic/organic.json) and
writes campaigns/cadence/out/index.html, its email preview images, and files.json. Public copy:
python3 campaigns/cadence/deploy.py (mitchell-fall-cadence.vercel.app).
"""
import json, os, re, shutil
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
OUT = f"{HERE}/out"
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(f"{OUT}/email")
files = []
MONTHS = {"October": 10, "November": 11}
START, WEEKS = date(2026, 10, 19), 6


def when(text):
    m = re.search(r"(October|November) (\d{1,2})", text or "")
    return date(2026, MONTHS[m.group(1)], int(m.group(2))) if m else None


def campaign(*texts):
    t = " ".join(x or "" for x in texts)
    if re.search(r"Design Dollars|reserve.by|ladder", t, re.I) and not re.search(r"Home Portrait|Four Buyers", t):
        return "dd"
    if re.search(r"Home Portrait|portrait|quiz", t, re.I) and not re.search(r"Four Buyers", t):
        return "hp"
    if re.search(r"Four Buyers|landowner|your land|own land|construction loan|folder|no land|looking for land", t, re.I):
        return "fb"
    if re.search(r"realtor|homeowner|partner", t, re.I):
        return "ref"
    return "all"


def clean(n):
    n = n or ""
    n = n.replace("Downey quote verbatim from FACTS.md.", "Downey quote word for word.")
    n = n.replace("which FACTS.md does not allow", "which the approved pricing line does not allow")
    n = n.replace("Ladder figures from FACTS.md.", "Ladder figures exactly as approved.")
    n = n.replace("Attach the two episode links from FACTS.md.", "Attach two Behind the Build episode links.")
    return n.replace("FACTS.md", "the approved wording")


def hold(*texts):
    return any(re.search(r"\bhold\b", t or "", re.I) for t in texts)


ev = []
em = json.load(open(f"{C}/email/out/emails.json"))
for e in em["emails"]:
    shutil.copy(f"{C}/kit/out/email/{e['id']}.jpg", f"{OUT}/email/{e['id']}.jpg")
    files.append(f"email/{e['id']}.jpg")
    camp = {"designdollars": "dd", "portrait": "hp", "fourbuyers": "fb", "partners": "ref", "nurture": "all", "homeowners": "ref"}[e["series"]]
    ev.append({"d": when(e["send"]), "ch": "Email", "camp": camp, "title": e["subject"], "aud": e["segment"], "who": "Marketing",
               "body": "Preview text: " + e["preview"], "img": f"email/{e['id']}.jpg", "hold": e["hold"], "tag": e["id"].upper()})

dr = {s["id"]: s for s in json.load(open(f"{C}/direct/direct.json"))["sections"]}
for i in dr["sms"]["items"]:
    ev.append({"d": when(i["meta"]), "ch": "Text", "camp": campaign(i["title"]), "title": i["title"].split(" · ", 1)[1], "aud": "Contacts with text consent who did not open Tuesday's email",
               "who": "Marketing", "body": i["body"], "link": i.get("link", ""), "notes": clean(i.get("notes", "")), "hold": ""})
for i in dr["followups"]["items"]:
    d = when(i["meta"])
    if d:
        meta = i["meta"].split(" · ")
        camp = {"Bring your photos: text": "fb", "Old-lead check-in: text and email": "hp", "Realtor follow-up email": "ref"}.get(i["title"]) or campaign(i["title"], i["body"])
        ev.append({"d": d, "ch": "Sales team", "camp": camp, "title": i["title"], "aud": meta[1] if len(meta) > 1 else "",
                   "who": "New Home Consultants", "body": i["body"], "notes": clean(i.get("notes", "")), "hold": "Waits on question 11" if "question 11" in i.get("notes", "") else ""})
# the weekly Friday call list and the Thursday first touch for the quiz launch
first = [x for x in dr["sales"]["items"] if x["title"].startswith("Text to a cold")][0]
ev.append({"d": date(2026, 10, 22), "ch": "Sales team", "camp": "hp", "title": "Share the Home Portrait with your leads", "aud": "Every New Home Consultant to their cold or stalled leads",
           "who": "New Home Consultants", "body": first["body"], "notes": "The personal side of the first Home Portrait email the same day.", "hold": ""})
land = [x for x in dr["followups"]["items"] if x["title"].startswith("Clicked a Four Buyers")][0]
ev.append({"d": date(2026, 11, 5), "ch": "Sales team", "camp": "fb", "title": "Landowners: personal text to active leads", "aud": "Every New Home Consultant to active leads who own land, with text consent",
           "who": "New Home Consultants", "body": land["body"], "notes": "The personal side of the landowner emails that week.", "hold": ""})
for w in range(WEEKS):
    fri = START + timedelta(days=7 * w + 4)
    ev.append({"d": fri, "ch": "Sales team", "camp": "all", "title": "Friday call list", "aud": "Everyone who clicked an email, opened a text link or visited a campaign page this week and has not booked",
               "who": "Online sales counselors and New Home Consultants", "body": "Call first, then text if there is no answer. Use the follow-up script that matches what they looked at: Design Dollars, the Home Portrait, or their land.", "hold": ""})

org = {s["id"]: s for s in json.load(open(f"{C}/traffic/organic.json"))["sections"]}
for i in org["social"]["items"]:
    if i.get("tier") == "later":
        continue
    d = when(i["meta"])
    if not d or not re.match(r"\w+day, ", i["meta"]):
        continue
    parts = i["meta"].split(" · ")
    fmt = i["title"].split(" · ")[-1].split(",")[0]
    line = i["body"].strip().split("\n")[0]
    if line.startswith("Frame 1:"):
        fmt, line = "Story", line[len("Frame 1:"):].strip()
    first = re.split(r"(?<=[.?!])\s", line)[0]
    ev.append({"d": d, "ch": "Social", "camp": campaign(i["title"]), "title": f"{fmt}: {first}", "aud": parts[1] if len(parts) > 1 else "",
               "who": "Marketing", "body": i["body"], "link": i.get("link", ""), "notes": clean(i.get("notes", "")), "hold": "Hold" if hold(i.get("notes", ""), i["title"]) else ""})
groups = {}
for i in org["gbp"]["items"]:
    d = when(i["meta"])
    if not d:
        continue
    studio, kind = i["title"].split(": ", 1)
    kind = re.sub(r"\s*\(.*\)$", "", kind).replace(" post", "")
    g = groups.setdefault((d, kind), {"parts": [], "held": [], "camp": campaign(i["title"])})
    g["parts"].append(f"{studio.upper()}\n{i['body']}")
    if hold(i.get("notes", "")):
        g["held"].append(studio.split(" (")[0])
for (d, kind), g in groups.items():
    ev.append({"d": d, "ch": "Google", "camp": g["camp"], "title": f"{kind}, all five Design Centers", "aud": "Google Business Profile for each Design Center",
               "who": "Marketing", "body": "\n\n".join(g["parts"]),
               "notes": ("On hold for " + " and ".join(g["held"]) + " until the Dreamer pages are fixed; the others can go now.") if g["held"] else "",
               "hold": "Hold" if g["held"] else ""})
for i in org["community"]["items"] + org["youtube"]["items"]:
    if i.get("tier") == "later":
        continue
    d = when(i["meta"])
    if d and re.match(r"(October|November) \d", i["meta"]):
        ch = "Nextdoor" if "Nextdoor" in i["title"] else "YouTube"
        ev.append({"d": d, "ch": ch, "camp": campaign(i["title"], i["body"]), "title": i["title"], "aud": i["meta"].split(" · ")[1] if " · " in i["meta"] else "",
                   "who": "Marketing", "body": i["body"], "link": i.get("link", ""), "notes": clean(i.get("notes", "")), "hold": ""})
# one time setup on day one
setup = [("Website pop-up, announcement bar and thank-you pages", "Website vendor and marketing"),
         ("Listing portal profiles and the Design Dollars snippet", "Marketing"), ("Print the counter cards", "Design Centers"),
         ("Missed-call text-back with the quiz link", "Marketing"), ("Email signature line or banner for everyone at Mitchell", "Everyone")]
for t, who in setup:
    ev.append({"d": START, "ch": "Setup", "camp": "all", "title": t, "aud": "One time, the first week", "who": who, "body": "Everything for this is in the approval document and the traffic kit.", "hold": ""})

ep = f"{C}/events/events.json"
if os.path.exists(ep):
    # (event day, consultant invites, RSVP reminder); e3, e4 and e5 are banked for winter
    SCHED = {"e2": (date(2026, 10, 29), date(2026, 10, 26), date(2026, 10, 28)), "e1": (date(2026, 11, 7), date(2026, 11, 2), date(2026, 11, 6)),
             "e7": (date(2026, 11, 17), date(2026, 11, 5), date(2026, 11, 16)), "e6": (date(2026, 11, 18), date(2026, 11, 11), date(2026, 11, 17))}
    camp_of = {"e1": "dd", "e2": "dd", "e3": "fb", "e4": "all", "e5": "hp", "e6": "ref", "e7": "ref"}
    for e in json.load(open(ep))["events"]:
        if e.get("tier") == "later" or e["id"] not in SCHED:
            continue
        day, inv, rem = SCHED.get(e["id"], (None, None, None))
        cp = camp_of.get(e["id"], "all")
        ev.append({"d": day, "ch": "Event", "camp": cp, "title": e["name"], "aud": e.get("audience", ""), "who": e.get("where", ""),
                   "body": "\n".join(e.get("what", [])) + ("\n\nWhen: " + e["date"] + ", " + e["time"]), "notes": "Mitchell confirms: " + "; ".join(e.get("confirm", [])), "hold": "Proposal"})
        if inv and e.get("invite_text"):
            ev.append({"d": inv, "ch": "Sales team", "camp": cp, "title": f"Invite to {e['name']}", "aud": {"e6": "Agents each consultant knows", "e7": "Homeowners each consultant built with"}.get(e["id"], "Each consultant's own active leads"),
                       "who": "New Home Consultants", "body": e["invite_text"] + ("\n\nEmail version: " + e["invite_email"]["subject"] if e.get("invite_email") else ""), "hold": ""})
        if rem and e.get("reminder_text"):
            ev.append({"d": rem, "ch": "Text", "camp": cp, "title": f"Reminder: {e['name']}", "aud": "Only people who RSVPed", "who": "Builder Studio workflow", "body": e["reminder_text"], "hold": ""})
        for x in e.get("extra_texts", []):
            ev.append({"d": when(x["date"]), "ch": "Text", "camp": cp, "title": f"Invitation: {e['name']}", "aud": x.get("audience", ""), "who": "Marketing", "body": x["body"], "hold": ""})
        for i, x in enumerate(e.get("social", [])):
            d2 = when(x.get("date", ""))
            if d2:
                ev.append({"d": d2, "ch": "Social", "camp": cp, "title": f"Event: {e['name']}", "aud": x.get("channels", ""), "who": "Marketing", "body": x["body"], "link": x.get("link", ""), "hold": ""})
# My Mitchell Story, the homeowner contest (campaigns/homeowners/contest.json); its emails come in with the rest,
# and E7 (Homeowner Appreciation Night) carries the invitation and reminder
cp = f"{C}/homeowners/contest.json"
if os.path.exists(cp):
    ct = json.load(open(cp))
    for t in ct["texts"]:
        if t["title"] in ("Consultant invite to Homeowner Appreciation Night", "RSVP reminder"):
            continue
        ch = "Sales team" if "1-to-1" in t["to"] else "Text"
        ev.append({"d": when(t["when"]), "ch": ch, "camp": "ref", "title": "My Mitchell Story: " + t["title"][0].lower() + t["title"][1:],
                   "aud": t["to"], "who": "New Home Consultants" if ch == "Sales team" else "Builder Studio", "body": t["body"], "hold": ""})
    for x in ct["social"]:
        ev.append({"d": when(x["date"]), "ch": "Social", "camp": "ref", "title": f"My Mitchell Story: {x['title']}", "aud": x["channels"], "who": "Marketing",
                   "body": x["body"], "link": x.get("link", ""), "notes": clean(x.get("notes", "")), "hold": ""})
    g = ct["gbp"]
    ev.append({"d": when(g["post_on"]), "ch": "Google", "camp": "ref", "title": g["title"], "aud": "Google Business Profile for each Design Center", "who": "Marketing",
               "body": g["body"], "link": g.get("link", ""), "notes": clean(g.get("notes", "")), "hold": ""})
    sale = ct["sales"][0]
    ev.append({"d": date(2026, 11, 18), "ch": "Sales team", "camp": "ref", "title": "My Mitchell Story: " + sale["title"][0].lower() + sale["title"][1:], "aud": sale.get("when", ""),
               "who": "New Home Consultants", "body": sale["body"], "hold": ""})
# Facebook group outreach, Nextdoor and YouTube cleanup are banked for winter (campaigns/plan), so they stay off this calendar
ev = [x for x in ev if x["d"] and START <= x["d"] < START + timedelta(days=7 * WEEKS)]
for x in ev:
    x["d"] = x["d"].isoformat()
ORDER = ["Event", "Setup", "Email", "Text", "Sales team", "Social", "Google", "Nextdoor", "FB groups", "YouTube"]
ev.sort(key=lambda x: (x["d"], ORDER.index(x["ch"]) if x["ch"] in ORDER else 9))
playbook = [{"title": i["title"], "meta": i["meta"], "body": i["body"], "notes": clean(i.get("notes", ""))} for i in dr["followups"]["items"]]

plan = json.load(open(f"{C}/plan/plan.json"))
data = {"start": START.isoformat(), "weeks": WEEKS, "events": ev, "playbook": playbook, "themes": plan["week_themes"], "batchOfWeek": [1, 1, 2, 2, 3, 3]}
page = open(f"{HERE}/page.html").read().replace("/*DATA*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
if re.search(r"[–—]", page):
    raise SystemExit("dash found")
for banned in ("FACTS.md", "previous agency", "CEA Marketing Group", "HighLevel"):
    if banned in page:
        raise SystemExit(f"page contains {banned!r}")
open(f"{OUT}/index.html", "w").write(page)
json.dump(files, open(f"{HERE}/files.json", "w"), indent=0)
by = {}
for x in ev:
    by[x["ch"]] = by.get(x["ch"], 0) + 1
print("index.html", len(page) // 1024, "KB;", len(ev), "dated touches", by)
