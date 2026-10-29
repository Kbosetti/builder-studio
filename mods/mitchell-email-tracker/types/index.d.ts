export type EmailRow = {
  id: string
  series: string
  series_name: string
  send: string
  subject: string
  hold: string
  status: 'edited' | 'needs upload' | 'changes' | 'approved' | 'ready to proof'
  note: string
  uploaded: string
}

export type Snapshot = {
  emails: EmailRow[]
  stale: { name: string; why: string }[]
  checked: string
  error: string
}

export type Filter = 'all' | 'work' | 'holds'

declare module 'claude-code' {
  interface PluginState {
    'mitchell-email-tracker': {
      snapshot: Shaped<Snapshot>
      filter: Filter
    }
  }
}
