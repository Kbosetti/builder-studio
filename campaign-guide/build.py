#!/usr/bin/env python3
"""Build the Mitchell Fall Campaign Guide page (one self-contained HTML file).

usage: python3 campaign-guide/build.py      writes campaign-guide/out/index.html
Edit src.html, drop new images in img/ and reference them as %%img:<file>%%. Decks come from
prepare_decks.py (decks/<key>.json plus slide images). Publish out/index.html to the existing artifact
(see CLAUDE.md) with root campaign-guide and every decks/<key>/*.jpg and reels/*.mp4 in `files`, so the slides
and reels load
and the team's link stays the same.
"""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".woff2": "font/woff2"}
EXT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')

def uri(path):
    return f"data:{MIME[os.path.splitext(path)[1].lower()]};base64," + base64.b64encode(open(path, "rb").read()).decode()

src = open(f"{HERE}/src.html").read()
src = src.replace("%%ext%%", EXT)
src = src.replace("%%charlotte%%", uri(f"{HERE}/../home-portrait/fonts/charlotte.woff2"))
src = re.sub(r"%%img:([\w.-]+)%%", lambda m: uri(f"{HERE}/img/{m.group(1)}"), src)
# decks: cover thumbnails inline, notes and links as data; the slide images publish as separate files
DECKS = ("hp", "fb", "dd")
src = re.sub(r"%%thumb:(\w+)%%", lambda m: uri(f"{HERE}/decks/{m.group(1)}/t01.jpg"), src)
decks = {k: json.load(open(f"{HERE}/decks/{k}.json")) for k in DECKS}
src = re.sub(r"%%count:(\w+)%%", lambda m: str(decks[m.group(1)]["count"]), src)
src = src.replace("%%decks%%", json.dumps(decks, ensure_ascii=False).replace("</", "<\\/"))
# reels: reels/reels.json plus reels/<key>.mp4 and <key>.jpg (fetch_reels.py); videos publish as separate files
def reels_html():
    path = f"{HERE}/reels/reels.json"
    if not os.path.exists(path):
        return ""
    cards = ""
    for r in json.load(open(path)):
        key, title = r["key"], r["title"]
        poster = uri(f"{HERE}/reels/{key}.jpg")
        note = f"<small>{r['note']}</small>" if r.get("note") else ""
        pill = "soon" if r.get("organic_only") else "live"
        cards += (f'<figure class="reel"><div class="rv"><video data-src="reels/{key}.mp4" poster="{poster}" '
                  f'playsinline preload="none" aria-label="{title} reel"></video><button class="rplay" type="button" aria-label="Play {title}">'
                  f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></button></div>'
                  f'<figcaption><b>{title}</b><span class="pill {pill}">{r["tag"]}</span>{note}</figcaption></figure>')
    return ('<div class="head"><h3>The reels</h3><p class="hint">Vertical, captions burned in, for Reels, Stories, TikTok and Shorts. Tap one to play it.</p></div>'
            f'<div class="reels">{cards}</div>'
            '<script>(function(){[].forEach.call(document.querySelectorAll(".reel"),function(f){var v=f.querySelector("video"),b=f.querySelector(".rplay");'
            'b.addEventListener("click",function(){b.hidden=true;[].forEach.call(document.querySelectorAll(".reel video"),function(o){if(o!==v)o.pause();});'
            'var go=function(){v.controls=true;var p=v.play();if(p&&p.catch)p.catch(function(){b.hidden=false;});};if(v.src)return go();'
            'fetch(v.dataset.src).then(function(r){if(!r.ok)throw 0;return r.blob();}).then(function(x){v.src=URL.createObjectURL(new Blob([x],{type:"video/mp4"}));go();})'
            '.catch(function(){v.src=v.dataset.src;go();});});});})();</script>')
src = src.replace("%%reels%%", reels_html())
left = re.findall(r"%%[\w:.-]+%%", src)
assert not left, left
os.makedirs(f"{HERE}/out", exist_ok=True)
open(f"{HERE}/out/index.html", "w").write(src)
print(f"wrote out/index.html, {len(src) // 1024} KB")
