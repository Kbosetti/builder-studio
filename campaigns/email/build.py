#!/usr/bin/env python3
"""Render the fall email series (series.py) into paste-ready HTML and plain text.

usage: python3 campaigns/email/build.py     writes campaigns/email/out/<id>.html, <id>.txt and emails.json
Each HTML file is one complete email: 600px, table layout, inline styles, Mitchell colors, works in
Builder Studio's custom HTML editor and in Lasso. Links get UTMs here, so the copy stays clean.
"""
import html, json, os, re, sys
from urllib.parse import urlencode

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from series import SERIES  # noqa: E402

OUT = f"{HERE}/out"
LOGO = "https://assets.cdn.filesafe.space/5o5zLlUPPizy6Ajp61oF/media/8f411080-4033-4bae-81e3-fd4fa4ea1aa1.png"
GREEN, DEEP, SUN, CREAM, INK, MUTED = "#2b6d47", "#1e4f33", "#f5d053", "#faf8f3", "#24332a", "#5b6f62"
FONT = "Montserrat, 'Segoe UI', Helvetica, Arial, sans-serif"
LADDER = [["Any Mitchell home", "$5,000"], ["$25,000", "$7,500"], ["$40,000", "$11,000"], ["$60,000", "$15,000"], ["$80,000", "$20,000"], ["$100,000 or more", "$25,000"]]
FINE_DD = ("*Design Dollars apply to Design Center selections including cabinets, countertops, flooring, tile, trim and millwork, doors, "
           "lighting and electrical, plumbing fixtures, appliances, paint, and hardware. Not applicable to structural options, decks, garages, "
           "basements, well, septic, site work, or contract category options. Not applied to base price and not redeemable for cash. Tier "
           "determined at the time selections are made. One offer per contract. Program effective September 1, 2026. Full terms available "
           "from your New Home Consultant.")
FINE_FIN = "Financing terms are illustrative only and subject to credit approval. Not a commitment to lend."
E = html.escape


def utm(href, campaign, content):
    if not href.startswith("http") or "youtube.com" in href:
        return href
    sep = "&" if "?" in href else "?"
    return href + sep + urlencode({"utm_source": "email", "utm_medium": "email", "utm_campaign": campaign, "utm_content": content})


def button(text, href):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 6px"><tr>'
            f'<td align="center" bgcolor="{SUN}" style="border-radius:999px;mso-padding-alt:14px 30px">'
            f'<a href="{E(href)}" target="_blank" style="display:inline-block;padding:15px 32px;font-family:{FONT};font-size:16px;'
            f'font-weight:800;color:{DEEP};text-decoration:none;border-radius:999px">{E(text)}</a></td></tr></table>')


