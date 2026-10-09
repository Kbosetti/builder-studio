#!/usr/bin/env python3
"""Build the client approval document for the fall traffic kit.

usage: python3 campaigns/kit/build_kit.py && python3 campaigns/approval/build_approval.py
Writes campaigns/approval/out/index.html (page content for the Artifact tool) plus the preview images it
shows, and campaigns/approval/files.json. Also writes out/batch-1, batch-2 and batch-3: the proofing pages
Mitchell actually uses, each with only the pieces and questions of that batch (campaigns/plan/plan.json),
sharing the images in out/. Approvals live in each reviewer's browser and come back to Kelly
through the Copy summary button, because Mitchell's team opens the public copy (deploy.py), not Claude.
"""
import base64, copy, json, os, re, shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
KIT = f"{C}/kit/out"
OUT = f"{HERE}/out"
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
files = []


def take(rel):
    os.makedirs(os.path.dirname(f"{OUT}/{rel}"), exist_ok=True)
    shutil.copy(f"{KIT}/{rel}", f"{OUT}/{rel}")
    files.append(rel)
    return rel


em = json.load(open(f"{C}/email/out/emails.json"))
for e in em["emails"]:
    e["img"] = take(f"email/{e['id']}.jpg")
    e["html"] = open(f"{C}/email/out/{e['id']}.html").read()
kitdata = json.load(open(f"{KIT}/live.json"))
live = {u: take(rel) for u, rel in kitdata["live"].items()}
org = {s["id"]: s for s in json.load(open(f"{C}/traffic/organic.json"))["sections"]}
plan = json.load(open(f"{C}/plan/plan.json"))
PIECE = {p["id"]: p for p in plan["pieces"]}
MONTHS = {"October": 10, "November": 11, "December": 12}


def batch_of_date(text):
    m = re.search(r"(October|November|December) (\d{1,2})", text or "")
    if not m:
        return None
    d = date(2026, MONTHS[m.group(1)], int(m.group(2)))
    return 1 if d < date(2026, 11, 2) else 2 if d < date(2026, 11, 16) else 3


def email_batch(eid):
    if eid.startswith("nu"):
        return PIECE["nurture"]["batch"]
    return PIECE[eid]["batch"] if eid in PIECE else None


dr = {s["id"]: s for s in json.load(open(f"{C}/direct/direct.json"))["sections"]}
prints = [{"title": t, "size": z, "img": take(f"print/{n}.jpg")} for n, t, z in [
    ("portrait-counter-card", "Home Portrait counter card", "5 x 7 in, Design Center counters"),
    ("design-dollars-counter-card", "Design Dollars counter card", "5 x 7 in, the design table"),
    ("landowner-community-flyer", "Landowner community board flyer", "8.5 x 11 in, feed stores, farm supply, hardware stores"),
    ("email-signature-banner", "Email signature banner", "600 x 150, every Mitchell email signature")]]
web = {k: take(f"website/{k}.jpg") for k in ["popup-open-desktop", "popup-open-phone", "slidein-desktop", "slidein-phone", "landing-desktop-full", "landing-phone-full", "videos-desktop", "videos-phone"]}


def clean(items, skip=()):
    out = []
    for it in items:
        if any(s in it["title"] for s in skip):
            continue
        out.append({"title": it["title"], "meta": it.get("meta", ""), "body": it["body"], "link": it.get("link", ""), "b": it.get("batch"),
                    "hold": bool(re.search(r"\bhold\b", (it.get("notes", "") + " " + it["title"]), re.I)), "notes": it.get("notes", "")})
    return out


def qref(text):
    t = text or ""
    for pat, q in [(r"dreamer|price locked|locked from day one", 5), (r"legal", 7), (r"/math|calculator|comparison", 6), (r"plan guide", 8),
                   (r"realtor incentive", 11), (r"referral|thank.you exists", 12), (r"November|reserve.by", 1)]:
        if re.search(pat, t, re.I):
            return q
    return 0


for e in em["emails"]:
    e["q"] = qref(e["hold"]) if e["hold"] else 0
    e["b"] = email_batch(e["id"])
lists = {k: clean(v["items"], skip=("How to post",)) for k, v in
         {"social": org["social"], "gbp": org["gbp"], "youtube": org["youtube"], "portals": org["portals"], "community": org["community"]}.items()}
lists.update({k: clean(dr[k]["items"]) for k in ("sms", "sales", "followups", "nurture", "website", "events")})
for it in lists["sms"]:
    it["b"] = PIECE.get("sms" + it["title"].split(" · ")[0].split()[-1], {}).get("batch")
for it in lists["followups"]:
    it["b"] = batch_of_date(it["meta"]) or 1
for k, b in (("sales", 1), ("website", 1), ("nurture", 2)):
    for it in lists[k]:
        it["b"] = b
ev_path = f"{C}/events/events.json"
lists["eventsSeries"] = []
if os.path.exists(ev_path):
    for e in json.load(open(ev_path))["events"]:
        rides = ", ".join(r["email"].upper() for r in e.get("rides_in", []))
        body = "\n".join(e.get("what", []))
        body += "\n\nInvitations: " + (f"a short block in email {rides}, " if rides else "") + "social posts, a Facebook event, the Google profile, " + ("Nextdoor, " if e.get("nextdoor") else "") + "a personal invitation from each consultant, and a reminder text the day before to people who RSVP."
        if e.get("extra_texts"):
            body += " Plus one invitation text: " + e["extra_texts"][0]["body"]
        body += "\n\nWhat Mitchell confirms: " + "; ".join(e.get("confirm", []))
        b = None if e.get("tier") == "later" else PIECE.get(e["id"], {}).get("batch")
        lists["eventsSeries"].append({"title": e["name"], "meta": f"{e['date']} · {e['time']} · {e.get('where', '')}", "body": body, "link": "", "hold": False, "q": 14, "b": b})
