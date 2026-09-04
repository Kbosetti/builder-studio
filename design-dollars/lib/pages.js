// Landing page registry. One entry per page (or per variant). Adding a new landing page = add an entry here
// and set data-page="<key>" on its form. Everything the pipeline needs to attribute and tag a lead lives here.

export const GHL_FIELDS = {
  personaSegment: 'MpgBUOsBEwwPggf2tW7o',   // Persona Segment (single option)
  nurtureTrack: 'WA8UU2i2cdmIIZmOOIGb',     // Nurture Track (single option)
  landStatus: 'cmmUk59B9gxkJFtHXYnl',       // Land Status: owned | family | searching | dreaming
  landProcessStage: '38vGuirv93K3fXh7XY1R', // Land Process Stage
  hasLandWebsite: 'hzQx4ZpbFWd3XvPxfQVe',   // Has Land Website: Yes | No
  sourcePageUrl: '9RmEfRn3CcxHxLNmuHHg',    // Source Page URL (text)
  websiteFormType: 'nSxE2vLaTaQJMmdAMzPM',  // Website Form Type: OSC | Contact | Download | RSVP | Referral | Vendor
  countyOfInterest: 'c8B2d5tXqTmicZQFNatt', // County of Interest (picklist, see counties.js)
  qualifiedLeadSignal: '9BeKxpKzp1vG9WH049T9', // 'true' | 'false'
  adPlatformEvent: 'GPWtXqs85WK8PYpANGgR',  // qualified_lead_landowner | lead_engaged
  phoneCallOptIn: 'J6bZz5p5arE6A5DiwEeb',   // Opted In | Opted Out | Unknown
  smsOptIn: 'auIysKo72FTRmpUaGd8l',         // Opted In | Opted Out | Unknown
  timeline: 'y5uwMcdTlpNcElX1PkId',         // 0 to 6 months | 6 to 12 months | 12 to 24 months | exploring
  budgetBracket: '5Kh4sPR9awuN0hNhithS',    // free text
};

// Pipelines available in the account (for the opportunity step when it is switched on).
export const PIPELINES = {
  osc: { id: 'SqOpD7nz9dzJNDwPYbSV', newLeadStageId: '5ccccff0-2d4d-41c9-a403-e38dd7dd41c9' },
};

const PERSONAS = {
  valueUnlocker: {
    segment: 'The Value Unlocker',
    tag: 'the value unlocker',
    nurtureTrack: 'the_value_unlocker_sequence',
  },
  planner: { segment: 'The Planner', tag: 'the planner', nurtureTrack: 'the_planner_sequence' },
  transitioner: { segment: 'The Transitioner', tag: 'the transitioner', nurtureTrack: 'the_transitioner_sequence' },
  groundedDreamer: { segment: 'The Grounded Dreamer', tag: 'the grounded dreamer', nurtureTrack: 'the_grounded_dreamer_sequence' },
};

