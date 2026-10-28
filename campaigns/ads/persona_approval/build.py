#!/usr/bin/env python3
"""Approval page for the persona ads without an incentive, in the same style as the November offer approval page.

usage: python3 campaigns/ads/persona_approval/build.py [--deploy]   (--deploy needs VERCEL_TOKEN)
Reads the copy from campaigns/ads/persona_kit/index.html, the reels from the media library (or the local zip
folder), the carousel cards from campaign-guide/img, and writes out/ (index.html, reels/, img/). With --deploy it
publishes https://mitchell-persona-ads-approval.vercel.app (noindex).
"""
import html, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = f"{HERE}/out"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
E = html.escape
kit = open(f"{ROOT}/campaigns/ads/persona_kit/index.html").read()
OFFER = json.loads(re.search(r'var OFFER = (".*?");\n', kit, re.S).group(1))
REELS = json.loads(re.search(r'var REELS = (\[.*?\]);\n', kit, re.S).group(1).replace('"more": OFFER', '"more": ""'))
GUIDE = {"value-unlocker": "value-unlocker", "planner": "planner", "transitioner": "transitioner", "grounded-dreamer": "grounded-dreamer"}
ALT = {}
for m in re.finditer(r'buyers-([a-z-]+)-(\d)\.jpg%%" alt="Card \d: ([^"]+)"', open(f"{ROOT}/campaign-guide/src.html").read()):
    ALT[(m.group(1), int(m.group(2)))] = m.group(3)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(f"{OUT}/reels"); os.makedirs(f"{OUT}/img")
