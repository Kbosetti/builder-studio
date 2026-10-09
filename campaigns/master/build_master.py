#!/usr/bin/env python3
"""Build the master plan page Mitchell reads first: the whole fall strategy in one read.

usage: python3 campaigns/email/build.py && python3 campaigns/master/build_master.py
Reads campaigns/plan/plan.json (dates, tiers, batches), the built emails for subject lines, the events and the
approval document's questions. Writes campaigns/master/out/index.html (Artifact page) and deploy.py publishes the
public copy. Client facing: no internal notes, no platform vendor names, no dashes.
"""
import base64, json, os, re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
OUT = f"{HERE}/out"
MONTHS = {"October": 10, "November": 11, "December": 12}
APPROVAL = "https://mitchell-fall-approval.vercel.app"

plan = json.load(open(f"{C}/plan/plan.json"))
emails = {e["id"]: e for e in json.load(open(f"{C}/email/out/emails.json"))["emails"]}
events = {e["id"]: e for e in json.load(open(f"{C}/events/events.json"))["events"]}
start = date.fromisoformat(plan["start"])


def parse(text):
    m = re.search(r"(October|November|December) (\d{1,2})", text or "")
    return date(2026, MONTHS[m.group(1)], int(m.group(2))) if m else None


KIND = {"email": "Email", "text": "Text", "event": "Event"}
AUDIENCE = {"Full list": "the database", "Engaged contacts": "engaged contacts", "Landowners": "landowners", "Realtors": "realtors",
            "Past homeowners": "homeowners", "Text list, non-openers": "text list", "Text list, landowners": "landowners who agreed to texts"}
weeks = []
for w in range(plan["weeks"]):
    a = date.fromordinal(start.toordinal() + 7 * w)
    b = date.fromordinal(a.toordinal() + 6)
    weeks.append({"label": f"Week {w + 1} · {a.strftime('%B')} {a.day} to {('' if b.month == a.month else b.strftime('%B') + ' ')}{b.day}",
                  "batch": [1, 1, 2, 2, 3, 3][w], "theme": plan["week_themes"][w], "items": []})
