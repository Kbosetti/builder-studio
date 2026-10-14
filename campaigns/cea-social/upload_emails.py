#!/usr/bin/env python3
"""Load the six CEA emails into the CEA sub-account in Builder Studio as drafts (nothing is sent).

usage: python3 campaigns/cea-social/upload_emails.py   (needs GHL_PIT_CEA and GHL_LOCATION_CEA)
Folder "Fall 2026 | CEA emails (drafts, do not send until approved)", templates named "CEA26 · ID · subject".
The HTML comes from the CEA Content Approvals page (emails/send/); its images load from ceamarketing.com.
Safe to run again: existing templates are updated in place. Records IDs in emails_created.json.
"""
import json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
B = "https://services.leadconnectorhq.com"
L, TOK = os.environ["GHL_LOCATION_CEA"], os.environ["GHL_PIT_CEA"]
EDITOR = "ziynYGfckcj08ySP3qVN"  # Kelly Bosetti's Builder Studio user
FOLDER_NAME = "Fall 2026 | CEA emails (drafts, do not send until approved)"
FROM = "Kelly Bosetti Primeau"
EMAILS = [
    ("NEWS", "00-newsletter-new-on-the-blog.html", "Seven new guides for builders who want buyers"),
    ("AUDIT1", "01-nurture-thank-you-plus-what-the-audit-reveals.html", "Your AI Visibility Audit is underway"),
    ("AUDIT2", "02-nurture-why-ai-visibility-matters-now.html", "AI local search jumped from 6% to 45%"),
    ("AUDIT3", "03-nurture-clicks-vs-appointments-and-junk-leads.html", "Traffic is an expense. Appointments pay."),
    ("AUDIT4", "04-nurture-after-hours-lead-response.html", "Who answers your leads at 11pm?"),
    ("AUDIT5", "05-nurture-how-to-evaluate-any-agency-plus-a-strate.html", "Seven questions to ask any agency"),
]


def call(method, path, body=None):
    args = ["curl", "-sS", "-A", "Mozilla/5.0", "-X", method, "-H", f"Authorization: Bearer {TOK}", "-H", "Version: 2021-07-28", "-w", "\n%{http_code}"]
    if body is not None:
        f = "/tmp/claude-0/ghl_cea_body.json"
        json.dump(body, open(f, "w"))
        args += ["-H", "Content-Type: application/json", "--data-binary", f"@{f}"]
    for attempt in range(4):
        r = subprocess.run(args + [f"{B}/{path}"], capture_output=True, text=True)
        out, _, code = r.stdout.rpartition("\n")
        if code.startswith("2"):
            return json.loads(out or "{}")
        if code in ("429", "500", "502", "503", "") or r.returncode:
            time.sleep(2 * (attempt + 1))
            continue
        raise SystemExit(f"{method} {path} failed {code}: {out[:300]}")
    raise SystemExit(f"{method} {path} kept failing")


def main():
    top = call("GET", f"emails/builder?locationId={L}&limit=100")["builders"]
    folder = next((b for b in top if b.get("name") == FOLDER_NAME), None)
    fid = folder["id"] if folder else call("POST", "emails/builder", {"locationId": L, "type": "folder", "name": FOLDER_NAME, "builderVersion": "2"})["id"]
    existing = {b["name"].split(" · ")[1]: b["id"] for b in call("GET", f"emails/builder?locationId={L}&parentId={fid}&limit=100")["builders"] if (b.get("name") or "").startswith("CEA26 · ")}
    rec = {"folder": {"id": fid, "name": FOLDER_NAME}, "templates": {}}
    for key, fn, subject in EMAILS:
        html = open(os.path.join(HERE, "emails", fn)).read()
        m = re.search(r'<div style="display:none[^>]*>(.*?)</div>', html)
        preview = m.group(1) if m else ""
        name = f"CEA26 · {key} · {subject}"
        tid = existing.get(key) or call("POST", "emails/builder", {"locationId": L, "type": "html", "title": name, "parentId": fid, "builderVersion": "2"})["id"]
        call("POST", "emails/builder/data", {"locationId": L, "templateId": tid, "editorType": "html", "html": html, "updatedBy": EDITOR, "previewText": preview})
        call("PATCH", f"emails/builder/{tid}", {"locationId": L, "name": name, "subjectLine": subject, "fromName": FROM})
        rec["templates"][key] = {"id": tid, "name": name}
        print("loaded", name)
    json.dump(rec, open(os.path.join(HERE, "emails_created.json"), "w"), indent=1, ensure_ascii=False)
    print(len(rec["templates"]), "templates in", FOLDER_NAME)


if __name__ == "__main__":
    main()
