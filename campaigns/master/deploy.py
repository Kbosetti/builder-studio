#!/usr/bin/env python3
"""Publish the master plan to its public address, https://mitchell-fall-plan.vercel.app (noindex).

usage: python3 campaigns/master/build_master.py && python3 campaigns/master/deploy.py   (needs VERCEL_TOKEN)
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="robots" content="noindex,nofollow">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif;background:#faf8f3}'
        'img{max-width:100%}[hidden]{display:none!important}</style>\n')
site = tempfile.mkdtemp(prefix="plan-site-")
open(f"{site}/index.html", "w").write(HEAD + open(f"{HERE}/out/index.html").read() + "\n</body></html>\n")
open(f"{site}/vercel.json", "w").write('{"headers":[{"source":"/(.*)","headers":[{"key":"X-Robots-Tag","value":"noindex, nofollow"}]}]}\n')
subprocess.run([sys.executable, f"{ROOT}/scripts/vercel_static_deploy.py", site, "mitchell-fall-plan"], check=True)
shutil.rmtree(site)
