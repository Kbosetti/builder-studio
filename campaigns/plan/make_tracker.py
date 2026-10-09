#!/usr/bin/env python3
"""The fall tracker: every proof, decision, build and send, by batch, for Kelly's team (Google Sheets).

usage: python3 campaigns/plan/make_tracker.py      writes campaigns/plan/out/Mitchell-Fall-Tracker.xlsx
Uploaded to Kelly's Google Drive as a Google Sheet. Tabs: How to use, Batch 1, Batch 2, Batch 3 (the working
tabs: one row per task with due date, owner and a Status dropdown), Questions (Mitchell's decisions) and Later.
Built from plan.json, the emails, the posts, the events, the contest and the Builder Studio build sheet, so it
matches the approval pages and the calendar.
"""
import json, os, re
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
OUT = f"{HERE}/out"
MONTHS = {"October": 10, "November": 11, "December": 12}
APPROVAL = "https://mitchell-fall-approval.vercel.app"

plan = json.load(open(f"{HERE}/plan.json"))
emails = {e["id"]: e for e in json.load(open(f"{C}/email/out/emails.json"))["emails"]}
org = {s["id"]: s for s in json.load(open(f"{C}/traffic/organic.json"))["sections"]}
events = {e["id"]: e for e in json.load(open(f"{C}/events/events.json"))["events"]}
setup = json.load(open(f"{C}/builder_studio/setup.json"))
created = json.load(open(f"{C}/builder_studio/created.json"))
src = open(f"{C}/approval/page.html").read()
qblock = src[src.index("var QUESTIONS=["):src.index("];", src.index("var QUESTIONS=["))]
QS = [(a, b.replace("\\'", "'")) for a, b in re.findall(r"\['([^']+)','((?:[^'\\]|\\.)*)'\]", qblock)]
QMAP = {int(k): v for k, v in plan["questions"].items()}
BATCH = {b["n"]: b for b in plan["batches"]}


def d(text):
    m = re.search(r"(October|November|December) (\d{1,2})", text or "")
    return date(2026, MONTHS[m.group(1)], int(m.group(2))) if m else None


def due(text):
    return d(text)


rows = {1: [], 2: [], 3: []}


def add(b, when, kind, task, channel="", audience="", owner="", link="", notes="", status="Not started"):
    rows[b].append({"when": when, "kind": kind, "task": task, "channel": channel, "audience": audience, "owner": owner, "link": link, "notes": notes, "status": status})


TPL = {k: v["name"] for k, v in created.get("templates", {}).items()}
WF = {w["name"]: w for w in setup["workflows"]}

# proofing and decisions
for n, b in BATCH.items():
    add(n, due(b["proof_by"]), "Proof", f"Mitchell proofs Batch {n}: {b['name']} (approve or flag each piece, copy the summary to Kelly)", "Approval page",
        "Mitchell", "Mitchell", f"{APPROVAL}/batch-{n}/", f"Sends {b['sends']}.")
    for q, qb in sorted(QMAP.items()):
        if qb == n and q <= len(QS):
            add(n, due(b["proof_by"]), "Decision", f"Q{q} {QS[q - 1][0]}: {QS[q - 1][1]}", "Approval page", "Mitchell", "Mitchell", f"{APPROVAL}/batch-{n}/#questions")
add(1, date(2026, 10, 9), "Proof", "Send Mitchell the master plan and the Batch 1 link", "Email", "Mitchell", "Kelly", "https://mitchell-fall-plan.vercel.app")
add(2, date(2026, 10, 23), "Proof", "Send Mitchell the Batch 2 link", "Email", "Mitchell", "Kelly", f"{APPROVAL}/batch-2/")
add(3, date(2026, 11, 6), "Proof", "Send Mitchell the Batch 3 link", "Email", "Mitchell", "Kelly", f"{APPROVAL}/batch-3/")

