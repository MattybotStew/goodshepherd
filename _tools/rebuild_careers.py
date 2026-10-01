import json, os

def px(top, right, bottom, left, unit="px"):
    return {"unit": unit, "top": top, "right": right, "bottom": bottom, "left": left, "isLinked": False}

def el(node_id, el_type, settings, elements=None, is_inner=False):
    return {"id": node_id, "elType": el_type, "settings": settings, "elements": elements or [], "isInner": is_inner}

def widget(node_id, widget_type, settings):
    node = el(node_id, "widget", settings, is_inner=False)
    node["widgetType"] = widget_type
    return node

WHITE = "globals/colors?id=astglobalcolor5"
ALT_BG = "globals/colors?id=astglobalcolor4"
HEADING = "globals/colors?id=astglobalcolor2"
BODY = "globals/colors?id=astglobalcolor3"
ACCENT = "globals/colors?id=astglobalcolor0"

def rebuild_careers():
    # Load existing data to preserve the Job Openings and Benefits containers
    try:
        with open("/tmp/careers_audit.json", "r") as f:
            existing_data = json.load(f)
    except:
        existing_data = []

    # Filter for only the containers we want to keep
    preserved = [c for c in existing_data if c.get("elType") == "container"]
    style_widget = [w for w in existing_data if w.get("widgetType") == "html"]

    # 1. Hero Section
    hero = el("car_hero", "container", {
        "content_width": "full",
        "background_background": "classic",
        "background_image": {"id": "370", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/contact-bg.jpg"},
        "background_overlay_background": "classic",
        "__globals__": {"background_overlay_color": "globals/colors?id=astglobalcolor7"},
        "padding": px("160", "40", "160", "40"),
    }, [
        widget("car_h1", "heading", {
            "title": "Join Our Team", 
            "header_size": "h1", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        }),
        widget("car_sub", "heading", {
            "title": "Make a meaningful difference in the lives of the men we serve.", 
            "header_size": "p", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        })
    ])

    # 2. CTA Section
    cta = el("car_cta", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "80", "40"),
        "flex_direction": "column",
        "align_items": "center",
        "background_background": "classic",
        "__globals__": {"background_color": ALT_BG},
    }, [
        widget("car_cta_h2", "heading", {
            "title": "Ready to Apply?", 
            "header_size": "h2", 
            "align": "center", 
            "__globals__": {"title_color": HEADING}
        }),
        widget("car_cta_btn", "button", {
            "text": "Submit Your Application", 
            "link": {"url": "mailto:careers@goodshepherdmanor.org", "is_external": False}, 
            "align": "center", 
            "__globals__": {"background_color": ACCENT}
        })
    ])

    # Assemble: Hero -> Preserved Containers -> CTA -> Style Widget
    new_data = [hero] + preserved + [cta] + style_widget

    with open("/tmp/careers_rebuilt.json", "w") as f:
        json.dump(new_data, f, separators=(",", ":"))
    
    print("Careers page rebuilt successfully.")

if __name__ == "__main__":
    rebuild_careers()
