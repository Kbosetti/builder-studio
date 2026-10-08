#!/usr/bin/env python3
"""Publish a built approval page as a public static site (noindex) on CEA Marketing's Vercel team.

usage: VERCEL_TOKEN=... python3 deploy_vercel.py <out_dir> <project_name>
Wraps out_dir/index.html in a full document, adds every file in out_dir/files.json, uploads through the
Vercel API with curl (each request retries, because sandbox proxies reset connections), deploys to
production and prints https://<project_name>.vercel.app. Reusing a project name keeps the client's link.
Team: VERCEL_TEAM_ID if set, otherwise CEA Marketing.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, time

TEAM = os.environ.get("VERCEL_TEAM_ID") or "team_ruPVbZ5by79KqyoOnsn9JUZ8"
API = "https://api.vercel.com"
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="robots" content="noindex,nofollow">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n')


def curl(args, data_file=None):
    cmd = ["curl", "-sS", "-H", f"Authorization: Bearer {os.environ['VERCEL_TOKEN']}", *args]
    if data_file:
        cmd += ["--data-binary", f"@{data_file}"]
    for attempt in range(5):
        r = subprocess.run(cmd + ["-w", "\n%{http_code}"], capture_output=True, text=True)
        body, _, code = r.stdout.rpartition("\n")
        if code.startswith("2"):
            return json.loads(body or "{}")
        time.sleep(2 * (attempt + 1))
    sys.exit(f"request failed ({code}): {args[-1]}\n{body[:300]}")


def main(out, name):
    site = tempfile.mkdtemp(prefix="approval-site-")
    open(f"{site}/index.html", "w").write(HEAD + open(f"{out}/index.html").read() + "\n</body></html>\n")
    json.dump({"headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}]}, open(f"{site}/vercel.json", "w"))
    for rel in json.load(open(f"{out}/files.json")):
        os.makedirs(os.path.dirname(f"{site}/{rel}"), exist_ok=True)
        shutil.copy(f"{out}/{rel}", f"{site}/{rel}")
    files = []
    for root, _, names in os.walk(site):
        for n in names:
            f = os.path.join(root, n)
            sha = hashlib.sha1(open(f, "rb").read()).hexdigest()
            curl(["-X", "POST", "-H", f"x-vercel-digest: {sha}", "-H", "Content-Type: application/octet-stream", f"{API}/v2/files?teamId={TEAM}"], f)
            files.append({"file": os.path.relpath(f, site), "sha": sha, "size": os.path.getsize(f)})
    body = os.path.join(tempfile.mkdtemp(), "deploy.json")
    json.dump({"name": name, "files": files, "target": "production",
               "projectSettings": {"framework": None, "buildCommand": None, "outputDirectory": None, "installCommand": None}}, open(body, "w"))
    d = curl(["-X", "POST", "-H", "Content-Type: application/json", f"{API}/v13/deployments?teamId={TEAM}&skipAutoDetectionConfirmation=1"], body)
    for _ in range(40):
        s = curl([f"{API}/v13/deployments/{d['id']}?teamId={TEAM}"])
        if s.get("readyState") in ("READY", "ERROR", "CANCELED"):
            break
        time.sleep(3)
    shutil.rmtree(site)
    for _ in range(20):  # the vercel.app alias can take a few seconds to answer
        if subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"https://{name}.vercel.app/"], capture_output=True, text=True).stdout == "200":
            break
        time.sleep(3)
    print(s.get("readyState"), f"https://{name}.vercel.app", f"({len(files)} files)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
