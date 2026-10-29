# Claude Code mods for the Mitchell fall campaign

Three mods that run inside a Claude Code session while we work on the campaign. They change nothing in Builder Studio on their own.

* **mitchell-email-tracker**: type `/emails` for a pane listing every fall email with its status (edited, needs upload, ready to proof, approved, changes), the review pages that are behind their sources, and buttons to upload the changed emails, rebuild and publish everything, or record Mitchell's call on an email. It reads `campaigns/email/status.py`; approvals are kept in `campaigns/email/approvals.json`.
* **drafts-only-lock**: anything that would send, text, schedule, post or publish to a real person stops and asks Kelly first. Drafts and reads pass.
* **no-dash-guard**: copy with an em dash, an en dash, or a spaced hyphen in a subject or headline is stopped before it is saved or loaded anywhere.

## Turning them on in a new session

Cloud sessions start from a fresh container, so the mods have to be loaded each time. Ask Claude: "load the mods from the mods folder". Claude copies each folder into the session's mods folder, and Claude Code asks once whether to turn them on.

## Changing a mod

Edit it in the session's mods folder (it reloads by itself), run `claude plugin validate <folder>` and `claude plugin test <folder>`, then copy it back here and commit.
