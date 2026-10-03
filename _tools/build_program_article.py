#!/usr/bin/env python3
"""Rebuild the article area on the five program pages to the wire's
ArticleDetailPage: a 240px sidebar + 640px richtext column, with the sidebar
list (dividers, sticky), nested section sub-links, section separators and a
gallery.

Run:  python3 _tools/build_program_article.py
"""
import json
import os
import subprocess
import tempfile

from el import (NAVY, BLUE, BODY, SLATE, PALE, WHITE, RULE, PLACE, PLACE_SOFT,
                LOREM, LOREM_SHORT, LOREM_LONG, LOREM_EXTRA, dims, gap,
                typography, container, widget, heading, para, text_link)

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PROGRAMS = [
    ("Community Day Services", "/programs/community-day-services/"),
    ("Vocational Program", "/programs/vocational/"),
    ("Special Olympics", "/programs/special-olympics/"),
    ("Residential Living", "/programs/residential-living/"),
    ("Health & Well Being", "/programs/health-well-being/"),
]

# block spec: ('p'|'h3'|'ul'|'ol'|'quote'|'callout'|'figure'|'link', ...)
OVERVIEW = [
    ("p", LOREM_LONG), ("p", LOREM),
    ("h3", "Care on campus"), ("p", LOREM_LONG),
    ("ul", [LOREM_SHORT, LOREM, LOREM_EXTRA]),
]

PAGE_DATA = {
    2088: {"sections": [("digital-den", "Digital Den", [
        ("p", LOREM_LONG), ("quote", LOREM_LONG, "Placeholder quote"),
        ("h3", "What the space is for"), ("p", LOREM),
        ("p", LOREM_LONG), ("callout", "Note", LOREM)])],
        "sublinks": [("Digital Den", "digital-den")]},
    2091: {"sections": [
        ("nursing", "Nursing Services", [("p", LOREM_LONG), ("quote", LOREM_LONG, "Placeholder quote"), ("p", LOREM)]),
        ("clinic", "On-site Clinic", [("p", LOREM_LONG), ("h3", "What a visit looks like"), ("p", LOREM)]),
        ("pharmacy", "Pharmacy Services", [("p", LOREM_LONG), ("figure", "Placeholder photo — on-site pharmacy and medication support.")]),
        ("supports", "Community Supports", [("p", LOREM_LONG), ("h3", "In the community"), ("p", LOREM), ("h3", "With families"), ("p", LOREM_LONG)]),
        ("transportation", "Transportation Assistance", [("p", LOREM_LONG), ("callout", "Appointments", LOREM), ("link", "/contact", "Ask about transportation")]),
    ],
        "sublinks": [("Nursing Services", "nursing"), ("On-site Clinic", "clinic"),
                     ("Pharmacy Services", "pharmacy"), ("Community Supports", "supports"),
                     ("Transportation Assistance", "transportation")]},
    2089: {"sections": [], "sublinks": []},
    2127: {"sections": [], "sublinks": []},
    2090: {"sections": [], "sublinks": []},
}


def blocks_html(blocks, nid):
    """Return Elementor elements for a list of block specs."""
    els = []
    for i, b in enumerate(blocks):
        t = b[0]
        if t == "p":
            els.append(para(f"{nid}_p{i}", b[1]))
        elif t == "h3":
            els.append(heading(f"{nid}_h3_{i}", b[1], "h3", NAVY, "left",
                               typography(size=20, weight=600, line_height=1.3)))
        elif t in ("ul", "ol"):
            tag = "ul" if t == "ul" else "ol"
            items = "".join(f"<li>{x}</li>" for x in b[1])
            els.append(widget(f"{nid}_{t}{i}", "text-editor",
                              {"editor": f"<{tag}>{items}</{tag}>", "text_color": BODY}))
        elif t == "quote":
            els.append(widget(f"{nid}_q{i}", "text-editor",
                              {"editor": f"<blockquote><p>{b[1]}</p><cite>{b[2]}</cite></blockquote>",
                               "text_color": BODY}))
        elif t == "callout":
            els.append(container(f"{nid}_co{i}", {
                "content_width": "full", "flex_direction": "column",
                "background_background": "classic", "background_color": PALE,
                "border_radius": dims(8, 8, 8, 8), "padding": dims(16, 20, 16, 20),
                "margin": dims(8, 0, 24, 0),
            }, [
                heading(f"{nid}_co{i}_t", b[1], "p", BLUE, "left",
                        typography(size=14, weight=700, transform="uppercase", letter_spacing=0.5)),
                para(f"{nid}_co{i}_p", b[2]),
            ]))
        elif t == "figure":
            els.append(container(f"{nid}_fig{i}", {
                "content_width": "full", "flex_direction": "column",
                "margin": dims(8, 0, 24, 0),
            }, [
                container(f"{nid}_fig{i}_ph", {
                    "content_width": "full", "min_height": {"unit": "px", "size": 220, "sizes": []},
                    "background_background": "classic", "background_color": PLACE,
                    "border_radius": dims(16, 16, 16, 16),
                }, []),
                heading(f"{nid}_fig{i}_cap", b[1], "p", BODY, "left",
                        typography(size=14, weight=400, line_height=1.5)),
            ]))
        elif t == "link":
            els.append(text_link(f"{nid}_link{i}", b[2], b[1]))
    return els