def block(b, link):
    t = b["t"]
    P = f'margin:0 0 16px;font-family:{FONT};font-size:16px;line-height:1.65;color:{INK}'
    if t == "p":
        return f'<p style="{P}">{E(b["text"])}</p>'
    if t == "small":
        txt = E(b["text"])
        if b.get("href"):
            txt = f'<a href="{E(link(b["href"]))}" style="color:{GREEN};font-weight:700">{txt}</a>'
        return f'<p style="margin:0 0 18px;font-family:{FONT};font-size:13px;line-height:1.55;color:{MUTED}">{txt}</p>'
    if t == "list":
        lis = "".join(f'<tr><td valign="top" style="padding:0 10px 10px 0;font-family:{FONT};font-size:16px;color:{GREEN};font-weight:800">&#8226;</td>'
                      f'<td style="padding:0 0 10px;font-family:{FONT};font-size:16px;line-height:1.6;color:{INK}">{E(x)}</td></tr>' for x in b["items"])
        return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px">{lis}</table>'
    if t == "steps":
        rows = "".join(
            f'<tr><td valign="top" style="padding:0 14px 16px 0"><div style="width:30px;height:30px;line-height:30px;border-radius:15px;background:{SUN};'
            f'color:{DEEP};font-family:{FONT};font-weight:800;font-size:15px;text-align:center">{i}</div></td>'
            f'<td style="padding:2px 0 16px;font-family:{FONT};font-size:15px;line-height:1.6;color:{INK}"><b style="display:block;font-size:16px;color:{DEEP}">{E(h)}</b>{E(x)}</td></tr>'
            for i, (h, x) in enumerate(b["items"], 1))
        return f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 8px">{rows}</table>'
    if t == "covers":
        rows = "".join(f'<tr><td style="padding:12px 0;border-top:1px solid #e3e6dc;font-family:{FONT};font-size:15px;line-height:1.55;color:{INK}">'
                       f'<b style="display:block;font-size:16px;color:{DEEP}">{E(h)}</b>{E(x)}</td></tr>' for h, x in b["items"])
        return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 16px">{rows}</table>'
    if t == "ladder":
        rows = "".join(
            f'<tr><td style="padding:10px 14px;border-top:1px solid #e3e6dc;font-family:{FONT};font-size:15px;color:{INK}">{E(a)}</td>'
            f'<td align="right" style="padding:10px 14px;border-top:1px solid #e3e6dc;font-family:{FONT};font-size:16px;font-weight:800;color:{GREEN if i < 5 else DEEP};'
            f'{"background:" + SUN + ";" if i == 5 else ""}">{E(v)}</td></tr>'
            for i, (a, v) in enumerate(LADDER))
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 20px;border:1px solid #e3e6dc;border-radius:10px;background:{CREAM}">'
                f'<tr><td style="padding:10px 14px;font-family:{FONT};font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{MUTED}">Selections you choose</td>'
                f'<td align="right" style="padding:10px 14px;font-family:{FONT};font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{MUTED}">Mitchell adds</td></tr>{rows}</table>')
    if t == "twocol":
        def col(title, items, good):
            mark = "&#10003;" if good else "&#215;"
            lis = "".join(f'<tr><td valign="top" style="padding:0 8px 6px 0;font-family:{FONT};font-size:14px;color:{GREEN if good else MUTED};font-weight:800">{mark}</td>'
                          f'<td style="padding:0 0 6px;font-family:{FONT};font-size:14px;line-height:1.45;color:{INK}">{E(x)}</td></tr>' for x in items)
            return (f'<td class="col" valign="top" width="50%" style="padding:0 8px 0 0"><p style="margin:0 0 10px;font-family:{FONT};font-size:13px;font-weight:800;'
                    f'letter-spacing:1px;text-transform:uppercase;color:{DEEP}">{E(title)}</p><table role="presentation" cellpadding="0" cellspacing="0" border="0">{lis}</table></td>')
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 18px"><tr>'
                f'{col(b["left"][0], b["left"][1], True)}{col(b["right"][0], b["right"][1], False)}</tr></table>')
    if t == "quote":
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 22px"><tr>'
                f'<td style="border-left:4px solid {SUN};padding:6px 0 6px 18px;font-family:{FONT}">'
                f'<p style="margin:0 0 10px;font-size:16px;line-height:1.6;font-style:italic;color:{DEEP}">&#8220;{E(b["text"])}&#8221;</p>'
                f'<p style="margin:0;font-size:13px;color:{MUTED}">{E(b["by"])}. <a href="{E(b["link"])}" style="color:{GREEN};font-weight:700">{E(b["linktext"])}</a></p></td></tr></table>')
    if t == "grid":
        n = b.get("cols", 2)
        w = (520 - 12 * (n - 1)) // n
        cells = [f'<td class="col" width="{100 // n}%" valign="top" style="padding:0 6px 12px"><img src="{E(src)}" width="{w}" alt="A watercolor Home Portrait painting for {E(name)}" '
                 f'style="display:block;width:100%;max-width:{w}px;height:auto;border-radius:8px;border:0">'
                 f'<p style="margin:6px 0 0;font-family:{FONT};font-size:12px;font-weight:700;color:{MUTED}">{E(name)}</p></td>' for name, src in b["items"]]
        rows = "".join("<tr>" + "".join(cells[i:i + n]) + "</tr>" for i in range(0, len(cells), n))
        cap = f'<p style="margin:0 0 18px;font-family:{FONT};font-size:13px;color:{MUTED};text-align:center">{E(b["caption"])}</p>'
        return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 -6px 4px">{rows}</table>{cap}'
    if t == "offer":
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:10px 0 22px"><tr>'
                f'<td bgcolor="{DEEP}" style="border-radius:14px;padding:22px 24px;font-family:{FONT}">'
                f'<p style="margin:0 0 8px;font-size:20px;line-height:1.3;font-weight:800;color:{SUN}">{E(b["head"])}</p>'
                f'<p style="margin:0;font-size:15px;line-height:1.6;color:#ffffff">{E(b["text"])}</p></td></tr></table>')
    if t == "deadline":
        return (f'<p style="margin:0 0 18px;padding:12px 16px;border-radius:10px;background:#fff4d6;font-family:{FONT};font-size:15px;line-height:1.55;'
                f'font-weight:600;color:{DEEP}">{E(b["text"])}</p>')
    if t == "cta":
        return button(b["text"], link(b["href"]))
    raise ValueError(t)