# CEA build work, due the Friday of proofing week
B1, B2 = (due(BATCH[n]["build_by"]) for n in (1, 2))
for t, owner, notes in [
    ("Sending domain: add a Mitchell sending domain in Builder Studio (Settings, Email Services)", "CEA team and Mitchell IT", "One DNS change from whoever manages mitchellhomesinc.com (question 16)."),
    ("Text registration (A2P 10DLC) confirmed for Mitchell's numbers", "CEA team", "No bulk texts until it is approved."),
    ("Unsubscribe test: send one test email and confirm the footer link works", "CEA team", ""),
    ("Repoint the old Home Portrait Quiz trigger link and custom value to mitchellhomesliving.com/portrait", "CEA team", "They still point at an older quiz."),
    ("Remove the Show build notes toggle and reviewer notes from the mitchellhomesliving.com landing pages", "CEA team", "Before any ad points at /land or /math."),
    ("Smart lists: Full marketing list, Engaged, No quiz yet, Text list, Realtors", "CEA team", "Filters are in the kit, Builder Studio setup tab."),
    ("Workflows 01 Engagement tagger, 02 Clicked hand to a consultant, 03 Quiz taker first touch", "CEA team", "Steps in the kit, Builder Studio setup tab."),
    ("Workflow 06 Event RSVP and the RSVP form (for the October 29 live Q&A)", "CEA team", "Point the Fall26 Event RSVP trigger links at the form."),
    ("Workflow 07 Realtor replies, and missed-call text-back on every division number", "CEA team", ""),
    ("Website: pop-up, Home Portrait landing page, video strip, announcement bar and thank-you pages live", "Website vendor", "Files are in the kit, Website tab."),
    ("Print: counter cards in all five Design Centers, email signature banner for everyone", "Design Centers", ""),
]:
    add(1, B1, "Build", t, "Builder Studio" if "Workflow" in t or "list" in t or "Sending" in t or "registration" in t or "trigger" in t else "", "", owner, "", notes)
for t, owner, notes in [
    ("Smart lists: Landowners VA and MD, Landowners Carolinas, Looking for land VA and MD, Looking for land Carolinas", "CEA team", ""),
    ("Workflows 04 Quiet-lead detector and 05 Quiet-lead nurture (live November 2)", "CEA team", "Nine nurture emails and five texts are already in Builder Studio as drafts."),
    ("Workflow 08 After a Design Center visit, and turn the Design Studio Visit calendars back on", "CEA team", ""),
    ("Bring Your Photos Saturday (November 7): staff and supplies at all five Design Centers", "Mitchell", ""),
    ("Realtor Lunch and Learn (November 18): lunch, room and presenter at each Design Center", "Mitchell", ""),
]:
    add(2, B2, "Build", t, "Builder Studio" if "Workflow" in t or "list" in t or "form" in t else "", "", owner, "", notes)
# every scheduled send
CH = {"email": "Email", "text": "Text"}
for p in plan["pieces"]:
    if p["tier"] == "later" or p["batch"] is None:
        continue
    when = d(p["date"])
    if p["kind"] in CH and when:
        tid = p["id"].upper()
        name = TPL.get(tid, "")
        task = f"Schedule {tid}: " + (emails[p["id"]]["subject"] if p["id"] in emails else p["title"])
        notes = (p["note"] + ". " if p["note"] else "") + (f"Template: {name}" if name else "")
        add(p["batch"], when, "Send", task, CH[p["kind"]], p["to"], "CEA team", "", notes.strip(), )
    elif p["kind"] == "event" and when:
        e = events.get(p["id"], {})
        add(p["batch"], when, "Event", p["title"], "Event", p["to"] or e.get("audience", "")[:60], "Mitchell and CEA", "", p["note"])
    elif p["kind"] == "sales" and when:
        add(p["batch"], when, "Sales", p["title"], "Personal text or email", p["to"], "New Home Consultants")
