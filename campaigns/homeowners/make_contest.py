#!/usr/bin/env python3
"""My Mitchell Story: the fall 2026 homeowner video contest for Mitchell Homes.

usage: python3 campaigns/homeowners/make_contest.py   writes contest.json and contest.md next to this file.
Run campaigns/events/make_events.py first: the Homeowner Appreciation Night texts (event E7) come from events.json.

DRAFTS ONLY. Nothing here is sent, posted, scheduled, uploaded or created anywhere. Every date and amount is a
proposal for Mitchell to confirm, and the Official Rules are a draft for Mitchell's legal review.
Facts come from campaigns/FACTS.md and the Mitchell Homes messaging skill only.
"""
import json, os, re, sys
from urllib.parse import urlencode

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
CAMP = "fall26_homeowners"
M = "https://media.mitchellhomesinc.com/276/"
ENTRY = "[entry form link]"
RSVP = "[RSVP link]"
RULES = "[official rules link]"
BOOK = "[photo session booking link]"
SIG = "\n\n[your name]\nNew Home Consultant, Mitchell Homes\n[your phone]"

CH = {  # channel: (utm_source, utm_medium)
    "facebook": ("facebook", "organic_social"), "instagram": ("instagram", "organic_social"),
    "gbp": ("google_business_profile", "organic"), "sales_email": ("sales_email", "email"),
}


def u(base, ch, cid):
    s, m = CH[ch]
    return base + "?" + urlencode({"utm_source": s, "utm_medium": m, "utm_campaign": CAMP, "utm_content": cid})


# ---------------------------------------------------------------- sources
ev_path = os.path.join(C, "events", "events.json")
E7 = None
if os.path.exists(ev_path):
    E7 = next((e for e in json.load(open(ev_path))["events"] if e["id"] == "e7"), None)
if not E7:
    sys.exit("Run campaigns/events/make_events.py first: event e7 (Homeowner Appreciation Night) is not in events.json")

# real Mitchell home photos already used in the email series, with their alt text
series_src = open(os.path.join(C, "email", "series.py")).read()
HEROES = dict(re.findall(r'hero\("([^"]+)",\s*"([^"]+)"\)', series_src))
HOMES = {p: a for p, a in HEROES.items() if "Design_Center" not in p and "Design_Studio" not in p}

# ---------------------------------------------------------------- the contest
NAME = "My Mitchell Story"
LINE = "Every home is a portrait. Show us yours."
TAG = "#MyMitchellStory"
CLOSE = "Sunday, December 6, 2026, at 11:59pm Eastern"
PROMPTS = [
    "What do you love most about your home?",
    "How do you use it, day to day?",
    "How does your home make you feel?",
    "Where is your favorite place to hang out?",
]
SESSION = "Every eligible entrant gets a professional photo session at home, paid for by Mitchell, while sessions last. The photos are theirs to keep."
HP_THEIR = "their own Home Portrait, a framed painting of their Mitchell home"
FINALISTS = "Five finalists, one from each Design Center region, receive " + HP_THEIR + ", and one grand prize winner also receives $2,500."
WHO = "Open to Mitchell homeowners 18 or older in Virginia, North Carolina, South Carolina and Maryland; one entry per household."
SMALL = WHO + " Entries close " + CLOSE + ". No purchase necessary. Official Rules: " + RULES

ABOUT = [
    "Drafts only. Nothing has been sent, posted, scheduled, uploaded or created in any system.",
    "Every date and amount is a proposal for Mitchell to confirm. The Official Rules are a draft for Mitchell's legal review and make no legal conclusions.",
    "Homeowner Appreciation Night, the kickoff, is event E7 in campaigns/events/events.json (invitation post, Facebook event, Google post, consultant invite, reminder, thank-you and follow-up). The event texts here are read from there, so the two never drift apart.",
    "Placeholders: [entry form link], [RSVP link], [official rules link], [photo session booking link], [trigger link], [contest email address], [number], [ARV], [first name], [your name], [city], [time]. Email CTAs carry the bare placeholder; social and Google links show the tracked version (utm_campaign=fall26_homeowners). Put the real URL where the placeholder sits and keep the UTM string.",
    "Emails use the series.py email format, with hero_path and hero_alt in place of hero. They are not in series.py, so build.py does not render or upload them yet; to do that, add them to series.py as a series and turn each hero_path into hero(path, alt).",
    "Workflow emails (hw1 to hw4) are plain personal notes. build.py adds the Hi {{contact.first_name}} line and the {{user.name}} New Home Consultant signature, and in plain mode shows only p, list and link blocks, so their links sit in link blocks.",
    "No painted Home Portrait appears anywhere, and none is described as an image to look at. The prize is named in words only: a framed painting of their Mitchell home.",
    "Rule Zero holds for homeowners too: every piece opens with the home and the homeowner, and the prizes come after.",
]

SUMMARY = ("My Mitchell Story invites Mitchell homeowners to show us, in a short phone video, what they love about their home, how they live in it and where they like to spend their time. "
           "Every eligible entrant gets a professional photo session at home, paid for by Mitchell, while sessions last, with the photos theirs to keep; five finalists, one from each Design Center region, receive "
           + HP_THEIR + ", and one grand prize winner also receives $2,500. "
           "It opens at Homeowner Appreciation Night at all five Design Centers on Tuesday, November 10, 2026, and closes Sunday, December 6, 2026; every date and amount is a proposal for Mitchell to confirm.")

HOW = [
    "Film a short video at home on your phone, about 30 to 90 seconds.",
    "Answer one or more of the four questions, in your own words and your own voice.",
    "Send it through the entry form: upload the video or paste a link.",
    "We confirm your entry and send a link to book your photo session at home, paid for by Mitchell, while sessions last.",
    "After entries close, a panel from Mitchell and CEA Marketing chooses five finalists, one from each Design Center region, and one grand prize winner.",
    "Want to share it too? Post it on your own Instagram or TikTok with #MyMitchellStory and tag Mitchell Homes. Welcome, never required.",
]

PRIZES = [
    {"tier": "Every eligible entrant",
     "what": "A professional photo session at their Mitchell home, about 45 to 60 minutes, paid for by Mitchell. The edited photos are theirs to keep.",
     "note": "Proposal. Limited to [number] sessions, or while sessions last, within a budget Mitchell sets. Sessions take place after the entry arrives, from mid-November through [January 31, 2027]. Approximate retail value [ARV] each, stated in the rules."},
    {"tier": "Five finalists, one from each Design Center region",
     "what": "Their own Home Portrait: a framed painting of their Mitchell home.",
     "note": "Proposal. Artist, size, frame and delivery date are open questions. Approximate retail value [ARV] each. Described in words only and never shown."},
    {"tier": "Grand prize, one winner chosen from the five finalists",
     "what": "$2,500, plus their Home Portrait.",
     "note": "Proposal, at the amount Kelly suggested. The form (check, prepaid card, gift card or other) is an open question. Approximate retail value $2,500 plus the Home Portrait. Prizes of $600 or more in a year are reported on IRS Form 1099."},
]

TIMELINE = [
    {"date": "Wednesday, October 28, 2026", "what": "Invitation to Homeowner Appreciation Night (ho2) to past homeowners. Facebook events and Google event posts go up (E7)."},
    {"date": "Thursday, October 29 to Tuesday, November 3, 2026", "what": "New Home Consultants personally invite the homeowners they built with."},
    {"date": "Monday, November 9, 2026", "what": "RSVP reminder text. Photo session calendars live in Builder Studio, so homeowners can book at the event."},
    {"date": "Tuesday, November 10, 2026, 5:30pm to 7:30pm", "what": "Homeowner Appreciation Night at all five Design Centers. Entries open at 5:30pm Eastern."},
    {"date": "Wednesday, November 11, 2026", "what": "Launch email (ho3) to homeowners who did not come; each consultant's follow-up email to those who did. Announcement post and Google post."},
    {"date": "Thursday, November 12, 2026", "what": "Launch text to homeowners with text consent who did not RSVP."},
    {"date": "From mid-November", "what": "Photo sessions roll as entries are confirmed, through [January 31, 2027]."},
    {"date": "Wednesday, November 18, 2026", "what": "Filming tips email (ho4) to homeowners who have not entered."},
    {"date": "Fridays, November 20, November 27 and December 4, 2026", "what": "Entrant spotlights on social, only with the entrant's consent."},
    {"date": "Wednesday, December 2, 2026", "what": "Last-week email (ho5) to homeowners who have not entered."},
    {"date": "Thursday, December 3, 2026", "what": "Last-week text to homeowners with text consent who have not entered."},
    {"date": "Sunday, December 6, 2026, 11:59pm Eastern", "what": "Entries close."},
    {"date": "Monday, December 7 and Tuesday, December 8, 2026", "what": "Judging."},
    {"date": "Tuesday, December 8, 2026", "what": "Finalists and the potential grand prize winner get a phone call, then their note (hw3, hw4). Documents due within five business days."},
    {"date": "Thursday, December 10, 2026", "what": "Finalists announced on social."},
    {"date": "Tuesday, December 15, 2026", "what": "Grand prize winner announced (ho6 and social), once verification is complete."},
    {"date": "[Date, with the artist]", "what": "Home Portraits delivered to the five finalists, privately."},
]

JUDGING = [
    {"criterion": "The story", "weight": "40 percent", "what": "How clearly and personally the entry tells what the homeowner loves about the home, and why."},
    {"criterion": "The home in everyday life", "weight": "30 percent", "what": "How the home shows up in the way they live: the rooms they use, the routines, the favorite places."},
    {"criterion": "How it feels to watch", "weight": "30 percent", "what": "The warmth, honesty and feeling of home that come through."},
    {"criterion": "Never judged", "weight": "", "what": "Who appears in the video, how many people appear, or whether anyone appears at all; the size, price, plan or location of the home; video production quality; likes, views, comments or followers."},
    {"criterion": "How it works", "weight": "", "what": "A panel of [three to five] judges from Mitchell and CEA Marketing scores every eligible entry. The top entry in each of the five Design Center regions is a finalist; the top finalist wins the grand prize. Ties go to the higher score for the story. A judged contest, not a random drawing."},
]

