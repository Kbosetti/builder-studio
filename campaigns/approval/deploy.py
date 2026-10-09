#!/usr/bin/env python3
"""Publish the approval document to its public address, https://mitchell-fall-approval.vercel.app (noindex),
with the three proofing batches at /batch-1/, /batch-2/ and /batch-3/.

usage: python3 campaigns/approval/build_approval.py && python3 campaigns/approval/deploy.py   (needs VERCEL_TOKEN)
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex,nofollow">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif;background:#faf8f3}'
        'img{max-width:100%}[hidden]{display:none!important}</style>\n')
site = tempfile.mkdtemp(prefix="approval-site-")
shutil.copytree(f"{HERE}/out", site, dirs_exist_ok=True)
open(f"{site}/index.html", "w").write(HEAD + open(f"{HERE}/out/index.html").read() + "\n</body></html>\n")
for name in sorted(os.listdir(f"{HERE}/out")):
    if name.startswith("batch-"):
        open(f"{site}/{name}/index.html", "w").write(HEAD + open(f"{HERE}/out/{name}/index.html").read() + "\n</body></html>\n")
open(f"{site}/vercel.json", "w").write('{"headers":[{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow"}]}]}\n')
subprocess.run([sys.executable, f"{ROOT}/scripts/vercel_static_deploy.py", site, "mitchell-fall-approval"], check=True)
shutil.rmtree(site)
