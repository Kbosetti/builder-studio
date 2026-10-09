#!/usr/bin/env python3
"""Assemble the Fall Traffic Kit review page from everything in campaigns/.

usage: python3 campaigns/kit/build_kit.py     writes campaigns/kit/out/index.html and campaigns/kit/out/files.json
Inputs: email/out (HTML, text, emails.json), email/previews (screenshots), traffic/organic.json,
direct/direct.json, print/out, website/ (pop-up, landing page, screenshots). Published with the Artifact
tool: index.html as the page, every path in files.json as a supporting file (root campaigns/kit/out).
"""
import json, os, re, shutil, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
OUT = f"{HERE}/out"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"


def copy(src, rel):
    dst = f"{OUT}/{rel}"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)
    files.append(rel)
    return rel


def jpg(src, rel, width):
    dst = f"{OUT}/{rel}"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", src, "-vf", f"scale='min({width},iw)':-2:flags=lanczos", "-q:v", "2", dst], check=True)
    files.append(rel)
    return rel


if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
files = []

# emails
em = json.load(open(f"{C}/email/out/emails.json"))
for e in em["emails"]:
    e["html"] = open(f"{C}/email/out/{e['id']}.html").read()
    e["text"] = open(f"{C}/email/out/{e['id']}.txt").read()
    e["preview_img"] = copy(f"{C}/email/previews/{e['id']}.jpg", f"email/{e['id']}.jpg")
    e["file"] = copy(f"{C}/email/out/{e['id']}.html", f"email/{e['id']}.html")

# live email viewer: Claude pages block outside images, so every picture an email uses ships with the page
CACHE = f"{C}/email/live_cache"
os.makedirs(CACHE, exist_ok=True)
live = {}
for e in em["emails"]:
    for u in re.findall(r'<img[^>]+src="(https?://[^"]+)"', e["html"]):
        if u in live:
            continue
        name = re.sub(r"[^\w.-]", "_", u.split("?")[0].rsplit("/", 1)[-1])
        if not os.path.exists(f"{CACHE}/{name}") or os.path.getsize(f"{CACHE}/{name}") < 500:
            subprocess.run(["curl", "-sS", "--retry", "5", "-o", f"{CACHE}/{name}", u], check=True)
        live[u] = copy(f"{CACHE}/{name}", f"live/{name}")
created = json.load(open(f"{C}/builder_studio/created.json")) if os.path.exists(f"{C}/builder_studio/created.json") else {}
links = {v["id"]: v["to"] for v in created.get("links", {}).values()}
json.dump({"live": live, "links": links}, open(f"{OUT}/live.json", "w"))  # read by the approval build

organic = json.load(open(f"{C}/traffic/organic.json"))
direct = json.load(open(f"{C}/direct/direct.json"))

# print pieces
prints = []
for name, title, size in [("portrait-counter-card", "Home Portrait counter card", "5 x 7 in"),
                          ("design-dollars-counter-card", "Design Dollars counter card", "5 x 7 in"),
                          ("landowner-community-flyer", "Landowner community board flyer", "8.5 x 11 in"),
                          ("email-signature-banner", "Email signature banner", "600 x 150")]:
    p = {"title": title, "size": size, "img": jpg(f"{C}/print/out/{name}.png", f"print/{name}.jpg", 1600),
         "png": copy(f"{C}/print/out/{name}.png", f"print/{name}.png")}
    if os.path.exists(f"{C}/print/out/{name}.pdf"):
        p["pdf"] = copy(f"{C}/print/out/{name}.pdf", f"print/{name}.pdf")
    prints.append(p)
sig_html = open(f"{C}/print/out/email-signature.html").read()

# website pieces (from the website agent)
web = {"shots": [], "snippet": "", "landing": "", "readme": ""}
W = f"{C}/website"
for f, label in [("popup-open-desktop.png", "Pop-up on a computer"), ("popup-open-phone.png", "Pop-up on a phone"),
                 ("slidein-desktop.png", "Slide-in corner card, the gentler option"), ("slidein-phone.png", "Slide-in on a phone"),
                 ("landing-desktop-full.png", "Landing page on a computer"), ("landing-phone-full.png", "Landing page on a phone"),
                 ("videos-desktop.png", "Video strip for any page, on a computer"), ("videos-phone.png", "Video strip on a phone")]:
    if os.path.exists(f"{W}/shots/{f}"):
        width = 780 if "phone" in f else (1600 if "full" in f else 2000)  # sharp in the full-size view
        web["shots"].append({"label": label, "img": jpg(f"{W}/shots/{f}", f"website/{f.replace('.png', '.jpg')}", width)})
if os.path.exists(f"{W}/popup/portrait-popup-snippet.html"):
    web["snippet"] = open(f"{W}/popup/portrait-popup-snippet.html").read()
    web["snippet_file"] = copy(f"{W}/popup/portrait-popup-snippet.html", "website/portrait-popup-snippet.html")
if os.path.exists(f"{W}/videos/video-strip-snippet.html"):
    web["video_file"] = copy(f"{W}/videos/video-strip-snippet.html", "website/video-strip-snippet.html")
if os.path.exists(f"{W}/landing/home-portrait.html"):
    web["landing_file"] = copy(f"{W}/landing/home-portrait.html", "website/home-portrait-landing.html")
for rd in ("landing/README.md", "README.md", "popup/README.md"):
    if os.path.exists(f"{W}/{rd}"):
        web["readme"] += open(f"{W}/{rd}").read() + "\n\n"

def opt(path):
    return json.load(open(path)) if os.path.exists(path) else None
DATA = {"emails": em, "organic": organic, "direct": direct, "prints": prints, "sig_html": sig_html, "web": web,
        "events": opt(f"{C}/events/events.json"), "groups": opt(f"{C}/traffic/facebook_groups.json"), "setup": opt(f"{C}/builder_studio/setup.json"), "live": live, "links": links}
data = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")
page = open(f"{HERE}/page.html").read().replace("/*DATA*/null", data)
if re.search(r"[–—]", page):
    raise SystemExit("dash found in kit page")
open(f"{OUT}/index.html", "w").write(page)
json.dump(files, open(f"{HERE}/files.json", "w"), indent=0)
print("index.html", len(page) // 1024, "KB;", len(files), "files,", sum(os.path.getsize(f"{OUT}/{f}") for f in files) // 1024, "KB")
