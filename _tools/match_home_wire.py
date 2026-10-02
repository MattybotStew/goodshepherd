"""Rebuild Home (post 315) so the WordPress canvas matches the React wire
(src/pages/HomePage.jsx at localhost:5173).

Run:  python3 _tools/match_home_wire.py
Reads /tmp/home315_orig.json (dumped from wp post meta get 315 _elementor_data)
and writes /tmp/home_wire.json.
"""
import json

SRC = "/tmp/home315_orig.json"
OUT = "/tmp/home_wire.json"

# --- media uploaded from src/assets (see conversation) ---
HERO = {"id": "2171", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/hero.jpg"}
WORKSHOP = {"id": "2172", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/mosaic-workshop.jpg"}
KITCHEN = {"id": "2173", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/mosaic-kitchen.jpg"}
GARDEN = {"id": "2174", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/mosaic-garden.jpg"}
PORCH = {"id": "2175", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/mosaic-porch.jpg"}
ICONS = {
    "/programs/community-day-services": {"id": "2176", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/community-day.svg"},
    "/programs/vocational": {"id": "2177", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/vocational.svg"},
    "/programs/special-olympics": {"id": "2178", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/special-olympics.svg"},
    "/programs/residential-living": {"id": "2179", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/residential.svg"},
    "/programs/health-well-being": {"id": "2180", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/health.svg"},
}

NAVY = "#002A4E"
BLUE = "#0089DF"
BODY = "#303336"
SLATE = "#F1F5F9"
PALE = "#FAFCFE"
RULE = "#E8EDF2"

LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
         "eiusmod tempor incididunt ut labore et dolore magna aliqua.")
LOREM_SHORT = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
               "do eiusmod tempor incididunt ut labore.")


def dims(t=None, r=None, b=None, l=None, unit="px"):
    return {"unit": unit, "top": t, "right": r, "bottom": b, "left": l, "isLinked": False}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def typography(size=None, weight=None, line_height=None, letter_spacing=None, transform=None):
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


def widget(nid, wtype, settings, is_inner=False):
    return {"id": nid, "elType": "widget", "widgetType": wtype,
            "settings": settings, "elements": [], "isInner": is_inner}


def heading(nid, title, tag="h2", color=None, align=None, extra=None):
    s = {"title": title, "header_size": tag}
    if align:
        s["align"] = align
    if color:
        s["title_color"] = color
    if extra:
        s.update(extra)
    return widget(nid, "heading", s)


def set_bg(node, hex_color):
    s = node["settings"]
    s["background_background"] = "classic"
    s["background_color"] = hex_color
    s.pop("background_color_b", None)
    s.pop("background_color_b_stop", None)
    s.pop("background_color_stop", None)
    s.pop("background_gradient_type", None)
    s.pop("background_gradient_angle", None)
    gl = s.get("__globals__", {})
    gl.pop("background_color", None)
    gl.pop("background_color_b", None)
    if gl:
        s["__globals__"] = gl
    elif "__globals__" in s:
        del s["__globals__"]


def set_text_color(node, hex_color):
    s = node["settings"]
    s["title_color"] = hex_color
    gl = s.get("__globals__", {})
    gl.pop("title_color", None)
    if gl:
        s["__globals__"] = gl
    elif "__globals__" in s:
        del s["__globals__"]


def text_link_button(nid, text, url, size=16, color=NAVY, icon=True):
    s = {
        "text": text,
        "link": {"url": url, "is_external": False, "nofollow": False},
        "align": "left",
        "border_border": "none",
        "text_padding": dims("0", "0", "0", "0"),
        "background_color": "rgba(0,0,0,0)",
        "button_text_color": color,
        "typography_typography": "custom",
        "typography_font_size": {"unit": "px", "size": size, "sizes": []},
        "typography_font_weight": "700",
    }
    if icon:
        s["selected_icon"] = {"value": "fas fa-long-arrow-alt-right", "library": "fa-solid"}
        s["icon_align"] = "row-reverse"
        s["icon_indent"] = {"unit": "px", "size": 6, "sizes": []}
    return widget(nid, "button", s)


# --------------------------------------------------------------------------
data = json.load(open(SRC))
byid = {}


def index(nodes):
    for n in nodes:
        byid[n["id"]] = n
        index(n.get("elements", []))


index(data)

# =========================== 1. HERO ======================================
hero = byid["138ba28"]
hs = hero["settings"]
hs["background_image"] = dict(HERO)
hs["background_overlay_color"] = "#001424"
hs["background_overlay_opacity"] = {"unit": "px", "size": 0.6, "sizes": []}
hs.get("__globals__", {}).pop("background_overlay_color", None)

hero_p = byid["1050c07"]
hero_p["settings"].update(typography(size=19, weight=400, line_height=1.65))
hero_p["settings"]["typography_font_size_tablet"] = {"unit": "px", "size": 17, "sizes": []}
hero_p["settings"]["title_color"] = "rgba(255,255,255,0.92)"
hero_p["settings"].get("__globals__", {}).pop("title_color", None)
hero_p["settings"]["_padding"] = dims("0", "210", "40", "210")

# =========================== 2. INTRO STRIP ================================
intro = byid["b233779"]
set_bg(intro, SLATE)

card = byid["66df653"]
card["settings"]["border_border"] = "none"
card["settings"]["border_radius"] = dims("16", "16", "16", "16")
card["settings"]["box_shadow_box_shadow_type"] = "yes"
card["settings"]["box_shadow_box_shadow"] = {
    "horizontal": 0, "vertical": 12, "blur": 32, "spread": 0,
    "color": "rgba(0,42,78,0.12)",
}
card["settings"].get("__globals__", {}).pop("border_color", None)

for col_id in ("8aa656b", "eacef01", "137de2d"):
    c = byid[col_id]["settings"]
    c["border_color"] = RULE
    c.get("__globals__", {}).pop("border_color", None)

num = byid["c340137"]["settings"]
num.update(typography(size=40, weight=500, line_height=1.2, letter_spacing=-1.6))

for num_id in ("c2bd476", "0be7ecc"):
    byid[num_id]["settings"].update(typography(size=40, weight=500, line_height=1.2, letter_spacing=-1.6))

for ib_id in ("7b6ee0d", "0497ba5", "67bdf6f"):
    s = byid[ib_id]["settings"]
    s["title_typography_typography"] = "custom"
    s["title_typography_font_size"] = {"unit": "px", "size": 22, "sizes": []}
    s["title_typography_font_weight"] = "700"
    s["description_typography_typography"] = "custom"
    s["description_typography_font_size"] = {"unit": "px", "size": 16, "sizes": []}
    s["description_typography_line_height"] = {"unit": "em", "size": 1.65, "sizes": []}

for btn_id, url in (("9db92a4", "/programs"), ("7b30df7", "/support-gsm"), ("4dc8404", "/support-gsm")):
    s = byid[btn_id]["settings"]
    s["typography_font_size"] = {"unit": "px", "size": 16, "sizes": []}
    s["typography_font_weight"] = "700"
    s["button_text_color"] = "var(--ast-global-color-2)"
    s["__globals__"] = s.get("__globals__", {})
    s["__globals__"]["button_text_color"] = "globals/colors?id=astglobalcolor2"
    s["__globals__"].pop("background_color", None)
    s["background_color"] = "rgba(0,0,0,0)"
    s["border_border"] = "none"
    s["text_padding"] = dims("0", "0", "0", "0")

# =========================== 3. IMPACT =====================================
impact = byid["78cc2f2"]
set_bg(impact, SLATE)

set_text_color(byid["cd53980"], NAVY)
byid["cd53980"]["settings"].update(typography(size=44, weight=600, line_height=1.15, letter_spacing=-0.8))
byid["cd53980"]["settings"]["header_size"] = "h2"

for counter_id in ("9de2e7f", "d2e6f88", "4a8b216", "2904838"):
    s = byid[counter_id]["settings"]
    s["title_color"] = "#4A6278"
    s.get("__globals__", {}).pop("title_color", None)
    s["typography_title_font_size"] = {"unit": "px", "size": 15, "sizes": []}
    s["typography_title_font_weight"] = "500"
    s["typography_title_line_height"] = {"unit": "em", "size": 1.5, "sizes": []}

# wire shows "1971", not "1,971"
byid["2904838"]["settings"]["thousand_separator"] = ""

# ===================== 4. PROGRAMS & SERVICES (rebuild) ====================
programs = [
    {"name": "Community Day Services", "path": "/programs/community-day-services"},
    {"name": "TBD Vocational Program", "path": "/programs/vocational"},
    {"name": "Special Olympics", "path": "/programs/special-olympics"},
    {"name": "Residential Living", "path": "/programs/residential-living"},
    {"name": "Health & Well Being", "path": "/programs/health-well-being"},
]

prog_h2_widget = heading("prog_h2", "Our Programs &amp; Services", "h2", NAVY, "left",
                         typography(size=48, weight=600, line_height=1.2, letter_spacing=-1))
prog_h2_widget["settings"]["typography_font_size_tablet"] = {"unit": "px", "size": 36, "sizes": []}
prog_h2_widget["settings"]["typography_font_size_mobile"] = {"unit": "px", "size": 32, "sizes": []}

prog_intro = container("prog_intro", {
    "content_width": "full",
    "width": {"unit": "%", "size": 72, "sizes": []},
    "width_tablet": {"unit": "%", "size": 100, "sizes": []},
    "width_mobile": {"unit": "%", "size": 100, "sizes": []},
    "flex_direction": "column",
    "flex_gap": gap(0),
}, [
    prog_h2_widget,
    heading("prog_lede", LOREM, "p", BODY, "left",
            typography(size=16, weight=400, line_height=1.6)),
])

prog_more = container("prog_more", {
    "content_width": "full",
    "width": {"unit": "%", "size": 28, "sizes": []},
    "width_tablet": {"unit": "%", "size": 100, "sizes": []},
    "width_mobile": {"unit": "%", "size": 100, "sizes": []},
    "flex_direction": "column",
    "flex_align_items": "flex-end",
    "flex_align_items_tablet": "flex-start",
    "flex_align_items_mobile": "flex-start",
}, [
    text_link_button("prog_view_all", "View all programs", "/programs", size=18, color=BLUE),
])

prog_head = container("prog_head", {
    "content_width": "full",
    "flex_direction": "row",
    "flex_direction_tablet": "column",
    "flex_direction_mobile": "column",
    "flex_justify_content": "space-between",
    "flex_align_items": "flex-end",
    "flex_align_items_tablet": "flex-start",
    "flex_align_items_mobile": "flex-start",
    "flex_wrap": "nowrap",
    "flex_gap": gap(24),
    "flex_gap_tablet": gap(16),
    "flex_gap_mobile": gap(16),
    "margin": dims("0", "0", "32", "0"),
}, [prog_intro, prog_more])

cards = []
for i, p in enumerate(programs):
    is_first, is_last = i == 0, i == len(programs) - 1
    radius = dims("0", "0", "0", "0")
    if is_first:
        radius = dims("16", "0", "0", "16")
    if is_last:
        radius = dims("0", "16", "16", "0")
    card_settings = {
        "content_width": "full",
        "width": {"unit": "%", "size": 20, "sizes": []},
        "width_tablet": {"unit": "%", "size": 50, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "flex_gap": gap(0),
        "padding": dims("32", "28", "36", "28"),
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "border_radius": radius,
    }
    if not is_last:
        card_settings.update({
            "border_border": "solid",
            "border_width": dims("0", "1", "0", "0"),
            "border_width_mobile": dims("0", "0", "1", "0"),
            "border_color": RULE,
        })
    icon_box = container(f"prog_iconbox_{i}", {
        "content_width": "full",
        "width": {"unit": "px", "size": 48, "sizes": []},
        "width_tablet": {"unit": "px", "size": 48, "sizes": []},
        "width_mobile": {"unit": "px", "size": 48, "sizes": []},
        "min_height": {"unit": "px", "size": 48, "sizes": []},
        "flex_direction": "row",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims("12", "12", "12", "12"),
        "margin": dims("0", "0", "16", "0"),
    }, [
        widget(f"prog_icon_{i}", "image", {
            "image": dict(ICONS[p["path"]]),
            "width": {"unit": "px", "size": 24, "sizes": []},
            "height": {"unit": "px", "size": 24, "sizes": []},
            "object-fit": "contain",
        })
    ])
    title = heading(f"prog_title_{i}", p["name"], "h3", NAVY, "left",
                    typography(size=22, weight=700, line_height=1.2))
    title["settings"]["_margin"] = dims("0", "0", "10", "0")
    desc = widget(f"prog_desc_{i}", "text-editor", {
        "editor": f"<p>{LOREM_SHORT}</p>",
        "text_color": "#4B4D50",
        "_flex_size": "grow",
        **typography(size=16, weight=400, line_height=1.5),
    })
    link = text_link_button(f"prog_btn_{i}", "Learn more \u2192", p["path"], size=16, color=NAVY, icon=False)
    cards.append(container(f"prog_card_{i}", card_settings, [icon_box, title, desc, link]))

prog_row = container("prog_row", {
    "content_width": "full",
    "flex_direction": "row",
    "flex_wrap": "nowrap",
    "flex_wrap_tablet": "wrap",
    "flex_wrap_mobile": "wrap",
    "flex_gap": gap(0),
    "background_background": "classic",
    "background_color": "#FFFFFF",
    "border_radius": dims("16", "16", "16", "16"),
    "box_shadow_box_shadow_type": "yes",
    "box_shadow_box_shadow": {
        "horizontal": 0, "vertical": 12, "blur": 32, "spread": 0,
        "color": "rgba(0,42,78,0.12)",
    },
}, cards)

prog_sec = byid["prog_sec"]
set_bg(prog_sec, PALE)
prog_sec["settings"]["padding"] = dims("64", "24", "88", "24")
prog_sec["elements"] = [prog_head, prog_row]

# =========================== 5. ABOUT ======================================
about = byid["e743605"]
set_bg(about, SLATE)

# copy column: wire keeps the h2 to 460px so the title wraps to three lines
byid["4892689"]["settings"]["padding"] = dims("0", "76", "0", "0")

about_h2 = byid["7a81b49"]["settings"]
about_h2.update(typography(size=44, weight=600, line_height=1.15, letter_spacing=-0.8))
about_h2["typography_typography"] = "custom"

set_text_color(byid["1251f3f"], BODY)
byid["1251f3f"]["settings"]["typography_font_weight"] = "700"
byid["1251f3f"]["settings"]["typography_letter_spacing"] = {"unit": "px", "size": 1.5, "sizes": []}

# first paragraph lives in the image-box description
ib = byid["aa50bb0"]["settings"]
ib["description_typography_typography"] = "custom"
ib["description_typography_font_size"] = {"unit": "px", "size": 16, "sizes": []}
ib["description_typography_line_height"] = {"unit": "em", "size": 1.65, "sizes": []}
ib["description_color"] = BODY

p2 = byid["about_p2"]["settings"]
p2["text_color"] = BODY
p2.update(typography(size=16, weight=400, line_height=1.65))

# mosaic photos
for img_id, asset in (("0d09488", WORKSHOP), ("f3ad32e", KITCHEN),
                      ("20d717a", GARDEN), ("49d2511", PORCH)):
    byid[img_id]["settings"]["image"] = dict(asset)

# Read More outline button
rm = byid["2e4da81"]["settings"]
rm["typography_typography"] = "custom"
rm["typography_font_size"] = {"unit": "px", "size": 16, "sizes": []}
rm["typography_font_weight"] = "700"
rm["border_border"] = "solid"
rm["border_width"] = dims("1", "1", "1", "1")
rm["border_color"] = "var(--ast-global-color-2)"
rm["border_radius"] = dims("8", "8", "8", "8")
rm["text_padding"] = dims("16", "24", "16", "24")
rm["background_color"] = "rgba(0,0,0,0)"
rm["button_text_color"] = "var(--ast-global-color-2)"
rm["button_background_hover_color"] = NAVY
rm["hover_color"] = "#FFFFFF"
rm["__globals__"] = rm.get("__globals__", {})
rm["__globals__"].pop("background_color", None)
rm["__globals__"].pop("button_background_hover_color", None)
rm["__globals__"].pop("hover_color", None)
rm["__globals__"].pop("border_color", None)

# =========================== 6. SUPPORT ====================================
support = byid["support_gsm"]
# already #FAFCFE; keep explicit
set_bg(support, PALE)

sh2 = byid["support_h2"]["settings"]
sh2.update(typography(size=28, weight=600, line_height=1.2))

for i in range(4):
    cs = byid[f"support_card_{i}"]["settings"]
    cs["border_border"] = "none"
    cs["border_radius"] = dims("8", "8", "8", "8")
    cs["padding"] = dims("28", "24", "28", "24")

    ts = byid[f"support_title_{i}"]["settings"]
    ts.update(typography(size=18, weight=600, line_height=1.3))

    ds = byid[f"support_desc_{i}"]["settings"]
    ds["text_color"] = BODY
    ds.update(typography(size=15, weight=400, line_height=1.5))

    ls = byid[f"support_link_{i}"]["settings"]
    ls["border_border"] = "none"
    ls["text_padding"] = dims("0", "0", "0", "0")
    ls["background_color"] = "rgba(0,0,0,0)"
    ls["button_text_color"] = BLUE
    ls["typography_typography"] = "custom"
    ls["typography_font_size"] = {"unit": "px", "size": 14, "sizes": []}
    ls["typography_font_weight"] = "600"
    ls["selected_icon"] = {"value": "fas fa-long-arrow-alt-right", "library": "fa-solid"}
    ls["icon_align"] = "row-reverse"
    ls["icon_indent"] = {"unit": "px", "size": 6, "sizes": []}
    ls["__globals__"] = ls.get("__globals__", {})
    ls["__globals__"].pop("background_color", None)

# ===================== 7. Reorder + drop Stories ===========================
order = ["138ba28", "b233779", "78cc2f2", "prog_sec", "e743605", "support_gsm"]
new_data = [byid[nid] for nid in order]

json.dump(new_data, open(OUT, "w"), separators=(",", ":"))
print("wrote", OUT, "sections:", [n["id"] for n in new_data])
