#!/usr/bin/env python3
"""Rebuild the News & Updates canvas (post 318) to match the wire.

Run:  python3 _tools/build_news.py
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
PAGE_ID = 318
HERO_IDS = ["3cb39b3"]
DONATE = {"id": "2188", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/donate-picnic.jpg"}

NEWS = [
    ("GSM's 35th Annual Fall Festival",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
     "/news/35th-annual-fall-festival"),
    ("GSM's New Digital Den in Community Day Services",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.",
     "/news/digital-den-community-day"),
    ("30th Anniversary Golf Invitational Sponsors",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "/news/30th-golf-invitational"),
    ("Family Cookouts and campus gatherings",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.",
     "/events#family"),
]

STATS = [("55", "", "Years serving our community"),
         ("100", "+", "Men supported daily"),
         ("5", "", "Core programs offered"),
         ("1971", "", "Founded in Momence, IL")]


def counter(nid, num, suffix, label):
    s = {
        "ending_number": int(num), "title": label, "number_color": NAVY,
        "title_color": "#4A6278",
        "title_gap": {"unit": "px", "size": 8, "sizes": []},
        "typography_number_typography": "custom",
        "typography_number_font_size": {"unit": "px", "size": 48, "sizes": []},
        "typography_number_font_weight": "700",
        "typography_title_typography": "custom",
        "typography_title_font_size": {"unit": "px", "size": 15, "sizes": []},
        "typography_title_font_weight": "500",
    }
    if suffix:
        s["suffix"] = suffix
    if num == "1971":
        s["thousand_separator"] = ""
    return widget(nid, "counter", s)


def build_impact():
    header = container("news_impact_header", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(40),
        "flex_align_items": "flex-start", "flex_wrap": "nowrap",
        "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, [
        container("news_impact_labelcol", {
            "content_width": "full", "width": {"unit": "px", "size": 180, "sizes": []},
            "width_tablet": {"unit": "%", "size": 100, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []}, "flex_direction": "column",
        }, [eyebrow("news_impact_label", "Our Impact")]),
        container("news_impact_col", {
            "content_width": "full", "width": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            h2w("news_impact_h2", "The impact we have made in our community"),
            para("news_impact_p", LOREM_LONG),
        ]),
    ])
    ph = lambda nid, w, h: container(nid, {
        "content_width": "full", "width": {"unit": "%", "size": w, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "min_height": {"unit": "px", "size": h, "sizes": []},
        "background_background": "classic", "background_color": PLACE,
        "border_radius": dims(20, 20, 20, 20),
    }, [])
    mosaic = container("news_impact_mosaic", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(20),
        "flex_align_items": "flex-end", "margin": dims(24, 0, 8, 0),
        "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, [ph("news_ph1", 43, 280), ph("news_ph2", 28, 360), ph("news_ph3", 28, 360)])
    stats = container("news_impact_stats", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(20),
        "padding": dims(32, 0, 0, 0), "flex_wrap": "wrap",
    }, [
        container(f"news_stat_{i}", {
            "content_width": "full", "width": {"unit": "%", "size": 24, "sizes": []},
            "width_tablet": {"unit": "%", "size": 48, "sizes": []},
            "width_mobile": {"unit": "%", "size": 48, "sizes": []}, "flex_direction": "column",
        }, [counter(f"news_counter_{i}", *s)]) for i, s in enumerate(STATS)
    ])
    inner = container("news_impact_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40), "flex_direction": "column",
    }, [header, mosaic, stats])
    return container("news_impact", {
        "content_width": "full", "background_background": "classic",
        "background_color": WHITE, "padding": dims(80, 0, 48, 0),
    }, [inner])


def build_donate():
    copy = container("news_donate_copy", {
        "content_width": "full", "width": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, [
        heading("news_donate_h2", "We can create a better tomorrow", "h2", WHITE, "left",
                {**typography(weight=600, line_height=1.05, letter_spacing=-1.4),
                 "typography_font_size": {"unit": "custom", "size": "clamp(32px, 4vw, 48px)", "sizes": []}}),
        para("news_donate_p", LOREM, color="rgba(255,255,255,0.82)"),
    ])
    btn = widget("news_donate_btn", "button", {
        "text": "Support GSM", "link": {"url": "/support-gsm", "is_external": False},
        "border_border": "none", "border_radius": dims(8, 8, 8, 8),
        "background_color": WHITE, "button_text_color": NAVY,
        "typography_typography": "custom",
        "typography_font_size": {"unit": "px", "size": 16, "sizes": []},
        "typography_font_weight": "700",
        "text_padding": dims(18, 28, 18, 28),
    })
    inner = container("news_donate_inner", {
        "content_width": "full",
        "flex_direction": "row", "flex_justify_content": "space-between",
        "flex_align_items": "center", "flex_gap": gap(40),
        "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
        "background_background": "classic", "background_color": NAVY,
        "background_image": dict(DONATE), "background_position": "center center",
        "background_size": "cover",
        "background_overlay_background": "gradient",
        "background_overlay_color": "rgba(0,20,38,0.93)",
        "background_overlay_color_b": "rgba(0,107,179,0.82)",
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": {"unit": "deg", "size": 150, "sizes": []},
        "border_radius": dims(20, 20, 20, 20),
        "padding": dims(72, 64, 72, 64),
    }, [copy, btn])
    return container("news_donate", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "background_background": "classic",
        "background_color": WHITE, "padding": dims(24, 24, 24, 24),
    }, [inner])


def story_card(i, title, excerpt, url):
    is_left = i % 2 == 0
    radius = dims(20, 0, 0, 20) if is_left else dims(0, 20, 20, 0)
    return container(f"news_story_card_{i}", {
        "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "padding": dims(0, 56, 56, 56),
        "background_background": "classic", "background_color": WHITE,
        "border_border": "solid", "border_width": dims(1, 1, 1, 1),
        "border_color": RULE, "border_radius": radius,
    }, [
        container(f"news_story_ph_{i}", {
            "content_width": "full", "min_height": {"unit": "px", "size": 240, "sizes": []},
            "background_background": "classic", "background_color": PLACE,
            "border_radius": dims(16, 16, 16, 16), "margin": dims(-56, 0, 29, 0),
        }, []),
        heading(f"news_story_h3_{i}", title, "h3", NAVY, "left",
                typography(size=24, weight=600, line_height=1.35)),
        para(f"news_story_p_{i}", excerpt),
        text_link(f"news_story_link_{i}", "Read More", url, size=16, color=NAVY),
    ])


def build_stories():
    header = container("news_stories_header", {
        "content_width": "full", "flex_direction": "column", "flex_align_items": "center",
        "margin": dims(0, 0, 8, 0),
    }, [
        heading("news_stories_h2", "What\u2019s Happening at GSM", "h2", NAVY, "center",
                {**typography(weight=600, line_height=1.15, letter_spacing=-0.8),
                 "typography_font_size": {"unit": "custom", "size": "clamp(32px, 3.4vw, 44px)", "sizes": []}}),
        para("news_stories_p", LOREM),
    ])
    row1 = container("news_stories_row1", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(0),
        "padding": dims(120, 0, 0, 0), "flex_wrap": "nowrap",
        "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, [story_card(0, *NEWS[0]), story_card(1, *NEWS[1])])
    row2 = container("news_stories_row2", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(0),
        "padding": dims(120, 0, 0, 0), "flex_wrap": "nowrap",
        "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, [story_card(0, *NEWS[2]), story_card(1, *NEWS[3])])
    inner = container("news_stories_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "flex_direction": "column",
    }, [header, row1, row2])
    return container("news_stories", {
        "content_width": "full", "background_background": "classic",
        "background_color": SLATE, "padding": dims(100, 24, 100, 24),
    }, [inner])


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    old = json.loads(raw)
    hero = next((n for n in old if n.get("id") in HERO_IDS),
                next((n for n in old if n.get("elType") == "container"), None))
    data = [hero, build_impact(), build_donate(), build_stories(), build_band()]
    fd, path = tempfile.mkstemp(suffix="_news.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"News rebuilt: {len(data)} sections")


if __name__ == "__main__":
    main()
