"""Build every content page as an Elementor replica of the React wires.

    python3 _tools/build_pages.py 2088           # -> /tmp/page_2088.json
    python3 _tools/build_pages.py all            # -> every page
    ./_tools/apply_elementor.sh 2088 /tmp/page_2088.json

Copy comes from _tools/page_data.json, a JSON dump of src/data/*.js produced by
importing those modules with Node. Re-generate it when the wires change:

    cp src/data/*.js /tmp/gsmdata/  # then rewrite './x' -> './x.js'
    node --input-type=module -e "…"  # see AGENTS.md
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from elementor_kit import (BASE, px, gap, size, container, widget, heading,
                           text, link_button, cta_button, image, section, inner)

DATA = json.load(open(os.path.join(os.path.dirname(__file__), "page_data.json")))

INK = "#002A4E"
BODY = "#303336"
ALT = "#F1F5F9"
SOFT = "#FAFCFE"
LINK = "#006BB3"

# GSM photography already in the media library
IMG = {
    "hero": (2171, "2026/10/hero.jpg"),
    "workshop": (2172, "2026/10/mosaic-workshop.jpg"),
    "kitchen": (2173, "2026/10/mosaic-kitchen.jpg"),
    "garden": (2174, "2026/10/mosaic-garden.jpg"),
    "porch": (2175, "2026/10/mosaic-porch.jpg"),
    "day": (2260, "2026/11/Day-Program-1.jpg"),
    "vocational": (2326, "2026/11/Vocational-1.jpg"),
    "infirmary": (2288, "2026/11/Infirmary-1.jpg"),
    "community": (2253, "2026/11/BGS-Momence-010.jpg"),
    "sing": (2263, "2026/11/dollars-at-work-2-scaled.jpg"),
    "chapel": (2265, "2026/11/dollars-at-work-4-scaled.jpg"),
    "chapel_hands": (2266, "2026/11/dollars-at-work-5-scaled.jpg"),
    "festival": (2264, "2026/11/dollars-at-work-3-scaled.jpg"),
    "golf": (2218, "2026/11/2014-Golf-Fun-on-Hole-18-scaled.jpg"),
}
ICONS = {
    "cds": (2176, "2026/10/community-day.svg"),
    "engagement": (2178, "2026/10/special-olympics.svg"),
    "residential": (2179, "2026/10/residential.svg"),
    "health": (2180, "2026/10/health.svg"),
}

CRUMB_PREFIX = "Programs & Services"


# ------------------------------------------------------------------ blocks

def rich_blocks(blocks, prefix):
    """Render React rich-text blocks as native Elementor widgets."""
    out = []
    for i, b in enumerate(blocks):
        cid = f"{prefix}_{i}"
        t = b.get("type")
        if t == "p":
            out.append(text(cid, f"<p>{b['text']}</p>", margin=(0, 0, 16, 0)))
        elif t == "h3":
            out.append(heading(cid, b["text"], "h3", color=INK, size_px=20,
                               weight="600", line_height=1.35, letter_spacing=-0.2,
                               margin=(8, 0, 8, 0)))
        elif t in ("ul", "ol"):
            items = "".join(f"<li>{x}</li>" for x in b["items"])
            tag = "ul" if t == "ul" else "ol"
            out.append(text(cid, f"<{tag}>{items}</{tag}>", margin=(0, 0, 16, 0)))
        elif t == "figure":
            out.append(image(cid, IMG["day"][0], IMG["day"][1], radius=16))
            if b.get("caption"):
                out.append(text(cid + "_cap", f"<p><em>{b['caption']}</em></p>",
                                color="#5A6B7B", size_px=14, margin=(8, 0, 24, 0)))
        elif t == "quote":
            out.append(text(cid, f"<blockquote><p>{b.get('text','')}</p>"
                                 f"<cite>{b.get('cite','')}</cite></blockquote>",
                            margin=(0, 0, 20, 0)))
        elif t == "callout":
            out.append(text(cid, f"<p><strong>{b.get('title','')}</strong><br/>{b.get('text','')}</p>",
                            margin=(0, 0, 20, 0)))
        elif t == "link":
            out.append(link_button(cid, b["label"] + " →", b["to"], margin=(0, 0, 16, 0)))
    return out


def numbered_card(prefix, i, num, title, body, url, link_label="Learn more"):
    return container(f"{prefix}_card{i}", {
        "content_width": "full",
        "width": {"unit": "%", "size": 33.33, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "padding": px(32, 40, 36, 40),
        "padding_mobile": px(24),
    }, [
        heading(f"{prefix}_num{i}", num, "p", color="#7D93A8", size_px=40,
                weight="500", line_height=1.2, letter_spacing=-1.6, margin=(0, 0, 16, 0)),
        heading(f"{prefix}_title{i}", title, "h3", color=INK, size_px=22,
                weight="700", line_height=1.2, letter_spacing=0, margin=(0, 0, 10, 0)),
        text(f"{prefix}_body{i}", f"<p>{body}</p>", margin=(0, 0, 20, 0), flex_grow=True),
        link_button(f"{prefix}_link{i}", f"{link_label} →", url, margin=(0, 0, 0, 0)),
    ], inner=True)


def cards_strip(prefix, cards, bg=SOFT, overlap=True):
    """The white 3-card strip used under heroes (Home / Support / Events)."""
    cols = [numbered_card(prefix, i, *c) for i, c in enumerate(cards)]
    row = container(f"{prefix}_row", {
        "content_width": "boxed",
        "boxed_width": size(1200),
        "flex_direction": "row",
        "flex_gap": gap(0),
        "flex_wrap": "wrap",
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "border_radius": px(16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
        "margin": px(-120 if overlap else 0, 0, 0, 0),
        "margin_tablet": px(-80 if overlap else 0, 0, 0, 0),
        "margin_mobile": px(-56 if overlap else 0, 0, 0, 0),
        "z_index": 2,
        "_element_id": f"{prefix}-cards",
    }, cols, inner=True)

    band = container(f"{prefix}_band", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": bg,
        "padding": px(0 if overlap else 56, 24, 48, 24),
        "padding_mobile": px(0 if overlap else 40, 24, 32, 24),
    }, [row])
    return band


def hero(title, lede, img="hero", height=520, align="center"):
    att, url = IMG[img]
    return container("hero", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
        "min_height": size(height),
        "background_background": "classic",
        "background_image": {"id": str(att), "url": BASE + url, "size": ""},
        "background_position": "center center",
        "background_repeat": "no-repeat",
        "background_size": "cover",
        "background_overlay_background": "classic",
        "background_overlay_color": "#001424",
        "background_overlay_opacity": {"unit": "px", "size": 0.62, "sizes": []},
        "padding": px(140, 24, 96, 24),
        "padding_tablet": px(120, 32, 80, 32),
        "padding_mobile": px(104, 24, 64, 24),
        "_element_id": "page-hero",
    }, [
        inner("hero_inner", [
            heading("hero_h1", title, "h1", color="#FFFFFF", size_px=54,
                    weight="600", line_height=1.12, letter_spacing=-1,
                    align=align, margin=(0, 0, 16, 0)),
            text("hero_p", f"<p>{lede}</p>", color="rgba(255,255,255,0.92)",
                 size_px=19, align=align, margin=(0, 0, 0, 0), max_width=760),
        ], width=1200, flex_align_items="center" if align == "center" else "flex-start"),
    ])


def split(cid, eyebrow, title, paragraphs, img, flip=False, bg="#FFFFFF",
          padding=(88, 24, 88, 24), link=None, list_items=None, side_note=None):
    att, url = IMG[img]
    copy_children = []
    if eyebrow:
        copy_children.append(heading(f"{cid}_eb", eyebrow, "p", color=INK, size_px=13,
                                     weight="700", line_height=1.4, letter_spacing=1.56,
                                     text_transform="uppercase", margin=(0, 0, 16, 0)))
    copy_children.append(heading(f"{cid}_h2", title, "h2", size_px=44, weight="600",
                                 line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 20, 0)))
    for i, p in enumerate(paragraphs):
        copy_children.append(text(f"{cid}_p{i}", f"<p>{p}</p>", margin=(0, 0, 16, 0)))
    if list_items:
        copy_children.append(text(f"{cid}_ul", "<ul>" + "".join(f"<li>{x}</li>" for x in list_items) + "</ul>",
                                  margin=(0, 0, 16, 0)))
    if link:
        copy_children.append(link_button(f"{cid}_link", link[0], link[1], margin=(12, 0, 0, 0)))

    copy_col = container(f"{cid}_copy", {
        "content_width": "full",
        "width": {"unit": "%", "size": 48, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, copy_children, inner=True)

    img_col = container(f"{cid}_imgcol", {
        "content_width": "full",
        "width": {"unit": "%", "size": 46, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "order": "-1" if flip else "1",
    }, [image(f"{cid}_img", att, url, radius=16)], inner=True)

    row = container(f"{cid}_row", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(72),
        "flex_align_items": "center",
        "flex_wrap": "wrap",
    }, [copy_col, img_col], inner=True)

    return container(cid, {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": bg,
        "padding": px(*padding),
        "padding_tablet": px(padding[0] * 0.8, 32, padding[2] * 0.8, 32),
        "padding_mobile": px(padding[0] * 0.6, 24, padding[2] * 0.6, 24),
        "_element_id": cid,
    }, [inner(f"{cid}_inner", [row])])


def prose_section(cid, title, children, bg="#FFFFFF", padding=(0, 24, 88, 24), anchor=None):
    inner_children = []
    if title:
        inner_children.append(heading(f"{cid}_h2", title, "h2", size_px=30, weight="600",
                                      line_height=1.25, letter_spacing=-0.4, margin=(0, 0, 16, 0)))
    inner_children.extend(children)
    return container(cid, {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": bg,
        "padding": px(*padding),
        "padding_mobile": px(padding[0] * 0.6, 24, padding[2] * 0.6, 24),
        "_element_id": anchor or cid,
    }, [inner(f"{cid}_inner", inner_children, width=760)])


# ------------------------------------------------------------------ pages

PROGRAM_NAV = [
    ("Community Day Services", "community-day-services"),
    ("Community Engagement", "special-olympics"),
    ("Vocational Program", "vocational"),
    ("Residential Living", "residential-living"),
    ("Health & Well Being", "health-well-being"),
]


def program_sidebar(current_slug):
    """Figma 9560:437 — Programs label and a ruled list of program pages.
    The current page is blue. Rows are pages, not on-page anchors."""
    rows = []
    for label, slug in PROGRAM_NAV:
        active = slug == current_slug
        kids = [link_button(
            f"nav_{slug.replace('-', '_')}", label, f"/programs/{slug}/",
            color="#0089DF" if active else INK,
            size_px=15, weight="600",
            margin=(10, 0, 10, 0),
        )]
        rows.append(container(f"navrow_{slug.replace('-', '_')}", {
            "content_width": "full",
            "flex_direction": "column",
            "border_border": "solid",
            "border_width": px(0, 0, 1, 0),
            "border_color": "#C8D4E0",
        }, kids, inner=True))

    return container("pg_side", {
        "content_width": "full",
        "width": size(240, "px"),
        "width_tablet": size(240, "px"),
        "width_mobile": size(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "stretch",
        "_flex_size": "none",
        "sticky": "top",
        "sticky_on": ["desktop", "tablet"],
        "sticky_offset": 120,
    }, [
        heading("pg_side_label", "Programs", "p", color="#0089DF", size_px=13,
                weight="700", line_height=1.6, letter_spacing=1.04,
                text_transform="uppercase", margin=(0, 0, 10, 0)),
        container("pg_side_list", {
            "content_width": "full",
            "flex_direction": "column",
            "border_border": "solid",
            "border_width": px(1, 0, 0, 0),
            "border_color": "#C8D4E0",
        }, rows, inner=True),
    ], inner=True)


def program_page(data, img, slug_prefix, gallery=False):
    name = data["name"]
    blocks = []
    overview = data.get("overview")
    children = []
    if overview:
        children.append(heading("ov_h2", "Overview", "h2", size_px=30, weight="600",
                                line_height=1.25, letter_spacing=-0.4, margin=(0, 0, 16, 0)))
        children.extend(rich_blocks(overview["blocks"], "ov"))
    for s in data.get("sections", []):
        children.append(heading(f"s_{s['id']}_h2", s["title"], "h2", size_px=30,
                                weight="600", line_height=1.25, letter_spacing=-0.4,
                                margin=(48, 0, 16, 0)))
        children.extend(rich_blocks(s["blocks"], s["id"]))
    if gallery:
        children.append(heading("gal_h2", "Photo gallery", "h2", size_px=30, weight="600",
                                line_height=1.25, letter_spacing=-0.4, margin=(48, 0, 16, 0)))
        for i, key in enumerate(["workshop", "kitchen", "garden", "porch"]):
            children.append(image(f"gal_{i}", IMG[key][0], IMG[key][1], radius=12))

    content_col = container("pg_content", {
        "content_width": "full",
        "width": {"unit": "custom", "size": "calc(100% - 296px)", "sizes": []},
        "width_tablet": {"unit": "custom", "size": "calc(100% - 296px)", "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
        "_flex_size": "none",
    }, children, inner=True)

    sidebar = program_sidebar(slug_prefix)

    body = container("pg_body", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_gap": gap(56),
        "flex_wrap": "nowrap",
        "flex_wrap_mobile": "wrap",
        "flex_align_items": "flex-start",
    }, [sidebar, content_col], inner=True)

    return [
        hero(name, data.get("tagline", ""), img=img, height=480, align="left"),
        container("pg_intro", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "padding": px(72, 24, 0, 24),
            "padding_mobile": px(48, 24, 0, 24),
        }, [inner("pg_inner", [body], width=1200)]),
    ]


def page_programs_landing():
    intro = container("prog_intro_sec", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": ALT,
        "padding": px(72, 24, 72, 24),
        "padding_mobile": px(48, 24, 48, 24),
    }, [inner("prog_intro_inner", [
        container("prog_intro_row", {
            "content_width": "full",
            "flex_direction": "row",
            "flex_gap": gap(72),
            "flex_wrap": "wrap",
            "flex_align_items": "center",
        }, [
            container("prog_intro_copy", {
                "content_width": "full",
                "width": {"unit": "%", "size": 46, "sizes": []},
                "width_mobile": {"unit": "%", "size": 100, "sizes": []},
                "flex_direction": "column",
            }, [
                heading("pi_h2", "Building Skills, Connections, and Confidence", "h2",
                        size_px=40, weight="600", line_height=1.2, letter_spacing=-0.8,
                        margin=(0, 0, 20, 0)),
                text("pi_p", "<p>Through personalized support and engaging experiences, each man discovers his strengths, develops everyday skills, builds lasting friendships, and gains confidence to try new things.</p>"),
            ], inner=True),
            container("prog_intro_imgs", {
                "content_width": "full",
                "width": {"unit": "%", "size": 46, "sizes": []},
                "width_mobile": {"unit": "%", "size": 100, "sizes": []},
                "flex_direction": "row",
                "flex_gap": gap(20),
            }, [
                image("pi_img1", IMG["workshop"][0], IMG["workshop"][1], radius=16),
                image("pi_img2", IMG["kitchen"][0], IMG["kitchen"][1], radius=16),
            ], inner=True),
        ], inner=True),
    ])])

    cards = [
        ("cds", "Community Day Services",
         "Our Community Day Services build skills, friendships, and meaningful community connections.",
         "/programs/community-day-services"),
        ("engagement", "Community Engagement",
         "Explore interests and connect with others through activities, outings and Special Olympics.",
         "/programs/special-olympics"),
        ("residential", "Residential Living",
         "Our 13 CILA homes offer welcoming living across our 60-acre campus and the city of Momence",
         "/programs/residential-living"),
        ("health", "Health & Well Being",
         "Personalized support helps each man stay active, feel his best, and enjoy a fulfilling life.",
         "/programs/health-well-being"),
    ]
    tiles = []
    for i, (key, title, desc, path) in enumerate(cards):
        icon = ICONS[key]
        tiles.append(container(f"pl_card{i}", {
            "content_width": "full",
            "width": {"unit": "%", "size": 24.9, "sizes": []},
            "width_tablet": {"unit": "%", "size": 49.9, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "padding": px(32, 28, 36, 28),
        }, [
            container(f"pl_icon{i}", {
                "content_width": "full",
                "width": size(48),
                "min_height": size(48),
                "flex_direction": "column",
                "flex_justify_content": "center",
                "flex_align_items": "center",
                "background_background": "classic",
                "background_color": INK,
                "border_radius": px(12),
                "margin": px(0, 0, 16, 0),
            }, [image(f"pl_iconimg{i}", icon[0], icon[1], radius=0)], inner=True),
            heading(f"pl_title{i}", title, "h3", color=INK, size_px=22,
                    weight="700", line_height=1.2, letter_spacing=0, margin=(0, 0, 10, 0)),
            text(f"pl_desc{i}", f"<p>{desc}</p>", color="#4B4D50",
                 line_height=1.5, margin=(0, 0, 20, 0), flex_grow=True),
            link_button(f"pl_link{i}", "Learn more+", path, color=INK),
        ], inner=True))

    grid = container("pl_grid", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(1),
        "flex_wrap": "wrap",
        "background_background": "classic",
        "background_color": "#E8EDF2",
        "border_radius": px(16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
    }, tiles, inner=True)

    sec = container("prog_cards_sec", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": SOFT,
        "padding": px(72, 24, 96, 24),
        "padding_mobile": px(48, 24, 64, 24),
    }, [inner("prog_cards_inner", [grid])])

    return [
        hero("Programs & Services",
             "From welcoming homes and engaging day programs to personalized health and wellness support, we help each man build skills, explore interests, form friendships, and enjoy a meaningful, fulfilling life.",
             height=560, align="left"),
        intro, sec,
    ]


def page_events():
    data = DATA["site"]
    cards = [
        ("01.", "Donate",
         "Donate to help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home. Every gift makes a difference.",
         "/support-gsm#ways-to-give"),
        ("02.", "Volunteer",
         "Volunteer your time and talents to support GSM Foundation’s fundraisers to enrich the lives of the men.",
         "/support-gsm#events"),
        ("03.", "Make A Lasting Impact",
         "Formed in 2007, the Shepherds Endowment Fund provides income to support Good Shepherd Manor’s mission in perpetuity.",
         "/shepherd-endowment-society"),
    ]
    events = [
        ("fall-festival", "Fall Festival", "September 2027",
         "Join us on the second Saturday of September for GSM’s beloved 36th Annual Fall Festival! Enjoy food, bingo, entertainment, and family fun for everyone while supporting the mission of the Manor."),
        ("golf", "Golf Invitational", "June 28, 2027",
         "Tee off for a great cause at GSM’s 31st Annual Golf Invitational! Enjoy a day of golf, food, and camaraderie while raising funds for compassionate care and meaningful opportunities for the men of Good Shepherd Manor. Join us on the course to do good."),
        ("brunch-auction", "Brunch Auction", "April 18, 2027",
         "Join GSM’s 52nd Brunch Auction for live & silent auctions, & Meet A Manor Need - which funds a specific need for the men. Past MAMN’s include the Digital Den, CHAIR the Love and a paratransit vehicle. This event makes such an impact on GSM’s mission!"),
        ("family", "Community & Family Events", "All Year",
         "Building community at GSM! Enjoy free events: the 5th Annual Touch A Truck on October 2, Twelfth Night Bonfire in early January 2027, and summer Community Movie Nights. Our monthly summer Friends & Family cookouts offer extra ways to connect."),
    ]
    sections = []
    for i, (slug, title, when, body) in enumerate(events):
        sections.append(container(f"ev_{slug}", {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF" if i % 2 == 0 else ALT,
            "padding": px(56, 24, 56, 24),
            "_element_id": slug,
        }, [inner(f"ev_{slug}_inner", [
            heading(f"ev_{slug}_h2", title, "h2", size_px=32, weight="600",
                    line_height=1.25, letter_spacing=-0.4, margin=(0, 0, 6, 0)),
            heading(f"ev_{slug}_date", when, "p", color=LINK, size_px=15, weight="700",
                    line_height=1.4, letter_spacing=0.4, margin=(0, 0, 14, 0)),
            text(f"ev_{slug}_p", f"<p>{body}</p>", margin=(0, 0, 0, 0)),
        ], width=800)]).replace if False else container(f"ev_{slug}", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": "#FFFFFF" if i % 2 == 0 else ALT,
            "padding": px(56, 24, 56, 24),
            "_element_id": slug,
        }, [inner(f"ev_{slug}_inner", [
            heading(f"ev_{slug}_h2", title, "h2", size_px=32, weight="600",
                    line_height=1.25, letter_spacing=-0.4, margin=(0, 0, 6, 0)),
            heading(f"ev_{slug}_date", when, "p", color=LINK, size_px=15, weight="700",
                    line_height=1.4, letter_spacing=0.4, margin=(0, 0, 14, 0)),
            text(f"ev_{slug}_p", f"<p>{body}</p>", margin=(0, 0, 0, 0)),
        ], width=800)]))

    return [
        hero("Events",
             "GSM’s events raise funds to bridge the gap between state funding and the care the men need. They bring people together, introduce our mission to new supporters, and build lasting relationships that sustain the Foundation’s work and enrich daily life.",
             height=520),
        cards_strip("ev", cards),
    ] + sections


def page_news():
    stats = DATA["site"]["impactStats"]
    items = DATA["site"]["newsItems"]
    stat_cols = []
    for i, s in enumerate(stats):
        st = {
            "content_width": "full",
            "width": {"unit": "%", "size": 23.75, "sizes": []},
            "width_mobile": {"unit": "%", "size": 46, "sizes": []},
            "flex_direction": "column",
            "padding": px(0, 24, 20, 0),
        }
        if i < len(stats) - 1:
            st.update({"border_border": "solid", "border_width": px(0, 1, 0, 0),
                       "border_color": "#C8D4E0"})
        stat_cols.append(container(f"nw_stat{i}", st, [
            heading(f"nw_val{i}", s["value"], "p", color=INK, size_px=48, weight="700",
                    line_height=1.2, letter_spacing=-0.5, margin=(0, 0, 8, 0)),
            heading(f"nw_lbl{i}", s["label"], "p", color="#4A6278", size_px=15,
                    weight="500", line_height=1.5, letter_spacing=0, margin=(0, 0, 0, 0)),
        ], inner=True))

    cards = []
    for i, item in enumerate(items):
        cards.append(container(f"nw_card{i}", {
            "content_width": "full",
            "width": {"unit": "%", "size": 23.2, "sizes": []},
            "width_tablet": {"unit": "%", "size": 47, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_radius": px(8),
            "padding": px(28, 24, 28, 24),
        }, [
            heading(f"nw_t{i}", item["title"], "h3", color=INK, size_px=18, weight="700",
                    line_height=1.3, letter_spacing=0, margin=(0, 0, 10, 0)),
            text(f"nw_e{i}", f"<p>{item['excerpt']}</p>", margin=(0, 0, 16, 0), flex_grow=True),
            link_button(f"nw_l{i}", "Read More", item["path"], color=INK, size_px=14),
        ], inner=True))

    return [
        hero("News & Updates",
             "Stay connected with the men and life at GSM. Find latest updates, event news, and stories from our community, along with The Messenger, our twice-yearly newsletter celebrating the people of the Manor.",
             height=480, align="left"),
        container("nw_impact", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "padding": px(80, 24, 48, 24),
        }, [inner("nw_impact_inner", [
            heading("nw_h2", "Our Impact", "p", color=INK, size_px=13, weight="700",
                    line_height=1.4, letter_spacing=1.56, text_transform="uppercase",
                    margin=(0, 0, 12, 0)),
            heading("nw_title", "Helping men with disabilities thrive", "h2", size_px=40,
                    weight="600", line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 16, 0)),
            text("nw_lede", "<p>With compassionate care, welcoming homes, and meaningful opportunities, GSM helps each man build independence, form friendships, explore interests, and enjoy a life of dignity, purpose, and belonging.</p>",
                 margin=(0, 0, 32, 0), max_width=760),
            container("nw_stats", {
                "content_width": "full",
                "flex_direction": "row",
                "flex_gap": gap(20),
                "flex_wrap": "wrap",
            }, stat_cols, inner=True),
        ])]),
        container("nw_cta", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": INK,
            "padding": px(64, 24, 64, 24),
            "width": {"unit": "%", "size": 92, "sizes": []},
            "border_radius": px(16),
            "_element_id": "donate",
        }, [inner("nw_cta_inner", [
            heading("nw_cta_h2", "Help Make Home Happen", "h2", color="#FFFFFF",
                    size_px=44, weight="600", line_height=1.15, letter_spacing=-0.8,
                    align="center", margin=(0, 0, 16, 0)),
            text("nw_cta_p", "<p>Give now to help men with disabilities have compassionate care, meaningful lives, and a home at GSM.</p>",
                 color="rgba(255,255,255,0.86)", align="center", margin=(0, 0, 28, 0), max_width=640),
            cta_button("nw_cta_btn", "Donate Now", "/support-gsm#ways-to-give",
                       bg="#FFFFFF", color=INK),
        ], width=900, flex_align_items="center")]),
        container("nw_cards_sec", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": SOFT,
            "padding": px(88, 24, 88, 24),
        }, [inner("nw_cards_inner", [
            heading("nw_cards_h2", "What’s Happening at GSM", "h2", size_px=40,
                    weight="600", line_height=1.15, letter_spacing=-0.8, align="center",
                    margin=(0, 0, 16, 0)),
            text("nw_cards_p", "<p>See how the men of GSM are learning, connecting, and thriving. Explore the new stories, events, and everyday moments your support helps make possible.</p>",
                 align="center", margin=(0, 0, 40, 0), max_width=760),
            container("nw_grid", {
                "content_width": "full",
                "flex_direction": "row",
                "flex_gap": gap(24),
                "flex_wrap": "wrap",
            }, cards, inner=True),
        ])]),
    ]


def page_newsletters():
    issues = ["The Messenger Fall 2026", "The Messenger Spring 2026", "The Messenger Fall 2025"]
    desc = ("Explore stories, photos, and updates celebrating the men of GSM and the community "
            "that helps them flourish.")
    archive = []
    for i, title in enumerate(issues):
        archive.append(container(f"nl_issue{i}", {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_radius": px(10),
            "padding": px(28, 28, 28, 28),
            "margin": px(0, 0, 16, 0),
        }, [
            heading(f"nl_t{i}", title, "h3", color=INK, size_px=20, weight="700",
                    line_height=1.3, letter_spacing=0, margin=(0, 0, 10, 0)),
            text(f"nl_d{i}", f"<p>{desc}</p>", margin=(0, 0, 16, 0)),
            link_button(f"nl_l{i}", "Download PDF", "#", color=LINK, size_px=15),
        ], inner=True))

    return [
        hero("Newsletters & Family Resources",
             "Discover stories, photos and updates from life at GSM in The Messenger, our twice-yearly newsletter.",
             height=480, align="left"),
        container("nl_body", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "padding": px(80, 24, 88, 24),
        }, [inner("nl_inner", [
            heading("nl_h2", "Get The Messenger straight to your inbox", "h2", size_px=36,
                    weight="600", line_height=1.2, letter_spacing=-0.6, margin=(0, 0, 16, 0)),
            text("nl_p", "<p>Discover stories, photos and updates from life at GSM in The Messenger, our twice-yearly newsletter.</p>",
                 margin=(0, 0, 24, 0)),
            widget("nl_form", "shortcode", {"shortcode": '[sureforms id="2202" show_title="false"]'}),
            heading("nl_arch_h2", "Recent Issues", "h2", size_px=30, weight="600",
                    line_height=1.25, letter_spacing=-0.4, margin=(48, 0, 20, 0)),
            container("nl_arch", {
                "content_width": "full",
                "flex_direction": "column",
            }, archive, inner=True),
        ], width=900)]),
    ]


def page_careers():
    c = DATA["careers"]
    cards = [(col["num"], col["title"], col["description"], col["path"])
             for col in c["careersIntroColumns"]]

    jobs = []
    for i, job in enumerate(c["careersJobs"]):
        jobs.append(container(f"cr_job{i}", {
            "content_width": "full",
            "flex_direction": "column",
            "border_border": "solid",
            "border_width": px(1, 0, 0, 0),
            "border_color": "#E8EDF2",
            "padding": px(24, 0, 8, 0),
        }, [
            heading(f"cr_jt{i}", job["title"], "h3", color=INK, size_px=20, weight="700",
                    line_height=1.3, letter_spacing=0, margin=(0, 0, 8, 0)),
            text(f"cr_jb{i}", f"<p>{job['body']}</p>", margin=(0, 0, 12, 0)),
            link_button(f"cr_jl{i}", job["applyLabel"], job["applyTo"], size_px=15),
        ], inner=True))

    return [
        hero("Careers",
             "Build a career with purpose at Good Shepherd Manor. Join a caring team that supports men with intellectual and developmental disabilities in living full, meaningful lives.",
             height=520, align="left"),
        container("cr_intro", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": ALT,
            "padding": px(80, 24, 72, 24),
        }, [inner("cr_intro_inner", [
            heading("cr_eb", c["careersIntro"]["eyebrow"], "p", color=INK, size_px=13,
                    weight="700", line_height=1.4, letter_spacing=1.56,
                    text_transform="uppercase", margin=(0, 0, 16, 0)),
            heading("cr_h1", c["careersIntro"]["title"], "h2", size_px=44, weight="600",
                    line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 20, 0)),
            text("cr_p0", f"<p>{c['careersIntro']['paragraphs'][0]}</p>", margin=(0, 0, 16, 0)),
            text("cr_p1", f"<p>{c['careersIntro']['paragraphs'][1]}</p>", margin=(0, 0, 0, 0)),
        ], width=900)]),
        cards_strip("cr", cards, bg=SOFT, overlap=False),
        split("cr_benefits", c["careersBenefits"]["eyebrow"], c["careersBenefits"]["title"],
              c["careersBenefits"]["paragraphs"], "vocational", bg="#FFFFFF",
              list_items=c["careersBenefits"]["listItems"]),
        split("cr_culture", c["careersCulture"]["eyebrow"], c["careersCulture"]["title"],
              c["careersCulture"]["paragraphs"], "community", flip=True, bg=ALT),
        container("cr_jobs", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "padding": px(88, 24, 88, 24),
        }, [inner("cr_jobs_inner", [
            heading("cr_jobs_eb", c["careersOpenings"]["eyebrow"], "p", color=INK, size_px=13,
                    weight="700", line_height=1.4, letter_spacing=1.56,
                    text_transform="uppercase", margin=(0, 0, 16, 0)),
            heading("cr_jobs_h2", c["careersOpenings"]["title"], "h2", size_px=44,
                    weight="600", line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 16, 0)),
            text("cr_jobs_lede", f"<p>{c['careersOpenings']['lede']}</p>", margin=(0, 0, 24, 0)),
            container("cr_jobs_list", {"content_width": "full", "flex_direction": "column"},
                      jobs, inner=True),
            text("cr_jobs_apply", "<p>Apply online at Indeed.com, or call or text 815-592-7423.</p>",
                 margin=(24, 0, 0, 0)),
        ], width=900)]),
        split("cr_apply", c["careersApply"]["eyebrow"], c["careersApply"]["title"],
              c["careersApply"]["paragraphs"], "porch", bg=ALT,
              link=(c["careersApply"]["linkLabel"], c["careersApply"]["linkTo"])),
    ]


def page_endowment():
    e = DATA["endowment"]
    cards = [
        ("01.", "Donate",
         "A gift to the Shepherd Endowment Society is invested, not spent, and supports the Manor in perpetuity.",
         "/support-gsm#ways-to-give"),
        ("02.", "Membership",
         "Members make a current gift and a deferred commitment, joining a community of supporters.",
         "#membership"),
        ("03.", "Legacy",
         "Remember Good Shepherd Manor in your will, trust, or through another planned gift.",
         "#gift-options"),
    ]
    table_rows = "".join(
        f"<tr><th scope='row'>{r['level']}</th><td>{r['current']}</td><td>{r['deferred']}</td></tr>"
        for r in e["membershipLevels"])
    table = ("<table><thead><tr><th>Member Levels</th><th>Current Gift</th>"
             f"<th>Deferred Gift</th></tr></thead><tbody>{table_rows}</tbody></table>")

    gift_lists = (
        "<h3>Current Gifts</h3><ul>" + "".join(f"<li>{x}</li>" for x in e["currentGifts"]) +
        "</ul><h3>Deferred Gifts</h3><ul>" +
        "".join(f"<li>{x}</li>" for x in e["deferredGifts"]) + "</ul>")

    return [
        hero("Shepherd Endowment Society", "Stewardship that outlives a gift", height=480),
        cards_strip("en", cards),
        split("en_overview", "Shepherd Endowment Society", "Income for the Manor, in perpetuity",
              e["endowmentIntro"] + [e["endowmentDisbursement"]], "chapel_hands", bg="#FFFFFF"),
        prose_section("en_quote", None, [
            text("en_quote_p", f"<blockquote><p>“{e['endowmentQuote']['text']}”</p>"
                               f"<cite>{e['endowmentQuote']['cite']}</cite></blockquote>",
                 margin=(0, 0, 0, 0)),
        ], bg=ALT, padding=(64, 24, 64, 24)),
        prose_section("en_gift", "So How Can You Ensure More Tomorrows?",
                      [text("en_gift_p", "".join(f"<p>{p}</p>" for p in e["giftOptionsIntro"]), margin=(0, 0, 16, 0)),
                       text("en_gift_lists", gift_lists, margin=(0, 0, 0, 0))],
                      bg="#FFFFFF", anchor="gift-options"),
        prose_section("en_member", "Membership", [
            text("en_m_p", f"<p>{e['membershipIntro']}</p>", margin=(0, 0, 20, 0)),
            text("en_table", table, margin=(0, 0, 20, 0)),
            text("en_outro", f"<p>{e['membershipOutro']}</p>", margin=(0, 0, 16, 0)),
            link_button("en_ask", "Ask about joining →", "/contact", margin=(0, 0, 0, 0)),
        ], bg=ALT, anchor="membership"),
    ]


def page_support():
    cards = [
        ("01.", "Donate",
         "Donate to help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home. Every gift makes a difference.",
         "#ways-to-give"),
        ("02.", "Volunteer",
         "Volunteer your time and talents to support GSM Foundation’s fundraisers to enrich the lives of the men.",
         "/events"),
        ("03.", "Make A Lasting Impact",
         "Formed in 2007, the Shepherds Endowment Fund provides income to support Good Shepherd Manor’s mission in perpetuity.",
         "/shepherd-endowment-society"),
    ]
    return [
        hero("Support GSM Foundation",
             "Founded in 1981, GSM’s Foundation has provided continual support for the programs, services and operating costs of the Manor, allowing us to go above and beyond what the state mandates and provides.",
             height=520, align="left"),
        cards_strip("sg", cards),
        split("foundation", "GSM Foundation", "Supporting the Manor for over 45 years", [
            "Then Board President William J. McAllister called the Foundation an important step toward financial stability and excellent care. Its goals included facility improvements, unbudgeted needs, and a permanent endowment that would take shape in later years.",
            "Today, the Foundation helps bridge a funding gap of more than $20,000 per man each year beyond state support, sustaining the daily care, programs, and services that enrich life at Good Shepherd Manor.",
        ], "sing", bg="#FFFFFF"),
        split("ways-to-give", "Ways to Give", "Every gift stays on campus", [
            "Every gift, big or small, helps support the men of GSM. Give through our three signature events—the Brunch Auction, Golf Invitational, and Fall Festival—or our annual Christmas Appeal. You can also make a general gift to support the Foundation.",
            "Other opportunities to give are through the Family Donor Program, honoring someone special with a tribute, remember a loved one with a memorial gift, or supporting the Manor’s future through the Shepherds Endowment Society.",
        ], "golf", flip=True, bg=ALT,
            link=("Ways to Give →", "https://secure.qgiv.com/for/wdof/")),
        split("endowment", "Shepherds Endowment Society", "Your Legacy. Their Future.", [
            "Established in 2007 within the Good Shepherd Manor Foundation, the Shepherds Endowment Society generates income for GSM in perpetuity. Endowment gifts are invested rather than spent, generating annual income that extends beyond the life of the donor.",
            "Investment income provides a stable source of funding for GSM’s future operating expenses. Your legacy helps sustain compassionate care, meaningful opportunities, and a welcoming home for generations.",
        ], "chapel", bg="#FFFFFF",
            link=("Explore the Shepherds Endowment Society →", "/shepherd-endowment-society")),
        split("events", "Events",
              "Fall Festival, Golf Invitational, Brunch Auction, community &amp; family events", [
                  "GSM’s events raise needed funds for the Foundation while bringing people together. They introduce our mission, deepen community connections, and build lasting relationships that support meaningful lives for the men who call the Manor home.",
              ], "festival", flip=True, bg=ALT,
              list_items=["Fall Festival", "Golf Invitational", "Brunch Auction", "Community & Family Events"],
              link=("See all events →", "/events")),
    ]


def page_about():
    history = [
        ("1970's", "The Manor opened in 1971, welcoming 122 men. It was a decade of welcome & new beginnings."),
        ("1980's", "Securing the Manor's future, dawn of the Day Program while activities & Special Olympics grow."),
        ("1990's", "The path to Independence, new group homes and community fundraisers"),
        ("2000 and beyond", "Progress, challenges and change shape the era as healthcare takes center stage in the Manor's story."),
    ]
    hist_cards = []
    for i, (yr, txt) in enumerate(history):
        hist_cards.append(container(f"ab_hist{i}", {
            "content_width": "full",
            "width": {"unit": "%", "size": 23, "sizes": []},
            "width_tablet": {"unit": "%", "size": 47, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_radius": px(12),
            "padding": px(28, 24, 28, 24),
        }, [
            heading(f"ab_yr{i}", yr, "p", color=LINK, size_px=17, weight="700",
                    line_height=1.3, letter_spacing=0, margin=(0, 0, 10, 0)),
            text(f"ab_ht{i}", f"<p>{txt}</p>", size_px=15, margin=(0, 0, 0, 0)),
        ], inner=True))

    return [
        hero("About Us",
             "Since 1971, Good Shepherd Manor has offered men with disabilities compassionate care, purpose, and a place to call home.",
             height=560, align="left"),
        split("about_overview", "About Us",
              "A community of care, growth, and dignity for over 55 years.", [
                  "Rooted in compassion, we help men with disabilities lead meaningful lives through personalized support, lasting friendships and opportunities to grow.",
                  "Our welcoming homes and dedicated staff create a family atmosphere where each man receives personalized support, builds daily living skills, and enjoys meaningful connections on campus and in the surrounding community.",
              ], "porch", bg=ALT),
        cards_strip("ab", [
            ("01.", "Programs & Services",
             "Personalized programs and compassionate services help each man learn, connect, and thrive.", "/programs"),
            ("02.", "Get Involved",
             "Discover ways to support the Manor through giving, events and sharing your time and talent.", "/support-gsm"),
            ("03.", "News You Can Use",
             "Get connected with Manor news, newsletters, useful updates and resources for GSM families", "/news"),
        ], bg=SOFT, overlap=False),
        split("mission", "Who We Are", "The Heart of Our Mission", [
            "Our Mission is to serve men with intellectual and developmental disabilities by providing high quality & compassionate care. Our vision is to meet individual needs, build individual abilities, and make each day meaningful and rewarding.",
            "Our Values are guided by our legacy of compassion, honoring each man's dignity and envisioning a community where all feel valued, supported and truly at home.",
        ], "chapel", bg="#FFFFFF"),
        container("ab_history", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": ALT,
            "padding": px(88, 24, 88, 24),
            "_element_id": "history",
        }, [inner("ab_hist_inner", [
            heading("ab_hist_eb", "Our History", "p", color=INK, size_px=13, weight="700",
                    line_height=1.4, letter_spacing=1.56, text_transform="uppercase",
                    margin=(0, 0, 16, 0)),
            heading("ab_hist_h2", "A Timeline of Care", "h2", size_px=44, weight="600",
                    line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 32, 0)),
            container("ab_hist_row", {
                "content_width": "full",
                "flex_direction": "row",
                "flex_gap": gap(20),
                "flex_wrap": "wrap",
            }, hist_cards, inner=True),
        ])]),
        split("affiliations", "Memberships", "Member Organizations or Affiliations", [
            "GSM is a member of a variety of local professional and civic organizations, as well as statewide organizations such as the Kankakee & Momence Chamber of Commerce, Intersect For Ability, United Way of Kankakee County, Special Olympics & ARC of IL.",
        ], "community", bg="#FFFFFF", link=("ARC of Illinois", "#")),
        split("accessibility", "Accessibility Statement", "Website Accessibility Statement", [
            "Good Shepherd Manor is committed to treating every person with dignity and respect. In keeping with our mission of providing high-quality, compassionate care to men with intellectual and developmental disabilities, we strive to make our website accessible and welcoming to people of all abilities. Our goal is to continually improve the accessibility and usability of our website so everyone can learn about our programs, access resources, and connect with our mission.",
            "If you experience difficulty accessing any part of our website or need information in an alternative format, please contact us at 815-472-3700 or info@goodshepherdmanor.org. Please include the page address and a brief description of the difficulty so we can better assist you.",
        ], "garden", flip=True, bg=ALT, link=("Contact Us for More Information", "/contact")),
    ]


BUILDERS = {
    317: ("Programs & Services", page_programs_landing),
    316: ("About Us", page_about),
    2092: ("Support GSM Foundation", page_support),
    2093: ("Shepherd Endowment Society", page_endowment),
    2094: ("Events", page_events),
    318: ("News & Updates", page_news),
    2095: ("Newsletters & Family Resources", page_newsletters),
    2096: ("Careers", page_careers),
    2088: ("Community Day Services",
           lambda: program_page(DATA["programs"]["communityDay"], "day", "community-day-services")),
    2089: ("Vocational Program",
           lambda: program_page(DATA["programs"]["vocational"], "vocational", "vocational")),
    2127: ("Community Engagement",
           lambda: program_page(DATA["programs"]["communityEngagement"], "community", "special-olympics")),
    2090: ("Residential Living",
           lambda: program_page(DATA["programs"]["residential"], "porch", "residential-living")),
    2091: ("Health & Well Being",
           lambda: program_page(DATA["health"]["healthData"], "infirmary", "health-well-being")),
}


def build(pid):
    name, fn = BUILDERS[pid]
    data = fn()
    # give every top-level section a stable id based on its element id
    out = f"/tmp/page_{pid}.json"
    with open(out, "w") as f:
        json.dump(data, f)
    return out




def srfm(form_id, show_title="false"):
    return widget(f"srfm_{form_id}", "sureforms_form", {
        "srfm_form_block": form_id,
        "srfm_show_form_title": show_title,
    })


def page_contact():
    bar_cards = [
        ("Phone", "Tel: (815) 472-3700", "/contact/#visit"),
        ("Campus", "P.O. Box 260, 4129 N. State Route 1-17, Momence, IL 60954", "/contact/#visit"),
        ("Need Assistance?", "Our Team Is Here to Help", "/contact/#visit"),
    ]
    cols = []
    for i, (label, value, _url) in enumerate(bar_cards):
        st = {
            "content_width": "full",
            "width": {"unit": "%", "size": 33.33, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
            "padding": px(28, 32, 28, 32),
        }
        if i < 2:
            st.update({"border_border": "solid", "border_width": px(0, 1, 0, 0),
                       "border_color": "#E8EDF2"})
        cols.append(container(f"cb_card{i}", st, [
            heading(f"cb_l{i}", label, "p", color=INK, size_px=13, weight="700",
                    line_height=1.4, letter_spacing=1.04, text_transform="uppercase",
                    margin=(0, 0, 8, 0)),
            heading(f"cb_v{i}", value, "p", color=BODY, size_px=16, weight="400",
                    line_height=1.5, letter_spacing=0, margin=(0, 0, 0, 0)),
        ], inner=True))

    bar = container("contact_bar", {
        "content_width": "boxed",
        "boxed_width": size(1200),
        "flex_direction": "row",
        "flex_gap": gap(0),
        "flex_wrap": "wrap",
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "border_radius": px(16),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 32,
                                  "spread": 0, "color": "rgba(0,42,78,0.12)"},
        "margin": px(-56, 0, 0, 0),
        "z_index": 2,
    }, cols, inner=True)

    directory = container("ct_dir", {
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(40),
        "flex_wrap": "wrap",
        "margin": px(32, 0, 0, 0),
    }, [
        container("ct_main", {
            "content_width": "full",
            "width": {"unit": "%", "size": 46, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            heading("ct_main_h", "Main Office", "h3", color=INK, size_px=18, weight="700",
                    line_height=1.3, letter_spacing=0, margin=(0, 0, 8, 0)),
            text("ct_main_p", "<p>(815) 472-3700<br/>4129 N. State Route 1-17, Momence, IL 60954<br/>P.O. Box 260, Momence, IL 60954</p>",
                 margin=(0, 0, 0, 0)),
        ], inner=True),
        container("ct_careers", {
            "content_width": "full",
            "width": {"unit": "%", "size": 46, "sizes": []},
            "width_mobile": {"unit": "%", "size": 100, "sizes": []},
            "flex_direction": "column",
        }, [
            heading("ct_car_h", "Careers", "h3", color=INK, size_px=18, weight="700",
                    line_height=1.3, letter_spacing=0, margin=(0, 0, 8, 0)),
            link_button("ct_car_l", "View openings →", "/careers", margin=(0, 0, 0, 0)),
        ], inner=True),
    ], inner=True)

    follow = container("ct_follow", {
        "content_width": "full",
        "flex_direction": "column",
        "margin": px(28, 0, 0, 0),
    }, [
        heading("ct_follow_h", "Follow us on:", "h3", color=INK, size_px=18, weight="700",
                line_height=1.3, letter_spacing=0, margin=(0, 0, 8, 0)),
        link_button("ct_fb", "Facebook", "https://www.facebook.com/goodshepherdmanormomence/",
                    margin=(0, 0, 0, 0)),
    ], inner=True)

    touch = container("ct_touch", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": ALT,
        "padding": px(88, 24, 88, 24),
        "_element_id": "visit",
    }, [inner("ct_touch_inner", [
        container("ct_touch_row", {
            "content_width": "full",
            "flex_direction": "row",
            "flex_gap": gap(64),
            "flex_wrap": "wrap",
            "flex_align_items": "flex-start",
        }, [
            container("ct_touch_copy", {
                "content_width": "full",
                "width": {"unit": "%", "size": 48, "sizes": []},
                "width_mobile": {"unit": "%", "size": 100, "sizes": []},
                "flex_direction": "column",
            }, [
                heading("ct_eb", "Get in touch", "p", color=INK, size_px=13, weight="700",
                        line_height=1.4, letter_spacing=1.56, text_transform="uppercase",
                        margin=(0, 0, 16, 0)),
                heading("ct_h2", "How can we help you?", "h2", size_px=44, weight="600",
                        line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 20, 0)),
                text("ct_p", "<p>Whether you’re exploring care for a loved one, sharing feedback or recognizing someone who made a difference, we’re here to listen and help you take the next step.</p>",
                     margin=(0, 0, 0, 0)),
                directory, follow,
            ], inner=True),
            container("ct_form_col", {
                "content_width": "full",
                "width": {"unit": "%", "size": 46, "sizes": []},
                "width_mobile": {"unit": "%", "size": 100, "sizes": []},
                "flex_direction": "column",
            }, [srfm(2056)], inner=True),
        ], inner=True),
    ])])

    map_sec = container("ct_map", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": INK,
        "padding": px(72, 24, 64, 24),
    }, [inner("ct_map_inner", [
        heading("ct_map_eb", "Our Location", "p", color="rgba(255,255,255,0.8)", size_px=13,
                weight="700", line_height=1.4, letter_spacing=1.56, text_transform="uppercase",
                margin=(0, 0, 12, 0)),
        heading("ct_map_h2", "Rooted in Momence. Connected by Care.", "h2", color="#FFFFFF",
                size_px=40, weight="600", line_height=1.2, letter_spacing=-0.6, margin=(0, 0, 32, 0)),
        text("ct_map_addr", "<p>4129 N. State Route 1-17, Momence, IL 60954</p>",
             color="rgba(255,255,255,0.8)", align="center", margin=(0, 0, 24, 0)),
        cta_button("ct_map_btn", "Open in Google Maps →",
                   "https://maps.google.com/?q=4129+N.+State+Route+1-17,+Momence,+IL+60954",
                   bg="#FFFFFF", color=INK),
    ])])

    thank = container("ct_thank", {
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "padding": px(88, 24, 88, 24),
        "_element_id": "thank",
    }, [inner("ct_thank_inner", [
        container("ct_thank_row", {
            "content_width": "full",
            "flex_direction": "row",
            "flex_gap": gap(64),
            "flex_wrap": "wrap",
            "flex_align_items": "flex-start",
        }, [
            container("ct_thank_copy", {
                "content_width": "full",
                "width": {"unit": "%", "size": 48, "sizes": []},
                "width_mobile": {"unit": "%", "size": 100, "sizes": []},
                "flex_direction": "column",
            }, [
                heading("ct_thank_eb", "Thank a Staff Member", "p", color=INK, size_px=13,
                        weight="700", line_height=1.4, letter_spacing=1.56,
                        text_transform="uppercase", margin=(0, 0, 16, 0)),
                heading("ct_thank_h2", "Make Their Day", "h2", size_px=44, weight="600",
                        line_height=1.15, letter_spacing=-0.8, margin=(0, 0, 20, 0)),
                text("ct_thank_p", "<p>Has a GSM staff member made a difference? Share your appreciation and let them know how much their kindness and dedication mean to you.</p>",
                     margin=(0, 0, 0, 0)),
            ], inner=True),
            container("ct_thank_form", {
                "content_width": "full",
                "width": {"unit": "%", "size": 46, "sizes": []},
                "width_mobile": {"unit": "%", "size": 100, "sizes": []},
                "flex_direction": "column",
            }, [srfm(2370)], inner=True),
        ], inner=True),
    ])])

    return [
        hero("Contact Us",
             "Have a question about Good Shepherd Manor, our services or ways to get involved? Connect with our team to learn more, thank a staff member or find the information you need. We’d love to hear from you!",
             height=480, align="left"),
        container("ct_bar_band", {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "background_background": "classic",
            "background_color": ALT,
            "padding": px(0, 24, 0, 24),
        }, [bar]),
        touch, map_sec, thank,
    ]


BUILDERS[319] = ("Contact Us", page_contact)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    ids = list(BUILDERS) if target == "all" else [int(target)]
    for pid in ids:
        print(build(pid), BUILDERS[pid][0])
