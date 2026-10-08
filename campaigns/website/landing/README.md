# Home Portrait landing page (draft for Kelly)

`home-portrait.html` is the page a visitor sees when they come to the Mitchell website to take the Home Portrait quiz. Draft only, October 8, 2026. Nothing has been deployed or uploaded.

To preview, open the file in a browser. Photos load from Mitchell's own media CDN, the logos and the one sample painting load from the Builder Studio media library, and the Montserrat and Charlotte fonts load from https://mitchellhomesliving.com/fonts/. Screenshots are in `../shots/` (`landing-desktop-full.png`, `landing-phone-full.png`).

## What is on the page

1. Header with the Mitchell logo and a Begin My Portrait button.
2. Hero: a real Mitchell farmhouse, the tagline "Every home is a portrait. Discover Yours." with Yours in Charlotte, the quiz line, Begin My Portrait, and "About 90 seconds. No land yet is a good answer too."
3. How it works: three steps, plus the Design Center locations (Virginia and North Carolina).
4. Inside your portrait: the eight things the portrait holds, with ONE sample painting labeled as a sample (flagged for Kelly in an HTML comment).
5. The five portrait names, each with one plain sentence and a real Mitchell photo.
6. SimplyMitchell band with the illustrative financing qualifier.
7. Design Dollars band with the exact Current Incentives wording, the ladder, and the long fine print.
8. Downey homeowner quote, verbatim, with the YouTube link.
9. FAQ (four questions) plus matching FAQPage schema in the head.
10. Closing call to action and a footer with the address, both New Home Consultant lines, "Building on your land since 1992", and where Mitchell builds (stated separately from the Design Center claim).

On phones a Begin My Portrait button stays pinned to the bottom of the screen between the hero and the closing section. No people appear in any photo, so the page is also safe under the Meta housing category rules if it ever takes paid traffic.

## How to put it on the Mitchell site

**Option A, recommended: a page on mitchellhomesinc.com built by the website vendor.**
1. Ask the vendor for a new page at the suggested URL below, using a blank template (no site header and footer) or the standard template if they prefer the site navigation.
2. Paste the `<style>` block and the FAQ `<script type="application/ld+json">` into the page head, and everything inside `<body>` into the page body. Every style is scoped under the `.mhl` wrapper, so it will not restyle the rest of the site. If the page uses the site template, drop the three lines marked "Standalone page only".
3. Keep the small script at the bottom (it only runs the phone sticky button).
4. Make sure the site's analytics and Meta pixel load on the page, as they do sitewide.
5. The website pop-up snippet already skips any URL containing `/home-portrait` and `/portrait`, so the pop-up will not appear on this page.

**Option B: a Builder Studio funnel page.** Create a one-step funnel, add a full-width custom code element, and paste the whole file. Connect it to a Mitchell domain path or subdomain. This keeps the page in the same account as the quiz leads, but it sits outside the main site's navigation and search history.

Either way, the quiz itself stays where it is at https://mitchellhomesliving.com/portrait. Every button on this page links there with UTMs.

## Suggested URL and meta

* URL: https://www.mitchellhomesinc.com/home-portrait/
* Meta title: The Home Portrait | Mitchell Homes
* Meta description: Answer eight questions about the home you dream of and the land it belongs on, and Mitchell Homes paints your Home Portrait. About 90 seconds. No land yet is a good answer too.
* Social share image: the farmhouse hero photo (already set in the og:image tag).

## UTM map

All quiz links use `utm_source=mitchellhomesinc`, `utm_medium=landing`, `utm_campaign=fall26_portrait`. The `utm_content` value names the spot: `header`, `hero`, `howitworks`, `inside`, `portraits`, `closing`, `sticky` (phone only).

## Things the vendor should know

* Fonts load from mitchellhomesliving.com, which allows cross-site loading. If the vendor would rather self-host, copy `home-portrait/fonts/montserrat.woff2` and `charlotte.woff2` to the site and change the two `@font-face` URLs plus the preload link.
* Photos use Mitchell's media CDN size and crop parameters (`?width=...&height=...&mode=crop`). If the vendor swaps a photo, keep the parameters.
* The Design Dollars fine print is the working draft from the Current Incentives doc and must be swapped for Mitchell's official terms sheet when it arrives. If the offer changes, the Design Dollars band and the one line in "Inside your portrait" are the only places to edit.

## Open questions for Kelly

1. **Sample painting.** The page shows one painting, once, labeled Sample (the Fredericksburg cover). The painting is the reward, so keep it or delete that one `<figure>`; the page reads correctly either way.
2. **Downey quote.** FACTS clears it for organic and email. If this page will take paid traffic, confirm it is cleared for a paid landing page too.
3. **Phone lines.** The footer uses (540) 701-2759 for Virginia and Maryland and (984) 331-5468 for the Carolinas. The live site header shows (804) 538-3912. Which should this page carry?
4. **Design Studio or Design Center.** FACTS names the portrait's next step "a Design Studio visit" and the locations "Design Centers". The page uses both that way. Confirm Mitchell is happy with that, or pick one.
5. **Buyers without land.** The page welcomes them but does not say SimplyMitchell works the same when the land is still being bought, because that is an open question from the no land page. Confirm with Mitchell.
6. **"The quiz and your Home Portrait cost nothing."** Plainly true, but not written in FACTS. Confirm it is fine to say.
7. **Reserve-by date.** The October 31, 2026 rolling date is left off on purpose so the page does not need a monthly edit. Add it if Mitchell wants the urgency.
8. **License numbers.** Contractor license numbers by state have not been supplied. Add them to the footer if required.
9. **Hero photo.** The farmhouse sunset sky looks enhanced. It is Mitchell's own photo, but confirm Kelly is comfortable leading with it.
10. **Things in the live quiz a visitor will hit next** (not changed here): question eight's subline and the Planner portrait text say "about 150 days", which conflicts with the no-build-duration rule; the capture screen's SimplyMitchell logo alt text reads "Simply Mitchell" as two words; and question five says "Helping you find it is part of what we do", which is still an open flag on the no land page.
