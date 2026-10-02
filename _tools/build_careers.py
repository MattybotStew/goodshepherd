#!/usr/bin/env python3
"""Rebuild the Careers page canvas (post 2096) to match the wire.

Run:  python3 _tools/build_careers.py
"""
import json
import os
import subprocess
import tempfile

from el import (NAVY, BLUE, BODY, SLATE, PALE, WHITE, RULE, PLACE, PLACE_SOFT,
                MEDIA, LOREM, LOREM_LONG, LOREM_EXTRA, dims, gap, typography,
                container, widget, heading, eyebrow, h2 as h2w, para, text_link,
                placeholder, image, intro_strip, intro_column)
from rebuild_cta_band import build_band

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 2096
HERO_IDS = ["3cb39b3"]

INTRO_PAGE = [
    ("01.", "Projects",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.", "/programs"),
    ("02.", "Support GSM",
     "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.", "/support-gsm"),
    ("03.", "Donate",
     "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit nulla pariatur.", "/support-gsm"),
]

JOBS = [
    ("Direct Service Provider", "Full-time",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor."),
    ("Direct Service Provider", "Openings",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."),
]


def split(nid, element_id, eyebrow_text, title, children, flip=False,
          soft=False, section_bg=SLATE, image_height=420):
    copy = container(f"{nid}_copy", {
        "content_width": "full", "width": {"unit": "%", "size": 47, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, [eyebrow(f"{nid}_eyebrow", eyebrow_text), h2w(f"{nid}_h2", title), *children])
    ph = placeholder(f"{nid}_img", height=image_height, soft=soft)
    ph["settings"].update({
        "width": {"unit": "%", "size": 47, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
    })
    inner_children = [ph, copy] if flip else [copy, ph]
    inner = container(f"{nid}_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40),
        "flex_direction": "row", "flex_gap": gap(64), "flex_align_items": "center",
        "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, inner_children)
    return container(nid, {
        "content_width": "full", "background_background": "classic",
        "background_color": section_bg, "padding": dims(88, 0, 88, 0),
        "_element_id": element_id,
    }, [inner])


def build_mission():
    eyebrow_w = eyebrow("careers_mission_eyebrow", "Careers at Good Shepherd Manor")
    h2_w = h2w("careers_mission_h2", "Build a career with purpose")
    copy = container("careers_mission_copy", {
        "content_width": "full", "width": {"unit": "%", "size": 44, "sizes": []},
        "flex_direction": "column",
    }, [eyebrow_w, h2_w, para("careers_mission_p1", LOREM_LONG),
        para("careers_mission_p2", LOREM_EXTRA)])
    mosaic = container("careers_mission_mosaic", {
        "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
        "flex_direction": "row", "flex_gap": gap(20),
    }, [
        container("careers_mosaic_col1", {
            "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
            "flex_direction": "column", "flex_gap": gap(20),
        }, [placeholder("careers_mosaic_1", 339), placeholder("careers_mosaic_2", 248)]),
        container("careers_mosaic_col2", {
            "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
            "flex_direction": "column", "flex_gap": gap(20), "margin": dims(80, 0, 0, 0),
        }, [placeholder("careers_mosaic_3", 248), placeholder("careers_mosaic_4", 339)]),
    ])
    inner = container("careers_mission_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40), "flex_direction": "row",
        "flex_gap": gap(64), "flex_align_items": "center",
        "flex_wrap": "nowrap", "flex_wrap_mobile": "wrap",
    }, [copy, mosaic])
    return container("careers_mission", {
        "content_width": "full", "background_background": "classic",
        "background_color": SLATE, "padding": dims(96, 0, 72, 0),
    }, [inner])


def build_openings_children():
    children = [para("careers_openings_p", LOREM)]
    for i, (title, jtype, note) in enumerate(JOBS):
        job = container(f"careers_job_{i}", {
            "content_width": "full", "flex_direction": "column",
            "margin": dims(24, 0, 0, 0), "padding": dims(24, 0, 0, 0),
            "border_border": "solid", "border_width": dims(1, 0, 0, 0),
            "border_color": "#C8D4E0",
        }, [
            heading(f"careers_job_{i}_h3", title, "h3", NAVY, "left",
                    typography(size=20, weight=600, line_height=1.3)),
            para(f"careers_job_{i}_p", f"{jtype}. {note}"),
            text_link(f"careers_job_{i}_link", f"Apply for {title}", "/contact"),
        ])
        children.append(job)
    return children


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    old = json.loads(raw)
    hero = next((n for n in old if n.get("id") in HERO_IDS),
                next((n for n in old if n.get("elType") == "container"), None))

    benefits = [para("careers_ben_p1", LOREM_LONG), para("careers_ben_p2", LOREM)]
    culture = [para("careers_cul_p1", LOREM_LONG), para("careers_cul_p2", LOREM)]
    apply_children = [para("careers_apply_p1", LOREM_LONG), para("careers_apply_p2", LOREM),
                      text_link("careers_apply_link", "Contact us to apply \u2192", "/contact")]

    data = [
        hero,
        build_mission(),
        intro_strip("careers_intro", INTRO_PAGE),
        split("careers_benefits", "benefits", "Benefits", "Rewards that support you", benefits),
        split("careers_culture", "culture", "Our Culture", "A workplace that cares", culture,
              flip=True, soft=True, section_bg=PALE),
        split("careers_openings", "openings", "Job Openings", "Join our team",
              build_openings_children()),
        split("careers_apply", "apply", "Apply Today", "Ready to make a difference?",
              apply_children, soft=True, section_bg=PALE),
        build_band(),
    ]
    fd, path = tempfile.mkstemp(suffix="_careers.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"Careers rebuilt: {len(data)} sections")


if __name__ == "__main__":
    main()
