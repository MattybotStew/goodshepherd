#!/usr/bin/env python3
"""Replace the global `gsm_cta_band` on every content page with the wire's
GetInvolvedCta (photo-overlay band, "Support GSM Foundation" + Donate /
Volunteer / Careers cards).

Reads each page's live _elementor_data via wp.sh, swaps the band, writes a temp
file, then applies it with apply_elementor.sh (which clears the Elementor cache
and regenerates the page CSS).

Run:  python3 _tools/rebuild_cta_band.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
TOOLS = os.path.dirname(os.path.abspath(__file__))
APPLY = os.path.join(TOOLS, "apply_elementor.sh")

PAGE_IDS = [316, 317, 2088, 2089, 2127, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 318, 319]

CTA_IMAGE = {
    "id": "2184",
    "url": "https://goodshepherd.local/wp-content/uploads/2026/10/cta-greenhouse.jpg",
}
NAVY = "#002A4E"
PALE = "#FAFCFE"
WHITE = "#FFFFFF"

PATHWAYS = [
    {"title": "Donate", "link": "Give now \u2192", "path": "/support-gsm"},
    {"title": "Volunteer", "link": "Get involved \u2192", "path": "/events"},
    {"title": "Careers", "link": "View openings \u2192", "path": "/careers"},
]
LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
         "eiusmod tempor.")


def dims(t, r, b, l, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def container(nid, settings, elements, is_inner=True):
    return {"id": nid, "elType": "container", "settings": settings,
            "elements": elements, "isInner": is_inner}


def widget(nid, wtype, settings):
    return {"id": nid, "elType": "widget", "widgetType": wtype,
            "settings": settings, "elements": [], "isInner": False}


def build_card(i, p):
    is_last = i == len(PATHWAYS) - 1
    settings = {
        "content_width": "full",
        "width": {"unit": "%", "size": 33.33, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "flex_gap": {"column": "16", "row": "16", "isLinked": True, "unit": "px", "size": 16},
        "padding": dims(40, 36, 44, 36),
        "padding_mobile": dims(32, 0, 36, 0),
    }
    if not is_last:
        settings["border_border"] = "solid"
        settings["border_width"] = dims(0, 1, 0, 0)
        settings["border_width_mobile"] = dims(0, 0, 1, 0)
        settings["border_color"] = "rgba(255,255,255,0.16)"
    return container(f"cta_card_{i}", settings, [
        widget(f"cta_h3_{i}", "heading", {
            "title": p["title"], "header_size": "h3", "align": "left",
            "title_color": WHITE,
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 33, "sizes": []},
            "typography_font_size_mobile": {"unit": "px", "size": 28, "sizes": []},
            "typography_font_weight": "600",
            "typography_line_height": {"unit": "em", "size": 1.05, "sizes": []},
            "typography_letter_spacing": {"unit": "px", "size": -1, "sizes": []},
        }),
        widget(f"cta_p_{i}", "text-editor", {
            "editor": f"<p>{LOREM}</p>",
            "text_color": "rgba(255,255,255,0.82)",
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 16, "sizes": []},
            "typography_line_height": {"unit": "em", "size": 1.65, "sizes": []},
        }),
        widget(f"cta_link_{i}", "button", {
            "text": p["link"],
            "link": {"url": p["path"], "is_external": False, "nofollow": False},
            "align": "left",
            "border_border": "none",
            "text_padding": dims(0, 0, 0, 0),
            "background_color": "rgba(0,0,0,0)",
            "button_text_color": WHITE,
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 13, "sizes": []},
            "typography_font_weight": "700",
            "typography_text_transform": "uppercase",
            "typography_letter_spacing": {"unit": "px", "size": 2, "sizes": []},
        }),
    ])


def build_band():
    return container("gsm_cta_band", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "background_background": "classic",
        "background_color": PALE,
        "padding": dims(72, 40, 72, 40),
        "padding_mobile": dims(48, 20, 48, 20),
        "flex_direction": "column",
    }, [
        container("cta_inner", {
            "content_width": "full",
            "background_background": "classic",
            "background_color": NAVY,
            "background_image": dict(CTA_IMAGE),
            "background_position": "center center",
            "background_repeat": "no-repeat",
            "background_size": "cover",
            "background_overlay_background": "gradient",
            "background_overlay_color": "rgba(0,20,38,0.92)",
            "background_overlay_color_b": "rgba(0,107,179,0.80)",
            "background_overlay_gradient_type": "linear",
            "background_overlay_gradient_angle": {"unit": "deg", "size": 170, "sizes": []},
            "border_radius": dims(28, 28, 28, 28),
            "padding": dims(132, 64, 136, 64),
            "padding_mobile": dims(72, 28, 56, 28),
            "flex_direction": "column",
        }, [
            widget("cta_h2", "heading", {
                "title": "Support GSM Foundation", "header_size": "h2", "align": "center",
                "title_color": WHITE,
                "typography_typography": "custom",
                "typography_font_size": {"unit": "custom", "size": "clamp(40px, 6vw, 76px)", "sizes": []},
                "typography_font_weight": "600",
                "typography_line_height": {"unit": "em", "size": 1.06, "sizes": []},
                "typography_letter_spacing": {"unit": "px", "size": -1.8, "sizes": []},
                "_padding": dims(0, 0, 64, 0),
            }),
            container("cta_row", {
                "content_width": "full",
                "flex_direction": "row",
                "flex_wrap": "nowrap",
                "flex_wrap_tablet": "wrap",
                "flex_wrap_mobile": "wrap",
                "border_border": "solid",
                "border_width": dims(1, 0, 0, 0),
                "border_width_mobile": dims(1, 0, 0, 0),
                "border_color": "rgba(255,255,255,0.25)",
            }, [build_card(i, p) for i, p in enumerate(PATHWAYS)]),
        ]),
    ])


def replace_band(page_id):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(page_id),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    found = False
    for i, node in enumerate(data):
        if node.get("id") == "gsm_cta_band":
            data[i] = build_band()
            found = True
            break
    if not found:
        print(f"  page {page_id}: no gsm_cta_band, skipping")
        return False
    fd, path = tempfile.mkstemp(suffix=f"_cta_{page_id}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(page_id), path],
                          stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  page {page_id}: band replaced ({len(data)} sections)")
    return True


if __name__ == "__main__":
    for pid in PAGE_IDS:
        replace_band(pid)
    print("Done.")
