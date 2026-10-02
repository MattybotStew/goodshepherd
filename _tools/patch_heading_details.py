#!/usr/bin/env python3
"""Fix the remaining heading-size details found in the design comparison.

  * Support GSM split h2s: 36 -> 44 (wire .split h2 = --type-section)
  * Contact "How can we help you?" image-box title: 36 -> 48
  * Endowment rte h2s: 26 -> 28

Run:  python3 _tools/patch_heading_details.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")


def px(v):
    return {"unit": "px", "size": v, "sizes": []}


def set_heading_size(settings, size):
    settings["typography_typography"] = "custom"
    settings["typography_font_size"] = px(size)
    settings["typography_font_size_tablet"] = px(36)
    settings["typography_font_size_mobile"] = px(32)


def set_imagebox_title_size(settings, size):
    settings["title_typography_typography"] = "custom"
    settings["title_typography_font_size"] = px(size)
    settings["title_typography_font_size_tablet"] = px(36)
    settings["title_typography_font_size_mobile"] = px(32)


def edit(page_id, fn):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(page_id),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    hits = []
    walk(data, fn, hits)
    fd, path = tempfile.mkstemp(suffix=f"_heads_{page_id}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(page_id), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {page_id}: {hits}")


def walk(nodes, fn, hits):
    for n in nodes:
        fn(n, hits)
        walk(n.get("elements", []), fn, hits)


def support_gsm(n, hits):
    if n.get("id") in ("sb0t1", "sb1t1", "sb2t1", "sb3t1", "sb4t1"):
        set_heading_size(n["settings"], 44)
        hits.append(n["id"])


def contact(n, hits):
    if n.get("id") == "ddd017c":  # image-box "How can we help you?"
        set_imagebox_title_size(n["settings"], 48)
        hits.append(n["id"])


def endowment(n, hits):
    if n.get("id") in ("gifts_h2", "lvl_h2"):  # wire .rte h2 = 28
        s = n["settings"]
        s["typography_typography"] = "custom"
        s["typography_font_size"] = px(28)
        hits.append(n["id"])


if __name__ == "__main__":
    edit(2092, support_gsm)
    edit(319, contact)
    edit(2093, endowment)
    print("Done.")