fg_path = f"{C}/traffic/facebook_groups.json"
lists["groups"], lists["groupMsgs"] = [], []
if os.path.exists(fg_path):
    fg = json.load(open(fg_path))
    for g in sorted(fg.get("groups", []), key=lambda g: (g.get("priority") or 3, g.get("state") or "")):
        meta = " · ".join(x for x in (g.get("area"), {1: "First choice", 2: "Second wave", 3: "If time allows"}.get(g.get("priority") or 3)) if x)
        body = "\n\n".join(x for x in (g.get("why"), ("Members: " + g["members"]) if g.get("members") and not g["members"].startswith("Not shown") else "",
                                        ("What we know of the rules: " + g["rules"]) if g.get("rules") else "", "How we ask: " + g["ask"] if g.get("ask") else "",
                                        "" if g.get("url") else "The direct link was not public, so this one searches Facebook for the group name.") if x)
        lists["groups"].append({"title": g["name"], "meta": meta, "body": body, "hold": False,
                                "link": g.get("url") or "https://www.facebook.com/search/groups/?q=" + g["name"].replace(" ", "%20").replace("&", "%26")})
    for o in fg.get("outreach", []) + fg.get("posts", []):
        lists["groupMsgs"].append({"title": o["title"], "meta": o.get("fits", ""), "body": o["body"], "link": o.get("link", ""), "hold": False})
for k, items in lists.items():
    for it in items:
        if "notes" in it: it["q"] = qref(it["notes"]) if it["hold"] else 0
        it.pop("notes", None)
contest = None
ranking = [{"title": it["title"], "meta": it.get("meta", ""), "body": it["body"]} for it in org["summary"]["items"]]

os.makedirs(f"{OUT}/cadence", exist_ok=True)
for n in ("rhythm", "week1"):
    shutil.copy(f"{C}/cadence/shots/{n}.jpg", f"{OUT}/cadence/{n}.jpg")
    files.append(f"cadence/{n}.jpg")
cadence = {"rhythm": "cadence/rhythm.jpg", "week": "cadence/week1.jpg", "url": "https://mitchell-fall-cadence.vercel.app"}
DATA = {"emails": em, "lists": lists, "prints": prints, "web": web, "ranking": ranking, "cadence": cadence, "contest": contest, "live": live, "links": kitdata["links"]}
font = base64.b64encode(open(f"{C}/../home-portrait/fonts/charlotte.woff2", "rb").read()).decode()
page = (open(f"{HERE}/page.html").read()
        .replace("/*DATA*/null", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/"))
        .replace("%%charlotte%%", "data:font/woff2;base64," + font))
if re.search(r"[–—]", page):
    raise SystemExit("dash found in the approval page")
for banned in ("previous agency", "CEA Marketing Group", "HighLevel", "GoHighLevel", "Value Unlocker", "Grounded Dreamer"):
    if banned in page:
        raise SystemExit(f"client facing page contains {banned!r}")
open(f"{OUT}/index.html", "w").write(page)
json.dump(files, open(f"{HERE}/files.json", "w"), indent=0)


def up(path):
    return "../" + path if path else path


QMAP = {int(k): v for k, v in plan["questions"].items()}
for B in plan["batches"]:
    n = B["n"]
    d = copy.deepcopy(DATA)
    d["batch"] = {k: B[k] for k in ("n", "name", "sends", "proof_by", "build_by", "theme")}
    d["planUrl"] = "https://mitchell-fall-plan.vercel.app"
    d["qnums"] = sorted(q for q, b in QMAP.items() if b == n)
    d["emails"]["emails"] = [e for e in d["emails"]["emails"] if e.get("b") == n]
    for e in d["emails"]["emails"]:
        e["img"] = up(e["img"])
    d["lists"] = {k: [it for it in v if it.get("b") == n] for k, v in d["lists"].items()}
    d["prints"] = [dict(p, img=up(p["img"])) for p in d["prints"] if "community board" not in p["title"]] if n == 1 else []
    d["web"] = {k: up(v) for k, v in d["web"].items()} if n == 1 else None
    d["cadence"] = dict(d["cadence"], rhythm=up(d["cadence"]["rhythm"]), week=up(d["cadence"]["week"])) if n == 1 else None
    d["ranking"] = []
    d["live"] = {u: up(r) for u, r in d["live"].items()}
    bpage = (open(f"{HERE}/page.html").read().replace("/*DATA*/null", json.dumps(d, ensure_ascii=False).replace("</", "<\\/"))
             .replace("%%charlotte%%", "data:font/woff2;base64," + font))
    if re.search(r"[\u2013\u2014]", bpage):
        raise SystemExit(f"dash found in batch {n}")
    os.makedirs(f"{OUT}/batch-{n}", exist_ok=True)
    open(f"{OUT}/batch-{n}/index.html", "w").write(bpage)
    print(f"batch-{n}:", len(d["emails"]["emails"]), "emails,", sum(len(v) for v in d["lists"].values()), "other pieces,", len(d["qnums"]), "questions")
print("index.html", len(page) // 1024, "KB;", len(files), "images,", sum(os.path.getsize(f"{OUT}/{f}") for f in files) // 1024, "KB")
