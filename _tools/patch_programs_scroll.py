#!/usr/bin/env python3
"""Make the "Our Programs & Services" card row a horizontal scroller like the
wire (4.25 cards + custom scrollbar) on Home and the Programs landing.

Run:  python3 _tools/patch_programs_scroll.py
"""
import json
import os
import subprocess
import tempfile

from el import SLATE

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_IDS = [315, 317]
P23 = {"unit": "%", "size": 23.53, "sizes": []}


def dims(t=0, r=0, b=0, l=0):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def scrollbar():
    return {
        "id": "prog_scrollbar", "elType": "container", "isInner": True,
        "settings": {
            "content_width": "full", "flex_direction": "row",
            "min_height": {"unit": "px", "size": 10, "sizes": []},
            "background_background": "classic", "background_color": "#C8D4E0",
            "border_radius": dims(5, 5, 5, 5), "margin": dims(16, 0, 0, 0),
        },
        "elements": [{
            "id": "prog_scrollbar_thumb", "elType": "container", "isInner": True,
            "settings": {
                "content_width": "full", "width": {"unit": "%", "size": 85, "sizes": []},
                "min_height": {"unit": "px", "size": 10, "sizes": []},
                "background_background": "classic", "background_color": "#0089DF",
                "border_radius": dims(5, 5, 5, 5),
            },
            "elements": [],
        }],
    }


def edit(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    changed = []

    def walk(nodes):
        for i, n in enumerate(nodes):
            nid = n.get("id")
            if nid == "prog_row":
                s = n["settings"]
                s["overflow"] = "auto"
                s["css_classes"] = "gsm-cards-nowrap"
                changed.append("prog_row")
                # insert scrollbar right after the row
                if not any(c.get("id") == "prog_scrollbar" for c in nodes):
                    nodes.insert(i + 1, scrollbar())
                    changed.append("prog_scrollbar")
            if isinstance(nid, str) and nid.startswith("prog_card_"):
                n["settings"]["width"] = dict(P23)
                changed.append(nid)
            walk(n.get("elements", []))

    walk(data)
    fd, path = tempfile.mkstemp(suffix=f"_progscroll_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {pid}: {changed}")


if __name__ == "__main__":
    for pid in PAGE_IDS:
        edit(pid)
    print("Done.")
