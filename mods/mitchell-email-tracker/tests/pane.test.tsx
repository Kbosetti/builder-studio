import { expect, test } from 'claude-code/testing'

const PANE = {
  plugin: 'mitchell-email-tracker',
  component: 'Pane',
  requestId: 'mitchell-emails',
  props: { title: 'Mitchell fall emails', isFocused: false, bodyColumns: 70, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} },
} as const

const STATUS = {
  emails: [
    { id: 'hp1', series: 'portrait', series_name: 'The Home Portrait', send: 'Thursday, October 22', subject: 'What would your home look like?', hold: '', status: 'edited', note: '', uploaded: '' },
    { id: 'dd3', series: 'designdollars', series_name: 'Design Dollars', send: 'Tuesday, November 3', subject: 'Locked in', hold: 'Waits on Mitchell', status: 'approved', note: '', uploaded: '2026-10-29 10:00' },
  ],
  stale: [{ name: 'Review kit', why: 'older than emails.json' }],
  checked: '10:05',
}

test('the pane shows each email, its status and the pages behind, on every surface', async ($, on) => {
  on('command.register', () => ({ value: { command: 'emails' } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  on('process.run', (_, e) => ({
    value: e.argv[0] === 'git'
      ? { exitCode: 0, stdout: '/repo\n', stderr: '', isStdoutTruncated: false, isStderrTruncated: false }
      : { exitCode: 0, stdout: JSON.stringify(STATUS), stderr: '', isStdoutTruncated: false, isStderrTruncated: false },
  }))

  await $.session.start({ cwd: '/repo', surface: 'desktop', isInteractive: true })
  await $.command.run({ command: 'emails', args: '' })

  for (const surface of ['terminal', 'desktop', 'vscode', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect(await ui.find({ type: 'Text', text: /Review kit: older than emails.json/ })).toBeDefined()
    expect(await ui.find({ key: 'row-hp1' })).toBeDefined()
    expect(await ui.find({ key: 'rebuild' })).toBeDefined()
    await ui.press({ key: 'filter-work' })
    expect(await ui.find({ key: 'row-dd3' })).toBeUndefined()
    await ui.press({ key: 'filter-all' })
    await ui.unmount()
  }
})
