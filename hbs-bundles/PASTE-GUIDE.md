# Putting the campaign pages into Home Builder Studio

The page builder has no API, so these pages go in by hand. Each file in this folder is one page, self-contained: fonts, styles, images (hosted on Mitchell's CDN and the media library), and the form script that posts to the Design Dollars intake on Vercel. The reviewer build-notes layer is stripped from these copies; the open flags live in `../landing-pages/PRE-LAUNCH-FLAGS.md`.

## Before pasting (Claude does these once the subdomain is chosen)

1. Create the funnel subdomain on Vercel DNS and point it at HBS (CNAME to the target HBS shows under Sites, Domains, Add Domain).
2. Add that domain to the Design Dollars intake's `ALLOWED_ORIGINS` env var on Vercel and redeploy, so the forms are accepted from the new origin.
3. Add rewrites on the quiz project so the existing `mitchellhomesliving.com/calculator` style links forward to the new funnel URLs.

## In Home Builder Studio (person in the builder)

Sites, Funnels. Either reuse "Mitchell Homes August 2026 Persona Campaign" (id `fxejant48f6OjCRhtiCa`) or create a new funnel. For each step:

| Step name | Path | Bundle file | Form key it posts |
|---|---|---|---|
| Savings Calculator | `/calculator` | calculator.html | lp-calculator |
| Two Ways to Build | `/math` | math.html | lp-math |
| Your Land | `/land` | land.html | lp-land |
| No Land Yet | `/no-land` | no-land.html | lp-no-land |
| Dreamer VA | `/dreamer` | dreamer.html | lp-dreamer |
| Dreamer Carolinas | `/dreamer-carolinas` | dreamer-carolinas.html | lp-dreamer-carolinas |
| Thank You | `/thank-you` | thank-you.html | (none, conversion page) |
| Design Dollars | `/design-dollars` | design-dollars.html | design-dollars |
| Design Dollars NHI | `/design-dollars-nhi` | design-dollars-nhi.html | design-dollars-nhi |

1. Open the step, delete any default section, add one section, one row, one full-width column.
2. Add a **Custom JS/HTML** element to the column. Set the section and row padding to 0 and width to full.
3. Open the bundle file, select all, copy, paste into the element. Save.
4. In step settings, set the path from the table. Set SEO title and description from the page's `<title>` and meta description.
5. Preview: check the form submits (a test submission should redirect to `/thank-you` and appear in Contacts within seconds) and that the Design Studio cards and images load.
6. On the Thank You step, add the Meta pixel Lead event and Google Ads conversion under the step's tracking code once those IDs are available.

Notes:
- Set the funnel's default page CSS to none if HBS injects its own body font or spacing; the bundles carry their own reset.
- The Design Dollars bundles are larger (about 96 KB) because the Charlotte script font is embedded. If the element refuses the paste, split it: put the `<style>` block into the step's custom CSS and the rest into the element.
- The form script keeps working in the builder's preview because it posts to an absolute Vercel URL.

## After pasting

Tell Claude which funnel and domain were used. Claude will then run a test submission per page, confirm each lands in Builder Studio with the right source and persona, and update the notes.
