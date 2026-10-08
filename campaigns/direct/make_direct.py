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
 ("SMS 2 · Home Portrait", "Wednesday, October 21", "Mitchell Homes: What would your home look like? Answer 8 questions, we paint your Home Portrait. 90 seconds: {link} Reply STOP to opt out", QUIZ, "fall26_portrait", "sms2"),
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
                  "notes": "Only contacts with SMS consent on file, minus anyone who opened the Tuesday email, took the quiz, or is talking with a consultant. Make the link a Builder Studio trigger link pointing at the URL here, so it stays short and clicks are tracked. Send between 10am and 7pm local time."})
sections = [{"id": "sms", "title": "Text messages", "why": "Texts get read within minutes, and every contact who opted in to texts already raised a hand.", "items": items}]

sales = [
 {"title": "Text to a cold or stalled lead (Home Portrait)", "meta": "New Home Consultants and online sales counselors · 1-to-1 texts",
  "body": "Hi [first name], it is [your name] with Mitchell Homes. We just launched something I think you will like. Answer eight quick questions about the home you have in mind, and we paint a portrait of it. About 90 seconds: mitchellhomesliving.com/portrait. Happy to walk through it with you after.",
  "link": u(QUIZ, "sales_text", "sms", "fall26_portrait", "nhc_text"), "notes": "Use the tracked link when texting from Builder Studio; the plain address is fine from a phone."},
 {"title": "Text to an in-market lead (Design Dollars)", "meta": "New Home Consultants · 1-to-1 texts",
  "body": "Hi [first name], quick update from Mitchell. Every home now starts with $5,000 in Design Dollars for your Design Center selections, and it goes up to $25,000 the more you personalize. Sign now and it is locked; your tier is set later, when you make your selections. Want me to show you where your plan would land on the ladder?",
  "link": u(DD, "sales_text", "sms", "fall26_designdollars", "nhc_text"), "notes": "Design Dollars never come off the base price and are never cash. If asked, say so plainly."},
 {"title": "Voicemail", "meta": "New Home Consultants · about 25 seconds",
  "body": "Hi [first name], this is [your name], a New Home Consultant with Mitchell Homes. I am calling with two things. Every Mitchell home now comes with $5,000 in Design Dollars, and it grows to $25,000 the more you personalize. And if you want to see what your home could look like first, we built a 90-second quiz at mitchellhomesliving.com slash portrait. Call or text me back at [number]. Thanks, [first name].", "link": "", "notes": ""},
 {"title": "Opening the first call with a Home Portrait lead", "meta": "From the Home Portrait sales deck",
  "body": "1. Open with their portrait. Say the portrait name and the region. They will recognize it.\n2. Ask about one thing they picked: a must-have, the land, or the people who will live there.\n3. Offer the next step their portrait named: a Design Studio visit, or a land walk if they have land.\nSkip: So, what are you looking for? They already told you.", "link": "", "notes": "The full scripts per portrait are in the Home Portrait deck inside the Fall Campaign Guide."},
 {"title": "Email signature line", "meta": "Everyone at Mitchell who emails buyers",
  "body": "See what your home could look like. Take the Home Portrait quiz: mitchellhomesliving.com/portrait",
  "link": u(QUIZ, "email_signature", "email", "fall26_portrait", "signature_line"), "notes": "Or use the signature banner image in the print section. Host it in the Builder Studio media library and link it with this URL."},
]
sections.append({"id": "sales", "title": "Sales team kit", "why": "Every conversation the team already has can carry the quiz or the offer, at no cost.", "items": sales})

