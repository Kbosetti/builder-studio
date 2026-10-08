#!/usr/bin/env python3
"""Turn an exported deck into slide images and notes for the guide's deck viewer.

usage: python3 campaign-guide/prepare_decks.py <key> <deck.pdf> [<notes>]
  <notes> is the deck's .pptx export (Google Slides) or a JSON list of notes, one per slide (Canva).
Writes decks/<key>/NN.jpg (1600 wide), decks/<key>/tNN.jpg (thumbnail) and decks/<key>.json, which
build.py folds into the page. Re-run after re-exporting a deck; deck titles live in src.html.
"""
import json, os, re, sys, zipfile
from urllib.parse import parse_qs, urlparse
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
# concept pages that still carry reviewer build notes; never linked from the guide
SKIP_HOSTS = ("cea-mitchell-landing-pages-cea-marketing.vercel.app",)

def pptx_notes(path):
    z = zipfile.ZipFile(path)
    rels = lambda p: {a["Id"]: a["Target"] for a in (dict(re.findall(r'(\w+)="([^"]*)"', m))
                      for m in re.findall(r"<Relationship ([^>]+)/>", z.read(p).decode()))} if p in z.namelist() else {}
    prels = rels("ppt/_rels/presentation.xml.rels")
    order = [prels[r] for r in re.findall(r'<p:sldId [^>]*r:id="(\w+)"', z.read("ppt/presentation.xml").decode())]
    notes = []
    for target in order:
        n = next((t for t in rels(f"ppt/slides/_rels/{os.path.basename(target)}.rels").values() if "notesSlide" in t), None)
        text = ""
        if n:
            xml = z.read(os.path.normpath(f"ppt/slides/{n}")).decode()
            paras = []
            for p in re.findall(r"<a:p>.*?</a:p>", xml, flags=re.S):
                p = re.sub(r"<a:br/>|<a:br>.*?</a:br>", "<a:t>\n</a:t>", p, flags=re.S)
                paras.append("".join(re.findall(r"<a:t>([^<]*)</a:t>", p)))
            text = "\n".join(x for x in paras if x.strip() and x.strip() != "‹#›" and not x.strip().isdigit())
        for a, b in (("&amp;", "&"), ("&quot;", '"'), ("&apos;", "'"), ("&lt;", "<"), ("&gt;", ">")):
            text = text.replace(a, b)
        notes.append(re.sub(r"\n{3,}", "\n\n", text).strip())
    return notes

def main(key, pdf, notes_src=None):
    out = f"{HERE}/decks/{key}"
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(pdf)
    if notes_src and notes_src.endswith(".pptx"):
        notes = pptx_notes(notes_src)
    elif notes_src:
        notes = json.load(open(notes_src))
    else:
        notes = []
    slides = []
    for i, page in enumerate(doc):
        n = i + 1
        for name, width, q in ((f"{n:02d}.jpg", 1600, 80), (f"t{n:02d}.jpg", 360, 72)):
            z = width / page.rect.width
            page.get_pixmap(matrix=pymupdf.Matrix(z, z)).save(f"{out}/{name}", jpg_quality=q)
        links = []
        for l in page.get_links():
            u = l.get("uri") or ""
            if u.startswith("https://www.google.com/url?"):  # Google Slides wraps every link in a redirect
                u = parse_qs(urlparse(u).query).get("q", [""])[0]
            u = u.rstrip(".")
            if u.startswith("http") and not any(h in u for h in SKIP_HOSTS) and u not in links:
                links.append(u)
        slides.append({"notes": notes[i] if i < len(notes) else "", "links": links})
    json.dump({"count": len(slides), "slides": slides}, open(f"{HERE}/decks/{key}.json", "w"), indent=1, ensure_ascii=False)
    size = sum(os.path.getsize(f"{out}/{f}") for f in os.listdir(out))
    print(f"{key}: {len(slides)} slides, {size // 1024} KB, notes on {sum(1 for s in slides if s['notes'])}")

if __name__ == "__main__":
    main(*sys.argv[1:])
