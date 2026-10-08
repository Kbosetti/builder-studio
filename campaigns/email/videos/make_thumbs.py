#!/usr/bin/env python3
"""Video thumbnails for the fall emails and website: each YouTube still above a green Watch the video bar.

usage: python3 campaigns/email/videos/make_thumbs.py            writes <key>.jpg and videos.json here
       GHL_PIT=... python3 campaigns/email/videos/make_thumbs.py --upload   also puts them in the Builder Studio
       media library and records each CDN URL in videos.json (email clients load images from there).
Email cannot play video, so every email shows the thumbnail and links to the video on YouTube.
The YouTube stills come from i.ytimg.com (src/), already Mitchell's own thumbnails: real homes and people,
never a painted portrait.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONT = f"{ROOT}/campaigns/print/src/montserrat.woff2"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"

VIDEOS = [  # key, YouTube id, title as the caption shows it, kind
    ("downey", "9vmi-miQzKU", "The Downey family, Henrico, Virginia", "Homeowner story"),
    ("cuomo", "jMSBzlcQ4uU", "The Cuomo family, from their land to move-in, Wilmington, North Carolina", "Homeowner story"),
    ("wellseptic", "zWwtw8qgp4w", "Well and Septic", "Behind the Build"),
    ("land101", "trgJ8maymOA", "Purchasing Land 101", "Behind the Build"),
    ("savings", "8e8mkV1rdzM", "SimplyMitchell Savings", "Behind the Build"),
    ("keys", "sfnU69Gdqcs", "Contract to Keys", "Behind the Build"),
    ("roadmap", "HEqg3pcNJkk", "Homebuyer Roadmap to Success", "Behind the Build"),
    ("misconceptions", "d7AZtCxOLro", "Common Misconceptions", "Behind the Build"),
    ("ferguson", "xOWIqiEFkFM", "From Showroom to Dream Home: Ferguson's selection tips", "Behind the Build"),
    ("mortgage", "mBb3CXBtO2w", "Mortgage 101", "Behind the Build"),
]

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:M;src:url('%s') format('woff2');font-weight:100 900}
html,body{margin:0;width:1200px;height:771px;overflow:hidden;background:#1e4f33;font-family:M,Arial,sans-serif}
.bg{position:absolute;left:0;top:0;width:1200px;height:675px;background:url('%s') center/cover}
.bar{position:absolute;left:0;top:675px;width:1200px;height:96px;display:flex;align-items:center;gap:22px;padding:0 34px;box-sizing:border-box}
.play{position:relative;flex:none;width:62px;height:62px;border-radius:50%%;background:#f5d053}
.play:after{content:"";position:absolute;left:24px;top:17px;border-style:solid;border-width:14px 0 14px 22px;border-color:transparent transparent transparent #1e4f33}
.w{color:#fff;font-size:32px;font-weight:800;letter-spacing:.2px}
.k{margin-left:auto;color:#f5d053;font-size:20px;font-weight:700;letter-spacing:3px;text-transform:uppercase}
</style></head><body><div class="bg"></div><div class="bar"><div class="play"></div><div class="w">Watch the video</div><div class="k">%s</div></div></body></html>"""


def main():
    os.makedirs(f"{HERE}/src", exist_ok=True)
    rec = json.load(open(f"{HERE}/videos.json")) if os.path.exists(f"{HERE}/videos.json") else {}
    jobs = []
    for key, yt, title, kind in VIDEOS:
        src = f"{HERE}/src/{yt}.jpg"
        if not os.path.exists(src):
            subprocess.run(["curl", "-sS", "--retry", "3", "-o", src, f"https://i.ytimg.com/vi/{yt}/maxresdefault.jpg"], check=True)
        html = f"{HERE}/src/{key}.html"
        open(html, "w").write(PAGE % (FONT, src, kind))
        jobs.append({"html": html, "png": f"{HERE}/src/{key}.png", "w": 1200, "h": 771, "scale": 1})
        rec.setdefault(key, {}).update({"youtube": yt, "url": f"https://www.youtube.com/watch?v={yt}", "title": title, "kind": kind, "thumb": f"{key}.jpg"})
    json.dump(jobs, open(f"{HERE}/src/jobs.json", "w"))
    subprocess.run(["node", f"{ROOT}/campaigns/print/render.js", f"{HERE}/src/jobs.json"], check=True,
                   env={**os.environ, "NODE_PATH": subprocess.check_output(["npm", "root", "-g"], text=True).strip()})
    for key, *_ in VIDEOS:
        subprocess.run([FF, "-loglevel", "error", "-y", "-i", f"{HERE}/src/{key}.png", "-q:v", "3", f"{HERE}/{key}.jpg"], check=True)
    if "--upload" in sys.argv:
        upload(rec)
    json.dump(rec, open(f"{HERE}/videos.json", "w"), indent=1, ensure_ascii=False)
    print(len(VIDEOS), "thumbnails;", sum(1 for v in rec.values() if v.get("cdn")), "in the media library")


def upload(rec):
    """POST /medias/upload-file for any thumbnail not yet in the media library."""
    tok = os.environ["GHL_PIT"]
    for key, v in rec.items():
        if v.get("cdn"):
            continue
        for attempt in range(4):
            r = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-H", f"Authorization: Bearer {tok}", "-H", "Version: 2021-07-28",
                                "-F", f"file=@{HERE}/{key}.jpg;type=image/jpeg", "-F", f"name=fall26-video-{key}.jpg",
                                "https://services.leadconnectorhq.com/medias/upload-file"],
                               capture_output=True, text=True)
            try:
                d = json.loads(r.stdout)
                v["cdn"] = d.get("url") or d.get("fileUrl") or d["data"]["url"]
                print("uploaded", key, v["cdn"])
                break
            except Exception:
                print("retry", key, r.stdout[:200])
        else:
            raise SystemExit(f"upload failed for {key}")


if __name__ == "__main__":
    main()