for i in org["social"]["items"]:
    if i.get("tier") == "core" and i.get("batch") and d(i["meta"]):
        add(i["batch"], d(i["meta"]), "Post", i["title"].split(" · ", 1)[-1] + ": " + i["body"].strip().split("\n")[0][:80], "Social", i["meta"].split(" · ")[1] if " · " in i["meta"] else "", "CEA team", i.get("link", ""))
seen = set()
for i in org["gbp"]["items"]:
    kind = re.sub(r"\s*\(.*\)$", "", i["title"].split(": ", 1)[1])
    when = d(i["meta"])
    if when and (kind, when) not in seen:
        seen.add((kind, when))
        add(i["batch"] or 1, when, "Post", f"Google profile posts, all five Design Centers: {kind}", "Google Business Profile", "", "CEA team")
start = date.fromisoformat(plan["start"])
for w in range(plan["weeks"]):
    fri = start + timedelta(days=7 * w + 4)
    b = [1, 1, 2, 2, 3, 3][w]
    add(b, fri, "Sales", "Friday call list: everyone who clicked or visited this week and has not booked", "Calls", "", "Online sales counselors and consultants")
    add(b, fri, "Report", "Friday note to Mitchell: what went out, opens and clicks, quiz starts, Design Center bookings, next week", "Email", "Mitchell", "Kelly")

# Later and Questions
later = [(p["title"], p["note"] or "", p["date"]) for p in plan["pieces"] if p["tier"] == "later"]
later += [(i["title"].split(" · ", 1)[-1] + ": " + i["body"].strip().split("\n")[0][:70], "", "Winter") for i in org["social"]["items"] if i.get("tier") == "later" and i["title"][:1] == "s"]

# workbook
GREEN, PALE, SUN = "1E4F33", "E6F1EA", "F5D053"
wb = Workbook()
ws = wb.active
ws.title = "How to use"
guide = [
    ("Mitchell fall plan tracker", ""),
    ("", ""),
    ("How it works", "The fall plan runs in three batches. Mitchell proofs each batch about five days before it starts; CEA builds it in Builder Studio the same week; then it sends on schedule."),
    ("The tabs", "Batch 1, Batch 2 and Batch 3 are the working tabs: one row per task, sorted by date. Questions holds Mitchell's decisions. Later holds finished pieces saved for winter."),
    ("Status", "Use the dropdown: Not started, In progress, Waiting on Mitchell, Done. A send is Done once it is scheduled in Builder Studio and has gone out."),
    ("Every Monday", "Filter the current batch tab to this week, check anything not Done from last week, and move it or flag it."),
    ("Every Friday", "Kelly sends Mitchell a short note: what went out, what happened, what is next."),
    ("Links", "Master plan: https://mitchell-fall-plan.vercel.app   Approval batches: " + APPROVAL + "/batch-1/ (2, 3)   Calendar: https://mitchell-fall-cadence.vercel.app"),
    ("Builder Studio", "Every email is already a draft in the folder Fall 2026 | Campaign drafts from CEA. Tags and trigger links exist. Workflows, smart lists, forms and scheduled sends are built from the kit's Builder Studio setup tab."),
    ("Database rule", "One email a week to the full list. Engaged contacts get a Home Portrait email on four Thursdays. Four texts in six weeks. Nobody gets more than two emails in a week."),
]
for r in guide:
    ws.append(list(r))
ws["A1"].font = Font(bold=True, size=16, color=GREEN)
for r in range(3, len(guide) + 1):
    ws.cell(r, 1).font = Font(bold=True, color=GREEN)
    ws.cell(r, 2).alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(r, 1).alignment = Alignment(vertical="top")
ws.column_dimensions["A"].width = 18
ws.column_dimensions["B"].width = 110

