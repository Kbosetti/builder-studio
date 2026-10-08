---
name: cea-client-approval-doc
description: Build CEA Marketing's client approval document, one polished branded web page where a client reviews every piece of a campaign (emails, website pop-ups and landing pages, social posts, Google Business Profile posts, texts, sales scripts, print, events), marks each item Approve or Needs changes with a note, answers the open questions, and copies a signed summary back to Kelly. Use it whenever Kelly or the CEA team wants a client to sign off on campaign work, asks for an "approval doc", "approval page", "approval thing", "sign off page", "something the client can approve", "put everything together so they can see it", or wants to send a client one link with all the assets, even if the word approval is not used. Also use it to refresh an existing approval page after the client's changes come back. Works for any CEA client (Mitchell Homes, Sunlife, Vitale and others); always load that client's messaging skill first.
---

# Client approval document

One link a client opens to see everything they are being asked to approve, decide on each piece, answer the open questions, and send back a summary. Kelly sends it, the client signs off in about twenty minutes, and the work moves. It replaces long email threads and decks the client cannot open.

## Why it works the way it does

- **One decision per item.** Each approval item is one thing a person can say yes or no to (an email series, the pop-up, the social calendar). Grouping by decision, not by file, keeps the count around 10 to 20 and makes the summary readable.
- **In send order.** Items follow the order the work goes out, so the page doubles as the plan.
- **Show, do not describe.** Every visual piece appears as a real screenshot the client can open full size. Every written piece shows its exact words.
- **Questions unlock work.** Anything waiting on the client becomes a numbered question with an answer box, and every blocked item carries a "Waiting on question N" badge. The client sees exactly what their answer releases.
- **No backend.** Choices save in the reviewer's own browser and come back through Copy summary or Open in email. Clients often sit outside Kelly's organization (Microsoft accounts, other companies), so the page cannot depend on a Claude sign in.
- **Public link plus private copy.** Claude artifact links frequently cannot be made public from Kelly's account (the Share menu only offers invites), so the page is also deployed as a static site on CEA's Vercel team with noindex. Kelly sends the public link.

## Workflow

1. **Load the client's messaging skill** (for example `cea-mitchell-homes-messaging`) and follow its rules in every word on the page: banned words, dash rules, offer wording, titles, and the rule against naming vendor platforms or a previous agency. If no messaging skill exists, load `cea-brand` and ask Kelly for the client's colors.
2. **Collect everything to approve** from the conversation, the repo, Drive, Canva and earlier artifacts. Note which pieces are blocked and why.
3. **Make the visuals.** Screenshot every email, web page and print piece to JPG with `scripts/shoot.js` (full page, waits for images, retries through flaky proxies). Emails at 640 px wide, desktop pages at 1280, phones at 390, print pieces from their own PNG.
4. **Write the spec** (`spec.json`) following `references/spec.md`: client and brand, the cover, the at a glance section, the sections and items, the questions. Write the client facing copy now; see "Writing the page" below.
5. **Build:** `python3 scripts/build_approval.py spec.json out/` writes `out/index.html` (the page content, no doctype, ready for the Artifact tool), copies the images into `out/assets/`, and writes `out/files.json`. The build stops if it finds a dash or a banned phrase listed in the spec.
6. **Look once.** Serve `out/` locally (`python3 -m http.server`) and screenshot desktop and phone. Fix what the look shows, then move on.
7. **Publish both copies.**
   - Kelly's private copy: Artifact tool, `file_path` `out/index.html`, `root` `out`, `files` from `out/files.json`, an `icon` such as `checklist`.
   - The public copy: `VERCEL_TOKEN=... python3 scripts/deploy_vercel.py out/ <client>-<campaign>-approval` wraps the page in a full document with noindex and deploys it. It prints the `https://<project>.vercel.app` address. Fetch it once with curl to confirm it answers 200.
8. **Hand it over.** Give Kelly the public link, her private link, and a three line cover note she can paste to the client. Record both links in the repo's CLAUDE.md if the project keeps one.
9. **When summaries come back,** apply the changes, mark answered questions in the spec, clear the "waiting" badges they released, rebuild and redeploy to the same project name so the client's link never changes.

## Writing the page

- Title the page with the client and campaign, e.g. "Mitchell Fall Plan Approval". The cover says who it is for, who prepared it, the month, and that nothing has been sent or posted.
- Item titles name the thing and count it: "Design Dollars emails (4)". The "when" line gives the dates and audience. The "why" line is one sentence on what the item does.
- Questions are answerable in a sentence. State the options or our recommendation ("We suggest November 30, 2026"). Name what waits on the answer.
- Leave out everything internal: CEA working notes, holds written for the team, UTM instructions, vendor platform names, any mention of a previous agency, budget talk. If a blocker matters to the client, turn it into a question.
- Use the client's colors, type and one script word only if the brand allows it.

## Files

- `scripts/build_approval.py`: spec to page. Reads `assets/page.html`.
- `scripts/shoot.js`: screenshots for HTML files or URLs (Playwright, Chromium at /opt/pw-browsers/chromium when present).
- `scripts/deploy_vercel.py`: static deploy through the Vercel API with retries; creates the project on first use.
- `assets/page.html`: the page template.
- `references/spec.md`: the spec format with a full example. Read it before writing a spec.
