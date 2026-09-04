# Mitchell Design Dollars landing page + GoHighLevel integration

Static landing page on Vercel with serverless functions that push form submissions into the Mitchell Homes
GoHighLevel sub-account.

## Layout
- `index.html`, `nhi-index.html`: the pages. Each form has `data-page="<key>"` matching `lib/pages.js`.
- `api/lead.js`: form endpoint. Validates, runs the pipeline, sets the `mh_cid` cookie.
- `api/track.js`: return-visit hook for contacts who already submitted (tag + note).
- `lib/pages.js`: page registry (source, persona, tags, form type, opportunity settings) and GHL field ids.
- `lib/pipeline.js`: ordered steps (build contact, upsert, note, opportunity). Append steps to extend.
- `lib/ghl.js`: GHL V2 client (upsert, tags, notes, opportunities).
- `lib/counties.js`: County of Interest picklist + matcher.

## Environment variables (Vercel project settings)
- `GHL_PRIVATE_TOKEN`: sub-account private integration token
- `GHL_LOCATION_ID`: `5o5zLlUPPizy6Ajp61oF`
- `ALLOWED_ORIGINS` (optional): comma-separated origins allowed to post, for when the page is hosted elsewhere too

## Adding a page
1. Add an entry to `PAGES` in `lib/pages.js` (source, persona, tags).
2. Set `data-page="<key>"` on the form.

## Opportunities
Enabled for both pages: each new lead gets an opportunity in the OSC pipeline at New Lead (ids in `PIPELINES`).
A contact with an open opportunity does not get a second one. Set `opportunity.enabled: false` on a page entry to stop.

## Deploy
`npx vercel deploy --prod --yes` from this folder.
