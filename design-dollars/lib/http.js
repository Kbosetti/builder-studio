// Small helpers shared by the API routes.

export function allowedOrigins(env = process.env) {
  return (env.ALLOWED_ORIGINS || 'https://mitchell-design-dollars.vercel.app')
    .split(',').map((s) => s.trim()).filter(Boolean);
}

export function applyCors(req, res, env = process.env) {
  const origin = req.headers.origin;
  const list = allowedOrigins(env);
  if (origin && (list.includes('*') || list.includes(origin))) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

export async function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const raw = typeof req.body === 'string' ? req.body : await new Promise((resolve) => {
    let data = '';
    req.on('data', (c) => { data += c; });
    req.on('end', () => resolve(data));
  });
  const type = req.headers['content-type'] || '';
  if (type.includes('application/json')) { try { return JSON.parse(raw || '{}'); } catch { return {}; } }
  if (type.includes('application/x-www-form-urlencoded')) return Object.fromEntries(new URLSearchParams(raw));
  try { return JSON.parse(raw || '{}'); } catch { return {}; }
}

export function parseCookies(req) {
  return Object.fromEntries((req.headers.cookie || '').split(';').map((c) => {
    const i = c.indexOf('='); return i < 0 ? [c.trim(), ''] : [c.slice(0, i).trim(), decodeURIComponent(c.slice(i + 1))];
  }).filter(([k]) => k));
}

export function setCookie(res, name, value, maxAgeSec) {
  const prev = res.getHeader('Set-Cookie');
  const cookie = `${name}=${encodeURIComponent(value)}; Path=/; Max-Age=${maxAgeSec}; HttpOnly; Secure; SameSite=None`;
  res.setHeader('Set-Cookie', prev ? [].concat(prev, cookie) : cookie);
}

export function clientMeta(req, body) {
  const m = body.meta || {};
  return {
    pageUrl: String(m.pageUrl || '').slice(0, 500),
    referrer: String(m.referrer || '').slice(0, 500),
    utm: Object.fromEntries(Object.entries(m.utm || {}).filter(([k]) => /^utm_/.test(k)).map(([k, v]) => [k, String(v).slice(0, 120)])),
    visitorId: String(m.visitorId || '').slice(0, 64),
    userAgent: req.headers['user-agent'] || '',
    ip: (req.headers['x-forwarded-for'] || '').split(',')[0].trim(),
  };
}
