#!/usr/bin/env python3
"""Pull the four Home Portrait reels from the Builder Studio media library into the campaign guide.

usage: GHL_PIT=... python3 campaign-guide/fetch_reels.py      then build.py, publish and deploy.py
Finds the newest video file whose name matches each reel (land, space, which, saturday), downloads it to
reels/<key>.mp4, makes a poster from the frame at three seconds (reels/<key>.jpg), and writes reels/reels.json,
which build.py turns into the "The reels" row in the Home Portrait section. The titles, tags and the
organic-only note match the Home Portrait ad kit (https://claude.ai/artifact/MVB65BDPo5Zr9zCLJPpaft).
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = f"{HERE}/reels"
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
REELS = [  # key, how the file name usually reads, title, tag, note
    ("land", r"land", "Your Land", "Paid and organic", ""),
    ("space", r"space", "A Space of You", "Paid and organic", ""),
    ("which", r"which", "Which One Are You?", "Paid and organic", ""),
    ("saturday", r"saturday", "Saturday Morning", "Organic only", "Shows children, so it runs organically, never as a paid Meta housing ad."),
]


def media_videos():
    tok = os.environ["GHL_PIT"]
    base = ("https://services.leadconnectorhq.com/medias/files?altId=5o5zLlUPPizy6Ajp61oF&altType=location"
            "&sortBy=createdAt&sortOrder=desc&limit=100")

    def get(q):
        r = subprocess.run(["curl", "-sS", "--retry", "3", "-A", "Mozilla/5.0", "-H", f"Authorization: Bearer {tok}",
                            "-H", "Version: 2021-07-28", base + q], capture_output=True, text=True)
        return json.loads(r.stdout).get("files", [])
    found = [f for f in get("&type=file")]
    for folder in get("&type=folder"):
        found += get(f"&type=file&parentId={folder['_id']}")
    return [f for f in found if "video" in str(f.get("contentType", "")) or str(f.get("name", "")).lower().endswith((".mp4", ".mov"))]


def main():
    os.makedirs(OUT, exist_ok=True)
    vids = media_videos()
    rows, missing = [], []
    for key, pat, title, tag, note in REELS:
        match = next((v for v in vids if re.search(pat, v["name"], re.I)), None)
        if not match:
            missing.append(title)
            continue
        mp4 = f"{OUT}/{key}.mp4"
        subprocess.run(["curl", "-sS", "--retry", "5", "-o", mp4, match["url"]], check=True)
        if not match["name"].lower().endswith(".mp4"):  # a .mov from a phone: make a web-friendly mp4
            subprocess.run([FF, "-loglevel", "error", "-y", "-i", mp4, "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
                            "-c:a", "aac", "-movflags", "+faststart", mp4 + ".tmp.mp4"], check=True)
            os.replace(mp4 + ".tmp.mp4", mp4)
        subprocess.run([FF, "-loglevel", "error", "-y", "-ss", "3", "-i", mp4, "-frames:v", "1", "-vf", "scale=540:-2", "-q:v", "4",
                        f"{OUT}/{key}.jpg"], check=True)
        rows.append({"key": key, "title": title, "tag": tag, "note": note, "organic_only": tag == "Organic only", "source": match["name"]})
        print("got", title, "from", match["name"], os.path.getsize(mp4) // 1024, "KB")
    if missing:
        print("not in the media library yet:", ", ".join(missing), "| videos there:", [v["name"] for v in vids])
    if rows:
        json.dump(rows, open(f"{OUT}/reels.json", "w"), indent=1)
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
