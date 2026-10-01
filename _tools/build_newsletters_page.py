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

def build_newsletters_page():
    # 1. Hero
    hero = el("nl_hero", "container", {
        "content_width": "full",
        "background_background": "classic",
        "background_image": {"id": "370", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/contact-bg.jpg"},
        "background_overlay_background": "classic",
        "__globals__": {"background_overlay_color": "globals/colors?id=astglobalcolor7"},
        "padding": px("160", "40", "160", "40"),
    }, [
        widget("nl_h1", "heading", {
            "title": "Newsletters & Family Resources", 
            "header_size": "h1", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        }),
        widget("nl_sub", "heading", {
            "title": "Staying connected with the Good Shepherd community.", 
            "header_size": "p", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        })
    ])

    # 2. Signup Section
    signup = el("nl_signup", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "40", "40"),
        "flex_direction": "column",
        "align_items": "center",
        "background_background": "classic",
        "__globals__": {"background_color": ALT_BG},
    }, [
        widget("nl_sig_h2", "heading", {
            "title": "Join our Mailing List", 
            "header_size": "h2", 
            "align": "center", 
            "__globals__": {"title_color": HEADING}
        }),
        widget("nl_sig_p", "text-editor", {
            "editor": "<p style='text-align:center;'>Receive our quarterly newsletters, family updates, and event announcements directly in your inbox.</p>",
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 18}
        }),
        # Using a placeholder for the SureForms form (ID 2056 for now, as we'll build a real one later)
        widget("nl_form", "shortcode", {
            "shortcode": "[sureforms id=2056]",
            "align": "center"
        })
    ])

    # 3. Newsletter Archive Grid
    posts_grid = {
        "id": "nl_grid",
        "elType": "container",
        "settings": {
            "content_width": "boxed",
            "padding": px("40", "40", "80", "40"),
        },
        "elements": [
            {
                "id": "nl_posts_widget",
                "elType": "widget",
                "widgetType": "posts",
                "settings": {
                    "posts_per_page": "6",
                    "columns": "3",
                    "query": {
                        "post_type": "post",
                        "category": "newsletters",
                    },
                    "layout": "classic",
                    "show_excerpt": "yes",
                    "show_thumbnail": "yes",
                }
            }
        ]
    }

    return [hero, signup, posts_grid]

if __name__ == "__main__":
    canvas = build_newsletters_page()
    with open("/tmp/newsletters_fixed.json", "w") as f:
        json.dump(canvas, f, separators=(",", ":"))
    print("Newsletters landing JSON generated.")