SIG = "\n\n[your name]\nNew Home Consultant, Mitchell Homes\n[your phone]"
FINE = "\n\nDesign Dollars apply to Design Center selections only. Not applied to base price. No cash value."
followups = [
 {"title": "Quiz taker: first text", "meta": "Within 15 minutes of the quiz · online sales counselor · text",
  "body": "Hi [first name], this is [your name] with Mitchell Homes. Your [portrait name] just came through, and I love the [first must have] you picked. Would you like to see what it would take to build it? I can set up a quick call or a Design Studio visit.",
  "notes": "Merge fields: contact.portrait_name and contact.design_dollars_focus. Only when the buyer gave text consent on the quiz. This replaces the generic first touch for quiz leads."},
 {"title": "Quiz taker: next-day email", "meta": "Next day, if no reply · online sales counselor or New Home Consultant · personal email",
  "body": "Subject: Your [portrait name]\n\nHi [first name],\n\nI had a chance to look at your Home Portrait. [Region] is a beautiful place to build, and the [first must have] you picked tells me a lot about how you want to live.\n\nTwo things worth knowing as you think it over. Mitchell self-funds every build, so on land you own there is zero down and no construction loan. And every Mitchell home now starts with $5,000 in Design Dollars, up to $25,000 the more you personalize.\n\nWould you like to see the Design Studio, or start with a 15-minute call? Reply with a time that works and I will hold it for you." + SIG + FINE,
  "notes": "Plain text, sent from the consultant's own address so it reads like a person, because it is one."},
 {"title": "Clicked a Design Dollars email: text", "meta": "Within one business day of the click · online sales counselor · text",
  "body": "Hi [first name], [your name] with Mitchell Homes. Every home now starts with $5,000 in Design Dollars for your Design Center selections, up to $25,000 the more you personalize. Happy to show you where your plan would land. Would a quick call this week work?",
  "notes": "Never mention that they clicked. The click only decides who hears from us first."},
 {"title": "Design Dollars: personal email to active leads", "meta": "Thursday, October 22 · every New Home Consultant to their own active leads · personal email",
  "body": "Subject: Where your plan lands on the Design Dollars ladder\n\nHi [first name],\n\nQuick note on something new this fall. Every Mitchell home now comes with $5,000 in Design Dollars for your Design Center selections, and the more you personalize, the more Mitchell adds, up to $25,000. Choose $60,000 in selections, for example, and Mitchell adds $15,000, so you take home $75,000 worth.\n\nYou do not have to pick a single finish to secure it. Sign now and your incentive is locked; your tier is set later, when you sit down at the Design Center.\n\nIf you tell me the plan you are leaning toward, I will show you where it would land on the ladder." + SIG + FINE,
  "notes": "One email per lead, from their own consultant. Skip anyone who already heard about Design Dollars in a call this month."},
 {"title": "Deadline week: personal email", "meta": "Tuesday, October 27 · every New Home Consultant to active leads · personal email",
  "body": "Subject: Before October 31\n\nHi [first name],\n\nIf building on your land is on your list for next year, this is a good week to lock it in. Reserve by Saturday, October 31, and your Design Dollars are locked: $5,000 to start, up to $25,000 the more you personalize. Your tier is set later, when you choose your finishes.\n\nThe reservation deposit is $150, and that is all Mitchell receives until closing.\n\nWant to talk it through this week? Reply with a time, or call me at the number below." + SIG + FINE,
  "notes": "If Mitchell approves a November date, the same email runs the week of November 23 with the new date."},
 {"title": "Deadline week: text", "meta": "Thursday, October 29 · every New Home Consultant to active leads with text consent · text",
  "body": "Hi [first name], a quick heads-up from [your name] at Mitchell. Reserve by Saturday, Oct 31 and your Design Dollars are locked. You choose your finishes later, and the deposit is $150. Want me to walk you through it before Saturday?",
  "notes": "Send only to leads who have not reserved and did not reply to Tuesday's email."},
 {"title": "Clicked a Four Buyers email or page: text", "meta": "Within one business day · New Home Consultant for that division · text",
  "body": "Hi [first name], [your name] with Mitchell Homes. If you own land, it can count toward your home: zero down, zero closing costs and no construction loan, because Mitchell self-funds every build. Would you like me to run the numbers for your land?",
  "notes": "Financing terms are illustrative only and subject to credit approval; say so if they ask about numbers."},
 {"title": "Landowner: follow-up email", "meta": "Two days after the text, if no reply · New Home Consultant · personal email",
  "body": "Subject: Your land, in numbers\n\nHi [first name],\n\nMost landowners do not realize how far along they already are. With Mitchell, the land you own counts toward the home, there is no construction loan, and there is one closing instead of two.\n\nTell me the county and roughly how many acres, and I will put together what building on it could look like, including the plans that fit.\n\nFinancing terms are illustrative only and subject to credit approval. Not a commitment to lend." + SIG,
  "notes": "Plain text. Attach nothing; the conversation is the point."},
 {"title": "Looking for land: text", "meta": "Within one business day of a No Land click or a quiz answer of still looking · New Home Consultant · text",
  "body": "Hi [first name], [your name] with Mitchell Homes. We do not sell land, but you can start designing now and bring us the lot when you find it. Would you like to walk the plan library at a Design Studio?",
  "notes": "Never recommend counties or describe areas as desirable."},
 {"title": "After a Design Center visit: text", "meta": "Same day · Design Consultant or New Home Consultant · text",
  "body": "Thank you for coming in today, [first name]. You are [amount] away from the next Design Dollars tier, which adds [amount] more for your selections. Anything you want me to price before we talk next?",
  "notes": "Scott's rule at the design table: tell them the gap. Fill the amounts from the ladder."},
 {"title": "Old-lead check-in: text and email", "meta": "Once this fall, Thursday, November 12 · New Home Consultant to leads quiet for six months or more",
  "body": "Text: Hi [first name], [your name] with Mitchell Homes. It has been a while. We built a 90-second quiz that paints a portrait of the home you have in mind: mitchellhomesliving.com/portrait. If building is still on your list, I am here.\n\nEmail subject: Still thinking about building?\nHi [first name], it has been a while since we talked, so I wanted to share something new. Answer eight questions about the home you have in mind, and we paint your Home Portrait, along with what it would take to build it on your land. It takes about 90 seconds: mitchellhomesliving.com/portrait. If the timing is right, I would love to help." + SIG,
  "notes": "Text only to leads with text consent; everyone else gets the email."},
 {"title": "Bring your photos: text", "meta": "Thursday, November 19 · New Home Consultants to active leads with text consent · text",
  "body": "Hi [first name], [your name] with Mitchell Homes. If you have been saving photos of the home you want, bring them in. We will sit down with the plans and price what is in them. Would [day] work for a Design Studio visit?",
  "notes": "The personal side of the Dreamer email the same day. Fine to send even while that email waits on question 5, because this text makes no pricing claim."},
 {"title": "Realtor follow-up email", "meta": "Two days after the realtor email, to agents who opened it · New Home Consultant · personal email",
  "body": "Subject: Clients with land\n\nHi [first name],\n\nFollowing up on Mitchell's note this week. If you have a client who owns land, or is about to buy some, we would love to help them build on it: zero down, zero closing costs and no construction loan, and every home starts with $5,000 in Design Dollars, up to $25,000.\n\nHappy to meet for coffee or set up a call with your client. [Realtor incentive terms, once Mitchell confirms them.]" + SIG + FINE,
  "notes": "Waits on the realtor incentive terms (question 11)."},
]
nurture_texts = [
 ("Day 2 · every quiet lead", "Hi {{contact.first_name}}, this is {{user.first_name}} with Mitchell Homes. Still thinking about building? Reply 1 for this year, 2 for next year, or 3 for someday.", ""),
 ("Day 19 · quiet leads who took the Home Portrait", "Hi {{contact.first_name}}, {{user.first_name}} with Mitchell Homes. Your {{contact.portrait_name}} is saved. Want to see what it would take to build it? Just reply.", ""),
 ("Day 19 · quiet leads who have not taken it", "Hi {{contact.first_name}}, {{user.first_name}} with Mitchell. Answer 8 questions about your dream home and we paint your Home Portrait: [trigger link]", QUIZ),
 ("Day 45 · quiet leads who own land", "Hi {{contact.first_name}}, {{user.first_name}} with Mitchell. A short Behind the Build episode on how building on your land works: [trigger link]", "https://www.youtube.com/watch?v=HEqg3pcNJkk"),
 ("Day 45 · quiet leads still looking for land", "Hi {{contact.first_name}}, {{user.first_name}} with Mitchell. A short Behind the Build episode on buying land for a home: [trigger link]", "https://www.youtube.com/watch?v=trgJ8maymOA"),
]
nitems = []
for when_, text, url in nurture_texts:
    est = text.replace("{{contact.first_name}}", "Jennifer").replace("{{user.first_name}}", "Melissa").replace("{{contact.portrait_name}}", "Landowner's Portrait").replace("[trigger link]", "xxxxxxx.xx/xxxxxx")
    full = est + " Reply STOP to opt out"
    if len(full) > 160: sys.exit(f"nurture text too long ({len(full)}): {when_}")
    nitems.append({"title": "Nurture text, " + when_.split(" · ")[0], "meta": when_ + f" · Builder Studio workflow text · about {len(full)} of 160 characters with a typical name",
                   "body": text + " Reply STOP to opt out", "link": u(url, "sms", "sms", "fall26_nurture", "nurture_" + when_.split(" ")[1]) if url.startswith("https://mitchell") else url,
                   "notes": "Only with text consent. Any reply ends the sequence and alerts the consultant."})
