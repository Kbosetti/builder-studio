import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { EmailRow, Filter, Snapshot } from '../types'

const PANE = 'mitchell-emails'
const TITLE = 'Mitchell fall emails'
const STATUS_SCRIPT = 'campaigns/email/status.py'
// Change the tag when Snapshot's fields change: it declines what an earlier version stored.
const snapshot = atom({ plugin: 'mitchell-email-tracker', key: 'snapshot' } as const,
  { emails: [], stale: [], checked: '', error: '' }, { shape: 'snapshot-1' })
const filter = atom({ plugin: 'mitchell-email-tracker', key: 'filter' } as const, 'all' as Filter)

const NEEDS_WORK = new Set(['edited', 'needs upload', 'changes'])
const LABEL: Record<EmailRow['status'], string> = {
  edited: 'EDITED',
  'needs upload': 'UPLOAD',
  changes: 'CHANGES',
  approved: 'APPROVED',
  'ready to proof': 'PROOF',
}
const COLOR: Record<EmailRow['status'], string> = {
  edited: 'warning',
  'needs upload': 'warning',
  changes: 'error',
  approved: 'success',
  'ready to proof': 'suggestion',
}

const REBUILD = `Rebuild and publish every Mitchell fall page so they all match the email sources. Follow CLAUDE.md in order:
1. python3 campaigns/email/build.py (stop and tell me if it reports a dash).
2. Upload the changed emails to the Builder Studio drafts folder with campaigns/builder_studio/upload.py (drafts only, nothing sends).
3. Rebuild the kit, cadence, approval doc, master plan, events page and Builder Studio inventory.
4. Deploy the public copies and republish each Claude artifact to its existing link, with the files lists CLAUDE.md names.
5. Tell me in plain words what changed and anything that failed. Do not commit or push unless I ask.`

const UPLOAD = `Upload the Mitchell fall emails that changed to the Builder Studio drafts folder: run python3 campaigns/email/build.py, then campaigns/builder_studio/upload.py. Drafts only, nothing sends. Then tell me which templates were updated.`

let root = ''  // the repo, found once per load
let isRunning = false

async function refresh($: EngineInterface) {
  if (isRunning) return
  isRunning = true
  try {
    if (!root) {
      const top = await $.process.run(['git', 'rev-parse', '--show-toplevel'])
      root = top.stdout.trim()
    }
    const ran = await $.process.run(['python3', STATUS_SCRIPT], { cwd: root, timeoutMs: 60_000 })
    if (ran.exitCode !== 0) {
      await update($, snapshot, s => ({ ...s, error: ran.stderr.trim().split('\n').slice(-1)[0] ?? 'status check failed' }))
      return
    }
    const parsed = JSON.parse(ran.stdout) as Omit<Snapshot, 'error'>
    await update($, snapshot, () => ({ ...parsed, error: '' }))
    const work = parsed.emails.filter(e => NEEDS_WORK.has(e.status)).length
    $.ui.status(work || parsed.stale.length ? `Mitchell emails: ${work} need work, ${parsed.stale.length} pages behind` : undefined)
  } catch (err) {
    await update($, snapshot, s => ({ ...s, error: String(err).slice(0, 200) }))
  } finally {
    isRunning = false
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const started = await next(e)
    await $.command.register({ name: 'emails', description: 'Show where every Mitchell fall email stands' })
    void refresh($)

    return started
  })

  on('command.run', { command: 'emails' }, async $ => {
    await refresh($)
    await $.ui.open({ id: PANE, title: TITLE })

    return { text: 'Mitchell email tracker opened.' }
  })

  // Any edit, write or command may change a source or an output, so check again once it is done.
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    if (e.tool === 'Write' || e.tool === 'Edit' || e.tool === 'Bash') void refresh($)

    return ran
  }).catch(($, e, next) => next(e))

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const snap = await read($, snapshot)
    const show = await read($, filter)
    const width = Math.max(30, e.props.bodyColumns ?? 60)

    const counts = new Map<string, number>()
    for (const one of snap.emails) counts.set(one.status, (counts.get(one.status) ?? 0) + 1)
    const rows = snap.emails.filter(one =>
      show === 'all' ? true : show === 'work' ? NEEDS_WORK.has(one.status) : one.hold !== '')
    const series = [...new Set(rows.map(one => one.series_name))]

    const mark = async (one: EmailRow) => {
      const answer = await $.ui.ask(`What did Mitchell say about ${one.id.toUpperCase()}, "${one.subject}"?`,
        { header: 'Approval', options: ['Approved', 'Changes needed', 'Clear'] }).catch(() => '')
      const call = { Approved: 'approved', 'Changes needed': 'changes', Clear: 'clear' }[answer]
      if (!call) return
      await $.process.run(['python3', STATUS_SCRIPT, '--set', one.id, call], { cwd: root })
      await refresh($)
    }

    return (
      <Box flexDirection="column">
        <Text dimColor>
          {snap.emails.length} emails, checked {snap.checked || 'not yet'}
        </Text>
        {snap.error !== '' && <Text color="error">Status check failed: {snap.error}</Text>}
        <Text>
          {(Object.keys(LABEL) as EmailRow['status'][])
            .filter(s => counts.has(s))
            .map(s => `${LABEL[s]} ${counts.get(s)}`)
            .join('   ')}
        </Text>

        {snap.stale.length > 0 && (
          <Box flexDirection="column" marginTop={1}>
            <Text bold>Pages behind their sources</Text>
            {snap.stale.map(page => (
              <Text color="warning">
                {page.name}: {page.why}
              </Text>
            ))}
          </Box>
        )}

        <Box flexDirection="row" flexWrap="wrap" marginTop={1} gap={1}>
          <Button key="rebuild" variant="primary" onPress={() => void $.prompt.submit({ text: REBUILD })}>
            Rebuild and publish everything
          </Button>
          <Button key="upload" onPress={() => void $.prompt.submit({ text: UPLOAD })}>
            Upload changed emails
          </Button>
          <Button key="refresh" onPress={() => void refresh($)}>
            Check again
          </Button>
        </Box>

        <Box flexDirection="row" marginTop={1} gap={1}>
          {(['all', 'work', 'holds'] as const).map(f => (
            <Button key={`filter-${f}`} plain onPress={() => void update($, filter, () => f)}>
              <Text bold={show === f} dimColor={show !== f}>
                {{ all: 'All', work: 'Needs work', holds: 'On hold' }[f]}
              </Text>
            </Button>
          ))}
        </Box>

        {rows.length === 0 && <Text dimColor>Nothing here.</Text>}
        {series.map(name => (
          <Box flexDirection="column" marginTop={1}>
            <Text bold>{name}</Text>
            {rows
              .filter(one => one.series_name === name)
              .map(one => (
                <Button key={`row-${one.id}`} plain onPress={() => void mark(one)}>
                  <Text color={COLOR[one.status]}>{LABEL[one.status].padEnd(9)}</Text>
                  {one.id.toUpperCase().padEnd(5)}{' '}
                  {one.subject.slice(0, Math.max(10, width - 40))}
                  <Text dimColor>
                    {'  '}
                    {one.send}
                    {one.hold !== '' ? '  HOLD' : ''}
                    {one.note !== '' ? `  "${one.note}"` : ''}
                  </Text>
                </Button>
              ))}
          </Box>
        ))}
        <Text dimColor>Press an email to record Mitchell's call.</Text>
      </Box>
    )
  })
}
