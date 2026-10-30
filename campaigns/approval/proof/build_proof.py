#!/usr/bin/env python3
"""Small proofing batches for Mitchell: a few pieces at a time, so Brittany is never handed the whole fall at once.

usage: python3 campaigns/email/build.py && python3 campaigns/direct/make_direct.py
       python3 campaigns/approval/proof/build_proof.py [--deploy]      (--deploy needs VERCEL_TOKEN)
The order of approval: Kelly reviews the batch page first, CEA loads the approved pieces into Builder Studio as drafts
and sends a proof email and text to Kelly and Tom, then Kelly sends Brittany the same page. Each batch lives at
https://mitchell-content-approval.vercel.app/batch-N/ (noindex). Emails show exactly as they arrive (the built HTML
in an iframe), texts as phone messages, website pieces as screenshots or a mock bar. Approvals stay in each
reviewer's browser and come back through the Copy my answers button.
"""
import html, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(C)
OUT = f"{HERE}/out"
E = html.escape

# Each piece: ("email", email id) · ("text", text title prefix in direct.json) · ("bar", announcement bar title) · ("popup", "")
BATCHES = [
    {"n": 1, "name": "The November offer, the Home Portrait and landowners",
     "dates": "Sends Wednesday, November 4 to Friday, November 13",
     "approve_by": "Monday, November 2",
     "intro": "Seven pieces: three emails, two texts and two website pieces. The November offer goes to the whole database first, while it runs. "
              "Landowners hear that their land can be their down payment, and engaged contacts are invited to the Home Portrait.",
     "pieces": [("email", "no1"), ("text", "SMS 1"), ("email", "fb1"), ("email", "hp1"), ("text", "SMS 2"),
                ("bar", "Website announcement bar, November offer"), ("popup", "")]},
]

emails = {e["id"]: e for e in json.load(open(f"{C}/email/out/emails.json"))["emails"]}
direct = {s["id"]: s for s in json.load(open(f"{C}/direct/direct.json"))["sections"]}
texts = {it["title"].split(" · ")[0]: it for it in direct["sms"]["items"]}
web = {it["title"]: it for it in direct["website"]["items"]}
AUD_TEXT = "Contacts who agreed to texts, minus anyone who opened that week's email, took the quiz, or is already talking with a consultant. Sent between 10am and 7pm local time."


def approve(pid, label):
    return (f'<div class="approve"><span>{E(label)}</span><button type="button" class="ok">Approved</button>'
            f'<button type="button" class="no">Changes needed</button>'
            f'<textarea placeholder="Notes or changes (optional)" aria-label="Notes for {E(label)}"></textarea></div>')


def facts(rows):
    return "".join(f'<div class="field"><div class="flabel">{E(a)}</div><div class="fval">{b}</div></div>' for a, b in rows if b)


def link(url):
    return f'<a href="{E(url)}" target="_blank" rel="noopener">{E(url.split("?")[0])}</a>'


