#!/usr/bin/env python3
"""Fall 2026 events for Mitchell Homes: six proposals with every invitation and follow up.

usage: python3 campaigns/events/make_events.py   writes events.json and events.md next to this file.
DRAFTS ONLY. Nothing here is sent, posted, scheduled or created. Every event is a proposal until
Mitchell approves dates and staffing. Facts come from campaigns/FACTS.md only.
"""
import json, os, re, sys
from urllib.parse import urlencode

HERE = os.path.dirname(os.path.abspath(__file__))
CAMP = "fall26_events"
QUIZ = "https://mitchellhomesliving.com/portrait"
SMH = "https://simplymitchellhomes.com"
DD = SMH + "/design-dollars"
RSVP = "[RSVP link]"
M = "https://media.mitchellhomesinc.com/276/"

CH = {  # channel: (utm_source, utm_medium)
    "email": ("email", "email"),
    "facebook": ("facebook", "organic_social"),
    "instagram": ("instagram", "organic_social"),
    "linkedin": ("linkedin", "organic_social"),
    "facebook_event": ("facebook", "facebook_event"),
    "gbp": ("google_business_profile", "organic"),
    "nextdoor": ("nextdoor", "organic_social"),
    "invite_text": ("sales_text", "sms"),
    "invite_email": ("sales_email", "email"),
    "reminder": ("rsvp_reminder", "sms"),
    "sms": ("sms", "sms"),
    "followup": ("sales_email", "email"),
}


def u(base, ch, eid):
    s, m = CH[ch]
    return base + "?" + urlencode({"utm_source": s, "utm_medium": m, "utm_campaign": CAMP, "utm_content": eid})


SIG = "\n\n[your name]\nNew Home Consultant, Mitchell Homes\n[your phone]"
FINE = "Design Dollars apply to Design Center selections only. Not applied to base price. No cash value."
FIN = "Financing terms are illustrative only and subject to credit approval. Not a commitment to lend."
DD_SHORT = "Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize."
DD_SCOTT = "Your home comes with $5,000 in Design Dollars, and it goes up to $25,000 the more you personalize."
DD_DOC = "Every Mitchell home comes with $5,000 in Mitchell Design Dollars to spend on design selections. The more selections you buy, the more Mitchell adds, up to $25,000."
DD_LOCK = "Reserve by October 31, 2026, and your Design Dollars are locked. Your tier is set later, when you make your selections."
DD_LOCK_NOV = "Reserve by November 30, 2026, and your Design Dollars are locked. Your tier is set later, when you make your selections."
SM = "zero down, zero closing costs and no construction loan, because Mitchell self-funds every build"
PHONES = "Virginia and Maryland (540) 701-2759, North and South Carolina (984) 331-5468"
LUNCH = "[Lunch provided: Mitchell to confirm.]"
TBD = "Winter, date to be set"  # events banked for winter (tier later) until Mitchell schedules them

STUDIOS = [
    {"studio": "Fredericksburg VA", "city": "Fredericksburg", "address": "621 Warrenton Road, Fredericksburg, VA 22406", "phone": "(540) 701-2759",
     "page": "https://www.mitchellhomesinc.com/design-center/fredericksburg-va/"},
    {"studio": "Richmond VA (Midlothian)", "city": "Richmond", "address": "14300 Sommerville Court, Midlothian, VA 23113", "phone": "(540) 701-2759",
     "page": "https://www.mitchellhomesinc.com/design-center/richmond-va/", "note": "The live Design Dollars page lists (804) 538-3912 for this studio. Confirm which line Mitchell wants."},
    {"studio": "Newport News VA", "city": "Newport News", "address": "663 Turnberry Boulevard, Suite E, Newport News, VA 23602", "phone": "(540) 701-2759",
     "page": "https://www.mitchellhomesinc.com/design-center/newport-news-va/"},
    {"studio": "Raleigh NC (studio in Garner)", "city": "Raleigh", "address": "505 N. Greenfield Pkwy, Suite 120, Garner, NC 27529", "phone": "(984) 331-5468",
     "page": "https://www.mitchellhomesinc.com/design-center/raleigh-nc/"},
    {"studio": "Wilmington NC (studio in Belville, open since September 11, 2026)", "city": "Wilmington", "address": "42 Waterford Business Center Way, Suite A, Belville, NC 28451", "phone": "(984) 331-5468",
     "page": "https://www.mitchellhomesinc.com/design-center/wilmington-nc/"},
]
ALL5 = "All five Mitchell Design Centers: Fredericksburg VA, Richmond VA (Midlothian), Newport News VA, Raleigh NC (studio in Garner) and Wilmington NC (studio in Belville). Addresses in the studio table, as listed on the live Design Dollars page."
IG_NOTE = "Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to {ig} that morning."
BOOST = "Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category."


def sched(rows):
    return [{"date": d, "day": day, "channel": ch, "what": what, "who": who} for d, day, ch, what, who in rows]


EVENTS = []

