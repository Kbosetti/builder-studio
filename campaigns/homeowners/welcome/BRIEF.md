# Build brief: Mitchell Homes "Welcome to Our Homeowner Community" page

You are building a page for CEA Marketing (Kelly Bosetti) and its client Mitchell Homes. The repo is Kbosetti/builder-studio. Fetch and work from the branch `claude/research-ghl-hbs-i8YQV` unless your session is set to another branch, and pull before you push, because other sessions commit to it too. Commit as Kelly Bosetti <kelly@ceamarketing.com>. Draft work only: do not send, post or print anything, and do not create anything in Mitchell's Builder Studio account.

## Read first

1. `CLAUDE.md` at the repo root (accounts, hosting, deploy scripts, and the flags below).
2. The Mitchell messaging skill: invoke `anthropic-skills:cea-mitchell-homes-messaging` and read it fully before writing any copy.
3. `campaigns/FACTS.md`, the one fact sheet.
4. `campaigns/homeowners/welcome/brittany-closing-card-draft.webp`, the card this page has to match.

## Where it comes from

Brittany Horner, Mitchell's Marketing Lead, designed a printed card for the closing gift. The project superintendent hands it to every homeowner at the final walkthrough and on closing day, in the gift box with a logo knife set and a mug set. The card:

- Mitchell logo with the tagline lockup at the top.
- "Welcome to Our Homeowner Community!" in the Charlotte script, Mitchell green.
- A QR code in a yellow rounded frame, with: "Your feedback is valuable to our team. Please scan the QR code with your phone's camera to let us know how we are doing!"
- "Follow us on socials! Snap photos of your new Mitchell Home and tag us."
- "Thank you, The Mitchell Homes Team", with "Thank you" in Charlotte.
- A sunrise landscape photo across the bottom, on a white card.

Her goals, from her video to the team:

- Get more five-star reviews on Google and Yelp for every location.
- Get user-generated content: homeowners posting their new home and tagging Mitchell, for organic social and stronger brand loyalty.
- Build trust early with future buyers who are already watching Mitchell's content.

Her ask to Kelly and Tom is a landing page behind the QR code (today it is a placeholder pointing at the website). It should have "very similar branding, identical if we can help it". She will send the assets. On it, the homeowner chooses the location they built with and gets that location's Google review link and Yelp link, plus the social links, "all in one link, really clean and a quick experience". The sales team will also keep the link "in their back pocket" for any happy homeowner. Scott, the CEO, still has to approve the idea, and Dorna prints the cards, so the QR code's destination has to be final before printing.

## What to build

A single static page, mobile first, since nearly everyone arrives from a phone camera:

1. **Header** matching the card: Mitchell logo and tagline lockup, then "Welcome to Our Homeowner Community!" in Charlotte, then one line of thanks for building with Mitchell.
2. **Leave a review.** "Which Design Center did you build with?" offers five large tap targets. Picking one shows that location's "Review us on Google" button first and biggest, with Yelp second. Below them go the studio's name, address and phone, all from the `studios` list in `campaigns/events/events.json`:
   - Fredericksburg VA
   - Richmond VA (Midlothian)
   - Newport News VA
   - Raleigh NC (Garner)
   - Wilmington NC (Belville)
3. **Follow along.** "Snap photos of your new Mitchell home and tag us @mitchellhomes." Buttons for:
   - Facebook https://www.facebook.com/MitchellHomesInc
   - Instagram https://www.instagram.com/mitchellhomes/
   - X https://twitter.com/_mitchellhomes

   Ask Kelly whether YouTube (Behind the Build) and TikTok belong here. Do not guess their URLs.
4. **Sign-off** matching the card: "Thank you, The Mitchell Homes Team", with the landscape photo along the bottom.
5. **Deep links for the sales team.** Each location has its own link that opens with that studio already chosen, for example `#richmond`. Remember the visitor's choice in localStorage, wrapped in try/catch.

Keep every link in one config object at the top of the script, so swapping in the real review links is a one-line edit each.

### Links we do not have yet

- **Google:** each Design Center's direct "Ask for reviews" link (`https://g.page/r/.../review`), which Brittany can copy from each Business Profile. Until she sends them, use a Google Maps search for that studio's address and mark it as a placeholder. Never use the old Powhatan headquarters profile; it is a stale duplicate.
- **Yelp:** each location's business page. Use a Yelp search for "Mitchell Homes" in that city as a placeholder.
- **Assets:** Brittany's logo with the tagline lockup and her landscape photo. Until they arrive, use `campaigns/print/src/mitchell-logo-color.png` and a real Mitchell landscape from `campaigns/print/src/` (farmland.jpg is close). Fonts are in `assets/fonts/` (Charlotte.woff2, Montserrat.woff2); self-host them with the page.