def piece(kind, key, n, idx, out):
    pid = f"b{n}p{idx}"
    if kind == "email":
        e = emails[key]
        shutil.copy(f"{C}/email/out/{key}.html", f"{out}/emails/{key}.html")
        hold = f'<p class="hold">{E(e["hold"])}</p>' if e.get("hold") else ""
        rows = [("Send", E(e["send"])), ("To", E(e["segment"])), ("Subject", E(e["subject"])), ("Preview text", E(e["preview"])),
                ("From", "Mitchell Homes")]
        title = f'Email: {e["subject"]}'
        body = (f'<div class="cols"><div class="copy">{facts(rows)}<p class="tip">The email shows exactly as it arrives, live images and working links. '
                f'<a href="emails/{key}.html" target="_blank" rel="noopener">Open it full size</a>.</p></div>'
                f'<div class="mail"><iframe src="emails/{key}.html" title="{E(title)}" loading="lazy" scrolling="no"></iframe></div></div>')
        return pid, title, f"Email · {e['series_name']}", hold, body
    if kind == "text":
        t = texts[key]
        when, _, rest = t["meta"].partition(" · ")
        chars = re.search(r"(\d+) of 160", rest).group(1)
        msg = E(t["body"]).replace("[trigger link]", '<u>mitchl.co/link</u>')
        rows = [("Send", E(when)), ("To", E(AUD_TEXT)), ("Length", f"{chars} of 160 characters, one text"),
                ("Link goes to", link(t["link"]) if t["link"] else "No link: the text invites a reply")]
        title = f'Text: {t["title"].split(" · ")[1]}'
        body = (f'<div class="cols"><div class="phone" aria-label="The text as it arrives"><p class="from">Mitchell Homes</p><p class="bubble">{msg}</p></div>'
                f'<div class="copy">{facts(rows)}<p class="tip">The link is a short Builder Studio link, so every click is tracked to the person who tapped it.</p></div></div>')
        return pid, title, "Text message", "", body
    if kind == "bar":
        w = web[key]
        text, _, cta = w["body"].rpartition(". ")
        rows = [("Where", E(w["meta"])), ("Link goes to", link(w["link"]))]
        title = w["title"]
        body = (f'<div class="bar" role="img" aria-label="The announcement bar as it appears on the website">{E(text)}. <u>{E(cta)}</u></div>'
                f'<div class="copy">{facts(rows)}</div>')
        return pid, title, "Website · mitchellhomesinc.com", "", body
    if kind == "popup":
        for name in ("popup-open-desktop", "popup-open-phone"):
            shutil.copy(f"{C}/kit/out/website/{name}.jpg", f"{out}/img/{name}.jpg")
        rows = [("Where", "mitchellhomesinc.com, every page that does not already link the quiz"),
                ("When it opens", "After 15 seconds on a page or halfway down it, whichever comes first. Once closed, it stays away for 14 days."),
                ("Button goes to", link("https://mitchellhomesliving.com/portrait"))]
        title = "Website pop-up: the Home Portrait"
        body = (f'<div class="shots"><figure><img src="img/popup-open-desktop.jpg" alt="The Home Portrait pop-up open on a desktop page" loading="lazy">'
                f'<figcaption>Desktop</figcaption></figure><figure class="ph"><img src="img/popup-open-phone.jpg" alt="The Home Portrait pop-up on a phone" loading="lazy">'
                f'<figcaption>Phone</figcaption></figure></div><div class="copy">{facts(rows)}</div>')
        return pid, title, "Website · mitchellhomesinc.com", "", body
    raise SystemExit(f"unknown piece {kind}")


