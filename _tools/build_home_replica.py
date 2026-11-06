"""Build the Home page (315) as an exact Elementor replica of src/pages/HomePage.jsx.

Everything is native Elementor: containers + heading / text-editor / button /
image widgets. No raw HTML, no custom CSS — so the page stays editable in the
Elementor editor.

    python3 _tools/build_home_replica.py            # writes /tmp/home_replica.json
    ./_tools/apply_elementor.sh 315 /tmp/home_replica.json
"""

import json

# Host-agnostic: the same JSON has to render on Local and on stage.
BASE = "/wp-content/uploads/"

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


# ---------------------------------------------------------------- content

HERO_IMAGE = (2171, "2026/10/hero.jpg")
# Pre-cropped to the wire's mosaic ratios (316.8x339 tall, 316.8x248 short) so the
# section height matches the React build instead of following each photo's ratio.
MOSAIC = [
    (2374, "2026/11/mosaic-workshop-tall.jpg", "tall"),
    (2372, "2026/11/mosaic-kitchen-short.jpg", "short"),
    (2371, "2026/11/mosaic-garden-short.jpg", "short"),
    (2373, "2026/11/mosaic-porch-tall.jpg", "tall"),
]
PROGRAM_ICONS = {
    "/programs/community-day-services": (2176, "2026/10/community-day.svg"),
    "/programs/special-olympics": (2178, "2026/10/special-olympics.svg"),
    "/programs/residential-living": (2179, "2026/10/residential.svg"),
    "/programs/health-well-being": (2180, "2026/10/health.svg"),
}

INTRO_CARDS = [
    ("01.", "Get Involved",
     "Share your time and talents, join an event, or volunteer to make a meaningful difference in the lives of the men at GSM.",
     "/events"),
    ("02.", "Donate",
     "Help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home.",
     "/support-gsm"),
    ("03.", "News You Can Use",
     "Get connected with Manor news, newsletters, useful updates and resources for GSM families",
     "/news"),
]

STATS = [
    ("55+", "Years serving our community"),
    ("100+", "Men supported daily"),
    ("2", "Core programs offered"),
    ("1971", "Founded in Momence, IL"),
]

# Client order (2026-11-06): CDS, Residential, Health, Community Engagement.
# Vocational is not a program page — its content lives inside Community Day Services.
PROGRAMS = [
    ("Community Day Services", "Our Community Day Services build skills, friendships, and meaningful community connections.",
     "/programs/community-day-services"),
    ("Residential Living", "Our 13 CILA homes offer welcoming living across our 60-acre campus and the city of Momence",
     "/programs/residential-living"),
    ("Health & Well Being", "Personalized support helps each man stay active, feel his best, and enjoy a fulfilling life.",
     "/programs/health-well-being"),
    ("Community Engagement", "Explore interests and connect with others through activities, outings and Special Olympics.",
     "/programs/special-olympics"),
]

STORIES = [
    ("GSM's Annual Fall Festival",
     "An annual celebration of family fun, community spirit, and support for the men of GSM.",
     "/events#fall-festival"),
    ("GSM Family Cookouts & More",
     "Celebrating 35 years of family fun, community spirit, and support for the men of GSM.",
     "/events#family"),
]


# ---------------------------------------------------------------- sections

