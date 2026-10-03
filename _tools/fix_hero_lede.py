#!/usr/bin/env python3
"""Cap every hero lede at 660px (wire .home-hero p max-width).

Image-box heroes (About/Support GSM/Events/Contact) constrain the image-box;
heading/text-editor heroes (Home/Programs/programs/Careers/Newsletters/
Endowment) constrain the lede widget that follows the H1.

Run:  python3 _tools/fix_hero_lede.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGES = [315, 316, 317, 2088, 2089, 2127, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 318, 319]
W660 = {"unit": "px", "size": 660, "sizes": []}


def width(settings):
    settings["_element_width"] = "initial"
    settings["_element_custom_width"] = dict(W660)
    # drop any side padding used to fake the width
    p = settings.get("_padding")
    if isinstance(p, dict):
        settings["_padding"] = {"unit": p.get("unit", "px"), "top": p.get("top", "0"),
                                "right": "0", "bottom": p.get("bottom", "0"),
                                "left": "0", "isLinked": False}


def widgets(nodes, out):
    for c in nodes:
        if c.get("widgetType"):
            out.append(c)
        widgets(c.get("elements", []), out)
    return out


def find_hero(data):
    for n in data:
        if n.get("elType") == "container" and n.get("settings", {}).get("background_image", {}).get("url"):
            return n
    return None


def edit(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    hero = find_hero(data)
    if not hero:
        print(f"  {pid}: no hero")
        return
    ws = widgets(hero.get("elements", []), [])
    h1i = next((i for i, w in enumerate(ws)
                if w.get("widgetType") == "heading"
                and w.get("settings", {}).get("header_size") == "h1"), None)
    action = "none"
    if h1i is not None and h1i + 1 < len(ws):
        width(ws[h1i + 1]["settings"])
        action = ws[h1i + 1]["id"]
    else:
        # image-box heroes (title + description) already self-constrain; make
        # sure no widget width override is applied to them
        ib = next((w for w in ws if w.get("widgetType") == "image-box"), None)
        if ib:
            width(ib["settings"])
            action = ib["id"]
    fd, path = tempfile.mkstemp(suffix=f"_lede_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {pid}: hero {hero['id']} lede capped -> {action}")


if __name__ == "__main__":
    for pid in PAGES:
        edit(pid)
    print("Done.")
