// Home Portrait intake, version two (September 2026).
// Receives the quiz payload from the same domain, upserts a contact in
// Builder Studio with custom fields and tags, writes the quiz note,
// creates or updates the opportunity in the division pipeline, and sends
// the portrait email with the link to the personalized presentation and
// the matching portrait document. The integration token lives in Vercel
// env vars, never in the browser.
//
// Env vars (unchanged from July): HBS_PIT, HBS_LOCATION_ID,
// optional EMAIL_PROVIDER=gmail with GMAIL_USER and GMAIL_APP_PASSWORD.
const BASE = "https://services.leadconnectorhq.com";

// Opportunity custom field IDs (model: opportunity), created July 2026.
// The four September fields (region, home_intent, selection_appetite,
// portrait_name) were created in the account on September 4, 2026 and are
// written to both the contact and the opportunity.
const OPP_FIELDS = {
  persona_segment: "YAbz66mcBmEHn9H7Wi1E",
  land_status: "pUlJE1FOdRTbTXhY7P0T",
  timeline: "bYcu0QYEocQVq2D3Rckt",
  style_preference: "e2Ye7Jzw8ShV5PP7EU4P",
  must_have_spaces: "h9aju5NIsxcc0MGKwrQj",
  qualified_lead_signal: "woqbKLwtJKFciNDyqQuY",
  quiz_submitted_at: "vawmYa0Vuah9ypLdk0KN",
  region: "uSnPQrmupBeVotpCqdOQ",
  home_intent: "xGOnZobp613pvo4aOLZc",
  selection_appetite: "4CrQDEDiUxNrcLR6n4Ic",
  portrait_name: "FbKWoNRebNSVYAEPtkKp"
};

const ILLUSTRATIVE_VALUE = 389000;
const SITE = process.env.SITE_URL || "https://mitchell-home-portrait-quiz-cea-marketing.vercel.app";
const LOGO = "https://assets.cdn.filesafe.space/5o5zLlUPPizy6Ajp61oF/media/8f411080-4033-4bae-81e3-fd4fa4ea1aa1.png";

// Persona and land status -> the matching portrait document (sample shells).
// The Gathering Place has one document regardless of land status.
const SHELL_PDF = {
  "The Value Unlocker": ["landownerhasland", "landownerneedsland"],
  "The Planner": ["plannerhasland", "plannerneedsland"],
  "The Transitioner": ["familyhasland", "familyneedsland"],
  "The Grounded Dreamer": ["dreamerhasland", "dreamerneedsland"],
  "The Gathering Place": ["gatheringplace", "gatheringplace"]
};

// Hosted portrait documents. Fill a URL here to serve the document from the
// Mitchell media library; any shell without an entry falls back to SITE/pdf/.
const PDF_URLS = {
  landownerhasland: "", landownerneedsland: "",
  plannerhasland: "", plannerneedsland: "",
  familyhasland: "", familyneedsland: "",
  dreamerhasland: "", dreamerneedsland: "",
  gatheringplace: ""
};

const PORTRAIT_NAMES = {
  "The Value Unlocker": "The Landowner's Portrait",
  "The Planner": "The Planner's Portrait",
  "The Transitioner": "The Family Portrait",
  "The Grounded Dreamer": "The Dreamer's Portrait",
  "The Gathering Place": "The Gathering Place Portrait"
};

const DIVISION_STUDIO = {
  "Richmond, VA": "Richmond Design Studio",
  "Fredericksburg, VA": "Fredericksburg Design Studio",
  "Newport News, VA": "Newport News Design Studio",
  "Raleigh, NC": "Raleigh Design Studio",
  "Wilmington, NC": "Wilmington Design Studio"
};

