import json, os

def wire_buttons(post_id, slug, mapping):
    json_path = f"/tmp/raw_{post_id}.json"
    fixed_path = f"/tmp/fixed_{post_id}.json"
    
    if not os.path.exists(json_path):
        print(f"Skipping {slug}: {json_path} not found.")
        return False

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return False

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

                target_url = None
                # Exact match
                if text in mapping:
                    target_url = mapping[text]
                # Partial match
                elif "Read More" in text:
                    target_url = "/news"
                elif "See all events" in text:
                    target_url = "/events"
                
                if target_url:
                    settings["link"] = {"url": target_url, "is_external": False, "nofollow": False}
                    buttons_fixed += 1
            
            if "elements" in el:
                walk(el["elements"])

    walk(data)
    
    if buttons_fixed > 0:
        with open(fixed_path, "w") as f:
            json.dump(data, f, separators=(",", ":"))
        print(f"Fixed {buttons_fixed} buttons on {slug}.")
        return True
    else:
        print(f"No buttons to fix on {slug}.")
        return False

if __name__ == "__main__":
    mapping = {
        "Donate Now": "/support-gsm/#ways-to-give",
        "Our Impact": "/about#mission",
        "Ways to Give": "/support-gsm#ways-to-give",
        "Learn More": "/programs",
        "Get Involved": "/support-gsm",
        "View Programs": "/programs",
        "Read More": "/news",
        "See all events": "/events",
        "Support GSM": "/support-gsm",
    }
    
    pages = [
        (316, "/about"),
        (317, "/programs"),
        (2094, "/events"),
        (318, "/news"),
        (2095, "/newsletters"),
    ]
    
    for pid, slug in pages:
        if wire_buttons(pid, slug, mapping):
            # apply_elementor.sh path
            apply_cmd = f"/Users/matthewstewart/Developer/goodshepherd/_tools/apply_elementor.sh {pid} /tmp/fixed_{pid}.json"
            os.system(apply_cmd)