# ---------------------------------------------------------------- E1
e = "e1"
EVENTS.append({
    "id": e,
    "name": "Bring Your Photos Saturday",
    "tier": "add",
    "date": "Saturday, November 7, 2026",
    "time": "10am to 2pm, local time at every studio",
    "where": ALL5,
    "audience": "Anyone planning a Mitchell home who has not signed yet, above all the buyers who have been saving photos of the home they want: active leads, Design Dollars email clickers and Home Portrait quiz takers. Walk-ins welcome; an RSVP gets a reserved time with a Design Consultant.",
    "what": [
        "Buyers bring the photos they have been saving, on their phone or in a folder.",
        "A Design Consultant matches the favorites to Mitchell selections and shows what they cost.",
        "Together they see where that list lands on the Design Dollars ladder, and how far it is to the next tier.",
    ],
    "why": "Turns the Four Buyers emails on November 4 (fb1, fb5 and fb5c) into a seat at the design table three weeks before the November 30 reserve-by date, with the buyer's own photos as the reason to come in.",
    "confirm": [
        "Approve the date and the 10am to 2pm hours, or name the studios that will take part.",
        "Staffing at every studio: a Design Consultant for the full four hours, plus a New Home Consultant for land and plan questions. Newport News and Wilmington each have one New Home Consultant; name the cover.",
        "Reserved times: CEA proposes 30-minute slots with walk-ins between them. Confirm the length and how many tables each studio can run at once.",
        "Pricing at the table: can a Design Consultant price a photo list on the spot? If not, copy changes to: we will send you the numbers.",
        "RSVP form (Kelly builds it in Builder Studio): name, phone, email, studio, preferred time, and the text consent checkbox with legal-approved wording.",
        "Food: none promised anywhere. If Mitchell wants coffee or light refreshments, add one line to the Facebook event.",
        "Studio addresses as listed on the live Design Dollars page, and which phone line Richmond shows.",
        "Design Dollars in November: these pieces say reserve by November 30, the date Kelly recommends. It waits on Mitchell's approval (question 1); if Mitchell sets another date, only the date changes.",
    ],
    "rides_in": [{
        "email": em, "send": "Wednesday, November 4, 2026",
        "placement": place,
        "block": {
            "head": "Bring Your Photos Saturday, November 7",
            "text": "Bring the photos you have been saving to any Mitchell Design Center between 10am and 2pm, and sit down with a Design Consultant who will show you what your favorites cost. You will also see where they land on the Design Dollars ladder, which starts at $5,000 on every home and grows up to $25,000 the more you personalize.",
            "cta": "Save My Time",
            "link": u(RSVP, "email", e),
            "fine": FINE}} for em, place in [
        ("fb1", "Event block near the end, after the Downey quote and before the Design Dollars band."),
        ("fb5", "Event block after the floor plans line, before the Design Dollars band. fb5 is on hold until the plan guide email is built; if it slips past November 6, this block moves to the consultant invites only."),
        ("fb5c", "The same block as fb5, in the Carolinas version, which is built from fb5 and carries the block and the hold with it.")]],
    "social": [
        {"date": "Monday, November 2, 2026", "channels": "Facebook, Instagram feed",
         "body": "You have been saving photos of this house for years. The kitchen. The porch. The light over the table.\n\nBring them in. On Saturday, November 7, from 10am to 2pm, every Mitchell Design Center is open for Bring Your Photos Saturday. Sit down with a Design Consultant, see what your favorites cost, and see where they land on the Design Dollars ladder. " + DD_SHORT + "\n\nFredericksburg, Richmond, Newport News, Raleigh and Wilmington. Walk-ins welcome. RSVP and we will save you a time: " + RSVP + "\n\n" + FINE + "\n\n#BuildOnYourLand #MitchellHomes",
         "link": u(RSVP, "facebook", e),
         "notes": "Image: a Design Center finish wall or kitchen display, e.g. " + M + "2023/2/6/Design_Center_13_IfaBRgj.jpg . " + BOOST + " " + IG_NOTE.format(ig=u(RSVP, "instagram", e))},
        {"date": "Friday, November 6, 2026", "channels": "Facebook, Instagram Stories",
         "body": "Tomorrow, 10am to 2pm. Bring the photos you have been saving to your nearest Mitchell Design Center, and a Design Consultant will show you what your favorites cost.\n\n" + DD_SHORT + " " + DD_LOCK_NOV + "\n\nRSVP: " + RSVP + "\n\n" + FINE,
         "link": u(RSVP, "facebook", e),
         "notes": "Stories: use the link sticker with the Instagram link " + u(RSVP, "instagram", e) + " . Fine print stays on the Story frame. " + BOOST},
    ],
    "facebook_event": "Bring Your Photos Saturday at the Mitchell Homes [city] Design Center\nSaturday, November 7, 2026, 10am to 2pm\n[studio address]\n\nYou know what you want. You have the photos to prove it. Bring them in.\n\nSit down with a Mitchell Design Consultant, show us the kitchens, porches, tile and lighting you have been saving, and we will match them to Mitchell selections and show you what they cost. With more than 40,000 selections, most of what is in your folder is something we already carry.\n\nYou will also see where your list lands on the Mitchell Design Dollars ladder. " + DD_DOC + " " + DD_LOCK_NOV + "\n\nWalk-ins are welcome. RSVP and we will save you a time with a Design Consultant: " + RSVP + "\n\nQuestions? Call a New Home Consultant: " + PHONES + ".\n\n" + FINE + " One offer per contract.",
    "facebook_event_notes": "One Facebook event per Design Center, so each shows a real address to people nearby; only [city] and [studio address] change. Link: " + u(RSVP, "facebook_event", e) + " . Cover image: no people.",
    "gbp": {
        "title": "Bring Your Photos Saturday",
        "body": "Bring the photos you have been saving for your future home to our [city] Design Center. A Design Consultant will match your favorites to Mitchell selections, show you what they cost, and show you where they land on the Design Dollars ladder. " + DD_SHORT + " Walk-ins welcome, or tap Sign up to save a time.\n\n" + FINE,
        "button": "Sign up",
        "link": u(RSVP, "gbp", e),
        "post_on": "All five Design Center profiles, Monday, November 2. Event-type post, start Saturday, November 7, 10am, end 2pm.",
        "notes": "Title holds 58 characters. Image: that studio's interior, no people."},
    "nextdoor": "Saving photos of the home you want to build? Bring them in.\n\nOn Saturday, November 7, from 10am to 2pm, the Mitchell Homes [city] Design Center at [studio address] is open for Bring Your Photos Saturday. Sit down with a Design Consultant, see what your favorites cost, and see where they land on the Design Dollars ladder. " + DD_SHORT + "\n\nWalk-ins welcome. RSVP for a reserved time: " + u(RSVP, "nextdoor", e) + "\n\nMitchell Homes, building on your land since 1992.\n\n" + FINE,
    "nextdoor_when": "Wednesday, November 4, 2026, from each Design Center's Nextdoor business page where one exists.",
    "invite_when": "Monday, November 2 to Thursday, November 5, 2026. Every New Home Consultant to their own active leads.",
    "invite_text": "Hi [first name], it is [your name] with Mitchell Homes. This Saturday, Nov 7, from 10 to 2, bring the home photos you have been saving to our [city] Design Center. A Design Consultant will show you what your favorites cost. Want me to save you a time?",
    "invite_email": {
        "subject": "Bring your photos Saturday",
        "body": "Hi [first name],\n\nIf you have been saving photos of the home you want, this Saturday is a good day to bring them in.\n\nOn Saturday, November 7, from 10am to 2pm, our [city] Design Center is open for Bring Your Photos Saturday. Sit down with one of our Design Consultants, show us what you have been saving, and we will match it to Mitchell selections and show you what it costs.\n\nYou will also see where your list lands on the Design Dollars ladder. " + DD_DOC + " Choose $60,000 in selections, for example, and Mitchell adds $15,000, so you take home $75,000 worth. Sign now, and your incentive is locked, but your tier will be decided when you make your selections. Reserve by November 30.\n\nReply with a time that works and I will hold it for you, or just come by." + SIG + "\n\n" + FINE},
    "reminder_when": "Friday, November 6, 2026. Builder Studio workflow on the RSVP form, to RSVPs with text consent only.",
    "reminder_text": "Mitchell Homes: See you tomorrow at [time] at our [city] Design Center, [studio address]. Bring the photos you have been saving. Need a new time? Reply here. Reply STOP to opt out",
    "thanks_when": "Saturday, November 7, 2026, by 6pm. The Design Consultant or New Home Consultant each attendee met.",
    "thanks_text": "Thank you for coming in today, [first name]. It was great to see the home you have been picturing. I will send your priced list on Monday so you have it all in one place. Questions before then? Just text me.",
    "followup_when": "Monday, November 9, 2026. The New Home Consultant, from their own address.",
    "followup_email": {
        "subject": "Your photos, priced",
        "body": "Hi [first name],\n\nThank you for bringing your photos in on Saturday. It was good to see the home you have been picturing, and [one thing they loved, in their words] belongs in it.\n\nHere is what we priced together:\n[selection list with prices, from the Design Consultant]\n\nOn the Design Dollars ladder, that list puts you at [tier]. You are [amount] away from the next tier, which adds [amount] more for your selections. Every Mitchell home starts with $5,000 in Mitchell Design Dollars, up to $25,000 the more you personalize. See the full ladder: " + u(DD, "followup", e) + "\n\nReserve by Monday, November 30, and your Design Dollars are locked. Your tier is set later, when you make your selections, and your reservation deposit is $150, which is all Mitchell receives until closing.\n\nOne more thing: on Thursday, October 29, Scott Sleeme and Deven Sellers answered Design Dollars and SimplyMitchell questions live on Facebook and YouTube. The replay is here: [replay link]. If you have a question they did not get to, send it to me.\n\nWant to pick a plan to go with your list? Reply with a time this week." + SIG + "\n\n" + FINE},
    "extra_texts": [],
    "notes": [
        "November 5 already has a consultant text in the cadence (the landowner text to active leads who own land). Send this invite to those leads on November 2 to 4, so nobody gets two consultant texts that day.",
        "fb4 (banked for winter) and the consultant text on Monday, November 23 also say bring your photos. This Saturday is the November version; both stay as written.",
        "Never show the painted Home Portrait at the event table or in any of these pieces.",
    ],
    "schedule": sched([
        ("2026-11-02", "Monday, November 2", "Social", "Post 1 (Facebook, Instagram feed). Publish the five Facebook events.", "Marketing"),
        ("2026-11-02", "Monday, November 2", "Google", "Event post on all five Design Center profiles", "Marketing"),
        ("2026-11-02", "Monday, November 2", "Sales team", "Personal invite text and email to own active leads, through Thursday, November 5 (leads who own land by November 4)", "New Home Consultants"),
        ("2026-11-04", "Wednesday, November 4", "Email", "Event block in fb1, fb5 and fb5c", "Marketing"),
        ("2026-11-04", "Wednesday, November 4", "Nextdoor", "Post from each Design Center page", "Marketing"),
        ("2026-11-06", "Friday, November 6", "Social", "Post 2 (Facebook, Instagram Stories)", "Marketing"),
        ("2026-11-06", "Friday, November 6", "Text", "Reminder to RSVPs only", "Builder Studio workflow"),
        ("2026-11-07", "Saturday, November 7", "Event", "Bring Your Photos Saturday, 10am to 2pm; thank-you text by 6pm", "Design Consultants, New Home Consultants"),
        ("2026-11-09", "Monday, November 9", "Sales team", "Follow-up email with the priced list", "New Home Consultants"),
    ]),
})

