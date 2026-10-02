import json, subprocess, os

def run_wp(cmd):
    full_cmd = f"/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh {cmd}"
    return subprocess.run(full_cmd, shell=True, capture_output=True, text=True).stdout

def apply_json(post_id, data):
    json_path = f"/tmp/fixed_{post_id}.json"
    with open(json_path, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    
    apply_cmd = f"/Users/matthewstewart/Developer/goodshepherd/_tools/apply_elementor.sh {post_id} {json_path}"
    subprocess.run(apply_cmd, shell=True, check=True)

def wire_page_buttons(post_id, slug):
    print(f"Wiring buttons for {slug} (ID {post_id})...")
    raw_data = run_wp(f"post meta get {post_id} _elementor_data")
    if not raw_data:
        print(f"No data found for {slug}")
        return

    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON for {slug}")
        return

    # Mapping based on PLAN.md §6
    mapping = {
        "Donate Now": "/support-gsm/#ways-to-give",
        "Our Impact": "/about#mission",
        "Ways to Give": "/support-gsm#ways-to-give",
        "Learn More": "/programs", # Default, can be overridden
        "Get Involved": "/support-gsm",
        "View Programs": "/programs",
        "Read More": "/news",
        "See all events": "/events",
        "Support GSM": "/support-gsm",
    }

    buttons_fixed = 0

    def walk(elements):
        nonlocal buttons_fixed
        for el in elements:
            if el.get("widgetType") == "button":
                settings = el.get("settings", {})
                text = settings.get("text", "").strip()
                
                if not text:
                    if "elements" in el: walk(el["elements"])
                    continue

                # Special logic for specific pages
                target_url = None
                if text in mapping:
                    target_url = mapping[text]
                elif "Read More" in text:
                    target_url = "/news"
                elif "See all events" in text:
                    target_url = "/events"
                elif "Learn More" in text and slug == "/programs":
                    target_url = "/about#mission" # Example override for programs
                
                if target_url:
                    settings["link"] = {"url": target_url, "is_external": False, "nofollow": False}
                    buttons_fixed += 1
            
            if "elements" in el:
                walk(el["elements"])

    walk(data)
    if buttons_fixed > 0:
        apply_json(post_id, data)
        print(f"Fixed {buttons_fixed} buttons on {slug}.")
    else:
        print(f"No buttons to fix on {slug}.")

if __name__ == "__main__":
    # Pages listed in PLAN.md §6
    pages = [
        (316, "/about"),
        (317, "/programs"),
        (2094, "/events"),
        (318, "/news"),
        (2095, "/newsletters"),
    ]
    
    for pid, slug in pages:
        wire_page_buttons(pid, slug)
