#!/usr/bin/env python3
"""Deploy a folder of static files to production of a Vercel project in the CEA Marketing team.

usage: VERCEL_TOKEN=... python3 scripts/vercel_static_deploy.py <site_dir> <project_name>
Uploads through the Vercel API with curl, retrying each request, because the sandbox proxy resets some
connections and the Vercel CLI is not installed in every sandbox. Creates the project on first use.
Prints the production state and the project's vercel.app address.
"""
import glob, hashlib, json, os, subprocess, sys, time

TEAM, API = "team_ruPVbZ5by79KqyoOnsn9JUZ8", "https://api.vercel.com"


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


def deploy(site, name):
    files = []
    for f in sorted(glob.glob(f"{site}/**/*", recursive=True)):
        if os.path.isdir(f) or os.path.basename(f) == ".deploy.json":
            continue
        sha = hashlib.sha1(open(f, "rb").read()).hexdigest()
        curl(["-X", "POST", "-H", f"x-vercel-digest: {sha}", "-H", "Content-Type: application/octet-stream", f"{API}/v2/files?teamId={TEAM}"], f)
        files.append({"file": os.path.relpath(f, site), "sha": sha, "size": os.path.getsize(f)})
    body = f"{site}/.deploy.json"
    json.dump({"name": name, "files": files, "target": "production",
               "projectSettings": {"framework": None, "buildCommand": None, "outputDirectory": None, "installCommand": None}}, open(body, "w"))
    d = curl(["-X", "POST", "-H", "Content-Type: application/json", f"{API}/v13/deployments?teamId={TEAM}&skipAutoDetectionConfirmation=1"], body)
    os.remove(body)
    for _ in range(40):
        s = curl([f"{API}/v13/deployments/{d['id']}?teamId={TEAM}"])
        if s.get("readyState") in ("READY", "ERROR", "CANCELED"):
            break
        time.sleep(3)
    print(s.get("readyState"), f"https://{name}.vercel.app", f"({len(files)} files)", s.get("projectId", ""))


if __name__ == "__main__":
    deploy(sys.argv[1], sys.argv[2])
