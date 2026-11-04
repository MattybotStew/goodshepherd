"""Shared helpers for generating Elementor page JSON from the React wires.

All output is native Elementor: containers + heading / text-editor / button /
image / icon-list widgets. No raw HTML, no page-level custom CSS.

Everything is native Elementor: containers + heading / text-editor / button /
image widgets. No raw HTML, no custom CSS — so the page stays editable in the
Elementor editor.

"""

import json

BASE = "https://goodshepherd.local/wp-content/uploads/"

# ---------------------------------------------------------------- helpers

def px(top, right=None, bottom=None, left=None):
    if right is None:
        right = bottom = left = top
    elif bottom is None:
        bottom, left = top, right
    elif left is None:
        left = right
    return {"unit": "px", "top": str(top), "right": str(right),
            "bottom": str(bottom), "left": str(left), "isLinked": False}


def gap(size, row=None):
    row = size if row is None else row
    return {"unit": "px", "size": size, "column": str(size), "row": str(row),
            "isLinked": size == row}


def size(value, unit="px"):
    return {"unit": unit, "size": value, "sizes": []}


def container(cid, settings, children=None, inner=False):
    return {"id": cid, "elType": "container", "settings": settings,
            "elements": children or [], "isInner": inner}


def widget(cid, wtype, settings):
    return {"id": cid, "elType": "widget", "settings": settings,
            "elements": [], "isInner": False, "widgetType": wtype}


def heading(cid, text, tag="h2", color="#002A4E", size_px=44, weight="600",
            line_height=1.15, letter_spacing=-0.8, align="left",
            margin=None, text_transform=None):
    s = {
        "title": text,
        "header_size": tag,
        "align": align,
        "title_color": color,
        "typography_typography": "custom",
        "typography_font_size": size(size_px),
        "typography_font_weight": weight,
        "typography_line_height": {"unit": "em", "size": line_height, "sizes": []},
        "typography_letter_spacing": size(letter_spacing),
    }
    # Mirror the wire's clamp() scale so headings shrink on small screens
    # instead of breaking mid-word.
    if size_px >= 56:
        s["typography_font_size_tablet"] = size(44)
        s["typography_font_size_mobile"] = size(40)
    elif size_px >= 40:
        s["typography_font_size_tablet"] = size(36)
        s["typography_font_size_mobile"] = size(36)
    if text_transform:
        s["typography_text_transform"] = text_transform
    if margin:
        s["_margin"] = px(*margin)
    return widget(cid, "heading", s)


def text(cid, html, color="#303336", size_px=16, line_height=1.65,
         weight="400", align="left", margin=None, max_width=None,
         flex_grow=False):
    s = {
        "editor": html,
        "text_color": color,
        "typography_typography": "custom",
        "typography_font_size": size(size_px),
        "typography_font_weight": weight,
        "typography_line_height": {"unit": "em", "size": line_height, "sizes": []},
        "align": align,
    }
    if margin:
        s["_margin"] = px(*margin)
    if max_width:
        s["_element_width"] = "initial"
        s["_element_custom_width"] = size(max_width)
    if flex_grow:
        s["_flex_size"] = "grow"
    return widget(cid, "text-editor", s)


def link_button(cid, label, url, color="#006BB3", size_px=16, weight="700",
                align="left", margin=None):
    return widget(cid, "button", {
        "text": label,
        "link": {"url": url, "is_external": "", "nofollow": ""},
        "align": align,
        "background_color": "rgba(0,0,0,0)",
        "button_text_color": color,
        "hover_color": "#004F85",
        "typography_typography": "custom",
        "typography_font_size": size(size_px),
        "typography_font_weight": weight,
        "text_padding": px(0),
        "border_radius": px(0),
        "border_border": "solid",
        "border_width": px(0),
        "button_box_shadow_box_shadow_type": "",
        "_margin": px(*margin) if margin else px(0),
    })


def cta_button(cid, label, url, bg="#006BB3", color="#FFFFFF",
               padding=(18, 28), radius=8, size_px=16, border=None):
    return widget(cid, "button", {
        "text": label,
        "link": {"url": url, "is_external": "", "nofollow": ""},
        "align": "center",
        "background_color": bg,
        "button_text_color": color,
        "hover_color": "#FFFFFF",
        "button_background_hover_color": "#004F85",
        "typography_typography": "custom",
        "typography_font_size": size(size_px),
        "typography_font_weight": "700",
        "typography_line_height": {"unit": "em", "size": 1, "sizes": []},
        "text_padding": px(padding[0], padding[1]),
        "border_radius": px(radius),
        "border_border": "solid",
        "border_width": px(*border) if border else px(0),
        "border_color": color if border else "#000000",
    })


def image(cid, att_id, url, radius=16, css_class=""):
    s = {
        "image": {"id": str(att_id), "url": BASE + url, "size": ""},
        "image_size": "full",
        "width": {"unit": "%", "size": 100, "sizes": []},
        "image_border_radius": px(radius),
    }
    if css_class:
        s["_css_classes"] = css_class
    return widget(cid, "image", s)


def section(cid, bg, padding, children, inner_width=1200):
    return container(cid, {
        "_element_id": cid,
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": bg,
        "padding": px(*padding),
        "padding_tablet": px(padding[0] * 0.8, 32, padding[2] * 0.9, 32),
        "padding_mobile": px(padding[0] * 0.7, 24, padding[2] * 0.75, 24),
    }, children)


def inner(cid, children, width=1200, **extra):
    s = {
        "content_width": "boxed",
        "boxed_width": size(width),
        "flex_direction": "column",
        "width": {"unit": "%", "size": 100, "sizes": []},
    }
    s.update(extra)
    return container(cid, s, children, inner=True)


