#!/usr/bin/env python3
"""Render the Design Center counter cards, the community board flyer and the email signature banner.

usage: python3 campaigns/print/make_print.py      writes campaigns/print/out/*.png and *.pdf
Print sizes: counter cards 5 x 7 in, flyer 8.5 x 11 in, both at 300 dpi. QR codes carry UTMs so every
scan is counted (utm_medium=print). Copy follows campaigns/FACTS.md.
"""
import json, os, subprocess
from urllib.parse import urlencode
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = f"{HERE}/src", f"{HERE}/out"
os.makedirs(OUT, exist_ok=True)
QUIZ = "https://mitchellhomesliving.com/portrait"
DD = "https://simplymitchellhomes.com/design-dollars"
FINE_DD = ("*Design Dollars apply to Design Center selections only. Not applied to base price. No cash value. "
           "One offer per contract. Tier determined when selections are made. Full terms from your New Home Consultant.")
FINE_FIN = "Financing terms are illustrative only and subject to credit approval. Not a commitment to lend."


def link(url, source, content, campaign):
    return url + "?" + urlencode({"utm_source": source, "utm_medium": "print", "utm_campaign": campaign, "utm_content": content})


def qr(url, color="#1e4f33"):
    return segno.make(url, error="m").svg_inline(scale=10, dark=color, light=None, border=0, omitsize=True)


BASE = f"""
@font-face{{font-family:M;src:url({SRC}/montserrat.woff2)}}
@font-face{{font-family:C;src:url({SRC}/charlotte.woff2)}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:%(w)spx;height:%(h)spx;overflow:hidden;font-family:M,sans-serif;color:#1e4f33;background:#faf8f3}}
.s{{font-family:C,cursive;font-weight:400;font-style:oblique 10deg;-webkit-text-stroke:.035em currentColor;paint-order:stroke fill;color:#f5d053;font-size:1.55em;line-height:.7;padding:0 .04em}}
.qr svg{{display:block;width:100%;height:auto}}
"""

PIECES = []

# 1. Home Portrait counter card, 5 x 7 in, for Design Center counters and event tables
q1 = link(QUIZ, "designcenter", "counter_card", "fall26_portrait")
PIECES.append(("portrait-counter-card", 480, 672, "5in", "7in", f"""
<style>{BASE}
.ph{{position:absolute;inset:0 0 auto 0;height:400px;background:url({SRC}/farmhouse.jpg) center/cover}}
.ph:after{{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(16,44,28,.35),rgba(16,44,28,0) 30%,rgba(16,44,28,.2) 55%,rgba(16,44,28,.94) 100%)}}
.logo{{position:absolute;left:26px;top:22px;width:74px;z-index:2}}
.t{{position:absolute;left:28px;right:28px;top:250px;z-index:2;color:#fff}}
.eb{{font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#f5d053;margin-bottom:8px}}
h1{{font-size:27px;line-height:1.12;font-weight:700}}
.b{{position:absolute;left:0;right:0;bottom:0;height:272px;padding:24px 28px;display:flex;gap:22px;align-items:center}}
.qr{{width:150px;flex:none;padding:10px;background:#fff;border-radius:12px;box-shadow:0 2px 10px rgba(16,44,28,.12)}}
.c p{{font-size:13px;line-height:1.5;color:#24332a;margin-bottom:12px}}
.c b.go{{display:inline-block;background:#f5d053;color:#1e4f33;font-size:13px;font-weight:800;padding:9px 16px;border-radius:999px;margin-bottom:10px}}
.c .u{{font-size:11px;font-weight:700;color:#2b6d47}}
</style>
<div class="ph"></div><img class="logo" src="{SRC}/mitchell-logo-white.png" alt="Mitchell Homes">
<div class="t"><div class="eb">The Home Portrait</div><h1>Every home is a portrait. Discover <span class="s">Yours</span></h1></div>
<div class="b"><div class="qr">{qr(q1)}</div><div class="c">
<p>Answer eight questions about the home you dream of and the land it belongs on. We paint your Home Portrait.</p>
<b class="go">Scan to begin</b><div class="u">About 90 seconds<br>mitchellhomesliving.com/portrait</div></div></div>
"""))

