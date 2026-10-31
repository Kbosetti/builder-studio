// Receives a reviewer's answers from a content batch page and hands them to Kelly through Builder Studio:
// a note on Kelly's contact (the record) and an email to her (the notice). Deployed with the batch pages to
// https://mitchell-content-approval.vercel.app/api/submit. Env: HBS_PIT (Mitchell's private integration token),
// NOTIFY_CONTACT_IDS (comma separated contact ids that get the note and the email), EMAIL_FROM (optional).
const BASE = "https://services.leadconnectorhq.com";
const EMAIL_FROM = process.env.EMAIL_FROM || "info@send.mitchellhomesliving.com";
const VERDICTS = ["Approved", "Changes needed", "Not marked"];

function headers(version) {
  return {
    Authorization: `Bearer ${process.env.HBS_PIT}`,
    Version: version || "2021-07-28",
    "Content-Type": "application/json",
    Accept: "application/json",
    "User-Agent": "Mozilla/5.0 (compatible; MitchellContentApproval/1.0)"
  };
}

async function api(method, path, body, version) {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 8000);
  try {
    const r = await fetch(BASE + path, { method, headers: headers(version), body: body ? JSON.stringify(body) : undefined, signal: ctl.signal });
    const data = await r.json().catch(() => ({}));
    return { ok: r.ok, status: r.status, data };
  } catch (e) {
    return { ok: false, status: 0, data: { error: String(e) } };
  } finally {
    clearTimeout(timer);
  }
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const clip = (s, n) => String(s == null ? "" : s).trim().slice(0, n);

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return res.status(405).json({ ok: false, error: "Use POST" });
  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = null; } }
  if (!b || typeof b !== "object") return res.status(400).json({ ok: false, error: "No answers received" });
  if (b.website) return res.status(200).json({ ok: true });  // honeypot: bots fill every field

  const batch = parseInt(b.batch, 10);
  const name = clip(b.name, 80);
  const email = clip(b.email, 120);
  const items = Array.isArray(b.items) ? b.items.slice(0, 40).map(x => ({
    item: clip(x && x.item, 200), v: VERDICTS.includes(x && x.v) ? x.v : "Not marked", n: clip(x && x.n, 2000)
  })).filter(x => x.item) : [];
  if (!(batch >= 1 && batch <= 30)) return res.status(400).json({ ok: false, error: "Unknown batch" });
  if (name.length < 2) return res.status(400).json({ ok: false, error: "Please add your name" });
  if (!items.length) return res.status(400).json({ ok: false, error: "No pieces were marked" });

  const ids = (process.env.NOTIFY_CONTACT_IDS || "").split(",").map(s => s.trim()).filter(Boolean);
  if (!process.env.HBS_PIT || !ids.length) return res.status(500).json({ ok: false, error: "Sending is not set up yet" });
  if (b.dry === true) {  // health check: reads each notify contact, saves and sends nothing
    const t0 = Date.now();
    const looks = await Promise.all(ids.map(id => api("GET", `/contacts/${id}`)));
    return res.status(200).json({ ok: looks.every(x => x.ok), dry: true, ms: Date.now() - t0 });
  }

  const when = new Date().toLocaleString("en-US", { timeZone: "America/New_York", dateStyle: "full", timeStyle: "short" });
  const count = v => items.filter(x => x.v === v).length;
  const tally = `${count("Approved")} approved, ${count("Changes needed")} with changes, ${count("Not marked")} not marked`;
  const who = name + (email ? ` (${email})` : "");
  const test = /\btest\b/i.test(name);
  const subject = `${test ? "[Test] " : ""}Mitchell content Batch ${batch}: answers from ${name}`;
  const lines = [`Mitchell content Batch ${batch} answers from ${who}, ${when}.`, tally + ".", ""]
    .concat(items.map(x => `${x.item}: ${x.v}${x.n ? `\n   Notes: ${x.n}` : ""}`))
    .concat(["", `Page: https://mitchell-content-approval.vercel.app/batch-${batch}/`]);
  const rows = items.map(x => `<tr><td style="padding:8px 10px;border-top:1px solid #e3e6dc;vertical-align:top">${esc(x.item)}</td>` +
    `<td style="padding:8px 10px;border-top:1px solid #e3e6dc;vertical-align:top;font-weight:700;color:${x.v === "Approved" ? "#2b6d47" : x.v === "Changes needed" ? "#8a5a00" : "#777"}">${esc(x.v)}</td>` +
    `<td style="padding:8px 10px;border-top:1px solid #e3e6dc;vertical-align:top;white-space:pre-wrap">${esc(x.n)}</td></tr>`).join("");
  const html = `<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.5;color:#222;max-width:680px">
<p style="margin:0 0 6px;font-size:18px;font-weight:700;color:#1e4f33">Batch ${batch} answers from ${esc(who)}</p>
<p style="margin:0 0 14px;color:#555">${esc(when)} · ${esc(tally)}</p>
<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;width:100%;font-size:14px"><tr>
<th align="left" style="padding:6px 10px;background:#f1f5f2">Piece</th><th align="left" style="padding:6px 10px;background:#f1f5f2">Answer</th><th align="left" style="padding:6px 10px;background:#f1f5f2">Notes</th></tr>${rows}</table>
<p style="margin:16px 0 0"><a href="https://mitchell-content-approval.vercel.app/batch-${batch}/" style="color:#2b6d47;font-weight:700">Open the Batch ${batch} page</a></p></div>`;

  const results = await Promise.all(ids.map(contactId => Promise.all([
    api("POST", `/contacts/${contactId}/notes`, { body: lines.join("\n") }),
    api("POST", "/conversations/messages", { type: "Email", contactId, subject, html, emailFrom: EMAIL_FROM }, "2021-04-15")
  ])));
  let saved = 0, sent = 0;
  for (const [note, mail] of results) {
    if (note.ok) saved++; else console.error("note failed", note.status, JSON.stringify(note.data).slice(0, 300));
    if (mail.ok) sent++; else console.error("email failed", mail.status, JSON.stringify(mail.data).slice(0, 300));
  }
  if (!saved && !sent) return res.status(502).json({ ok: false, error: "Could not reach Builder Studio. Please use Copy my answers and email them to Kelly." });
  return res.status(200).json({ ok: true, saved, sent, at: when });
};
