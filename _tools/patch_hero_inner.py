#!/usr/bin/env python3
"""Give every page hero the same inner container and a cover background.

Canonical inner (already used by the program pages): a boxed 1200 column.
Heroes that currently hold bare widgets (or a single image-box) get their
content wrapped in that inner container; heroes that already have one are
normalised to the same settings. Every hero background is set to cover.

Run:  python3 _tools/patch_hero_inner.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGE_IDS = [315, 316, 317, 2088, 2089, 2127, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 318, 319]

CANON = {
    "content_width": "boxed",
    "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
    "flex_direction": "column",
    "flex_gap": {"unit": "px", "size": 8, "sizes": [], "column": "8", "row": "8"},
}


def find_hero(data):
    for n in data:
        if n.get("elType") == "container" and n.get("settings", {}).get("background_image", {}).get("url"):
            return n
    return None


def is_plain_container(n):
    return n.get("elType") == "container" and not n.get("widgetType")


def edit(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    hero = find_hero(data)
    if hero is None:
        print(f"  {pid}: no hero")
        return

    # 1) cover background everywhere
    s = hero["settings"]
    s["background_size"] = "cover"
    s["background_position"] = "center center"
    s["background_repeat"] = "no-repeat"
    s.setdefault("background_background", "classic")

    children = hero.get("elements", [])
    if len(children) == 1 and is_plain_container(children[0]):
        inner = children[0]
        inner["settings"].update(CANON)
        action = f"normalised inner {inner['id']}"
    else:
        inner = {
            "id": "hero_inner",
            "elType": "container",
            "isInner": True,
            "settings": dict(CANON),
            "elements": children,
        }
        hero["elements"] = [inner]
        action = f"wrapped {len(children)} child(ren)"

    fd, path = tempfile.mkstemp(suffix=f"_heroinner_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {pid}: hero={hero['id']} cover + {action}")


if __name__ == "__main__":
    for pid in PAGE_IDS:
        edit(pid)
    print("Done.")