# 2. Design Dollars counter card, 5 x 7 in, for the design table
q2 = link(DD, "designcenter", "counter_card", "fall26_designdollars")
rows = [["Any Mitchell home", "$5,000"], ["$25,000 in selections", "$7,500"], ["$40,000 in selections", "$11,000"], ["$60,000 in selections", "$15,000"], ["$80,000 in selections", "$20,000"], ["$100,000 or more", "$25,000"]]
tr = "".join(f'<tr class="{"top" if i == 5 else ""}"><td>{a}</td><td>{v}</td></tr>' for i, (a, v) in enumerate(rows))
PIECES.append(("design-dollars-counter-card", 480, 672, "5in", "7in", f"""
<style>{BASE}
body{{background:#1e4f33;color:#fff;padding:26px 28px}}
.logo{{width:62px;margin-bottom:16px}}
.eb{{font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#f5d053;margin-bottom:8px}}
h1{{font-size:24px;line-height:1.15;font-weight:700;margin-bottom:14px}}
table{{width:100%;border-collapse:collapse;font-size:12.5px;margin-bottom:14px}}
th{{text-align:left;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#cfe0d4;padding:0 10px 6px}}
th:last-child,td:last-child{{text-align:right}}
td{{padding:7px 10px;border-top:1px solid rgba(255,255,255,.18)}}
td:last-child{{font-weight:800;color:#f5d053;font-size:14px}}
tr.top td{{background:#f5d053;color:#1e4f33}} tr.top td:last-child{{color:#1e4f33}}
.r{{display:flex;gap:16px;align-items:center}}
.qr{{width:104px;flex:none;padding:7px;background:#fff;border-radius:10px}}
.r p{{font-size:12px;line-height:1.5;color:#e8efe9}}
.r p b{{color:#fff}}
.f{{position:absolute;left:28px;right:28px;bottom:18px;font-size:7.5px;line-height:1.4;color:#b9cfc0}}
.tg{{position:absolute;left:28px;right:28px;bottom:58px;text-align:center;color:#fff;font-weight:600;font-size:12.5px;letter-spacing:.06em}}
.tg .s{{font-size:2.3em;margin:0 .06em 0 .14em;position:relative;top:.06em}}
</style>
<img class="logo" src="{SRC}/mitchell-logo-white.png" alt="Mitchell Homes">
<div class="eb">Mitchell Design Dollars</div>
<h1>The more you personalize, the more we cover.*</h1>
<table><tr><th>Selections you choose</th><th>Mitchell adds</th></tr>{tr}</table>
<div class="r"><div class="qr">{qr(q2)}</div><p><b>Sign now and your incentive is locked.</b> Your tier is set when you make your selections. Ask your Design Consultant how close you are to the next tier.</p></div>
<div class="tg">Our legacy is building<span class="s">Dreams</span>. Simply.</div>
<div class="f">{FINE_DD}</div>
"""))