def build_hero():
    intro_cols = []
    for i, (num, title, desc, url) in enumerate(INTRO_CARDS):
        col_settings = {
            "content_width": "full",
            "width": {"unit": "%", "size": 33.33, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "padding": px(32, 40, 36, 40),
            "padding_mobile": px(24),
        }
        if i < len(INTRO_CARDS) - 1:
            col_settings.update({
                "border_border": "solid",
                "border_width": px(0, 1, 0, 0),
                "border_color": "#E8EDF2",
            })
        intro_cols.append(container(f"hi_col{i}", col_settings, [
            heading(f"hi_num{i}", num, "p", color="#7D93A8", size_px=40,
                    weight="500", line_height=1.2, letter_spacing=-1.6,
                    margin=(0, 0, 16, 0)),
            heading(f"hi_title{i}", title, "h3", color="#002A4E", size_px=22,
                    weight="700", line_height=1.2, letter_spacing=0,
                    margin=(0, 0, 10, 0)),
            text(f"hi_desc{i}", f"<p>{desc}</p>", margin=(0, 0, 20, 0)),
            link_button(f"hi_link{i}", "Learn more →", url, margin=(0, 0, 0, 0)),
        ], inner=True))

    intro = container("hi_row", {
        "content_width": "boxed",
        "boxed_width": size(1200),
        "flex_direction": "row",
        "flex_gap": gap(0),
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "border_radius": px(16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
        "margin": px(-160, 0, 0, 0),
        "margin_tablet": px(-96, 0, 0, 0),
        "margin_mobile": px(-64, 0, 0, 0),
        "z_index": 2,
        "_element_id": "home-intro",
    }, intro_cols, inner=True)

    hero_inner = inner("hero_inner", [
        heading("hero_h1", "A Community of Compassion, Dignity, and Purpose.",
                "h1", color="#FFFFFF", size_px=64, weight="600",
                line_height=1.12, letter_spacing=-1.2, align="center",
                margin=(0, 0, 20, 0)),
        text("hero_p",
             "<p>Supporting men with intellectual and developmental disabilities through compassionate care, meaningful opportunities, and a life rich with possibility</p>",
             color="rgba(255,255,255,0.92)", size_px=19, line_height=1.65,
             align="center", margin=(0, 0, 40, 0), max_width=660),
        cta_button("hero_cta", "Learn more", "/about"),
    ], width=1080, flex_align_items="center")

    hero = container("hero", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
        "min_height": size(868),
        "background_background": "classic",
        "background_image": {"id": str(HERO_IMAGE[0]), "url": BASE + HERO_IMAGE[1], "size": ""},
        "background_position": "center center",
        "background_repeat": "no-repeat",
        "background_size": "cover",
        "background_overlay_background": "classic",
        "background_overlay_color": "#001424",
        "background_overlay_opacity": {"unit": "px", "size": 0.62, "sizes": []},
        "padding": px(108, 24, 160, 24),
        "padding_tablet": px(96, 32, 140, 32),
        "padding_mobile": px(88, 24, 120, 24),
        "_element_id": "home-hero",
    }, [hero_inner])

    band = container("intro_band", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": "#F1F5F9",
        "padding": px(0, 24, 56, 24),
        "padding_tablet": px(0, 32, 40, 32),
        "padding_mobile": px(0, 24, 32, 24),
        "_element_id": "home-intro-band",
    }, [intro])

    return [hero, band]


def build_impact():
    header = container("imp_head", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(100),
        "flex_align_items": "start",
        "flex_wrap": "wrap",
    }, [
        container("imp_h2col", {
            "content_width": "full",
            "width": {"unit": "%", "size": 44, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            heading("imp_h2", "Our Mission &amp; Vision: Serving with Dignity", "h2",
                    size_px=44, weight="600", line_height=1.15, letter_spacing=-0.8,
                    margin=(0, 0, 0, 0)),
        ], inner=True),
        container("imp_ledecol", {
            "content_width": "full",
            "width": {"unit": "%", "size": 44, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            text("imp_lede",
                 "<p>We honor the dignity of every man we serve, providing compassionate care, encouraging personal growth, and creating a welcoming community where men with disabilities feel valued, supported, and at home.</p>",
                 margin=(0, 0, 0, 0)),
        ], inner=True),
    ], inner=True)

    stats = []
    for i, (value, label) in enumerate(STATS):
        st = {
            "content_width": "full",
            "width": {"unit": "%", "size": 23.75, "sizes": []},
            "width_mobile": {"unit": "%", "size": 46, "sizes": []},
            "flex_direction": "column",
            "padding": px(0, 24, 20, 0),
        }
        if i < len(STATS) - 1:
            st.update({
                "border_border": "solid",
                "border_width": px(0, 1, 0, 0),
                "border_color": "#C8D4E0",
            })
        stats.append(container(f"imp_stat{i}", st, [
            heading(f"imp_val{i}", value, "p", color="#002A4E", size_px=48,
                    weight="700", line_height=1.2, letter_spacing=-0.5,
                    margin=(0, 0, 8, 0)),
            heading(f"imp_lbl{i}", label, "p", color="#4A6278", size_px=15,
                    weight="500", line_height=1.5, letter_spacing=0,
                    margin=(0, 0, 0, 0)),
        ], inner=True))

    stats_row = container("imp_stats", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(20),
        "flex_wrap": "wrap",
        "margin": px(32, 0, 0, 0),
    }, stats, inner=True)

    return section("impact", "#F1F5F9", (24, 24, 96, 24), [
        inner("imp_inner", [header, stats_row]),
    ])


