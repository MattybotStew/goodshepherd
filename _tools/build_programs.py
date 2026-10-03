#!/usr/bin/env python3
"""Rebuild the Programs & Services landing canvas (post 317) to the wire.

Run:  python3 _tools/build_programs.py
"""
import json
import os
import subprocess
import tempfile

from el import (NAVY, BLUE, BODY, SLATE, PALE, WHITE, RULE, PLACE, PLACE_SOFT,
                MEDIA, LOREM, LOREM_LONG, LOREM_SHORT, dims, gap, typography,
                container, widget, heading, eyebrow, h2 as h2w, para, text_link)
from rebuild_cta_band import build_band

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 317
HERO_IDS = ["prog_hero", "3cb39b3"]

PROGRAMS = [
    ("Community Day Services", "/programs/community-day-services", "icon-community"),
    ("TBD Vocational Program", "/programs/vocational", "icon-vocational"),
    ("Special Olympics", "/programs/special-olympics", "icon-special"),
    ("Residential Living", "/programs/residential-living", "icon-residential"),
    ("Health & Well Being", "/programs/health-well-being", "icon-health"),
]


def patch_hero(hero, align="left"):
    s = hero["settings"]
    s["background_image"] = dict(MEDIA["hero"])
    s["background_overlay_color"] = "#001424"
    s["background_overlay_opacity"] = {"unit": "px", "size": 0.6, "sizes": []}
    s["background_overlay_background"] = "classic"
    s.get("__globals__", {}).pop("background_overlay_color", None)
    s["min_height"] = {"unit": "px", "size": 620, "sizes": []}
    s["padding"] = dims(160, 40, 120, 40)

    def align_children(node):
        for c in node.get("elements", []):
            if c.get("elType") == "widget":
                c.setdefault("settings", {})["align"] = align
            align_children(c)

    align_children(hero)
    return hero


def ph(nid, height, radius=24):
    return container(nid, {
        "content_width": "full",
        "min_height": {"unit": "px", "size": height, "sizes": []},
        "background_background": "classic", "background_color": PLACE,
        "border_radius": dims(radius, radius, radius, radius),
    }, [])


