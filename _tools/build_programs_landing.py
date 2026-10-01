import json, os

def px(top, right, bottom, left, unit="px"):
    return {"unit": unit, "top": top, "right": right, "bottom": bottom, "left": left, "isLinked": False}

def el(node_id, el_type, settings, elements=None, is_inner=False):
    return {"id": node_id, "elType": el_type, "settings": settings, "elements": elements or [], "isInner": is_inner}

def widget(node_id, widget_type, settings):
    node = el(node_id, "widget", settings, is_inner=False)
    node["widgetType"] = widget_type
    return node

# Global Tokens
WHITE = "globals/colors?id=astglobalcolor5"
ALT_BG = "globals/colors?id=astglobalcolor4"
HEADING = "globals/colors?id=astglobalcolor2"
BODY = "globals/colors?id=astglobalcolor3"
ACCENT = "globals/colors?id=astglobalcolor0"

def build_programs_landing():
    # Data from src/data/programs.js (mimicked here for the builder)
    programs = [
        {"name": "Community Day Services", "path": "/programs/community-day-services", "desc": "Daytime activities, social engagement, and skill-building for men with IDD."},
        {"name": "Vocational Program", "path": "/programs/vocational", "desc": "Meaningful employment opportunities and job-skills training in the community."},
        {"name": "Special Olympics", "path": "/programs/special-olympics", "desc": "Competitive athletics and teamwork through the Special Olympics program."},
        {"name": "Residential Living", "path": "/programs/residential-living", "desc": "A supportive, dignified home environment tailored to individual needs."},
        {"name": "Health & Well Being", "path": "/programs/health-well-being", "desc": "Comprehensive nursing, clinic, and pharmacy services on campus."},
    ]

    # 1. Hero
    hero = el("prog_hero", "container", {
        "content_width": "full",
        "background_background": "classic",
        "background_image": {"id": "370", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/contact-bg.jpg"},
        "background_overlay_background": "classic",
        "__globals__": {"background_overlay_color": "globals/colors?id=astglobalcolor7"},
        "padding": px("160", "40", "160", "40"),
    }, [
        widget("prog_h1", "heading", {
            "title": "Programs & Services", 
            "header_size": "h1", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        }),
        widget("prog_sub", "heading", {
            "title": "Empowering lives through compassion, dignity, and purpose.", 
            "header_size": "p", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        })
    ])

    # 2. Intro Section (ProgramsIntroSection equivalent)
    intro = el("prog_intro", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "40", "40"),
        "flex_direction": "column",
        "align_items": "center",
    }, [
        widget("prog_intro_h2", "heading", {
            "title": "Our Approach to Care", 
            "header_size": "h2", 
            "align": "center", 
            "__globals__": {"title_color": HEADING}
        }),
        widget("prog_intro_p", "text-editor", {
            "editor": "<p style='text-align:center;'>At Good Shepherd Manor, we provide a comprehensive suite of programs designed to foster independence, health, and community integration for the men we serve.</p>",
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 18}
        })
    ])

    # 3. Program Cards Grid
    cards = []
    for i, p in enumerate(programs):
        card = el(f"prog_card_{i}", "container", {
            "width": {"unit": "%", "size": 20 if len(programs) == 5 else 25, "sizes": []},
            "padding": px("30", "30", "30", "30"),
            "background_background": "classic",
            "__globals__": {"background_color": WHITE},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "globals/colors?id=astglobalcolor6",
            "border_radius": px("16", "16", "16", "16"),
            "flex_direction": "column",
        }, [
            widget(f"prog_icon_{i}", "image", {
                "image": {"id": "377", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/home-06.jpg"}, 
                "width": {"unit": "%", "size": 100, "sizes": []}, 
                "height": {"unit": "px", "size": 60, "sizes": []}, 
                "object-fit": "cover"
            }),
            widget(f"prog_title_{i}", "heading", {
                "title": p["name"], 
                "header_size": "h6", 
                "align": "center", 
                "__globals__": {"title_color": HEADING}
            }),
            widget(f"prog_desc_{i}", "text-editor", {
                "editor": f"<p style='text-align:center; font-size:14px;'>{p['desc']}</p>"
            }),
            widget(f"prog_btn_{i}", "button", {
                "text": "Learn More", 
                "link": {"url": p["path"], "is_external": False}, 
                "size": "sm", 
                "align": "center", 
                "__globals__": {"background_color": ACCENT}
            })
        ], is_inner=True)
        cards.append(card)

    grid_row = el("prog_grid_row", "container", {
        "flex_direction": "row",
        "flex_wrap": "wrap",
        "justify_content": "center",
        "gap": {"unit": "px", "size": 20, "sizes": []},
        "padding": px("40", "40", "40", "40"),
    }, cards, is_inner=True)

    grid_sec = el("prog_grid_sec", "container", {
        "content_width": "boxed",
        "background_background": "classic",
        "__globals__": {"background_color": ALT_BG},
        "padding": px("80", "40", "80", "40"),
    }, [grid_row])

    # 4. View All CTA
    footer = el("prog_footer", "container", {
        "content_width": "boxed",
        "padding": px("40", "40", "80", "40"),
        "flex_direction": "column",
        "align_items": "center",
    }, [
        widget("prog_view_all", "button", {
            "text": "View all services", 
            "link": {"url": "/programs", "is_external": False}, 
            "align": "center", 
            "__globals__": {"background_color": ACCENT}
        })
    ])

    return [hero, intro, grid_sec, footer]

if __name__ == "__main__":
    canvas = build_programs_landing()
    with open("/tmp/programs_fixed.json", "w") as f:
        json.dump(canvas, f, separators=(",", ":"))
    print("Programs landing JSON generated.")
