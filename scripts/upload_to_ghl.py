#!/usr/bin/env python3
"""Upload staged assets to the GoHighLevel media library and print a link table.

Usage:
    GHL_PIT=pit-xxxx GHL_LOCATION_ID=xxxx python3 scripts/upload_to_ghl.py assets/portraits

Reads <dir>/manifest.json, uploads each file via POST /medias/upload-file,
and writes <dir>/uploaded.json plus a markdown table to stdout.
Requires network access to services.leadconnectorhq.com.
"""
import json
import os
import sys
import urllib.request
import uuid

API = "https://services.leadconnectorhq.com/medias/upload-file"


def multipart(fields, file_field, filename, data, mime):
    boundary = "----ghl" + uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; "
             f"filename=\"{filename}\"\r\nContent-Type: {mime}\r\n\r\n").encode()
    body += data + f"\r\n--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def main():
    pit = os.environ.get("GHL_PIT")
    loc = os.environ.get("GHL_LOCATION_ID")
    if not pit or not loc or len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    folder = sys.argv[1]
    manifest = json.load(open(os.path.join(folder, "manifest.json")))
    results = []
    for item in manifest:
        path = os.path.join(folder, item["file"])
        mime = "image/png" if path.endswith(".png") else "image/jpeg"
        body, ctype = multipart(
            {"name": item["file"]},
            "file", item["file"], open(path, "rb").read(), mime,
        )
        req = urllib.request.Request(API, data=body, method="POST", headers={
            "Authorization": f"Bearer {pit}",
            "Version": "2021-07-28",
            "Content-Type": ctype,
            # Cloudflare in front of GHL rejects the default urllib UA with error 1010.
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.load(r)
        except urllib.error.HTTPError as e:
            print(f"FAILED {item['file']}: {e.code} {e.read().decode()[:300]}", file=sys.stderr)
            continue
        url = resp.get("url") or resp.get("fileUrl") or resp.get("data", {}).get("url")
        results.append({**item, "ghl_url": url, "ghl_response": resp})
        print(f"uploaded {item['file']} -> {url}", file=sys.stderr)

    json.dump(results, open(os.path.join(folder, "uploaded.json"), "w"), indent=2)
    print("| File | GHL URL | Description |")
    print("|---|---|---|")
    for r in results:
        print(f"| {r['file']} | {r['ghl_url']} | {r['description']} |")


if __name__ == "__main__":
    main()