function portraitEmail(p, firstName, presUrl, pdfUrl) {
  const hi = firstName ? `${firstName}, your` : "Your";
  const portrait = PORTRAIT_NAMES[p.persona_segment] || "Your Home Portrait";
  const owns = p.land_status === "owned" || p.land_status === "family";
  const studio = DIVISION_STUDIO[p.division] || "Design Studio";
  const pick = Array.isArray(p.must_have_spaces) && p.must_have_spaces.length ? p.must_have_spaces[0] : "the spaces you described";
  const simply = p.persona_segment === "The Gathering Place"
    ? "The second home banks make hard, Mitchell makes simple. Because Mitchell self funds every build, the construction loan never exists, even when the address is not your primary one."
    : owns
      ? "Your land can be your down payment. Zero down, zero closing costs, no construction loan, because Mitchell self funds every build."
      : "No land yet? You are closer than you think. Zero down, zero closing costs, no construction loan, and our team helps you evaluate every lot before you buy.";
  return `
  <div style="background:#faf8f3;padding:34px 16px;font-family:Georgia,serif;">
    <div style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #e3ded2;border-radius:8px;overflow:hidden;">
      <div style="background:#1e4f33;padding:26px 30px;text-align:center;">
        <img src="${LOGO}" alt="Mitchell Homes" width="86" style="display:block;margin:0 auto 10px;width:86px;height:auto;">
        <div style="color:#ffffff;font-size:26px;font-style:italic;">${hi} Home Portrait is painted.</div>
        <div style="color:#f5d053;font-size:13px;letter-spacing:2px;text-transform:uppercase;margin-top:8px;font-family:Arial,sans-serif;">${portrait}</div>
      </div>
      <div style="padding:30px;">
        <p style="font-size:15px;line-height:1.7;color:#333b36;margin:0 0 16px;">Every home we build is a portrait of its owner. Yours is ready: the home only you would build, the land it belongs on, the spaces shaped around your answers, and the clearest path to building it.</p>
        <div style="text-align:center;margin:26px 0;">
          <a href="${presUrl}" style="background:#2b6d47;color:#ffffff;text-decoration:none;padding:15px 34px;border-radius:4px;font-family:Arial,sans-serif;font-size:14px;letter-spacing:1px;font-weight:bold;">VIEW MY PORTRAIT</a>
        </div>
        <p style="font-size:14px;line-height:1.7;color:#333b36;margin:0 0 14px;">${simply}</p>
        <p style="font-size:14px;line-height:1.7;color:#333b36;margin:0 0 14px;border-left:3px solid #b8860b;padding-left:14px;"><b style="color:#1e4f33;">And the finish is funded too.</b> Every Mitchell home comes with $5,000 in Design Dollars for the Design Center, and the more you personalize, the more we add, up to $25,000. The ${pick} you chose is exactly where Design Dollars work. Sign now and the incentive is locked; your tier is decided when you make your selections.</p>
        <p style="font-size:13px;line-height:1.6;color:#6d746f;text-align:center;margin:0 0 6px;">${pdfUrl ? `Prefer to keep a copy? <a href="${pdfUrl}" style="color:#2b6d47;">Download your portrait document</a>.` : ""}</p>
        <p style="font-size:13px;line-height:1.6;color:#6d746f;text-align:center;margin:14px 0 0;">Bring this portrait to the ${studio}. Your New Home Consultant starts from it, not from zero.</p>
        <p style="font-size:11px;line-height:1.6;color:#9aa39c;text-align:center;margin:18px 0 0;">Zero down, zero closing costs, no construction loan, on approved terms. Design Dollars apply to Design Center selections only, not to base price, structural options, or site work, and are not redeemable for cash; tier determined at selections. Program effective September 1, 2026. Sample document shows an illustrative buyer.</p>
      </div>
    </div>
  </div>`;
}

function headers(version) {
  return {
    Authorization: `Bearer ${process.env.HBS_PIT}`,
    Version: version || "2021-07-28",
    "Content-Type": "application/json",
    Accept: "application/json",
    "User-Agent": "Mozilla/5.0 (compatible; HomePortraitIntake/2.0)"
  };
}

async function api(method, path, body, version) {
  const r = await fetch(BASE + path, { method, headers: headers(version), body: body ? JSON.stringify(body) : undefined });
  const data = await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, data };
}

let pipelineCache = null;
async function resolvePipeline(division) {
  if (!division) return null;
  if (!pipelineCache) {
    const r = await api("GET", `/opportunities/pipelines?locationId=${process.env.HBS_LOCATION_ID}`);
    if (!r.ok) return null;
    pipelineCache = r.data.pipelines || [];
  }
  const div = division.toLowerCase();
  const pipeline = pipelineCache.find(p => p.name.toLowerCase() === div) ||
    pipelineCache.find(p => div.indexOf(p.name.toLowerCase().split(",")[0]) > -1);
  if (!pipeline) return null;
  const stage = (pipeline.stages || []).slice().sort((a, b) => a.position - b.position)[0];
  return stage ? { pipelineId: pipeline.id, stageId: stage.id } : null;
}