FILMING = [
    "Film in daylight, with the light in front of you, not behind you.",
    "Start in your favorite spot, then tell us why it matters.",
    "Use your own voice. No popular songs: Mitchell cannot share a video that carries one.",
    "Hold the phone steady, or prop it on a shelf. Slow moves beat fast ones.",
    "Get close when you talk, and turn off the TV and the dishwasher.",
    "Keep house numbers, street signs and license plates out of the frame.",
    "Ask before you film anyone, and keep children's full names out of it.",
    "One take is fine. Real beats perfect.",
]

# ---------------------------------------------------------------- emails (series.py format)
P = lambda text: {"t": "p", "text": text}
EMAILS = [
    {"id": "ho2", "send": "Wednesday, October 28", "segment": "Past Mitchell homeowners (smart list: Past Mitchell homeowners), minus anyone the warranty team is calling first",
     "hold": "Hold until Mitchell approves the November 10 date, staffing and refreshments, and the contest itself (prizes, session cap, Official Rules after legal review). If the contest is not approved by Monday, October 26, send it without the My Mitchell Story paragraph.",
     "subject": "An evening for the people who built with us",
     "preview": "Homeowner Appreciation Night, Tuesday, November 10, at your Mitchell Design Center.",
     "hero_path": "2024/7/24/1.jpg",
     "eyebrow": "For Mitchell homeowners", "headline": "Thank you for building with us",
     "blocks": [
         P("Every Mitchell home started with someone who could already picture it: the porch, the kitchen, the room where everyone ends up. You brought that picture to us, and then you made the home your own."),
         P("So we would like to say thank you, in person. On Tuesday, November 10, from 5:30pm to 7:30pm, every Mitchell Design Center is hosting Homeowner Appreciation Night. Catch up with the New Home Consultants and Design Consultants who helped build your home, meet other Mitchell homeowners, and bring the family. [Refreshments: Mitchell to confirm.]"),
         P("It is also the night we open My Mitchell Story, a chance to show us, in a short phone video, what you love about your home. Everyone who enters gets a professional photo session at home, paid for by Mitchell, while sessions last, and you can book yours that night."),
         {"t": "cta", "text": "RSVP", "href": RSVP},
         {"t": "small", "text": "Fredericksburg, Richmond (Midlothian), Newport News, Raleigh (Garner) and Wilmington (Belville), 5:30pm to 7:30pm local time. Please RSVP so each studio can plan."}]},
    {"id": "ho3", "send": "Wednesday, November 11", "segment": "Past Mitchell homeowners who did not come to Homeowner Appreciation Night (those who came get their consultant's follow-up that morning instead)",
     "hold": "Hold until legal approves the Official Rules and Mitchell confirms the prizes, the form of the $2,500, the session cap and the dates.",
     "subject": "What do you love most about your home?",
     "preview": "Show us in a short phone video. Your photo session at home is on us, while sessions last.",
     "hero_path": "2026/3/24/07-DJI_20260224134444_0238_D_copy.jpg",
     "eyebrow": "My Mitchell Story", "headline": LINE,
     "blocks": [
         P("You know your home in a way no floor plan ever could. The chair by the window that gets the morning light. The counter where homework happens. The porch at the end of a long day."),
         P("Tell us about it. My Mitchell Story is open to Mitchell homeowners through Sunday, December 6. Film a short video on your phone, about 30 to 90 seconds, and answer one or more of these:"),
         {"t": "list", "items": PROMPTS},
         {"t": "steps", "items": [
             ["Film it at home", "On your phone, in your own voice. No music needed, and no need to be perfect."],
             ["Send it in", "Upload your video or paste a link on the entry form."],
             ["Book your photo session", "We send you a link to schedule a professional photo session at your home, paid for by Mitchell, while sessions last. The photos are yours to keep."]]},
         P("After entries close, a panel from Mitchell and CEA Marketing chooses five finalists, one from each Design Center region. Each finalist receives their own Home Portrait, a framed painting of their Mitchell home. One grand prize winner also receives $2,500."),
         {"t": "cta", "text": "Tell Your Story", "href": ENTRY},
         {"t": "small", "text": "Want to share it too? Post it on your own Instagram or TikTok with #MyMitchellStory and tag Mitchell Homes. Never required: entries count only through the form. " + SMALL}]},
    {"id": "ho4", "send": "Wednesday, November 18", "segment": "Past Mitchell homeowners who have not entered (no tag my mitchell story entry)",
     "hold": "Holds with ho3 (Official Rules and prize details).",
     "subject": "Your phone is all you need",
     "preview": "A few tips for filming your Mitchell story, and your photo session is on us.",
     "hero_path": "2026/3/24/38-DSC06023.jpg",
     "eyebrow": "My Mitchell Story", "headline": "Start with your favorite spot",
     "blocks": [
         P("Most good home stories start in one place: the chair by the fireplace, the kitchen island, the back porch. Start there, and tell us why it matters to you."),
         {"t": "steps", "items": [
             ["Find the light", "Film in daylight, with the window in front of you, not behind you."],
             ["Show it, then say why", "Show us the place first. Then tell us what happens there and why you love it."],
             ["Use your own voice", "No popular songs. We cannot share a video that carries one, so your voice or the sounds of home are best."],
             ["Hold steady", "Prop the phone on a shelf or hold it with both hands. Slow moves beat fast ones."],
             ["Keep it yours", "Keep house numbers, street signs and license plates out of the frame, and ask before you film anyone."]]},
         P("Once your entry is in, we send a link to book your photo session: about an hour at your home with a professional photographer, paid for by Mitchell, while sessions last. The photos are yours to keep."),
         {"t": "cta", "text": "Tell Your Story", "href": ENTRY},
         {"t": "small", "text": SMALL}]},
    {"id": "ho5", "send": "Wednesday, December 2", "segment": "Past Mitchell homeowners who have not entered (no tag my mitchell story entry)",
     "hold": "Holds with ho3 (Official Rules and prize details). If Mitchell caps photo sessions and they run out before December 2, drop the photo session sentence.",
     "subject": "Your story, by Sunday",
     "preview": "My Mitchell Story closes Sunday, December 6, at 11:59pm Eastern.",
     "hero_path": "2026/3/3/55-DSC06124.jpg",
     "eyebrow": "My Mitchell Story", "headline": "There is still time to tell it",
     "blocks": [
         P("Somewhere in your home is the spot where the day slows down. Maybe it is the kitchen everyone ends up in, or the porch after dinner. That is the story we would love to see."),
         P("My Mitchell Story closes this Sunday, December 6, at 11:59pm Eastern. A minute on your phone is enough. Show us the place, and tell us why you love it."),
         {"t": "list", "items": PROMPTS},
         P("Every entrant gets a professional photo session at home, paid for by Mitchell, while sessions last. " + FINALISTS),
         {"t": "cta", "text": "Send My Story", "href": ENTRY},
         {"t": "small", "text": SMALL}]},
    {"id": "ho6", "send": "Tuesday, December 15", "segment": "All past Mitchell homeowners, including every entrant",
     "hold": "Waits on the winner's verification and signed releases. Fill every bracket from the entries, with permission. The hero can be a home-only photo from the winner's session once they sign the release. Never show the painting.",
     "subject": "Meet the My Mitchell Story winner",
     "preview": "And thank you to every homeowner who showed us their home.",
     "hero_path": "2026/3/3/ava_farmhouse-extended_sky.jpg",
     "eyebrow": "My Mitchell Story", "headline": "Thank you for showing us your homes",
     "blocks": [
         P("This fall, [number] Mitchell homeowners showed us the places they love most: [two or three real examples from entries, in their words, with permission]. Every one of them reminded us why we build."),
         P("[First names], Mitchell homeowners in [state], told us [one line about their story, in their words]. Their story is the My Mitchell Story grand prize winner. They receive $2,500 and their own Home Portrait, a framed painting of their Mitchell home."),
         {"t": "quote", "text": "[A line from the winner's video, word for word]", "by": "[First names], Mitchell homeowners, [state]", "link": "[winner video link]", "linktext": "Watch their story"},
         P("Our finalists, one from each Design Center region: [first names and state for each of the five]. Each receives their own Home Portrait."),
         P("If you entered, thank you. Your session photos are yours to keep, and if your session is still on the calendar, we will see you soon."),
         {"t": "cta", "text": "Watch the Winning Story", "href": "[winner video link]"},
         {"t": "small", "text": "Shared with the permission of every homeowner named."}]},
]
for em in EMAILS:
    em["hero_alt"] = HEROES.get(em["hero_path"], "")

