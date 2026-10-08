#!/usr/bin/env python3
"""Direct traffic pieces: SMS, sales team scripts, website snippets, events, print placement.
usage: python3 campaigns/direct/make_direct.py   writes direct.json (same shape as campaigns/traffic/organic.json)"""
import json, os, re, sys
from urllib.parse import urlencode
HERE = os.path.dirname(os.path.abspath(__file__))
QUIZ, DD, SMH = "https://mitchellhomesliving.com/portrait", "https://simplymitchellhomes.com/design-dollars", "https://simplymitchellhomes.com"
def u(url, src, med, camp, cont):
    return url + "?" + urlencode({"utm_source": src, "utm_medium": med, "utm_campaign": camp, "utm_content": cont})

sms = [
 ("SMS 1 · Design Dollars", "Wednesday, October 14", "Mitchell Homes: Every home now starts with $5,000 in Design Dollars, up to $25,000 as you personalize. Terms apply. {link} Reply STOP to opt out", DD, "fall26_designdollars", "sms1"),
 ("SMS 2 · Home Portrait", "Friday, October 16", "Mitchell Homes: What would your home look like? Answer 8 questions, we paint your Home Portrait. 90 seconds: {link} Reply STOP to opt out", QUIZ, "fall26_portrait", "sms2"),
 ("SMS 3 · Design Dollars reserve by", "Wednesday, October 28", "Mitchell Homes: Reserve by Oct 31 and your Design Dollars are locked. Choose finishes later. Terms apply. Questions? Just reply. STOP to opt out", None, "fall26_designdollars", "sms3"),
 ("SMS 4 · Landowners", "Wednesday, November 4", "Mitchell Homes: Your land can be your down payment. Zero down, zero closing costs, no construction loan. Terms apply. {link} STOP to opt out", SMH + "/land", "fall26_fourbuyers", "sms4"),
]
items = []
for title, when, text, url, camp, cid in sms:
    link = u(url, "sms", "sms", camp, cid) if url else ""
    short = text.replace("{link}", "xxxxxxx.xx/xxxxxx")  # a trigger link is about 18 characters
    n = len(short)
    if n > 160: sys.exit(f"{title}: {n} characters")
    items.append({"title": title, "meta": f"{when} · Builder Studio bulk SMS · {n} of 160 characters with a short trigger link",
                  "body": text.replace("{link}", "[trigger link]") if url else text, "link": link,
                  "notes": "Only contacts with SMS consent on file. Make the link a Builder Studio trigger link pointing at the URL here, so it stays short and clicks are tracked. Send between 10am and 7pm local time."})
sections = [{"id": "sms", "title": "Text messages", "why": "Texts get read within minutes, and every contact who opted in to texts already raised a hand.", "items": items}]

sales = [
 {"title": "Text to a cold or stalled lead (Home Portrait)", "meta": "New Home Consultants and online sales counselors · 1 to 1 texts",
  "body": "Hi [first name], it is [your name] with Mitchell Homes. We just launched something I think you will like. Answer eight quick questions about the home you have in mind, and we paint a portrait of it. About 90 seconds: mitchellhomesliving.com/portrait. Happy to walk through it with you after.",
  "link": u(QUIZ, "sales_text", "sms", "fall26_portrait", "nhc_text"), "notes": "Use the tracked link when texting from Builder Studio; the plain address is fine from a phone."},
 {"title": "Text to an in market lead (Design Dollars)", "meta": "New Home Consultants · 1 to 1 texts",
  "body": "Hi [first name], quick update from Mitchell. Every home now starts with $5,000 in Design Dollars for your Design Center selections, and it goes up to $25,000 the more you personalize. Sign now and it is locked; your tier is set later, when you make your selections. Want me to show you where your plan would land on the ladder?",
  "link": u(DD, "sales_text", "sms", "fall26_designdollars", "nhc_text"), "notes": "Design Dollars never come off the base price and are never cash. If asked, say so plainly."},
 {"title": "Voicemail", "meta": "New Home Consultants · about 25 seconds",
  "body": "Hi [first name], this is [your name], a New Home Consultant with Mitchell Homes. I am calling with two things. Every Mitchell home now comes with $5,000 in Design Dollars, and it grows to $25,000 the more you personalize. And if you want to see what your home could look like first, we built a 90 second quiz at mitchellhomesliving.com slash portrait. Call or text me back at [number]. Thanks, [first name].", "link": "", "notes": ""},
 {"title": "Opening the first call with a Home Portrait lead", "meta": "From the Home Portrait sales deck",
  "body": "1. Open with their portrait. Say the portrait name and the region. They will recognize it.\n2. Ask about one thing they picked: a must have, the land, or the people who will live there.\n3. Offer the next step their portrait named: a Design Studio visit, or a land walk if they have land.\nSkip: So, what are you looking for? They already told you.", "link": "", "notes": "The full scripts per portrait are in the Home Portrait deck inside the Fall Campaign Guide."},
 {"title": "Email signature line", "meta": "Everyone at Mitchell who emails buyers",
  "body": "See what your home could look like. Take the Home Portrait quiz: mitchellhomesliving.com/portrait",
  "link": u(QUIZ, "email_signature", "email", "fall26_portrait", "signature_line"), "notes": "Or use the signature banner image in the print section. Host it in the Builder Studio media library and link it with this URL."},
]
sections.append({"id": "sales", "title": "Sales team kit", "why": "Every conversation the team already has can carry the quiz or the offer, at no cost.", "items": sales})