# ---------------------------------------------------------------- E2
e = "e2"
EVENTS.append({
    "id": e,
    "name": "Behind the Build Live: Your Design Dollars and SimplyMitchell Questions",
    "tier": "add",
    "date": "Thursday, October 29, 2026",
    "time": "7pm Eastern, about 30 minutes",
    "where": "Online: live on the Mitchell Homes Facebook page and YouTube channel at the same time. No studio needed.",
    "audience": "Everyone still deciding before the October 31 reserve-by date: active leads, Design Dollars email clickers, quiz takers, and anyone curious how SimplyMitchell works. Agents and past homeowners welcome.",
    "what": [
        "Scott Sleeme and Deven Sellers explain Mitchell Design Dollars in plain terms: $5,000 on every home, up to $25,000 the more you personalize, and what it covers.",
        "They answer questions sent in ahead and asked live, including how SimplyMitchell works: " + SM + ".",
        "The recording stays on both channels, and each answer becomes its own short clip.",
    ],
    "why": "Answers the two questions that stall a Design Dollars decision (what does it cover, do I have to choose now) two days before the October 31 reserve-by date, in Scott's own voice.",
    "confirm": [
        "Scott and Deven's time: Thursday, October 29, about 6:30pm to 7:45pm Eastern for setup, the live half hour and a short wrap.",
        "Streaming: one tool that sends to Facebook and YouTube at once, a camera and microphone, and who runs it (Brittany or CEA). If the YouTube channel has never streamed, enable live streaming at least a day ahead; first-time approval can take up to 24 hours.",
        "Questions: a question field on the RSVP form, comments on the October 22 post, and consultant replies. Name who screens them before the show and who answers comments live.",
        "On screen: the Design Dollars fine print and the financing line. Answers stay inside the approved wording (Scott's two sentences; Every choice priced before we build; no build duration; no claim that the price cannot change).",
        "Who posts the replay and cuts the clips.",
        "RSVP form (Kelly): name, email, phone, text consent, your question.",
    ],
    "rides_in": [{
        "email": "dd2", "send": "Tuesday, October 27, 2026",
        "placement": "Event block near the end, after the Find Your Tier button and before the footer. dd2 already carries the long fine print in its footer. dd2 goes two days before the show, so the October 22 post, the Facebook event and the consultant invites on October 26 carry the call for questions.",
        "block": {
            "head": "Ask Scott and Deven, live",
            "text": "On Thursday, October 29, at 7pm Eastern, Scott Sleeme and Deven Sellers go live on Facebook and YouTube for about 30 minutes to answer your questions about SimplyMitchell and Design Dollars, from the $5,000 every home starts with to the $25,000 top tier. Send yours ahead of time, and they will answer as many as they can.",
            "cta": "Send a Question",
            "link": u(RSVP, "email", e),
            "fine": FINE}}],
    "social": [
        {"date": "Thursday, October 22, 2026", "channels": "Facebook, Instagram feed",
         "body": "Building a home on your land comes with questions. Ask the people who build them.\n\nOn Thursday, October 29, at 7pm Eastern, Scott Sleeme and Deven Sellers from Behind the Build go live on Facebook and YouTube to answer your questions about Mitchell Design Dollars and SimplyMitchell. What Design Dollars cover. When you choose. How building on your land works with zero down, zero closing costs and no construction loan.\n\nLeave your question in the comments, or send it here and we will remind you before we go live: " + RSVP + "\n\n" + DD_SHORT + " " + FINE,
         "link": u(RSVP, "facebook", e),
         "notes": "Image: the Behind the Build title card or Scott and Deven at the microphones (hosts, not a family photo, so it can be boosted). " + IG_NOTE.format(ig=u(RSVP, "instagram", e))},
        {"date": "Thursday, October 29, 2026", "channels": "Facebook, Instagram Stories",
         "body": "Tonight at 7pm Eastern, Scott Sleeme and Deven Sellers go live to answer your questions about Mitchell Design Dollars and SimplyMitchell. About 30 minutes. Watch on our Facebook page or YouTube channel, and ask in the comments.\n\n" + DD_SHORT + " Reserve by October 31, 2026.\n\n" + FINE,
         "link": "[YouTube Live link]",
         "notes": "Stories: link sticker to the YouTube Live link. Post the morning of the show."},
    ],
    "facebook_event": "Behind the Build Live: Your Design Dollars and SimplyMitchell Questions\nThursday, October 29, 2026, 7pm Eastern, about 30 minutes\nOnline: live here on Facebook and on the Mitchell Homes YouTube channel\n\nBuilding a home on your land comes with questions. Bring yours to the people who answer them every day.\n\nScott Sleeme, Owner and CEO of Mitchell Homes, and Deven Sellers, Executive Vice President, host Behind the Build. For one live half hour, they answer your questions about:\n\nMitchell Design Dollars. " + DD_DOC + " What they cover, and why you do not have to choose a single finish to lock them in.\n\nSimplyMitchell. Zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.\n\nSend your question ahead of time and we will remind you before we go live: " + RSVP + " . Or ask in the comments during the show.\n\n" + DD_LOCK + "\n\n" + FINE + " " + FIN,
    "facebook_event_notes": "One online Facebook event with Facebook Live as the location. Link: " + u(RSVP, "facebook_event", e) + " . Publish Thursday, October 22.",
    "gbp": {
        "title": "Behind the Build Live: Design Dollars Q&A",
        "body": "Building on your land comes with questions. On Thursday, October 29, at 7pm Eastern, Scott Sleeme and Deven Sellers go live on the Mitchell Homes Facebook page and YouTube channel to answer yours about Mitchell Design Dollars and SimplyMitchell. About 30 minutes. Tap Sign up to send a question and get a reminder.\n\n" + DD_SHORT + " " + FINE,
        "button": "Sign up",
        "link": u(RSVP, "gbp", e),
        "post_on": "All five Design Center profiles, Thursday, October 22. Event-type post, start October 29, 7pm, end 7:30pm.",
        "notes": "The event is online. If Google rejects an online event on a studio profile, post it as an Update instead or skip it."},
    "nextdoor": None,
    "nextdoor_when": "Skip: online event, not local.",
    "invite_when": "Monday, October 26, 2026. Every New Home Consultant to their own active leads.",
    "invite_text": "Hi [first name], [your name] with Mitchell Homes. Thursday at 7pm Eastern, Scott and Deven are live on Facebook and YouTube for 30 minutes answering questions about building on your land with Mitchell. Got one you want answered? Text it to me and I will pass it along.",
    "invite_email": {
        "subject": "Your question, answered live by Scott and Deven",
        "body": "Hi [first name],\n\nIf you have a question about building with Mitchell that you have not asked yet, here is a good place to ask it.\n\nOn Thursday, October 29, at 7pm Eastern, Scott Sleeme, our Owner and CEO, and Deven Sellers, our Executive Vice President, are going live on Facebook and YouTube for about 30 minutes to answer questions about Mitchell Design Dollars and SimplyMitchell.\n\nA quick refresher on both. " + DD_SCOTT + " Sign now, and your incentive is locked, but your tier will be decided when you make your selections. And with SimplyMitchell, building on land you own means " + SM + ".\n\nReply with your question and I will make sure it gets to them. Here is where to watch: [Facebook Live link] or [YouTube Live link]." + SIG + "\n\n" + FINE + " " + FIN},
    "reminder_when": "Wednesday, October 28, 2026. Builder Studio workflow, RSVPs with text consent only.",
    "reminder_text": "Mitchell Homes: Tomorrow at 7pm Eastern, Scott and Deven go live to answer your questions. About 30 minutes. Watch: [YouTube Live link] Reply STOP to opt out",
    "thanks_when": "Thursday, October 29, 2026, right after the show. Each consultant to their own leads who RSVPed; online sales counselors to the rest.",
    "thanks_text": "Thank you for joining Scott and Deven tonight, [first name]. If you missed it or want to watch again, the replay is here: [replay link]. Anything they did not get to, text me and I will answer it myself.",
    "followup_when": "Friday, October 30, 2026. The consultant (or an online sales counselor), to every RSVP.",
    "followup_email": {
        "subject": "The answers from last night, and October 31",
        "body": "Hi [first name],\n\nThank you for tuning in to Behind the Build Live last night. If you missed any of it, the full replay is here: [YouTube replay link]\n\nThe two questions we heard most: [question one, answered in a sentence] and [question two, answered in a sentence].\n\nIf you are planning to build, this is the week that matters. Reserve by Saturday, October 31, and your Design Dollars are locked: $5,000 on every Mitchell home, up to $25,000 the more you personalize. Your tier is set later, when you make your selections, and your reservation deposit is $150, which is all Mitchell receives until closing.\n\nSee the full ladder: " + u(DD, "followup", e) + "\n\nWant to talk it through before Saturday? Reply with a time, or call me at the number below." + SIG + "\n\n" + FINE},
    "extra_texts": [],
    "notes": [
        "October 29 already has the deadline week text to active leads. For a consultant's own active leads who RSVPed, the thank-you text that night stands in for it; skip the deadline text for them, since Friday's follow-up carries the October 31 date.",
        "Clips: one question per Short, titled with the question, per the YouTube plan.",
    ],
    "schedule": sched([
        ("2026-10-22", "Thursday, October 22", "Social", "Post 1, the question call (Facebook, Instagram feed). Publish the online Facebook event.", "Marketing"),
        ("2026-10-22", "Thursday, October 22", "Google", "Event post on all five profiles (or Update if Google rejects an online event)", "Marketing"),
        ("2026-10-26", "Monday, October 26", "Sales team", "Personal invite text and email to own active leads", "New Home Consultants"),
        ("2026-10-27", "Tuesday, October 27", "Email", "Event block in dd2", "Marketing"),
        ("2026-10-28", "Wednesday, October 28", "Text", "Reminder to RSVPs only", "Builder Studio workflow"),
        ("2026-10-29", "Thursday, October 29", "Social", "Post 2, tonight at 7 (Facebook, Instagram Stories)", "Marketing"),
        ("2026-10-29", "Thursday, October 29", "Event", "Live at 7pm Eastern; thank-you text after the show", "Scott and Deven; consultants"),
        ("2026-10-30", "Friday, October 30", "Sales team", "Follow-up email with the replay and the October 31 date", "New Home Consultants, online sales counselors"),
    ]),
})

