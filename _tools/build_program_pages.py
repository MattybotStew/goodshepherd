#!/usr/bin/env python3
"""Align the five program detail pages to the wire template.

The WordPress pages already use the article layout; this patches the hero to
the wire's compact photo hero, left-aligns its copy, and removes the redundant
"Support GSM Foundation" section (the shared gsm_cta_band replaces it).

Run:  python3 _tools/build_program_pages.py
"""
import json
import os
import subprocess
import tempfile

from el import MEDIA, dims

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGE_IDS = [2088, 2089, 2127, 2090, 2091]


def has_bg_image(node):
    return bool(node.get("settings", {}).get("background_image", {}).get("url"))


def contains(node, needle):
    s = node.get("settings", {})
    for v in (s.get("title"), s.get("title_text"), s.get("text"), s.get("editor")):
        if isinstance(v, str) and needle in v:
            return True
    return any(contains(c, needle) for c in node.get("elements", []))


def align_children(node):
    for c in node.get("elements", []):
        if c.get("elType") == "widget":
            c.setdefault("settings", {})["align"] = "left"
        align_children(c)


def patch_hero(hero):
    s = hero["settings"]
    s["background_image"] = dict(MEDIA["hero"])
    s["background_overlay_background"] = "classic"
    s["background_overlay_color"] = "#001424"
    s["background_overlay_opacity"] = {"unit": "px", "size": 0.6, "sizes": []}
    s.get("__globals__", {}).pop("background_overlay_color", None)
    s["min_height"] = {"unit": "px", "size": 380, "sizes": []}
    s["padding"] = dims(140, 40, 56, 40)
    s["padding_mobile"] = dims(110, 24, 40, 24)
    align_children(hero)


def process(page_id):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(page_id),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)

    hero = next((n for n in data if n.get("elType") == "container" and has_bg_image(n)), None)
    if hero is None:
        print(f"  {page_id}: no hero found")
        return
    patch_hero(hero)

    # drop the duplicate "Support GSM Foundation" section (keep gsm_cta_band)
    kept = []
    removed = 0
    for n in data:
        if (n.get("id") != "gsm_cta_band" and n.get("elType") == "container"
                and contains(n, "Support GSM Foundation") and contains(n, "Volunteer")):
            removed += 1
            continue
        kept.append(n)

    fd, path = tempfile.mkstemp(suffix=f"_prog_{page_id}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(kept, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(page_id), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {page_id}: hero patched, removed {removed} duplicate section(s), {len(kept)} sections")


if __name__ == "__main__":
    for pid in PAGE_IDS:
        process(pid)
    print("Done.")