web = [
 {"title": "Website announcement bar, Design Dollars", "meta": "mitchellhomesinc.com, top of every page, through October 31",
  "body": "Every Mitchell home now starts with $5,000 in Design Dollars, up to $25,000. See how it works", "link": u(DD, "mitchellhomesinc", "announcement_bar", "fall26_designdollars", "bar"),
  "notes": "The words See how it works are the link. The Design Dollars page carries the fine print."},
 {"title": "Website announcement bar, Home Portrait", "meta": "mitchellhomesinc.com, alternate weeks or after October 31",
  "body": "Every home is a portrait. Discover yours in about 90 seconds. Take the quiz", "link": u(QUIZ, "mitchellhomesinc", "announcement_bar", "fall26_portrait", "bar"), "notes": "Pair with the website pop-up, which never shows on pages that already link the quiz."},
 {"title": "Missed call text back", "meta": "Builder Studio automation, every division number",
  "body": "Sorry we missed you. This is Mitchell Homes. A New Home Consultant will call you back shortly. While you wait, see what your home could look like: mitchellhomesliving.com/portrait",
  "link": u(QUIZ, "missed_call", "sms", "fall26_portrait", "text_back"), "notes": "Only where the account already sends a missed call text and the caller can receive texts. Keep the callback promise as written; it does not name a time."},
 {"title": "Every form thank you page", "meta": "All Builder Studio and older campaign forms",
  "body": "Thank you. A New Home Consultant will be in touch soon. While you wait, take 90 seconds to see what your home could look like.\n[Take the Quiz]", "link": u(QUIZ, "thank_you_page", "website", "fall26_portrait", "thank_you"),
  "notes": "Adds the quiz to the busiest moment of intent on the site. The answers then reach the consultant before the first call."},
]
sections.append({"id": "website", "title": "Website and automations", "why": "People already on the site or already in the CRM are the cheapest clicks there are.", "items": web})

events = [
 {"title": "Bring Your Photos Saturdays", "meta": "Proposal · all five Design Centers · needs Mitchell approval and staffing",
  "body": "Open studio hours on two Saturdays this fall. Buyers bring the photos they have been saving, sit with a Design Consultant, and see what their favorites cost and which Design Dollars tier they would reach. Promote it in the Design Dollars emails, a text, the Google Business Profile event post for each studio, and Facebook events.",
  "link": u(DD, "event", "event", "fall26_designdollars", "photos_saturday"), "notes": "Ties the Design Dollars offer to the Grounded Dreamer argument: one appointment, bring the photos."},
 {"title": "Fold both campaigns into the next Sip and See", "meta": "Proposal · existing event · needs Mitchell approval",
  "body": "At the next Sip and See, put the Home Portrait counter card on every table and the Design Dollars card at the design table. Guests take the quiz on their phones and walk out with their portrait in their inbox.", "link": "", "notes": "Uses an event Mitchell already runs; adds no cost beyond printing."},
 {"title": "Behind the Build live: your Design Dollars questions", "meta": "Proposal · Facebook and YouTube live · needs Scott and Deven",
  "body": "A 20 minute live session where Scott and Deven answer Design Dollars and SimplyMitchell questions from viewers. Collect questions beforehand with a social post and a line in the Design Dollars email.", "link": "", "notes": "The recording becomes three or four Shorts, one question each."},
]
sections.append({"id": "events", "title": "Events", "why": "Mitchell already has five studios and an event format; they can carry both campaigns without paid media.", "items": events})

printp = [
 {"title": "Home Portrait counter card (5 x 7 in)", "meta": "Design Center counters, event tables, closing packets", "body": "Every home is a portrait. Discover Yours. QR code to the quiz.", "link": u(QUIZ, "designcenter", "print", "fall26_portrait", "counter_card"), "notes": "Files: portrait-counter-card.pdf and .png. Print on heavy card stock; fold a second copy into a tent if needed."},
 {"title": "Design Dollars counter card (5 x 7 in)", "meta": "The design table at every Design Center", "body": "The ladder, the sign now line, and a QR code to the Design Dollars page, with fine print.", "link": u(DD, "designcenter", "print", "fall26_designdollars", "counter_card"), "notes": "Files: design-dollars-counter-card.pdf and .png. Lets a consultant point at the gap to the next tier, as Scott asked."},
 {"title": "Landowner community board flyer (8.5 x 11 in)", "meta": "Feed and farm supply stores, hardware stores, county extension offices, libraries, in the counties Mitchell serves", "body": "Own land? See what it could Become. Zero down, zero closing costs, no construction loan. QR code and tear off tabs to the quiz.", "link": u(QUIZ, "community_board", "print", "fall26_portrait", "flyer"), "notes": "Files: landowner-community-flyer.pdf and .png. Ask before posting; many stores keep a community board for exactly this. Replace monthly."},
]
sections.append({"id": "print", "title": "Print", "why": "Landowners in rural counties still read the board at the feed store; the QR code makes every flyer measurable.", "items": printp})

text = json.dumps({"sections": sections}, indent=1, ensure_ascii=False)
if re.search(r"[–—]", text): sys.exit("dash found")
open(f"{HERE}/direct.json", "w").write(text)
for s in sections: print(s["id"], len(s["items"]))
for i in items: print(i["meta"])