# ---------------------------------------------------------------- E3
e = "e3"
EVENTS.append({
    "id": e,
    "name": "Building on Your Land 101",
    "tier": "later",
    "date": TBD,
    "time": "10am to 11:30am",
    "where": ALL5 + " A free fall edition of the Homebuyer Roadmap to Success class.",
    "audience": "People who own land, have family land, or are shopping for land to build on: the landowner and looking for land segments, quiz takers who answered either way, and anyone who clicked a Four Buyers email or page.",
    "what": [
        "A one-hour class on what to know before you build: perc tests and soil, wells and septic, road access and utilities.",
        "How the money works: SimplyMitchell on land you own (zero down, zero closing costs, no construction loan), and what to plan for if you are still buying.",
        "Thirty minutes of open questions, then time with a New Home Consultant for anyone who brings a parcel address, survey or plat.",
    ],
    "why": "Puts the Four Buyers argument (your land is worth more than you think) in a room with a New Home Consultant the week fb1 and fb5 land, using a class format Mitchell already runs.",
    "confirm": [
        "Approve the date and which studios host; seats per studio (room, chairs, a screen).",
        "Presenter at each studio: a New Home Consultant, plus someone who can speak to perc tests, wells, septic and site work.",
        "The class deck: CEA can draft it from the Homebuyer Roadmap to Success, Well and Septic and Purchasing Land 101 episodes for Mitchell to approve.",
        "SimplyMitchell for buyers still purchasing land: confirm whether the terms are the same before the class answers that question (open flag on the No Land page).",
        "Food: none promised. If Mitchell wants coffee, add one line to the Facebook event and the invite email.",
        "RSVP form (Kelly): name, phone, email, studio, own land or still looking, county (optional), text consent.",
    ],
    "rides_in": [],
    "rides_in_note": "Banked for winter: no email block this fall. The blocks first written for fb1 and fb5 are kept below for when Mitchell sets the date.",
    "banked_rides_in": [
        {"email": "fb1", "send": TBD,
         "placement": "Event block near the end, after the Downey quote and before the Design Dollars band.",
         "block": {
             "head": "Building on Your Land 101, Saturday, [date]",
             "text": "Before a home goes on your land, a few things decide the plan: perc tests and soil, well and septic, road access and utilities, and how the money works. Spend 90 minutes with us at your nearest Mitchell Design Center, from 10am to 11:30am, and leave with a clear list of what to check on your land next.",
             "cta": "Save My Seat",
             "link": u(RSVP, "email", e)}},
        {"email": "fb5", "send": TBD + " (and fb5c for the Carolinas)",
         "placement": "Event block after the floor plans line, before the Design Dollars band. fb5 is on hold until the plan guide email is built; if it slips past [date], this block moves to the consultant invites only.",
         "block": {
             "head": "Shopping for land? Start with this class.",
             "text": "On Saturday, [date], from 10am to 11:30am, every Mitchell Design Center is hosting Building on Your Land 101: what to check before you buy, from perc tests and soil to well, septic, access and utilities. It is free, and you do not need to own land yet to come.",
             "cta": "Save My Seat",
             "link": u(RSVP, "email", e)}},
    ],
    "social": [
        {"date": TBD + " (5 days before)", "channels": "Facebook, Instagram feed",
         "body": "Land is silent until you give it a voice. Before it can carry a home, a few questions need answers.\n\nWill the soil perc? Where does the well go? Can a driveway and power reach the homesite? How does the money work when the land is already yours?\n\nBuilding on Your Land 101 is a free class at every Mitchell Design Center on Saturday, [date], from 10am to 11:30am. Bring your parcel address and your questions. Still looking for land? Come anyway. This is the class to take before you buy.\n\nSave a seat: " + RSVP + "\n\n#BuildOnYourLand #MitchellHomes",
         "link": u(RSVP, "facebook", e),
         "notes": "Image: a Mitchell home alone on open land, e.g. " + M + "2024/7/5/1_GuQrrFW.jpg . " + BOOST + " " + IG_NOTE.format(ig=u(RSVP, "instagram", e))},
        {"date": TBD + " (the day before)", "channels": "Facebook, Instagram Stories",
         "body": "Tomorrow morning, 10am to 11:30am: Building on Your Land 101 at every Mitchell Design Center. Perc tests and soil, wells and septic, access and utilities, and how the money works with SimplyMitchell. Free. RSVP so we have a seat ready for you: " + RSVP,
         "link": u(RSVP, "facebook", e),
         "notes": "Stories: link sticker with " + u(RSVP, "instagram", e) + " . " + BOOST},
    ],
    "facebook_event": "Building on Your Land 101 at the Mitchell Homes [city] Design Center\nSaturday, [date], 10am to 11:30am\n[studio address]\n\nOwning land is the hardest part of building a custom home, and the most misunderstood. This free 90-minute class is the fall edition of Mitchell's Homebuyer Roadmap to Success, built around the questions landowners ask us first:\n\nPerc tests and soil: what they tell you about your homesite.\nWells and septic: what your land needs, and how it shapes the plan.\nAccess and utilities: driveways, power and water, and where the home can sit.\nThe money: how SimplyMitchell works on land you own, with " + SM + ", and what to plan for if you are still buying.\n\nBring your parcel address, a survey or plat if you have one, and your questions. Stay after for time with a New Home Consultant.\n\nStill looking for land? You are welcome too. This is the class to take before you buy.\n\nRSVP: " + RSVP + "\n\nCannot make it? Watch Behind the Build: Well and Septic https://www.youtube.com/watch?v=zWwtw8qgp4w and Purchasing Land 101 https://www.youtube.com/watch?v=trgJ8maymOA\n\n" + FIN,
    "facebook_event_notes": "One Facebook event per Design Center; only [city] and [studio address] change. Link: " + u(RSVP, "facebook_event", e) + " . Cover image: land or a finished home, no people.",
    "gbp": {
        "title": "Building on Your Land 101: Free Class",
        "body": "Own land, or shopping for it? Join us at our [city] Design Center on Saturday, [date], from 10am to 11:30am for Building on Your Land 101, a free class on what to know before you build: perc tests and soil, wells and septic, access and utilities, and how the money works with SimplyMitchell. Bring your parcel address and your questions. Tap Sign up to save a seat.",
        "button": "Sign up",
        "link": u(RSVP, "gbp", e),
        "post_on": "All five Design Center profiles, 5 days before. Event-type post, start [date], 10am, end 11:30am.",
        "notes": "Image: land or a finished Mitchell home, no people."},
    "nextdoor": "Own land, or thinking about buying some to build on?\n\nMitchell Homes is hosting a free class, Building on Your Land 101, at our [city] Design Center ([studio address]) on Saturday, [date], from 10am to 11:30am. We will cover perc tests and soil, wells and septic, access and utilities, and how the money works.\n\nBring your parcel address and your questions. RSVP: " + u(RSVP, "nextdoor", e) + "\n\nMitchell Homes, building on your land since 1992.",
    "nextdoor_when": TBD + " (4 days before), from each Design Center's Nextdoor business page. Fair housing: never name a county or call an area a good place to live.",
    "invite_when": TBD + " (2 days before). Every New Home Consultant to their own active leads who own land or are looking for it.",
    "invite_text": "Hi [first name], [your name] with Mitchell Homes. This Saturday, [date], 10 to 11:30, we are holding a free class at our [city] Design Center on building on your land: perc, well and septic, access and the money. Bring your parcel address. Can I save you a seat?",
    "invite_email": {
        "subject": "Saturday morning: Building on Your Land 101",
        "body": "Hi [first name],\n\nWhen we talk about your land, the same questions come up every time. Will it perc? Where does the well go? Can we get a driveway and power to the homesite? How does the money work?\n\nThis Saturday, [date], from 10am to 11:30am, we are answering all of them in one free class at our [city] Design Center: Building on Your Land 101. Bring your parcel address, and a survey or plat if you have one, and stay after so we can look at your land together.\n\nIf you are still looking for land, come anyway. It is the class I wish every buyer took before they bought.\n\nReply and I will save you a seat." + SIG},
    "reminder_when": TBD + " (the day before). Builder Studio workflow, RSVPs with text consent only.",
    "reminder_text": "Mitchell Homes: See you tomorrow, Sat [date], 10 to 11:30am, for Building on Your Land 101 at our [city] Design Center, [studio address]. Bring your parcel address. Reply STOP to opt out",
    "thanks_when": TBD + " (class day), by early afternoon. The New Home Consultant who met each attendee.",
    "thanks_text": "Thank you for coming this morning, [first name]. If a question about your land comes up this weekend, text me. I will send the class notes tomorrow with the next step for your land.",
    "followup_when": TBD + " (the day after; schedule it Saturday). The New Home Consultant.",
    "followup_email": {
        "subject": "Your land, next steps",
        "body": "Hi [first name],\n\nThank you for joining Building on Your Land 101 yesterday. Here is a short recap, and the next step for you.\n\nWhat to gather: your parcel address, any survey or plat, and anything you have on the soil, perc or well.\nWhat to check: soil and perc, well and septic, road access and utilities.\nHow the money works: on land you own, SimplyMitchell means " + SM + ".\n\nYour next step: [a land walk at your property, or a Design Center visit to walk the plans]. Reply with two times that work and I will set it up.\n\nTwo Behind the Build episodes worth watching this week:\nWell and Septic: https://www.youtube.com/watch?v=zWwtw8qgp4w\nPurchasing Land 101: https://www.youtube.com/watch?v=trgJ8maymOA\n\nSee what your land can build: " + u(SMH + "/land", "followup", e) + "\n[Carolinas: " + u(SMH + "/onyourland", "followup", e) + " . Still looking for land: " + u(SMH + "/no-land", "followup", e) + " , or /no-land-carolinas.]\n\n" + FIN + SIG},
    "extra_texts": [],
    "notes": [
        "[date] already has a consultant text to landowner leads in the cadence. For those leads, this invite text replaces it, so nobody gets two texts that day.",
        "/land covers Virginia and Southern Maryland only; Carolinas attendees get /onyourland. Use /no-land only once its plan guide email is fixed.",
        "Fair housing: presenters and posts never recommend a county or describe an area as desirable.",
    ],
    "schedule": sched([
        ("", "Date to be set (5 days before)", "Social", "Post 1 (Facebook, Instagram feed). Publish the five Facebook events.", "Marketing"),
        ("", "Date to be set (5 days before)", "Google", "Event post on all five profiles", "Marketing"),
        ("", "Date to be set (4 days before)", "Nextdoor", "Post from each Design Center page", "Marketing"),
        ("", "Date to be set (2 days before)", "Sales team", "Personal invite text and email (the text replaces that day's landowner text)", "New Home Consultants"),
        ("", "Date to be set (the day before)", "Social", "Post 2 (Facebook, Instagram Stories)", "Marketing"),
        ("", "Date to be set (the day before)", "Text", "Reminder to RSVPs only", "Builder Studio workflow"),
        ("", "Date to be set (class day)", "Event", "Class, 10am to 11:30am; thank-you text", "Presenters, New Home Consultants"),
        ("", "Date to be set (the day after)", "Sales team", "Follow-up email with recap and next step", "New Home Consultants"),
    ]),
})

