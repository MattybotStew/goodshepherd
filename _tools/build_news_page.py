import json, os

def build_news_page():
    # We are converting the static page (ID 318) into a real archive.
    # In Elementor, a "post archive" usually means a specific template or a 
    # laout using the "Posts" widget.
    
    # Data from src/data/news.js
    news_items = [
        {"title": "GSM's 35th Annual Fall Festival", "path": "/news/35th-annual-fall-festival"},
        {"title": "GSM's New Digital Den in Community Day Services", "path": "/news/digital-den-community-day"},
        {"title": "30th Anniversary Golf Invitational Sponsors", "path": "/news/30th-golf-invitational"},
        {"title": "Family Cookouts and campus gatherings", "path": "/events#family"},
    ]

    # 1. Hero
    hero = {
        "id": "news_hero",
        "elType": "container",
        "settings": {
            "content_width": "full",
            "background_background": "classic",
            "background_image": {"id": "370", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/contact-bg.jpg"},
            "background_overlay_background": "classic",
            "__globals__": {"background_overlay_color": "globals/colors?id=astglobalcolor7"},
            "padding": {"unit": "px", "top": "160", "right": "40", "bottom": "160", "left": "40", "isLinked": False},
        },
        "elements": [
            {
                "id": "news_h1",
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": "News & Updates",
                    "header_size": "h1",
                    "align": "center",
                    "__globals__": {"title_color": "globals/colors?id=astglobalcolor5"},
                }
            }
        ]
    }

    # 2. Posts Grid (using the "posts" widget)
    # Note: The "posts" widget automatically fetches posts from the category.
    posts_grid = {
        "id": "news_grid",
        "elType": "container",
        "settings": {
            "content_width": "boxed",
            "padding": {"unit": "px", "top": "80", "right": "40", "bottom": "80", "left": "40", "isLinked": False},
        },
        "elements": [
            {
                "id": "news_posts_widget",
                "elType": "widget",
                "widgetType": "posts",
                "settings": {
                    "posts_per_page": "4",
                    "columns": "3",
                    "posts_offset": "0",
                    "query": {
                        "post_type": "post",
                        "category": "news",
                    },
                    "layout": "classic",
                    "show_excerpt": "yes",
                    "show_thumbnail": "yes",
                    "show_date": "yes",
                }
            }
        ]
    }

    # 3. CTA Band
    cta = {
        "id": "news_cta",
        "elType": "container",
        "settings": {
            "content_width": "full",
            "background_background": "classic",
            "__globals__": {"background_color": "globals/colors?id=astglobalcolor0"},
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False},
            "flex_direction": "row",
            "justify_content": "center",
        },
        "elements": [
            {
                "id": "news_cta_text",
                "elType": "widget",
                "widgetType": "heading",
                "settings": {
                    "title": "Stay Updated with the Manor",
                    "header_size": "h2",
                    "align": "center",
                    "__globals__": {"title_color": "globals/colors?id=astglobalcolor5"},
                }
            },
            {
                "id": "news_cta_btn",
                "elType": "widget",
                "widgetType": "button",
                "settings": {
                    "text": "Join our Newsletter",
                    "link": {"url": "/newsletters", "is_external": False},
                    "align": "center",
                    "__globals__": {"background_color": "globals/colors?id=astglobalcolor5", "button_text_color": "globals/colors?id=astglobalcolor0"},
                }
            }
        ]
    }

    return [hero, posts_grid, cta]

if __name__ == "__main__":
    canvas = build_news_page()
    with open("/tmp/news_fixed.json", "w") as f:
        json.dump(canvas, f, separators=(",", ":"))
    print("News landing JSON generated.")