sections.append({"id": "nurture", "title": "Quiet-lead nurture texts", "why": "Short texts with a question to answer get replies that emails do not; any reply hands the lead straight back to a person.", "items": nitems})
sections.append({"id": "followups", "title": "Sales team follow-ups", "why": "Marketing starts the conversation; a person finishes it. Each follow-up fires on what the buyer just did, in the consultant's own voice.", "items": followups})

web = [
 {"title": "Website announcement bar, Design Dollars", "meta": "mitchellhomesinc.com, top of every page, through October 31",
  "body": "Every Mitchell home now starts with $5,000 in Design Dollars, up to $25,000. See how it works", "link": u(DD, "mitchellhomesinc", "announcement_bar", "fall26_designdollars", "bar"),
  "notes": "The words See how it works are the link. The Design Dollars page carries the fine print."},
 {"title": "Website announcement bar, Home Portrait", "meta": "mitchellhomesinc.com, alternate weeks or after October 31",
  "body": "Every home is a portrait. Discover yours in about 90 seconds. Take the quiz", "link": u(QUIZ, "mitchellhomesinc", "announcement_bar", "fall26_portrait", "bar"), "notes": "Pair with the website pop-up, which never shows on pages that already link the quiz."},
 {"title": "Missed-call text-back", "meta": "Builder Studio automation, every division number",
  "body": "Sorry we missed you. This is Mitchell Homes. A New Home Consultant will call you back shortly. While you wait, see what your home could look like: mitchellhomesliving.com/portrait",
  "link": u(QUIZ, "missed_call", "sms", "fall26_portrait", "text_back"), "notes": "Only where the account already sends a missed call text and the caller can receive texts. Keep the callback promise as written; it does not name a time."},
 {"title": "Every form thank-you page", "meta": "All Builder Studio and older campaign forms",
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
  "body": "A 20-minute live session where Scott and Deven answer Design Dollars and SimplyMitchell questions from viewers. Collect questions beforehand with a social post and a line in the Design Dollars email.", "link": "", "notes": "The recording becomes three or four Shorts, one question each."},
]
sections.append({"id": "events", "title": "Events", "why": "Mitchell already has five studios and an event format; they can carry both campaigns without paid media.", "items": events})