export const PAGES = {
  'design-dollars': {
    key: 'design-dollars',
    name: 'Mitchell Design Dollars Landing Page',
    url: 'https://mitchell-design-dollars.vercel.app/',
    source: 'Design Dollars Landing Page',
    persona: PERSONAS.valueUnlocker,
    formType: 'OSC',
    tags: ['design dollars landing page', 'landing page lead'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Design Dollars' },
  },
  'design-dollars-nhi': {
    key: 'design-dollars-nhi',
    name: 'Mitchell Design Dollars Landing Page (NHI)',
    url: 'https://mitchell-design-dollars.vercel.app/nhi-index',
    source: 'Design Dollars Landing Page NHI',
    persona: PERSONAS.valueUnlocker,
    formType: 'OSC',
    tags: ['design dollars landing page', 'design dollars nhi', 'landing page lead'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Design Dollars NHI' },
  },

  // ---- cea-mitchell-landing-pages project (August concepts). Plan guide forms. ----
  'lp-calculator': {
    key: 'lp-calculator', name: 'Land Savings Calculator Page', url: 'https://cea-mitchell-landing-pages.vercel.app/calculator.html',
    source: 'Land Savings Calculator Page', persona: PERSONAS.valueUnlocker, formType: 'Download',
    tags: ['landing page lead', 'land savings calculator page', 'plan guide requested'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Land Calculator' },
  },
  'lp-math': {
    key: 'lp-math', name: 'Two Ways to Build (Math) Page', url: 'https://cea-mitchell-landing-pages.vercel.app/math.html',
    source: 'Two Ways to Build Page', persona: PERSONAS.valueUnlocker, formType: 'Download',
    tags: ['landing page lead', 'two ways to build page', 'plan guide requested'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Two Ways to Build' },
  },
  'lp-land': {
    key: 'lp-land', name: 'Your Land Is Worth More Page', url: 'https://cea-mitchell-landing-pages.vercel.app/land.html',
    source: 'Your Land Landing Page', persona: PERSONAS.valueUnlocker, formType: 'Download',
    tags: ['landing page lead', 'your land landing page', 'plan guide requested'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Your Land' },
  },
  'lp-no-land': {
    key: 'lp-no-land', name: 'No Land Yet Page', url: 'https://cea-mitchell-landing-pages.vercel.app/no-land.html',
    source: 'No Land Yet Landing Page', persona: PERSONAS.planner, formType: 'Download',
    tags: ['landing page lead', 'no land yet landing page', 'plan guide requested'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'No Land Yet' },
  },
  'lp-dreamer': {
    key: 'lp-dreamer', name: 'Dreamer Page (Virginia and Maryland)', url: 'https://cea-mitchell-landing-pages.vercel.app/dreamer.html',
    source: 'Dreamer Landing Page', persona: PERSONAS.groundedDreamer, formType: 'Download',
    tags: ['landing page lead', 'dreamer landing page', 'plan guide requested'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Dreamer' },
  },
  'lp-dreamer-carolinas': {
    key: 'lp-dreamer-carolinas', name: 'Dreamer Page (Carolinas)', url: 'https://cea-mitchell-landing-pages.vercel.app/dreamer-carolinas.html',
    source: 'Dreamer Carolinas Landing Page', persona: PERSONAS.groundedDreamer, formType: 'Download',
    tags: ['landing page lead', 'dreamer landing page', 'dreamer carolinas', 'plan guide requested'],
    opportunity: { enabled: true, pipeline: PIPELINES.osc, nameSuffix: 'Dreamer Carolinas' },
  },
};

export function resolvePage(key) {
  return PAGES[key] || null;
}

// Maps the "Do you already own your land?" select to GHL fields and tags.
export const LAND_ANSWERS = {
  'Yes, I own it': {
    landStatus: 'owned', processStage: 'Owns Land Outright', hasLand: 'Yes',
    tags: ['land owned'], qualified: 'true', adEvent: 'qualified_lead_landowner',
  },
  'It is under contract': {
    landStatus: 'owned', processStage: 'Offer Made', hasLand: 'Yes',
    tags: ['land owned', 'land under contract'], qualified: 'true', adEvent: 'qualified_lead_landowner',
  },
  'Not yet, I am still looking': {
    landStatus: 'searching', processStage: 'Actively Looking', hasLand: 'No',
    tags: ['land searching'], qualified: 'false', adEvent: 'lead_engaged',
  },
};
LAND_ANSWERS['Still looking for land'] = LAND_ANSWERS['Not yet, I am still looking'];

// "When are you looking to build" -> Timeline field + existing timeline tags.
export const TIMELINE_ANSWERS = {
  'Within 6 months': { timeline: '0 to 6 months', tags: ['timeline 0 to 6 months'] },
  '6 to 12 months': { timeline: '6 to 12 months', tags: ['timeline 6 to 12 months'] },
  'More than 12 months': { timeline: '12 to 24 months', tags: ['timeline 12 to 24 months'] },
  'Still deciding': { timeline: 'exploring', tags: ['timeline exploring'] },
};

// "How far along are you" (dreamer pages) -> buying stage tags; "just starting" also sets Timeline = exploring.
export const STAGE_ANSWERS = {
  'Just starting to explore': { timeline: 'exploring', tags: ['timeline exploring', 'stage just starting'] },
  'Comparing builders': { tags: ['stage comparing builders'] },
  'Ready to pick a plan': { tags: ['stage ready to pick a plan'] },
};
