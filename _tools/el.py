"""Shared helpers for building Elementor page data that mirrors the wire.

Keeps the two documented traps in one place:
  * fixed/% widths only render with content_width 'full'
  * flex controls must use the flex_ prefix
"""

NAVY = "#002A4E"
BLUE = "#0089DF"
BODY = "#303336"
SLATE = "#F1F5F9"
PALE = "#FAFCFE"
WHITE = "#FFFFFF"
RULE = "#E8EDF2"
PLACE = "#C8D4E0"
PLACE_SOFT = "#DAEBF7"

BASE = "https://goodshepherd.local/wp-content/uploads/2026/10/"

MEDIA = {
    "hero": {"id": "2171", "url": BASE + "hero.jpg"},
    "workshop": {"id": "2172", "url": BASE + "mosaic-workshop.jpg"},
    "kitchen": {"id": "2173", "url": BASE + "mosaic-kitchen.jpg"},
    "garden": {"id": "2174", "url": BASE + "mosaic-garden.jpg"},
    "porch": {"id": "2175", "url": BASE + "mosaic-porch.jpg"},
    "cta": {"id": "2184", "url": BASE + "cta-greenhouse.jpg"},
    "icon-community": {"id": "2176", "url": BASE + "community-day.svg"},
    "icon-vocational": {"id": "2177", "url": BASE + "vocational.svg"},
    "icon-special": {"id": "2178", "url": BASE + "special-olympics.svg"},
    "icon-residential": {"id": "2179", "url": BASE + "residential.svg"},
    "icon-health": {"id": "2180", "url": BASE + "health.svg"},
}

LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
         "eiusmod tempor incididunt ut labore et dolore magna aliqua.")
LOREM_SHORT = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
               "do eiusmod tempor incididunt ut labore.")
LOREM_LONG = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
              "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
              "enim ad minim veniam, quis nostrud exercitation ullamco laboris "
              "nisi ut aliquip ex ea commodo consequat.")
LOREM_EXTRA = ("Duis aute irure dolor in reprehenderit in voluptate velit esse "
               "cillum dolore eu fugiat nulla pariatur.")
