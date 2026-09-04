// POST /api/track  ->  lightweight activity hook for known contacts returning to a landing page.
// Only acts when the browser carries the mh_cid cookie set by /api/lead. Extend `EVENTS` for more activity types.

import { createGhlClient } from '../lib/ghl.js';
import { resolvePage } from '../lib/pages.js';
import { applyCors, readBody, parseCookies, clientMeta } from '../lib/http.js';

const EVENTS = {
  async return_visit(ctx) {
    await ctx.ghl.addTags(ctx.contactId, ['returning visitor']);
    await ctx.ghl.addNote(ctx.contactId, [
      `Returned to ${ctx.page.name}`,
      `When: ${new Date().toISOString()}`,
      `Page URL: ${ctx.meta.pageUrl || ctx.page.url}`,
      ctx.meta.referrer ? `Referrer: ${ctx.meta.referrer}` : null,
    ].filter(Boolean).join('\n'));
  },
};

export default async function handler(req, res) {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false });

  const body = await readBody(req);
  const contactId = parseCookies(req).mh_cid;
  const page = resolvePage(body.page);
  const event = EVENTS[body.event];
  if (!contactId || !page || !event) return res.status(204).end();

  try {
    const ghl = createGhlClient();
    await event({ ghl, contactId, page, meta: clientMeta(req, body) });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('[track] failed', err.status || '', err.body || err.message);
    return res.status(204).end();
  }
}