def build_programs():
    head = container("prog_head", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_justify_content": "space-between",
        "flex_align_items": "end",
        "flex_gap": gap(24),
        "flex_wrap": "wrap",
        "margin": px(0, 0, 32, 0),
    }, [
        container("prog_intro", {
            "content_width": "full",
            "width": {"unit": "%", "size": 62, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            heading("prog_h2", "Our Programs &amp; Services", "h2", size_px=48,
                    weight="600", line_height=1.2, letter_spacing=-1,
                    margin=(0, 0, 20, 0)),
            text("prog_lede",
                 "<p>Explore the programs and services that bring care, opportunity, and purpose to everyday life.</p>",
                 max_width=600, margin=(0, 0, 0, 0)),
        ], inner=True),
        link_button("prog_more", "Explore Our Programs →", "/programs", size_px=18,
                    margin=(0, 0, 0, 0)),
    ], inner=True)

    cards = []
    for i, (name, desc, url) in enumerate(PROGRAMS):
        cards.append(container(f"prog_card{i}", {
            "content_width": "full",
            "width": {"unit": "%", "size": 24.9, "sizes": []},
            "width_tablet": {"unit": "%", "size": 49.9, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "padding": px(32, 28, 36, 28),
            "padding_mobile": px(24),
        }, [
            container(f"prog_icon{i}", {
                "content_width": "full",
                "width": size(48),
                "min_height": size(48),
                "flex_direction": "column",
                "flex_justify_content": "center",
                "flex_align_items": "center",
                "background_background": "classic",
                "background_color": "#002A4E",
                "border_radius": px(12),
                "margin": px(0, 0, 16, 0),
            }, [
                image(f"prog_iconimg{i}", PROGRAM_ICONS[url][0], PROGRAM_ICONS[url][1], radius=0),
            ], inner=True),
            heading(f"prog_title{i}", name, "h3", color="#002A4E", size_px=22,
                    weight="700", line_height=1.2, letter_spacing=0, margin=(0, 0, 10, 0)),
            text(f"prog_desc{i}", f"<p>{desc}</p>", color="#4B4D50", line_height=1.5,
                 margin=(0, 0, 20, 0), flex_grow=True),
            link_button(f"prog_link{i}", "Learn more+", url, color="#002A4E"),
        ], inner=True))

    grid = container("prog_grid", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(1),
        "flex_wrap": "wrap",
        "background_background": "classic",
        "background_color": "#E8EDF2",
        "border_radius": px(16),
        "overflow": "hidden",
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
    }, cards, inner=True)

    return section("programs", "#FAFCFE", (64, 24, 88, 24), [
        inner("prog_inner", [head, grid]),
    ])