CSS = """
:root{--green:#2b6d47;--deep:#1e4f33;--yellow:#f5d053;--ink:#1d2a22;--muted:#5b6b61;--paper:#fbfaf5;--soft:#f1f5f2;--line:#dfe6e1;--white:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.6 Montserrat,system-ui,Arial,sans-serif}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left));padding-right:max(16px,env(safe-area-inset-right))}
header.top{background:var(--deep);color:var(--white)}
header.top .wrap{padding-block:40px;display:grid;gap:12px}
header.top h1{margin:0;font-size:clamp(28px,5vw,44px);line-height:1.1;text-wrap:balance}
header.top p{margin:0;color:#d5e3d9;max-width:54em}
.pill{display:inline-block;background:var(--yellow);color:var(--deep);font-weight:800;font-size:13px;letter-spacing:.08em;text-transform:uppercase;padding:6px 14px;border-radius:999px;justify-self:start}
nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
nav a{color:var(--white);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:6px 14px;font-weight:600;font-size:14px;text-decoration:none}
.eyebrow{margin:0;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--green)}
h2{margin:0;font-size:clamp(22px,3.2vw,30px);color:var(--deep);line-height:1.2;text-wrap:balance}
.how{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:28px;counter-reset:s}
.how div{background:var(--white);border:1px solid var(--line);border-radius:14px;padding:16px;min-width:0}
.how b{display:block;color:var(--deep);font-size:16px;line-height:1.3;margin-bottom:4px}
.how b::before{counter-increment:s;content:counter(s) ". "}
.how span{color:var(--muted);font-size:14px}
.ver{background:var(--white);border:1px solid var(--line);border-radius:20px;padding:28px;margin-top:28px;display:grid;gap:20px;scroll-margin-top:16px;min-width:0}
.sechead{display:grid;gap:6px}
.hold{margin:0;background:#fff4d6;color:#6b4f00;border-radius:10px;padding:8px 12px;font-size:14px;font-weight:600}
.cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,640px);gap:28px;align-items:start}
.cols .phone{order:0}
.copy{display:grid;min-width:0}
.field{display:grid;grid-template-columns:130px minmax(0,1fr);gap:14px;padding:12px 0;border-top:1px solid var(--line)}
.flabel{font-weight:700;color:var(--deep);font-size:14px}
.fval{overflow-wrap:anywhere;font-size:15px}
.fval a{color:var(--green);font-weight:600}
.tip{margin:8px 0 0;font-size:14px;color:var(--muted)}
.tip a{color:var(--green);font-weight:700}
.mail{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#eef1ee}
.mail iframe{display:block;width:100%;height:900px;border:0;background:#fff}
.phone{justify-self:center;width:100%;max-width:340px;background:#f2f2f4;border-radius:28px;padding:22px 16px 30px;border:1px solid var(--line)}
.from{margin:0 0 10px;text-align:center;font-size:13px;font-weight:700;color:#555}
.bubble{margin:0;background:#e5e5ea;color:#111;border-radius:18px;padding:10px 14px;font:15px/1.4 -apple-system,system-ui,Arial,sans-serif;max-width:88%}
.bubble u{color:#0a5bd3}
.bar{background:var(--deep);color:var(--white);text-align:center;padding:12px 16px;border-radius:10px;font-weight:600;font-size:15px}
.bar u{color:var(--yellow);font-weight:800}
.shots{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,1fr);gap:16px;align-items:start}
figure{margin:0;display:grid;gap:6px;min-width:0}
figure img{width:100%;border-radius:12px;border:1px solid var(--line);display:block}
figcaption{font-size:13px;color:var(--muted);font-weight:600}
.approve{display:flex;flex-wrap:wrap;gap:10px;align-items:center;background:var(--soft);border-radius:12px;padding:12px 16px;font-weight:700;color:var(--deep)}
.approve span{flex:1;min-width:200px}
.approve button{font:inherit;font-size:14px;border:2px solid var(--green);border-radius:8px;padding:6px 14px;font-weight:700;color:var(--green);background:var(--white);cursor:pointer;min-height:40px}
.approve button.on.ok{background:var(--green);color:var(--white)}
.approve button.on.no{background:#6b4f00;border-color:#6b4f00;color:var(--white)}
.approve textarea{flex-basis:100%;font:inherit;font-size:14px;font-weight:400;min-height:56px;border:1px solid var(--line);border-radius:8px;padding:8px 10px}
button:focus-visible,a:focus-visible,textarea:focus-visible,input:focus-visible{outline:3px solid var(--yellow);outline-offset:2px}
.done{background:var(--deep);color:var(--white);border-radius:20px;padding:28px;margin:28px 0 48px;display:grid;gap:12px}
.done h2{color:var(--white)}
.done input{font:inherit;padding:8px 10px;border-radius:8px;border:0;max-width:340px;width:100%}
.done button{justify-self:start;font:inherit;font-weight:800;background:var(--yellow);color:var(--deep);border:0;border-radius:999px;padding:10px 20px;cursor:pointer}
.done pre{white-space:pre-wrap;background:rgba(255,255,255,.08);border-radius:10px;padding:12px;font-size:13px;margin:0;overflow-wrap:anywhere}
footer{color:var(--muted);font-size:13px;padding-bottom:40px}
@media (max-width:860px){.how{grid-template-columns:repeat(2,minmax(0,1fr))}.cols{grid-template-columns:1fr}.field{grid-template-columns:1fr;gap:2px}.shots{grid-template-columns:1fr}.shots .ph{max-width:260px}.ver{padding:20px}}
"""

JS = """
(function(){
  var KEY='mitchell-content-batch-%N%',S={};
  try{S=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}}
  document.querySelectorAll('.mail iframe').forEach(function(f){
    function fit(){try{var h=f.contentDocument.documentElement.scrollHeight;if(h>200)f.style.height=h+'px';}catch(e){}}
    f.addEventListener('load',function(){fit();setTimeout(fit,800);setTimeout(fit,2500);});
  });
  document.querySelectorAll('section.ver').forEach(function(sec){
    var id=sec.id,ok=sec.querySelector('.ok'),no=sec.querySelector('.no'),ta=sec.querySelector('textarea');
    function paint(){var v=(S[id]||{}).v;ok.classList.toggle('on',v==='Approved');no.classList.toggle('on',v==='Changes needed');ok.setAttribute('aria-pressed',v==='Approved');no.setAttribute('aria-pressed',v==='Changes needed');}
    S[id]=S[id]||{};ta.value=S[id].n||'';paint();
    ok.onclick=function(){S[id].v='Approved';save();paint();};
    no.onclick=function(){S[id].v='Changes needed';save();paint();};
    ta.oninput=function(){S[id].n=ta.value;save();};
  });
  document.getElementById('copy').onclick=function(){
    var lines=['Batch %N% approval, from '+(document.getElementById('who').value||'(name)')+':'];
    document.querySelectorAll('section.ver').forEach(function(sec){var s=S[sec.id]||{};lines.push(sec.dataset.item+': '+(s.v||'Not marked')+(s.n?' ('+s.n+')':''));});
    var t=lines.join('\\n'),o=document.getElementById('out');o.textContent=t;o.hidden=false;
    try{navigator.clipboard.writeText(t).then(function(){document.getElementById('copy').textContent='Copied';},function(){});}catch(e){}
  };
})();
"""