# ---------------------------------------------------------------- E4
e = "e4"
WIL = "42 Waterford Business Center Way, Suite A, Belville, NC 28451"
E4_TEXT = "Mitchell Homes: Open house Sat [date], 10 to 3, Wilmington Design Center, Belville. Bring your land questions. {link} Reply STOP to opt out"
EVENTS.append({
    "id": e,
    "name": "Wilmington Design Center Open House",
    "tier": "later",
    "date": TBD,
    "time": "10am to 3pm",
    "where": "Mitchell Homes Wilmington Design Center, " + WIL + " (address as listed on the live Design Dollars page).",
    "audience": "North and South Carolina contacts, led by the Wilmington division: coastal North Carolina and Dillon, Horry, Marion and Marlboro counties in South Carolina. Landowners, buyers still looking for land, Carolinas quiz takers and active leads.",
    "what": [
        "Walk the Wilmington Design Center: cabinets, countertops, flooring, tile, lighting and hardware in person.",
        "Sit with a New Home Consultant about your land, more than 40 floor plans, and how SimplyMitchell works: zero down, zero closing costs, no construction loan.",
        "See the Design Dollars ladder with a Design Consultant: $5,000 on every home, up to $25,000 the more you personalize.",
    ],
    "why": "Gives the Carolinas launch of the Four Buyers campaign a physical place to land, and introduces the coast and the four South Carolina counties to the studio that opened September 11.",
    "confirm": [
        "Approve the date and 10am to 3pm hours. Wilmington has one New Home Consultant; name who joins (a Design Consultant, the New Home Sales Associate, or a Raleigh consultant).",
        "Design Dollars: the Facebook event and follow-up name the offer without a reserve-by date. Approve the reserve-by date for that month by [date], or CEA removes the Design Dollars lines from every E4 piece.",
        "The one text on [date]: confirm the audience. The brief says all Carolinas contacts with text consent; Mitchell may prefer to limit it to the Wilmington division, since Belville is a long drive from the Triangle.",
        "Refreshments or a giveaway: none promised. If Mitchell wants either, add one line to the Facebook event and the Nextdoor post.",
        "Parking and door signage for Suite A.",
        "RSVP form (Kelly), optional for a drop-in event: name, phone, email, own land or still looking, county, text consent.",
    ],
    "rides_in": [],
    "rides_in_note": "No email block, as briefed. The Wilmington profile, social, Nextdoor, consultant invites and one text carry it. Banked for winter, with its text, until Mitchell sets the date.",
    "social": [
        {"date": TBD + " (5 days before)", "channels": "Facebook, Instagram feed",
         "body": "Building on your land near the coast? Come see where it starts.\n\nOur Wilmington Design Center in Belville is hosting an open house on Saturday, [date], from 10am to 3pm. Walk the cabinets, counters, tile and lighting in person, look through more than 40 floor plans, and sit down with a New Home Consultant about your land.\n\nOwn land in coastal North Carolina or in Dillon, Horry, Marion or Marlboro County, South Carolina? Ask how SimplyMitchell works: " + SM + ".\n\nDrop in any time, or RSVP and we will have a time ready for you: " + RSVP + "\n\n#BuildOnYourLand #MitchellHomes #WilmingtonNC",
         "link": u(RSVP, "facebook", e),
         "notes": "Image: the Wilmington Design Center interior (Brittany's photos), no people. " + BOOST + " " + IG_NOTE.format(ig=u(RSVP, "instagram", e))},
        {"date": TBD + " (the day before)", "channels": "Facebook, Instagram Stories",
         "body": "Tomorrow, 10am to 3pm: open house at the Mitchell Homes Wilmington Design Center, " + WIL + ". Bring your land questions, your saved photos and your plans. Drop in any time: " + RSVP,
         "link": u(RSVP, "facebook", e),
         "notes": "Stories: link sticker with " + u(RSVP, "instagram", e) + " , plus a map sticker on the studio. " + BOOST},
    ],
    "facebook_event": "Open House at the Mitchell Homes Wilmington Design Center\nSaturday, [date], 10am to 3pm\n" + WIL + "\n\nIf you have been picturing a home on land you own, or land you are still looking for, this is the place to start.\n\nDrop in any time between 10 and 3 to:\nWalk the Design Center and see cabinets, countertops, flooring, tile, lighting and hardware in person.\nLook through more than 40 floor plans, from 1,000 to 3,000 square feet.\nSit down with a New Home Consultant about your land and how SimplyMitchell works: " + SM + ".\nSee the Mitchell Design Dollars ladder with a Design Consultant. " + DD_DOC + " [Reserve by date, once Mitchell approves it for that month.]\n\nThe Wilmington Design Center serves coastal North Carolina and Dillon, Horry, Marion and Marlboro counties in South Carolina.\n\nRSVP (optional): " + RSVP + " . Questions? Call a New Home Consultant at (984) 331-5468.\n\n" + FINE + " One offer per contract. " + FIN,
    "facebook_event_notes": "One event, Wilmington address. Link: " + u(RSVP, "facebook_event", e) + " . Publish 9 days before. If the Design Dollars date for that month is not approved by [date], delete the Design Dollars sentence, the bracket and the Design Dollars fine print.",
    "gbp": {
        "title": "Open House at our Wilmington Design Center",
        "body": "Join us Saturday, [date], from 10am to 3pm, for an open house at our Wilmington Design Center in Belville. Walk the finishes in person, look through more than 40 floor plans, and sit down with a New Home Consultant about building on your land. Ask how SimplyMitchell works: zero down, zero closing costs and no construction loan. Drop in any time, or tap Sign up to RSVP.",
        "button": "Sign up",
        "link": u(RSVP, "gbp", e),
        "post_on": "Wilmington NC profile only, 9 days before. Event-type post, start [date], 10am, end 3pm.",
        "notes": "Image: the studio interior, no people."},
    "nextdoor": "Thinking about building a home on land you own, or land you are still looking for?\n\nMitchell Homes is hosting an open house at our Wilmington Design Center, 42 Waterford Business Center Way, Suite A, in Belville, on Saturday, [date], from 10am to 3pm. Walk the finishes in person, look through more than 40 floor plans, and bring your land questions to a New Home Consultant.\n\nDrop in any time. RSVP if you would like a time set aside: " + u(RSVP, "nextdoor", e) + "\n\nMitchell Homes, building on your land since 1992.",
    "nextdoor_when": TBD + " (4 days before), from the Wilmington Design Center's Nextdoor business page.",
    "invite_when": TBD + " (5 days before). Raleigh and Wilmington New Home Consultants to their own active leads.",
    "invite_text": "Hi [first name], [your name] with Mitchell Homes. We are hosting an open house at our Wilmington Design Center in Belville this Saturday, [date], 10 to 3. Come walk the finishes and bring your land questions. Want me to set aside a time for you?",
    "invite_email": {
        "subject": "Open house Saturday in Belville",
        "body": "Hi [first name],\n\nIf you have been thinking about the home you want to build, this Saturday is an easy way to take the next step.\n\nOn Saturday, [date], from 10am to 3pm, we are hosting an open house at our Wilmington Design Center, 42 Waterford Business Center Way, Suite A, in Belville. You can walk the cabinets, counters, tile and lighting in person, look through more than 40 floor plans, and bring your land questions to a New Home Consultant.\n\nIf you own land, ask about SimplyMitchell: " + SM + ". If you are still looking, you can start designing now and bring us the lot when you find it.\n\nDrop in any time, or reply and I will set aside a time for you." + SIG + "\n\n" + FIN},
    "reminder_when": TBD + " (the day before). Builder Studio workflow, RSVPs with text consent only.",
    "reminder_text": "Mitchell Homes: See you tomorrow, Sat [date], 10am to 3pm, at our Wilmington Design Center, 42 Waterford Business Center Way, Suite A, Belville. Reply STOP to opt out",
    "thanks_when": TBD + " (open house day), by 6pm. Whoever each guest met.",
    "thanks_text": "Thank you for coming by the Wilmington Design Center today, [first name]. I enjoyed hearing about [their land or plan]. I will follow up tomorrow with the plans and numbers we talked about. Text me any time.",
    "followup_when": TBD + " (the day after; schedule it Saturday). The New Home Consultant.",
    "followup_email": {
        "subject": "From Saturday at the Wilmington Design Center",
        "body": "Hi [first name],\n\nThank you for coming to the open house yesterday. It was good to talk about [their land, plan or favorite finish].\n\nAs promised, here is what we talked about:\n[plans that fit, with links]\n[selections they liked, priced if they asked]\n\nA few things worth having in one place. With SimplyMitchell, building on land you own means " + SM + ". See how it works: " + u(SMH + "/onyourland", "followup", e) + "\n\n" + DD_SHORT + " [Reserve by date, once Mitchell approves it for that month.]\n\nIf you would like to see a Mitchell home on the coast first, Rob and Kat Cuomo built theirs in Wilmington: https://www.youtube.com/watch?v=jMSBzlcQ4uU\n\nReady for the next step? Reply with a time for a land walk or a second visit." + SIG + "\n\n" + FINE + " " + FIN},
    "extra_texts": [],
    "banked_extra_texts": [{
        "date": TBD + " (3 days before)",
        "audience": "North and South Carolina contacts with text consent, minus anyone who already RSVPed, anyone under contract, past Mitchell homeowners, active leads their consultant invited on [date], and E5 RSVPs (they get the E5 reminder that day). The only bulk text that week.",
        "body": E4_TEXT.replace("{link}", "[trigger link]"),
        "link": u(RSVP, "sms", e),
        "notes": "Builder Studio bulk SMS between 10am and 7pm. Make the link a Builder Studio trigger link to the tracked RSVP URL so it stays short."}],
    "notes": [
        "South Carolina is served from the Wilmington Design Center; keep the two geography claims separate in any added copy.",
        "The Cuomo video is cleared for organic and email; quote them only word for word from the live pages.",
    ],
    "schedule": sched([
        ("", "Date to be set (9 days before)", "Google", "Event post on the Wilmington profile. Publish the Facebook event.", "Marketing"),
        ("", "Date to be set (5 days before)", "Social", "Post 1 (Facebook, Instagram feed)", "Marketing"),
        ("", "Date to be set (5 days before)", "Sales team", "Personal invite text and email", "Raleigh and Wilmington New Home Consultants"),
        ("", "Date to be set (4 days before)", "Nextdoor", "Post from the Wilmington page", "Marketing"),
        ("", "Date to be set (3 days before)", "Text", "The one bulk text to Carolinas contacts with text consent", "Marketing"),
        ("", "Date to be set (the day before)", "Social", "Post 2 (Facebook, Instagram Stories)", "Marketing"),
        ("", "Date to be set (the day before)", "Text", "Reminder to RSVPs only", "Builder Studio workflow"),
        ("", "Date to be set (open house day)", "Event", "Open house, 10am to 3pm; thank-you text", "Wilmington team"),
        ("", "Date to be set (the day after)", "Sales team", "Follow-up email", "New Home Consultants"),
    ]),
})

