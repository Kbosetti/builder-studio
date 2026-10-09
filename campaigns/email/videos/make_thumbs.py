#!/usr/bin/env python3
"""Video thumbnails for the fall emails and website: each YouTube still above a green Watch the video bar.

usage: python3 campaigns/email/videos/make_thumbs.py            writes <key>.jpg and videos.json here
       GHL_PIT=... python3 campaigns/email/videos/make_thumbs.py --upload   also puts them in the Builder Studio
       media library and records each CDN URL in videos.json (email clients load images from there).
Email cannot play video, so every email shows the thumbnail and links to the video on YouTube. The four Home
Portrait reels (vertical, hosted in the Builder Studio media library) get a widescreen card: the reel's frame at
three seconds, centered over a blurred copy of itself, with a "Watch the reel" bar; their posters go to the media
library too, for the website.
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

CDN = "https://assets.cdn.filesafe.space/5o5zLlUPPizy6Ajp61oF/media/"
REELS = [  # key, the reel in the media library (uploaded by Kelly from the Home Portrait ad kit), title, guide file
    ("reel_land", CDN + "6ac8218f89da6e6f9bc29a28.mp4", "Your Land", "land"),
    ("reel_space", CDN + "6ac8218f6fdae56241ba2f34.mp4", "A Space of You", "space"),
    ("reel_which", CDN + "6ac8218f02ee523cd5edbece.mp4", "Which One Are You?", "which"),
    ("reel_saturday", CDN + "6ac8218f195f9172edfef8b0.mp4", "Saturday Morning", "saturday"),
]
REEL_PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:M;src:url('%s') format('woff2');font-weight:100 900}
html,body{margin:0;width:1200px;height:771px;overflow:hidden;background:#1e4f33;font-family:M,Arial,sans-serif}
.clip{position:absolute;left:0;top:0;width:1200px;height:675px;overflow:hidden}
.bg{position:absolute;inset:-60px;background:url('%s') center/cover;filter:blur(30px) brightness(.55)}
.reel{position:absolute;left:410px;top:0;width:380px;height:675px;background:url('%s') center/cover;box-shadow:0 0 60px rgba(0,0,0,.5)}
.bar{position:absolute;left:0;top:675px;width:1200px;height:96px;display:flex;align-items:center;gap:22px;padding:0 34px;box-sizing:border-box}
.play{position:relative;flex:none;width:62px;height:62px;border-radius:50%%;background:#f5d053}
.play:after{content:"";position:absolute;left:24px;top:17px;border-style:solid;border-width:14px 0 14px 22px;border-color:transparent transparent transparent #1e4f33}
.w{color:#fff;font-size:32px;font-weight:800;letter-spacing:.2px}
.k{margin-left:auto;color:#f5d053;font-size:20px;font-weight:700;letter-spacing:3px;text-transform:uppercase}
</style></head><body><div class="clip"><div class="bg"></div><div class="reel"></div></div><div class="bar"><div class="play"></div><div class="w">Watch the reel</div><div class="k">The Home Portrait</div></div></body></html>"""

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
    for key, mp4url, title, gkey in REELS:
        mp4 = f"{ROOT}/campaign-guide/reels/{gkey}.mp4"
        if not os.path.exists(mp4):
            mp4 = f"{HERE}/src/{key}.mp4"
            if not os.path.exists(mp4):
                subprocess.run(["curl", "-sS", "--retry", "5", "-o", mp4, mp4url], check=True)
        frame = f"{HERE}/src/{key}_frame.jpg"
        subprocess.run([FF, "-loglevel", "error", "-y", "-ss", "3", "-i", mp4, "-frames:v", "1", "-q:v", "2", frame], check=True)
        subprocess.run([FF, "-loglevel", "error", "-y", "-i", frame, "-vf", "scale=540:-2", "-q:v", "3", f"{HERE}/{key}_poster.jpg"], check=True)
        html = f"{HERE}/src/{key}.html"
        open(html, "w").write(REEL_PAGE % (FONT, frame, frame))
        jobs.append({"html": html, "png": f"{HERE}/src/{key}.png", "w": 1200, "h": 771, "scale": 1})
        rec.setdefault(key, {}).update({"url": mp4url, "title": title, "kind": "Home Portrait reel", "thumb": f"{key}.jpg", "poster": f"{key}_poster.jpg"})
    json.dump(jobs, open(f"{HERE}/src/jobs.json", "w"))
    subprocess.run(["node", f"{ROOT}/campaigns/print/render.js", f"{HERE}/src/jobs.json"], check=True,
                   env={**os.environ, "NODE_PATH": subprocess.check_output(["npm", "root", "-g"], text=True).strip()})
    for key, *_ in VIDEOS + REELS:
        subprocess.run([FF, "-loglevel", "error", "-y", "-i", f"{HERE}/src/{key}.png", "-q:v", "3", f"{HERE}/{key}.jpg"], check=True)
    if "--upload" in sys.argv:
        upload(rec)
    json.dump(rec, open(f"{HERE}/videos.json", "w"), indent=1, ensure_ascii=False)
    print(len(VIDEOS) + len(REELS), "thumbnails;", sum(1 for v in rec.values() if v.get("cdn")), "in the media library")


def send(path, name):
    tok = os.environ["GHL_PIT"]
    for attempt in range(4):
        r = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-H", f"Authorization: Bearer {tok}", "-H", "Version: 2021-07-28",
                            "-F", f"file=@{path};type=image/jpeg", "-F", f"name={name}", "https://services.leadconnectorhq.com/medias/upload-file"],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            return d.get("url") or d.get("fileUrl") or d["data"]["url"]
        except Exception:
            pass
    raise SystemExit(f"upload failed for {name}")


def upload(rec):
    """POST /medias/upload-file for any thumbnail not yet in the media library."""
    tok = os.environ["GHL_PIT"]
    for key, v in rec.items():
        if v.get("poster") and not v.get("poster_cdn"):
            v["poster_cdn"] = send(f"{HERE}/{v['poster']}", f"fall26-reel-poster-{key}.jpg")
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
