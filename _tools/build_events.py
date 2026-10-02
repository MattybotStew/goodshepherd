#!/usr/bin/env python3
"""Rebuild the Events page canvas (post 2094) to match the wire.

Run:  python3 _tools/build_events.py
"""
import json
import os
import subprocess
import tempfile

from el import (NAVY, BODY, SLATE, PALE, RULE, LOREM, LOREM_LONG, dims, gap,
                typography, container, heading, para, intro_strip)
from rebuild_cta_band import build_band

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 2094
HERO_IDS = ["3cb39b3"]

COLUMNS = [
    ("01.", "Support GSM",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
     "/support-gsm"),
    ("02.", "Volunteer",
     "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.",
     "/events"),
    ("03.", "Shepherd Endowment Society",
     "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit nulla pariatur.",
     "/shepherd-endowment-society"),
]

EVENTS = [
    ("fall-festival", "Fall Festival", "October 2026"),
    ("brunch-auction", "Brunch Auction", "Spring"),
    ("golf", "Golf Invitational", "Summer"),
    ("family", "Family Events", "Year-round"),
]


def rte_section(i, eid, title, when):
    settings = {
        "content_width": "full", "width": {"unit": "px", "size": 720, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "_element_id": eid,
    }
    if i > 0:
        settings["border_border"] = "solid"
        settings["border_width"] = dims(1, 0, 0, 0)
        settings["border_color"] = "#C8D4E0"
        settings["margin"] = dims(40, 0, 0, 0)
        settings["padding"] = dims(40, 0, 0, 0)
    return container(f"ev_sec_{i}", settings, [
        heading(f"ev_h2_{i}", title, "h2", NAVY, "left",
                typography(size=28, weight=600, line_height=1.25, letter_spacing=-0.4)),
        para(f"ev_when_{i}", when),
        para(f"ev_body_{i}", LOREM_LONG),
    ])


def build_body():
    secs = [rte_section(i, *e) for i, e in enumerate(EVENTS)]
    inner = container("ev_body_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(64, 40, 88, 40), "flex_direction": "column",
        "flex_align_items": "flex-start",
    }, secs)
    return container("ev_body", {
        "content_width": "full", "flex_direction": "column",
    }, [inner])


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    old = json.loads(raw)
    hero = next((n for n in old if n.get("id") in HERO_IDS),
                next((n for n in old if n.get("elType") == "container"), None))
    data = [hero, intro_strip("ev_intro", COLUMNS), build_body(), build_band()]
    fd, path = tempfile.mkstemp(suffix="_events.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"Events rebuilt: {len(data)} sections")


if __name__ == "__main__":
    main()