WORKFLOW_EMAILS = [
    {"id": "hw1", "send": "Immediately after an entry form is submitted (workflow My Mitchell Story | 01 Entry received), from the homeowner's assigned New Home Consultant",
     "segment": "Every entrant", "plain": True,
     "subject": "Your story is in", "preview": "Thank you. Here is what happens next.",
     "blocks": [
         P("Thank you for sending in your My Mitchell Story. Your home is one we are proud to have built, and I cannot wait to watch it."),
         P("Here is what happens next:"),
         {"t": "list", "items": [
             "We confirm your entry within two business days.",
             "Then we send a link to book your photo session at home, paid for by Mitchell, while sessions last.",
             "Entries close Sunday, December 6, at 11:59pm Eastern, and we plan to announce the finalists about December 10."]},
         P("If you need to change anything, just reply to this email.")]},
    {"id": "hw2", "send": "When the contest coordinator adds the tag my mitchell story verified (workflow My Mitchell Story | 02 Photo session)",
     "segment": "Every verified entrant", "plain": True,
     "hold": "Waits on the photographers, the session cap and the booking calendar.",
     "subject": "Let us book your photo session", "preview": "About an hour at your home, and the photos are yours to keep.",
     "blocks": [
         P("Your My Mitchell Story entry is confirmed. Thank you."),
         P("Next is your photo session. A professional photographer will spend about 45 to 60 minutes at your home, paid for by Mitchell. Here is what to expect:"),
         {"t": "list", "items": [
             "We like to finish outside in the hour before sunset, when the front of the home looks its best.",
             "Inside, we photograph the kitchen, the porch and the favorite spot from your video, plus a few details.",
             "Family photos only if you want them. Everyone pictured signs a short release, and a parent signs for any child.",
             "You receive [number] edited photos within [two weeks], yours to keep."]},
         {"t": "link", "text": "Book your photo session", "href": BOOK},
         P("If none of the times work, reply and we will find one. Sessions run through [January 31, 2027].")]},
    {"id": "hw3", "send": "About Tuesday, December 8, after the phone call, when the coordinator adds the tag my mitchell story finalist (workflow My Mitchell Story | 03 Finalists)",
     "segment": "The four finalists who are not the grand prize winner", "plain": True,
     "hold": "Waits on judging, the artist and delivery date, and the release and affidavit from legal.",
     "subject": "You are a My Mitchell Story finalist", "preview": "Congratulations. Here is what happens next.",
     "blocks": [
         P("Congratulations again. As I said on the phone, your story is one of five My Mitchell Story finalists, one from each Design Center region."),
         P("As a finalist, you receive your own Home Portrait, a framed painting of your Mitchell home. [Artist and delivery date, once Mitchell confirms.]"),
         P("To confirm your prize, please return these within five business days:"),
         {"t": "list", "items": [
             "The signed affidavit of eligibility and release (attached).",
             "A completed W-9, if your prizes total $600 or more in the year. [Tax advisor to confirm.]",
             "A good time for a short call about your Home Portrait."]},
         P("We announce the finalists on Thursday, December 10, so please keep the news in the family until then. Thank you for showing us your home.")]},
    {"id": "hw4", "send": "About Tuesday, December 8, after the phone call; sent by hand from the template, not by workflow",
     "segment": "The potential grand prize winner", "plain": True,
     "hold": "Waits on judging, the form of the $2,500, and the release and affidavit from legal.",
     "subject": "Your story won", "preview": "Congratulations. You are the My Mitchell Story grand prize winner.",
     "blocks": [
         P("Congratulations again. Of every story we received, the judges chose yours as the My Mitchell Story grand prize winner."),
         P("You receive $2,500 [as a check, prepaid card or gift card, once Mitchell confirms] and your own Home Portrait, a framed painting of your Mitchell home."),
         P("To confirm your prize, please return these within five business days:"),
         {"t": "list", "items": [
             "The signed affidavit of eligibility, release and publicity release (attached).",
             "A completed W-9. Prizes of $600 or more are reported on IRS Form 1099.",
             "A good time for a short call to plan the announcement and your Home Portrait."]},
         P("We announce the winner on Tuesday, December 15, so please keep it in the family until then. Thank you for letting us share your story.")]},
]

# ---------------------------------------------------------------- texts (E7 texts come from events.json)
PERSONAL = set()
TEXTS = [
    {"title": "Consultant invite to Homeowner Appreciation Night", "when": E7["invite_when"],
     "to": "Homeowners each New Home Consultant built with, 1-to-1, only where the consultant already texts that homeowner. A personal text, so no STOP line.",
     "body": E7["invite_text"]},
    {"title": "RSVP reminder", "when": E7["reminder_when"],
     "to": "Homeowners tagged homeowner appreciation rsvp who gave text consent.", "body": E7["reminder_text"]},
    {"title": "Thank-you after the event", "when": E7["thanks_when"],
     "to": "Each homeowner who came, 1-to-1 from the consultant who invited them. A personal text, so no STOP line.", "body": E7["thanks_text"]},
    {"title": "Contest launch", "when": "Thursday, November 12, 2026, between 10am and 7pm. Builder Studio bulk text.",
     "to": "Past homeowners with text consent who did not RSVP to Homeowner Appreciation Night and have not entered. Their only text that week.",
     "body": "Mitchell Homes: My Mitchell Story is open. Show us what you love about your home in a short video by Dec 6: [trigger link] Reply STOP to opt out"},
    {"title": "Photo session reminder", "when": "The day before each session. Workflow My Mitchell Story | 02, on the photo session calendar.",
     "to": "Entrants with a booked session who gave text consent.",
     "body": "Mitchell Homes: Your My Mitchell Story photo session is tomorrow at [time]. Need a different time? Just reply. Reply STOP to opt out"},
    {"title": "Last-week contest reminder", "when": "Thursday, December 3, 2026, between 10am and 7pm. Builder Studio bulk text.",
     "to": "Past homeowners with text consent who have not entered (no tag my mitchell story entry). Their only text that week. If sessions have run out, drop the words Photo sessions on us.",
     "body": "Mitchell Homes: What do you love most about your home? Show us in a short video by Sun, Dec 6. Photo sessions on us: [trigger link] Reply STOP to opt out"},
]
PERSONAL = {"Consultant invite to Homeowner Appreciation Night", "Thank-you after the event"}
SUBS = {"[first name]": "Jennifer", "[your name]": "Melissa", "[city]": "Fredericksburg", "[trigger link]": "xxxxxxx.xx/xxxxxx", "[time]": "4:15pm"}


def chars(t):
    for k, v in SUBS.items():
        t = t.replace(k, v)
    return len(t)


for t in TEXTS:
    t["characters"] = chars(t["body"])

SALES = [
    {"title": "Text to a homeowner you built with", "who": "New Home Consultants, 1-to-1",
     "when": "Wednesday, November 11 to Friday, December 4, to homeowners who have not entered (no tag my mitchell story entry)",
     "body": "Hi [first name], it is [your name] from Mitchell. My Mitchell Story is open: a short phone video about what you love about your home. Entrants get a photo session at home, on us, while they last. Want the link?",
     "notes": "A personal text from your own phone or your Builder Studio number, so no STOP line. Only where you already text this homeowner. Send the link only if they say yes."},
    {"title": "Short email to a homeowner you built with", "who": "New Home Consultants",
     "when": "Any time from Wednesday, November 11 to Wednesday, December 2, to homeowners who have not entered",
     "body": "Subject: I would love to see your home again\n\nHi [first name],\n\nI still think about [one thing about their home or their build], and I would love to see how the home has turned out with you in it.\n\nWe just opened My Mitchell Story for Mitchell homeowners. Film a short video on your phone, about 30 to 90 seconds, and tell us what you love most about your home, how you use it, or where you like to hang out. Everyone who enters gets a professional photo session at home, paid for by Mitchell, while sessions last, and the photos are yours to keep.\n\nHere is the link: " + u(ENTRY, "sales_email", "nhc_email") + "\n\nEntries close Sunday, December 6. If you have any questions, just reply." + SIG,
     "notes": "From your own address, so it reads like a person, because it is one. Skip anyone who already got your text and replied."},
    {"title": "20-second phone script", "who": "New Home Consultants",
     "when": "At the end of any call with a past homeowner, November 11 to December 4",
     "body": "Before I let you go: we just opened something for Mitchell homeowners called My Mitchell Story. You film a short video on your phone about what you love about your home, and everyone who enters gets a professional photo session at the house, on us, while sessions last. Can I text you the link?",
     "notes": "About 55 words. If they say yes, text the entry link and note it in Builder Studio."},
    {"title": "20-second script for the warranty team", "who": "Warranty team, on the phone or at the end of a visit",
     "when": "November 11 to December 4, only when the service item is resolved and the homeowner is happy",
     "body": "Glad we got that taken care of. One more thing, if you have a minute: Mitchell just opened My Mitchell Story for homeowners. It is a short phone video about what you love about your home, and everyone who enters gets a professional photo session at home, on us, while sessions last. Would you like someone to send you the link?",
     "notes": "Never on a call about an open or unresolved issue, and never if the homeowner is frustrated. Log the yes in Builder Studio so their consultant sends the link."},
]

# ---------------------------------------------------------------- social
SPOT_NOTES = ("Only entries with the spotlight box checked, after the coordinator confirms consent and the music rule. Credit first names and state; the town only if they agree; never a street, house number or child's name. "
              "Captions describe the home and the homeowner's words, never the town or neighborhood (fair housing). Quote word for word; trim any line Mitchell cannot claim (a build time, a price promise, financing terms). "
              "Organic only: never boost a video with people in it. Spotlights show variety, not a preview of the winners, and likes and views never count toward judging.")
