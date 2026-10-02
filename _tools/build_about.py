#!/usr/bin/env python3
"""Rebuild the About page canvas (post 316) to match the React wire.

Run:  python3 _tools/build_about.py
"""
import json
import os
import subprocess
import tempfile

from el import (NAVY, BLUE, BODY, SLATE, PALE, WHITE, RULE, PLACE, PLACE_SOFT,
                MEDIA, LOREM, LOREM_LONG, LOREM_EXTRA, dims, gap, typography,
                container, widget, heading, eyebrow, h2 as h2w, para, text_link,
                placeholder, image)
from rebuild_cta_band import build_band

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 316
HERO_ID = "3cb39b3"


def w(nid, wtype, settings):
    return widget(nid, wtype, settings)


def patch_hero(hero):
    s = hero["settings"]
    s["background_image"] = dict(MEDIA["hero"])
    s["background_overlay_color"] = "#001424"
    s["background_overlay_opacity"] = {"unit": "px", "size": 0.6, "sizes": []}
    s["background_overlay_background"] = "classic"
    s.get("__globals__", {}).pop("background_overlay_color", None)
    s["min_height"] = {"unit": "px", "size": 620, "sizes": []}
    s["padding"] = dims(160, 40, 120, 40)
    return hero


def build_mission():
    col = lambda nid, h, img: container(nid, {
        "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
        "flex_direction": "column", "flex_gap": gap(20),
    }, [image(f"{nid}_img", MEDIA[img], height=h)])

    col2 = container("about_mosaic_col2", {
        "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
        "flex_direction": "column", "flex_gap": gap(20),
        "margin": dims(80, 0, 0, 0),
    }, [image("about_mosaic_garden", MEDIA["garden"], height=248),
        image("about_mosaic_porch", MEDIA["porch"], height=339)])

    mosaic = container("about_mission_mosaic", {
        "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "row", "flex_gap": gap(20), "flex_wrap_tablet": "wrap",
    }, [
        container("about_mosaic_col1", {
            "content_width": "full", "width": {"unit": "%", "size": 50, "sizes": []},
            "flex_direction": "column", "flex_gap": gap(20),
        }, [image("about_mosaic_workshop", MEDIA["workshop"], height=339),
            image("about_mosaic_kitchen", MEDIA["kitchen"], height=248)]),
        col2,
    ])

    copy = container("about_mission_copy", {
        "content_width": "full", "width": {"unit": "%", "size": 44, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, [
        eyebrow("about_mission_eyebrow", "About Us"),
        h2w("about_mission_h2",
            "A community of care, growth, and dignity for over 50 years."),
        para("about_mission_p1", LOREM_LONG),
        para("about_mission_p2", LOREM_EXTRA),
    ])

    inner = container("about_mission_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40),
        "flex_direction": "row", "flex_gap": gap(64), "flex_align_items": "center",
        "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, [copy, mosaic])

    return container("about_mission", {
        "content_width": "full", "background_background": "classic",
        "background_color": SLATE, "padding": dims(96, 0, 72, 0),
        "flex_direction": "column",
    }, [inner])


def intro_column(nid, num, title, text, url):
    return container(nid, {
        "content_width": "full", "width": {"unit": "%", "size": 33.33, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column", "padding": dims(32, 40, 36, 40),
        "padding_mobile": dims(20, 20, 20, 20),
        "border_border": "solid", "border_width": dims(0, 1, 0, 0),
        "border_width_mobile": dims(0, 0, 1, 0),
        "border_color": RULE,
    }, [
        heading(f"{nid}_num", num, "p", PLACE, "left",
                typography(size=40, weight=500, line_height=1.2, letter_spacing=-1.6)),
        heading(f"{nid}_title", title, "h3", NAVY, "left",
                typography(size=22, weight=700, line_height=1.2)),
        para(f"{nid}_text", text),
        text_link(f"{nid}_link", "Learn more \u2192", url, size=16, color=NAVY),
    ])


def build_intro():
    # wire About uses the home columns (Projects / Support GSM / Donate)
    descriptions = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit nulla pariatur.",
    ]
    card = container("about_intro_card", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "flex_direction": "row", "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap",
        "flex_wrap_mobile": "wrap",
        "background_background": "classic", "background_color": WHITE,
        "border_radius": dims(16, 16, 16, 16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
    }, [
        intro_column("about_intro_0", "01.", "Projects", descriptions[0], "/programs"),
        intro_column("about_intro_1", "02.", "Support GSM", descriptions[1], "/support-gsm"),
        intro_column("about_intro_2", "03.", "Donate", descriptions[2], "/support-gsm"),
    ])
    return container("about_intro", {
        "content_width": "full", "background_background": "classic",
        "background_color": SLATE, "padding": dims(0, 40, 72, 40),
        "flex_direction": "column",
    }, [card])


def split_inner(nid, copy_children, image_node, flip=False):
    children = [image_node, *copy_children] if flip else [*copy_children, image_node]
    return container(f"{nid}_inner", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "padding": dims(0, 40, 0, 40),
        "flex_direction": "row", "flex_gap": gap(64), "flex_align_items": "center",
        "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
    }, children)


def split_copy(nid, children):
    return container(f"{nid}_copy", {
        "content_width": "full", "width": {"unit": "%", "size": 47, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, children)


def split_image(nid, height=420, soft=False):
    node = placeholder(f"{nid}_img", height=height, soft=soft)
    node["settings"].update({
        "width": {"unit": "%", "size": 47, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
    })
    return node


def build_split_mission():
    copy = split_copy("about_mission_split", [
        eyebrow("about_mission_split_eyebrow", "Mission, Vision & Values"),
        h2w("about_mission_split_h2", "Why we exist"),
        para("about_mission_split_p1", LOREM_LONG),
        para("about_mission_split_p2", LOREM),
    ])
    return container("about_split_mission", {
        "content_width": "full", "background_background": "classic",
        "background_color": SLATE, "padding": dims(88, 0, 88, 0),
        "_element_id": "mission",
    }, [split_inner("about_mission_split", [copy], split_image("about_mission_split"))])


def build_affiliations():
    pills = w("about_aff_pills", "text-editor", {
        "editor": (
            '<p>'
            '<span style="display:inline-block;padding:12px 18px;margin:0 12px 12px 0;'
            'border:1px solid #C8D4E0;border-radius:8px;background:#fff;'
            'font-size:14px;font-weight:700;color:#002A4E;">Brothers of the Good Shepherd</span>'
            '<span style="display:inline-block;padding:12px 18px;margin:0 0 12px 0;'
            'border:1px solid #C8D4E0;border-radius:8px;background:#fff;'
            'font-size:14px;font-weight:700;color:#002A4E;">Special Olympics</span>'
            '</p>'
        ),
    })
    copy = split_copy("about_aff", [
        eyebrow("about_aff_eyebrow", "Affiliations"),
        h2w("about_aff_h2", "Partners in care"),
        para("about_aff_p", LOREM),
        pills,
    ])
    return container("about_affiliations", {
        "content_width": "full", "background_background": "classic",
        "background_color": SLATE, "padding": dims(88, 0, 88, 0),
        "_element_id": "affiliations",
    }, [split_inner("about_aff", [copy], split_image("about_aff"))])


def build_history():
    years = ["Prior to 1970", "1970", "1971", "1979", "1981", "1993", "1995",
             "1997", "1998", "1999", "2001", "2004", "2005", "2006", "2007",
             "2009", "2010", "2012"]
    cards = []
    for i, y in enumerate(years):
        cards.append(container(f"tl_card_{i}", {
            "content_width": "full", "width": {"unit": "px", "size": 300, "sizes": []},
            "width_mobile": {"unit": "px", "size": 260, "sizes": []},
            "flex_direction": "column", "padding": dims(20, 20, 20, 20),
            "background_background": "classic", "background_color": WHITE,
            "border_border": "solid", "border_width": dims(1, 1, 1, 1),
            "border_color": PLACE, "border_radius": dims(12, 12, 12, 12),
        }, [
            heading(f"tl_year_{i}", y, "p", BLUE, "left",
                    typography(size=17, weight=700, line_height=1.2)),
            para(f"tl_text_{i}", LOREM),
        ]))

    head_photo = container("about_history_photo", {
        "content_width": "full", "width": {"unit": "px", "size": 220, "sizes": []},
        "min_height": {"unit": "px", "size": 150, "sizes": []},
        "background_background": "classic", "background_color": PLACE_SOFT,
        "border_radius": dims(12, 12, 12, 12),
    }, [])
    head = container("about_history_head", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(32),
        "flex_align_items": "center", "margin": dims(0, 0, 8, 0),
    }, [
        head_photo,
        container("about_history_headcopy", {
            "content_width": "full", "width": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            eyebrow("about_history_eyebrow", "Our History"),
            h2w("about_history_h2", "A Timeline of Caring"),
        ]),
    ])

    track = container("about_history_track", {
        "content_width": "full", "flex_direction": "row", "flex_gap": gap(20),
        "flex_wrap": "nowrap", "overflow": "auto", "margin": dims(32, 0, 0, 0),
        "css_classes": "gsm-cards-nowrap",
    }, cards)

    bar = container("about_history_bar", {
        "content_width": "full", "flex_direction": "row", "min_height": {"unit": "px", "size": 10, "sizes": []},
        "background_background": "classic", "background_color": PLACE,
        "border_radius": dims(5, 5, 5, 5), "margin": dims(12, 0, 0, 0),
    }, [
        container("about_history_thumb", {
            "content_width": "full", "width": {"unit": "%", "size": 42, "sizes": []},
            "min_height": {"unit": "px", "size": 10, "sizes": []},
            "background_background": "classic", "background_color": BLUE,
            "border_radius": dims(5, 5, 5, 5),
        }, []),
    ])

    return container("about_history", {
        "content_width": "full", "background_background": "classic",
        "background_color": PALE, "padding": dims(88, 0, 88, 0),
        "_element_id": "history",
    }, [
        container("about_history_inner", {
            "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
            "padding": dims(0, 40, 0, 40), "flex_direction": "column",
        }, [head, track, bar]),
    ])


def build_accessibility():
    copy = split_copy("about_acc", [
        eyebrow("about_acc_eyebrow", "Accessibility Statement"),
        h2w("about_acc_h2", "This site should work for everyone"),
        para("about_acc_p1", LOREM),
        para("about_acc_p2", LOREM),
        text_link("about_acc_link", "Contact us about accessibility \u2192", "/contact"),
    ])
    return container("about_accessibility", {
        "content_width": "full", "background_background": "classic",
        "background_color": PALE, "padding": dims(88, 0, 88, 0),
        "_element_id": "accessibility",
    }, [split_inner("about_acc", [copy], split_image("about_acc", soft=True), flip=True)])


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    old = json.loads(raw)
    hero = next((n for n in old if n.get("id") == HERO_ID), old[0] if old else None)
    if hero is None:
        raise SystemExit("hero not found")
    patch_hero(hero)

    data = [hero, build_mission(), build_intro(), build_split_mission(),
            build_history(), build_affiliations(), build_accessibility(), build_band()]

    fd, path = tempfile.mkstemp(suffix="_about.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"About rebuilt: {len(data)} sections")


if __name__ == "__main__":
    main()
