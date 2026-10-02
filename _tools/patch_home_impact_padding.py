#!/usr/bin/env python3
"""Home impact section: add the wire's bottom padding (96px) and stat
padding-bottom (20px), and drop the last stat's divider.

Run:  python3 _tools/patch_home_impact_padding.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 315
STATS = ["0895290", "0a89313", "298487e", "a03e378"]


def px(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def walk(nodes, fn):
    for n in nodes:
        fn(n)
        walk(n.get("elements", []), fn)


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    changed = []

    def apply(n):
        nid = n.get("id")
        s = n.get("settings", {})
        if nid == "78cc2f2":
            # wire .home-impact padding: 24px 24px 96px (96 bottom at all widths)
            s["padding"] = px(100, 40, 96, 40)
            for key in ("padding_tablet", "padding_mobile"):
                if key in s:
                    s[key]["bottom"] = "96"
            changed.append(nid)
        if nid in STATS:
            # wire .home-impact__stat: padding-bottom 20
            s["padding"] = px(0, 0, 20, 0)
            changed.append(nid)
        if nid == "a03e378":
            # last stat has no right divider
            s["border_width"] = px(0, 0, 0, 0)
            changed.append(nid)

    walk(data, apply)
    fd, path = tempfile.mkstemp(suffix="_home_impact.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"Home impact padding: {changed}")


if __name__ == "__main__":
    main()
