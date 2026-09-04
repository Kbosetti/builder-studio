// POST /api/lead  ->  creates/updates a GoHighLevel contact from a landing page form.
// Body (JSON): { page, firstName, lastName, email, phone, county, landStatus, company (honeypot), meta:{...} }

import { createGhlClient } from '../lib/ghl.js';
import { resolvePage } from '../lib/pages.js';
import { runPipeline } from '../lib/pipeline.js';
import { applyCors, readBody, setCookie, clientMeta } from '../lib/http.js';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default async function handler(req, res) {
  applyCors(req, res);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'POST only' });

  const body = await readBody(req);

  // Honeypot: bots fill the hidden "company" field. Pretend success so they stop.
  if (body.company) return res.status(200).json({ ok: true });

  const page = resolvePage(body.page);
  if (!page) return res.status(400).json({ ok: false, error: `Unknown page "${body.page}"` });

  const form = {
    firstName: body.firstName, lastName: body.lastName, email: body.email,
    phone: body.phone, county: body.county, landStatus: body.landStatus,
    timeline: body.timeline, stage: body.stage, homePrice: body.homePrice,
    smsConsent: body.smsConsent === undefined ? undefined : Boolean(body.smsConsent && body.smsConsent !== 'false'),
  };
  const email = String(form.email || '').trim();
  const phoneDigits = String(form.phone || '').replace(/\D/g, '');
  if (!form.firstName || (!email && !phoneDigits)) {
    return res.status(400).json({ ok: false, error: 'First name and an email or phone are required' });
  }
  if (email && !EMAIL_RE.test(email)) return res.status(400).json({ ok: false, error: 'Email looks invalid' });
  if (phoneDigits && phoneDigits.length < 10) return res.status(400).json({ ok: false, error: 'Phone looks invalid' });

  let ghl;
  try { ghl = createGhlClient(); } catch (err) {
    console.error('[lead] config', err.message);
    return res.status(500).json({ ok: false, error: 'Integration not configured' });
  }

  const ctx = { ghl, page, form, meta: clientMeta(req, body) };
  try {
    await runPipeline(ctx);
  } catch (err) {
    console.error('[lead] pipeline failed', err.status || '', err.body || err.message);
    return res.status(502).json({ ok: false, error: 'Could not save your details. Please call us instead.' });
  }

  // Remember the contact for return-visit tracking (/api/track).
  setCookie(res, 'mh_cid', ctx.contact.id, 60 * 60 * 24 * 365);
  return res.status(200).json({ ok: true, contactId: ctx.contact.id, isNew: ctx.isNewContact, steps: ctx.log });
}
