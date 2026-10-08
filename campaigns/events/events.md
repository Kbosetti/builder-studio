# Mitchell Homes fall events, October 12 to November 22, 2026

Seven event proposals for CEA Marketing (Kelly Bosetti), each with every invitation and follow-up. Built from `campaigns/FACTS.md` by `make_events.py`; `events.json` holds the same content.

## Read first

- Drafts only. Nothing has been sent, posted, scheduled or created in any system. Every event is a proposal until Mitchell approves its date and staffing.
- [RSVP link] is the Builder Studio form Kelly will create (one per event, or one form with an event field). Every link field shows the tracked version: put the real form URL where [RSVP link] sits and keep the UTM string, so each RSVP shows where it came from. In body copy, paste the link from that item's link field.
- Cadence: no new marketing emails and no extra marketing texts. Invitations ride existing emails, social, Facebook events, Google profiles, Nextdoor and personal consultant messages. The only bulk text is E4's on November 11. E7 is the one exception: a thank-you evening for past homeowners gets its own homeowner invitation (ho2, October 28), drafted with the My Mitchell Story contest in campaigns/homeowners/contest.json.
- Reminder texts go only to people who RSVPed with text consent, from one Builder Studio workflow per event. Consultants tag anyone who RSVPs by reply with the event tag so the same workflow reaches them.
- Design Dollars: wherever named, it carries the $5,000 floor and the short fine print. Texts never name it. After October 31, pieces that name it (E4, E6) wait for Mitchell's November reserve-by date.
- Images: anything that could be boosted (social posts, Facebook events) uses real Mitchell homes or Design Centers with no people. Never show or describe the painted Home Portrait in any invitation. The one exception is E7, which names the My Mitchell Story finalist prize in words only (a framed painting of their Mitchell home) and never shows one.
- Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to the Instagram link listed for that post.
- Placeholders: [first name], [your name], [your phone], [city], [studio address], [time], [Facebook Live link], [YouTube Live link], [replay link], and for E7 [entry form link] and [official rules link]. Studio addresses are in the studio table.

## Where the events touch the existing cadence

