#!/usr/bin/env python3
"""Where every fall email stands, and which review pages are behind. Read by the email tracker pane.

usage: python3 campaigns/email/status.py                    prints the status as JSON
       python3 campaigns/email/status.py --set hp1 approved [note]   records Mitchell's call (approved, changes, clear)
Statuses, first match wins: edited (series.py changed since the last build.py), needs upload (the Builder Studio
draft is not the built email; upload.py records what it loaded), changes (Mitchell asked for changes),
approved, ready to proof. Approvals live in approvals.json, since the approval page keeps them in the browser.
"""
import hashlib, io, json, os, sys, time
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
sys.path.insert(0, HERE)
APPROVALS = f"{HERE}/approvals.json"

# each review page: its built file and what it is built from (relative to campaigns/)
SOURCES = [
    ("Texts and sales follow ups", "direct/direct.json", ["direct/make_direct.py"]),
    ("My Mitchell Story", "homeowners/contest.json", ["homeowners/make_contest.py"]),
    ("Events", "events/events.json", ["events/make_events.py"]),
    ("Plan", "plan/plan.json", ["plan/make_plan.py"]),
]
SHARED = ["email/out/emails.json", "direct/direct.json", "events/events.json", "homeowners/contest.json", "traffic/organic.json"]
PAGES = [
    ("Review kit", "kit/out/index.html", SHARED + ["traffic/facebook_groups.json", "builder_studio/created.json", "builder_studio/setup.json", "kit/page.html"]),
    ("Cadence", "cadence/out/index.html", SHARED + ["plan/plan.json", "cadence/page.html", "kit/out/index.html"]),
    ("Approval doc", "approval/out/index.html", SHARED + ["plan/plan.json", "approval/page.html", "kit/out/index.html"]),
    ("Master plan", "master/out/index.html", ["email/out/emails.json", "events/events.json", "plan/plan.json", "master/page.html"]),
    ("Events page", "events/out/index.html", ["email/out/emails.json", "events/events.json", "homeowners/contest.json", "events/events_page.html"]),
    ("Builder Studio inventory", "builder_studio/out/inventory.html", ["email/out/emails.json", "direct/direct.json", "events/events.json", "plan/plan.json",
                                                                       "builder_studio/created.json", "builder_studio/setup.json", "builder_studio/inventory.html"]),
]


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def read(path):
    return open(path).read() if os.path.exists(path) else None


def behind(out, deps):
    """Why a built file is behind its sources, or None."""
    if not os.path.exists(f"{C}/{out}"):
        return "not built yet"
    t = os.path.getmtime(f"{C}/{out}")
    newer = [d for d in deps if os.path.exists(f"{C}/{d}") and os.path.getmtime(f"{C}/{d}") > t + 1]
    return f"older than {', '.join(os.path.basename(d) for d in newer)}" if newer else None


def emails():
    with redirect_stdout(io.StringIO()):  # build.py prints nothing on import, but its imports might
        import build
    approvals = json.load(open(APPROVALS)) if os.path.exists(APPROVALS) else {}
    created = json.load(open(f"{C}/builder_studio/created.json")).get("templates", {})
    rows = []
    for s in build.SERIES:
        for base in s["emails"]:
            for em in build.expand(base):
                built = read(f"{HERE}/out/{em['id']}.html")
                up = created.get(em["id"].upper(), {})
                call = approvals.get(em["id"], {})
                if built != build.render(s, em):
                    status = "edited"
                elif up.get("sha") != sha(built):
                    status = "needs upload"
                else:
                    status = {"approved": "approved", "changes": "changes"}.get(call.get("status"), "ready to proof")
                rows.append({"id": em["id"], "series": s["key"], "series_name": s["name"], "send": em["send"], "subject": em["subject"],
                             "hold": em.get("hold", ""), "status": status, "note": call.get("note", ""), "uploaded": up.get("uploaded", "")})
    return rows


def main():
    if sys.argv[1:2] == ["--set"]:
        key, call, note = sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])
        approvals = json.load(open(APPROVALS)) if os.path.exists(APPROVALS) else {}
        if call == "clear":
            approvals.pop(key, None)
        elif call in ("approved", "changes"):
            approvals[key] = {"status": call, "note": note, "date": time.strftime("%Y-%m-%d")}
        else:
            raise SystemExit("use approved, changes or clear")
        json.dump(approvals, open(APPROVALS, "w"), indent=1, ensure_ascii=False)
        return
    stale = [{"name": n, "why": w} for n, out, deps in SOURCES + PAGES if (w := behind(out, deps))]
    json.dump({"emails": emails(), "stale": stale, "checked": time.strftime("%H:%M")}, sys.stdout)


if __name__ == "__main__":
    main()
