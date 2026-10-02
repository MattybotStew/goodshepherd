#!/usr/bin/env python3
"""Align every inner-page hero with the wire's PageHero: the shared hero photo,
the navy overlay, and left/center copy per page.

Run:  python3 _tools/patch_heroes.py
"""
import json
import os
import subprocess
import tempfile

from el import MEDIA, dims

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

# page_id: align  (wire PageHero align prop; default center)
PAGES = {
    2092: "center",   # Support GSM
    2093: "center",   # Endowment
    2094: "center",   # Events
    2095: "center",   # Newsletters
    318: "left",      # News
    2096: "left",     # Careers
    319: "left",      # Contact
}


def has_bg_image(node):
    return bool(node.get("settings", {}).get("background_image", {}).get("url"))


def align_children(node, align):
    for c in node.get("elements", []):
        if c.get("elType") == "widget":
            c.setdefault("settings", {})["align"] = align
        align_children(c, align)


def patch(hero, align):
    s = hero["settings"]
    s["background_image"] = dict(MEDIA["hero"])
    s["background_overlay_background"] = "classic"
    s["background_overlay_color"] = "#001424"
    s["background_overlay_opacity"] = {"unit": "px", "size": 0.6, "sizes": []}
    s.get("__globals__", {}).pop("background_overlay_color", None)
    s["min_height"] = {"unit": "px", "size": 620, "sizes": []}
    s["padding"] = dims(160, 40, 120, 40)
    s["padding_mobile"] = dims(120, 24, 80, 24)
    align_children(hero, align)


def main():
    for pid, align in PAGES.items():
        raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                       "_elementor_data"]).decode()
        data = json.loads(raw)
        hero = next((n for n in data if n.get("elType") == "container" and has_bg_image(n)), None)
        if hero is None:
            print(f"  {pid}: no hero; skipped")
            continue
        patch(hero, align)
        fd, path = tempfile.mkstemp(suffix=f"_hero_{pid}.json")
        with os.fdopen(fd, "w") as fh:
            json.dump(data, fh, separators=(",", ":"))
        subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
        os.remove(path)
        print(f"  {pid}: hero patched (align={align})")
    print("Done.")


if __name__ == "__main__":
    main()