seen = set()
for p in plan["pieces"]:
    if p["tier"] == "later" or p["kind"] not in KIND:
        continue
    d = parse(p["date"])
    if not d or not (start <= d < date.fromordinal(start.toordinal() + 7 * plan["weeks"])):
        continue
    if p["id"] in ("fb5c",):
        continue
    title = p["title"]
    if p["kind"] == "email" and p["id"] in emails:
        title = "“" + emails[p["id"]]["subject"] + "”"
        if p["id"] == "fb5":
            title += " (buyers still looking for land)"
    if p["kind"] == "event":
        title = p["title"]
    who = AUDIENCE.get(p["to"], p["to"].lower() if p["to"] else "")
    kind = KIND[p["kind"]] + (f" to {who}" if who and p["kind"] != "event" else "")
    weeks[(d - start).days // 7]["items"].append({"sort": d.isoformat(), "day": d.strftime("%a") + " " + str(d.day), "kind": kind, "title": title})
for w in weeks:
    w["items"].sort(key=lambda i: i["sort"])

EVENT_CARD = {  # where, and who it is for, in a line each
    "e2": ("Online, live on Facebook and YouTube", "For anyone deciding before the October 31 reserve-by date. Scott and Deven answer Design Dollars and SimplyMitchell questions."),
    "e1": ("All five Mitchell Design Centers, 10am to 2pm", "For active leads: bring the photos you have been saving, and see what they would cost with Design Dollars."),
    "e7": ("All five Mitchell Design Centers, 5:30 to 7:30pm", "For past Mitchell homeowners, invited by the consultant who built with them. My Mitchell Story begins that night, and homeowners can book their photo session there."),
    "e6": ("All five Mitchell Design Centers, over lunch", "For local real estate agents, land listing agents first: how Mitchell builds on the land their clients own."),
}
ev_cards = []
for p in plan["pieces"]:
    if p["kind"] == "event" and p["tier"] != "later":
        where, who = EVENT_CARD[p["id"]]
        ev_cards.append({"when": p["date"], "name": p["title"], "where": where, "who": who})

src = open(f"{C}/approval/page.html").read()
qblock = src[src.index("var QUESTIONS=["):src.index("];", src.index("var QUESTIONS=["))]
QS = [(a, b.replace("\\'", "'")) for a, b in re.findall(r"\['([^']+)','((?:[^'\\]|\\.)*)'\]", qblock)]
qmap = {int(k): v for k, v in plan["questions"].items()}
first = [QS[n - 1] for n in sorted(qmap) if qmap[n] == 1 and n <= len(QS)]

batches = []
for b in plan["batches"]:
    n = b["n"]
    count = sum(1 for p in plan["pieces"] if p["batch"] == n) + sum(1 for v in plan["social"].values() if v[1] == n)
    batches.append({**b, "count": count, "qcount": sum(1 for v in qmap.values() if v == n), "link": f"{APPROVAL}/batch-{n}/"})

later = [p["title"] for p in plan["pieces"] if p["tier"] == "later"]

DATA = {
    "stages": [
        {"stage": "Discover", "name": "The Home Portrait", "does": "Answer eight questions and Mitchell paints a Home Portrait of the home you would build. It turns a quiet contact into a conversation with a name, a region and a land answer.", "to": "mitchellhomesliving.com/portrait"},
        {"stage": "Believe", "name": "The Four Buyers", "does": "One argument per email for landowners and for buyers still looking for land: your land can be your down payment, a custom home without the unknowns.", "to": "simplymitchellhomes.com/land and /no-land"},
        {"stage": "Decide", "name": "Mitchell Design Dollars", "does": "Every Mitchell home starts with $5,000 in Design Dollars, up to $25,000 the more you personalize. The reserve-by date gives a reason to act now.", "to": "simplymitchellhomes.com/design-dollars"},
    ],
    "tracks": [
        {"name": "Realtors", "does": "About every other week to agents whose clients own land, and to agents who know land for buyers still looking. Plus a Realtor Lunch and Learn."},
        {"name": "The sales team", "does": "Every click and every quiz gets a person: an online sales counselor within 15 minutes for quiz takers, a New Home Consultant within one business day for anyone who clicks, and a Friday call list."},
        {"name": "Homeowners", "does": "My Mitchell Story: homeowners share a short phone video about the home they love, and every entrant gets a professional photo session at home, paid for by Mitchell, in time for holiday cards. It starts with Homeowner Appreciation Night on November 17."},
        {"name": "Quiet leads", "does": "Leads who have not answered get 60 days of personal notes from their consultant, a few designed emails and short texts. It stops the moment they reply or book."},
    ],
    "weeks": weeks, "events": ev_cards, "batches": batches, "questions": first, "later": later,
    "links": [["The full day-by-day calendar", "https://mitchell-fall-cadence.vercel.app"], ["The sales team guide", "https://mitchell-fall-campaign-guide.vercel.app"]],
}

font = base64.b64encode(open(f"{C}/../home-portrait/fonts/charlotte.woff2", "rb").read()).decode()
page = (open(f"{HERE}/page.html").read().replace("/*DATA*/null", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/"))
        .replace("%%charlotte%%", "data:font/woff2;base64," + font))
if re.search(r"[–—]", page):
    raise SystemExit("dash found in the master plan")
for banned in ("HighLevel", "GoHighLevel", "CEA Marketing Group", "previous agency", "Value Unlocker", "Grounded Dreamer"):
    if banned in page:
        raise SystemExit(f"master plan contains {banned!r}")
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/index.html", "w").write(page)
print("index.html", len(page) // 1024, "KB;", sum(len(w["items"]) for w in weeks), "pieces across", len(weeks), "weeks;", len(first), "first questions;", len(later), "saved for winter")