printp = [
 {"title": "Home Portrait counter card (5 x 7 in)", "meta": "Design Center counters, event tables, closing packets", "body": "Every home is a portrait. Discover Yours. QR code to the quiz.", "link": u(QUIZ, "designcenter", "print", "fall26_portrait", "counter_card"), "notes": "Files: portrait-counter-card.pdf and .png. Print on heavy card stock; fold a second copy into a tent if needed."},
 {"title": "Design Dollars counter card (5 x 7 in)", "meta": "The design table at every Design Center", "body": "The ladder, the sign-now line, and a QR code to the Design Dollars page, with fine print.", "link": u(DD, "designcenter", "print", "fall26_designdollars", "counter_card"), "notes": "Files: design-dollars-counter-card.pdf and .png. Lets a consultant point at the gap to the next tier, as Scott asked."},
 {"title": "Landowner community board flyer (8.5 x 11 in)", "meta": "Feed and farm supply stores, hardware stores, county extension offices, libraries, in the counties Mitchell serves", "body": "Own land? See what it could Become. Zero down, zero closing costs, no construction loan. QR code and tear-off tabs to the quiz.", "link": u(QUIZ, "community_board", "print", "fall26_portrait", "flyer"), "notes": "Files: landowner-community-flyer.pdf and .png. Ask before posting; many stores keep a community board for exactly this. Replace monthly."},
]
sections.append({"id": "print", "title": "Print", "why": "Landowners in rural counties still read the board at the feed store; the QR code makes every flyer measurable.", "items": printp})

text = json.dumps({"sections": sections}, indent=1, ensure_ascii=False)
if re.search(r"[–—]", text): sys.exit("dash found")
open(f"{HERE}/direct.json", "w").write(text)
for s in sections: print(s["id"], len(s["items"]))
for i in items: print(i["meta"])