## Brand rules that apply

- No em dashes or en dashes anywhere. Grammatical hyphens in compound modifiers are fine.
- Montserrat for all text. Charlotte is the script, and in our work it always gets the tagline logo treatment: `font-style:oblique 10deg;-webkit-text-stroke:.035em currentColor;paint-order:stroke fill`. The brand guide keeps Charlotte to one word. Brittany's card sets the whole welcome line in it, and since she owns the brand and asked for identical, match the card and mention the guideline to Kelly once.
- **Colors:**
  - Mitchell Green #2b6d47
  - Deep Green #1e4f33
  - Yellow #f5d053, for the frame
  - Warm Grey #929292
  - a white ground, as on the card
- SimplyMitchell is one word. The title is New Home Consultant. The platform is Builder Studio, never HighLevel. Never name a previous agency.
- Geography is two separate claims. The five Design Centers are in Virginia and North Carolina. Mitchell builds in Virginia, North Carolina, South Carolina and Maryland. Never merge them into one sentence.
- Real Mitchell homes in the photos. This is an organic page, so the paid-ad limit on family photos does not apply, but keep it to homes and land anyway.
- Never show a painted Home Portrait. The painting is what people get from the quiz.

## Compliance points to build in, and to explain to Kelly in a few lines

- **No review gating.** Every visitor sees the review links. Do not ask "how did we do?" first and send only happy people to Google; Google's policy forbids filtering reviews by sentiment. A private feedback option is fine only as an equal choice, never as a screen in front of the review links.
- **The gift is not tied to a review.** The card and page must never suggest the gift depends on leaving one. That is an FTC and Google rule.
- **Yelp.** Yelp asks businesses not to solicit reviews and filters ones it thinks were solicited. Label the Yelp button "Find us on Yelp", not "Review us on Yelp", and tell Kelly why, so she and Brittany can decide.
- Basic accessibility: real buttons and links, visible focus, enough contrast, alt text, and tap targets of at least 44px.

## Ideas worth offering (as options, not built unless Kelly says yes)

- **"Need warranty service?"** A homeowner with a problem should find the warranty request path here, before they find the review button out of frustration. Ask Kelly for Mitchell's warranty page URL.
- **A referral tile.** "Know someone dreaming of building on their land? Send them the Home Portrait." Link to https://mitchellhomesliving.com/portrait with `utm_source=homeowner_welcome&utm_medium=qr&utm_campaign=homeowner_referral`. The quiz is eight questions, about 90 seconds, and ends with a painted Home Portrait of the home they would build. The page never shows the painting itself.
- **My Mitchell Story.** That's Brittany's homeowner photo and video contest, planned for Q1 2027 (see `campaigns/homeowners/contest.md`). Once it launches, this page is a natural home for the hashtag #MyMitchellStory and the entry link. For now, add only an optional "Coming soon" slot if Kelly wants it.
- **Measurement.** UTM-tag the outbound links where the platform allows it. Leave a clearly marked spot for a GTM or GA4 container ID, so scans and taps per location can be counted once Kelly sends the ID.

## Hosting and the QR code

- **Draft hosting:** deploy the draft as its own Vercel project with `scripts/vercel_static_deploy.py <folder> mitchell-homeowner-welcome`, which needs `VERCEL_TOKEN` (see CLAUDE.md for credentials). Keep it noindex while it is a draft. Follow the pattern of the other deploy scripts, such as `campaigns/events/deploy_events_page.py`.
- **Do not deploy the `home-portrait/` project.** CLAUDE.md explains why: the live quiz runs newer code than this repo. So do not add a `/welcome` rewrite to mitchellhomesliving.com from here.
- **The printed URL has to be permanent.** Recommend a short address Mitchell controls, for example mitchellhomesliving.com/welcome once the quiz code is synced, or a page on mitchellhomesinc.com. Let Kelly and Brittany pick before Dorna prints.
- **The QR code:** generate it once the URL is final, as SVG plus a 1200px PNG, Mitchell-green modules with a quiet zone. `campaigns/print/make_print.py` has a `qr()` helper. Print the short URL under the code too, for anyone whose camera won't scan.

## Deliverables

1. The page source and assets in `campaigns/homeowners/welcome/`, with a build or deploy script.
2. The draft link on Vercel, checked at phone and desktop widths.
3. A short note to Kelly covering:
   - what is placeholder
   - the links and assets to get from Brittany: five Google review links, five Yelp pages or a decision to skip Yelp, her logo lockup and photo, the warranty URL, the final URL, and Dorna's print deadline
   - the compliance points
   - two or three quick suggestions for the card itself: point the QR at the final URL, add the @mitchellhomes handle, print the short URL under the code
4. A CLAUDE.md entry for the page, then commit and push.