MEN = "Never ask people to share, like or tag friends to enter (Meta promotion rules). Instagram: replace the link with Link in bio and set the bio link to {ig}."
SOCIAL = [
    {"title": "Announcement", "date": "Wednesday, November 11, 2026", "channels": "Facebook, Instagram feed",
     "format": "Single image of a real Mitchell home exterior with no people, or a 15-second Reel of home-only footage",
     "body": LINE + "\n\nMitchell homeowners, My Mitchell Story is open. Film a short video on your phone, about 30 to 90 seconds, and tell us what you love most about your home, how you use it, how it makes you feel, or where you like to hang out.\n\n" + SESSION.replace("theirs", "yours") + " " + FINALISTS + "\n\nEnter by Sunday, December 6: " + ENTRY + "\nOpen to Mitchell homeowners 18 or older. No purchase necessary. Official Rules: " + RULES + "\n\n#MyMitchellStory #MitchellHomes",
     "link": u(ENTRY, "facebook", "mms_announce"),
     "notes": "Image: e.g. " + M + "2026/3/24/07-DJI_20260224134444_0238_D_copy.jpg . Pin to the top of the Facebook page through December 6. Organic only. " + MEN.format(ig=u(ENTRY, "instagram", "mms_announce"))},
    {"title": "How to enter", "date": "Friday, November 13, 2026", "channels": "Instagram carousel, Facebook",
     "format": "Carousel, five slides of text on real Mitchell home photos with no people: 1 Every home is a portrait. Show us yours. 2 Film it at home. 3 Answer one question. 4 Send it in. 5 Your photo session is on us.",
     "body": "How to tell your Mitchell story, in four steps:\n\n1. Film a short video at home on your phone, about 30 to 90 seconds.\n2. Answer one or more: " + " ".join(PROMPTS) + "\n3. Send it through the entry form: upload it or paste a link.\n4. Book your photo session at home, on us, while sessions last.\n\nWant to share it too? Post it on your own Instagram or TikTok with #MyMitchellStory and tag us. Never required.\n\nEnter by Sunday, December 6: " + ENTRY + "\nOfficial Rules: " + RULES + "\n\n#MyMitchellStory",
     "link": u(ENTRY, "facebook", "mms_howto"),
     "notes": "Organic only. " + MEN.format(ig=u(ENTRY, "instagram", "mms_howto"))},
    {"title": "Filming tips", "date": "Tuesday, November 17, 2026", "channels": "Instagram Reels, Facebook Reels",
     "format": "30-second Reel: a team member's hands filming a Mitchell home on a phone, tips on screen. Home-only footage, no faces, no popular music.",
     "body": "Your phone is all you need. Five tips for your My Mitchell Story video:\n\nFilm in daylight, with the light in front of you.\nStart in your favorite spot, then tell us why.\nUse your own voice. No popular songs, so we can share it.\nHold steady, or prop the phone on a shelf.\nKeep house numbers and license plates out of the frame.\n\nOne take is fine. Real beats perfect. Enter by Sunday, December 6: " + ENTRY + "\n\n#MyMitchellStory",
     "link": u(ENTRY, "facebook", "mms_tips"),
     "notes": "If filmed in the Mitchell model home, do not name the plan until Brittany confirms its spelling. " + MEN.format(ig=u(ENTRY, "instagram", "mms_tips"))},
    {"title": "Entrant spotlight 1: a favorite place", "date": "Friday, November 20, 2026", "channels": "Facebook, Instagram Reels",
     "format": "The entrant's video as submitted, trimmed for length only",
     "body": "[First names] have lived in their Mitchell home in [state] since [year]. Their favorite place to hang out? [Their answer, in their words.]\n\nThis is My Mitchell Story. Mitchell homeowners, show us yours by Sunday, December 6: " + ENTRY + "\n\n#MyMitchellStory #MitchellHomes",
     "link": u(ENTRY, "facebook", "mms_spot1"), "notes": SPOT_NOTES},
    {"title": "Entrant spotlight 2: how it feels", "date": "Friday, November 27, 2026", "channels": "Facebook, Instagram Reels",
     "format": "The entrant's video as submitted, trimmed for length only",
     "body": "\"[How their home makes them feel, in their words.]\"\n\n[First names], Mitchell homeowners in [state], told us what coming home feels like. This is My Mitchell Story. Show us yours by Sunday, December 6: " + ENTRY + "\n\n#MyMitchellStory #MitchellHomes",
     "link": u(ENTRY, "facebook", "mms_spot2"), "notes": SPOT_NOTES},
    {"title": "Entrant spotlight 3: a day at home", "date": "Friday, December 4, 2026", "channels": "Facebook, Instagram Reels",
     "format": "The entrant's video as submitted, trimmed for length only",
     "body": "A day in [first names]' Mitchell home in [state] starts [where their day starts, in their words].\n\nThis is My Mitchell Story, and there are two days left to tell yours. Entries close Sunday, December 6, at 11:59pm Eastern: " + ENTRY + "\n\n#MyMitchellStory #MitchellHomes",
     "link": u(ENTRY, "facebook", "mms_spot3"), "notes": SPOT_NOTES},
    {"title": "Last call", "date": "Thursday, December 3, 2026 (Story again on Sunday, December 6)", "channels": "Facebook, Instagram feed and Stories",
     "format": "Single image of a real Mitchell home at dusk with no people; the Sunday Story uses the same image with the link sticker",
     "body": "Mitchell homeowners, there is still time. My Mitchell Story closes Sunday, December 6, at 11:59pm Eastern.\n\nA minute on your phone is enough. Show us the place you love most at home, and tell us why. Every eligible entrant gets a professional photo session at home, on us, while sessions last.\n\nEnter here: " + ENTRY + "\nOfficial Rules: " + RULES + "\n\n#MyMitchellStory",
     "link": u(ENTRY, "facebook", "mms_last"),
     "notes": "Image: e.g. " + M + "2026/3/3/ava_farmhouse-extended_sky.jpg . If sessions have run out, drop the photo session sentence. " + MEN.format(ig=u(ENTRY, "instagram", "mms_last"))},
    {"title": "Finalists", "date": "Thursday, December 10, 2026", "channels": "Facebook, Instagram carousel",
     "format": "Carousel: one home-only exterior photo from each finalist's session, with their release, first names and state on each slide",
     "body": "Meet the five My Mitchell Story finalists, one from each Design Center region.\n\n[First names, state: one line from their video, in their words.]\n[First names, state: one line.]\n[First names, state: one line.]\n[First names, state: one line.]\n[First names, state: one line.]\n\nThank you to every homeowner who showed us their home. The grand prize winner is announced Tuesday, December 15.\n\n#MyMitchellStory #MitchellHomes",
     "link": "",
     "notes": "Only finalists who returned their documents and agreed to publicity. Never show the Home Portrait paintings. Organic only."},
    {"title": "Grand prize winner", "date": "Tuesday, December 15, 2026", "channels": "Facebook, Instagram Reels, YouTube Shorts",
     "format": "The winner's video as submitted, with their release",
     "body": "[First names] love [what they love most about their home, in their words]. Their story, from their Mitchell home in [state], is the My Mitchell Story grand prize winner.\n\n\"[One line from their video, word for word.]\"\n\nThey receive $2,500 and their own Home Portrait, a framed painting of their Mitchell home. Thank you to every homeowner who told us their story. Every home is a portrait, and yours showed us why we build.\n\n#MyMitchellStory #MitchellHomes",
     "link": "",
     "notes": "Only after verification is complete. Never show the painting, not even at the hand-off: if Mitchell wants a moment on camera, film the winner's reaction with the frame turned away. Organic only."},
]

GBP = {
    "title": "My Mitchell Story: tell us about your home",
    "body": "Mitchell homeowners, what do you love most about your home? Show us in a short phone video, about 30 to 90 seconds, through Sunday, December 6, 2026. Every eligible entrant gets a professional photo session at home, paid for by Mitchell, while sessions last. " + FINALISTS + " Open to Mitchell homeowners 18 or older. No purchase necessary. Official Rules at the link.",
    "button": "Learn more",
    "link": u(ENTRY, "gbp", "mms_gbp"),
    "post_on": "All five Design Center profiles, Wednesday, November 11, after the E7 event post ends. Event-type post, start November 11, end December 6, 11:59pm.",
    "notes": "Image: a real Mitchell home exterior, no people. If Google rejects the event post, post it as an Update.",
}

# ---------------------------------------------------------------- entry form
FORM = {
    "name": "My Mitchell Story entry form",
    "where": "A Builder Studio form at [entry form link], linked from every contest email, post and text. Mobile first: most entrants fill it in on the phone that holds the video.",
    "intro": LINE + " Tell us about your Mitchell home in a short video, about 30 to 90 seconds, filmed on your phone. Entries close " + CLOSE + ".",
    "fields": [
        {"label": "First name", "type": "Text", "required": "Required", "help": ""},
        {"label": "Last name", "type": "Text", "required": "Required", "help": ""},
        {"label": "Email", "type": "Email", "required": "Required", "help": "We send your confirmation and your photo session link here."},
        {"label": "Mobile phone", "type": "Phone", "required": "Required", "help": "So we can reach you about your photo session and, if you are chosen, your prize."},
        {"label": "Address of your Mitchell home", "type": "Address: street, city, state, ZIP", "required": "Required", "help": "The home in your video. We use it to confirm the home and to plan your photo session. It is never published."},
        {"label": "State", "type": "Dropdown: Virginia, North Carolina, South Carolina, Maryland", "required": "Required", "help": ""},
        {"label": "Your Design Center region", "type": "Dropdown: Fredericksburg, Richmond, Newport News, Raleigh, Wilmington", "required": "Required", "help": "The Design Center that serves your area today. Not sure? Choose the closest and we will confirm."},
        {"label": "Year you moved in", "type": "Number", "required": "Optional", "help": ""},
        {"label": "Your floor plan, if you know it", "type": "Text", "required": "Optional", "help": ""},
        {"label": "Upload your video", "type": "File upload: MP4 or MOV", "required": "This or the link below", "help": "About 30 to 90 seconds, vertical or horizontal. [File size limit: confirm in Builder Studio.] Large file? Paste a link below instead."},
        {"label": "Or paste a link to your video", "type": "Website URL", "required": "This or the upload above", "help": "Instagram, TikTok, YouTube (unlisted is fine), Google Drive, iCloud or Dropbox. Make sure anyone with the link can view it."},
        {"label": "Which questions does your video answer?", "type": "Checkboxes: the four questions", "required": "Optional", "help": ""},
        {"label": "In one sentence, what do you love most about your home?", "type": "Short text", "required": "Optional", "help": "In your words. We may use it as a caption, with your permission."},
        {"label": "Did you post it too? Your Instagram or TikTok handle", "type": "Text", "required": "Optional", "help": "Never required to enter, and it does not affect judging."},
        {"label": "Photos at your session", "type": "Radio: The home only / The home and my family / I will decide at the session", "required": "Required", "help": "Family photos are only taken if you want them."},
        {"label": "Best times for your photo session", "type": "Checkboxes: weekday afternoons, weekday evenings, Saturday, Sunday", "required": "Optional", "help": "The front of the home looks best in the hour before sunset."},
        {"label": "Does anyone in your household work for Mitchell Homes, CEA Marketing, or a photographer or artist working on this contest?", "type": "Radio: No / Yes", "required": "Required", "help": "Household members of the contest team are not eligible. Thank you for understanding."},
    ],
    "consents": [
        {"label": "Eligibility", "required": "Required", "text": "I am 18 or older, I own a home built by Mitchell Homes in Virginia, North Carolina, South Carolina or Maryland, or live in it with the owner, and this is the only entry from my household."},
        {"label": "My video", "required": "Required", "text": "I made this video, it shows my Mitchell home, and it uses my own voice, natural sound or no music. It has no popular songs and nothing that belongs to someone else."},
        {"label": "People in my video", "required": "Required", "text": "Everyone who appears or can be heard in my video agreed to be in it. For anyone under 18, I am their parent or legal guardian, or I have their parent or guardian's permission."},
        {"label": "Official Rules and license", "required": "Required", "text": "I have read and agree to the Official Rules (" + RULES + "), including the license that lets Mitchell Homes share my video as the rules describe."},
        {"label": "Spotlight", "required": "Optional", "text": "Mitchell may feature my video in a weekly My Mitchell Story spotlight on its social media before judging. It does not affect judging."},
        {"label": "Text messages", "required": "Optional", "text": "[Legal-approved text consent wording, for example: Mitchell Homes may text me about my entry and photo session. Message and data rates may apply. Reply STOP to opt out.]"},
    ],
    "submit": "Send My Story",
    "thank_you": "Thank you, [first name]. Your story is in. Watch your email for a note from us, and once we confirm your entry, we will send a link to book your photo session.",
    "on_submit": {"tags": ["my mitchell story entry"], "workflow": "My Mitchell Story | 01 Entry received",
                  "notes": "If the text consent box is checked, record text consent the way the account already does for other forms."},
    "notes": [
        "Builder Studio forms may not enforce one of two fields. If not, make both optional and let workflow 01's coordinator task catch an entry with neither.",
        "If the household question is Yes, the entry still saves; the coordinator replies personally rather than the form showing an error.",
        "No painted Home Portrait or sample painting on the form page. A real Mitchell home photo, no people, as the header image.",
    ],
}