def rte_section(nid, title, blocks, element_id=None, first=False):
    s = {
        "content_width": "full", "flex_direction": "column",
        "css_classes": "gsm-rte",
    }
    if element_id:
        s["_element_id"] = element_id
    if not first:
        s["border_border"] = "solid"
        s["border_width"] = dims(1, 0, 0, 0)
        s["border_color"] = "#C8D4E0"
        s["margin"] = dims(40, 0, 0, 0)
        s["padding"] = dims(40, 0, 0, 0)
    return container(nid, s, [
        heading(f"{nid}_h2", title, "h2", NAVY, "left",
                typography(size=28, weight=600, line_height=1.25, letter_spacing=-0.4)),
        *blocks_html(blocks, nid),
    ])


def gallery(nid):
    items = [container(f"{nid}_g{i}", {
        "content_width": "full", "min_height": {"unit": "px", "size": 140, "sizes": []},
        "background_background": "classic", "background_color": PLACE,
        "border_radius": dims(12, 12, 12, 12),
    }, []) for i in range(6)]
    return container(nid, {
        "content_width": "full", "flex_direction": "column",
        "border_border": "solid", "border_width": dims(1, 0, 0, 0),
        "border_color": "#C8D4E0", "margin": dims(40, 0, 0, 0), "padding": dims(40, 0, 0, 0),
    }, [
        heading(f"{nid}_h2", "Photo gallery", "h2", NAVY, "left",
                typography(size=28, weight=600, line_height=1.25, letter_spacing=-0.4)),
        container(f"{nid}_grid", {
            "content_width": "full", "flex_direction": "row", "flex_wrap": "wrap",
            "flex_gap": gap(12), "flex_wrap_mobile": "wrap",
        }, [
            container(f"{nid}_col{i}", {
                "content_width": "full", "width": {"unit": "%", "size": 32, "sizes": []},
                "width_mobile": {"unit": "%", "size": 48, "sizes": []},
                "flex_direction": "column",
            }, [items[i * 2], items[i * 2 + 1]]) for i in range(3)
        ]),
    ])


def sidebar_html(active_name, sublinks):
    rows = []
    for name, url in PROGRAMS:
        active = name == active_name
        cls = " is-active" if active else ""
        rows.append(f'<li><a class="gsm-nav{cls}" href="{url}">{name}</a>')
        if active and sublinks:
            sub = "".join(f'<a href="{url}#{sid}">{label}</a>' for label, sid in sublinks)
            rows.append(f'<ul class="gsm-subnav">{sub}</ul>')
        rows.append("</li>")
    return '<ul class="gsm-nav-list">' + "".join(rows) + "</ul>"


def build_sidebar(active_name, sublinks):
    label = heading("art_label", "Programs", "p", BLUE, "left",
                    typography(size=13, weight=700, transform="uppercase", letter_spacing=0.8))
    nav = widget("art_nav", "text-editor", {"editor": sidebar_html(active_name, sublinks)})
    return container("art_sidebar", {
        "content_width": "full", "width": {"unit": "px", "size": 240, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column", "flex_gap": gap(10),
        "css_classes": "gsm-article-sidebar",
    }, [label, nav])


def build_content(pid, data):
    secs = [rte_section("art_overview", "Overview", OVERVIEW, first=True)]
    for i, (sid, title, blocks) in enumerate(data["sections"]):
        secs.append(rte_section(f"art_sec_{i}", title, blocks, element_id=sid))
    secs.append(gallery("art_gallery"))
    return container("art_content", {
        "content_width": "full", "width": {"unit": "px", "size": 640, "sizes": []},
        "width_tablet": {"unit": "%", "size": 100, "sizes": []},
        "width_mobile": {"unit": "%", "size": 100, "sizes": []},
        "flex_direction": "column",
    }, secs)


def row(pid, active_name):
    data = PAGE_DATA.get(pid, {"sections": [], "sublinks": []})
    return container("art_row", {
        "content_width": "boxed", "boxed_width": {"unit": "px", "size": 1200, "sizes": []},
        "flex_direction": "row", "flex_gap": gap(56), "flex_align_items": "flex-start",
        "flex_wrap": "nowrap", "flex_wrap_tablet": "wrap", "flex_wrap_mobile": "wrap",
        "padding": dims(64, 40, 88, 40),
    }, [build_sidebar(active_name, data["sublinks"]), build_content(pid, data)])


def edit(pid, active_name):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    # keep hero + cta band, replace everything between with the new article row
    hero = next((n for n in data if n.get("elType") == "container"
                 and n.get("settings", {}).get("background_image", {}).get("url")), data[0])
    band = next((n for n in data if n.get("id") == "gsm_cta_band"), None)
    new = [hero, row(pid, active_name)]
    if band:
        new.append(band)
    fd, path = tempfile.mkstemp(suffix=f"_article_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(new, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  {pid}: article rebuilt ({len(new)} sections)")


if __name__ == "__main__":
    for pid, (name, _) in zip([2088, 2089, 2127, 2090, 2091], PROGRAMS):
        edit(pid, name)
    print("Done.")