# 3. Community board flyer with tear-off tabs, 8.5 x 11 in, for feed stores, farm supply, hardware stores, libraries
q3 = link(QUIZ, "community_board", "flyer", "fall26_portrait")
tabs = "".join('<div class="tab"><b>Home Portrait quiz</b><span>mitchellhomesliving.com/portrait</span></div>' for _ in range(8))
PIECES.append(("landowner-community-flyer", 816, 1056, "8.5in", "11in", f"""
<style>{BASE}
.ph{{height:360px;background:url({SRC}/farmland.jpg) center/cover;position:relative}}
.logo{{position:absolute;left:40px;top:32px;width:96px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.35))}}
.m{{padding:34px 48px 0;display:grid;grid-template-columns:1fr 210px;gap:34px}}
.eb{{font-size:12px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#2b6d47;margin-bottom:10px}}
h1{{font-size:44px;line-height:1.05;font-weight:800;margin-bottom:18px}}
h1 .s{{color:#2b6d47}}
p{{font-size:16px;line-height:1.55;color:#24332a;margin-bottom:12px}}
.pts{{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 14px}}
.pts span{{background:#1e4f33;color:#fff;font-weight:700;font-size:13px;padding:7px 13px;border-radius:999px}}
.qr{{padding:12px;background:#fff;border-radius:14px;box-shadow:0 2px 12px rgba(16,44,28,.14)}}
.side .go{{display:block;text-align:center;font-weight:800;font-size:15px;margin:12px 0 4px}}
.side .u{{text-align:center;font-size:11.5px;font-weight:700;color:#2b6d47}}
.fine{{padding:10px 48px 0;font-size:9px;color:#5b6f62}}
.tabs{{position:absolute;left:0;right:0;bottom:0;height:215px;display:flex;border-top:2px dashed #929292}}
.tab{{flex:1;border-left:2px dashed #929292;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;font-size:11px;font-weight:600;color:#24332a;white-space:nowrap}}
.tab:last-child{{border-right:0}}
.tab b{{font-size:12px;color:#1e4f33}}
</style>
<div class="ph"><img class="logo" src="{SRC}/mitchell-logo-white.png" alt="Mitchell Homes"></div>
<div class="m"><div>
<div class="eb">For landowners</div>
<h1>Own land? See what it could <span class="s">Become</span></h1>
<p>Mitchell Homes builds custom homes on land you already own, and has since 1992.</p>
<div class="pts"><span>Zero down</span><span>Zero closing costs</span><span>No construction loan</span></div>
<p>Mitchell self-funds every build. Answer eight questions about the home you dream of, and we paint your Home Portrait.</p>
</div><div class="side"><div class="qr">{qr(q3)}</div><b class="go">Scan to begin</b><div class="u">About 90 seconds<br>mitchellhomesliving.com/portrait</div></div></div>
<div class="fine">{FINE_FIN} Virginia and Maryland (540) 701-2759. North and South Carolina (984) 331-5468.</div>
<div class="tabs">{tabs}</div>
"""))

# 4. Email signature banner, 600 x 150 (rendered at 2x)
PIECES.append(("email-signature-banner", 600, 150, None, None, f"""
<style>{BASE}
body{{display:flex;background:#1e4f33;color:#fff}}
.ph{{width:220px;background:url({SRC}/porch.jpg) center/cover}}
.t{{flex:1;padding:20px 24px;display:flex;flex-direction:column;justify-content:center;gap:8px}}
.eb{{font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#f5d053}}
h1{{font-size:21px;line-height:1.1;font-weight:700}}
.go{{align-self:flex-start;background:#f5d053;color:#1e4f33;font-weight:800;font-size:12px;padding:7px 14px;border-radius:999px}}
</style>
<div class="ph"></div><div class="t"><div class="eb">The Home Portrait</div><h1>What would your home look like?</h1><div class="go">Take the 90-second quiz</div></div>
"""))

jobs = []
for name, w, h, pw, ph, body in PIECES:
    path = f"{OUT}/{name}.html"
    open(path, "w").write("<!doctype html><html><head><meta charset='utf-8'></head><body>" + body.replace("%(w)spx", f"{w}px").replace("%(h)spx", f"{h}px") + "</body></html>")
    jobs.append({"html": path, "png": path.replace(".html", ".png"), "pdf": path.replace(".html", ".pdf") if pw else None, "w": w, "h": h, "pw": pw, "ph": ph,
                 "scale": 2 if not pw else 3.125})
json.dump(jobs, open(f"{OUT}/jobs.json", "w"))
subprocess.run(["node", f"{HERE}/render.js", f"{OUT}/jobs.json"], check=True,
               env={**os.environ, "NODE_PATH": subprocess.check_output(["npm", "root", "-g"], text=True).strip()})
open(f"{OUT}/email-signature.html", "w").write(
    '<a href="https://mitchellhomesliving.com/portrait?utm_source=email_signature&amp;utm_medium=email&amp;utm_campaign=fall26_portrait&amp;utm_content=signature_banner" '
    'target="_blank"><img src="REPLACE_WITH_HOSTED_BANNER_URL" width="600" height="150" alt="What would your home look like? Take the 90-second Home Portrait quiz." '
    'style="display:block;width:100%;max-width:600px;height:auto;border:0;border-radius:8px"></a>\n')
for j in jobs:
    print(os.path.basename(j["png"]), j["pdf"] and os.path.basename(j["pdf"]) or "")