PHOTOGRAPHER = {
    "what": "One professional photo session at each verified entrant's Mitchell home, paid for by Mitchell. The homeowner keeps the edited photos. For the five finalists, the session photos are also the artist's reference for their Home Portrait.",
    "length": "About 45 to 60 minutes on site, plus travel.",
    "when": "Sessions roll as entries are confirmed, from mid-November through [January 31, 2027]. Book each session to end at the front of the home in the hour before sunset (roughly 4pm to 5pm in December).",
    "before": [
        "Watch the homeowner's entry video. Note the favorite spot and anything they said they love.",
        "Bring the model release and property release. Nothing is photographed until they are signed.",
        "Confirm the time the day before (the workflow sends a reminder text) and arrive on time.",
    ],
    "flow": [
        "Five minutes with the homeowner: what they love, the favorite spot from the video, and whether they want people in any photos.",
        "Interiors first, in natural light: the kitchen, the favorite spot, the living spaces.",
        "Details.",
        "Family moments, only if they want them.",
        "The porch, then the front elevation as the light turns golden.",
    ],
    "shot_list": [
        ["Front elevation at golden hour", "Straight on and from a three-quarter angle, interior lights on as the sun drops. The hero image of every session."],
        ["The porch", "The chairs, the front door, and the view from the porch looking out."],
        ["The kitchen", "Wide, then the island or table the way the family uses it."],
        ["The favorite spot", "The place the homeowner named in their video, wide and close."],
        ["Family moments, only if they want them", "Natural and candid, never staged. Children only with a parent there and agreeing."],
        ["Details", "Hardware, tile, the mantel, light through a window, the view out the back."],
        ["The land", "The yard, the trees, the view: the ground the home stands on."],
    ],
    "do_not_photograph": [
        "House numbers, street signs, numbered mailboxes and license plates.",
        "Mail, documents, screens, and family photos on the walls.",
        "Children's names on doors or walls, school logos, or anything else that identifies a child.",
        "Anything the homeowner asks you to skip.",
    ],
    "style": "Warm, never cool. Natural light, no hard shadows, lived in but uncluttered. Ask before moving anything, and put it back.",
    "delivery": "[25 to 40] edited images in an online gallery within [two weeks]: full resolution for the homeowner, and web and full-resolution sets for Mitchell. Label every image Home only, Adults or Children, so Mitchell knows where each one may run.",
    "release": "Every adult pictured signs a model release before the camera comes out, and a parent or legal guardian signs for each child. The owner signs a property release. Without signed releases, the session is home only. [Release forms: for Mitchell's legal to draft.]",
    "mitchell_use": "Images with people: organic social, email, Mitchell's websites, print and Design Centers, credited by first names and state. Home-only images: anywhere, including paid ads. Never in paid: any image with a person or a child. The photographer's agreement grants Mitchell this license and the homeowner a personal-use license; the photographer uses images in a portfolio only with the homeowner's OK.",
    "budget": "[Rate per session and travel, once Mitchell sets the budget and chooses photographers.]",
}

USAGE = [
    "Entries and session photos that show people, adults or children: organic social, email, Mitchell's websites, print and Design Center screens, only with the consent on the entry form and signed releases.",
    "Paid ads and paid landing pages: only home-only photos and clips, with no people and no children in the frame (Meta Housing category). A homeowner's voice over home-only footage in a paid ad needs Mitchell's and legal's OK first.",
    "Credit: first names and state, for example: Sarah and James, Mitchell homeowners, Virginia. The town only if the homeowner agrees. Never a street, a house number or a child's name.",
    "Word for word: quote homeowners exactly. Trim, never reword. If a homeowner says something Mitchell cannot claim (a build time, a price promise, financing terms), cut that part before Mitchell shares the video.",
    "Music: Mitchell never reuses a video that carries a popular song, and never adds one. Use the homeowner's own sound, or licensed library music.",
    "Spotlights before judging: only entries with the spotlight box checked.",
    "Fair housing: captions describe the home and the homeowner's own words, never a town or neighborhood as good, safe or desirable, and never who lives in a home.",
    "Home Portraits: the finalists' and the winner's paintings stay private, never in posts, emails, ads, the website or the Design Centers (CEA's recommendation, pending Mitchell's answer).",
    "Takedown: if a homeowner asks, Mitchell removes their entry from its own channels within [number] business days.",
    "How long: [license term] from the entry date, as the Official Rules set it.",
]