# ---------------------------------------------------------------- E5
e = "e5"
EVENTS.append({
    "id": e,
    "name": "The Gathering Place Live: Building Your Getaway",
    "tier": "later",
    "date": TBD,
    "time": "7pm Eastern, 30 minutes",
    "where": "Online: live on the Mitchell Homes Facebook page and YouTube channel, the same setup as Behind the Build Live.",
    "audience": "People planning a getaway, a family retreat, a second home or the place they will retire, at the lake, on the coast or in the mountains: quiz takers who chose Smith Mountain Lake, Lake Gaston, the Shenandoah Valley or the Eastern Shore and Outer Banks, contacts interested in those areas, and past homeowners thinking about a second place.",
    "what": [
        "A 30-minute live conversation about building a getaway, second home or retirement home at the lake, on the coast or in the mountains.",
        "What to look at first on a lake, coastal or mountain lot, and how building works when you live hours away, with weekly communication from groundbreaking to move-in.",
        "Why second homes are where banks get strict, and how SimplyMitchell answers it: no construction loan, because Mitchell self-funds every build. Live questions throughout.",
    ],
    "why": "Gives retreat and retirement buyers, the audience for The Gathering Place Portrait, a reason to talk to Mitchell the same night hp4 lands, and answers their biggest objection, second-home financing, out loud.",
    "confirm": [
        "Host: Scott and Deven, or a New Home Consultant who builds at the lake and on the coast. [date], about 6:30pm to 7:45pm Eastern.",
        "Second homes: confirm the SimplyMitchell terms for a second home or retirement home before the show, so live answers match.",
        "Which areas to name on air (the quiz uses Smith Mountain Lake, Lake Gaston, the Shenandoah Valley and the Eastern Shore and Outer Banks).",
        "Streaming setup and who runs it (same as E2), with the financing line on screen.",
        "RSVP form (Kelly): name, email, phone, text consent, where you are thinking of building, your question.",
    ],
    "rides_in": [],
    "rides_in_note": "Banked for winter: no email block this fall. The block first written for hp4 is kept below for when Mitchell sets the date.",
    "banked_rides_in": [{
        "email": "hp4", "send": TBD,
        "placement": "Event block after the Take the Quiz button and before the footer. hp4's job is the quiz, so the block stays short and sits under the button.",
        "block": {
            "head": "Tonight at 7: The Gathering Place, live",
            "text": "Tonight at 7pm Eastern, join us on Facebook or YouTube for a 30-minute live conversation about building the getaway, the second home or the place you plan to retire, at the lake, on the coast or in the mountains. Bring your questions, especially the hard ones about second-home financing.",
            "cta": "Join Us Tonight",
            "link": u(RSVP, "email", e)}}],
    "social": [
        {"date": TBD + " (2 days before)", "channels": "Facebook, Instagram feed",
         "body": "Some homes are built for every day. Some are built for the long table, the full-house weekend and the years after work.\n\nIf you are planning a getaway, a second home or the place you will retire, at the lake, on the coast or in the mountains, join us live on Thursday, [date], at 7pm Eastern. In 30 minutes we will cover what to look at first on a lake, coastal or mountain lot, how building works when you live hours away, and why the second home banks make hard, Mitchell makes simple.\n\nWatch on Facebook or YouTube. RSVP for a reminder: " + RSVP + "\n\n#BuildOnYourLand #MitchellHomes",
         "link": u(RSVP, "facebook", e),
         "notes": "Image: a real Mitchell home by the water, e.g. the hp4 hero " + M + "2026/3/24/10_mwFjkrl.jpg . Never the painted portrait. " + BOOST + " " + IG_NOTE.format(ig=u(RSVP, "instagram", e))},
        {"date": TBD + " (the day of the show)", "channels": "Facebook, Instagram Stories",
         "body": "Tonight at 7pm Eastern: The Gathering Place, live. Thirty minutes on building a getaway, second home or retirement home at the lake, on the coast or in the mountains. Watch here on Facebook or on our YouTube channel, and ask your questions live.",
         "link": "[YouTube Live link]",
         "notes": "Stories: link sticker to the YouTube Live link. Post the morning of the show."},
    ],
    "facebook_event": "The Gathering Place Live: Building Your Getaway\nThursday, [date], 7pm Eastern, 30 minutes\nOnline: live here on Facebook and on the Mitchell Homes YouTube channel\n\nSome homes are built for every day. Some are built for the long table, the full-house weekend and the place you plan to retire.\n\nIf you are planning a getaway, a family retreat, a second home or a home for retirement, at the lake, on the coast or in the mountains, spend 30 minutes with us. We will talk through:\n\nWhat to look at first on a lake, coastal or mountain lot.\nHow building works when you live hours away, with weekly communication from groundbreaking to move-in.\nWhy second homes are where banks get strict, and how SimplyMitchell answers it: no construction loan to qualify for, because Mitchell self-funds every build.\n\nAsk your questions live in the comments, or send them ahead: " + RSVP + "\n\n" + FIN,
    "facebook_event_notes": "One online Facebook event with Facebook Live as the location. Link: " + u(RSVP, "facebook_event", e) + " . Publish 2 days before.",
    "gbp": {
        "title": "The Gathering Place: Build Your Getaway",
        "body": "Planning a getaway, a second home or the place you will retire, at the lake, on the coast or in the mountains? Join Mitchell Homes live on Thursday, [date], at 7pm Eastern, on our Facebook page and YouTube channel. In 30 minutes we cover what to look at first on a lake, coastal or mountain lot, building from hours away, and how SimplyMitchell removes the construction loan. Tap Sign up for a reminder.",
        "button": "Sign up",
        "link": u(RSVP, "gbp", e),
        "post_on": "All five Design Center profiles, 2 days before. Event-type post, start [date], 7pm, end 7:30pm.",
        "notes": "Online event. If Google rejects it on a studio profile, post as an Update or skip."},
    "nextdoor": None,
    "nextdoor_when": "Skip: online event, not local.",
    "invite_when": TBD + " (2 days before). New Home Consultants to their own active leads who mentioned a lake, the coast or the mountains, or whose quiz answer was a getaway, retreat or retirement.",
    "invite_text": "Hi [first name], [your name] with Mitchell Homes. You mentioned [the lake / the coast / the mountains]. Thursday at 7pm Eastern we are live on Facebook and YouTube for 30 minutes on building a getaway or retirement home. Want me to send you the link?",
    "invite_email": {
        "subject": "Thursday at 7: building the getaway",
        "body": "Hi [first name],\n\nYou mentioned [the lake, the coast or the mountains] when we talked, so I wanted you to hear about this first.\n\nOn Thursday, [date], at 7pm Eastern, we are going live on Facebook and YouTube for 30 minutes on building a getaway, a second home or the place you plan to retire. We will cover what to look at first on a lake, coastal or mountain lot, how building works when you live hours away, and why second homes are where banks get strict.\n\nThat last one matters. Mitchell self-funds every build, so there is no construction loan to qualify for. The second home banks make hard, Mitchell makes simple.\n\nWatch here: [Facebook Live link] or [YouTube Live link]. If you have a question you want answered on air, reply and I will pass it along." + SIG + "\n\n" + FIN},
    "reminder_when": TBD + " (the day before). Builder Studio workflow, RSVPs with text consent only.",
    "reminder_text": "Mitchell Homes: Tomorrow at 7pm Eastern, The Gathering Place, live: 30 minutes on building your getaway. Watch: [YouTube Live link] Reply STOP to opt out",
    "thanks_when": TBD + ", right after the show. Each consultant to their own leads who RSVPed; online sales counselors to the rest.",
    "thanks_text": "Thank you for joining us tonight, [first name]. The replay is here if you want to share it with whoever you are building the getaway with: [replay link]. Any question we did not get to, text me.",
    "followup_when": TBD + " (the day after). The consultant (or an online sales counselor), to every RSVP.",
    "followup_email": {
        "subject": "The getaway, one step closer",
        "body": "Hi [first name],\n\nThank you for joining The Gathering Place live last night. The full replay is here: [YouTube replay link]\n\nThe short version: start with the lot itself, from soil and septic to access and utilities. Building from hours away works because you hear from us every week from groundbreaking to move-in. And with Mitchell there is no construction loan to qualify for, because Mitchell self-funds every build.\n\nIf you have not taken the Home Portrait quiz yet, choose your lake, coast or mountain region and tell us what the home is for. Eight questions, about 90 seconds: " + u(QUIZ, "followup", e) + "\n\n[Carolinas contacts only: We are also hosting an open house at our Wilmington Design Center in Belville tomorrow, Saturday, [date], from 10am to 3pm. Come by any time.]\n\nOr reply with a time, and we can talk about your land, or the land you are still looking for.\n\n" + FIN + SIG},
    "extra_texts": [],
    "notes": [
        "The invitation never shows or describes the painted Home Portrait; the follow-up names the quiz only.",
        "Hosts describe what to check on a lot, never which areas are better places to live (fair housing).",
        "hp4 goes the morning of the show, so most RSVPs come from the Tuesday post, the Facebook event and the consultant invites; the day-before reminder only reaches those.",
    ],
    "schedule": sched([
        ("", "Date to be set (2 days before)", "Social", "Post 1 (Facebook, Instagram feed). Publish the online Facebook event.", "Marketing"),
        ("", "Date to be set (2 days before)", "Google", "Event post on all five profiles (or Update)", "Marketing"),
        ("", "Date to be set (2 days before)", "Sales team", "Personal invite text and email to lake, coast and mountain leads", "New Home Consultants"),
        ("", "Date to be set (the day before)", "Text", "Reminder to RSVPs only", "Builder Studio workflow"),
        ("", "Date to be set (the day of the show)", "Social", "Post 2, tonight at 7 (Facebook, Instagram Stories)", "Marketing"),
        ("", "Date to be set (the day of the show)", "Event", "Live at 7pm Eastern; thank-you text after the show", "Host; consultants"),
        ("", "Date to be set (the day after)", "Sales team", "Follow-up email with the replay (and Saturday's open house for Carolinas contacts)", "New Home Consultants, online sales counselors"),
    ]),
})