def build_mission():
    copy_col = container("mis_copy", {
        "content_width": "full",
        "width": {"unit": "%", "size": 38.3, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, [
        heading("mis_eyebrow", "About Us", "p", color="#002A4E", size_px=13,
                weight="700", line_height=1.4, letter_spacing=1.56,
                text_transform="uppercase", margin=(0, 0, 16, 0)),
        heading("mis_h2", "A community of care, growth, and dignity for over 55 years.",
                "h2", size_px=44, weight="600", line_height=1.15,
                letter_spacing=-0.8, margin=(0, 0, 20, 0)),
        text("mis_p",
             "<p>Founded in 1971 by families seeking a brighter future for their sons, Good Shepherd Manor carries forward a legacy of faith and compassionate care. Today, we support men with intellectual and developmental disabilities build community, discover possibilities, and live with dignity and purpose.</p>",
             margin=(0, 0, 0, 0)),
        cta_button("mis_cta", "Read More", "/about", bg="rgba(0,0,0,0)",
                   color="#002A4E", padding=(16, 24), radius=8, border=(1, 1, 1, 1)),
    ], inner=True)

    def mosaic_img(cid, att, url):
        return image(cid, att, url, radius=16)

    col_a = container("mis_col_a", {
        "content_width": "full",
        "width": {"unit": "%", "size": 50, "sizes": []},
        "flex_direction": "column",
        "flex_gap": gap(20),
    }, [
        mosaic_img("mis_img0", MOSAIC[0][0], MOSAIC[0][1]),
        mosaic_img("mis_img1", MOSAIC[1][0], MOSAIC[1][1]),
    ], inner=True)

    col_b = container("mis_col_b", {
        "content_width": "full",
        "width": {"unit": "%", "size": 50, "sizes": []},
        "flex_direction": "column",
        "flex_gap": gap(20),
        "padding": px(80, 0, 0, 0),
        "padding_mobile": px(0),
    }, [
        mosaic_img("mis_img2", MOSAIC[2][0], MOSAIC[2][1]),
        mosaic_img("mis_img3", MOSAIC[3][0], MOSAIC[3][1]),
    ], inner=True)

    mosaic = container("mis_mosaic", {
        "content_width": "full",
        "width": {"unit": "%", "size": 54.5, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "row",
        "flex_gap": gap(20),
        "flex_align_items": "start",
    }, [col_a, col_b], inner=True)

    row = container("mis_row", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(86),
        "flex_align_items": "center",
        "flex_wrap": "wrap",
    }, [copy_col, mosaic], inner=True)

    return section("mission", "#F1F5F9", (96, 24, 96, 24), [row])


def build_stories():
    head = container("st_head", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "margin": px(0, 0, 0, 0),
    }, [
        heading("st_h2", "What's Happening at GSM", "h2", color="#002A4E",
                size_px=28, weight="600", line_height=1.2, letter_spacing=-0.4,
                align="center", margin=(0, 0, 16, 0)),
        text("st_lede",
             "<p>GSM brings our men and community together through a wide variety of activities &amp; events.</p>",
             align="center", margin=(0, 0, 12, 0), max_width=640),
        link_button("st_more", "See all events", "/events", size_px=15,
                    align="center", margin=(0, 0, 48, 0)),
    ], inner=True)

    cards = []
    for i, (title, excerpt, url) in enumerate(STORIES):
        cards.append(container(f"st_card{i}", {
            "content_width": "full",
            "width": {"unit": "%", "size": 31.85, "sizes": []},
            "width_tablet": {"unit": "%", "size": 48, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "flex_gap": gap(12),
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_radius": px(8),
            "padding": px(28, 24, 28, 24),
        }, [
            heading(f"st_title{i}", title, "h3", color="#002A4E", size_px=17.6,
                    weight="700", line_height=1.3, letter_spacing=0, margin=(0, 0, 0, 0)),
            text(f"st_exc{i}", f"<p>{excerpt}</p>", margin=(0, 0, 0, 0)),
            link_button(f"st_link{i}", "Read More", url, color="#002A4E",
                        size_px=14, margin=(0, 0, 0, 0)),
        ], inner=True))

    grid = container("st_grid", {
        "content_width": "full",
        "boxed_width": size(1080),
        "flex_direction": "row",
        "flex_gap": gap(24),
        "flex_wrap": "wrap",
        "flex_justify_content": "flex-start",
    }, cards, inner=True)

    return section("stories", "#FAFCFE", (72, 24, 72, 24), [
        inner("st_inner", [head, grid]),
    ])


def build():
    return [*build_hero(), build_impact(), build_programs(), build_mission(), build_stories()]


if __name__ == "__main__":
    data = build()
    with open("/tmp/home_replica.json", "w") as f:
        json.dump(data, f)
    print("wrote /tmp/home_replica.json", len(json.dumps(data)), "bytes")
