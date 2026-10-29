import type { Register } from 'claude-code'

// Tools that reach a real person: send, reply, forward, schedule, post, publish. Drafts and review queues stay open.
const SENDS = /send_message|send-a-new-message|send_invoice|send_estimate|send_payment|reply|forward|schedule_message|schedulepost|createscheduledpost|updatescheduledpost|social-media-posting_(create|edit)-post|blogs_(create|update)-blog-post|tiktok_publish|publish_project|publish_website|signature_request/i
const SAFE = /draft|forreview|for_review/i
// Builder Studio API calls made with curl that would send or publish.
const CURL_SENDS = /leadconnectorhq\.com\S*(conversations\/messages|social-media-posting|\/blogs\/posts|campaigns|workflows\/.+\/subscribe)/i
const SAY = ['to', 'email', 'phone', 'contactId', 'subject', 'title', 'message', 'text', 'channel', 'summary']

const STOP = 'Stop, keep it a draft'
const GO = 'Yes, send it now'

export const register: Register = on => {
  on('tool.call', async ($, e, next) => {
    const isBash = e.tool === 'Bash'
    const command = isBash ? String((e as { command?: unknown }).command ?? '') : ''
    const isSend = isBash
      ? /\bcurl\b/.test(command) && /-X\s*(POST|PUT)|--data|-d\s/.test(command) && CURL_SENDS.test(command)
      : e.tool.startsWith('mcp__') && SENDS.test(e.tool) && !SAFE.test(e.tool)
    if (!isSend) return next(e)

    const fields = e as unknown as Record<string, unknown>
    const detail = isBash
      ? command.slice(0, 160)
      : SAY.filter(k => typeof fields[k] === 'string' || typeof fields[k] === 'number')
          .map(k => `${k}: ${String(fields[k]).slice(0, 80)}`)
          .join(', ')
    const name = isBash ? 'a Builder Studio API call' : e.tool.replace(/^mcp__/, '').replace(/__/g, ' ')
    const answer = await $.ui
      .ask(`This would go to a real person: ${name}${detail ? ` (${detail})` : ''}. Send it?`, {
        header: 'Send?',
        options: [STOP, GO],
      })
      .catch(() => STOP)

    return answer === GO
      ? next(e)
      : { deny: `${$.plugin.name}: Kelly kept this as a draft. Nothing was sent. Save it as a draft instead, or ask her before trying again.` }
  }).catch(($, e, next) =>
    next.called ? next(e) : { deny: `${$.plugin.name}: the send check failed, so nothing was sent.` },
  )
}
