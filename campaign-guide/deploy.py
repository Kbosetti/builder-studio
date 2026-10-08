#!/usr/bin/env python3
"""Publish the built guide to its public web address, https://mitchell-fall-campaign-guide.vercel.app

usage: python3 campaign-guide/build.py && python3 campaign-guide/deploy.py      (needs VERCEL_TOKEN)
Wraps out/index.html in a full page (noindex), adds the deck slides, uploads through the Vercel API with
curl (the sandbox proxy resets some connections, so every upload retries), and deploys to production of
project mitchell-fall-campaign-guide (prj_64xxrfKyQ9YoLQpuBRAowodj6xyi) in the CEA Marketing team.
"""
import glob, hashlib, json, os, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
TEAM, NAME = "team_ruPVbZ5by79KqyoOnsn9JUZ8", "mitchell-fall-campaign-guide"
API = "https://api.vercel.com"
HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif;background:#faf8f3}img{max-width:100%}[hidden]{display:none!important}</style>
"""
VERCEL_JSON = {"cleanUrls": True, "headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}]}


def curl(args, data_file=None):
    tok = os.environ["VERCEL_TOKEN"]
    cmd = ["curl", "-sS", "-H", f"Authorization: Bearer {tok}", *args]
    if data_file:
        cmd += ["--data-binary", f"@{data_file}"]
    for attempt in range(5):
        r = subprocess.run(cmd + ["-w", "\n%{http_code}"], capture_output=True, text=True)
        body, _, code = r.stdout.rpartition("\n")
        if code.startswith("2"):
            return json.loads(body or "{}")
        time.sleep(2 * (attempt + 1))
    sys.exit(f"request failed ({code}): {' '.join(args[-1:])}\n{body[:300]}")


def main():
    site = tempfile.mkdtemp(prefix="guide-site-")
    open(f"{site}/index.html", "w").write(HEAD + open(f"{HERE}/out/index.html").read() + "\n</body></html>\n")
    json.dump(VERCEL_JSON, open(f"{site}/vercel.json", "w"))
    for f in glob.glob(f"{HERE}/decks/*/*.jpg"):
        dst = os.path.join(site, os.path.relpath(f, HERE))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f, dst)
    files = []
    for f in sorted(glob.glob(f"{site}/**/*", recursive=True)):
        if os.path.isdir(f):
            continue
        sha = hashlib.sha1(open(f, "rb").read()).hexdigest()
        curl(["-X", "POST", "-H", f"x-vercel-digest: {sha}", "-H", "Content-Type: application/octet-stream", f"{API}/v2/files?teamId={TEAM}"], f)
        files.append({"file": os.path.relpath(f, site), "sha": sha, "size": os.path.getsize(f)})
    body = f"{site}/.deploy.json"
    json.dump({"name": NAME, "files": files, "target": "production",
               "projectSettings": {"framework": None, "buildCommand": None, "outputDirectory": None, "installCommand": None}}, open(body, "w"))
    d = curl(["-X", "POST", "-H", "Content-Type: application/json", f"{API}/v13/deployments?teamId={TEAM}&skipAutoDetectionConfirmation=1"], body)
    for _ in range(40):
        s = curl([f"{API}/v13/deployments/{d['id']}?teamId={TEAM}"])
        if s.get("readyState") in ("READY", "ERROR", "CANCELED"):
            break
        time.sleep(3)
    print(s.get("readyState"), "https://mitchell-fall-campaign-guide.vercel.app", f"({len(files)} files)")
    shutil.rmtree(site)


if __name__ == "__main__":
    main()