LOREM_XL = (LOREM_LONG + " " + LOREM_EXTRA + " Excepteur sint occaecat cupidatat "
            "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
LOREM_XXL = (LOREM_XL + " Sed ut perspiciatis unde omnis iste natus error sit "
             "voluptatem accusantium doloremque laudantium, totam rem aperiam.")


def dims(t=0, r=0, b=0, l=0, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": False}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True,
            "unit": "px", "size": size}


def fluid(mn, vw, mx):
    """Elementor custom-unit clamp() font size (fluid responsive type)."""
    return {"unit": "custom", "size": f"clamp({mn}px, {vw}vw, {mx}px)", "sizes": []}


def fluid_size(settings, mn, vw, mx):
    settings["typography_typography"] = "custom"
    settings["typography_font_size"] = fluid(mn, vw, mx)
    settings.pop("typography_font_size_tablet", None)
    settings.pop("typography_font_size_mobile", None)
    return settings


def typography(size=None, weight=None, line_height=None, letter_spacing=None,
               transform=None):
    out = {"typography_typography": "custom"}
    if size is not None:
        out["typography_font_size"] = {"unit": "px", "size": size, "sizes": []}
    if weight is not None:
        out["typography_font_weight"] = str(weight)
    if line_height is not None:
        out["typography_line_height"] = {"unit": "em", "size": line_height, "sizes": []}
    if letter_spacing is not None:
        out["typography_letter_spacing"] = {"unit": "px", "size": letter_spacing, "sizes": []}
    if transform is not None:
        out["typography_text_transform"] = transform
    return out


def container(nid, settings, elements, is_inner=True):
    return {"id": nid, "elType": "container", "settings": settings,
            "elements": elements, "isInner": is_inner}


def widget(nid, wtype, settings):
    return {"id": nid, "elType": "widget", "widgetType": wtype,
            "settings": settings, "elements": [], "isInner": False}


def heading(nid, title, tag="h2", color=None, align=None, extra=None):
    s = {"title": title, "header_size": tag}
    if align:
        s["align"] = align
    if color:
        s["title_color"] = color
    if extra:
        s.update(extra)
    return widget(nid, "heading", s)


def eyebrow(nid, text):
    return heading(nid, text, "p", NAVY, "left",
                   typography(size=13, weight=700, line_height=1.4,
                              letter_spacing=2, transform="uppercase"))


def h2(nid, text, size=44):
    # wire: --type-section clamp(32px, 3.4vw, 44px) — fluid, no breakpoint steps
    extra = typography(weight=600, line_height=1.15, letter_spacing=-0.8)
    extra["typography_font_size"] = fluid(32, 3.4, size)
    return heading(nid, text, "h2", NAVY, "left", extra)


def para(nid, text, color=BODY):
    return widget(nid, "text-editor", {
        "editor": f"<p>{text}</p>",
        "text_color": color,
        **typography(size=16, weight=400, line_height=1.65),
    })


def text_link(nid, text, url, size=16, color=BLUE):
    return widget(nid, "button", {
        "text": text,
        "link": {"url": url, "is_external": False, "nofollow": False},
        "align": "left",
        "border_border": "none",
        "text_padding": dims(0, 0, 0, 0),
        "background_color": "rgba(0,0,0,0)",
        "button_text_color": color,
        "typography_typography": "custom",
        "typography_font_size": {"unit": "px", "size": size, "sizes": []},
        "typography_font_weight": "700",
    })


def placeholder(nid, height=420, soft=False, radius=16):
    return container(nid, {
        "content_width": "full",
        "min_height": {"unit": "px", "size": height, "sizes": []},
        "background_background": "classic",
        "background_color": PLACE_SOFT if soft else PLACE,
        "border_radius": dims(radius, radius, radius, radius),
    }, [])


def image(nid, media, height=None, radius=16):
    s = {
        "image": dict(media),
        "width": {"unit": "%", "size": 100, "sizes": []},
    }
    if height:
        s["height"] = {"unit": "px", "size": height, "sizes": []}
    s["object-fit"] = "cover"
    if radius:
        s["image_border_radius"] = dims(radius, radius, radius, radius)
    return widget(nid, "image", s)


def intro_column(nid, num, title, text, url):
    return container(nid, {
        "content_width": "full", "width": {"unit": "%", "size": 33.33, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column", "padding": dims(32, 40, 36, 40),
        "padding_mobile": dims(20, 20, 20, 20),
        "border_border": "solid", "border_width": dims(0, 1, 0, 0),
        "border_width_mobile": dims(0, 0, 1, 0), "border_color": RULE,
    }, [
        heading(f"{nid}_num", num, "p", PLACE, "left",
                typography(size=40, weight=500, line_height=1.2, letter_spacing=-1.6)),
        heading(f"{nid}_title", title, "h3", NAVY, "left",
                typography(size=22, weight=700, line_height=1.2)),
        para(f"{nid}_text", text),
        text_link(f"{nid}_link", "Learn more \u2192", url, size=16, color=NAVY),
    ])


def intro_strip(prefix, columns, section_bg=SLATE, pad_top=0, pad_bottom=72):
    # The card is a full-width child of a boxed 1200 section, so the white box
    # (bg + radius + shadow) is itself 1200px - matching the Home intro strip.
    card = container(f"{prefix}_card", {
        "content_width": "full",
        "flex_direction": "row", "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap",
        "flex_wrap_mobile": "wrap",
        "background_background": "classic", "background_color": WHITE,
        "border_radius": dims(16, 16, 16, 16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
    }, [intro_column(f"{prefix}_{i}", *c) for i, c in enumerate(columns)])
    return container(prefix, {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "background_background": "classic",
        "background_color": section_bg, "padding": dims(pad_top, 40, pad_bottom, 40),
        "flex_direction": "column",
    }, [card])


def set_bg(node, hex_color):
    s = node["settings"]
    s["background_background"] = "classic"
    s["background_color"] = hex_color
    for k in ("background_color_b", "background_color_b_stop",
              "background_color_stop", "background_gradient_type",
              "background_gradient_angle"):
        s.pop(k, None)
    gl = s.get("__globals__", {})
    gl.pop("background_color", None)
    gl.pop("background_color_b", None)
    if gl:
        s["__globals__"] = gl
    elif "__globals__" in s:
        del s["__globals__"]
