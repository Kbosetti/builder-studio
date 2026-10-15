# AI Visibility Audit: build sheet for Mike

Everything happens in Builder Studio, in the **CEA Marketing** sub-account. The six emails are already built. You are building the form and the workflow that sends them, then approving them.

## Part 1. Build the form

1. Go to **Sites > Forms > Builder** and click **+ Add Form**, then **Blank form**.
2. Name it **AI Visibility Audit Request**.
3. Add these fields, in this order:
   - First Name (required)
   - Last Name (required)
   - Email (required)
   - Phone
   - Company Name (required)
   - Website
   - A new **multi line text** field labeled **"Which cities or communities should we check first?"** (required)
4. Submit button text: **Request my free audit**
5. On submit, show this message: **"Thank you! Kelly's team is starting your AI Visibility Audit. We will email you within one business day."**
6. Style it with the CEA colors: button pink `#E04A7E`, headings navy `#1A1830`, font Poppins.
7. Save. Then click **Integrate** and copy the **share link**. Send that link to Kelly.

## Part 2. Build the workflow (save as draft, do not publish yet)

1. Go to **Automation > Workflows > + Create Workflow > Start from scratch**.
2. Name it **CEA | AI Visibility Audit Request**.
3. **Trigger:** Form Submitted. Filter: Form is **AI Visibility Audit Request**.
4. **Actions, in order:**
   1. **Add Tag:** `ai audit request`
   2. **Internal Notification (email)** to kelly@ceamarketing.com and tom@ceamarketing.com. Subject: `New AI audit request: {{contact.name}}, {{contact.company_name}}`. Body: name, company, email, phone, website and the cities answer.
   3. **Send Email:** template **CEA26 · AUDIT1 · Your AI Visibility Audit is underway**
   4. **Wait:** 2 days
   5. **Send Email:** **CEA26 · AUDIT2 · AI local search jumped from 6% to 45%**
   6. **Wait:** 3 days
   7. **Send Email:** **CEA26 · AUDIT3 · Traffic is an expense. Appointments pay.**
   8. **Wait:** 4 days
   9. **Send Email:** **CEA26 · AUDIT4 · Who answers your leads at 11pm?**
   10. **Wait:** 5 days
   11. **Send Email:** **CEA26 · AUDIT5 · Seven questions to ask any agency**
5. For every Send Email step, set From Name **Kelly Bosetti Primeau** and From Email **kelly@ceamarketing.com**.
6. **Settings:** turn **Stop on response** on (if a builder replies, the emails stop so Kelly can talk to them personally). Leave **Allow re-entry** off.
7. **Save. Do not publish.** Leave it in Draft until Kelly says go.

## Part 3. Review and approve the emails

The six templates are in **Marketing > Emails > Templates**, folder **"Fall 2026 | CEA emails (drafts, do not send until approved)"**:

| Template | When it sends |
|---|---|
| CEA26 · NEWS · Seven new guides for builders who want buyers | One time newsletter to the builder, IBS and lead lists |
| CEA26 · AUDIT1 · Your AI Visibility Audit is underway | Right after the form |
| CEA26 · AUDIT2 · AI local search jumped from 6% to 45% | Day 2 |
| CEA26 · AUDIT3 · Traffic is an expense. Appointments pay. | Day 5 |
| CEA26 · AUDIT4 · Who answers your leads at 11pm? | Day 9 |
| CEA26 · AUDIT5 · Seven questions to ask any agency | Day 14 |

Open each one, check the copy and click every link and button. Send Kelly your approval or any changes.

## What happens next

1. Kelly sends Claude the form's share link.
2. Claude points the "Request my free AI Visibility Audit" buttons in the emails to the new form.
3. Claude sends a fresh round of tests to Kelly, Tom and Mike.
4. Mike fills out the form once with his own email to test the workflow, and confirms the notification and email 1 arrive.
5. Kelly gives the final go ahead, and Mike publishes the workflow.
