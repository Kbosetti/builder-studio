import { expect, test } from 'claude-code/testing'

test('dashes in copy are stopped; code and clean copy pass', async ($, on) => {
  const ran: string[] = []
  on('tool.call', (_, e) => {
    ran.push(e.tool)
    return { result: {} }
  })

  const edit = await $.tool.call({ tool: 'Edit', file_path: '/repo/campaigns/email/series.py', old_string: 'a', new_string: 'Build on your land — with zero down' })
  expect(edit.deny).toContain('no dashes')

  const subject = await $.tool.call({ tool: 'mcp__Homebuilder_Studio__emails_create-template', subject: 'Your land - your home', html: '<p>x</p>' })
  expect(subject.deny).toContain('no dashes')

  await $.tool.call({ tool: 'Edit', file_path: '/repo/campaigns/email/build.py', old_string: 'a', new_string: 'n = total - 1' })
  await $.tool.call({ tool: 'Write', file_path: '/repo/campaigns/email/notes.md', content: 'Build on your land, with zero down.' })
  await $.tool.call({ tool: 'Edit', file_path: '/repo/scripts/tool.py', old_string: 'a', new_string: '# range 1–3' })
  expect(ran).toEqual(['Edit', 'Write', 'Edit'])
})