def build_intro():
    rule = container("prog_intro_rule", {
        "content_width": "full", "width": {"unit": "px", "size": 48, "sizes": []},
        "min_height": {"unit": "px", "size": 3, "sizes": []},
        "background_background": "classic", "background_color": BLUE,
        "margin": dims(0, 0, 24, 0),
    }, [])
    aside = container("prog_intro_aside", {
        "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column", "padding": dims(8, 0, 0, 0),
    }, [rule, para("prog_intro_p", LOREM_LONG)])
    header = container("prog_intro_header", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(64),
        "flex_align_items": "flex-start", "margin": dims(0, 0, 64, 0),
        "flex_wrap": "nowrap", "flex_wrap_mobile": "wrap",
    }, [
        heading("prog_intro_h2",
                "Every small act of kindness creates a ripple of positive change.",
                "h2", NAVY, "left",
                {**typography(weight=600, line_height=1.15, letter_spacing=-0.5),
                 "typography_font_size": {"unit": "custom", "size": "clamp(32px, 4vw, 48px)", "sizes": []}}),
        aside,
    ])

    stack = container("prog_intro_stack", {
        "content_width": "full", "width": {"unit": "%", "size": 28, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column", "flex_gap": gap(20),
    }, [ph("prog_intro_ph4", 230), ph("prog_intro_ph5", 230)])
    mosaic = container("prog_intro_mosaic", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(20),
        "flex_wrap": "nowrap", "flex_wrap_mobile": "wrap",
    }, [
        container("prog_intro_ph1", {
            "content_width": "full", "width": {"unit": "%", "size": 28, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "min_height": {"unit": "px", "size": 480, "sizes": []},
            "background_background": "classic", "background_color": PLACE,
            "border_radius": dims(24, 24, 24, 24),
        }, []),
        container("prog_intro_ph2", {
            "content_width": "full", "width": {"unit": "%", "size": 44, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "min_height": {"unit": "px", "size": 480, "sizes": []},
            "background_background": "classic", "background_color": PLACE,
            "border_radius": dims(24, 24, 24, 24),
        }, []),
        stack,
    ])

    inner = container("prog_intro_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40), "flex_direction": "column",
    }, [header, mosaic])

    return container("prog_intro", {
        "content_width": "full", "background_background": "classic",
        "background_color": PALE, "padding": dims(88, 0, 0, 0),
    }, [inner])


def program_card(i, name, path, icon):
    is_first, is_last = i == 0, i == len(PROGRAMS) - 1
    radius = dims(16, 0, 0, 16) if is_first else dims(0, 0, 0, 0)
    if is_last:
        radius = dims(0, 16, 16, 0)
    settings = {
        "content_width": "full", "width": {"unit": "%", "size": 20, "sizes": []},
        "width_tablet": {"unit": "%", "size": 50, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column", "flex_gap": gap(0),
        "padding": dims(32, 28, 36, 28),
        "background_background": "classic", "background_color": WHITE,
        "border_radius": radius,
    }
    if not is_last:
        settings.update({
            "border_border": "solid", "border_width": dims(0, 1, 0, 0),
            "border_width_mobile": dims(0, 0, 1, 0), "border_color": RULE,
        })
    icon_box = container(f"prog_iconbox_{i}", {
        "content_width": "full", "width": {"unit": "px", "size": 48, "sizes": []},
        "width_tablet": {"unit": "px", "size": 48, "sizes": []},
        "width_mobile": {"unit": "px", "size": 48, "sizes": []},
        "min_height": {"unit": "px", "size": 48, "sizes": []},
        "flex_direction": "row", "flex_justify_content": "center",
        "flex_align_items": "center",
        "background_background": "classic", "background_color": NAVY,
        "border_radius": dims(12, 12, 12, 12), "margin": dims(0, 0, 16, 0),
    }, [widget(f"prog_icon_{i}", "image", {
        "image": dict(MEDIA[icon]),
        "width": {"unit": "px", "size": 24, "sizes": []},
        "height": {"unit": "px", "size": 24, "sizes": []},
        "object-fit": "contain",
    })])
    title = heading(f"prog_title_{i}", name, "h3", NAVY, "left",
                    typography(size=22, weight=700, line_height=1.2))
    title["settings"]["_margin"] = dims(0, 0, 10, 0)
    desc = widget(f"prog_desc_{i}", "text-editor", {
        "editor": f"<p>{LOREM_SHORT}</p>", "text_color": "#4B4D50",
        "_flex_size": "grow", **typography(size=16, weight=400, line_height=1.5),
    })
    link = text_link(f"prog_btn_{i}", "Learn more \u2192", path, size=16, color=NAVY)
    return container(f"prog_card_{i}", settings, [icon_box, title, desc, link])


def build_services():
    cards = [program_card(i, *p) for i, p in enumerate(PROGRAMS)]
    row = container("prog_row", {
        "content_width": "full", "flex_direction": "row", "flex_wrap": "nowrap",
        "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap", "flex_gap": gap(0),
        "background_background": "classic", "background_color": WHITE,
        "border_radius": dims(16, 16, 16, 16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
    }, cards)
    head = container("prog_head", {
        "content_width": "full", "flex_direction": "column",
        "margin": dims(0, 0, 32, 0),
    }, [
        h2w("prog_services_h2", "Our Programs & Services", size=48),
        para("prog_services_p", LOREM),
    ])
    inner = container("prog_services_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40), "flex_direction": "column",
    }, [head, row])
    return container("prog_services", {
        "content_width": "full", "background_background": "classic",
        "background_color": PALE, "padding": dims(64, 0, 88, 0),
    }, [inner])


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    old = json.loads(raw)
    hero = next((n for n in old if n.get("id") in HERO_IDS), old[0])
    patch_hero(hero)

    data = [hero, build_intro(), build_services(), build_band()]
    fd, path = tempfile.mkstemp(suffix="_programs.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"Programs rebuilt: {len(data)} sections")


if __name__ == "__main__":
    main()
