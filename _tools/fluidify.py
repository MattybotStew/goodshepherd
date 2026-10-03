#!/usr/bin/env python3
"""Convert every stepwise heading (desktop + tablet/mobile px override) into a
fluid clamp() so type scales smoothly instead of jumping at breakpoints.

clamp(min, vw, max) where vw is chosen so the size reaches `max` at ~1280px
and bottoms out at the mobile value.

Run:  python3 _tools/fluidify.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGES = [315, 316, 317, 2088, 2089, 2127, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 318, 319]


def fluidify(s, prefix="typography"):
    d = s.get(f"{prefix}_font_size", {})
    if not isinstance(d, dict) or d.get("unit") == "custom":
        return False
    mx = d.get("size")
    mn = (s.get(f"{prefix}_font_size_mobile", {}) or {}).get("size") \
        or (s.get(f"{prefix}_font_size_tablet", {}) or {}).get("size")
    if not mx or not mn or float(mx) <= float(mn):
        return False
    vw = round(float(mx) / 12.8, 2)
    s[f"{prefix}_font_size"] = {
        "unit": "custom", "size": f"clamp({int(float(mn))}px, {vw}vw, {int(float(mx))}px)",
        "sizes": [],
    }
    s.pop(f"{prefix}_font_size_tablet", None)
    s.pop(f"{prefix}_font_size_mobile", None)
    return True


def edit(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    n = 0

    def walk(nodes):
        nonlocal n
        for c in nodes:
            st = c.get("settings", {}) or {}
            if c.get("widgetType") == "heading" and fluidify(st):
                n += 1
            if c.get("widgetType") == "image-box":
                if fluidify(st, "title_typography"):
                    n += 1
                fluidify(st, "description_typography")
            walk(c.get("elements", []))

    walk(data)
    if n:
        fd, path = tempfile.mkstemp(suffix=f"_fluid_{pid}.json")
        with os.fdopen(fd, "w") as fh:
            json.dump(data, fh, separators=(",", ":"))
        subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
        os.remove(path)
    print(f"  {pid}: {n} fluid heading(s)")


if __name__ == "__main__":
    for pid in PAGES:
        edit(pid)
    print("Done.")