# ---------------------------------------------------------------- official rules (draft)
RULES_DRAFT = [
    ("DRAFT FOR MITCHELL'S LEGAL REVIEW", "These Official Rules are a working draft prepared by CEA Marketing for review by Mitchell Homes' legal counsel. They are not final, have not been reviewed by counsel, and make no legal conclusions. Every date, amount, value and number is a proposal for Mitchell to confirm, and bracketed items are placeholders. Nothing is published until legal approves the final text."),
    ("No purchase necessary", "NO PURCHASE OR PAYMENT OF ANY KIND IS NECESSARY TO ENTER OR WIN. A purchase or payment does not improve the chances of winning. [Legal: entry is limited to people who already own a home built by Mitchell Homes; confirm how this line should read.]"),
    ("Sponsor", "My Mitchell Story (the Contest) is sponsored by Mitchell Homes, Inc., 14300 Sommerville Court, Midlothian, VA 23113 (Mitchell or Sponsor). [Administrator, if any: Mitchell Homes or CEA Marketing, to confirm.] Questions: [contest email address]."),
    ("Eligibility", "The Contest is open to legal residents of the United States who are 18 or older at the time of entry and who own a home built by Mitchell Homes, Inc. in Virginia, North Carolina, South Carolina or Maryland, or who are an adult member of that owner's household and live in that home (Entrant). The video must show that home. Limit one entry per household; a household is everyone living at the same address. Not eligible: employees of Mitchell Homes, Inc., employees of CEA Marketing, the photographers and artists working on the Contest, and the members of their immediate families and households. [Legal: confirm whether owners who bought a Mitchell-built home from an earlier owner are eligible, and the household definition.]"),
    ("Entry period", "The Contest begins on Tuesday, November 10, 2026, at 5:30pm Eastern Time and ends on Sunday, December 6, 2026, at 11:59pm Eastern Time (the Entry Period). Sponsor's computer is the official clock. Entries received after the Entry Period ends are not eligible."),
    ("How to enter", "Complete the official entry form at " + ENTRY + " during the Entry Period: provide the requested information, upload a video file or paste a link to a video that Sponsor can view and download, and check the required consent boxes. A video posted on Instagram, TikTok or any other site is not an entry unless it is also submitted through the entry form. Posting on your own social media with #MyMitchellStory, or tagging Mitchell Homes, is welcome but never required, and has no effect on judging. Entrants are never asked to share on a personal Facebook timeline or to tag friends in order to enter. Sponsor may disqualify an incomplete entry, or an entry whose video cannot be viewed, after a reasonable attempt to contact the Entrant."),
    ("Content requirements", "Each entry is one original video of about 30 to 90 seconds (judges watch up to the first two minutes) that shows the Entrant's Mitchell home and answers one or more of these questions: " + " ".join(PROMPTS) + " The video must be made by the Entrant or a member of the Entrant's household; use the Entrant's own voice, natural sound or no music, with no commercial or popular music and no footage, artwork or other material owned by someone else; include only people who agreed to appear, with the consent of a parent or legal guardian for anyone under 18; and contain nothing unlawful, unsafe, defamatory, obscene or hateful, and nothing that disparages any person or group. Please keep house numbers, street signs and license plates out of the frame; Sponsor may trim or blur them before sharing. Sponsor may disqualify any entry that does not meet these requirements. The Entrant keeps ownership of the video."),
    ("Judging and criteria", "On or about December 7 and 8, 2026, a panel of [three to five] judges from Mitchell Homes and CEA Marketing will score every eligible entry on: the story, 40 percent (how clearly and personally the entry tells what the Entrant loves about the home, and why); the home in everyday life, 30 percent (how the home shows up in the way the Entrant lives: the rooms, the routines, the favorite places); and how it feels to watch, 30 percent (the warmth, honesty and feeling of home that come through). Judging never considers who appears in the video, how many people appear or whether anyone appears at all; the size, price, plan or location of the home; video production quality; or likes, views, comments or followers on any platform. The highest-scoring eligible entry from each of the five Mitchell Design Center regions (Fredericksburg, Richmond, Newport News, Raleigh and Wilmington, assigned by the region that serves the home's location) becomes a finalist. If a region has no eligible entries, that finalist place goes to the next-highest-scoring eligible entry from any region. The grand prize winner is the highest-scoring finalist. Ties are broken by the score for the story, then by a vote of the judges. The judges' decisions are final."),
    ("Prizes and approximate retail value", "Photo session, for every eligible Entrant while sessions last: one professional photo session at the Entrant's Mitchell home, about 45 to 60 minutes, with [number] edited digital photos delivered for the Entrant's personal use. Limited to the first [number] eligible entries [or: within a budget of [amount]]. Sessions take place after the entry is received, between [November 11, 2026] and [January 31, 2027], at a time arranged with Sponsor's photographer. Approximate retail value (ARV): [ARV] each. Finalist prize (five): the Entrant's own Home Portrait, a framed painting of their Mitchell home, about [size], by [artist], delivered on or about [date]. ARV: [ARV] each. Grand prize (one, chosen from the five finalists): $2,500 [form: check, prepaid card, gift card or other, to confirm], in addition to the finalist prize. ARV: $2,500. Total ARV of all prizes: [ARV total]. Prizes are not transferable. No substitution or cash equivalent, except that Sponsor may substitute a prize of equal or greater value if a prize becomes unavailable. Sessions not used by [January 31, 2027] and prizes not claimed are forfeited."),
    ("Taxes", "Winners are responsible for all federal, state and local taxes on prizes. Sponsor will issue IRS Form 1099 to any winner whose prizes from Sponsor total $600 or more in the year, including the grand prize winner, and may require a completed IRS Form W-9 before awarding a prize. The photo session's value is stated in these rules so Entrants know it. [Mitchell's tax advisor: confirm how the photo session and the Home Portrait are reported.]"),
    ("Odds", "This is a judged contest, not a random drawing. The odds of winning depend on the number and quality of the eligible entries received."),
    ("Winner notification and verification", "Potential finalists and the potential grand prize winner will be notified by phone and email on or about December 8, 2026. Each must respond, and return a signed affidavit of eligibility, a liability release and, where lawful, a publicity release, plus a W-9 where required, within five business days of notification. If a potential winner cannot be reached after reasonable attempts, does not respond in time, is found ineligible or does not comply with these rules, the prize may be forfeited and awarded to the next-highest-scoring eligible entry. Finalists are announced on or about December 10, 2026, and the grand prize winner on or about December 15, 2026, once verification is complete."),
    ("License to use entries", "The Entrant keeps ownership of the video. By entering, the Entrant grants Mitchell Homes, Inc. a non-exclusive, royalty-free license for [term, legal to set] to copy, edit for length, caption and share the entry, in whole or in part, with the Entrant's first name and state, on Mitchell's own social media accounts, in email, on Mitchell's websites, in print, and at Mitchell events and Design Centers. In paid advertising, Mitchell may use only portions of an entry that show no people. Mitchell is not required to use any entry. If an Entrant asks Mitchell to remove an entry, Mitchell will take it down from its own channels within [number] business days; materials already printed or distributed are not recalled. The Entrant confirms that everyone who appears in or can be heard in the video agreed to it, and that a parent or legal guardian agreed for anyone under 18."),
    ("Photo session photos", "The photographer delivers the edited photos to the Entrant for personal, non-commercial use. Everyone pictured signs a model release before the session (a parent or legal guardian for anyone under 18), and the owner signs a property release. Mitchell may use the session photos on the same terms as the license to use entries: photos with people only in organic social media, email, Mitchell's websites, print and Design Centers; in paid advertising, only photos with no people. [Photographer agreement: confirm the licenses to Mitchell and to the homeowner.]"),
    ("Publicity", "Except where prohibited by law, by accepting a prize each finalist and the grand prize winner agree that Mitchell may use their first names, state, entry, session photos and the fact that they won, without further compensation, as these rules describe. Mitchell never publishes an Entrant's street address or house number, or the names of children."),
    ("Release of Meta, Instagram and TikTok", "This Contest is in no way sponsored, endorsed or administered by, or associated with, Facebook, Instagram or Meta Platforms, Inc., or TikTok. By entering, each Entrant releases Meta Platforms, Inc., Facebook, Instagram and TikTok from all responsibility and liability related to the Contest. Any post an Entrant makes on a social media platform is subject to that platform's own terms."),
    ("Privacy", "Information collected on the entry form is used to run the Contest: to confirm eligibility, schedule photo sessions, contact Entrants and winners, and award prizes. It is handled under Mitchell's privacy policy at [privacy policy link]. Mitchell does not sell Entrant information, and never publishes an Entrant's home address. Marketing messages go only to Entrants who consented, and Entrants can opt out at any time."),
    ("General conditions", "Sponsor may disqualify any Entrant who tampers with the entry process, submits more than one entry per household, gives false information or acts in violation of these rules. If the Contest cannot run as planned for reasons beyond Sponsor's control, Sponsor may cancel, suspend or modify it and, if it is canceled, may award prizes from the eligible entries received before cancellation. Sponsor is not responsible for lost, late, incomplete, corrupted or misdirected entries, or for technical failures of any kind."),
    ("Release and limitation of liability", "By entering, Entrants release Sponsor, CEA Marketing, the photographers and artists, and their officers, employees and agents from liability for any injury, loss or damage arising from taking part in the Contest or a photo session, or from accepting or using a prize, to the extent the law allows. [Legal to draft.]"),
    ("Disputes and governing law", "[Legal to set: governing law, venue and dispute terms.]"),
    ("Winners list", "For the names of the winners, send a request to [contest email address or mailing address] by [date]."),
    ("Void where prohibited", "Void where prohibited or restricted by law. The Contest is subject to all applicable federal, state and local laws and regulations."),
    ("Questions for legal", "For counsel's review, with no conclusions from CEA: how a homeowner-only contest sits with the no purchase line; any registration, bonding or disclosure requirements in Virginia, North Carolina, South Carolina or Maryland; the 1099 threshold and how the photo session and the Home Portrait are valued and reported; whether a photo session for every eligible Entrant, limited to [number] sessions, needs its own terms; the license term and the takedown promise; consent for minors who appear in videos and photos; and whether judges from CEA Marketing need a conflict statement."),
]
RULES_JSON = [{"head": h, "text": t} for h, t in RULES_DRAFT]

QUESTIONS = [
    {"topic": "The $2,500", "question": "In what form does the grand prize winner receive $2,500: a check, a prepaid card, a gift card, or something else?", "recommend": "A check is the simplest to deliver and report."},
    {"topic": "Photo sessions", "question": "How many sessions, or what budget, and which photographers? One photographer per Design Center region, or one who travels? How far from a Design Center will they travel?", "recommend": "Set a number per region, so no region runs out first. CEA can shortlist photographers in each region. Sessions through January 31, 2027."},
    {"topic": "Home Portraits", "question": "Who paints the five Home Portraits, at what size, in what frame, by when, and at what value (for the rules)?", "recommend": "An artist working from each finalist's session photos, delivered privately in January."},
    {"topic": "Showing the paintings", "question": "May a finalist's or the winner's painting ever be shown publicly?", "recommend": "Keep them private. The painting is the reward, the same promise the Home Portrait quiz makes, and showing one would break the rule that no painted portrait appears before someone takes the quiz."},
    {"topic": "Judges", "question": "Who sits on the panel from Mitchell (for example Scott Sleeme, Deven Sellers, Brittany Horner) and from CEA Marketing, and how many judges in all?", "recommend": "Three to five judges, with no one judging an entry from a homeowner they personally sold to."},
    {"topic": "Homeowner Appreciation Night", "question": "Approve Tuesday, November 10, 5:30pm to 7:30pm at all five Design Centers, with staffing, refreshments and a budget per studio.", "recommend": "All five studios, with the photo session booking table and story corner at each. See E7 in events.md."},
    {"topic": "Official Rules", "question": "Legal review of the draft rules, including the questions for legal in its last section.", "recommend": "Start the review by October 23 so the rules are final before the October 28 invitation names the contest."},
    {"topic": "Eligibility", "question": "Are later owners of a Mitchell-built home (bought from an earlier owner) eligible? Do the exclusions cover CEA Marketing, the photographers and the artist, as drafted?", "recommend": "Yes to later owners, verified by deed or tax record. Keep the wider exclusions."},
    {"topic": "The homeowner list", "question": "Where do past homeowners live today (Builder Studio or Lasso), how are they marked, and which have email and text consent?", "recommend": "Build the Past Mitchell homeowners smart list in Builder Studio before October 26, with a view per division."},
    {"topic": "Homeowners with open warranty issues", "question": "Should homeowners with an open warranty issue get the invitation and contest emails?", "recommend": "Yes, after a personal call from their consultant or the warranty team first."},
    {"topic": "Contest coordinator", "question": "Who at Mitchell checks entries, books sessions and answers questions, and what email address appears in the rules?", "recommend": "One named coordinator and one contest inbox."},
    {"topic": "Usage", "question": "How long may Mitchell use entries (the license term), how are homeowners credited, and how fast are takedowns?", "recommend": "First names and state; three years; takedown within five business days."},
    {"topic": "Social handles", "question": "Which Mitchell Homes Instagram and TikTok handles do entrants tag?", "recommend": ""},
    {"topic": "Entry form", "question": "What video file size does the Builder Studio form accept?", "recommend": "If it is small, lead with the paste-a-link field and keep upload as the second option."},
]

