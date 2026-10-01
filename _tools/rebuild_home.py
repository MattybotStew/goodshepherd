import json, os

def px(top, right, bottom, left, unit="px"):
    return {"unit": unit, "top": top, "right": right, "bottom": bottom, "left": left, "isLinked": False}

def el(node_id, el_type, settings, elements=None, is_inner=False):
    return {"id": node_id, "elType": el_type, "settings": settings, "elements": elements or [], "isInner": is_inner}

def widget(node_id, widget_type, settings):
    node = el(node_id, "widget", settings, is_inner=False)
    node["widgetType"] = widget_type
    return node

def build_programs_section():
    # 5 program cards from src/data/programs.js
    programs = [
        {"name": "Community Day Services", "path": "/programs/community-day-services"},
        {"name": "Vocational Program", "path": "/programs/vocational"},
        {"name": "Special Olympics", "path": "/programs/special-olympics"},
        {"name": "Residential Living", "path": "/programs/residential-living"},
        {"name": "Health & Well Being", "path": "/programs/health-well-being"},
    ]
    
    cards = []
    for i, p in enumerate(programs):
        card = el(f"prog_card_{i}", "container", {
            "width": {"unit": "%", "size": 20 if len(programs) == 5 else 25, "sizes": []},
            "padding": px("20", "20", "20", "20"),
            "background_background": "classic",
            "__globals__": {"background_color": "globals/colors?id=astglobalcolor5"},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "globals/colors?id=astglobalcolor6",
            "border_radius": px("16", "16", "16", "16"),
        }, [
            widget(f"prog_icon_{i}", "image", {"image": {"id": "377", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/home-06.jpg"}, "width": {"unit": "%", "size": 100, "sizes": []}, "height": {"unit": "px", "size": 60, "sizes": []}, "object-fit": "cover"}),
            widget(f"prog_title_{i}", "heading", {"title": p["name"], "header_size": "h6", "align": "center", "__globals__": {"title_color": "globals/colors?id=astglobalcolor2"}}),
            widget(f"prog_btn_{i}", "button", {"text": "Learn More", "link": {"url": p["path"], "is_external": False}, "size": "sm", "align": "center", "__globals__": {"background_color": "globals/colors?id=astglobalcolor0"}})
        ], is_inner=True)
        cards.append(card)

    row = el("prog_row", "container", {
        "flex_direction": "row",
        "flex_wrap": "wrap",
        "justify_content": "center",
        "gap": {"unit": "px", "size": 20, "sizes": []},
        "padding": px("40", "40", "40", "40"),
    }, cards, is_inner=True)

    return el("prog_sec", "container", {
        "content_width": "boxed",
        "background_background": "classic",
        "__globals__": {"background_color": "globals/colors?id=astglobalcolor5"},
        "padding": px("80", "40", "80", "40"),
    }, [
        widget("prog_h2", "heading", {"title": "Our Programs & Services", "header_size": "h2", "align": "center", "__globals__": {"title_color": "globals/colors?id=astglobalcolor2"}}),
        row,
        widget("prog_view_all", "button", {"text": "View all programs", "link": {"url": "/programs", "is_external": False}, "align": "center", "__globals__": {"background_color": "globals/colors?id=astglobalcolor0"}})
    ])

def build_stories_section():
    stories = [
        {"title": "GSM's 35th Annual Fall Festival", "path": "/events#fall-festival"},
        {"title": "GSM Family Cookouts & MORE", "path": "/events#family"},
        {"title": "GSM's New Digital Den", "path": "/news/digital-den-community-day"},
    ]
    
    cards = []
    for i, s in enumerate(stories):
        card = el(f"story_card_{i}", "container", {
            "width": {"unit": "%", "size": 33.33, "sizes": []},
            "padding": px("20", "20", "20", "20"),
            "background_background": "classic",
            "__globals__": {"background_color": "globals/colors?id=astglobalcolor5"},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "globals/colors?id=astglobalcolor6",
            "border_radius": px("16", "16", "16", "16"),
        }, [
            widget(f"story_img_{i}", "image", {"image": {"id": "378", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/home-07.jpg"}, "width": {"unit": "%", "size": 100, "sizes": []}, "height": {"unit": "px", "size": 200, "sizes": []}, "object-fit": "cover"}),
            widget(f"story_title_{i}", "heading", {"title": s["title"], "header_size": "h6", "__globals__": {"title_color": "globals/colors?id=astglobalcolor2"}}),
            widget(f"story_btn_{i}", "button", {"text": "Read More", "link": {"url": s["path"], "is_external": False}, "size": "sm", "__globals__": {"background_color": "globals/colors?id=astglobalcolor0"}})
        ], is_inner=True)
        cards.append(card)

    row = el("story_row", "container", {
        "flex_direction": "row",
        "gap": {"unit": "px", "size": 30, "sizes": []},
        "padding": px("0", "40", "0", "40"),
    }, cards, is_inner=True)

    return el("story_sec", "container", {
        "content_width": "boxed",
        "background_background": "classic",
        "__globals__": {"background_color": "globals/colors?id=astglobalcolor4"},
        "padding": px("80", "40", "80", "40"),
    }, [
        widget("story_h2", "heading", {"title": "Inspiring tales of transformation", "header_size": "h2", "align": "center", "__globals__": {"title_color": "globals/colors?id=astglobalcolor2"}}),
        row
    ])

def rebuild_home():
    with open("/tmp/home_audit.json", "r") as f:
        data = json.load(f)

    # 1. Update Hero (ID 138ba28)
    # Find the CTA button inside the hero
    def update_hero(elements):
        for el in elements:
            if el.get("widgetType") == "button":
                el["settings"]["text"] = "Now Hiring! Apply Today"
                el["settings"]["link"] = {"url": "/careers", "is_external": False, "nofollow": False}
            if "elements" in el: update_hero(el["elements"])
    update_hero(data)

    # 2. Update Intro Strip (ID b233779)
    # Update the card titles and buttons
    def update_intro(elements):
        intro_links = ["/programs", "/support-gsm", "/support-gsm"]
        link_idx = 0
        for el in elements:
            if el.get("elType") == "container" and "elements" in el:
                # This is a card
                card_els = el["elements"]
                # Update title (image-box widget)
                for la in card_els:
                    if la.get("widgetType") == "image-box":
                        titles = ["01. Projects", "02. Support GSM", "03. Donate"]
                        if link_idx < len(titles):
                            la["settings"]["title_text"] = titles[link_idx]
                    # Update button
                    if la.get("widgetType") == "button":
                        if link_idx < len(intro_links):
                            la["settings"]["link"] = {"url": intro_links[link_idx], "is_external": False}
                            link_idx += 1
                if "elements" in el: update_intro(el["elements"])
            elif "elements" in el:
                update_intro(el["elements"])
    update_intro(data)

    # 3. Reorder and Filter Containers
    # Identify existing critical containers
    hero = next((c for c in data if c["id"] == "138ba28"), None)
    intro = next((c for c in data if c["id"] == "b233779"), None)
    about = next((c for c in data if "About Us" in str(c)), None) # Rough match
    impact = next((c for c in data if "Mission" in str(c)), None)
    
    # If we can't find them by keyword, we'll use indices but let's try to keep it safe.
    # Actually, let's just rebuild the shell and preserve the content of the specific containers.
    
    new_data = []
    if hero: new_data.append(hero)
    if intro: new_data.append(intro)
    if impact: new_data.append(impact)
    if about: new_data.append(about)
    
    # Add Foundation CTA Band
    cta_band = el("foundation_cta", "container", {
        "content_width": "full",
        "background_background": "classic",
        "__globals__": {"background_color": "globals/colors?id=astglobalcolor0"},
        "padding": px("60", "40", "60", "40"),
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
    }, [
        widget("cta_text", "heading", {"title": "We can create a better tomorrow", "header_size": "h2", "align": "center", "__globals__": {"title_color": "globals/colors?id=astglobalcolor5"}}),
        widget("cta_btn", "button", {"text": "Support GSM", "link": {"url": "/support-gsm", "is_external": False}, "align": "center", "__globals__": {"background_color": "globals/colors?id=astglobalcolor5", "button_text_color": "globals/colors?id=astglobalcolor0"}})
    ])
    new_data.append(cta_band)
    
    # Add Programs Section
    new_data.append(build_programs_section())
    
    # Add Stories Section
    new_data.append(build_stories_section())
    
    with open("/tmp/home_rebuilt.json", "w") as f:
        json.dump(new_data, f, separators=(",", ":"))
    
    print("Homepage rebuilt successfully.")

if __name__ == "__main__":
    rebuild_home()
