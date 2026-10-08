#!/usr/bin/env python3
"""The Builder Studio build sheet for the fall campaigns: what is already loaded, the smart lists, the scheduled
sends, the workflows step by step, and the go live checklist.

usage: python3 campaigns/builder_studio/setup.py     writes campaigns/builder_studio/setup.json (read by the kit page)
Workflows, smart lists and campaign schedules cannot be created through the API, so they are written here as
exact build steps. Templates, tags and trigger links are created by upload.py and recorded in created.json.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
created = json.load(open(f"{HERE}/created.json")) if os.path.exists(f"{HERE}/created.json") else {}
emails = json.load(open(f"{C}/email/out/emails.json"))["emails"]
direct = {s["id"]: s for s in json.load(open(f"{C}/direct/direct.json"))["sections"]}
T = lambda eid: next((f"Fall26 · {e['id'].upper()} · {e['subject']}" for e in emails if e["id"] == eid), eid)

lists = [
    {"name": "Fall26 · Full marketing list", "filters": ["Email is not empty", "Email DND is off", "Opportunity status is not Won", "Tags do not include: disqualified, out of area, outside service area, vendor, realtor, realtor database, test contact, hbs test, source internal test"], "used_by": "Tuesday emails"},
    {"name": "Fall26 · Engaged", "filters": ["Everything in the full marketing list", "Tag includes fall26 engaged, OR date created is on or after September 1, 2026", "Tags do not include fall26 quiet (they are in the nurture)"], "used_by": "Thursday emails"},
    {"name": "Fall26 · No quiz yet", "filters": ["Everything in the engaged list", "Tags do not include home portrait quiz"], "used_by": "HP3"},
    {"name": "Fall26 · Landowners VA and MD", "filters": ["Everything in the full marketing list", "Tags include land owned OR land family", "Tags include fredericksburg, va OR richmond, va OR newport news, va, or a Virginia region tag"], "used_by": "FB1, FB2, FB3, FB4, SMS4"},
    {"name": "Fall26 · Landowners Carolinas", "filters": ["Everything in the full marketing list", "Tags include land owned OR land family", "Tags include raleigh, nc OR wilmington, nc, or a Carolinas region tag"], "used_by": "FB4C"},
    {"name": "Fall26 · Looking for land VA and MD", "filters": ["Everything in the full marketing list", "Tags include land searching OR land dreaming", "Virginia division or region tags"], "used_by": "FB5"},
    {"name": "Fall26 · Looking for land Carolinas", "filters": ["Everything in the full marketing list", "Tags include land searching OR land dreaming", "Carolinas division or region tags"], "used_by": "FB5C"},
    {"name": "Fall26 · Text list", "filters": ["Phone is not empty", "SMS DND is off and the contact gave text consent", "Tags do not include fall26 clicked, fall26 skip text this week, fall26 quiet", "If the campaign report can export non-openers of that week's Tuesday email, send to that export instead"], "used_by": "The weekly text"},
    {"name": "Fall26 · Realtors", "filters": ["Tags include realtor OR realtor database", "Email DND is off"], "used_by": "Realtor emails"},
    {"name": "Fall26 · Past homeowners", "filters": ["No tag exists yet. Tag closed buyers homeowner (opportunity status Won, or the Lasso homeowner list), then filter on it"], "used_by": "HO1"},
]

times = {"Tuesday": "10:00 am", "Wednesday": "11:00 am", "Thursday": "10:00 am"}
sends = []
for e in emails:
    if not re.match(r"(Mon|Tues|Wednes|Thurs|Fri)day, (October|November)", e["send"]):
        continue
    day = e["send"].split(",")[0]
    sends.append({"when": e["send"].split(", after")[0], "time": times.get(day, "10:00 am"), "channel": "Email campaign", "template": T(e["id"]),
                  "subject": e["subject"], "preview": e["preview"], "to": e["segment"], "from": "Mitchell Homes", "hold": e["hold"]})
for i in direct["sms"]["items"]:
    sends.append({"when": i["meta"].split(" · ")[0], "time": "11:00 am", "channel": "Bulk text", "template": i["title"], "subject": "", "preview": i["body"],
                  "to": "Fall26 · Text list", "from": "Mitchell Homes number", "hold": ""})

ev_path = f"{C}/events/events.json"
if os.path.exists(ev_path):
    for ev in json.load(open(ev_path))["events"]:
        for x in ev.get("extra_texts", []):
            sends.append({"when": x["date"].replace(", 2026", ""), "time": "11:00 am", "channel": "Bulk text", "template": f"{ev['name']} invitation",
                          "subject": "", "preview": x["body"], "to": x.get("audience", ""), "from": "Mitchell Homes number", "hold": ""})


def sms(title):
    return next(i["body"] for i in direct["nurture"]["items"] + direct["followups"]["items"] if i["title"].startswith(title))

workflows = [
    {"name": "Fall26 | 01 Engagement tagger", "purpose": "Keeps the engaged list current, so Thursday emails only go to people who are reading.",
     "trigger": "Email Events: Opened or Clicked (any email)", "settings": "Allow re-entry: on",
     "steps": ["Add tag: fall26 engaged", "Wait: 90 days", "Remove tag: fall26 engaged"],
     "exits": [], "notes": "Contacts created since September 1, 2026 count as engaged through the smart list filter, so nobody new is missed while the tag fills in."},
    {"name": "Fall26 | 02 Clicked, hand to a consultant", "purpose": "A person follows every click within one business day, and the clicker skips that week's marketing text.",
     "trigger": "Trigger Link Clicked: any link named Fall26; and Email Events: Clicked, on the Fall26 templates", "settings": "Allow re-entry: on",
     "steps": ["Add tags: fall26 clicked, fall26 skip text this week", "Create task for the assigned user: Follow up within one business day. Use the follow-up script for what they clicked. Due in 1 business day",
               "Send internal notification to the assigned user", "Wait: 7 days", "Remove tags: fall26 clicked, fall26 skip text this week"],
     "exits": [], "notes": "Scripts: Clicked a Design Dollars email: text; Clicked a Four Buyers email or page: text; Landowner: follow-up email."},
    {"name": "Fall26 | 03 Quiz taker first touch", "purpose": "Every quiz taker hears from a person within 15 minutes, by name and portrait.",
     "trigger": "Contact Tag added: home portrait quiz", "settings": "Business hours 8 am to 8 pm local time; outside them, send at 8 am",
     "steps": ["If the contact has a phone and text consent: Send SMS from the assigned user: " + sms("Quiz taker: first text"),
               "Otherwise: Create task for the assigned user: Call within 15 minutes",
               "Wait: until the contact replies, or 1 day", "If no reply: Send email from the assigned user, template Fall26 · SALES01 · Your {{contact.portrait_name}} (Quiz taker: next-day email)"],
     "exits": ["Contact replied", "Appointment booked"],
     "notes": "Check Mitchell | 01 Inquiry routing first. If it already sends a first text, add this text there instead, so nobody gets two."},
    {"name": "Fall26 | 04 Quiet-lead detector", "purpose": "Finds leads who have gone quiet, so the nurture starts on its own.",
     "trigger": "Opportunity Created, in any division pipeline", "settings": "Allow re-entry: off",
     "steps": ["Wait: until the contact replies, or an appointment is booked, or 7 days pass", "If 7 days passed with no reply and no appointment, and the opportunity is still in New Lead or Contacted: Add tag fall26 quiet"],
     "exits": [], "notes": "For leads already in the pipeline, add fall26 quiet in bulk to anyone with no reply in 7 or more days and no appointment."},
    {"name": "Fall26 | 05 Quiet lead nurture", "purpose": "Sixty days of personal notes, designed emails and texts, until the lead replies or books.",
     "trigger": "Contact Tag added: fall26 quiet", "settings": "Texts only with consent, between 10 am and 7 pm local time",
     "steps": ["Day 0: Send email from the assigned user, template " + T("nu1"),
               "Wait 2 days. If text consent: Send SMS, Nurture text, Day 2",
               "Wait 3 days. If tags include land owned or land family: Send email " + T("nu3") + ". Otherwise: Send email " + T("nu3n"),
               "Wait 7 days: Send email from the assigned user, " + T("nu4"),
               "Wait 7 days. If tags include home portrait quiz: Send SMS, Nurture text, Day 19 (took the quiz). Otherwise: Send SMS, Nurture text, Day 19 (not yet), with trigger link Fall26 · Nurture · Home Portrait",
               "Wait 7 days: Send email " + T("nu6") + " (skip this step if Design Dollars has ended)",
               "Wait 9 days: Send email from the assigned user, " + T("nu7"),
               "Wait 10 days. If land owned or land family: Send SMS, Nurture text, Day 45 (own land), link Fall26 · Nurture · Roadmap episode. Otherwise: Day 45 (looking), link Fall26 · Nurture · Purchasing Land 101 episode",
               "Wait 15 days: Send email " + T("nu9"),
               "Add tag fall26 nurture done. Remove tag fall26 quiet"],
     "exits": ["Goal: Contact replied (email or text). Then create a task for the assigned user: Replied to the nurture, call today", "Goal: Appointment booked", "Goal: Opportunity moves to Appointment Set or later", "Email or text DND"],
     "notes": "If a lead replies later, the consultant sets a task to check back in the spring. Designed emails send from Mitchell Homes; personal ones from the assigned user."},
    {"name": "Fall26 | 06 Event RSVP", "purpose": "Confirms each RSVP, reminds the day before, and follows up after.",
     "trigger": "Form Submitted: Fall26 Event RSVP (fields: name, email, phone, event, Design Center, text consent)", "settings": "One workflow, a branch per event",
     "steps": ["Add the event tag, for example event bring your photos oct24", "Send confirmation email and, with consent, a confirmation text",
               "Wait until the day before the event at 9 am: Send the RSVP reminder text", "Wait until the event day at 4 pm: Send the thank-you text from the assigned user",
               "Wait 1 day: Send the follow-up email from the assigned user, and create a task to call"],
     "exits": [], "notes": "The event invitations, reminders and follow-ups are in the Events tab. Create the RSVP form first; its link replaces [RSVP link] in every invitation."},
    {"name": "Fall26 | 07 Realtor replies", "purpose": "Turns realtor replies into partners.",
     "trigger": "Customer Replied (email), and tags include realtor or realtor database", "settings": "",
     "steps": ["Create task for Noele Riedl: A realtor replied to a Fall26 email. Note their counties and tag them realtor land partner or realtor on your land", "Notify the New Home Consultant for that division"],
     "exits": [], "notes": "Land partners get introductions to buyers still looking for land, once Mitchell approves (question 17)."},
    {"name": "Fall26 | 08 After a Design Center visit", "purpose": "Same-day text that tells the buyer how close they are to the next Design Dollars tier.",
     "trigger": "Appointment Status: Showed, on the Design Studio Visit calendars", "settings": "Or add these steps to Mitchell | NHC 04 Appointment Completed tasks",
     "steps": ["Create task for the assigned user: Send the After a Design Center visit text today, with the gap to the next tier filled in"],
     "exits": [], "notes": "The amounts change per buyer, so this stays a task with the script rather than an automatic text."},
]

checklist = [
    "Mitchell signs off in the approval document.",
    "Sending domain: add a dedicated Mitchell sending domain under Settings, Email Services. Today the platform sends from its default address, which will hurt a 30,000-contact send.",
    "Unsubscribe: send one test. If the account's automatic footer link is on, remove the {{unsubscribe}} line from the templates so there is only one.",
    "Texting: confirm the A2P 10DLC registration for Mitchell's numbers is approved before any bulk text.",
    "Calendars: the Design Studio Visit calendars are switched off. Turn them on with availability before the events and the quiz follow-ups.",
    "The Home Portrait Quiz trigger link and the Home Portrait Quiz URL custom value point to mitchellhomeportrait.vercel.app, an older copy of the quiz outside CEA's Vercel account. Point both to https://mitchellhomesliving.com/portrait once confirmed.",
    "Routing: check Mitchell | 01 Inquiry routing so quiz leads do not get two first texts.",
    "Past homeowners: tag them homeowner so the referral email has a list.",
    "Event RSVP form: create it, then point the six Fall26 · Event RSVP trigger links at it. Today they open Mitchell's contact page, so every invitation already works and updates the moment the links change.",
    "A few event emails say [city] where the Design Center name goes: set it per division before sending, or duplicate the template per studio.",
]

done = []
if created.get("folder"):
    done.append(f"Template folder: {created['folder']['name']}")
if created.get("templates"):
    done.append(f"{len(created['templates'])} email templates loaded into that folder, each named Fall26 · ID · subject line, with its preview text")
if created.get("tags"):
    done.append(f"{len(created['tags'])} tags: " + ", ".join(created["tags"]))
if created.get("links"):
    done.append(f"{len(created['links'])} trigger links: " + ", ".join(created["links"]))

json.dump({"done": done, "lists": lists, "sends": sends, "workflows": workflows, "checklist": checklist}, open(f"{HERE}/setup.json", "w"), indent=1, ensure_ascii=False)
txt = json.dumps({"lists": lists, "workflows": workflows, "checklist": checklist}, ensure_ascii=False)
assert not re.search(r"[–—]", txt), "dash"
print(len(done), "done lines,", len(lists), "smart lists,", len(sends), "scheduled sends,", len(workflows), "workflows")
