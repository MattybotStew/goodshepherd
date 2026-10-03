#!/usr/bin/env python3
"""Unify container widths to 1200px across pages.

  * Home hero (138ba28): drop the odd 1080px boxed width -> full bleed
  * any boxed container without an explicit width -> 1200px
  * program article rows (the sidebar + content grid) -> boxed 1200

Run:  python3 _tools/fix_widths.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGES = [315, 316, 317, 2088, 2089, 2127, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 318, 319]
W1200 = {"unit": "px", "size": 1200, "sizes": []}


def dims(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def has_title(node, title):
    s = node.get("settings", {})
    if s.get("title") == title or s.get("title_text") == title:
        return True
    return any(has_title(c, title) for c in node.get("elements", []))


def walk(nodes, fn):
    for n in nodes:
        fn(n)
        walk(n.get("elements", []), fn)


def edit(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    changed = []

    def apply(n):
        if n.get("elType") != "container":
            return
        s = n.get("settings", {})
        nid = n.get("id")
        # Home hero
        if pid == 315 and nid == "138ba28":
            s["content_width"] = "full"
            s["boxed_width"] = dict(W1200)
            changed.append(nid)
            return
        # sidebar + content article row
        if s.get("flex_direction") in ("row", "row-reverse"):
            kids = n.get("elements", [])
            if len(kids) == 2 and any(has_title(k, "Programs") for k in kids):
                s["content_width"] = "boxed"
                s["boxed_width"] = dict(W1200)
                s["padding"] = dims(64, 40, 88, 40)
                changed.append(nid)
                return
        # boxed with no explicit width
        if s.get("content_width") == "boxed" and not s.get("boxed_width", {}).get("size"):
            s["boxed_width"] = dict(W1200)
            changed.append(nid)

    walk(data, apply)
    fd, path = tempfile.mkstemp(suffix=f"_widths_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    if changed:
        print(f"  {pid}: {changed}")


if __name__ == "__main__":
    for pid in PAGES:
        edit(pid)
    print("Done.")
