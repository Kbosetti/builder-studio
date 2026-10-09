#!/usr/bin/env python3
"""The fall plan as Mitchell approves it and CEA builds it: every piece's send date, tier and batch.

usage: python3 campaigns/plan/make_plan.py      writes plan.json and plan.md next to this file
Tiers: core runs from October 19; add runs if Mitchell can staff it; later is finished and banked for winter.
Batches: Mitchell proofs each batch about five days before its first send, and CEA builds it in Builder Studio
the same week. The cadence keeps the database from being flooded: the full list gets one email a week
(Tuesday, or Wednesday in Election Day week), engaged contacts get a Home Portrait email on four Thursdays,
and there are four bulk texts in six weeks. Realtors and homeowners are their own lists.
Design Dollars: pieces sending in October keep October 31; pieces sending in November say November 30 and
wait for Mitchell to confirm it (question 1).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
START, WEEKS = "2026-10-19", 6

BATCHES = [
    {"n": 1, "name": "Launch", "sends": "October 19 to November 1", "proof_by": "Wednesday, October 14", "build_by": "Friday, October 16",
     "theme": "Design Dollars to the database through the October 31 reserve-by date, the Home Portrait to engaged contacts, the website and the counter cards."},
    {"n": 2, "name": "Landowners", "sends": "November 2 to 15", "proof_by": "Wednesday, October 28", "build_by": "Friday, October 30",
     "theme": "The Four Buyers to landowners and buyers still looking, Design Dollars in November, the quiet-lead nurture, Bring Your Photos Saturday and the homeowner invitation."},
    {"n": 3, "name": "Close and homeowners", "sends": "November 16 to 29, with the homeowner contest through December 18", "proof_by": "Wednesday, November 11", "build_by": "Friday, November 13",
     "theme": "The last Four Buyers and Home Portrait emails, the November 30 last call, the Realtor Lunch follow-up and My Mitchell Story, whose free photo sessions land in time for holiday cards."},
]

WEEK_THEMES = [
    "Design Dollars launch, and the Home Portrait to engaged contacts",
    "Reserve by Saturday, October 31, with the Design Dollars live Q&A on Thursday",
    "Landowners: your land can be your down payment, and Bring Your Photos Saturday",
    "Design Dollars in November, and the nine portraits",
    "Without the unknowns, Homeowner Appreciation Night and the Realtor Lunch",
    "Thanksgiving week: one email, the November 30 last call",
]


def P(id, kind, title, date, tier, batch, to="", note=""):
    return {"id": id, "kind": kind, "title": title, "date": date, "tier": tier, "batch": batch, "to": to, "note": note}


PIECES = [
    # emails to buyers: one a week to the full list, Thursdays to engaged contacts only
    P("dd1", "email", "Design Dollars launch", "Tuesday, October 20", "core", 1, "Full list"),
    P("hp1", "email", "Home Portrait invitation, with the Your Land reel", "Thursday, October 22", "core", 1, "Engaged contacts"),
    P("dd2", "email", "The spend and add ladder, reserve by Saturday, October 31, and the live Q&A invitation", "Tuesday, October 27", "core", 1, "Full list"),
    P("fb1", "email", "Four Buyers: your land is worth more than you think, and Bring Your Photos Saturday", "Wednesday, November 4", "core", 2, "Landowners", "Wednesday, not Election Day"),
    P("fb5", "email", "Four Buyers: you do not have to own land yet (Virginia and Maryland)", "Wednesday, November 4", "core", 2, "Buyers still looking for land"),
    P("fb5c", "email", "Four Buyers: you do not have to own land yet (Carolinas)", "Wednesday, November 4", "core", 2, "Buyers still looking for land"),
    P("hp2", "email", "Home Portrait: your land is part of the portrait", "Thursday, November 5", "core", 2, "Engaged contacts"),
    P("dd3", "email", "Design Dollars in November: sign now, choose later", "Tuesday, November 10", "core", 2, "Full list", "Says reserve by November 30; waits on question 1"),
    P("hp3", "email", "Home Portrait: nine portraits, with the Which One Are You? reel", "Thursday, November 12", "core", 2, "Engaged contacts"),
    P("fb2", "email", "Four Buyers: a custom home on your land, without the unknowns", "Tuesday, November 17", "core", 3, "Landowners"),
    P("hp4", "email", "Home Portrait: the getaway, with the Saturday Morning reel", "Thursday, November 19", "core", 3, "Engaged contacts"),
    P("dd4", "email", "Design Dollars last call: reserve by Monday, November 30", "Tuesday, November 24", "core", 3, "Full list", "Waits on question 1"),
    P("fb3", "email", "Four Buyers: no construction loan", "When legal clears the wording", "later", None, "Landowners", "Waits on question 7"),
    P("fb4", "email", "Four Buyers: your dream home has a folder (Virginia and Maryland)", "When the Dreamer page is fixed", "later", None, "Dreamers", "Waits on question 5"),
    P("fb4c", "email", "Four Buyers: your dream home has a folder (Carolinas)", "When the Dreamer page is fixed", "later", None, "Dreamers", "Waits on question 5"),
    # realtors: their own list, about every other week
    P("re1", "email", "Realtors: your buyer owns land, we build on it", "Wednesday, October 21", "add", 1, "Realtors"),
    P("ra1", "email", "Realtors: our buyers need land, do you know land?", "Wednesday, November 4", "add", 2, "Realtors", "Waits on question 17"),
    P("rb2", "email", "Realtors: when your land listing needs a picture, and the Realtor Lunch invitation", "Wednesday, November 11", "add", 2, "Realtors"),
    P("ra2", "email", "Realtors: what our buyers check before they buy a lot", "Thursday, November 19", "add", 3, "Realtors", "The day after the Realtor Lunch"),
    P("rb3", "email", "Realtors: your client's down payment may be in the ground", "When the incentive terms are confirmed", "later", None, "Realtors", "Waits on question 11"),
    # homeowners: their own list
    P("ho1", "email", "Homeowners: know someone with land and a dream?", "When a referral thank-you is decided", "later", None, "Past homeowners", "Waits on question 12"),
    P("ho2", "email", "Homeowners: invitation to Homeowner Appreciation Night", "Wednesday, November 4", "add", 2, "Past homeowners", "Waits on question 21"),
    P("ho3", "email", "My Mitchell Story launch", "Wednesday, November 18", "add", 3, "Past homeowners"),
    P("ho4", "email", "My Mitchell Story: your phone is all you need", "Wednesday, December 2", "add", 3, "Homeowners who have not entered"),
    P("ho5", "email", "My Mitchell Story: last week to enter", "Wednesday, December 9", "add", 3, "Homeowners who have not entered"),
    P("ho6", "email", "My Mitchell Story winner", "Friday, December 18", "add", 3, "Past homeowners"),
    P("hw", "automation", "My Mitchell Story notes to entrants (four automatic emails)", "From November 17", "add", 3, "Entrants"),
    # texts: four bulk texts in six weeks, never on an email day, only to people who agreed to texts
    P("sms1", "text", "Design Dollars", "Wednesday, October 21", "core", 1, "Text list, non-openers"),
    P("sms3", "text", "Reserve by October 31", "Wednesday, October 28", "core", 1, "Text list, non-openers"),
    P("sms4", "text", "Landowners", "Friday, November 6", "core", 2, "Text list, landowners"),
    P("sms2", "text", "Home Portrait", "Wednesday, November 11", "core", 2, "Text list, non-openers"),
    # always on
    P("auto-core", "automation", "Engagement tagger, clicked hand-off to a consultant, quiz taker first touch, missed-call text-back", "Live October 19", "core", 1),
    P("nurture", "automation", "Quiet-lead nurture: four personal notes, three designed emails, five texts over 60 days", "Live November 2", "core", 2, "Quiet leads"),
    P("auto-visit", "automation", "After a Design Center visit text", "Live November 2", "core", 2),
    P("auto-realtor", "automation", "Realtor replies go to a consultant", "Live October 21", "add", 1, "Realtors"),
    # sales team, personal
    P("sales-share", "sales", "Share the Home Portrait with your leads", "Thursday, October 22", "core", 1, "Each consultant's cold or stalled leads"),
    P("sales-dd", "sales", "Design Dollars personal email to active leads", "Friday, October 23", "core", 1, "Each consultant's active leads"),
    P("sales-deadline", "sales", "Deadline week personal email and text", "Tuesday, October 27 and Thursday, October 29", "core", 1, "Active leads"),
    P("sales-land", "sales", "Landowners personal text", "Thursday, November 5", "core", 2, "Active leads who own land"),
    P("sales-old", "sales", "Old-lead check-in", "Thursday, November 19", "core", 3, "Leads quiet for 90 days or more"),
    P("sales-photos", "sales", "Bring your photos text", "Monday, November 23", "core", 3, "Active leads"),
    P("sales-friday", "sales", "Friday call list: everyone who clicked and has not booked", "Every Friday", "core", 1),
    # events
    P("e2", "event", "Behind the Build Live: your Design Dollars questions (online)", "Thursday, October 29, 7pm", "add", 1, "", "Moved from Election Day"),
    P("e1", "event", "Bring Your Photos Saturday at all five Design Centers", "Saturday, November 7", "add", 2, "", "Moved from Halloween"),
    P("e7", "event", "Homeowner Appreciation Night at the Design Centers", "Tuesday, November 17", "add", 2, "Past homeowners"),
    P("e6", "event", "Realtor Lunch and Learn", "Wednesday, November 18", "add", 2, "Realtors"),
    P("e3", "event", "Building on Your Land 101", "Winter", "later", None),
    P("e4", "event", "Wilmington Design Center Open House", "Winter", "later", None),
    P("e5", "event", "The Gathering Place Live", "Winter", "later", None),
    P("contest", "contest", "My Mitchell Story: rules, entry form, photo sessions, posts and texts", "November 17 to December 18", "add", 3, "Past homeowners", "Rules go to legal now; photographers booked for the holiday card window, November 18 to December 5"),
    # posts
    P("social-1", "social", "Social: four posts in week 1 and four in week 2", "October 19 to November 1", "core", 1),
    P("social-2", "social", "Social: three posts a week", "November 2 to 15", "core", 2),
    P("social-3", "social", "Social: three posts, then two in Thanksgiving week", "November 16 to 29", "core", 3),
    P("gbp-1", "google", "Google profile posts at all five Design Centers: Design Dollars offer and Home Portrait update", "Monday, October 19 and Wednesday, October 21", "core", 1),
    P("gbp-2", "google", "Google profile posts: Four Buyers update, Home Portrait repost, November Design Dollars offer", "Monday, November 2 and Wednesday, November 11", "core", 2),
    # website and print
    P("web", "website", "Website pop-up, Home Portrait landing page and homeowner video strip", "Live October 19", "core", 1),
    P("web-bars", "website", "Website announcement bars and thank-you pages", "Live October 19", "core", 1),
    P("print", "print", "Counter cards for every Design Center and the email signature banner", "In the studios by October 19", "core", 1),
    # banked for winter
    P("later-social", "social", "Fifteen more social posts and two video series ideas", "Winter", "later", None),
    P("later-groups", "social", "Facebook group outreach (26 groups) and Nextdoor posts", "Winter", "later", None),
    P("later-youtube", "website", "YouTube descriptions, pinned comment and episode retitles", "Winter", "later", None),
    P("later-flyer", "print", "Landowner community board flyer", "Winter", "later", None),
    P("later-partners", "sales", "Local partner outreach", "Winter", "later", None),
]

SOCIAL = {  # social post id: (new date, batch); every other post is banked for winter
    "s01": ("Monday, October 19", 1), "s02": ("Tuesday, October 20", 1), "st01": ("Thursday, October 22", 1), "s04": ("Friday, October 23", 1),
    "s07": ("Tuesday, October 27", 1), "s08": ("Wednesday, October 28", 1), "st04": ("Thursday, October 29", 1), "s14": ("Friday, October 30", 1),
    "s11": ("Monday, November 2", 2), "s13": ("Wednesday, November 4", 2), "s17": ("Thursday, November 5", 2),
    "s09": ("Tuesday, November 10", 2), "s23": ("Thursday, November 12", 2), "s20": ("Saturday, November 14", 2),
    "s19": ("Tuesday, November 17", 3), "s21": ("Thursday, November 19", 3), "s15": ("Saturday, November 21", 3),
    "s27": ("Monday, November 23", 3), "s22": ("Tuesday, November 24", 3),
}

QUESTIONS = {  # approval question number: the batch whose pieces wait on it
    2: 1, 3: 1, 4: 1, 9: 1, 14: 1, 15: 1, 16: 1,
    1: 2, 6: 2, 8: 2, 10: 2, 17: 2, 19: 2, 20: 2, 21: 2,
    11: 3, 18: 3,
    5: None, 7: None, 12: None,
}


def main():
    data = {"start": START, "weeks": WEEKS, "batches": BATCHES, "week_themes": WEEK_THEMES, "pieces": PIECES, "social": SOCIAL, "questions": QUESTIONS}
    json.dump(data, open(f"{HERE}/plan.json", "w"), indent=1, ensure_ascii=False)
    lines = ["# Mitchell fall plan: dates, tiers and batches", "", "Generated by make_plan.py. Edit the script, not this file.", ""]
    for b in BATCHES:
        lines += [f"## Batch {b['n']}: {b['name']}", "", f"Sends {b['sends']}. Mitchell proofs by {b['proof_by']}; CEA builds by {b['build_by']}.", "", b["theme"], ""]
        for p in PIECES:
            if p["batch"] == b["n"]:
                lines.append(f"- {p['date']}: {p['title']} ({p['tier']}{', ' + p['to'] if p['to'] else ''}){'. ' + p['note'] if p['note'] else ''}")
        lines.append("")
    lines += ["## Later (finished, banked for winter)", ""]
    lines += [f"- {p['title']}: {p['date']}{'. ' + p['note'] if p['note'] else ''}" for p in PIECES if p["tier"] == "later"]
    open(f"{HERE}/plan.md", "w").write("\n".join(lines) + "\n")
    print(len(PIECES), "pieces;", sum(1 for p in PIECES if p["tier"] == "core"), "core,", sum(1 for p in PIECES if p["tier"] == "add"), "add,",
          sum(1 for p in PIECES if p["tier"] == "later"), "later;", len(SOCIAL), "social posts kept")


if __name__ == "__main__":
    main()