def render(series, em):
    content = em["id"]
    link = lambda h: utm(h, series["campaign"], content)
    hero = ""
    if em.get("hero"):
        hero = (f'<tr><td style="padding:0"><img src="{E(em["hero"]["src"])}" width="600" alt="{E(em["hero"]["alt"])}" '
                f'style="display:block;width:100%;max-width:600px;height:auto;border:0"></td></tr>')
    body = "".join(block(b, link) for b in em["blocks"])
    fine = []
    if em.get("dd"):
        fine.append(FINE_DD)
    if em.get("financing"):
        fine.append(FINE_FIN)
    fine_html = "".join(f'<p style="margin:0 0 8px">{E(f)}</p>' for f in fine)
    pre = E(em["preview"]) + "&#847;&zwnj;&nbsp;" * 30
    return f"""<!doctype html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>{E(em["subject"])}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');
body{{margin:0;padding:0;background:{CREAM}}}
a{{color:{GREEN}}}
@media (max-width:620px){{
  .wrap{{width:100%!important}}
  .pad{{padding-left:22px!important;padding-right:22px!important}}
  .col{{display:block!important;width:100%!important;padding-right:0!important}}
  h1{{font-size:24px!important}}
}}
</style>
</head>
<body style="margin:0;padding:0;background:{CREAM}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:{CREAM}">{pre}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{CREAM}"><tr><td align="center" style="padding:24px 10px">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#ffffff;border-radius:14px;overflow:hidden">
<tr><td bgcolor="{DEEP}" align="center" style="padding:20px 24px"><a href="https://www.mitchellhomesinc.com/" target="_blank"><img src="{LOGO}" width="96" alt="Mitchell Homes" style="display:block;width:96px;height:auto;border:0"></a></td></tr>
{hero}
<tr><td class="pad" style="padding:30px 40px 12px">
<p style="margin:0 0 10px;font-family:{FONT};font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{GREEN}">{E(em["eyebrow"])}</p>
<h1 style="margin:0 0 18px;font-family:{FONT};font-size:28px;line-height:1.2;font-weight:800;color:{DEEP}">{E(em["headline"])}</h1>
{body}
</td></tr>
<tr><td class="pad" style="padding:6px 40px 30px;font-family:{FONT};font-size:14px;line-height:1.6;color:{INK}">
<p style="margin:0 0 4px">Questions? Call a New Home Consultant.</p>
<p style="margin:0 0 14px;color:{MUTED}">Virginia and Maryland <a href="tel:+15407012759" style="color:{GREEN};font-weight:700;text-decoration:none">(540) 701-2759</a><br>North and South Carolina <a href="tel:+19843315468" style="color:{GREEN};font-weight:700;text-decoration:none">(984) 331-5468</a></p>
<p style="margin:0;font-weight:700;color:{DEEP}">The Mitchell Homes team</p>
</td></tr>
<tr><td class="pad" bgcolor="#f1efe8" style="padding:22px 40px;font-family:{FONT};font-size:11px;line-height:1.55;color:{MUTED}">
{fine_html}<p style="margin:0 0 8px">Mitchell Homes, Inc., 14300 Sommerville Court, Midlothian, VA 23113. Building on your land since 1992.</p>
<p style="margin:0">You are receiving this email because you asked Mitchell Homes about building a home. {{{{unsubscribe}}}}</p>
</td></tr>
</table>
</td></tr></table>
</body>
</html>
"""