HEAD = ["Date", "Day", "Type", "Task", "Channel", "Audience", "Owner", "Status", "Link", "Notes"]
WIDTH = [12, 6, 10, 70, 18, 26, 24, 18, 34, 46]
STATUS = '"Not started,In progress,Waiting on Mitchell,Done"'
ORDER = {"Proof": 0, "Decision": 1, "Build": 2, "Send": 3, "Event": 4, "Sales": 5, "Post": 6, "Report": 7}
for n in (1, 2, 3):
    b = BATCH[n]
    sh = wb.create_sheet(f"Batch {n}")
    sh.append([f"Batch {n}: {b['name']}  ·  sends {b['sends']}  ·  Mitchell proofs by {b['proof_by']}  ·  CEA builds by {b['build_by']}"])
    sh["A1"].font = Font(bold=True, size=13, color=GREEN)
    sh.append(HEAD)
    for c in range(1, len(HEAD) + 1):
        cell = sh.cell(2, c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=GREEN)
    items = sorted(rows[n], key=lambda r: (r["when"] or date(2027, 1, 1), ORDER.get(r["kind"], 9), r["task"]))
    for r in items:
        sh.append([r["when"], r["when"].strftime("%a") if r["when"] else "", r["kind"], r["task"], r["channel"], r["audience"], r["owner"], r["status"], r["link"], r["notes"]])
    last = sh.max_row
    for row in sh.iter_rows(min_row=3, max_row=last):
        row[0].number_format = "mmm d"
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        if row[2].value in ("Proof", "Decision"):
            for cell in row[:4]:
                cell.fill = PatternFill("solid", fgColor=PALE)
    dv = DataValidation(type="list", formula1=STATUS, allow_blank=True)
    sh.add_data_validation(dv)
    dv.add(f"H3:H{last}")
    for i, w in enumerate(WIDTH, 1):
        sh.column_dimensions[chr(64 + i)].width = w
    sh.freeze_panes = "A3"
    sh.auto_filter.ref = f"A2:J{last}"

qs = wb.create_sheet("Questions")
qs.append(["Q", "Question", "Details", "Batch", "Needed by", "Mitchell's answer", "Status"])
for c in range(1, 8):
    qs.cell(1, c).font = Font(bold=True, color="FFFFFF")
    qs.cell(1, c).fill = PatternFill("solid", fgColor=GREEN)
for i, (t, body) in enumerate(QS, 1):
    b = QMAP.get(i)
    status = "Done" if "(decided)" in t else "Not started"
    qs.append([i, t, body, b if b else "Later", BATCH[b]["proof_by"] if b else "When those pieces are scheduled", "", status])
for row in qs.iter_rows(min_row=2):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical="top")
dvq = DataValidation(type="list", formula1=STATUS, allow_blank=True)
qs.add_data_validation(dvq)
dvq.add(f"G2:G{qs.max_row}")
for col, w in zip("ABCDEFG", (5, 30, 80, 8, 24, 50, 18)):
    qs.column_dimensions[col].width = w
qs.freeze_panes = "A2"

lt = wb.create_sheet("Later")
lt.append(["Saved for winter", "Waits on", "When"])
for c in range(1, 4):
    lt.cell(1, c).font = Font(bold=True, color="FFFFFF")
    lt.cell(1, c).fill = PatternFill("solid", fgColor=GREEN)
for r in later:
    lt.append(list(r))
for row in lt.iter_rows(min_row=2):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical="top")
for col, w in zip("ABC", (80, 40, 34)):
    lt.column_dimensions[col].width = w

os.makedirs(OUT, exist_ok=True)
path = f"{OUT}/Mitchell-Fall-Tracker.xlsx"
wb.save(path)
for t in [x for v in rows.values() for x in v]:
    if re.search(r"[–—]", " ".join(str(v) for v in t.values())):
        raise SystemExit("dash in tracker: " + t["task"])
print(path, os.path.getsize(path) // 1024, "KB;", {n: len(v) for n, v in rows.items()}, "tasks per batch;", len(QS), "questions;", len(later), "later")