sections, nav = [], []
for n, r in enumerate(REELS, 1):
    k = r["key"]
    mp4 = f"{OUT}/reels/{k}.mp4"
    subprocess.run(["curl", "-sS", "--retry", "4", "-o", mp4, r["lib"]], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "3", "-i", mp4, "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "4", f"{OUT}/reels/{k}.jpg"], check=True)
    cards = ""
    for c in range(1, 6):
        src = f"{ROOT}/campaign-guide/img/buyers-{GUIDE[k]}-{c}.jpg"
        shutil.copy(src, f"{OUT}/img/{k}-{c}.jpg")
        tag = "New" if c == 5 else "Unchanged"
        cards += (f'<figure><img src="img/{k}-{c}.jpg" alt="{E(ALT.get((k, c), ""))}" loading="lazy">'
                  f'<figcaption>Card {c} · {tag}</figcaption></figure>')
    title = r["title"].split(". ", 1)[1]
    sid = f"p{n}"
    nav.append(f'<a href="#{sid}">{E(title)}</a>')
    note = f'<p class="hold">{E(r["note"])}</p>' if r.get("note") else ""
    fields = [("Primary text", r["primary"]), ("See more", OFFER), ("Headline", r["head"]), ("Description", r["desc"]),
              ("Button", "Learn More"), ("Landing page", "https://" + r["url"])]
    fhtml = "".join(f'<div class="field"><div class="flabel">{E(a)}</div><div class="fval">{E(b)}</div></div>' for a, b in fields)
    sections.append(f'''<section class="ver" id="{sid}" data-item="{E(title)}">
  <div class="sechead"><p class="eyebrow">Meta · Facebook and Instagram · Persona {n}</p><h2>{E(title)}</h2>{note}</div>
  <div class="cols">
    <figure class="reel"><video controls playsinline preload="none" poster="reels/{k}.jpg" src="reels/{k}.mp4"></video><figcaption>Reel 1080x1920 · new end card</figcaption></figure>
    <div class="copy">{fhtml}</div>
  </div>
  <h3>Carousel (1080x1080)</h3>
  <div class="cards">{cards}</div>
  <div class="approve"><span>Approve {E(title)}</span><button type="button" class="ok">Approved</button><button type="button" class="no">Changes needed</button>
    <textarea placeholder="Notes or changes (optional)" aria-label="Notes for {E(title)}"></textarea></div>
</section>''')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><title>Persona Ads Approval</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap">
<style>
:root{{--green:#2b6d47;--deep:#1e4f33;--yellow:#f5d053;--ink:#1d2a22;--body:#3d4d43;--muted:#5b6b61;--paper:#fbfaf5;--soft:#f1f5f2;--line:#dfe6e1;--white:#fff}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.6 Montserrat,system-ui,Arial,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left));padding-right:max(18px,env(safe-area-inset-right))}}
header.top{{background:var(--deep);color:var(--white)}}
header.top .wrap{{padding-block:40px;display:grid;gap:12px}}
header.top h1{{margin:0;font-size:clamp(30px,5vw,46px);line-height:1.1}}
header.top p{{margin:0;color:#d5e3d9;max-width:52em}}
.pill{{display:inline-block;background:var(--yellow);color:var(--deep);font-weight:800;font-size:13px;letter-spacing:.08em;text-transform:uppercase;padding:6px 14px;border-radius:999px;justify-self:start}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}}
nav a{{color:var(--white);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:6px 14px;font-weight:600;font-size:14px;text-decoration:none}}
.eyebrow{{margin:0;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--green)}}
h2{{margin:0;font-size:clamp(24px,3.4vw,32px);color:var(--deep);line-height:1.2}}
h3{{margin:4px 0 0;font-size:16px;color:var(--deep)}}
.summary{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:28px}}
.summary div{{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:16px}}
.summary b{{display:block;color:var(--deep);font-size:17px;line-height:1.3;margin-bottom:4px}}
.summary div{{min-width:0}}
.summary span{{color:var(--muted);font-size:14px;overflow-wrap:anywhere}}
.ver{{background:var(--white);border:1px solid var(--line);border-radius:20px;padding:28px;margin-top:28px;display:grid;gap:20px;scroll-margin-top:16px}}
.sechead{{display:grid;gap:6px}}
.hold{{margin:0;background:#fff4d6;color:#7a5a00;border-radius:10px;padding:8px 12px;font-size:14px;font-weight:600}}
.cols{{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:28px;align-items:start}}
figure{{margin:0;display:grid;gap:6px}}
figure img,figure video{{width:100%;border-radius:12px;border:1px solid var(--line);background:#000;display:block}}
.reel video{{aspect-ratio:9/16;object-fit:cover}}
figcaption{{font-size:13px;color:var(--muted);font-weight:600}}
.copy{{display:grid}}
.field{{display:grid;grid-template-columns:150px minmax(0,1fr);gap:14px;padding:12px 0;border-top:1px solid var(--line)}}
.flabel{{font-weight:700;color:var(--deep);font-size:14px}}
.fval{{color:var(--ink);overflow-wrap:anywhere;white-space:pre-line;font-size:15px}}
.cards{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}}
.approve{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;background:var(--soft);border-radius:12px;padding:12px 16px;font-weight:700;color:var(--deep)}}
.approve span{{flex:1;min-width:200px}}
.approve button{{font:inherit;font-size:14px;border:2px solid var(--green);border-radius:8px;padding:6px 14px;font-weight:700;color:var(--green);background:var(--white);cursor:pointer}}
.approve button.on.ok{{background:var(--green);color:var(--white)}}
.approve button.on.no{{background:#7a5a00;border-color:#7a5a00;color:var(--white)}}
.approve textarea{{flex-basis:100%;font:inherit;font-size:14px;font-weight:400;min-height:56px;border:1px solid var(--line);border-radius:8px;padding:8px 10px}}
button:focus-visible,a:focus-visible,textarea:focus-visible{{outline:3px solid var(--yellow);outline-offset:2px}}
.done{{background:var(--deep);color:var(--white);border-radius:20px;padding:28px;margin:28px 0 48px;display:grid;gap:12px}}
.done h2{{color:var(--white)}}
.done input{{font:inherit;padding:8px 10px;border-radius:8px;border:0;max-width:340px}}
.done button{{justify-self:start;font:inherit;font-weight:800;background:var(--yellow);color:var(--deep);border:0;border-radius:999px;padding:10px 20px;cursor:pointer}}
.done pre{{white-space:pre-wrap;background:rgba(255,255,255,.08);border-radius:10px;padding:12px;font-size:13px;margin:0}}
footer{{color:var(--muted);font-size:13px;padding-bottom:40px}}
@media (max-width:820px){{.summary{{grid-template-columns:repeat(2,minmax(0,1fr))}}.cols{{grid-template-columns:1fr}}.cols .reel{{max-width:320px}}.cards{{grid-template-columns:repeat(3,minmax(0,1fr))}}.field{{grid-template-columns:1fr;gap:2px}}}}
</style></head><body>
<header class="top"><div class="wrap">
  <span class="pill">For approval</span>
  <h1>Persona Ads: Updated for Approval</h1>
  <p>For Scott Sleeme and Brittany Horner. Prepared by CEA Marketing, October 28, 2026. The four persona ads, updated so they carry no incentive. The persona campaign is a long-term awareness campaign, so the current offer lives on the landing pages instead, where it is a much easier update.</p>
  <nav>{"".join(nav)}<a href="#done">Send your answers</a></nav>
</div></header>
<main class="wrap">
  <div class="summary">
    <div><b>No incentive in the ads</b><span>No offer, no deadline. The ads stay the same when the offer changes.</span></div>
    <div><b>Offer on the landing pages</b><span>simplymitchellhomes.com/land and /math carry the November offer.</span></div>
    <div><b>New reel end cards</b><span>SimplyMitchell: zero down, closing costs paid, no construction loan.</span></div>
    <div><b>New carousel card 5</b><span>The same SimplyMitchell card in all four carousels. Cards 1 to 4 unchanged.</span></div>
  </div>
  {"".join(sections)}
  <section class="done" id="done">
    <h2>Send your answers</h2>
    <p style="margin:0;color:#d5e3d9">Mark each ad above, then copy your answers and send them to Kelly.</p>
    <input id="who" type="text" placeholder="Your name" aria-label="Your name">
    <button type="button" id="copy">Copy my answers</button>
    <pre id="out" hidden></pre>
  </section>
  <footer>Prepared by CEA Marketing for Mitchell Homes. Value Unlocker's reel now runs about 19 seconds, since the line about the earlier incentive is gone from its voiceover.</footer>
</main>
<script>
(function(){{
  var KEY='mitchell-persona-approval-v1',S={{}};
  try{{S=JSON.parse(localStorage.getItem(KEY)||'{{}}');}}catch(e){{}}
  function save(){{try{{localStorage.setItem(KEY,JSON.stringify(S));}}catch(e){{}}}}
  document.querySelectorAll('section.ver').forEach(function(sec){{
    var id=sec.id,ok=sec.querySelector('.ok'),no=sec.querySelector('.no'),ta=sec.querySelector('textarea');
    function paint(){{var v=(S[id]||{{}}).v;ok.classList.toggle('on',v==='Approved');no.classList.toggle('on',v==='Changes needed');ok.setAttribute('aria-pressed',v==='Approved');no.setAttribute('aria-pressed',v==='Changes needed');}}
    S[id]=S[id]||{{}};ta.value=S[id].n||'';paint();
    ok.onclick=function(){{S[id].v='Approved';save();paint();}};
    no.onclick=function(){{S[id].v='Changes needed';save();paint();}};
    ta.oninput=function(){{S[id].n=ta.value;save();}};
  }});
  document.getElementById('copy').onclick=function(){{
    var lines=['Persona ads approval, from '+(document.getElementById('who').value||'(name)')+':'];
    document.querySelectorAll('section.ver').forEach(function(sec){{var s=S[sec.id]||{{}};lines.push(sec.dataset.item+': '+(s.v||'Not marked')+(s.n?' ('+s.n+')':''));}});
    var t=lines.join('\\n'),o=document.getElementById('out');o.textContent=t;o.hidden=false;
    try{{navigator.clipboard.writeText(t).then(function(){{document.getElementById('copy').textContent='Copied';}},function(){{}});}}catch(e){{}}
  }};
}})();
</script></body></html>'''
if re.search(r"[–—]", page) or re.search(r"(?i)design dollars", page):
    raise SystemExit("dash or old incentive found")
open(f"{OUT}/index.html", "w").write(page)
open(f"{OUT}/vercel.json", "w").write('{"headers":[{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow"}]}]}\n')
print("built", OUT)
if "--deploy" in sys.argv:
    subprocess.run([sys.executable, f"{ROOT}/scripts/vercel_static_deploy.py", OUT, "mitchell-persona-ads-approval"], check=True)