BUILDER_STUDIO = {
    "note": "Nothing here has been created. The API can make tags, templates and trigger links; forms, smart lists, calendars and workflows are built by hand from this sheet, like the fall setup sheet.",
    "tags": [
        {"tag": "homeowner appreciation rsvp", "added_by": "The Homeowner Appreciation Night RSVP form, or a consultant when a homeowner RSVPs by reply", "used_for": "The reminder text on November 9; consultants' thank-you list"},
        {"tag": "my mitchell story entry", "added_by": "The entry form", "used_for": "Workflow 01, and excluding entrants from ho4, ho5 and the contest texts"},
        {"tag": "my mitchell story verified", "added_by": "The contest coordinator, after checking eligibility (CEA's addition to the three requested tags)", "used_for": "Workflow 02, the photo session booking note"},
        {"tag": "my mitchell story finalist", "added_by": "The contest coordinator, after judging and the phone call", "used_for": "Workflow 03, the finalist note, and the December 10 finalist list"},
    ],
    "smart_list": {
        "name": "Past Mitchell homeowners",
        "filters": ["[Whatever marks a closed home today: a homeowner tag, a closed or settled opportunity stage, or a list imported from Lasso. Mitchell to confirm.]",
                    "Email not unsubscribed (text sends also need text consent)",
                    "Not tagged as a Mitchell employee or employee household"],
        "views": "One view per division (Fredericksburg, Richmond, Newport News, Raleigh, Wilmington), so each studio sees its own homeowners for invites.",
        "used_by": "ho2 to ho6, the contest texts, and each consultant's invite list"},
    "forms": [
        "Homeowner Appreciation Night RSVP: name, email, phone, studio, number of guests, text consent. Adds homeowner appreciation rsvp.",
        "My Mitchell Story entry form: see the form spec. Adds my mitchell story entry.",
    ],
    "calendars": "My Mitchell Story photo sessions: one calendar per photographer or region, 60-minute slots plus travel, linked from hw2 as " + BOOK + ". Live by Monday, November 9, so homeowners can book at the event.",
    "trigger_links": [ENTRY, RSVP, RULES, BOOK],
    "workflows": [
        {"name": "My Mitchell Story | 00 Appreciation Night RSVP", "trigger": "Form submitted: Homeowner Appreciation Night RSVP",
         "steps": ["Add tag: homeowner appreciation rsvp", "Internal notification to the assigned consultant", "Wait until Monday, November 9, 10am", "If text consent: Send SMS, the RSVP reminder"]},
        {"name": "My Mitchell Story | 01 Entry received", "trigger": "Form submitted: My Mitchell Story entry form",
         "steps": ["Add tag: my mitchell story entry", "Send email hw1 (Your story is in) from the assigned user",
                   "Internal notification to the contest coordinator and the assigned consultant",
                   "Create task for the contest coordinator, due in 1 business day: check eligibility (Mitchell homeowner record and address, one entry per household, not a team household), that the video plays, the music rule, and the consent boxes",
                   "If the entry passes, the coordinator adds tag my mitchell story verified (starts workflow 02). If not, the coordinator calls the entrant."]},
        {"name": "My Mitchell Story | 02 Photo session", "trigger": "Contact tag added: my mitchell story verified",
         "steps": ["Send email hw2 (booking link) from the assigned user", "Wait 3 days, or until a session is booked on the photo session calendar",
                   "If no session is booked: create task for the coordinator to call and book",
                   "When a session is booked: the day before, if text consent, send the photo session reminder text; the photographer gets the calendar invite with the entry video link and the shot list"]},
        {"name": "My Mitchell Story | 03 Finalists", "trigger": "Contact tag added: my mitchell story finalist",
         "steps": ["The coordinator or consultant calls first; the tag goes on after the call",
                   "Send email hw3 from the assigned user (the grand prize winner gets hw4, sent by hand instead)",
                   "Wait 3 business days: if documents are not back, create task for the coordinator to call"]},
    ],
    "exclusions": "Every contest email and text after November 11 skips contacts tagged my mitchell story entry, except ho6, which goes to everyone.",
}

data = {
    "about": ABOUT,
    "name": NAME, "line": LINE, "hashtag": TAG, "summary": SUMMARY,
    "how_it_works": HOW, "prompts": PROMPTS, "prizes": PRIZES, "timeline": TIMELINE, "judging": JUDGING, "filming_tips": FILMING,
    "event": {"id": "e7", "name": E7["name"], "date": E7["date"], "time": E7["time"], "details": "campaigns/events/events.json and events.md"},
    "emails": EMAILS, "workflow_emails": WORKFLOW_EMAILS, "texts": TEXTS, "sales": SALES, "social": SOCIAL, "gbp": GBP,
    "form": FORM, "photographer": PHOTOGRAPHER, "rules": RULES_JSON, "usage": USAGE, "questions": QUESTIONS, "builder_studio": BUILDER_STUDIO,
}

# ---------------------------------------------------------------- checks
problems = []
blob = json.dumps(data, ensure_ascii=False)
for pat, why in [(r"[–—]", "em or en dash"), (r"Simply Mitchell", "SimplyMitchell is one word"), (r"New Home Specialist|[Ss]ales consultant", "title"),
                 (r"150 day|\bdays? from contract|\b\d+ days? to build", "build duration"), (r"price lock|locked pricing|price never changes", "pricing claim"),
                 (r"CEA Marketing Group", "agency name"), (r"HighLevel|GoHighLevel|LeadConnector|\bGHL\b", "vendor name"),
                 (r"Value Unlocker|Grounded Dreamer|Transitioner|\bPlanners?\b", "persona label"), (r" - |--", "hyphen as punctuation"),
                 (r"\b\d+ years (of|in business)|three decades|\d+ years building", "year count"), (r"\brebate|cash back|money off", "offer wording"),
                 (r"Mitchell funds your build", "unapproved financing line"), (r"filesafe\.space|watercolou?r", "painted portrait image or wording")]:
    for m in re.finditer(pat, blob):
        problems.append(f"{why}: ...{blob[max(0, m.start() - 50):m.end() + 50]}...")

# consumer-facing pieces: Meta promotion rules, fair housing, painting described in words only, Design Dollars kept out
consumer = []
for em in EMAILS + WORKFLOW_EMAILS:
    consumer.append((em["id"], " ".join([em["subject"], em["preview"], em.get("headline", "")] + [json.dumps(b, ensure_ascii=False) for b in em["blocks"]])))
consumer += [(t["title"], t["body"]) for t in TEXTS] + [(s["title"], s["body"]) for s in SALES] + [(s["title"], s["body"]) for s in SOCIAL]
consumer += [("gbp", GBP["title"] + " " + GBP["body"]), ("form", json.dumps({k: FORM[k] for k in ("intro", "fields", "consents", "submit", "thank_you")}, ensure_ascii=False))]
consumer += [("summary", SUMMARY), ("how_it_works", " ".join(HOW)), ("prizes", json.dumps(PRIZES)), ("filming_tips", " ".join(FILMING))]
for name, body in consumer:
    if re.search(r"tag (a|your) friends?|tag friends|share (this|it) (on|to) your (timeline|wall)|share to enter|like (this|our) (post|page) to enter|bonus entr", body, re.I):
        problems.append(f"{name}: asks for a share, like or friend tag (Meta promotion rules)")
    if re.search(r"\b(desirable|safe (area|neighborhood|town|community)|good (area|neighborhood|town|community)|family-friendly|best (area|neighborhood|town))\b", body, re.I):
        problems.append(f"{name}: fair housing wording")
    stripped = re.sub(r"framed painting of (their|your) Mitchell home", "", body)
    if re.search(r"\bpaint(ed|ing|ings|s)?\b", stripped, re.I):
        problems.append(f"{name}: mentions painting outside the approved prize wording")
    if "Design Dollars" in body or "SimplyMitchell" in body:
        problems.append(f"{name}: the homeowner contest carries no offer")

# email format
BLOCKS = {"p", "list", "steps", "quote", "cta", "small"}
PLAIN_BLOCKS = {"p", "list", "link"}
seen = set()
for em in EMAILS + WORKFLOW_EMAILS:
    i = em["id"]
    if i in seen:
        problems.append(f"{i}: duplicate id")
    seen.add(i)
    for k in ("id", "send", "segment", "subject", "preview", "blocks"):
        if not em.get(k):
            problems.append(f"{i}: missing {k}")
    allowed = PLAIN_BLOCKS if em.get("plain") else BLOCKS
    for b in em["blocks"]:
        if b["t"] not in allowed:
            problems.append(f"{i}: block type {b['t']} is not rendered in this mode")
        if b["t"] == "cta" and b["href"] not in (ENTRY, RSVP, "[winner video link]"):
            problems.append(f"{i}: CTA href {b['href']}")
    if not em.get("plain"):
        for k in ("hero_path", "hero_alt", "eyebrow", "headline"):
            if not em.get(k):
                problems.append(f"{i}: missing {k}")
        if em["hero_path"] not in HOMES:
            problems.append(f"{i}: hero_path {em['hero_path']} is not a Mitchell home photo used in series.py")
        first = em["blocks"][0]
        if first["t"] != "p" or re.search(r"\$|prize|photo session|finalist|\bwin(s|ner|ning)?\b|\bwon\b", first["text"], re.I):
            problems.append(f"{i}: Rule Zero, open with the home and the homeowner, not the prize")
    if len(em["subject"]) > 60:
        problems.append(f"{i}: subject {len(em['subject'])} characters")

