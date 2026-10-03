#!/usr/bin/env python3
"""Give every page hero the same layout: a full-bleed cover background with the
content vertically centred in a fixed-height hero.

  * inner pages: min-height 620px
  * Home:        min-height 868px (the gateway)
  * all:         padding 140px 40px, flex column, justify-content center

Run:  python3 _tools/unify_heroes.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGE_IDS = [315, 316, 317, 2088, 2089, 2127, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 318, 319]
HOME_ID = 315


def dims(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


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
    if hero is None:
        print(f"  {pid}: no hero")
        return
    s = hero["settings"]
    height = 868 if pid == HOME_ID else 620
    s["min_height"] = {"unit": "px", "size": height, "sizes": []}
    s["min_height_tablet"] = {"unit": "px", "size": 560 if pid != HOME_ID else 720, "sizes": []}
    s["min_height_mobile"] = {"unit": "px", "size": 520 if pid != HOME_ID else 620, "sizes": []}
    s["padding"] = dims(140, 40, 140, 40)
    s["padding_tablet"] = dims(120, 32, 120, 32)
    s["padding_mobile"] = dims(104, 24, 96, 24)
    s["flex_direction"] = "column"
    s["flex_justify_content"] = "center"
    s["background_size"] = "cover"
    s["background_position"] = "center center"
    s["background_repeat"] = "no-repeat"

    fd, path = tempfile.mkstemp(suffix=f"_unifyhero_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {pid}: hero={hero['id']} minH={height} centred")


if __name__ == "__main__":
    for pid in PAGE_IDS:
        edit(pid)
    print("Done.")
