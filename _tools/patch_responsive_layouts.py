#!/usr/bin/env python3
"""Stack the pre-existing two/three-column rows on tablet + mobile, matching
the wire's <=900px stacked layout.

Run:  python3 _tools/patch_responsive_layouts.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

P100 = {"unit": "%", "size": 100, "sizes": []}

# page_id: list of (row_id, [child ids that get width_tablet/mobile 100%])
LAYOUTS = {
    2092: [(f"sb{i}rw", [f"sb{i}cc", f"sb{i}ic"]) for i in range(5)],
    2093: [("endow_intro", ["intro_copy", "intro_img"]),
           ("gifts_row", ["current_col", "def_col"])],
    319: [("0271cda", ["304b4e5", "e8fe7b9", "d4eb1d9"]),
          ("cebd81e", ["a1e05eb", "37f8abc"])],
}


def walk(nodes, fn):
    for n in nodes:
        fn(n)
        walk(n.get("elements", []), fn)


def edit(page_id, rows):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(page_id),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    changed = []

    def apply(n):
        nid = n.get("id")
        for row_id, child_ids in rows:
            if nid == row_id and n.get("elType") == "container":
                s = n["settings"]
                s["flex_wrap"] = "nowrap"
                s["flex_wrap_tablet"] = "wrap"
                s["flex_wrap_mobile"] = "wrap"
                changed.append(row_id)
            if nid in child_ids:
                s = n["settings"]
                s["width_tablet"] = dict(P100)
                s["width_mobile"] = dict(P100)
                changed.append(nid)

    walk(data, apply)
    fd, path = tempfile.mkstemp(suffix=f"_resp_{page_id}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(page_id), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {page_id}: {changed}")


if __name__ == "__main__":
    for pid, rows in LAYOUTS.items():
        edit(pid, rows)
    print("Done.")