function presentationUrl(p, firstName) {
  const q = new URLSearchParams({
    n: firstName || "", p: p.persona_segment || "", d: p.division || "", l: p.land_status || "",
    s: p.style_preference || "", k: (p.must_have_spaces || []).join("|"), t: p.timeline || "",
    r: p.region || "", i: p.home_intent || "", x: p.rset || ""
  });
  return `${SITE}/fullportrait?${q.toString()}`;
}

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ ok: false, error: "POST only" }); return; }
  if (!process.env.HBS_PIT || !process.env.HBS_LOCATION_ID) {
    res.status(200).json({ ok: false, skipped: "integration not configured on this deployment" });
    return;
  }
  const p = req.body || {};
  const email = (p.email || "").trim();
  if (!email || email === "(not provided)") { res.status(200).json({ ok: true, skipped: "no email" }); return; }
  const firstName = (p.first_name && p.first_name !== "(not provided)") ? p.first_name : undefined;
  const qualified = p.qualified_lead_signal === true || p.qualified_lead_signal === "true";
  const hasLand = p.land_status === "owned" || p.land_status === "family";
  const portraitName = PORTRAIT_NAMES[p.persona_segment] || "";

  // ---- 1. Contact upsert ----
  const contactFields = [];
  const addC = (key, v) => { if (v !== undefined && v !== null && v !== "") contactFields.push({ key, field_value: v }); };
  addC("persona_segment", p.persona_segment);
  addC("portrait_name", portraitName);
  addC("land_status", p.land_status);
  addC("division", p.division);
  addC("region", p.region);
  addC("home_intent", p.home_intent);
  addC("style_preference", p.style_preference);
  if (Array.isArray(p.must_have_spaces) && p.must_have_spaces.length) addC("must_have_spaces", p.must_have_spaces);
  addC("selection_appetite", p.selection_appetite);
  addC("design_dollars_focus", p.design_dollars_focus);
  addC("timeline", p.timeline);
  addC("qualified_lead_signal", String(qualified));
  addC("nurture_track", p.nurture_track);
  addC("ad_platform_event", p.ad_platform_event);
  if (p.persona_scores) addC("persona_scores", JSON.stringify(p.persona_scores));
  addC("quiz_submitted_at", p.submitted_at);
  addC("quiz_source", p.source);

  const tags = [
    p.persona_segment,
    p.land_status ? "land " + p.land_status : null,
    p.division,
    p.region && p.region !== p.division ? "region " + p.region : null,
    p.home_intent && p.home_intent !== "everyday" ? "intent " + p.home_intent : null,
    p.timeline ? "timeline " + p.timeline : null,
    p.selection_appetite ? "selections " + p.selection_appetite : null,
    "home portrait quiz"
  ].filter(Boolean);
  if (qualified) tags.push("qualified lead");

  const out = { ok: true };
  try {
    const up = await api("POST", "/contacts/upsert", {
      locationId: process.env.HBS_LOCATION_ID, email, firstName,
      source: p.source || "home_portrait_quiz", tags, customFields: contactFields
    });
    if (!up.ok) { res.status(200).json({ ok: false, step: "contact", status: up.status, error: up.data }); return; }
    const contactId = up.data.contact && up.data.contact.id;
    out.contactId = contactId; out.isNewContact = up.data.new;

    // ---- 1b. Quiz results note on the contact profile ----
    if (contactId) {
      try {
        const scores = p.persona_scores || {};
        const noteLines = [
          "HOME PORTRAIT QUIZ RESULTS",
          "",
          "Portrait: " + (portraitName || "unknown"),
          "Persona: " + (p.persona_segment || "unknown"),
          "Land status: " + (p.land_status || "unknown"),
          "Division: " + (p.division || "unknown"),
          "Region: " + (p.region || "unknown"),
          "Home intent: " + (p.home_intent || "everyday"),
          "Timeline to keys: " + (p.timeline || "unknown"),
          "Style: " + (p.style_preference || "unknown"),
          "Must have spaces: " + ((p.must_have_spaces || []).join(", ") || "none selected"),
          "Selection appetite: " + (p.selection_appetite || "unknown") + " (Design Dollars focus: " + (p.design_dollars_focus || "none") + ")",
          "Qualified lead: " + (qualified ? "YES, owns or has family land with a near term timeline" : "not yet, nurture track"),
          "Nurture sequence: " + (p.nurture_track || "unknown"),
          "Ad platform event: " + (p.ad_platform_event || "unknown"),
          "Persona scores: Planner " + (scores.P ?? 0) + ", Transitioner " + (scores.T ?? 0) + ", Value Unlocker " + (scores.V ?? 0) + ", Grounded Dreamer " + (scores.D ?? 0),
          "Submitted: " + (p.submitted_at || "unknown")
        ];
        const note = await api("POST", `/contacts/${contactId}/notes`, { body: noteLines.join("\n") });
        out.noteAdded = note.ok;
      } catch (e) { out.noteAdded = false; }
    }

    // ---- 2. Portrait email: personalized presentation link plus the matching document ----
    if (contactId && SHELL_PDF[p.persona_segment]) {
      try {
        const shell = SHELL_PDF[p.persona_segment][hasLand ? 0 : 1];
        let pdfUrl = PDF_URLS[shell] || `${SITE}/pdf/${shell}.pdf`;
        // Only attach the document if it is actually hosted; the link in the body is dropped otherwise.
        try { const head = await fetch(pdfUrl, { method: "HEAD" }); if (!head.ok) pdfUrl = ""; } catch (e) { pdfUrl = ""; }
        const presUrl = presentationUrl(p, firstName);
        const subject = firstName ? `${firstName}, your Home Portrait is ready` : "Your Home Portrait is ready";
        const html = portraitEmail(p, firstName, presUrl, pdfUrl);
        const useGmail = process.env.EMAIL_PROVIDER === "gmail" && process.env.GMAIL_USER && process.env.GMAIL_APP_PASSWORD;
        if (useGmail) {
          const nodemailer = require("nodemailer");
          const transporter = nodemailer.createTransport({ host: "smtp.gmail.com", port: 465, secure: true, auth: { user: process.env.GMAIL_USER, pass: process.env.GMAIL_APP_PASSWORD } });
          let attachments = [];
          if (pdfUrl) { try { const pr = await fetch(pdfUrl); if (pr.ok) attachments = [{ filename: "Your Home Portrait.pdf", content: Buffer.from(await pr.arrayBuffer()) }]; } catch (e) {} }
          await transporter.sendMail({ from: `Mitchell Homes <${process.env.GMAIL_USER}>`, to: email, subject, html, attachments });
          out.emailQueued = true; out.emailProvider = "gmail";
          try { await api("POST", `/contacts/${contactId}/notes`, { body: "Home Portrait email sent to " + email + " with the presentation link" + (pdfUrl ? " and the matching portrait document attached." : ".") }); } catch (e) {}
        } else {
          const body = { type: "Email", contactId, subject, html };
          if (pdfUrl) body.attachments = [pdfUrl];
          const mail = await api("POST", "/conversations/messages", body, "2021-04-15");
          out.emailQueued = mail.ok; out.emailProvider = "platform";
          if (!mail.ok) out.emailError = mail.data;
        }
      } catch (e) { out.emailQueued = false; out.emailError = String(e); }
    }

    // ---- 3. Opportunity in the division pipeline ----
    const route = await resolvePipeline(p.division);
    if (!route || !contactId) { out.opportunity = "skipped: no pipeline match for division " + (p.division || "(none)"); res.status(200).json(out); return; }
    const oppFields = [];
    const addO = (key, v) => { if (OPP_FIELDS[key] && v !== undefined && v !== null && v !== "") oppFields.push({ id: OPP_FIELDS[key], field_value: v }); };
    addO("persona_segment", p.persona_segment);
    addO("land_status", p.land_status);
    addO("timeline", p.timeline);
    addO("style_preference", p.style_preference);
    if (Array.isArray(p.must_have_spaces) && p.must_have_spaces.length) addO("must_have_spaces", p.must_have_spaces);
    addO("qualified_lead_signal", String(qualified));
    addO("quiz_submitted_at", p.submitted_at);
    addO("region", p.region);
    addO("home_intent", p.home_intent);
    addO("selection_appetite", p.selection_appetite);
    addO("portrait_name", portraitName);

    const oppName = "Home Portrait | " + (firstName || email) + (portraitName ? " | " + portraitName : "");
    const search = await api("GET", `/opportunities/search?location_id=${process.env.HBS_LOCATION_ID}&contact_id=${contactId}`);
    const existing = ((search.ok && search.data.opportunities) || []).find(o => o.pipelineId === route.pipelineId && o.status === "open");
    if (existing) {
      const upd = await api("PUT", `/opportunities/${existing.id}`, { name: oppName, pipelineId: route.pipelineId, pipelineStageId: route.stageId, status: "open", monetaryValue: ILLUSTRATIVE_VALUE, customFields: oppFields });
      out.opportunityId = existing.id; out.opportunityUpdated = upd.ok; if (!upd.ok) out.opportunityError = upd.data;
    } else {
      const crt = await api("POST", "/opportunities/", { locationId: process.env.HBS_LOCATION_ID, pipelineId: route.pipelineId, pipelineStageId: route.stageId, contactId, name: oppName, status: "open", monetaryValue: ILLUSTRATIVE_VALUE, customFields: oppFields });
      out.opportunityId = crt.data.opportunity && crt.data.opportunity.id; out.opportunityCreated = crt.ok; if (!crt.ok) out.opportunityError = crt.data;
    }
    res.status(200).json(out);
  } catch (e) {
    res.status(200).json({ ok: false, error: String(e) });
  }
};
