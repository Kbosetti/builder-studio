// Lead pipeline: an ordered list of steps that each receive and return a shared context.
// Add a step by appending to STEPS. A step that throws is logged and skipped unless it is marked critical.

import { GHL_FIELDS, LAND_ANSWERS, TIMELINE_ANSWERS, STAGE_ANSWERS } from './pages.js';
import { matchCounty } from './counties.js';

const clean = (v, max = 200) => String(v ?? '').trim().slice(0, max);

export function normalizePhone(raw) {
  const digits = String(raw || '').replace(/\D/g, '');
  if (digits.length === 10) return `+1${digits}`;
  if (digits.length === 11 && digits.startsWith('1')) return `+${digits}`;
  return digits ? `+${digits}` : '';
}

// 1. Shape the incoming submission into a GHL contact payload.
export const buildContact = {
  name: 'buildContact', critical: true,
  run(ctx) {
    const { form, page, meta } = ctx;
    const land = LAND_ANSWERS[form.landStatus] || null;
    const county = matchCounty(form.county);

    const customFields = [
      { id: GHL_FIELDS.personaSegment, field_value: page.persona.segment },
      { id: GHL_FIELDS.nurtureTrack, field_value: page.persona.nurtureTrack },
      { id: GHL_FIELDS.websiteFormType, field_value: page.formType },
      { id: GHL_FIELDS.sourcePageUrl, field_value: meta.pageUrl || page.url },
      { id: GHL_FIELDS.phoneCallOptIn, field_value: 'Opted In' },
    ];
    if (land) {
      customFields.push(
        { id: GHL_FIELDS.landStatus, field_value: land.landStatus },
        { id: GHL_FIELDS.landProcessStage, field_value: land.processStage },
        { id: GHL_FIELDS.hasLandWebsite, field_value: land.hasLand },
        { id: GHL_FIELDS.qualifiedLeadSignal, field_value: land.qualified },
        { id: GHL_FIELDS.adPlatformEvent, field_value: land.adEvent },
      );
    }
    if (county) customFields.push({ id: GHL_FIELDS.countyOfInterest, field_value: county });

    const timeline = TIMELINE_ANSWERS[form.timeline] || STAGE_ANSWERS[form.stage] || null;
    if (timeline?.timeline) customFields.push({ id: GHL_FIELDS.timeline, field_value: timeline.timeline });

    if (form.smsConsent !== undefined) {
      const optedIn = ['on', 'true', '1', 'yes'].includes(String(form.smsConsent).toLowerCase());
      customFields.push({ id: GHL_FIELDS.smsOptIn, field_value: optedIn ? 'Opted In' : 'Opted Out' });
    }
    if (form.homePrice) customFields.push({ id: GHL_FIELDS.budgetBracket, field_value: clean(form.homePrice, 40) });

    const tags = [...page.tags, page.persona.tag, ...(land ? land.tags : []), ...(timeline ? timeline.tags : [])];

    ctx.contactPayload = {
      firstName: clean(form.firstName, 80),
      lastName: clean(form.lastName, 80),
      email: clean(form.email, 120).toLowerCase(),
      phone: normalizePhone(form.phone),
      city: clean(form.county, 80),
      source: page.source,
      tags,
      customFields,
    };
    ctx.derived = { land, county, timeline };
    return ctx;
  },
};

// 2. Create or update the contact in GHL.
export const upsertContact = {
  name: 'upsertContact', critical: true,
  async run(ctx) {
    // Tags and source are handled after the upsert: sending tags in the upsert body replaces the
    // contact's existing tags, and we want first-touch source preserved on returning contacts.
    const { tags, source, ...fields } = ctx.contactPayload;
    const { contact, isNew } = await ctx.ghl.upsertContact(fields);
    ctx.contact = contact;
    ctx.isNewContact = isNew;
    await ctx.ghl.addTags(contact.id, tags);
    if (isNew || !contact.source) await ctx.ghl.updateContact(contact.id, { source });
    return ctx;
  },
};

// 3. Leave an audit note with the full submission and attribution.
export const addSubmissionNote = {
  name: 'addSubmissionNote', critical: false,
  async run(ctx) {
    const { form, page, meta, derived } = ctx;
    const lines = [
      `${page.name} submission (${ctx.isNewContact ? 'new contact' : 'existing contact updated'})`,
      `When: ${new Date().toISOString()}`,
      `Land: ${form.landStatus || 'not answered'}`,
      form.timeline ? `Timeline: ${form.timeline}` : null,
      form.stage ? `Stage: ${form.stage}` : null,
      form.smsConsent !== undefined ? `SMS consent: ${form.smsConsent ? 'yes' : 'no'}` : null,
      form.homePrice ? `Home price entered: ${form.homePrice}` : null,
      `County or city entered: ${form.county || ''}${derived.county ? ` (matched to ${derived.county})` : ''}`,
      `Persona: ${page.persona.segment}`,
      `Page URL: ${meta.pageUrl || page.url}`,
      meta.referrer ? `Referrer: ${meta.referrer}` : null,
      meta.utm && Object.keys(meta.utm).length ? `UTM: ${JSON.stringify(meta.utm)}` : null,
      meta.visitorId ? `Visitor ID: ${meta.visitorId}` : null,
      meta.userAgent ? `Device: ${meta.userAgent.slice(0, 160)}` : null,
    ].filter(Boolean);
    await ctx.ghl.addNote(ctx.contact.id, lines.join('\n'));
    return ctx;
  },
};

// 4. (Off by default) Create an opportunity in the page's pipeline if none is open for the contact.
export const createOpportunity = {
  name: 'createOpportunity', critical: false,
  async run(ctx) {
    const opp = ctx.page.opportunity;
    if (!opp?.enabled) return ctx;
    // A brand-new contact cannot have an opportunity yet, so skip the search (its index lags a few seconds).
    if (!ctx.isNewContact) {
      const existing = await ctx.ghl.searchOpportunities(ctx.contact.id).catch(() => null);
      const open = existing?.opportunities?.some((o) => o.status === 'open');
      if (open) { ctx.opportunity = { skipped: 'open opportunity exists' }; return ctx; }
    }
    const name = `${ctx.contactPayload.firstName} ${ctx.contactPayload.lastName} ${opp.nameSuffix}`.trim();
    ctx.opportunity = await ctx.ghl.createOpportunity({
      contactId: ctx.contact.id,
      pipelineId: opp.pipeline.id,
      pipelineStageId: opp.pipeline.newLeadStageId,
      name,
      source: ctx.page.source,
    });
    return ctx;
  },
};

export const STEPS = [buildContact, upsertContact, addSubmissionNote, createOpportunity];

export async function runPipeline(ctx, steps = STEPS) {
  ctx.log = ctx.log || [];
  for (const step of steps) {
    try {
      await step.run(ctx);
      ctx.log.push({ step: step.name, ok: true });
    } catch (err) {
      ctx.log.push({ step: step.name, ok: false, error: err.message, status: err.status, body: err.body });
      console.error(`[lead] step ${step.name} failed`, err.status || '', err.body || err.message);
      if (step.critical) throw err;
    }
  }
  return ctx;
}
