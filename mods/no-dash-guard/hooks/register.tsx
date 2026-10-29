import type { Register } from 'claude-code'

// Kelly's rule: no dashes in any copy. Em and en dashes are never right in copy files; a spaced hyphen is
// checked only in fields that hold nothing but copy, since code uses " - " for subtraction.
const LONG_DASH = /[–—]/
const SPACED_HYPHEN = / - /
const COPY_FILES = /(^|\/)(campaigns|landing-pages|campaign-guide|design-dollars|home-portrait)\/|\.(md|html|txt)$/
const COPY_FIELDS = /^(subject|subjectLine|title|previewText|preview|text|message|body|caption|description|summary|content|headline|name)$/i
// Tools that load copy somewhere a person will read it.
const COPY_TOOLS = /^mcp__.*(email|template|blog|post|message|draft|page|social|caption|doc|canvas)/i

const hits = (text: string, re: RegExp) =>
  text
    .split('\n')
    .filter(line => re.test(line))
    .slice(0, 3)
    .map(line => line.trim().slice(0, 100))

export const register: Register = on => {
  on('tool.call', async ($, e, next) => {
    const found: string[] = []
    if (e.tool === 'Write' || e.tool === 'Edit') {
      const path = e.file_path
      const text = e.tool === 'Write' ? e.content : e.new_string
      if (COPY_FILES.test(path)) found.push(...hits(text, LONG_DASH))
    } else if (COPY_TOOLS.test(e.tool)) {
      for (const [key, value] of Object.entries(e as unknown as Record<string, unknown>)) {
        if (typeof value !== 'string') continue
        found.push(...hits(value, COPY_FIELDS.test(key) ? new RegExp(`${LONG_DASH.source}|${SPACED_HYPHEN.source}`) : LONG_DASH))
      }
    }
    if (found.length === 0) return next(e)

    $.ui.toast('Dash caught before it was saved')
    return {
      deny: `${$.plugin.name}: Kelly's copy has no dashes. Rewrite these lines with a comma, a period or "and", then try again:\n${found.map(l => `  ${l}`).join('\n')}`,
    }
  }).catch(($, e, next) => next(e))
}