# ---------------------------------------------------------------- E6
e = "e6"
EVENTS.append({
    "id": e,
    "name": "Realtor Lunch and Learn",
    "tier": "add",
    "date": "Wednesday, November 18, 2026",
    "time": "11:30am to 1pm",
    "where": ALL5,
    "audience": "Real estate agents and brokers in each Design Center's market: land listing agents first, then agents who have already sent Mitchell a buyer.",
    "what": [
        "How building on a client's land works with Mitchell: SimplyMitchell (zero down, zero closing costs, no construction loan) and one closing.",
        "Mitchell Design Dollars ($5,000 on every home, up to $25,000) and the Home Portrait quiz agents can send to clients, plus how to refer.",
        "Mitchell's realtor incentive program, on terms Mitchell confirms, then open questions and a walk through the Design Center.",
    ],
    "why": "Turns agents who meet landowners every week into a referral source for all three campaigns, at the cost of a room and a presenter at each studio.",
    "confirm": [
        "Realtor incentive terms, in writing, before any invitation goes out (the same open question as the October realtor email, re1).",
        "Lunch: the event name promises it. Confirm lunch and a budget at each studio, or rename the event Realtor Learn and Tour everywhere. Copy marks it " + LUNCH,
        "Continuing education credit: not offered and not mentioned anywhere. Offering it would need course approval first.",
        "Presenter at each studio (a New Home Consultant; Scott or Deven at one studio if possible) and room capacity.",
        "The agent list: the realtor segment in Builder Studio by division, land listing agents first.",
        "Design Dollars after October 31: these pieces name the offer without a reserve-by date. Confirm the program continues in November and approve the November date.",
        "RSVP form (Kelly): name, brokerage, email, phone, studio, text consent.",
    ],
    "rides_in": [{
        "email": "rb2", "send": "Wednesday, November 11, 2026",
        "placement": "Event block near the end of rb2 (When your land listing needs a picture), after the Send Your Buyer the Home Portrait button and before the incentive line. rb2 has no Design Dollars footer, so the short fine print sits right under this block.",
        "block": {
            "head": "Lunch and Learn at your nearest Mitchell Design Center",
            "text": "On Wednesday, November 18, from 11:30am to 1pm, each Mitchell Design Center is hosting agents for a short session on how building on a client's land works: SimplyMitchell, Design Dollars ($5,000 on every home, up to $25,000), the Home Portrait quiz, and how to refer. You will also hear the terms of Mitchell's realtor incentive program, and lunch is on us. [Lunch: Mitchell to confirm.]",
            "cta": "Save Your Seat",
            "link": u(RSVP, "email", e),
            "fine": FINE}}],
    "social": [
        {"date": "Wednesday, November 11, 2026", "channels": "Facebook, Instagram feed, LinkedIn",
         "body": "Your client owns land. We build the home on it.\n\nOn Wednesday, November 18, from 11:30am to 1pm, every Mitchell Homes Design Center is hosting a Realtor Lunch and Learn. " + LUNCH + " In 90 minutes: how building on a client's land works with Mitchell, from SimplyMitchell (zero down, zero closing costs, no construction loan) to Mitchell Design Dollars and the Home Portrait quiz, how to refer, and the terms of our realtor incentive program.\n\nFredericksburg, Richmond, Newport News, Raleigh and Wilmington. Save your seat: " + RSVP + "\n\n" + DD_SHORT + " " + FINE,
         "link": u(RSVP, "facebook", e),
         "notes": "Image: a Design Center interior, e.g. " + M + "2023/3/24/Richmond_Design_Studio.jpg , no people. " + BOOST + " LinkedIn: same caption with " + u(RSVP, "linkedin", e) + " . " + IG_NOTE.format(ig=u(RSVP, "instagram", e))},
        {"date": "Monday, November 16, 2026", "channels": "Facebook, Instagram Stories, LinkedIn",
         "body": "This Wednesday, 11:30am to 1pm: Realtor Lunch and Learn at every Mitchell Homes Design Center. " + LUNCH + " Bring your questions about clients who own land, or are about to buy it. Save your seat: " + RSVP,
         "link": u(RSVP, "facebook", e),
         "notes": "Stories: link sticker with " + u(RSVP, "instagram", e) + " . LinkedIn: " + u(RSVP, "linkedin", e)},
    ],
    "facebook_event": "Realtor Lunch and Learn at the Mitchell Homes [city] Design Center\nWednesday, November 18, 2026, 11:30am to 1pm\n[studio address]\n\nFor real estate agents and brokers. " + LUNCH + "\n\nYour clients who own land, or are about to buy it, usually hit the same wall: how do we build on it without a construction loan and a second closing? Mitchell answers that question every day. Spend 90 minutes with us and leave ready to answer it too.\n\nWhat we cover:\nHow building on a client's land works with Mitchell, and why there is zero down, zero closing costs and no construction loan: Mitchell self-funds every build.\nMitchell Design Dollars. Every Mitchell home comes with $5,000 in Design Dollars to spend on design selections. The more selections the customer buys, the more Mitchell adds, up to $25,000.\nThe Home Portrait: a quiz of eight questions, about 90 seconds, you can send to any client.\nHow to refer a client, and the terms of Mitchell's realtor incentive program.\nA walk through the Design Center.\n\nRSVP: " + RSVP + "\n\n" + FINE + " " + FIN,
    "facebook_event_notes": "One Facebook event per Design Center; only [city] and [studio address] change. Link: " + u(RSVP, "facebook_event", e) + " . Publish Wednesday, November 11.",
    "gbp": {
        "title": "Realtor Lunch and Learn",
        "body": "Real estate agents and brokers: join us at our [city] Design Center on Wednesday, November 18, from 11:30am to 1pm. Learn how building on a client's land works with Mitchell, from SimplyMitchell (zero down, zero closing costs, no construction loan) to Mitchell Design Dollars and the Home Portrait quiz, how to refer, and the terms of our realtor incentive program. Tap Sign up to save a seat.\n\n" + DD_SHORT + " " + FINE,
        "button": "Sign up",
        "link": u(RSVP, "gbp", e),
        "post_on": "All five Design Center profiles, Wednesday, November 11. Event-type post, start November 18, 11:30am, end 1pm.",
        "notes": "If lunch is confirmed, add: Lunch is on us."},
    "nextdoor": None,
    "nextdoor_when": "Skip: a professional audience, not neighbors.",
    "invite_when": "From Wednesday, November 11, 2026. New Home Consultants to agents they already know.",
    "invite_text": "Hi [first name], [your name] with Mitchell Homes. Next Wednesday, Nov 18, 11:30 to 1, we are hosting agents at our [city] Design Center: how building on a client's land works, how to refer, and our realtor incentive. Can I save you a seat?",
    "invite_email": {
        "subject": "Next Wednesday at our [city] Design Center",
        "body": "Hi [first name],\n\nYou talk with people who own land, or are about to buy it, every week, so I wanted to invite you personally.\n\nOn Wednesday, November 18, from 11:30am to 1pm, we are hosting a Lunch and Learn for agents at our [city] Design Center. " + LUNCH + " In 90 minutes we will cover how building on a client's land works with Mitchell, why there is zero down, zero closing costs and no construction loan (Mitchell self-funds every build), what Mitchell Design Dollars and the Home Portrait quiz mean for your clients, and how referrals and our realtor incentive program work.\n\nCan I save you a seat? Just reply, and tell me if a colleague would like to come." + SIG + "\n\n" + DD_SHORT + " " + FINE + " " + FIN},
    "reminder_when": "Tuesday, November 17, 2026. Builder Studio workflow, RSVPs with text consent only.",
    "reminder_text": "Mitchell Homes: See you tomorrow, Wed Nov 18, 11:30am to 1pm, for the Realtor Lunch and Learn at our [city] Design Center, [studio address]. Reply STOP to opt out",
    "thanks_when": "Wednesday, November 18, 2026, that afternoon. The New Home Consultant who hosted.",
    "thanks_text": "Thank you for coming in today, [first name]. Next time a client mentions land, text me their name and I will take it from there. The slides and referral details are coming tomorrow.",
    "followup_when": "Thursday, November 19, 2026. The New Home Consultant who hosted. ra2 goes to the realtor list the same day, so this personal note stays separate and short.",
    "followup_email": {
        "subject": "For your next client with land",
        "body": "Hi [first name],\n\nThank you for joining us at the Design Center yesterday. Here is everything in one place for the next client who mentions land.\n\nThe short version for your client: Mitchell has built custom homes on land the buyer owns since 1992. Mitchell self-funds every build, so there is zero down, zero closing costs and no construction loan. More than 40 floor plans from 1,000 to 3,000 square feet, and more than 40,000 selections.\n\nDesign Dollars: every Mitchell home comes with $5,000 in Mitchell Design Dollars, and it goes up to $25,000 the more your client personalizes.\n\nThe Home Portrait quiz to send a client: " + u(QUIZ, "followup", e) + "\n\nHow to refer: [referral steps, once Mitchell confirms]\nRealtor incentive: [terms, once Mitchell confirms]\n\nWhen you have a client ready to talk, text or call me directly." + SIG + "\n\n" + FINE + " " + FIN},
    "extra_texts": [],
    "notes": [
        "Every E6 piece waits on the realtor incentive terms; the lunch bracket comes out or becomes Lunch is on us once Mitchell decides.",
        "Never promise continuing education credit, in copy or in conversation.",
    ],
    "schedule": sched([
        ("2026-11-11", "Wednesday, November 11", "Email", "Event block in the realtor email rb2", "Marketing"),
        ("2026-11-11", "Wednesday, November 11", "Social", "Post 1 (Facebook, Instagram feed, LinkedIn). Publish the five Facebook events.", "Marketing"),
        ("2026-11-11", "Wednesday, November 11", "Google", "Event post on all five profiles", "Marketing"),
        ("2026-11-11", "Wednesday, November 11", "Sales team", "Personal invite text and email to agents they know, from this day", "New Home Consultants"),
        ("2026-11-16", "Monday, November 16", "Social", "Post 2 (Facebook, Instagram Stories, LinkedIn)", "Marketing"),
        ("2026-11-17", "Tuesday, November 17", "Text", "Reminder to RSVPs only", "Builder Studio workflow"),
        ("2026-11-18", "Wednesday, November 18", "Event", "Lunch and Learn, 11:30am to 1pm; thank-you text", "New Home Consultants"),
        ("2026-11-19", "Thursday, November 19", "Sales team", "Follow-up email with the referral kit (separate from ra2, which goes the same day)", "New Home Consultants"),
    ]),
})


ABOUT = [
    "Drafts only. Nothing has been sent, posted, scheduled or created in any system. Every event is a proposal until Mitchell approves its date and staffing.",
    "Tiers: E1, E2 and E6 are add, run if Mitchell can staff them. E3, E4 and E5 are later: finished and banked for winter, with every date set when Mitchell schedules them. Their email blocks and E4's bulk text are kept, marked banked, so nothing from them reaches the fall emails or calendar.",
    "[RSVP link] is the Builder Studio form Kelly will create (one per event, or one form with an event field). Every link field shows the tracked version: put the real form URL where [RSVP link] sits and keep the UTM string, so each RSVP shows where it came from. In body copy, paste the link from that item's link field.",
    "Cadence: no new marketing emails and no extra marketing texts. Invitations ride existing emails, social, Facebook events, Google profiles, Nextdoor and personal consultant messages.",
    "Reminder texts go only to people who RSVPed with text consent, from one Builder Studio workflow per event. Consultants tag anyone who RSVPs by reply with the event tag so the same workflow reaches them.",
    "Design Dollars: wherever named, it carries the $5,000 floor and the short fine print. Texts never name it. After October 31, pieces that name it wait for Mitchell's November reserve-by date (question 1): E1 says November 30, the date Kelly recommends, and E6 names the offer without a date.",
    "Images: anything that could be boosted (social posts, Facebook events) uses real Mitchell homes or Design Centers with no people. Never show or describe the painted Home Portrait in any invitation.",
    "Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to the Instagram link listed for that post.",
    "Placeholders: [first name], [your name], [your phone], [city], [studio address], [time], [Facebook Live link], [YouTube Live link], [replay link], and [date] in the events banked for winter. Studio addresses are in the studio table.",
]
CADENCE_NOTES = [
    "dd2 (October 27) carries one event block, E2's, two days before the show; the October 22 post, the Facebook event and the consultant invites on October 26 carry the call for questions. E1 now rides fb1, fb5 and fb5c (November 4).",
    "October 29: the deadline week text to active leads goes the same day as E2's thank-you text. For a consultant's own active leads who RSVPed, the thank-you text stands in for the deadline text; Friday's follow-up carries the October 31 date.",
    "November 2 to 5: E1's consultant invites. November 5 already has the landowner consultant text, so leads who own land get their E1 invite by November 4.",
    "fb5 is on hold for the plan guide email. If fb5 and fb5c miss November 4, E1 rides fb1 and the consultant invites only.",
    "November 6: E1's reminder goes to RSVPs the same day as sms4, the landowner bulk text. Leave E1 RSVPs out of sms4 so nobody gets two texts that day.",
    "E6 rides rb2, the realtor email on November 11, the day consultant invites to agents begin. ra2 goes to the realtor list on November 19, the same day as the E6 follow-up; ra2 already carries the lot checklist, so the personal follow-up stays separate and short and does not repeat it.",
    "E3, E4 and E5 are banked for winter: no email blocks, no bulk text and no dates on the fall calendar.",
    "build_cadence.py places events by its own date map. It needs E2 on October 29 (reminder October 28), E1 on November 7 (invites November 2, reminder November 6) and E6 on November 18 (invites November 11, reminder November 17), with E3, E4 and E5 off the fall calendar.",
]

