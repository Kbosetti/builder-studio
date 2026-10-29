import { expect, test } from 'claude-code/testing'

test('a send waits for Kelly, and a draft or a read goes straight through', async ($, on) => {
  const ran: string[] = []
  // Kelly closes the question without choosing: nothing may send.
  on('tool.call', { tool: 'AskUserQuestion' }, () => ({ deny: 'dismissed' }))
  on('tool.call', (_, e) => {
    ran.push(e.tool)
    return { result: {} }
  })

  const send = await $.tool.call({ tool: 'mcp__Gmail__send_message', to: 'buyer@example.com', subject: 'Hi' })
  expect(send.deny).toContain('Nothing was sent')

  const text = await $.tool.call({ tool: 'mcp__Homebuilder_Studio__conversations_send-a-new-message', contactId: 'c1' })
  expect(text.deny).toContain('Nothing was sent')

  const curl = await $.tool.call({ tool: 'Bash', command: 'curl -X POST https://services.leadconnectorhq.com/conversations/messages -d @m.json' })
  expect(curl.deny).toContain('Nothing was sent')

  await $.tool.call({ tool: 'mcp__Gmail__create_draft', to: 'buyer@example.com' })
  await $.tool.call({ tool: 'mcp__Homebuilder_Studio__blogs_get-blog-post', id: 'b1' })
  await $.tool.call({ tool: 'Bash', command: 'curl https://services.leadconnectorhq.com/emails/builder?locationId=x' })
  expect(ran).toEqual(['mcp__Gmail__create_draft', 'mcp__Homebuilder_Studio__blogs_get-blog-post', 'Bash'])
})