def text_version(series, em):
    link = lambda h: utm(h, series["campaign"], em["id"])
    out = [em["headline"].upper(), ""]
    for b in em["blocks"]:
        t = b["t"]
        if t in ("p", "small", "deadline"):
            out += [b["text"] + (f' {link(b["href"])}' if b.get("href") else ""), ""]
        elif t == "list":
            out += [f"* {x}" for x in b["items"]] + [""]
        elif t in ("steps", "covers"):
            out += [f"{h}: {x}" for h, x in b["items"]] + [""]
        elif t == "ladder":
            out += ["Selections you choose / Mitchell adds"] + [f"{a}: {v}" for a, v in LADDER] + [""]
        elif t == "twocol":
            out += [b["left"][0] + ": " + ", ".join(b["left"][1]) + ".", b["right"][0] + ": " + ", ".join(b["right"][1]) + ".", ""]
        elif t == "quote":
            out += [f'"{b["text"]}"', f'{b["by"]}. {b["linktext"]}: {b["link"]}', ""]
        elif t == "grid":
            out += [b["caption"], ""]
        elif t == "offer":
            out += [b["head"], b["text"], ""]
        elif t == "cta":
            out += [f'{b["text"]}: {link(b["href"])}', ""]
    out += ["Questions? Call a New Home Consultant.", "Virginia and Maryland (540) 701-2759", "North and South Carolina (984) 331-5468", "", "The Mitchell Homes team", ""]
    if em.get("dd"):
        out.append(FINE_DD)
    if em.get("financing"):
        out.append(FINE_FIN)
    out += ["Mitchell Homes, Inc., 14300 Sommerville Court, Midlothian, VA 23113.", "Unsubscribe: {{unsubscribe}}"]
    return "\n".join(out) + "\n"


def expand(em):
    yield em
    v = em.get("variant")
    if v:
        raw = json.dumps({k: x for k, x in em.items() if k != "variant"})
        for a, b in v["replace"]:
            raw = raw.replace(json.dumps(a)[1:-1], json.dumps(b)[1:-1])
        e2 = json.loads(raw)
        e2.update(id=v["id"], segment=v["segment"])
        yield e2


DASH = re.compile(r"[–—]| - ")


def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for s in SERIES:
        for base in s["emails"]:
            for em in expand(base):
                h = render(s, em)
                txt = text_version(s, em)
                for field in (em["subject"], em["preview"], txt):
                    if DASH.search(field):
                        sys.exit(f'{em["id"]}: dash in copy: {DASH.search(field).group(0)!r}')
                open(f'{OUT}/{em["id"]}.html', "w").write(h)
                open(f'{OUT}/{em["id"]}.txt', "w").write(txt)
                index.append({"series": s["key"], "series_name": s["name"], "stage": s["stage"], "id": em["id"], "send": em["send"],
                              "segment": em["segment"], "subject": em["subject"], "preview": em["preview"], "hold": em.get("hold", ""),
                              "subject_len": len(em["subject"])})
    json.dump({"series": [{k: s[k] for k in ("key", "name", "stage", "campaign", "audience", "goal")} for s in SERIES], "emails": index},
              open(f"{OUT}/emails.json", "w"), indent=1)
    for e in index:
        print(f'{e["id"]:5} {e["send"]:22} {e["subject_len"]:3}  {e["subject"]}')


if __name__ == "__main__":
    main()