# ---------------------------------------------------------------- checks
problems = []
TEXT_FIELDS = ("invite_text", "reminder_text", "thanks_text")
for ev in EVENTS:
    i = ev["id"]
    for f in TEXT_FIELDS:
        n = len(ev[f])
        lim = 300 if f == "invite_text" else 320
        if n > lim:
            problems.append(f"{i} {f}: {n} characters")
        if "Design Dollars" in ev[f]:
            problems.append(f"{i} {f}: texts never name Design Dollars")
    if ev.get("tier") not in ("add", "later"):
        problems.append(f"{i}: tier must be add or later")
    elif ev["tier"] == "later":
        if ev["rides_in"] or ev["extra_texts"]:
            problems.append(f"{i}: a banked event rides no fall email and sends no fall text")
        m = re.search(r"\b(October|November|December|Oct|Nov|Dec) \d", json.dumps(ev))
        if m:
            problems.append(f"{i}: banked event still names a fall date: {m.group(0)}")
    for t in ev["extra_texts"] + ev.get("banked_extra_texts", []):
        n = len(t["body"].replace("[trigger link]", "xxxxxxx.xx/xxxxxx"))
        t["characters"] = n
        if n > 160:
            problems.append(f"{i} extra text: {n} characters")
        if "Reply STOP to opt out" not in t["body"]:
            problems.append(f"{i} extra text: missing STOP line")
    if len(ev["gbp"]["title"]) > 58:
        problems.append(f"{i} gbp title too long")
    # offer rule: every surface naming Design Dollars carries the $5,000 floor and the short fine print
    surfaces = [("facebook_event", ev["facebook_event"]), ("gbp", ev["gbp"]["body"]), ("nextdoor", ev["nextdoor"] or ""),
                ("invite_email", ev["invite_email"]["body"]), ("followup_email", ev["followup_email"]["body"])]
    surfaces += [(f"social {s['date']}", s["body"]) for s in ev["social"]]
    surfaces += [(f"block {r['email']}", r["block"]["text"] + " " + r["block"].get("fine", "")) for r in ev["rides_in"] + ev.get("banked_rides_in", [])]
    for name, body in surfaces:
        if "Design Dollars" in body and not ("$5,000" in body and "No cash value." in body):
            problems.append(f"{i} {name}: Design Dollars without the $5,000 floor or fine print")
        if re.search(r"\bpaint(ed|ing|s)?\b", body.replace("paint and hardware", "").replace("paint, and hardware", ""), re.I):
            problems.append(f"{i} {name}: mentions painting")
for ev in EVENTS:
    ev["invite_text_characters"] = len(ev["invite_text"])
    ev["reminder_text_characters"] = len(ev["reminder_text"])
    ev["thanks_text_characters"] = len(ev["thanks_text"])

data = {"about": ABOUT, "cadence_notes": CADENCE_NOTES, "studios": STUDIOS, "events": EVENTS}
blob = json.dumps(data, ensure_ascii=False)
for pat, why in [(r"[–—]", "em or en dash"), (r"Simply Mitchell", "SimplyMitchell is one word"), (r"New Home Specialist|sales consultant", "title"),
                 (r"150 day|\bdays? from contract", "build duration"), (r"price lock|locked pricing|price never changes", "pricing claim"),
                 (r"CEA Marketing Group", "agency name"), (r"continuing education credit(?! *:)", None), (r"\brebate|cash back|money off|\$25,000 off", "offer wording"),
                 (r"giveaway(?!s? or)", None), (r" - |--", "hyphen as punctuation")]:
    for m in re.finditer(pat, blob):
        if why:
            problems.append(f"{why}: ...{blob[max(0, m.start() - 40):m.end() + 40]}...")
if problems:
    print("\n".join(problems))
    sys.exit(1)
open(f"{HERE}/events.json", "w").write(json.dumps(data, indent=1, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- markdown
def q(text):
    return "\n".join("> " + line if line else ">" for line in text.split("\n"))


COUNT = {6: "Six", 7: "Seven", 8: "Eight"}.get(len(EVENTS), str(len(EVENTS)))
TIER = {"add": "add, runs if Mitchell can staff it", "later": "later, finished and banked for winter; the date is set when Mitchell schedules it"}
BANKED = [ev["id"].upper() for ev in EVENTS if ev["tier"] == "later"]
L = ["# Mitchell Homes fall events, October 19 to November 29, 2026", "",
     f"{COUNT} event proposals for CEA Marketing (Kelly Bosetti), each with every invitation and follow-up. Built from `campaigns/FACTS.md` by `make_events.py`; `events.json` holds the same content.", "",
     "## Read first", ""]
L += [f"- {a}" for a in ABOUT]
L += ["", "## Where the events touch the existing cadence", ""] + [f"- {c}" for c in CADENCE_NOTES]
L += ["", f"## The {COUNT.lower()} at a glance", "", "| | Event | Tier | When | Where | Rides in |", "|---|---|---|---|---|---|"]
for ev in EVENTS:
    rides = ", ".join(r["email"] for r in ev["rides_in"]) or ("none this fall (banked)" if ev["tier"] == "later" else "no email (text, social, profile, Nextdoor, invites)")
    where = "Online" if ev["where"].startswith("Online") else ("Wilmington (Belville)" if ev["id"] == "e4" else "All five Design Centers")
    L.append(f"| {ev['id'].upper()} | {ev['name']} | {ev['tier']} | {ev['date']}, {ev['time']} | {where} | {rides} |")
L += ["", "## Every touch by date", "", f"The fall events only; {', '.join(BANKED)} are banked for winter." if BANKED else "All events.", "",
      "| Date | Event | Channel | What | Who |", "|---|---|---|---|---|"]
allrows = sorted(((s["date"], ev["id"], s) for ev in EVENTS if ev["tier"] != "later" for s in ev["schedule"]), key=lambda x: (x[0], x[1]))
for d, i, s in allrows:
    L.append(f"| {s['day']} | {i.upper()} | {s['channel']} | {s['what']} | {s['who']} |")
L += ["", "## Design Center addresses", "", "As listed on the live Design Dollars page. Confirm before printing any address.", "", "| Studio | Address | Phone in copy |", "|---|---|---|"]
for s in STUDIOS:
    L.append(f"| {s['studio']} | {s['address']} | {s['phone']}{' (' + s['note'] + ')' if s.get('note') else ''} |")

for ev in EVENTS:
    L += ["", "---", "", f"## {ev['id'].upper()}. {ev['name']}", "",
          "*Proposal until Mitchell approves the date and staffing.*", "",
          f"**Tier:** {TIER[ev['tier']]}  ", f"**When:** {ev['date']}, {ev['time']}  ", f"**Where:** {ev['where']}  ", f"**For:** {ev['audience']}", "",
          "**What happens**", ""] + [f"- {w}" for w in ev["what"]] + ["",
          f"**Why it helps the campaign (for Kelly):** {ev['why']}", "", "**Mitchell must confirm**", ""] + [f"- {c}" for c in ev["confirm"]]
    if ev.get("notes"):
        L += ["", "**Notes for Kelly**", ""] + [f"- {n}" for n in ev["notes"]]
    L += ["", "**Schedule**", "", "| Date | Channel | What | Who |", "|---|---|---|---|"]
    L += [f"| {s['day']} | {s['channel']} | {s['what']} | {s['who']} |" for s in ev["schedule"]]
    L += ["", "### Email event block", ""]
    if not ev["rides_in"]:
        L += [ev.get("rides_in_note", "None."), ""]
    for banked, r in [(False, r) for r in ev["rides_in"]] + [(True, r) for r in ev.get("banked_rides_in", [])]:
        b = r["block"]
        L += [f"**{'Banked, first written for ' if banked else ''}{r['email']}**, {r['send']}. {r['placement']}", "", q(f"**{b['head']}**\n\n{b['text']}\n\n[{b['cta']}]") , "",
              f"Link: `{b['link']}`"]
        if b.get("fine"):
            L += ["", f"Fine print under the block: {b['fine']}"]
        L.append("")
    L += ["### Social posts", ""]
    for s in ev["social"]:
        L += [f"**{s['date']}** · {s['channels']}", "", q(s["body"]), "", f"Link: `{s['link']}`  ", f"Notes: {s['notes']}", ""]
    L += ["### Facebook event description", "", q(ev["facebook_event"]), "", f"Notes: {ev['facebook_event_notes']}", "",
          "### Google Business Profile event post", "", f"Post on: {ev['gbp']['post_on']}", "",
          f"**Title:** {ev['gbp']['title']} ({len(ev['gbp']['title'])} of 58 characters)  ", f"**Button:** {ev['gbp']['button']}, linking to `{ev['gbp']['link']}`", "",
          q(ev["gbp"]["body"]), "", f"Notes: {ev['gbp']['notes']} If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.", "",
          "### Nextdoor", ""]
    if ev["nextdoor"]:
        L += [ev["nextdoor_when"], "", q(ev["nextdoor"]), ""]
    else:
        L += [ev["nextdoor_when"], ""]
    L += ["### Consultant personal invite", "", ev["invite_when"], "",
          f"**Text** ({ev['invite_text_characters']} characters)", "", q(ev["invite_text"]), "",
          f"**Email** · Subject: {ev['invite_email']['subject']}", "", "```text", ev["invite_email"]["body"], "```", "",
          f"### RSVP reminder text", "", ev["reminder_when"], "", q(ev["reminder_text"]), "", f"({ev['reminder_text_characters']} characters)", "",
          "### Same-day thank-you text", "", ev["thanks_when"], "", q(ev["thanks_text"]), "",
          f"### Next-day follow-up email", "", ev["followup_when"], "", f"Subject: {ev['followup_email']['subject']}", "", "```text", ev["followup_email"]["body"], "```", ""]
    for head, texts in (("### Extra text", ev["extra_texts"]), ("### Extra text (banked for winter)", ev.get("banked_extra_texts", []))):
        if not texts:
            continue
        L += [head, ""]
        for t in texts:
            L += [f"**{t['date']}** · {t['audience']}", "", q(t["body"]), "",
                  f"{t['characters']} of 160 characters with a short trigger link. Link: `{t['link']}`. {t['notes']}", ""]
md = "\n".join(L) + "\n"
if re.search(r"[–—]", md):
    sys.exit("dash in markdown")
open(f"{HERE}/events.md", "w").write(md)
print("events.json and events.md written;", len(EVENTS), "events")
for ev in EVENTS:
    print(ev["id"], ev["name"], "| invite", ev["invite_text_characters"], "| reminder", ev["reminder_text_characters"], "| thanks", ev["thanks_text_characters"],
          "| extra", [t["characters"] for t in ev["extra_texts"]])
