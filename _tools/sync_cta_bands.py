import json, os, subprocess, shlex

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

def create_cta_band():
    return el("gsm_cta_band", "container", {
        "content_width": "full",
        "background_background": "classic",
        "__globals__": {"background_color": ACCENT},
        "padding": px("60", "40", "60", "40"),
        "flex_direction": "row",
        "justify_content": "center",
        "align_items": "center",
        "gap": {"unit": "px", "size": 20, "sizes": []},
    }, [
        widget("cta_text", "heading", {
            "title": "We can create a better tomorrow", 
            "header_size": "h2", 
            "align": "center", 
            "__globals__": {"title_color": WHITE}
        }),
        widget("cta_btn", "button", {
            "text": "Support GSM", 
            "link": {"url": "/support-gsm", "is_external": False}, 
            "align": "center", 
            "__globals__": {"background_color": WHITE, "button_text_color": ACCENT}
        })
    ])

def apply_cta_to_page(post_id, slug):
    wp_path = "/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh"
    cmd = [shlex.quote(wp_path), "post", "meta", "get", str(post_id), "_elementor_data"]
    
    result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    raw_data = result.stdout.strip()
    
    if not raw_data:
        print(f"No data for {slug}")
        return

    try:
        data = json.loads(raw_data)
    except:
        print(f"JSON error for {slug}")
        return

    if any(c.get("id") == "gsm_cta_band" for c in data):
        print(f"CTA band already exists on {slug}. Skipping.")
        return

    data.append(create_cta_band())

    fixed_path = f"/tmp/cta_fixed_{post_id}.json"
    with open(fixed_path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    
    apply_cmd = f"/Users/matthewstewart/Developer/goodshepherd/_tools/apply_elementor.sh {post_id} {fixed_path}"
    subprocess.run(apply_cmd, shell=True, check=True)
    print(f"Applied CTA band to {slug}.")

if __name__ == "__main__":
    pages = [
        (315, "/"),
        (316, "/about"),
        (317, "/programs"),
        (2088, "/programs/community-day-services"),
        (2089, "/programs/vocational"),
        (2090, "/programs/residential-living"),
        (2091, "/programs/health-well-being"),
        (2127, "/programs/special-olympics"),
        (2092, "/support-gsm"),
        (2093, "/shepherd-endowment-society"),
        (2094, "/events"),
        (318, "/news"),
        (2095, "/newsletters"),
        (2096, "/careers"),
        (319, "/contact"),
    ]
    
    for pid, slug in pages:
        apply_cta_to_page(pid, slug)
