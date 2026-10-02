#!/usr/bin/env python3
"""Stack the program article (sidebar + content) on tablet/mobile."""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_IDS = [2088, 2089, 2127, 2090, 2091]
P100 = {"unit": "%", "size": 100, "sizes": []}


def walk(nodes, fn):
    for n in nodes:
        fn(n)
        walk(n.get("elements", []), fn)


def has_title(node, title):
    s = node.get("settings", {})
    if s.get("title") == title or s.get("title_text") == title:
        return True
    return any(has_title(c, title) for c in node.get("elements", []))


def edit(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    changed = []

    def apply(n):
        nid = n.get("id")
        s = n.get("settings", {})
        if s.get("flex_direction") in ("row", "row-reverse") and n.get("elType") == "container":
            kids = n.get("elements", [])
            # the article row: a 2-col row whose sidebar carries the "Programs" label
            if len(kids) == 2 and any(has_title(k, "Programs") for k in kids):
                s["flex_wrap"] = "nowrap"
                s["flex_wrap_tablet"] = "wrap"
                s["flex_wrap_mobile"] = "wrap"
                for k in kids:
                    k.setdefault("settings", {})["width_tablet"] = dict(P100)
                    k["settings"]["width_mobile"] = dict(P100)
                changed.append(nid)
    walk(data, apply)
    fd, path = tempfile.mkstemp(suffix=f"_pgresp_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {pid}: {changed}")


if __name__ == "__main__":
    for pid in PAGE_IDS:
        edit(pid)
    print("Done.")
