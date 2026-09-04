# Landing pages: build notes still live, pre-launch flags open

**Status (September 4, 2026): the "Show build notes" toggle and the yellow reviewer notes are still on every landing page, on purpose.** Kelly asked to leave them on for now. They are visible to any visitor who clicks the button, and the note text is in the page source.

Before any ad traffic points at `mitchellhomesliving.com/calculator`, `/math`, `/land`, `/no-land`, `/dreamer`, `/dreamer-carolinas`, or `/thank-you`:

1. Resolve the open flags below with Scott, Deven, and legal.
2. Remove the toggle (`<button class="modebar" id="modebtn">`, its script, and every `<p class="verify">`) from the seven pages.
3. Redeploy from `landing-pages/`.

## Open flags carried in the notes

### Calculator and Math
- Savings formula conflict: pages use 8 percent, supplied by the client. Mitchell's published blog states $29,250 on a $450,000 home, which is 6.5 percent. Both cannot be right. Flag to Scott. Notes say "held from market" until resolved.
- Math page, CLIENT HOLD Aug 19: Brittany is not confident the section she marked in red is factually correct. Confirm with Scott or Deven before publish. Kelly to confirm which rows were marked.
- TCPA language on the SMS consent checkbox requires legal sign off.

### Land, Dreamer, Dreamer Carolinas
- SimplyMitchell compliant short form disclaimer and "illustrative only" qualifier required before publish.
- "Locked pricing from day one" comes from the Behind the Build series. Confirm it is still approved wording and whether conditions apply.

### No Land
- Verify with Mitchell: does the company help buyers find land, refer them, or stay out of it entirely?
- Fair housing: this page must never recommend counties or describe areas as desirable.
- How far can a buyer get in the design process before closing on a lot?
- Do the Simply Mitchell terms work identically for a buyer purchasing land rather than already holding it? The page currently implies they do.

### Dreamer Carolinas
- Whether sales calls the studio Raleigh or Garner, since the address is in Garner.
- Some supplied coastal images appear to have composited skies.

### Thank You
- Page copy promises the plan guide by email. Nothing sends that email yet. Either build a HighLevel workflow on the `plan guide requested` tag that emails https://richmond-zone-mit.idapro.cloud/plan_flip, or change the copy.

### All pages
- Design Dollars offer copy: October 31, 2026 is the first rolling "reserve by" date; only the date changes month to month.
