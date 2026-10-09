#!/usr/bin/env python3
"""Animated hero images for the designed emails: four real Mitchell photos, one after another.

usage: GHL_PIT=... python3 campaigns/email/hero_gifs.py      then build.py
Each GIF opens on the email's own hero photo (Outlook on Windows shows only the first frame, so it still reads
right there), then cuts to three more photos chosen for that email, 2.4 seconds each, looping. 900 x 480
(1.5 times the 600 pixel email width, so it stays sharp on phones and retina screens) with its own color palette
per photo, clean cuts rather than fades, about 1 MB each. The GIFs go into the Builder Studio
media library and gifs.json records each URL; build.py uses the GIF wherever one exists. Photos come only from
Mitchell's own site (media.mitchellhomesinc.com): real homes, porches, kitchens and Design Centers, never a
painted portrait.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from series import SERIES  # noqa: E402
from build import expand  # noqa: E402

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
M = "https://media.mitchellhomesinc.com/276/"
SRC, OUT = f"{HERE}/gifs/src", f"{HERE}/gifs"
HOLD = 2.4
W, H = 900, 480
VERSION = "900px-per-frame-palette"

P = {  # the photo pool, by what is in the picture
    "farmhouse_field": "2022/10/7/Exterior_1.jpg", "farmhouse_drive": "2022/6/3/Exterior_SideView_copy.jpg",
    "porch_planks": "2022/6/3/Exterior_2_fU4xlYm.jpg", "screen_porch": "2022/7/1/8_Screen_Porch_6_49nxwnw.jpg",
    "kitchen_white": "2023/11/22/11-print-011.jpg", "kitchen_island": "2023/11/22/25-print-_DSC7636.jpg",
    "kitchen_quartz": "2023/11/22/7_Ava_Craftsman_Interior.jpg", "aerial_pond": "2023/3/16/Editted-_1_Exterior_-_Aerial_3.jpg",
    "aerial_hills": "2023/3/16/10_95fZm72.jpg", "porch_view": "2023/7/3/5-print-005.jpg", "aerial_lake": "2024/1/18/10.jpg",
    "drive_trees": "2024/12/3/8.jpg", "breakfast_nook": "2024/5/20/Mitchell_-_Breakfast_Nook.jpg", "coastal_dusk": "2024/6/10/Web_Image_7.jpg",
    "living_open": "2024/7/24/3.jpg", "cape_cod": "2024/7/24/2.jpg", "dining": "2024/7/5/4.jpg", "kitchen_wood": "2024/7/5/3_v29UEdJ.jpg",
    "aerial_woods": "2026/3/24/19-DJI_20260224134908_0275_D_copy_2.jpg", "two_story": "2026/3/24/1.jpg", "porch_farmhouse": "2026/3/24/3.jpg",
    "kitchen_living": "2026/3/24/3_TGlnRJ0.jpg", "living_water": "2026/3/24/55-DSC05726_1.jpg", "kitchen_brass": "2026/3/24/59-DSC06144.jpg",
    "blue_dusk": "2026/3/24/hayes_daytime.jpg", "bedroom": "2026/3/24/Bedroom1.jpg", "kitchen_long": "2021/6/15/WINCHESTER_KITCHEN_copy.jpg",
    "blue_ranch": "2021/6/15/Radford_C_copy_V1cFZ9I.jpg", "dc_kitchen": "2023/2/6/Design_Center_10.jpg", "dc_island": "2023/2/6/Design_Center_14_ocq1cUL.jpg",
    "dc_showroom": "2023/2/6/Design_Center_20_kAJkdka.jpg", "dc_tile": "2023/2/6/Design_Center_25.jpg", "dc_hood": "2023/2/6/Design_Center_30_aHNxi5P.jpg",
    "dc_samples": "2023/2/6/Design_Center_40_i73bHtf.jpg", "aerial_house_woods": "2024/7/5/1_GuQrrFW.jpg", "dc_hands": "2021/6/3/DesignCenter_Hero2.jpg",
    "aerial_farmland": "2025/10/8/oyl.jpg", "bath": "2024/5/14/Bathroom3.jpg",
}

MAP = {  # email id: the three photos after its own hero
    "hp1": ["porch_farmhouse", "living_open", "kitchen_brass"], "hp2": ["aerial_farmland", "drive_trees", "farmhouse_field"],
    "hp3": ["cape_cod", "blue_dusk", "blue_ranch"], "hp4": ["aerial_lake", "coastal_dusk", "living_water"],
    "dd1": ["dc_showroom", "kitchen_brass", "dc_hood"], "dd2": ["dc_tile", "dc_island", "kitchen_quartz"],
    "dd3": ["dc_hands", "dc_samples", "dc_kitchen"], "dd4": ["dc_hood", "bath", "kitchen_island"],
    "fb1": ["aerial_hills", "aerial_house_woods", "farmhouse_field"], "fb2": ["porch_farmhouse", "kitchen_wood", "living_open"],
    "fb3": ["drive_trees", "cape_cod", "kitchen_living"], "fb4": ["blue_dusk", "screen_porch", "bedroom"],
    "fb5": ["aerial_farmland", "two_story", "dining"], "re1": ["aerial_pond", "farmhouse_field", "blue_ranch"],
    "ra1": ["aerial_hills", "aerial_farmland", "aerial_woods"], "rb2": ["aerial_house_woods", "cape_cod", "porch_farmhouse"],
    "rb3": ["aerial_lake", "farmhouse_drive", "kitchen_island"], "ra2": ["aerial_woods", "drive_trees", "aerial_pond"],
    "ho1": ["porch_farmhouse", "breakfast_nook", "porch_view"], "nu3": ["aerial_farmland", "farmhouse_field", "kitchen_white"],
    "nu3n": ["aerial_hills", "two_story", "living_open"], "nu6": ["dc_showroom", "kitchen_quartz", "kitchen_brass"],
    "nu9": ["blue_dusk", "living_water", "kitchen_wood"],
}
MAP["fb4c"], MAP["fb5c"] = MAP["fb4"], MAP["fb5"]
VARIANTS = {"fb4c": "fb4", "fb5c": "fb5"}


def fetch(url, name):
    path = f"{SRC}/{name}.jpg"
    if not os.path.exists(path) or os.path.getsize(path) < 5000:
        subprocess.run(["curl", "-sS", "--retry", "5", "-o", path, url], check=True)
    return path


def gif(eid, hero_src, extras):
    frames = [fetch(hero_src, f"hero_{eid}")] + [fetch(M + P[k] + "?width=1200&height=640&mode=crop", k) for k in extras]
    args = [FF, "-loglevel", "error", "-y"]
    for f in frames:
        args += ["-loop", "1", "-t", str(HOLD), "-i", f]
    n = len(frames)
    chain = "".join(f"[{i}]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[s{i}];" for i in range(n))
    chain += "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,fps={1 / HOLD},split[a][b];[a]palettegen=max_colors=256:stats_mode=single[p];[b][p]paletteuse=dither=sierra2_4a:new=1[o]"
    out = f"{OUT}/{eid}.gif"
    subprocess.run(args + ["-filter_complex", chain, "-map", "[o]", "-loop", "0", out], check=True)
    return out


def upload(path, name):
    tok = os.environ["GHL_PIT"]
    for _ in range(4):
        r = subprocess.run(["curl", "-sS", "-A", "Mozilla/5.0", "-H", f"Authorization: Bearer {tok}", "-H", "Version: 2021-07-28",
                            "-F", f"file=@{path};type=image/gif", "-F", f"name={name}", "https://services.leadconnectorhq.com/medias/upload-file"],
                           capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            return d.get("url") or d.get("fileUrl") or d["data"]["url"]
        except Exception:
            pass
    raise SystemExit(f"upload failed for {name}: {r.stdout[:200]}")


def main():
    os.makedirs(SRC, exist_ok=True)
    rec_path = f"{OUT}/gifs.json"
    rec = json.load(open(rec_path)) if os.path.exists(rec_path) else {}
    for s in SERIES:
        for base in s["emails"]:
            for em in expand(base):
                eid = em["id"]
                if eid not in MAP or not em.get("hero"):
                    continue
                if eid in VARIANTS:  # same photos as the main version, so it shares that GIF
                    if VARIANTS[eid] in rec:
                        rec[eid] = dict(rec[VARIANTS[eid]])
                    continue
                sig = [VERSION, em["hero"]["src"]] + MAP[eid]
                if rec.get(eid, {}).get("sig") == sig and rec[eid].get("cdn"):
                    continue
                out = gif(eid, em["hero"]["src"], MAP[eid])
                entry = {"sig": sig, "file": os.path.relpath(out, HERE), "kb": os.path.getsize(out) // 1024}
                if "--upload" in sys.argv:
                    entry["cdn"] = upload(out, f"fall26-hero-{eid}.gif")
                rec[eid] = entry
                print(eid, entry["kb"], "KB", entry.get("cdn", ""))
                json.dump(rec, open(rec_path, "w"), indent=1)
    json.dump(rec, open(rec_path, "w"), indent=1)
    print(len(rec), "hero GIFs;", sum(1 for v in rec.values() if v.get("cdn")), "in the media library")


if __name__ == "__main__":
    main()
