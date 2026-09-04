// Thin GoHighLevel V2 API client. Reads credentials from environment variables only.
// Extend by adding methods here; keep request() as the single place that talks to GHL.

const BASE = process.env.GHL_BASE_URL || 'https://services.leadconnectorhq.com';
const VERSION = process.env.GHL_API_VERSION || '2021-07-28';

export class GhlError extends Error {
  constructor(message, status, body) {
    super(message);
    this.name = 'GhlError';
    this.status = status;
    this.body = body;
  }
}

export function createGhlClient(env = process.env) {
  const token = env.GHL_PRIVATE_TOKEN;
  const locationId = env.GHL_LOCATION_ID;
  if (!token || !locationId) {
    throw new Error('GHL_PRIVATE_TOKEN and GHL_LOCATION_ID must be set');
  }

  async function request(method, path, body, attempt = 0) {
    const res = await fetch(`${BASE}${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        Version: VERSION,
        Accept: 'application/json',
        ...(body ? { 'Content-Type': 'application/json' } : {}),
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if ((res.status === 429 || res.status >= 500) && attempt < 3) {
      const delay = 400 * 2 ** attempt + Math.random() * 250;
      await new Promise((r) => setTimeout(r, delay));
      return request(method, path, body, attempt + 1);
    }

    const text = await res.text();
    let json = null;
    try { json = text ? JSON.parse(text) : null; } catch { json = { raw: text }; }
    if (!res.ok) {
      throw new GhlError(`GHL ${method} ${path} -> ${res.status}`, res.status, json);
    }
    return json;
  }

  return {
    locationId,
    request,

    /** Create-or-update by email/phone. Returns { contact, new } */
    async upsertContact(fields) {
      const out = await request('POST', '/contacts/upsert', { locationId, ...fields });
      return { contact: out.contact, isNew: Boolean(out.new) };
    },

    async updateContact(contactId, fields) {
      return request('PUT', `/contacts/${contactId}`, fields);
    },

    async addTags(contactId, tags) {
      if (!tags?.length) return null;
      return request('POST', `/contacts/${contactId}/tags`, { tags });
    },

    async addNote(contactId, body) {
      return request('POST', `/contacts/${contactId}/notes`, { body });
    },

    /** Future step: create an opportunity in a pipeline stage. */
    async createOpportunity({ contactId, pipelineId, pipelineStageId, name, monetaryValue, status = 'open', source }) {
      return request('POST', '/opportunities/', {
        locationId, contactId, pipelineId, pipelineStageId, name, monetaryValue, status, source,
      });
    },

    async searchOpportunities(contactId) {
      return request('GET', `/opportunities/search?location_id=${locationId}&contact_id=${contactId}`);
    },
  };
}
