#!/usr/bin/env python3
"""The brand line lockup that closes every designed email: "Our legacy is building Yours. Simply." with the
modifier word set in Charlotte, the brand script (assets/fonts). Email clients like Gmail and Outlook ignore web
fonts, so the lockup ships as an image, white and Mitchell Yellow on the deep green footer band.

usage: python3 campaigns/email/taglines/make_taglines.py [--upload]   (--upload needs GHL_PIT)
Writes <word>.png (rendered at 2x) and taglines.json; with --upload, puts each PNG in the Builder Studio media
library and records its URL, which build.py then uses. Variants follow the brand guide: Yours for awareness
(Home Portrait, homeowners), Dreams and Trust for in market (Design Dollars; Four Buyers, realtors, nurture).
"""
import base64, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONTS = f"{ROOT}/assets/fonts"
WORDS = ["Yours", "Dreams", "Trust"]
W, H = 600, 96  # display size in the email; rendered at 2x
DEEP, SUN = "#1e4f33", "#f5d053"
VERSION = "charlotte-lockup-2-tagline-slant"


def b64(name):
    return base64.b64encode(open(f"{FONTS}/{name}", "rb").read()).decode()


def page(word):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:C;src:url(data:font/woff2;base64,{b64('Charlotte.woff2')}) format('woff2')}}
@font-face{{font-family:M;src:url(data:font/woff2;base64,{b64('Montserrat.woff2')}) format('woff2');font-weight:100 900}}
html,body{{margin:0;background:{DEEP}}}
#t{{width:{W}px;height:{H}px;display:flex;align-items:center;justify-content:center;background:{DEEP};color:#fff;
font-family:M;font-weight:600;font-size:19px;letter-spacing:.06em;white-space:nowrap}}
#t .s{{font-family:C;font-weight:400;color:{SUN};font-style:oblique 10deg;-webkit-text-stroke:.035em currentColor;paint-order:stroke fill;font-size:46px;letter-spacing:0;line-height:1;margin:0 .1em 0 .22em;position:relative;top:.04em}}
</style></head><body><div id="t">Our legacy is building<span class="s">{word}</span>.&nbsp;Simply.</div></body></html>"""


def upload(path, name):
    tok = os.environ["GHL_PIT"]
    for _ in range(4):
        r = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-H", f"Authorization: Bearer {tok}", "-H", "Version: 2021-07-28",
                            "-F", f"file=@{path};type=image/png", "-F", f"name={name}", "https://services.leadconnectorhq.com/medias/upload-file"],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            return d.get("url") or d.get("fileUrl") or d["data"]["url"]
        except Exception:
            pass
    raise SystemExit(f"upload failed for {name}: {r.stdout[:200]}")


def main():
    rec_path = f"{HERE}/taglines.json"
    rec = json.load(open(rec_path)) if os.path.exists(rec_path) else {}
    tmp = tempfile.mkdtemp(prefix="taglines-")
    js = f"{tmp}/render.js"
    jobs = []
    for w in WORDS:
        open(f"{tmp}/{w}.html", "w").write(page(w))
        jobs.append([f"file://{tmp}/{w}.html", f"{HERE}/{w.lower()}.png"])
    open(js, "w").write("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: %d, height: %d }, deviceScaleFactor: 2 });
  for (const [u, o] of %s) { await p.goto(u); await p.evaluate(() => document.fonts.ready);
    await (await p.$('#t')).screenshot({ path: o }); }
  await b.close(); })();""" % (W, H, json.dumps(jobs)))
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", js], check=True, env=dict(os.environ, NODE_PATH=npm_root))
    for w in WORDS:
        out = f"{HERE}/{w.lower()}.png"
        sig = [VERSION, w]
        entry = rec.get(w, {})
        if entry.get("sig") != sig:
            entry = {"sig": sig}
        entry.update({"file": os.path.relpath(out, os.path.dirname(HERE)), "alt": f"Our legacy is building {w}. Simply.", "width": W})
        if "--upload" in sys.argv and not entry.get("cdn"):
            entry["cdn"] = upload(out, f"fall26-tagline-{w.lower()}.png")
        rec[w] = entry
        print(w, os.path.getsize(out) // 1024, "KB", entry.get("cdn", "(not uploaded)"))
    json.dump(rec, open(rec_path, "w"), indent=1)


if __name__ == "__main__":
    main()
