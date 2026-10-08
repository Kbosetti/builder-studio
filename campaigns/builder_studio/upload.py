#!/usr/bin/env python3
"""Load the fall email templates into Builder Studio as drafts (nothing is sent).

usage: GHL_PIT=... python3 campaigns/builder_studio/upload.py
Puts every email from campaigns/email/out (plus the sales team's personal follow up emails) into the folder
"Fall 2026 | Campaign drafts from CEA (do not send until approved)", named "Fall26 · ID · subject", with the
subject line, preview text and from name set. Safe to run again: existing templates are updated in place.
Records everything in created.json. Designed emails send from Mitchell Homes; personal ones leave the from
name blank so the workflow sends them from the assigned user.
"""
import html, json, os, re, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
L, B = "5o5zLlUPPizy6Ajp61oF", "https://services.leadconnectorhq.com"
EDITOR = "ziynYGfckcj08ySP3qVN"  # Kelly Bosetti's Builder Studio user, shown as the last editor
FOLDER_NAME = "Fall 2026 | Campaign drafts from CEA (do not send until approved)"
TOK = os.environ["GHL_PIT"]


def call(method, path, body=None):
    args = ["curl", "-sS", "-A", "Mozilla/5.0", "-X", method, "-H", f"Authorization: Bearer {TOK}", "-H", "Version: 2021-07-28", "-w", "\n%{http_code}"]
    if body is not None:
        f = "/tmp/claude-0/ghl_body.json"
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


def plain_html(subject, preview, text):
    """A sales team follow up email as a personal, plain message."""
    text = (text.replace("[first name]", "{{contact.first_name}}").replace("[portrait name]", "{{contact.portrait_name}}")
            .replace("[Region]", "{{contact.region}}").replace("[first must have]", "{{contact.design_dollars_focus}}"))
    text = re.sub(r"\[your name\]\nNew Home Consultant, Mitchell Homes\n\[your phone\]", "{{user.name}}\nNew Home Consultant, Mitchell Homes\n{{user.phone}}", text)
    paras = [p for p in text.split("\n\n") if p.strip()]
    P = "margin:0 0 14px;font-family:Arial, Helvetica, sans-serif;font-size:15px;line-height:1.6;color:#222222"
    small = "margin:0 0 6px;font-family:Arial, Helvetica, sans-serif;font-size:11px;line-height:1.5;color:#888888"
    body = "".join(f'<p style="{small if p.startswith(("Design Dollars apply", "Financing terms")) else P}">{html.escape(p).replace(chr(10), "<br>")}</p>' for p in paras)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(subject)}</title></head>'
            f'<body style="margin:0;padding:0;background:#ffffff"><div style="display:none;max-height:0;overflow:hidden;opacity:0">{html.escape(preview)}</div>'
            f'<div style="max-width:560px;padding:24px 20px">{body}<div style="margin-top:24px;padding-top:12px;border-top:1px solid #e5e5e5">'
            f'<p style="{small}">Mitchell Homes, Inc., 14300 Sommerville Court, Midlothian, VA 23113.</p><p style="{small}">{{{{unsubscribe}}}}</p></div></div></body></html>')


def main():
    rec = json.load(open(f"{HERE}/created.json")) if os.path.exists(f"{HERE}/created.json") else {}
    top = call("GET", f"emails/builder?locationId={L}&limit=100")["builders"]
    folder = next((b for b in top if b.get("name") == FOLDER_NAME), None)
    fid = folder["id"] if folder else call("POST", "emails/builder", {"locationId": L, "type": "folder", "name": FOLDER_NAME, "builderVersion": "2"})["id"]
    rec["folder"] = {"id": fid, "name": FOLDER_NAME}
    existing = {b["name"].split(" · ")[1]: b["id"] for b in call("GET", f"emails/builder?locationId={L}&parentId={fid}&limit=200")["builders"] if (b.get("name") or "").startswith("Fall26 · ")}

    items = []
    for e in json.load(open(f"{C}/email/out/emails.json"))["emails"]:
        plain = 'max-width:560px;padding:24px 20px' in open(f"{C}/email/out/{e['id']}.html").read()
        items.append({"key": e["id"].upper(), "subject": e["subject"], "preview": e["preview"], "html": open(f"{C}/email/out/{e['id']}.html").read(),
                      "from": "" if plain else "Mitchell Homes"})
    direct = {s["id"]: s for s in json.load(open(f"{C}/direct/direct.json"))["sections"]}
    n = 0
    for f in direct["followups"]["items"]:
        m = re.match(r"(?:Email subject|Subject): (.+?)\n", f["body"])
        if not m or not f["body"].startswith(("Subject:",)):
            continue
        n += 1
        body = f["body"].split("\n", 1)[1].lstrip("\n")
        subj = m.group(1).replace("[portrait name]", "{{contact.portrait_name}}").replace("[first name]", "{{contact.first_name}}")
        items.append({"key": f"SALES{n:02d}", "subject": subj, "preview": f["title"], "html": plain_html(subj, f["title"], body), "from": ""})

    ev_path = f"{C}/events/events.json"
    if os.path.exists(ev_path):
        for ev in json.load(open(ev_path))["events"]:
            for kind, key in (("invite_email", "INVITE"), ("followup_email", "FOLLOW")):
                m = ev.get(kind)
                if not m:
                    continue
                subj = m["subject"].replace("[first name]", "{{contact.first_name}}")
                rsvp = next((v["field"] for v in rec.get("links", {}).values() if v.get("event") == ev["id"]), "[RSVP link]")
                body = re.sub(r"\[RSVP link\](\?[^\s]*)?", rsvp, m["body"])
                items.append({"key": f"{ev['id'].upper()}{key}", "subject": subj, "preview": f"{ev['name']}: {'personal invitation' if key == 'INVITE' else 'follow up after the event'}",
                              "html": plain_html(subj, ev["name"], body), "from": ""})
    rec["templates"] = {}
    for it in items:
        name = f"Fall26 · {it['key']} · {it['subject']}"
        tid = existing.get(it["key"]) or call("POST", "emails/builder", {"locationId": L, "type": "html", "title": name, "parentId": fid, "builderVersion": "2"})["id"]
        call("POST", "emails/builder/data", {"locationId": L, "templateId": tid, "editorType": "html", "html": it["html"], "updatedBy": EDITOR, "previewText": it["preview"]})
        call("PATCH", f"emails/builder/{tid}", {"locationId": L, "name": name, "subjectLine": it["subject"], "fromName": it["from"]})
        rec["templates"][it["key"]] = {"id": tid, "name": name}
        print("loaded", name)
    json.dump(rec, open(f"{HERE}/created.json", "w"), indent=1, ensure_ascii=False)
    print(len(rec["templates"]), "templates in", FOLDER_NAME)


if __name__ == "__main__":
    main()
