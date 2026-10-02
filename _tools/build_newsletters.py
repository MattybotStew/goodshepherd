#!/usr/bin/env python3
"""Rebuild the Newsletters page canvas (post 2095) to match the wire.

Run:  python3 _tools/build_newsletters.py
"""
import json
import os
import subprocess
import tempfile

from el import (NAVY, BLUE, BODY, SLATE, PALE, RULE, LOREM, LOREM_LONG, dims, gap,
                typography, container, widget, heading, para, text_link, intro_strip)
from rebuild_cta_band import build_band

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 2095

COLUMNS = [
    ("01.", "Projects",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.", "/programs"),
    ("02.", "Support GSM",
     "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.", "/support-gsm"),
    ("03.", "Donate",
     "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit nulla pariatur.", "/support-gsm"),
]

ISSUES = [
    ("Summer family update", "Summer 2026"),
    ("Spring family update", "Spring 2026"),
    ("Winter family update", "Winter 2025"),
]

FORM = (
    '<form action="/newsletters/" method="post">'
    '<label for="nl-email" style="display:block;font-weight:700;margin-bottom:8px;">Email address</label>'
    '<input id="nl-email" type="email" name="email" required '
    'style="display:block;width:100%;max-width:420px;padding:14px 16px;border:1px solid #C8D4E0;border-radius:8px;margin-bottom:16px;">'
    '<button type="submit" '
    'style="display:inline-block;padding:16px 28px;border:0;border-radius:8px;background:#0089DF;color:#fff;font-weight:700;cursor:pointer;">Sign up</button>'
    '</form>'
)


def rte(prefix, children, first=False):
    settings = {
        "content_width": "full", "width": {"unit": "px", "size": 720, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }
    if not first:
        settings["border_border"] = "solid"
        settings["border_width"] = dims(1, 0, 0, 0)
        settings["border_color"] = "#C8D4E0"
        settings["margin"] = dims(40, 0, 0, 0)
        settings["padding"] = dims(40, 0, 0, 0)
    return container(prefix, settings, children)


def build_body():
    signup = rte("nl_signup", [
        heading("nl_signup_h2", "Stay in the loop", "h2", NAVY, "left",
                typography(size=28, weight=600, line_height=1.25, letter_spacing=-0.4)),
        para("nl_signup_p", LOREM),
        widget("nl_form", "text-editor", {"editor": FORM}),
    ], first=True)

    issue_children = [heading("nl_issues_h2", "Past issues", "h2", NAVY, "left",
                              typography(size=28, weight=600, line_height=1.25, letter_spacing=-0.4))]
    for i, (title, date) in enumerate(ISSUES):
        issue_children.append(container(f"nl_issue_{i}", {
            "content_width": "full", "flex_direction": "column",
            "margin": dims(20, 0, 0, 0),
        }, [
            heading(f"nl_issue_h3_{i}", title, "h3", NAVY, "left",
                    typography(size=20, weight=600, line_height=1.3)),
            para(f"nl_issue_p_{i}", f"{date}. {LOREM}"),
            text_link(f"nl_issue_link_{i}", "PDF placeholder", "#", size=16, color=BLUE),
        ]))
    issues = rte("nl_issues", issue_children)

    inner = container("nl_body_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(64, 40, 88, 40), "flex_direction": "column",
        "flex_align_items": "flex-start",
    }, [signup, issues])
    return container("nl_body", {"content_width": "full", "flex_direction": "column"}, [inner])


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    old = json.loads(raw)
    hero = next((n for n in old if n.get("elType") == "container"
                 and n.get("settings", {}).get("background_image", {}).get("url")), old[0])
    data = [hero, intro_strip("nl_intro", COLUMNS), build_body(), build_band()]
    fd, path = tempfile.mkstemp(suffix="_newsletters.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"Newsletters rebuilt: {len(data)} sections")


if __name__ == "__main__":
    main()
