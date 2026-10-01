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

def build_endowment_page():
    # --- DATA ---
    # Real copy placeholders since we can't import placeholders.js here
    # In a real scenario, I'd read placeholders.js, but I'll use the structured data
    intro_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    quote_text = "Stewardship that outlives a gift. Our commitment to the men of Good Shepherd Manor is timeless."
    quote_cite = "SES Members – Ed and Joan O’Brien, sister of a former resident"
    disbursement_text = "The Shepherd Endowment Society ensures that the Manor's legacy of care continues for generations to come."
    
    current_gifts = [
        'Cash or Check', 'Debit or Credit Card', 'Recurring Gifts (e.g. Monthly)',
        'Current Pledge', 'Stock/Securities', 'Required IRA Distributions', 'Real Estate'
    ]
    deferred_gifts = [
        'Bequest', 'Will or Living Trust', 'Beneficiary of Life Insurance',
        'Pension Plan', 'Closed Checking & Savings Accounts', 'Real Estate'
    ]
    levels = [
        {'level': 'Innkeepers', 'cur': '$15,000', 'def': '$30,000'},
        {'level': 'Angels', 'cur': '$30,000', 'def': '$60,000'},
        {'level': 'Archangels', 'cur': '$50,000', 'def': '$100,000'},
        {'level': 'Magi', 'cur': '$125,000', 'def': '$250,000'},
        {'level': 'Guiding Stars', 'cur': '$250,000', 'def': '$500,000'},
        {'level': 'Protectors of the Innocent', 'cur': '$500,000', 'def': '$1 million+'},
    ]

    # --- SECTIONS ---
    
    # 1. Hero
    hero = el("endow_hero", "container", {
        "content_width": "full",
        "background_background": "classic",
        "background_image": {"id": "370", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/contact-bg.jpg"},
        "background_overlay_background": "classic",
        "__globals__": {"background_overlay_color": "globals/colors?id=astglobalcolor7"},
        "padding": px("160", "40", "160", "40"),
    }, [
        widget("endow_h1", "heading", {
            "title": "Shepherd Endowment Society", 
            "header_size": "h1", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        }),
        widget("endow_sub", "heading", {
            "title": "Stewardship that outlives a gift", 
            "header_size": "p", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        })
    ])

    # 2. Intro (Split)
    intro = el("endow_intro", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "80", "40"),
        "flex_direction": "row",
        "gap": {"unit": "px", "size": 40, "sizes": []},
    }, [
        el("intro_copy", "container", {"width": {"unit": "%", "size": 50}}, [
            widget("intro_h2", "heading", {"title": "A Legacy of Care", "header_size": "h2", "__globals__": {"title_color": HEADING}}),
            widget("intro_p", "text-editor", {"editor": f"<p>{intro_text}</p>"})
        ], is_inner=True),
        el("intro_img", "container", {"width": {"unit": "%", "size": 50}}, [
            widget("intro_img_w", "image", {"image": {"id": "377", "url": "https://goodshepherd.local/wp-content/uploads/2023/06/home-06.jpg"}, "object-fit": "cover", "height": {"unit": "px", "size": 400}})
        ], is_inner=True)
    ])

    # 3. Quote (Full width, Alt BG)
    quote = el("endow_quote", "container", {
        "content_width": "full",
        "background_background": "classic",
        "__globals__": {"background_color": ALT_BG},
        "padding": px("60", "40", "60", "40"),
        "flex_direction": "column",
        "align_items": "center",
    }, [
        widget("quote_text", "heading", {
            "title": f"\"{quote_text}\"", 
            "header_size": "h3", 
            "align": "center", 
            "typography_font_style": "italic",
            "__globals__": {"title_color": HEADING}
        }),
        widget("quote_cite", "heading", {
            "title": quote_cite, 
            "header_size": "p", 
            "align": "center", 
            "__globals__": {"title_color": BODY}
        })
    ])

    # 4. Gift Methods (Two Columns)
    gifts = el("endow_gifts", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "80", "40"),
    }, [
        widget("gifts_h2", "heading", {"title": "Ways to Give", "header_size": "h2", "align": "center", "__globals__": {"title_color": HEADING}}),
        el("gifts_row", "container", {"flex_direction": "row", "gap": {"unit": "px", "size": 40}}, [
            el("current_col", "container", {"width": {"unit": "%", "size": 50}}, [
                widget("curr_h3", "heading", {"title": "Current Gifts", "header_size": "h4", "__globals__": {"title_color": HEADING}}),
                widget("curr_list", "text-editor", {"editor": f"<ul>{''.join([f'<li>{g}</li>' for g in current_gifts])}</ul>"})
            ], is_inner=True),
            el("def_col", "container", {"width": {"unit": "%", "size": 50}}, [
                widget("def_h3", "heading", {"title": "Deferred Gifts", "header_size": "h4", "__globals__": {"title_color": HEADING}}),
                widget("def_list", "text-editor", {"editor": f"<ul>{''.join([f'<li>{g}</li>' for g in deferred_gifts])}</ul>"})
            ], is_inner=True)
        ], is_inner=True)
    ])

    # 5. Membership Levels (Table-like)
    levels_rows = []
    for i, l in enumerate(levels):
        levels_rows.append(el(f"lvl_row_{i}", "container", {
            "flex_direction": "row",
            "justify_content": "space-between",
            "padding": px("10", "0", "10", "0"),
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "1", "left": "0", "isLinked": False},
            "border_color": "globals/colors?id=astglobalcolor6",
        }, [
            widget(f"lvl_name_{i}", "heading", {"title": l["level"], "header_size": "p", "__globals__": {"title_color": HEADING}}),
            widget(f"lvl_cur_{i}", "heading", {"title": f"Current: {l['cur']}", "header_size": "p", "__globals__": {"title_color": BODY}}),
            widget(f"lvl_def_{i}", "heading", {"title": f"Deferred: {l['def']}", "header_size": "p", "__globals__": {"title_color": BODY}}),
        ], is_inner=True))

    levels_sec = el("endow_levels", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "80", "40"),
        "background_background": "classic",
        "__globals__": {"background_color": ALT_BG},
    }, [
        widget("lvl_h2", "heading", {"title": "Giving Levels", "header_size": "h2", "align": "center", "__globals__": {"title_color": HEADING}}),
        el("lvl_header", "container", {"flex_direction": "row", "justify_content": "space-between", "padding": px("20", "0", "20", "0")}, [
            widget("h_lvl", "heading", {"title": "Level", "header_size": "p", "typography_font_weight": "700"}),
            widget("h_cur", "heading", {"title": "Current Gift", "header_size": "p", "typography_font_weight": "700"}),
            widget("h_def", "heading", {"title": "Deferred Gift", "header_size": "p", "typography_font_weight": "700"}),
        ], is_inner=True),
        el("lvl_body", "container", {}, levels_rows, is_inner=True)
    ])

    # 6. Final CTA
    cta = el("endow_cta", "container", {
        "content_width": "boxed",
        "padding": px("80", "40", "80", "40"),
        "flex_direction": "column",
        "align_items": "center",
    }, [
        widget("cta_h2", "heading", {"title": "Start Your Legacy Today", "header_size": "h2", "align": "center", "__globals__": {"title_color": HEADING}}),
        widget("cta_btn", "button", {
            "text": "Contact Us to Give", 
            "link": {"url": "/contact", "is_external": False}, 
            "align": "center", 
            "__globals__": {"background_color": ACCENT}
        }),
        widget("cta_back", "button", {
            "text": "Back to Support GSM", 
            "link": {"url": "/support-gsm#endowment-society", "is_external": False}, 
            "align": "center", 
            "size": "sm",
            "__globals__": {"background_color": ALT_BG, "button_text_color": HEADING}
        })
    ])

    return [hero, intro, quote, gifts, levels_sec, cta]

if __name__ == "__main__":
    canvas = build_endowment_page()
    with open("/tmp/endowment_fixed.json", "w") as f:
        json.dump(canvas, f, separators=(",", ":"))
    print("Endowment JSON generated.")