# texts
for t in TEXTS:
    if t["characters"] > 160:
        problems.append(f"text {t['title']}: {t['characters']} characters")
    if t["title"] not in PERSONAL and "Reply STOP to opt out" not in t["body"]:
        problems.append(f"text {t['title']}: marketing text without the STOP line")
    if "$" in t["body"]:
        problems.append(f"text {t['title']}: texts lead with the home, never a dollar amount")
if len(GBP["title"]) > 58 or len(GBP["body"]) > 1500:
    problems.append("gbp title or body too long")
if len(SUMMARY.split(". ")) != 3:
    problems.append(f"summary is {len(SUMMARY.split('. '))} sentences, not three")
if "DRAFT" not in RULES_JSON[0]["head"]:
    problems.append("rules must open with the draft notice")

if problems:
    print("\n".join(problems))
    sys.exit(1)
open(f"{HERE}/contest.json", "w").write(json.dumps(data, indent=1, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- markdown for Kelly
def q(text):
    return "\n".join("> " + line if line else ">" for line in text.split("\n"))


def render_email(em):
    out = []
    for b in em["blocks"]:
        t = b["t"]
        if t == "p":
            out.append(b["text"])
        elif t == "small":
            out.append("*" + b["text"] + "*")
        elif t == "list":
            out.append("\n".join("- " + x for x in b["items"]))
        elif t == "steps":
            out.append("\n".join(f"{n}. **{h}** {x}" for n, (h, x) in enumerate(b["items"], 1)))
        elif t == "quote":
            out.append(f"“{b['text']}”\n{b['by']}. {b['linktext']}: `{b['link']}`")
        elif t == "cta":
            out.append(f"**[{b['text']}]** `{b['href']}`")
        elif t == "link":
            out.append(f"{b['text']}: `{b['href']}`")
    return "\n\n".join(out)


L = [f"# {NAME}: the fall 2026 homeowner contest", "",
     f"**{LINE}** {TAG}", "",
     "Drafts for Mitchell Homes, prepared by CEA Marketing for Kelly Bosetti. Built by `make_contest.py`; `contest.json` holds the same content. "
     "The kickoff event is E7, Homeowner Appreciation Night, in `campaigns/events/events.md`.", "",
     "## Read first", ""] + [f"- {a}" for a in ABOUT]
L += ["", "## The contest in three sentences", "", SUMMARY, "", "## How it works", ""] + [f"{n}. {s}" for n, s in enumerate(HOW, 1)]
L += ["", "## The four questions", ""] + [f"- {p}" for p in PROMPTS]
L += ["", "## Prizes (proposal)", "", "| Who | What | Notes |", "|---|---|---|"] + [f"| {p['tier']} | {p['what']} | {p['note']} |" for p in PRIZES]
L += ["", "## Timeline (proposal)", "", "| Date | What |", "|---|---|"] + [f"| {t['date']} | {t['what']} |" for t in TIMELINE]
L += ["", "## Judging", "", "| Criterion | Weight | What the judges look for |", "|---|---|---|"] + [f"| {j['criterion']} | {j['weight']} | {j['what']} |" for j in JUDGING]
L += ["", "## Filming tips (for homeowners)", ""] + [f"- {f}" for f in FILMING]
L += ["", "## Open questions for Mitchell", "", "| Topic | Question | CEA recommends |", "|---|---|---|"] + [f"| {x['topic']} | {x['question']} | {x['recommend']} |" for x in QUESTIONS]
L += ["", "---", "", "## Emails", "", "Series.py format. Every one is a draft and every one waits on Mitchell (see Hold)."]
for em in EMAILS:
    L += ["", f"### {em['id']} · {em['send']} · {em['subject']}", "",
          f"**To:** {em['segment']}  ", f"**Preview:** {em['preview']}  ",
          f"**Hero:** `{M + em['hero_path']}` ({em['hero_alt']})  ", f"**Eyebrow:** {em['eyebrow']}  ", f"**Headline:** {em['headline']}  ",
          f"**Hold:** {em.get('hold', 'None')}", "", render_email(em)]
L += ["", "## Workflow emails (plain personal notes)", "", "build.py adds Hi {{contact.first_name}} at the top and the {{user.name}}, New Home Consultant signature at the bottom."]
for em in WORKFLOW_EMAILS:
    L += ["", f"### {em['id']} · {em['subject']}", "", f"**When:** {em['send']}  ", f"**To:** {em['segment']}  ", f"**Preview:** {em['preview']}" + (f"  \n**Hold:** {em['hold']}" if em.get("hold") else ""), "", render_email(em)]
L += ["", "## Texts", ""]
for t in TEXTS:
    L += [f"**{t['title']}** ({t['characters']} of 160 characters with a typical name)  ", f"When: {t['when']}  ", f"To: {t['to']}", "", q(t["body"]), ""]
L += ["## Sales and warranty team scripts", ""]
for s in SALES:
    L += [f"### {s['title']}", "", f"**Who:** {s['who']}  ", f"**When:** {s['when']}", "", "```text", s["body"], "```", "", f"Notes: {s['notes']}", ""]
L += ["## Social posts", "", "Organic only. Nothing here is boosted."]
for s in SOCIAL:
    L += ["", f"### {s['title']} · {s['date']}", "", f"**Channels:** {s['channels']}  ", f"**Format:** {s['format']}", "", q(s["body"]), ""]
    if s["link"]:
        L.append(f"Link: `{s['link']}`  ")
    L.append(f"Notes: {s['notes']}")
L += ["", "## Google Business Profile post", "", f"Post on: {GBP['post_on']}", "", f"**Title:** {GBP['title']} ({len(GBP['title'])} of 58 characters)  ",
      f"**Button:** {GBP['button']}, linking to `{GBP['link']}`", "", q(GBP["body"]), "", f"Notes: {GBP['notes']}"]
L += ["", "## Entry form (Builder Studio)", "", FORM["where"], "", "**Intro at the top of the form:** " + FORM["intro"], "",
      "| Field | Type | Required | Help text |", "|---|---|---|---|"] + [f"| {f['label']} | {f['type']} | {f['required']} | {f['help']} |" for f in FORM["fields"]]
L += ["", "**Consent checkboxes**", "", "| Box | Required | Wording |", "|---|---|---|"] + [f"| {c['label']} | {c['required']} | {c['text']} |" for c in FORM["consents"]]
L += ["", f"**Submit button:** {FORM['submit']}  ", f"**Thank-you message:** {FORM['thank_you']}  ",
      f"**On submit:** tag `{', '.join(FORM['on_submit']['tags'])}`, workflow {FORM['on_submit']['workflow']}. {FORM['on_submit']['notes']}", ""] + [f"- {n}" for n in FORM["notes"]]
ph = PHOTOGRAPHER
L += ["", "## Photographer brief", "", ph["what"], "", f"**Length:** {ph['length']}  ", f"**When:** {ph['when']}", "", "**Before the session**", ""] + [f"- {x}" for x in ph["before"]]
L += ["", "**Session flow**", ""] + [f"{n}. {x}" for n, x in enumerate(ph["flow"], 1)]
L += ["", "**Shot list**", "", "| Shot | Notes |", "|---|---|"] + [f"| {a} | {b} |" for a, b in ph["shot_list"]]
L += ["", "**Do not photograph**", ""] + [f"- {x}" for x in ph["do_not_photograph"]]
L += ["", f"**Style:** {ph['style']}  ", f"**Delivery:** {ph['delivery']}  ", f"**Releases:** {ph['release']}  ", f"**What Mitchell may use, and where:** {ph['mitchell_use']}  ", f"**Budget:** {ph['budget']}"]
L += ["", "## Where entries and photos may be used", ""] + [f"- {x}" for x in USAGE]
bs = BUILDER_STUDIO
L += ["", "## Builder Studio setup", "", bs["note"], "", "**Tags**", "", "| Tag | Added by | Used for |", "|---|---|---|"] + [f"| `{t['tag']}` | {t['added_by']} | {t['used_for']} |" for t in bs["tags"]]
sl = bs["smart_list"]
L += ["", f"**Smart list: {sl['name']}**", ""] + [f"- {x}" for x in sl["filters"]] + ["", f"Views: {sl['views']}  ", f"Used by: {sl['used_by']}"]
L += ["", "**Forms**", ""] + [f"- {x}" for x in bs["forms"]] + ["", f"**Calendar:** {bs['calendars']}", "", "**Trigger links:** " + ", ".join(f"`{x}`" for x in bs["trigger_links"]), "", "**Workflows**", ""]
for w in bs["workflows"]:
    L += [f"*{w['name']}*. Trigger: {w['trigger']}", ""] + [f"{n}. {s}" for n, s in enumerate(w["steps"], 1)] + [""]
L += [f"**Exclusions:** {bs['exclusions']}", ""]
L += ["---", "", "## Official Rules (DRAFT for Mitchell's legal review)", ""]
for n, r in enumerate(RULES_JSON):
    L += [f"**{n}. {r['head']}**" if n else f"**{r['head']}**", "", r["text"], ""]
md = "\n".join(L) + "\n"
if re.search(r"[–—]", md):
    sys.exit("dash in markdown")
open(f"{HERE}/contest.md", "w").write(md)

print("contest.json and contest.md written")
print("emails:", ", ".join(f"{e['id']} ({e['send']}: {e['subject']})" for e in EMAILS))
print("workflow emails:", ", ".join(f"{e['id']} ({e['subject']})" for e in WORKFLOW_EMAILS))
print("texts:", len(TEXTS), [t["characters"] for t in TEXTS], "| sales:", len(SALES), "| social:", len(SOCIAL), "| rules sections:", len(RULES_JSON), "| questions:", len(QUESTIONS))