- October 22: E1's invite email replaces the Design Dollars consultant email already set for that day (one consultant email per lead).
- November 5: E3's invite text replaces the landowner consultant text already set for that day.
- October 28: E2's follow-up stands in for the October 29 deadline text for anyone who received it.
- November 11: the E4 text skips E5 RSVPs, who get the E5 reminder that day, and active leads invited personally on November 9.
- dd2 carries two event blocks (E1, then E2's short line). E2 was placed in dd2, not dd3, for lead time.
- E6 rides rb2, the November 4 realtor email. rb3 (November 11) lands the same day as the consultant invites to agents; if Kelly wants, add one line to rb3 pointing to the Lunch and Learn, otherwise leave it. ra2 (November 18, after the event) already carries the lot checklist, so the E6 follow-up on November 19 does not repeat it.
- fb5 is on hold for the plan guide email. If it misses November 4, E3 rides fb1 and the consultant invites only.
- October 28: E7's invitation, ho2, goes to past homeowners on the Wednesday partner day (ra1 goes to realtors the same day). Consultants' personal homeowner invites run October 29 to November 3, ahead of E3's November 5 invites to active leads.
- November 10: E7 shares the day with fb2 (landowner email), E5's first post, Google post and invites, and E4's Nextdoor post. None of those go to the homeowner list, so a past homeowner hears about one thing that day.
- November 11: the E4 bulk text skips past Mitchell homeowners, who get the My Mitchell Story launch that morning (ho3, or their consultant's follow-up if they came to E7).
- build_cadence.py places events by a date map that lists e1 to e6 only. Until e7 is added there (event November 10, invites October 29, reminder November 9), the cadence shows E7's social posts but not the evening itself.

## The seven at a glance

| | Event | When | Where | Rides in |
|---|---|---|---|---|
| E1 | Bring Your Photos Saturday | Saturday, October 24, 2026, 10am to 2pm, local time at every studio | All five Design Centers | dd2 |
| E2 | Behind the Build Live: Your Design Dollars and SimplyMitchell Questions | Tuesday, October 27, 2026, 7pm Eastern, about 30 minutes | Online | dd2 |
| E3 | Building on Your Land 101 | Saturday, November 7, 2026, 10am to 11:30am | All five Design Centers | fb1, fb5 |
| E4 | Wilmington Design Center Open House | Saturday, November 14, 2026, 10am to 3pm | Wilmington (Belville) | no email (text, social, profile, Nextdoor, invites) |
| E5 | The Gathering Place Live: Building Your Getaway | Thursday, November 12, 2026, 7pm Eastern, 30 minutes | Online | hp4 |
| E6 | Realtor Lunch and Learn | Wednesday, November 18, 2026, 11:30am to 1pm | All five Design Centers | rb2 |
| E7 | Homeowner Appreciation Night | Tuesday, November 10, 2026, 5:30pm to 7:30pm, local time at every studio | All five Design Centers | its own homeowner email, ho2 |

## Every touch by date

| Date | Event | Channel | What | Who |
|---|---|---|---|---|
| Monday, October 19 | E1 | Social | Post 1 (Facebook, Instagram feed). Publish the five Facebook events. | Marketing |
| Monday, October 19 | E1 | Google | Event post on all five Design Center profiles | Marketing |
| Tuesday, October 20 | E1 | Email | Event block in dd2 | Marketing |
| Tuesday, October 20 | E1 | Nextdoor | Post from each Design Center page | Marketing |
| Tuesday, October 20 | E2 | Email | Second short line in dd2 | Marketing |
| Thursday, October 22 | E1 | Sales team | Personal invite text and email to own active leads (the email replaces that day's Design Dollars consultant email) | New Home Consultants |
| Thursday, October 22 | E2 | Social | Post 1, the question call (Facebook, Instagram feed). Publish the online Facebook event. | Marketing |
| Thursday, October 22 | E2 | Google | Event post on all five profiles (or Update if Google rejects an online event) | Marketing |
| Friday, October 23 | E1 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Friday, October 23 | E1 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Friday, October 23 | E2 | Sales team | Personal invite text and email to active leads not coming Saturday | New Home Consultants |
| Saturday, October 24 | E1 | Event | Bring Your Photos Saturday, 10am to 2pm; thank-you text by 6pm | Design Consultants, New Home Consultants |
| Sunday, October 25 | E1 | Sales team | Follow-up email with the priced list | New Home Consultants |
| Monday, October 26 | E2 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Tuesday, October 27 | E2 | Social | Post 2, tonight at 7 (Facebook, Instagram Stories) | Marketing |
| Tuesday, October 27 | E2 | Event | Live at 7pm Eastern; thank-you text after the show | Scott and Deven; consultants |
| Wednesday, October 28 | E2 | Sales team | Follow-up email with the replay and the October 31 date | New Home Consultants, online sales counselors |
| Wednesday, October 28 | E7 | Email | ho2, the invitation, to past homeowners (campaigns/homeowners/contest.json) | Marketing |
| Wednesday, October 28 | E7 | Social | Post 1 (Facebook, Instagram feed). Publish the five Facebook events. | Marketing |
| Wednesday, October 28 | E7 | Google | Event post on all five Design Center profiles | Marketing |
| Thursday, October 29 | E7 | Sales team | Personal invites to the homeowners each consultant built with, through Tuesday, November 3 | New Home Consultants |
| Monday, November 2 | E3 | Social | Post 1 (Facebook, Instagram feed). Publish the five Facebook events. | Marketing |
| Monday, November 2 | E3 | Google | Event post on all five profiles | Marketing |
| Tuesday, November 3 | E3 | Email | Event block in fb1 | Marketing |
| Tuesday, November 3 | E3 | Nextdoor | Post from each Design Center page | Marketing |
| Wednesday, November 4 | E3 | Email | Event block in fb5 and fb5c (if fb5 is released) | Marketing |
| Wednesday, November 4 | E6 | Email | Event block in the realtor email rb2 | Marketing |
| Wednesday, November 4 | E6 | Social | Post 1 (Facebook, Instagram feed, LinkedIn). Publish the five Facebook events. | Marketing |
| Wednesday, November 4 | E6 | Google | Event post on all five profiles | Marketing |
| Thursday, November 5 | E3 | Sales team | Personal invite text and email (the text replaces that day's landowner text) | New Home Consultants |
| Thursday, November 5 | E4 | Google | Event post on the Wilmington profile. Publish the Facebook event. | Marketing |
| Friday, November 6 | E3 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Friday, November 6 | E3 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Saturday, November 7 | E3 | Event | Class, 10am to 11:30am; thank-you text | Presenters, New Home Consultants |
| Sunday, November 8 | E3 | Sales team | Follow-up email with recap and next step | New Home Consultants |
| Monday, November 9 | E4 | Social | Post 1 (Facebook, Instagram feed) | Marketing |
| Monday, November 9 | E4 | Sales team | Personal invite text and email | Raleigh and Wilmington New Home Consultants |
| Monday, November 9 | E7 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Tuesday, November 10 | E4 | Nextdoor | Post from the Wilmington page | Marketing |
| Tuesday, November 10 | E5 | Social | Post 1 (Facebook, Instagram feed). Publish the online Facebook event. | Marketing |
| Tuesday, November 10 | E5 | Google | Event post on all five profiles (or Update) | Marketing |
| Tuesday, November 10 | E5 | Sales team | Personal invite text and email to lake, coast and mountain leads | New Home Consultants |
| Tuesday, November 10 | E7 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Tuesday, November 10 | E7 | Event | Homeowner Appreciation Night, 5:30pm to 7:30pm; My Mitchell Story entries open; thank-you text by 9pm | New Home Consultants, Design Consultants, photo session booker |
| Wednesday, November 11 | E4 | Text | The one bulk text to Carolinas contacts with text consent | Marketing |
| Wednesday, November 11 | E5 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Wednesday, November 11 | E6 | Sales team | Personal invite text and email to agents they know | New Home Consultants |
| Wednesday, November 11 | E7 | Sales team | Follow-up email to every homeowner who came (in place of ho3) | New Home Consultants |
| Wednesday, November 11 | E7 | Email | ho3, the My Mitchell Story launch, to past homeowners who did not come | Marketing |
| Thursday, November 12 | E5 | Email | Event block in hp4, tonight at 7 | Marketing |
| Thursday, November 12 | E5 | Social | Post 2, tonight at 7 (Facebook, Instagram Stories) | Marketing |
| Thursday, November 12 | E5 | Event | Live at 7pm Eastern; thank-you text after the show | Host; consultants |
| Friday, November 13 | E4 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Friday, November 13 | E4 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Friday, November 13 | E5 | Sales team | Follow-up email with the replay (and Saturday's open house for Carolinas contacts) | New Home Consultants, online sales counselors |
| Saturday, November 14 | E4 | Event | Open house, 10am to 3pm; thank-you text | Wilmington team |
| Sunday, November 15 | E4 | Sales team | Follow-up email | New Home Consultants |
| Monday, November 16 | E6 | Social | Post 2 (Facebook, Instagram Stories, LinkedIn) | Marketing |
| Tuesday, November 17 | E6 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Wednesday, November 18 | E6 | Event | Lunch and Learn, 11:30am to 1pm; thank-you text | New Home Consultants |
| Thursday, November 19 | E6 | Sales team | Follow-up email with the referral kit | New Home Consultants |

## Design Center addresses

As listed on the live Design Dollars page. Confirm before printing any address.

| Studio | Address | Phone in copy |
|---|---|---|
| Fredericksburg VA | 621 Warrenton Road, Fredericksburg, VA 22406 | (540) 701-2759 |
| Richmond VA (Midlothian) | 14300 Sommerville Court, Midlothian, VA 23113 | (540) 701-2759 (The live Design Dollars page lists (804) 538-3912 for this studio. Confirm which line Mitchell wants.) |
| Newport News VA | 663 Turnberry Boulevard, Suite E, Newport News, VA 23602 | (540) 701-2759 |
| Raleigh NC (studio in Garner) | 505 N. Greenfield Pkwy, Suite 120, Garner, NC 27529 | (984) 331-5468 |
| Wilmington NC (studio in Belville, open since September 11, 2026) | 42 Waterford Business Center Way, Suite A, Belville, NC 28451 | (984) 331-5468 |

---

## E1. Bring Your Photos Saturday

*Proposal until Mitchell approves the date and staffing.*

**When:** Saturday, October 24, 2026, 10am to 2pm, local time at every studio  
**Where:** All five Mitchell Design Centers: Fredericksburg VA, Richmond VA (Midlothian), Newport News VA, Raleigh NC (studio in Garner) and Wilmington NC (studio in Belville). Addresses in the studio table, as listed on the live Design Dollars page.  
**For:** Anyone planning a Mitchell home who has not signed yet, above all the buyers who have been saving photos of the home they want: active leads, Design Dollars email clickers and Home Portrait quiz takers. Walk-ins welcome; an RSVP gets a reserved time with a Design Consultant.

**What happens**

- Buyers bring the photos they have been saving, on their phone or in a folder.
- A Design Consultant matches the favorites to Mitchell selections and shows what they cost.
- Together they see where that list lands on the Design Dollars ladder, and how far it is to the next tier.

**Why it helps the campaign (for Kelly):** Turns the dd2 ladder email into a seat at the design table one week before the October 31 reserve-by date, with the buyer's own photos as the reason to come in.

**Mitchell must confirm**

- Approve the date and the 10am to 2pm hours, or name the studios that will take part.
- Staffing at every studio: a Design Consultant for the full four hours, plus a New Home Consultant for land and plan questions. Newport News and Wilmington each have one New Home Consultant; name the cover.
- Reserved times: CEA proposes 30-minute slots with walk-ins between them. Confirm the length and how many tables each studio can run at once.
- Pricing at the table: can a Design Consultant price a photo list on the spot? If not, copy changes to: we will send you the numbers.
- RSVP form (Kelly builds it in Builder Studio): name, phone, email, studio, preferred time, and the text consent checkbox with legal-approved wording.
- Food: none promised anywhere. If Mitchell wants coffee or light refreshments, add one line to the Facebook event.
- Studio addresses as listed on the live Design Dollars page, and which phone line Richmond shows.

**Notes for Kelly**

- October 22 already has a consultant email in the cadence (Design Dollars: personal email to active leads). Send this invite email in its place, not beside it: it carries the same ladder and makes the ask concrete, so each lead gets one consultant email that day.
- fb4 (November 19) also says bring your photos. This Saturday is the October version; fb4 stays as written.
- Never show the painted Home Portrait at the event table or in any of these pieces.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Monday, October 19 | Social | Post 1 (Facebook, Instagram feed). Publish the five Facebook events. | Marketing |
| Monday, October 19 | Google | Event post on all five Design Center profiles | Marketing |
| Tuesday, October 20 | Email | Event block in dd2 | Marketing |
| Tuesday, October 20 | Nextdoor | Post from each Design Center page | Marketing |
| Thursday, October 22 | Sales team | Personal invite text and email to own active leads (the email replaces that day's Design Dollars consultant email) | New Home Consultants |
| Friday, October 23 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Friday, October 23 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Saturday, October 24 | Event | Bring Your Photos Saturday, 10am to 2pm; thank-you text by 6pm | Design Consultants, New Home Consultants |
| Sunday, October 25 | Sales team | Follow-up email with the priced list | New Home Consultants |

### Email event block

**dd2**, Tuesday, October 20, 2026. Event block near the end, after the Find Your Tier button and before the footer. dd2 already carries the long fine print in its footer.

> **Bring Your Photos Saturday, October 24**
>
> Bring the photos you have been saving to any Mitchell Design Center between 10am and 2pm, and sit down with a Design Consultant who will show you what your favorites cost. You will also see where they land on the Design Dollars ladder, which starts at $5,000 on every home and grows up to $25,000 the more you personalize.
>
> [Save My Time]

Link: `[RSVP link]?utm_source=email&utm_medium=email&utm_campaign=fall26_events&utm_content=e1`

Fine print under the block: Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

### Social posts

**Monday, October 19, 2026** · Facebook, Instagram feed

> You have been saving photos of this house for years. The kitchen. The porch. The light over the table.
>
> Bring them in. On Saturday, October 24, from 10am to 2pm, every Mitchell Design Center is open for Bring Your Photos Saturday. Sit down with a Design Consultant, see what your favorites cost, and see where they land on the Design Dollars ladder. Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize.
>
> Fredericksburg, Richmond, Newport News, Raleigh and Wilmington. Walk-ins welcome. RSVP and we will save you a time: [RSVP link]
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.
>
> #BuildOnYourLand #MitchellHomes

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e1`  
Notes: Image: a Design Center finish wall or kitchen display, e.g. https://media.mitchellhomesinc.com/276/2023/2/6/Design_Center_13_IfaBRgj.jpg . Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category. Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e1 that morning.

**Friday, October 23, 2026** · Facebook, Instagram Stories

> Tomorrow, 10am to 2pm. Bring the photos you have been saving to your nearest Mitchell Design Center, and a Design Consultant will show you what your favorites cost.
>
> Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Reserve by October 31, 2026, and your Design Dollars are locked. Your tier is set later, when you make your selections.
>
> RSVP: [RSVP link]
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e1`  
Notes: Stories: use the link sticker with the Instagram link [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e1 . Fine print stays on the Story frame. Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category.

### Facebook event description

> Bring Your Photos Saturday at the Mitchell Homes [city] Design Center
> Saturday, October 24, 2026, 10am to 2pm
> [studio address]
>
> You know what you want. You have the photos to prove it. Bring them in.
>
> Sit down with a Mitchell Design Consultant, show us the kitchens, porches, tile and lighting you have been saving, and we will match them to Mitchell selections and show you what they cost. With more than 40,000 selections, most of what is in your folder is something we already carry.
>
> You will also see where your list lands on the Mitchell Design Dollars ladder. Every Mitchell home comes with $5,000 in Mitchell Design Dollars to spend on design selections. The more selections you buy, the more Mitchell adds, up to $25,000. Reserve by October 31, 2026, and your Design Dollars are locked. Your tier is set later, when you make your selections.
>
> Walk-ins are welcome. RSVP and we will save you a time with a Design Consultant: [RSVP link]
>
> Questions? Call a New Home Consultant: Virginia and Maryland (540) 701-2759, North and South Carolina (984) 331-5468.
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. One offer per contract.

Notes: One Facebook event per Design Center, so each shows a real address to people nearby; only [city] and [studio address] change. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e1 . Cover image: no people.

### Google Business Profile event post

Post on: All five Design Center profiles, Monday, October 19. Event-type post, start Saturday, October 24, 10am, end 2pm.

**Title:** Bring Your Photos Saturday (26 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e1`

> Bring the photos you have been saving for your future home to our [city] Design Center. A Design Consultant will match your favorites to Mitchell selections, show you what they cost, and show you where they land on the Design Dollars ladder. Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Walk-ins welcome, or tap Sign up to save a time.
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Notes: Title holds 58 characters. Image: that studio's interior, no people. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Tuesday, October 20, 2026, from each Design Center's Nextdoor business page where one exists.

> Saving photos of the home you want to build? Bring them in.
>
> On Saturday, October 24, from 10am to 2pm, the Mitchell Homes [city] Design Center at [studio address] is open for Bring Your Photos Saturday. Sit down with a Design Consultant, see what your favorites cost, and see where they land on the Design Dollars ladder. Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize.
>
> Walk-ins welcome. RSVP for a reserved time: [RSVP link]?utm_source=nextdoor&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e1
>
> Mitchell Homes, building on your land since 1992.
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

### Consultant personal invite

Thursday, October 22, 2026. Every New Home Consultant to their own active leads.

**Text** (252 characters)

> Hi [first name], it is [your name] with Mitchell Homes. This Saturday, Oct 24, from 10 to 2, bring the home photos you have been saving to our [city] Design Center. A Design Consultant will show you what your favorites cost. Want me to save you a time?

**Email** · Subject: Bring your photos Saturday

```text
Hi [first name],

If you have been saving photos of the home you want, this Saturday is a good day to bring them in.

On Saturday, October 24, from 10am to 2pm, our [city] Design Center is open for Bring Your Photos Saturday. Sit down with one of our Design Consultants, show us what you have been saving, and we will match it to Mitchell selections and show you what it costs.

You will also see where your list lands on the Design Dollars ladder. Every Mitchell home comes with $5,000 in Mitchell Design Dollars to spend on design selections. The more selections you buy, the more Mitchell adds, up to $25,000. Choose $60,000 in selections, for example, and Mitchell adds $15,000, so you take home $75,000 worth. Sign now, and your incentive is locked, but your tier will be decided when you make your selections. Reserve by October 31.

Reply with a time that works and I will hold it for you, or just come by.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.
```

### RSVP reminder text

Friday, October 23, 2026. Builder Studio workflow on the RSVP form, to RSVPs with text consent only.

> Mitchell Homes: See you tomorrow at [time] at our [city] Design Center, [studio address]. Bring the photos you have been saving. Need a new time? Reply here. Reply STOP to opt out

(179 characters)

### Same-day thank-you text

Saturday, October 24, 2026, by 6pm. The Design Consultant or New Home Consultant each attendee met.

> Thank you for coming in today, [first name]. It was great to see the home you have been picturing. I will send your priced list tomorrow so you have it all in one place. Questions before then? Just text me.

### Next-day follow-up email

Sunday, October 25, 2026 (schedule it Saturday evening). The New Home Consultant, from their own address.

Subject: Your photos, priced

```text
Hi [first name],

Thank you for bringing your photos in yesterday. It was good to see the home you have been picturing, and [one thing they loved, in their words] belongs in it.

Here is what we priced together:
[selection list with prices, from the Design Consultant]

On the Design Dollars ladder, that list puts you at [tier]. You are [amount] away from the next tier, which adds [amount] more for your selections. Every Mitchell home starts with $5,000 in Mitchell Design Dollars, up to $25,000 the more you personalize. See the full ladder: https://simplymitchellhomes.com/design-dollars?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e1

Reserve by Saturday, October 31, and your Design Dollars are locked. Your tier is set later, when you make your selections, and your reservation deposit is $150, which is all Mitchell receives until closing.

One more thing: on Tuesday at 7pm Eastern, Scott Sleeme and Deven Sellers are answering Design Dollars and SimplyMitchell questions live on Facebook and YouTube. If you have a question, send it to me and I will pass it along.

Want to pick a plan to go with your list? Reply with a time this week.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.
```


---

## E2. Behind the Build Live: Your Design Dollars and SimplyMitchell Questions

*Proposal until Mitchell approves the date and staffing.*

**When:** Tuesday, October 27, 2026, 7pm Eastern, about 30 minutes  
**Where:** Online: live on the Mitchell Homes Facebook page and YouTube channel at the same time. No studio needed.  
**For:** Everyone still deciding before the October 31 reserve-by date: active leads, Design Dollars email clickers, quiz takers, and anyone curious how SimplyMitchell works. Agents and past homeowners welcome.

**What happens**

- Scott Sleeme and Deven Sellers explain Mitchell Design Dollars in plain terms: $5,000 on every home, up to $25,000 the more you personalize, and what it covers.
- They answer questions sent in ahead and asked live, including how SimplyMitchell works: zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.
- The recording stays on both channels, and each answer becomes its own short clip.

**Why it helps the campaign (for Kelly):** Answers the two questions that stall a Design Dollars decision (what does it cover, do I have to choose now) four days before the October 31 reserve-by date, in Scott's own voice.

**Mitchell must confirm**

- Scott and Deven's time: Tuesday, October 27, about 6:30pm to 7:45pm Eastern for setup, the live half hour and a short wrap.
- Streaming: one tool that sends to Facebook and YouTube at once, a camera and microphone, and who runs it (Brittany or CEA). If the YouTube channel has never streamed, enable live streaming at least a day ahead; first-time approval can take up to 24 hours.
- Questions: a question field on the RSVP form, comments on the October 22 post, and consultant replies. Name who screens them before the show and who answers comments live.
- On screen: the Design Dollars fine print and the financing line. Answers stay inside the approved wording (Scott's two sentences; Every choice priced before we build; no build duration; no claim that the price cannot change).
- Who posts the replay and cuts the clips.
- RSVP form (Kelly): name, email, phone, text consent, your question.

**Notes for Kelly**

- For a consultant's own active leads, this follow-up stands in for the October 29 deadline text in the cadence; skip that text for anyone who got this email.
- Clips: one question per Short, titled with the question, per the YouTube plan.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Tuesday, October 20 | Email | Second short line in dd2 | Marketing |
| Thursday, October 22 | Social | Post 1, the question call (Facebook, Instagram feed). Publish the online Facebook event. | Marketing |
| Thursday, October 22 | Google | Event post on all five profiles (or Update if Google rejects an online event) | Marketing |
| Friday, October 23 | Sales team | Personal invite text and email to active leads not coming Saturday | New Home Consultants |
| Monday, October 26 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Tuesday, October 27 | Social | Post 2, tonight at 7 (Facebook, Instagram Stories) | Marketing |
| Tuesday, October 27 | Event | Live at 7pm Eastern; thank-you text after the show | Scott and Deven; consultants |
| Wednesday, October 28 | Sales team | Follow-up email with the replay and the October 31 date | New Home Consultants, online sales counselors |

### Email event block

**dd2**, Tuesday, October 20, 2026. Second short line in dd2, directly under the Bring Your Photos block. Chosen over dd3 because questions have to arrive before the show and the day-before reminder only reaches people who RSVPed, so the invitation needs a week of lead time. dd3 keeps its one job: booking a Design Center visit before October 31.

> **Ask Scott and Deven, live**
>
> On Tuesday, October 27, at 7pm Eastern, Scott Sleeme and Deven Sellers go live on Facebook and YouTube for about 30 minutes to answer your questions about SimplyMitchell and Design Dollars, from the $5,000 every home starts with to the $25,000 top tier. Send yours ahead of time, and they will answer as many as they can.
>
> [Send a Question]

Link: `[RSVP link]?utm_source=email&utm_medium=email&utm_campaign=fall26_events&utm_content=e2`

Fine print under the block: Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

### Social posts

**Thursday, October 22, 2026** · Facebook, Instagram feed

> Building a home on your land comes with questions. Ask the people who build them.
>
> On Tuesday, October 27, at 7pm Eastern, Scott Sleeme and Deven Sellers from Behind the Build go live on Facebook and YouTube to answer your questions about Mitchell Design Dollars and SimplyMitchell. What Design Dollars cover. When you choose. How building on your land works with zero down, zero closing costs and no construction loan.
>
> Leave your question in the comments, or send it here and we will remind you before we go live: [RSVP link]
>
> Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e2`  
Notes: Image: the Behind the Build title card or Scott and Deven at the microphones (hosts, not a family photo, so it can be boosted). Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e2 that morning.

**Tuesday, October 27, 2026** · Facebook, Instagram Stories

> Tonight at 7pm Eastern, Scott Sleeme and Deven Sellers go live to answer your questions about Mitchell Design Dollars and SimplyMitchell. About 30 minutes. Watch on our Facebook page or YouTube channel, and ask in the comments.
>
> Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Reserve by October 31, 2026.
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Link: `[YouTube Live link]`  
Notes: Stories: link sticker to the YouTube Live link. Post the morning of the show.

### Facebook event description

> Behind the Build Live: Your Design Dollars and SimplyMitchell Questions
> Tuesday, October 27, 2026, 7pm Eastern, about 30 minutes
> Online: live here on Facebook and on the Mitchell Homes YouTube channel
>
> Building a home on your land comes with questions. Bring yours to the people who answer them every day.
>
> Scott Sleeme, Owner and CEO of Mitchell Homes, and Deven Sellers, Executive Vice President, host Behind the Build. For one live half hour, they answer your questions about:
>
> Mitchell Design Dollars. Every Mitchell home comes with $5,000 in Mitchell Design Dollars to spend on design selections. The more selections you buy, the more Mitchell adds, up to $25,000. What they cover, and why you do not have to choose a single finish to lock them in.
>
> SimplyMitchell. Zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.
>
> Send your question ahead of time and we will remind you before we go live: [RSVP link] . Or ask in the comments during the show.
>
> Reserve by October 31, 2026, and your Design Dollars are locked. Your tier is set later, when you make your selections.
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

Notes: One online Facebook event with Facebook Live as the location. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e2 . Publish Thursday, October 22.

### Google Business Profile event post

Post on: All five Design Center profiles, Thursday, October 22. Event-type post, start October 27, 7pm, end 7:30pm.

**Title:** Behind the Build Live: Design Dollars Q&A (41 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e2`

> Building on your land comes with questions. On Tuesday, October 27, at 7pm Eastern, Scott Sleeme and Deven Sellers go live on the Mitchell Homes Facebook page and YouTube channel to answer yours about Mitchell Design Dollars and SimplyMitchell. About 30 minutes. Tap Sign up to send a question and get a reminder.
>
> Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Notes: The event is online. If Google rejects an online event on a studio profile, post it as an Update instead or skip it. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Skip: online event, not local.

### Consultant personal invite

Friday, October 23, 2026. Every New Home Consultant to active leads who are not coming Saturday (Saturday's guests hear about it in person and in Sunday's follow-up), so nobody gets two invitations in one day.

**Text** (267 characters)

> Hi [first name], [your name] with Mitchell Homes. Tuesday at 7pm Eastern, Scott and Deven are live on Facebook and YouTube for 30 minutes answering questions about building on your land with Mitchell. Got one you want answered? Text it to me and I will pass it along.

**Email** · Subject: Your question, answered live by Scott and Deven

```text
Hi [first name],

If you have a question about building with Mitchell that you have not asked yet, here is a good place to ask it.

On Tuesday, October 27, at 7pm Eastern, Scott Sleeme, our Owner and CEO, and Deven Sellers, our Executive Vice President, are going live on Facebook and YouTube for about 30 minutes to answer questions about Mitchell Design Dollars and SimplyMitchell.

A quick refresher on both. Your home comes with $5,000 in Design Dollars, and it goes up to $25,000 the more you personalize. Sign now, and your incentive is locked, but your tier will be decided when you make your selections. And with SimplyMitchell, building on land you own means zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.

Reply with your question and I will make sure it gets to them. Here is where to watch: [Facebook Live link] or [YouTube Live link].

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.
```

### RSVP reminder text

Monday, October 26, 2026. Builder Studio workflow, RSVPs with text consent only.

> Mitchell Homes: Tomorrow at 7pm Eastern, Scott and Deven go live to answer your questions. About 30 minutes. Watch: [YouTube Live link] Reply STOP to opt out

(157 characters)

### Same-day thank-you text

Tuesday, October 27, 2026, right after the show. Each consultant to their own leads who RSVPed; online sales counselors to the rest.

> Thank you for joining Scott and Deven tonight, [first name]. If you missed it or want to watch again, the replay is here: [replay link]. Anything they did not get to, text me and I will answer it myself.

### Next-day follow-up email

Wednesday, October 28, 2026. The consultant (or an online sales counselor), to every RSVP.

Subject: The answers from last night, and October 31

```text
Hi [first name],

Thank you for tuning in to Behind the Build Live last night. If you missed any of it, the full replay is here: [YouTube replay link]

The two questions we heard most: [question one, answered in a sentence] and [question two, answered in a sentence].

If you are planning to build, this is the week that matters. Reserve by Saturday, October 31, and your Design Dollars are locked: $5,000 on every Mitchell home, up to $25,000 the more you personalize. Your tier is set later, when you make your selections, and your reservation deposit is $150, which is all Mitchell receives until closing.

See the full ladder: https://simplymitchellhomes.com/design-dollars?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e2

Want to talk it through before Saturday? Reply with a time, or call me at the number below.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.
```


---

## E3. Building on Your Land 101

*Proposal until Mitchell approves the date and staffing.*

**When:** Saturday, November 7, 2026, 10am to 11:30am  
**Where:** All five Mitchell Design Centers: Fredericksburg VA, Richmond VA (Midlothian), Newport News VA, Raleigh NC (studio in Garner) and Wilmington NC (studio in Belville). Addresses in the studio table, as listed on the live Design Dollars page. A free fall edition of the Homebuyer Roadmap to Success class.  
**For:** People who own land, have family land, or are shopping for land to build on: the landowner and looking for land segments, quiz takers who answered either way, and anyone who clicked a Four Buyers email or page.

**What happens**

- A one-hour class on what to know before you build: perc tests and soil, wells and septic, road access and utilities.
- How the money works: SimplyMitchell on land you own (zero down, zero closing costs, no construction loan), and what to plan for if you are still buying.
- Thirty minutes of open questions, then time with a New Home Consultant for anyone who brings a parcel address, survey or plat.

**Why it helps the campaign (for Kelly):** Puts the Four Buyers argument (your land is worth more than you think) in a room with a New Home Consultant the week fb1 and fb5 land, using a class format Mitchell already runs.

**Mitchell must confirm**

- Approve the date and which studios host; seats per studio (room, chairs, a screen).
- Presenter at each studio: a New Home Consultant, plus someone who can speak to perc tests, wells, septic and site work.
- The class deck: CEA can draft it from the Homebuyer Roadmap to Success, Well and Septic and Purchasing Land 101 episodes for Mitchell to approve.
- SimplyMitchell for buyers still purchasing land: confirm whether the terms are the same before the class answers that question (open flag on the No Land page).
- Food: none promised. If Mitchell wants coffee, add one line to the Facebook event and the invite email.
- RSVP form (Kelly): name, phone, email, studio, own land or still looking, county (optional), text consent.

**Notes for Kelly**

- November 5 already has a consultant text to landowner leads in the cadence. For those leads, this invite text replaces it, so nobody gets two texts that day.
- /land covers Virginia and Southern Maryland only; Carolinas attendees get /onyourland. Use /no-land only once its plan guide email is fixed.
- Fair housing: presenters and posts never recommend a county or describe an area as desirable.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Monday, November 2 | Social | Post 1 (Facebook, Instagram feed). Publish the five Facebook events. | Marketing |
| Monday, November 2 | Google | Event post on all five profiles | Marketing |
| Tuesday, November 3 | Email | Event block in fb1 | Marketing |
| Tuesday, November 3 | Nextdoor | Post from each Design Center page | Marketing |
| Wednesday, November 4 | Email | Event block in fb5 and fb5c (if fb5 is released) | Marketing |
| Thursday, November 5 | Sales team | Personal invite text and email (the text replaces that day's landowner text) | New Home Consultants |
| Friday, November 6 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Friday, November 6 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Saturday, November 7 | Event | Class, 10am to 11:30am; thank-you text | Presenters, New Home Consultants |
| Sunday, November 8 | Sales team | Follow-up email with recap and next step | New Home Consultants |

### Email event block

**fb1**, Tuesday, November 3, 2026. Event block near the end, after the Downey quote and before the Design Dollars band.

> **Building on Your Land 101, Saturday, November 7**
>
> Before a home goes on your land, a few things decide the plan: perc tests and soil, well and septic, road access and utilities, and how the money works. Spend 90 minutes with us at your nearest Mitchell Design Center, from 10am to 11:30am, and leave with a clear list of what to check on your land next.
>
> [Save My Seat]

Link: `[RSVP link]?utm_source=email&utm_medium=email&utm_campaign=fall26_events&utm_content=e3`

**fb5**, Wednesday, November 4, 2026 (and fb5c for the Carolinas). Event block after the floor plans line, before the Design Dollars band. fb5 is on hold until the plan guide email is built; if it slips past November 6, this block moves to the consultant invites only.

> **Shopping for land? Start with this class.**
>
> On Saturday, November 7, from 10am to 11:30am, every Mitchell Design Center is hosting Building on Your Land 101: what to check before you buy, from perc tests and soil to well, septic, access and utilities. It is free, and you do not need to own land yet to come.
>
> [Save My Seat]

Link: `[RSVP link]?utm_source=email&utm_medium=email&utm_campaign=fall26_events&utm_content=e3`

### Social posts

**Monday, November 2, 2026** · Facebook, Instagram feed

> Land is silent until you give it a voice. Before it can carry a home, a few questions need answers.
>
> Will the soil perc? Where does the well go? Can a driveway and power reach the homesite? How does the money work when the land is already yours?
>
> Building on Your Land 101 is a free class at every Mitchell Design Center on Saturday, November 7, from 10am to 11:30am. Bring your parcel address and your questions. Still looking for land? Come anyway. This is the class to take before you buy.
>
> Save a seat: [RSVP link]
>
> #BuildOnYourLand #MitchellHomes

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e3`  
Notes: Image: a Mitchell home alone on open land, e.g. https://media.mitchellhomesinc.com/276/2024/7/5/1_GuQrrFW.jpg . Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category. Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e3 that morning.

**Friday, November 6, 2026** · Facebook, Instagram Stories

> Tomorrow morning, 10am to 11:30am: Building on Your Land 101 at every Mitchell Design Center. Perc tests and soil, wells and septic, access and utilities, and how the money works with SimplyMitchell. Free. RSVP so we have a seat ready for you: [RSVP link]

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e3`  
Notes: Stories: link sticker with [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e3 . Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category.

### Facebook event description

> Building on Your Land 101 at the Mitchell Homes [city] Design Center
> Saturday, November 7, 2026, 10am to 11:30am
> [studio address]
>
> Owning land is the hardest part of building a custom home, and the most misunderstood. This free 90-minute class is the fall edition of Mitchell's Homebuyer Roadmap to Success, built around the questions landowners ask us first:
>
> Perc tests and soil: what they tell you about your homesite.
> Wells and septic: what your land needs, and how it shapes the plan.
> Access and utilities: driveways, power and water, and where the home can sit.
> The money: how SimplyMitchell works on land you own, with zero down, zero closing costs and no construction loan, because Mitchell self-funds every build, and what to plan for if you are still buying.
>
> Bring your parcel address, a survey or plat if you have one, and your questions. Stay after for time with a New Home Consultant.
>
> Still looking for land? You are welcome too. This is the class to take before you buy.
>
> RSVP: [RSVP link]
>
> Cannot make it? Watch Behind the Build: Well and Septic https://www.youtube.com/watch?v=zWwtw8qgp4w and Purchasing Land 101 https://www.youtube.com/watch?v=trgJ8maymOA
>
> Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

Notes: One Facebook event per Design Center; only [city] and [studio address] change. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e3 . Cover image: land or a finished home, no people.

### Google Business Profile event post

Post on: All five Design Center profiles, Monday, November 2. Event-type post, start November 7, 10am, end 11:30am.

**Title:** Building on Your Land 101: Free Class (37 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e3`

> Own land, or shopping for it? Join us at our [city] Design Center on Saturday, November 7, from 10am to 11:30am for Building on Your Land 101, a free class on what to know before you build: perc tests and soil, wells and septic, access and utilities, and how the money works with SimplyMitchell. Bring your parcel address and your questions. Tap Sign up to save a seat.

Notes: Image: land or a finished Mitchell home, no people. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Tuesday, November 3, 2026, from each Design Center's Nextdoor business page. Fair housing: never name a county or call an area a good place to live.

> Own land, or thinking about buying some to build on?
>
> Mitchell Homes is hosting a free class, Building on Your Land 101, at our [city] Design Center ([studio address]) on Saturday, November 7, from 10am to 11:30am. We will cover perc tests and soil, wells and septic, access and utilities, and how the money works.
>
> Bring your parcel address and your questions. RSVP: [RSVP link]?utm_source=nextdoor&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e3
>
> Mitchell Homes, building on your land since 1992.

### Consultant personal invite

Thursday, November 5, 2026. Every New Home Consultant to their own active leads who own land or are looking for it.

**Text** (261 characters)

> Hi [first name], [your name] with Mitchell Homes. This Saturday, Nov 7, 10 to 11:30, we are holding a free class at our [city] Design Center on building on your land: perc, well and septic, access and the money. Bring your parcel address. Can I save you a seat?

**Email** · Subject: Saturday morning: Building on Your Land 101

```text
Hi [first name],

When we talk about your land, the same questions come up every time. Will it perc? Where does the well go? Can we get a driveway and power to the homesite? How does the money work?

This Saturday, November 7, from 10am to 11:30am, we are answering all of them in one free class at our [city] Design Center: Building on Your Land 101. Bring your parcel address, and a survey or plat if you have one, and stay after so we can look at your land together.

If you are still looking for land, come anyway. It is the class I wish every buyer took before they bought.

Reply and I will save you a seat.

[your name]
New Home Consultant, Mitchell Homes
[your phone]
```

### RSVP reminder text

Friday, November 6, 2026. Builder Studio workflow, RSVPs with text consent only.

> Mitchell Homes: See you tomorrow, Sat Nov 7, 10 to 11:30am, for Building on Your Land 101 at our [city] Design Center, [studio address]. Bring your parcel address. Reply STOP to opt out

(185 characters)

### Same-day thank-you text

Saturday, November 7, 2026, by early afternoon. The New Home Consultant who met each attendee.

> Thank you for coming this morning, [first name]. If a question about your land comes up this weekend, text me. I will send the class notes tomorrow with the next step for your land.

### Next-day follow-up email

Sunday, November 8, 2026 (schedule it Saturday). The New Home Consultant.

Subject: Your land, next steps

```text
Hi [first name],

Thank you for joining Building on Your Land 101 yesterday. Here is a short recap, and the next step for you.

What to gather: your parcel address, any survey or plat, and anything you have on the soil, perc or well.
What to check: soil and perc, well and septic, road access and utilities.
How the money works: on land you own, SimplyMitchell means zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.

Your next step: [a land walk at your property, or a Design Center visit to walk the plans]. Reply with two times that work and I will set it up.

Two Behind the Build episodes worth watching this week:
Well and Septic: https://www.youtube.com/watch?v=zWwtw8qgp4w
Purchasing Land 101: https://www.youtube.com/watch?v=trgJ8maymOA

See what your land can build: https://simplymitchellhomes.com/land?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e3
[Carolinas: https://simplymitchellhomes.com/onyourland?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e3 . Still looking for land: https://simplymitchellhomes.com/no-land?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e3 , or /no-land-carolinas.]

Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

[your name]
New Home Consultant, Mitchell Homes
[your phone]
```


---

## E4. Wilmington Design Center Open House

*Proposal until Mitchell approves the date and staffing.*

**When:** Saturday, November 14, 2026, 10am to 3pm  
**Where:** Mitchell Homes Wilmington Design Center, 42 Waterford Business Center Way, Suite A, Belville, NC 28451 (address as listed on the live Design Dollars page).  
**For:** North and South Carolina contacts, led by the Wilmington division: coastal North Carolina and Dillon, Horry, Marion and Marlboro counties in South Carolina. Landowners, buyers still looking for land, Carolinas quiz takers and active leads.

**What happens**

- Walk the Wilmington Design Center: cabinets, countertops, flooring, tile, lighting and hardware in person.
- Sit with a New Home Consultant about your land, more than 40 floor plans, and how SimplyMitchell works: zero down, zero closing costs, no construction loan.
- See the Design Dollars ladder with a Design Consultant: $5,000 on every home, up to $25,000 the more you personalize.

**Why it helps the campaign (for Kelly):** Gives the Carolinas launch of the Four Buyers campaign a physical place to land, and introduces the coast and the four South Carolina counties to the studio that opened September 11.

**Mitchell must confirm**

- Approve the date and 10am to 3pm hours. Wilmington has one New Home Consultant; name who joins (a Design Consultant, the New Home Sales Associate, or a Raleigh consultant).
- Design Dollars after October 31: the Facebook event and follow-up name the offer without a reserve-by date. Approve the November date (Kelly recommends November 30) by November 9, or CEA removes the Design Dollars lines from every E4 piece.
- The one text on Wednesday, November 11: confirm the audience. The brief says all Carolinas contacts with text consent; Mitchell may prefer to limit it to the Wilmington division, since Belville is a long drive from the Triangle.
- Refreshments or a giveaway: none promised. If Mitchell wants either, add one line to the Facebook event and the Nextdoor post.
- Parking and door signage for Suite A.
- RSVP form (Kelly), optional for a drop-in event: name, phone, email, own land or still looking, county, text consent.

**Notes for Kelly**

- South Carolina is served from the Wilmington Design Center; keep the two geography claims separate in any added copy.
- The Cuomo video is cleared for organic and email; quote them only word for word from the live pages.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Thursday, November 5 | Google | Event post on the Wilmington profile. Publish the Facebook event. | Marketing |
| Monday, November 9 | Social | Post 1 (Facebook, Instagram feed) | Marketing |
| Monday, November 9 | Sales team | Personal invite text and email | Raleigh and Wilmington New Home Consultants |
| Tuesday, November 10 | Nextdoor | Post from the Wilmington page | Marketing |
| Wednesday, November 11 | Text | The one bulk text to Carolinas contacts with text consent | Marketing |
| Friday, November 13 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Friday, November 13 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Saturday, November 14 | Event | Open house, 10am to 3pm; thank-you text | Wilmington team |
| Sunday, November 15 | Sales team | Follow-up email | New Home Consultants |

### Email event block

No email block, as briefed. The Wilmington profile, social, Nextdoor, consultant invites and one text carry it.
### Social posts

**Monday, November 9, 2026** · Facebook, Instagram feed

> Building on your land near the coast? Come see where it starts.
>
> Our Wilmington Design Center in Belville is hosting an open house on Saturday, November 14, from 10am to 3pm. Walk the cabinets, counters, tile and lighting in person, look through more than 40 floor plans, and sit down with a New Home Consultant about your land.
>
> Own land in coastal North Carolina or in Dillon, Horry, Marion or Marlboro County, South Carolina? Ask how SimplyMitchell works: zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.
>
> Drop in any time, or RSVP and we will have a time ready for you: [RSVP link]
>
> #BuildOnYourLand #MitchellHomes #WilmingtonNC

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e4`  
Notes: Image: the Wilmington Design Center interior (Brittany's photos), no people. Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category. Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e4 that morning.

**Friday, November 13, 2026** · Facebook, Instagram Stories

> Tomorrow, 10am to 3pm: open house at the Mitchell Homes Wilmington Design Center, 42 Waterford Business Center Way, Suite A, Belville, NC 28451. Bring your land questions, your saved photos and your plans. Drop in any time: [RSVP link]

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e4`  
Notes: Stories: link sticker with [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e4 , plus a map sticker on the studio. Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category.

### Facebook event description

> Open House at the Mitchell Homes Wilmington Design Center
> Saturday, November 14, 2026, 10am to 3pm
> 42 Waterford Business Center Way, Suite A, Belville, NC 28451
>
> If you have been picturing a home on land you own, or land you are still looking for, this is the place to start.
>
> Drop in any time between 10 and 3 to:
> Walk the Design Center and see cabinets, countertops, flooring, tile, lighting and hardware in person.
> Look through more than 40 floor plans, from 1,000 to 3,000 square feet.
> Sit down with a New Home Consultant about your land and how SimplyMitchell works: zero down, zero closing costs and no construction loan, because Mitchell self-funds every build.
> See the Mitchell Design Dollars ladder with a Design Consultant. Every Mitchell home comes with $5,000 in Mitchell Design Dollars to spend on design selections. The more selections you buy, the more Mitchell adds, up to $25,000. [Reserve by date, once Mitchell approves the November date.]
>
> The Wilmington Design Center serves coastal North Carolina and Dillon, Horry, Marion and Marlboro counties in South Carolina.
>
> RSVP (optional): [RSVP link] . Questions? Call a New Home Consultant at (984) 331-5468.
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. One offer per contract. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

Notes: One event, Wilmington address. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e4 . Publish Thursday, November 5. If the November Design Dollars date is not approved by November 9, delete the Design Dollars sentence, the bracket and the Design Dollars fine print.

### Google Business Profile event post

Post on: Wilmington NC profile only, Thursday, November 5. Event-type post, start November 14, 10am, end 3pm.

**Title:** Open House at our Wilmington Design Center (42 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e4`

> Join us Saturday, November 14, from 10am to 3pm, for an open house at our Wilmington Design Center in Belville. Walk the finishes in person, look through more than 40 floor plans, and sit down with a New Home Consultant about building on your land. Ask how SimplyMitchell works: zero down, zero closing costs and no construction loan. Drop in any time, or tap Sign up to RSVP.

Notes: Image: the studio interior, no people. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Tuesday, November 10, 2026, from the Wilmington Design Center's Nextdoor business page.

> Thinking about building a home on land you own, or land you are still looking for?
>
> Mitchell Homes is hosting an open house at our Wilmington Design Center, 42 Waterford Business Center Way, Suite A, in Belville, on Saturday, November 14, from 10am to 3pm. Walk the finishes in person, look through more than 40 floor plans, and bring your land questions to a New Home Consultant.
>
> Drop in any time. RSVP if you would like a time set aside: [RSVP link]?utm_source=nextdoor&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e4
>
> Mitchell Homes, building on your land since 1992.

### Consultant personal invite

Monday, November 9, 2026. Raleigh and Wilmington New Home Consultants to their own active leads.

**Text** (245 characters)

> Hi [first name], [your name] with Mitchell Homes. We are hosting an open house at our Wilmington Design Center in Belville this Saturday, Nov 14, 10 to 3. Come walk the finishes and bring your land questions. Want me to set aside a time for you?

**Email** · Subject: Open house Saturday in Belville

```text
Hi [first name],

If you have been thinking about the home you want to build, this Saturday is an easy way to take the next step.

On Saturday, November 14, from 10am to 3pm, we are hosting an open house at our Wilmington Design Center, 42 Waterford Business Center Way, Suite A, in Belville. You can walk the cabinets, counters, tile and lighting in person, look through more than 40 floor plans, and bring your land questions to a New Home Consultant.

If you own land, ask about SimplyMitchell: zero down, zero closing costs and no construction loan, because Mitchell self-funds every build. If you are still looking, you can start designing now and bring us the lot when you find it.

Drop in any time, or reply and I will set aside a time for you.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.
```

### RSVP reminder text

Friday, November 13, 2026. Builder Studio workflow, RSVPs with text consent only.

> Mitchell Homes: See you tomorrow, Sat Nov 14, 10am to 3pm, at our Wilmington Design Center, 42 Waterford Business Center Way, Suite A, Belville. Reply STOP to opt out

(166 characters)

### Same-day thank-you text

Saturday, November 14, 2026, by 6pm. Whoever each guest met.

> Thank you for coming by the Wilmington Design Center today, [first name]. I enjoyed hearing about [their land or plan]. I will follow up tomorrow with the plans and numbers we talked about. Text me any time.

### Next-day follow-up email

Sunday, November 15, 2026 (schedule it Saturday). The New Home Consultant.

Subject: From Saturday at the Wilmington Design Center

```text
Hi [first name],

Thank you for coming to the open house yesterday. It was good to talk about [their land, plan or favorite finish].

As promised, here is what we talked about:
[plans that fit, with links]
[selections they liked, priced if they asked]

A few things worth having in one place. With SimplyMitchell, building on land you own means zero down, zero closing costs and no construction loan, because Mitchell self-funds every build. See how it works: https://simplymitchellhomes.com/onyourland?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e4

Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. [Reserve by date, once Mitchell approves the November date.]

If you would like to see a Mitchell home on the coast first, Rob and Kat Cuomo built theirs in Wilmington: https://www.youtube.com/watch?v=jMSBzlcQ4uU

Ready for the next step? Reply with a time for a land walk or a second visit.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.
```

### Extra text

**Wednesday, November 11, 2026** · North and South Carolina contacts with text consent, minus anyone who already RSVPed, anyone under contract, past Mitchell homeowners (My Mitchell Story opens for them that day), active leads their consultant invited on November 9, and E5 RSVPs (they get the E5 reminder that day). The only bulk text that week.

> Mitchell Homes: Open house Sat Nov 14, 10 to 3, Wilmington Design Center, Belville. Bring your land questions. [trigger link] Reply STOP to opt out

150 of 160 characters with a short trigger link. Link: `[RSVP link]?utm_source=sms&utm_medium=sms&utm_campaign=fall26_events&utm_content=e4`. Builder Studio bulk SMS between 10am and 7pm. Make the link a Builder Studio trigger link to the tracked RSVP URL so it stays short.


---

## E5. The Gathering Place Live: Building Your Getaway

*Proposal until Mitchell approves the date and staffing.*

**When:** Thursday, November 12, 2026, 7pm Eastern, 30 minutes  
**Where:** Online: live on the Mitchell Homes Facebook page and YouTube channel, the same setup as Behind the Build Live.  
**For:** People planning a getaway, a family retreat, a second home or the place they will retire, at the lake, on the coast or in the mountains: quiz takers who chose Smith Mountain Lake, Lake Gaston, the Shenandoah Valley or the Eastern Shore and Outer Banks, contacts interested in those areas, and past homeowners thinking about a second place.

**What happens**

- A 30-minute live conversation about building a getaway, second home or retirement home at the lake, on the coast or in the mountains.
- What to look at first on a lake, coastal or mountain lot, and how building works when you live hours away, with weekly communication from groundbreaking to move-in.
- Why second homes are where banks get strict, and how SimplyMitchell answers it: no construction loan, because Mitchell self-funds every build. Live questions throughout.

**Why it helps the campaign (for Kelly):** Gives retreat and retirement buyers, the audience for The Gathering Place Portrait, a reason to talk to Mitchell the same night hp4 lands, and answers their biggest objection, second-home financing, out loud.

**Mitchell must confirm**

- Host: Scott and Deven, or a New Home Consultant who builds at the lake and on the coast. Thursday, November 12, about 6:30pm to 7:45pm Eastern.
- Second homes: confirm the SimplyMitchell terms for a second home or retirement home before the show, so live answers match.
- Which areas to name on air (the quiz uses Smith Mountain Lake, Lake Gaston, the Shenandoah Valley and the Eastern Shore and Outer Banks).
- Streaming setup and who runs it (same as E2), with the financing line on screen.
- RSVP form (Kelly): name, email, phone, text consent, where you are thinking of building, your question.

**Notes for Kelly**

- The invitation never shows or describes the painted Home Portrait; the follow-up names the quiz only.
- Hosts describe what to check on a lot, never which areas are better places to live (fair housing).
- hp4 goes the morning of the show, so most RSVPs come from the Tuesday post, the Facebook event and the consultant invites; the day-before reminder only reaches those.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Tuesday, November 10 | Social | Post 1 (Facebook, Instagram feed). Publish the online Facebook event. | Marketing |
| Tuesday, November 10 | Google | Event post on all five profiles (or Update) | Marketing |
| Tuesday, November 10 | Sales team | Personal invite text and email to lake, coast and mountain leads | New Home Consultants |
| Wednesday, November 11 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Thursday, November 12 | Email | Event block in hp4, tonight at 7 | Marketing |
| Thursday, November 12 | Social | Post 2, tonight at 7 (Facebook, Instagram Stories) | Marketing |
| Thursday, November 12 | Event | Live at 7pm Eastern; thank-you text after the show | Host; consultants |
| Friday, November 13 | Sales team | Follow-up email with the replay (and Saturday's open house for Carolinas contacts) | New Home Consultants, online sales counselors |

### Email event block

**hp4**, Thursday, November 12, 2026. Event block after the Take the Quiz button and before the footer. hp4's job is the quiz, so the block stays short and sits under the button.

> **Tonight at 7: The Gathering Place, live**
>
> Tonight at 7pm Eastern, join us on Facebook or YouTube for a 30-minute live conversation about building the getaway, the second home or the place you plan to retire, at the lake, on the coast or in the mountains. Bring your questions, especially the hard ones about second-home financing.
>
> [Join Us Tonight]

Link: `[RSVP link]?utm_source=email&utm_medium=email&utm_campaign=fall26_events&utm_content=e5`

### Social posts

**Tuesday, November 10, 2026** · Facebook, Instagram feed

> Some homes are built for every day. Some are built for the long table, the full-house weekend and the years after work.
>
> If you are planning a getaway, a second home or the place you will retire, at the lake, on the coast or in the mountains, join us live on Thursday, November 12, at 7pm Eastern. In 30 minutes we will cover what to look at first on a lake, coastal or mountain lot, how building works when you live hours away, and why the second home banks make hard, Mitchell makes simple.
>
> Watch on Facebook or YouTube. RSVP for a reminder: [RSVP link]
>
> #BuildOnYourLand #MitchellHomes

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e5`  
Notes: Image: a real Mitchell home by the water, e.g. the hp4 hero https://media.mitchellhomesinc.com/276/2026/3/24/10_mwFjkrl.jpg . Never the painted portrait. Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category. Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e5 that morning.

**Thursday, November 12, 2026** · Facebook, Instagram Stories

> Tonight at 7pm Eastern: The Gathering Place, live. Thirty minutes on building a getaway, second home or retirement home at the lake, on the coast or in the mountains. Watch here on Facebook or on our YouTube channel, and ask your questions live.

Link: `[YouTube Live link]`  
Notes: Stories: link sticker to the YouTube Live link. Post the morning of the show.

### Facebook event description

> The Gathering Place Live: Building Your Getaway
> Thursday, November 12, 2026, 7pm Eastern, 30 minutes
> Online: live here on Facebook and on the Mitchell Homes YouTube channel
>
> Some homes are built for every day. Some are built for the long table, the full-house weekend and the place you plan to retire.
>
> If you are planning a getaway, a family retreat, a second home or a home for retirement, at the lake, on the coast or in the mountains, spend 30 minutes with us. We will talk through:
>
> What to look at first on a lake, coastal or mountain lot.
> How building works when you live hours away, with weekly communication from groundbreaking to move-in.
> Why second homes are where banks get strict, and how SimplyMitchell answers it: no construction loan to qualify for, because Mitchell self-funds every build.
>
> Ask your questions live in the comments, or send them ahead: [RSVP link]
>
> Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

Notes: One online Facebook event with Facebook Live as the location. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e5 . Publish Tuesday, November 10.

### Google Business Profile event post

Post on: All five Design Center profiles, Tuesday, November 10. Event-type post, start November 12, 7pm, end 7:30pm.

**Title:** The Gathering Place: Build Your Getaway (39 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e5`

> Planning a getaway, a second home or the place you will retire, at the lake, on the coast or in the mountains? Join Mitchell Homes live on Thursday, November 12, at 7pm Eastern, on our Facebook page and YouTube channel. In 30 minutes we cover what to look at first on a lake, coastal or mountain lot, building from hours away, and how SimplyMitchell removes the construction loan. Tap Sign up for a reminder.

Notes: Online event. If Google rejects it on a studio profile, post as an Update or skip. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Skip: online event, not local.

### Consultant personal invite

Tuesday, November 10, 2026. New Home Consultants to their own active leads who mentioned a lake, the coast or the mountains, or whose quiz answer was a getaway, retreat or retirement.

**Text** (250 characters)

> Hi [first name], [your name] with Mitchell Homes. You mentioned [the lake / the coast / the mountains]. Thursday at 7pm Eastern we are live on Facebook and YouTube for 30 minutes on building a getaway or retirement home. Want me to send you the link?

**Email** · Subject: Thursday at 7: building the getaway

```text
Hi [first name],

You mentioned [the lake, the coast or the mountains] when we talked, so I wanted you to hear about this first.

On Thursday, November 12, at 7pm Eastern, we are going live on Facebook and YouTube for 30 minutes on building a getaway, a second home or the place you plan to retire. We will cover what to look at first on a lake, coastal or mountain lot, how building works when you live hours away, and why second homes are where banks get strict.

That last one matters. Mitchell self-funds every build, so there is no construction loan to qualify for. The second home banks make hard, Mitchell makes simple.

Watch here: [Facebook Live link] or [YouTube Live link]. If you have a question you want answered on air, reply and I will pass it along.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.
```

### RSVP reminder text

Wednesday, November 11, 2026. Builder Studio workflow, RSVPs with text consent only.

> Mitchell Homes: Tomorrow at 7pm Eastern, The Gathering Place, live: 30 minutes on building your getaway. Watch: [YouTube Live link] Reply STOP to opt out

(153 characters)

### Same-day thank-you text

Thursday, November 12, 2026, right after the show. Each consultant to their own leads who RSVPed; online sales counselors to the rest.

> Thank you for joining us tonight, [first name]. The replay is here if you want to share it with whoever you are building the getaway with: [replay link]. Any question we did not get to, text me.

### Next-day follow-up email

Friday, November 13, 2026. The consultant (or an online sales counselor), to every RSVP.

Subject: The getaway, one step closer

```text
Hi [first name],

Thank you for joining The Gathering Place live last night. The full replay is here: [YouTube replay link]

The short version: start with the lot itself, from soil and septic to access and utilities. Building from hours away works because you hear from us every week from groundbreaking to move-in. And with Mitchell there is no construction loan to qualify for, because Mitchell self-funds every build.

If you have not taken the Home Portrait quiz yet, choose your lake, coast or mountain region and tell us what the home is for. Eight questions, about 90 seconds: https://mitchellhomesliving.com/portrait?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e5

[Carolinas contacts only: We are also hosting an open house at our Wilmington Design Center in Belville tomorrow, Saturday, November 14, from 10am to 3pm. Come by any time.]

Or reply with a time, and we can talk about your land, or the land you are still looking for.

Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

[your name]
New Home Consultant, Mitchell Homes
[your phone]
```


---

## E6. Realtor Lunch and Learn

*Proposal until Mitchell approves the date and staffing.*

**When:** Wednesday, November 18, 2026, 11:30am to 1pm  
**Where:** All five Mitchell Design Centers: Fredericksburg VA, Richmond VA (Midlothian), Newport News VA, Raleigh NC (studio in Garner) and Wilmington NC (studio in Belville). Addresses in the studio table, as listed on the live Design Dollars page.  
**For:** Real estate agents and brokers in each Design Center's market: land listing agents first, then agents who have already sent Mitchell a buyer.

**What happens**

- How building on a client's land works with Mitchell: SimplyMitchell (zero down, zero closing costs, no construction loan) and one closing.
- Mitchell Design Dollars ($5,000 on every home, up to $25,000) and the Home Portrait quiz agents can send to clients, plus how to refer.
- Mitchell's realtor incentive program, on terms Mitchell confirms, then open questions and a walk through the Design Center.

**Why it helps the campaign (for Kelly):** Turns agents who meet landowners every week into a referral source for all three campaigns, at the cost of a room and a presenter at each studio.

**Mitchell must confirm**

- Realtor incentive terms, in writing, before any invitation goes out (the same open question as the October realtor email, re1).
- Lunch: the event name promises it. Confirm lunch and a budget at each studio, or rename the event Realtor Learn and Tour everywhere. Copy marks it [Lunch provided: Mitchell to confirm.]
- Continuing education credit: not offered and not mentioned anywhere. Offering it would need course approval first.
- Presenter at each studio (a New Home Consultant; Scott or Deven at one studio if possible) and room capacity.
- The agent list: the realtor segment in Builder Studio by division, land listing agents first.
- Design Dollars after October 31: these pieces name the offer without a reserve-by date. Confirm the program continues in November and approve the November date.
- RSVP form (Kelly): name, brokerage, email, phone, studio, text consent.

**Notes for Kelly**

- Every E6 piece waits on the realtor incentive terms; the lunch bracket comes out or becomes Lunch is on us once Mitchell decides.
- Never promise continuing education credit, in copy or in conversation.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Wednesday, November 4 | Email | Event block in the realtor email rb2 | Marketing |
| Wednesday, November 4 | Social | Post 1 (Facebook, Instagram feed, LinkedIn). Publish the five Facebook events. | Marketing |
| Wednesday, November 4 | Google | Event post on all five profiles | Marketing |
| Wednesday, November 11 | Sales team | Personal invite text and email to agents they know | New Home Consultants |
| Monday, November 16 | Social | Post 2 (Facebook, Instagram Stories, LinkedIn) | Marketing |
| Tuesday, November 17 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Wednesday, November 18 | Event | Lunch and Learn, 11:30am to 1pm; thank-you text | New Home Consultants |
| Thursday, November 19 | Sales team | Follow-up email with the referral kit | New Home Consultants |

### Email event block

**rb2**, Wednesday, November 4, 2026. Event block near the end of rb2 (When your land listing needs a picture), after the Send Your Buyer the Home Portrait button and before the incentive line. rb2 has no Design Dollars footer, so the short fine print sits right under this block.

> **Lunch and Learn at your nearest Mitchell Design Center**
>
> On Wednesday, November 18, from 11:30am to 1pm, each Mitchell Design Center is hosting agents for a short session on how building on a client's land works: SimplyMitchell, Design Dollars ($5,000 on every home, up to $25,000), the Home Portrait quiz, and how to refer. You will also hear the terms of Mitchell's realtor incentive program, and lunch is on us. [Lunch: Mitchell to confirm.]
>
> [Save Your Seat]

Link: `[RSVP link]?utm_source=email&utm_medium=email&utm_campaign=fall26_events&utm_content=e6`

Fine print under the block: Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

### Social posts

**Wednesday, November 4, 2026** · Facebook, Instagram feed, LinkedIn

> Your client owns land. We build the home on it.
>
> On Wednesday, November 18, from 11:30am to 1pm, every Mitchell Homes Design Center is hosting a Realtor Lunch and Learn. [Lunch provided: Mitchell to confirm.] In 90 minutes: how building on a client's land works with Mitchell, from SimplyMitchell (zero down, zero closing costs, no construction loan) to Mitchell Design Dollars and the Home Portrait quiz, how to refer, and the terms of our realtor incentive program.
>
> Fredericksburg, Richmond, Newport News, Raleigh and Wilmington. Save your seat: [RSVP link]
>
> Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e6`  
Notes: Image: a Design Center interior, e.g. https://media.mitchellhomesinc.com/276/2023/3/24/Richmond_Design_Studio.jpg , no people. Could be boosted, so no people in the image (Meta Housing category); if boosted, run it under the Housing special ad category. LinkedIn: same caption with [RSVP link]?utm_source=linkedin&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e6 . Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e6 that morning.

**Monday, November 16, 2026** · Facebook, Instagram Stories, LinkedIn

> This Wednesday, 11:30am to 1pm: Realtor Lunch and Learn at every Mitchell Homes Design Center. [Lunch provided: Mitchell to confirm.] Bring your questions about clients who own land, or are about to buy it. Save your seat: [RSVP link]

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e6`  
Notes: Stories: link sticker with [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e6 . LinkedIn: [RSVP link]?utm_source=linkedin&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e6

### Facebook event description

> Realtor Lunch and Learn at the Mitchell Homes [city] Design Center
> Wednesday, November 18, 2026, 11:30am to 1pm
> [studio address]
>
> For real estate agents and brokers. [Lunch provided: Mitchell to confirm.]
>
> Your clients who own land, or are about to buy it, usually hit the same wall: how do we build on it without a construction loan and a second closing? Mitchell answers that question every day. Spend 90 minutes with us and leave ready to answer it too.
>
> What we cover:
> How building on a client's land works with Mitchell, and why there is zero down, zero closing costs and no construction loan: Mitchell self-funds every build.
> Mitchell Design Dollars. Every Mitchell home comes with $5,000 in Design Dollars to spend on design selections. The more selections the customer buys, the more Mitchell adds, up to $25,000.
> The Home Portrait: a quiz of eight questions, about 90 seconds, you can send to any client.
> How to refer a client, and the terms of Mitchell's realtor incentive program.
> A walk through the Design Center.
>
> RSVP: [RSVP link]
>
> Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.

Notes: One Facebook event per Design Center; only [city] and [studio address] change. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e6 . Publish Wednesday, November 4.

### Google Business Profile event post

Post on: All five Design Center profiles, Wednesday, November 4. Event-type post, start November 18, 11:30am, end 1pm.

**Title:** Realtor Lunch and Learn (23 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e6`

> Real estate agents and brokers: join us at our [city] Design Center on Wednesday, November 18, from 11:30am to 1pm. Learn how building on a client's land works with Mitchell, from SimplyMitchell (zero down, zero closing costs, no construction loan) to Mitchell Design Dollars and the Home Portrait quiz, how to refer, and the terms of our realtor incentive program. Tap Sign up to save a seat.
>
> Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Design Dollars apply to Design Center selections only. Not applied to base price. No cash value.

Notes: If lunch is confirmed, add: Lunch is on us. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Skip: a professional audience, not neighbors.

### Consultant personal invite

Wednesday, November 11, 2026. New Home Consultants to agents they already know.

**Text** (239 characters)

> Hi [first name], [your name] with Mitchell Homes. Next Wednesday, Nov 18, 11:30 to 1, we are hosting agents at our [city] Design Center: how building on a client's land works, how to refer, and our realtor incentive. Can I save you a seat?

**Email** · Subject: Next Wednesday at our [city] Design Center

```text
Hi [first name],

You talk with people who own land, or are about to buy it, every week, so I wanted to invite you personally.

On Wednesday, November 18, from 11:30am to 1pm, we are hosting a Lunch and Learn for agents at our [city] Design Center. [Lunch provided: Mitchell to confirm.] In 90 minutes we will cover how building on a client's land works with Mitchell, why there is zero down, zero closing costs and no construction loan (Mitchell self-funds every build), what Mitchell Design Dollars and the Home Portrait quiz mean for your clients, and how referrals and our realtor incentive program work.

Can I save you a seat? Just reply, and tell me if a colleague would like to come.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Every Mitchell home comes with $5,000 in Design Dollars, up to $25,000 the more you personalize. Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.
```

### RSVP reminder text

Tuesday, November 17, 2026. Builder Studio workflow, RSVPs with text consent only.

> Mitchell Homes: See you tomorrow, Wed Nov 18, 11:30am to 1pm, for the Realtor Lunch and Learn at our [city] Design Center, [studio address]. Reply STOP to opt out

(162 characters)

### Same-day thank-you text

Wednesday, November 18, 2026, that afternoon. The New Home Consultant who hosted.

> Thank you for coming in today, [first name]. Next time a client mentions land, text me their name and I will take it from there. The slides and referral details are coming tomorrow.

### Next-day follow-up email

Thursday, November 19, 2026. The New Home Consultant who hosted.

Subject: For your next client with land

```text
Hi [first name],

Thank you for joining us at the Design Center yesterday. Here is everything in one place for the next client who mentions land.

The short version for your client: Mitchell has built custom homes on land the buyer owns since 1992. Mitchell self-funds every build, so there is zero down, zero closing costs and no construction loan. More than 40 floor plans from 1,000 to 3,000 square feet, and more than 40,000 selections.

Design Dollars: every Mitchell home comes with $5,000 in Mitchell Design Dollars, and it goes up to $25,000 the more your client personalizes.

The Home Portrait quiz to send a client: https://mitchellhomesliving.com/portrait?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e6

How to refer: [referral steps, once Mitchell confirms]
Realtor incentive: [terms, once Mitchell confirms]

When you have a client ready to talk, text or call me directly.

[your name]
New Home Consultant, Mitchell Homes
[your phone]

Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. Financing terms are illustrative only and subject to credit approval. Not a commitment to lend.
```


---

## E7. Homeowner Appreciation Night

*Proposal until Mitchell approves the date and staffing.*

**When:** Tuesday, November 10, 2026, 5:30pm to 7:30pm, local time at every studio  
**Where:** All five Mitchell Design Centers: Fredericksburg VA, Richmond VA (Midlothian), Newport News VA, Raleigh NC (studio in Garner) and Wilmington NC (studio in Belville). Addresses in the studio table, as listed on the live Design Dollars page.  
**For:** Past Mitchell homeowners and their families, invited personally by the New Home Consultant who built with them and by email (ho2, the homeowner invitation in campaigns/homeowners/contest.json). RSVP requested so each studio can plan; families welcome.

**What happens**

- A thank-you evening for the people who built with Mitchell: homeowners catch up with the New Home Consultants and Design Consultants who helped build their home and meet other Mitchell homeowners. [Refreshments: Mitchell to confirm.]
- My Mitchell Story opens that night. Homeowners hear how it works (a short phone video about what they love about their home) and can book their photo session on the spot at a booking table.
- A simple story corner at each studio: a chair, good light, a phone stand and the four questions on a card. Staff help homeowners film a first take on their own phone, so the take is theirs to finish at home and send in.

**Why it helps the campaign (for Kelly):** Starts My Mitchell Story in person with the homeowners most likely to enter, from the people they built with. Homeowners leave with a photo session booked and, for many, a first take already on their phone, which is the hardest part of any video contest.

**Mitchell must confirm**

- Approve Tuesday, November 10, 5:30pm to 7:30pm, at all five studios, or name the studios that will host. Nothing else is in the studios that night: E3 is Saturday, November 7, E5 is online on Thursday, November 12, and E4 is Saturday, November 14 in Wilmington. The Wilmington team works three events in eight days; name the cover.
- Staffing at every studio: the New Home Consultants and Design Consultants who can attend, one person at the photo session booking table, and one at the story corner.
- Refreshments and a budget per studio. An appreciation night implies something to eat or drink; every piece marks it [Refreshments: Mitchell to confirm.]
- My Mitchell Story must be approved before November 10: the prizes, the form of the $2,500, the photo session cap and budget, the photographers, and the Official Rules after legal review. If it is not, the night runs as a thank-you evening and the contest launch moves.
- Photo session booking on the night: the photographers' calendars must be live in Builder Studio by Monday, November 9. A session booked that night is held for the homeowner and takes place after their entry arrives.
- The homeowner list: confirm past homeowners are in Builder Studio with email addresses, which have text consent, and which consultant invites homeowners whose consultant has left Mitchell.
- Homeowners with an open warranty issue: CEA suggests their consultant or the warranty team calls them before any invitation goes out.
- RSVP form (Kelly builds it in Builder Studio): name, email, phone, studio, number of guests, and the text consent checkbox with legal-approved wording. It adds the tag homeowner appreciation rsvp.
- Story corner kit per studio: a chair, a phone stand, a small light and a card with the four questions. No painted Home Portrait anywhere in the room or on screens.

**Notes for Kelly**

- Never show a painted Home Portrait at the event, on screens or at the story corner. The finalist prize is described in words only: a framed painting of their Mitchell home.
- Story corner: staff film on the homeowner's own phone, so the take belongs to the homeowner. Everyone filmed says yes first; children only with a parent there and agreeing. No popular music playing in the room, so the take can be used.
- Photos of homeowners at the event are for organic social, email and the website only, with their consent. Never in paid ads (Meta Housing category).
- Fair housing: hosts and captions never describe a town or neighborhood as good, safe or desirable.
- The full contest package (rules, form, emails ho2 to ho6, workflow emails, texts, social, photographer brief) is campaigns/homeowners/contest.md.

**Schedule**

| Date | Channel | What | Who |
|---|---|---|---|
| Wednesday, October 28 | Email | ho2, the invitation, to past homeowners (campaigns/homeowners/contest.json) | Marketing |
| Wednesday, October 28 | Social | Post 1 (Facebook, Instagram feed). Publish the five Facebook events. | Marketing |
| Wednesday, October 28 | Google | Event post on all five Design Center profiles | Marketing |
| Thursday, October 29 | Sales team | Personal invites to the homeowners each consultant built with, through Tuesday, November 3 | New Home Consultants |
| Monday, November 9 | Text | Reminder to RSVPs only | Builder Studio workflow |
| Tuesday, November 10 | Social | Post 2 (Facebook, Instagram Stories) | Marketing |
| Tuesday, November 10 | Event | Homeowner Appreciation Night, 5:30pm to 7:30pm; My Mitchell Story entries open; thank-you text by 9pm | New Home Consultants, Design Consultants, photo session booker |
| Wednesday, November 11 | Sales team | Follow-up email to every homeowner who came (in place of ho3) | New Home Consultants |
| Wednesday, November 11 | Email | ho3, the My Mitchell Story launch, to past homeowners who did not come | Marketing |

### Email event block

No block in a buyer email. A thank-you evening for homeowners has its own invitation, ho2, sent to past homeowners on Wednesday, October 28; it lives with the contest emails in campaigns/homeowners/contest.json.
### Social posts

**Wednesday, October 28, 2026** · Facebook, Instagram feed

> To everyone who has built a home with Mitchell: thank you.
>
> On Tuesday, November 10, from 5:30pm to 7:30pm, every Mitchell Design Center is hosting Homeowner Appreciation Night. Come see the people who helped build your home, meet other Mitchell homeowners, and bring the family.
>
> It is also the night My Mitchell Story opens: show us, in a short phone video, what you love about your home. Everyone who enters gets a professional photo session at their home, paid for by Mitchell, while sessions last.
>
> Fredericksburg, Richmond, Newport News, Raleigh and Wilmington. Mitchell homeowners, please RSVP so we can plan: [RSVP link]
>
> #MyMitchellStory #MitchellHomes

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e7`  
Notes: Image: a real Mitchell home at dusk, e.g. https://media.mitchellhomesinc.com/276/2026/3/3/ava_farmhouse-extended_sky.jpg . Organic only; do not boost (the audience is homeowners, and a boosted post would reach buyers). Instagram: replace the RSVP line with RSVP at the link in bio, and set the bio link to [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e7 that morning.

**Tuesday, November 10, 2026** · Facebook, Instagram Stories

> Tonight, 5:30pm to 7:30pm: Homeowner Appreciation Night at every Mitchell Design Center. Mitchell homeowners, come say hello, book your photo session, and film a first take of your story in our story corner.
>
> #MyMitchellStory

Link: `[RSVP link]?utm_source=facebook&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e7`  
Notes: Stories, the morning of the event, with the link sticker [RSVP link]?utm_source=instagram&utm_medium=organic_social&utm_campaign=fall26_events&utm_content=e7 . After the event, post photos from the night only of homeowners who said yes, organic only, never boosted.

### Facebook event description

> Homeowner Appreciation Night at the Mitchell Homes [city] Design Center
> Tuesday, November 10, 2026, 5:30pm to 7:30pm
> [studio address]
>
> For Mitchell homeowners and their families.
>
> You built a home with us, and we would like to say thank you in person. Catch up with the New Home Consultants and Design Consultants who helped build your home, meet other Mitchell homeowners, and bring the family. [Refreshments: Mitchell to confirm.]
>
> It is also the night My Mitchell Story opens. Tell us, in a short phone video, what you love about your home, how you use it and where you like to spend your time. Everyone who enters gets a professional photo session at their home, paid for by Mitchell, while sessions last. Book yours that night, and film a first take in our story corner if you like.
>
> Please RSVP so we can plan: [RSVP link]
>
> Questions? Call a New Home Consultant: Virginia and Maryland (540) 701-2759, North and South Carolina (984) 331-5468.

Notes: One Facebook event per Design Center; only [city] and [studio address] change. Link: [RSVP link]?utm_source=facebook&utm_medium=facebook_event&utm_campaign=fall26_events&utm_content=e7 . Publish Wednesday, October 28. Cover image: a real Mitchell home at dusk, no people. Do not boost. If a prospective buyer RSVPs, welcome them and have a consultant follow up separately.

### Google Business Profile event post

Post on: All five Design Center profiles, Wednesday, October 28. Event-type post, start November 10, 5:30pm, end 7:30pm.

**Title:** Homeowner Appreciation Night (28 of 58 characters)  
**Button:** Sign up, linking to `[RSVP link]?utm_source=google_business_profile&utm_medium=organic&utm_campaign=fall26_events&utm_content=e7`

> Mitchell homeowners, this evening is for you. Join us at our [city] Design Center on Tuesday, November 10, from 5:30pm to 7:30pm, to catch up with the people who helped build your home, meet other Mitchell homeowners and bring the family. It is also the night we open My Mitchell Story, a short video about what you love about your home. Tap Sign up to RSVP.

Notes: Image: a real Mitchell home exterior, no people. A public post that shows buyers how Mitchell treats its homeowners. If Google rejects a post for a phone number in the text, delete that sentence; the Call button uses the profile number.

### Nextdoor

Skip: an invitation for Mitchell homeowners, not the neighborhood.

### Consultant personal invite

Thursday, October 29 to Tuesday, November 3, 2026. Every New Home Consultant to the homeowners they built with: a text where they already text that homeowner, otherwise the email or a call. Homeowners whose consultant has left Mitchell hear from the division's consultant.

**Text** (156 characters)

> Hi [first name], [your name] from Mitchell. Join us for Homeowner Appreciation Night, Tue Nov 10, 5:30 to 7:30pm, at our [city] Design Center. Can you come?

**Email** · Subject: You are invited, [first name]

```text
Hi [first name],

I still remember [one thing about their home or their build]. I hope the home is treating you well.

On Tuesday, November 10, from 5:30pm to 7:30pm, we are hosting Homeowner Appreciation Night at our [city] Design Center, a thank-you evening for the people who built with us. Bring the family. [Refreshments: Mitchell to confirm.]

It is also the night we open My Mitchell Story: a chance to show us, in a short phone video, what you love about your home and how you live in it. Everyone who enters gets a professional photo session at their home, paid for by Mitchell, while sessions last. You can book yours that night.

Can you make it? Reply and I will save you a spot, or RSVP here: [RSVP link]

[your name]
New Home Consultant, Mitchell Homes
[your phone]
```

### RSVP reminder text

Monday, November 9, 2026. Builder Studio workflow on the RSVP form, to RSVPs with text consent only.

> Mitchell Homes: See you tomorrow, Tue Nov 10, 5:30 to 7:30pm, for Homeowner Appreciation Night at our [city] Design Center. Reply STOP to opt out

(145 characters)

### Same-day thank-you text

Tuesday, November 10, 2026, by 9pm. The consultant who invited each guest.

> Thank you for coming tonight, [first name]. It was so good to see you. I will email you the My Mitchell Story link in the morning, and if you filmed a first take, it is on your phone and ready to finish at home.

### Next-day follow-up email

Wednesday, November 11, 2026, morning. The consultant, to every homeowner who came. Attendees get this in place of ho3, the launch email, so nobody gets two that day.

Subject: Thank you for last night

```text
Hi [first name],

Thank you for coming to Homeowner Appreciation Night. It was good to see you, and to hear about [one thing they shared about their home].

Here is everything for My Mitchell Story in one place.

Film a short video on your phone, about 30 to 90 seconds, at home, answering one or more of these: What do you love most about your home? How do you use it, day to day? How does your home make you feel? Where is your favorite place to hang out?

Send it here: [entry form link]?utm_source=sales_email&utm_medium=email&utm_campaign=fall26_events&utm_content=e7 . Upload the video or paste a link. Entries close Sunday, December 6, at 11:59pm Eastern.

[If they booked: Your photo session is set for [date and time]. If not: Once your entry is in, you will get a link to book your photo session.]

If you filmed a first take in the story corner, it is on your phone. Add a minute at home, the porch, the kitchen, your favorite spot, and send it in.

Five finalists, one from each Design Center region, receive their own Home Portrait, a framed painting of their Mitchell home, and one grand prize winner also receives $2,500. Official Rules: [official rules link]

I cannot wait to see your story.

[your name]
New Home Consultant, Mitchell Homes
[your phone]
```