def build(B):
    n = B["n"]
    out = f"{OUT}/batch-{n}"
    os.makedirs(f"{out}/emails"); os.makedirs(f"{out}/img")
    secs, nav = [], []
    for idx, (kind, key) in enumerate(B["pieces"], 1):
        pid, title, eyebrow, hold, body = piece(kind, key, n, idx, out)
        nav.append(f'<a href="#{pid}">{idx}. {E(title.split(": ", 1)[0])}</a>')
        secs.append(f'<section class="ver" id="{pid}" data-item="{idx}. {E(title)}"><div class="sechead"><p class="eyebrow">{idx} of {len(B["pieces"])} · {E(eyebrow)}</p>'
                    f'<h2>{E(title)}</h2>{hold}</div>{body}{approve(pid, "Approve this piece")}</section>')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><title>Mitchell Content Batch {n}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap">
<style>{CSS}</style></head><body>
<header class="top"><div class="wrap">
  <span class="pill">Batch {n} · for approval</span>
  <h1>{E(B["name"])}</h1>
  <p>For Brittany Horner. Prepared by CEA Marketing. {E(B["dates"])}. Please approve by {E(B["approve_by"])}. {E(B["intro"])}</p>
  <nav>{"".join(nav)}<a href="#done">Send your answers</a></nav>
</div></header>
<main class="wrap">
  <div class="how">
    <div><b>Kelly approves</b><span>CEA's own review comes first, so only finished pieces reach you.</span></div>
    <div><b>Loaded and tested</b><span>Each piece goes into Builder Studio as a draft, and a test email and text go to Kelly and Tom.</span></div>
    <div><b>You approve</b><span>Mark each piece below. Notes are welcome on anything.</span></div>
    <div><b>Scheduled</b><span>Approved pieces are scheduled for the dates shown. Nothing sends before your OK.</span></div>
  </div>
  {"".join(secs)}
  <section class="done" id="done">
    <h2>Send your answers</h2>
    <p style="margin:0;color:#d5e3d9">Mark each piece above, then copy your answers and send them to Kelly. Your marks stay in this browser, so you can come back and finish later.</p>
    <input id="who" type="text" placeholder="Your name" aria-label="Your name">
    <button type="button" id="copy">Copy my answers</button>
    <pre id="out" hidden></pre>
  </section>
  <footer>Prepared by CEA Marketing for Mitchell Homes. Dates are proposals and move with approval. The November offer pieces carry Mitchell's approved wording and disclaimer.</footer>
</main>
<script>{JS.replace("%N%", str(n))}</script></body></html>"""
    if re.search(r"[–—]", page):
        raise SystemExit(f"dash found in batch {n}")
    for banned in ("Design Dollars", "HighLevel", "CEA Marketing Group", "Value Unlocker", "Grounded Dreamer", "Simply Mitchell"):
        if banned in page:
            raise SystemExit(f"batch {n} contains {banned!r}")
    open(f"{out}/index.html", "w").write(page)
    print(f"batch-{n}: {len(B['pieces'])} pieces")


shutil.rmtree(OUT, ignore_errors=True)
for B in BATCHES:
    build(B)
open(f"{OUT}/index.html", "w").write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>Mitchell Content Batches</title>'
                                     '<meta http-equiv="refresh" content="0; url=batch-1/"><a href="batch-1/">Batch 1</a>')
open(f"{OUT}/vercel.json", "w").write('{"headers":[{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow"}]}]}\n')
if "--deploy" in sys.argv:
    subprocess.run([sys.executable, f"{ROOT}/scripts/vercel_static_deploy.py", OUT, "mitchell-content-approval"], check=True)
