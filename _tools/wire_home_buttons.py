import json

def wire_buttons():
    with open("/tmp/home_for_buttons.json", "r") as f:
        data = json.load(f)

    # Mapping based on PLAN.md §6 and AGENTS.md
    # Key = exact text or substring to identify the button
    # Value = destination URL
    mapping = {
        "Donate Now": "/support-gsm/#ways-to-give",
        "Learn More": "/programs", # First "Learn More" in intro strip
        "Get Involved": "/support-gsm",
        "View Programs": "/programs",
        "Read More": "/news", # Default for story cards
    }
    
    # Special case for the 3-card intro strip (Learn More x 3)
    # 01. Projects -> /programs
    # 02. Support GSM -> /support-gsm
    # 03. Donate -> /support-gsm
    intro_strip_links = ["/programs", "/support-gsm", "/support-gsm"]
    intro_button_count = 0

    buttons_fixed = 0

    def walk(elements):
        nonlocal buttons_fixed, intro_button_count
        for el in elements:
            if el.get("widgetType") == "button":
                settings = el.get("settings", {})
                text = settings.get("text", "").strip()
                
                if not text:
                    # Check if it's a nested element
                    if "elements" in el:
                        walk(el["elements"])
                    continue

                # Handle Intro Strip "Learn More" buttons specifically
                if text == "Learn More" and intro_button_count < len(intro_strip_links):
                    settings["link"] = {"url": intro_strip_links[intro_button_count], "is_external": False, "nofollow": False}
                    intro_button_count += 1
                    buttons_fixed += 1
                elif text in mapping:
                    settings["link"] = {"url": mapping[text], "is_external": False, "nofollow": False}
                    buttons_fixed += 1
                elif "Read More" in text:
                    settings["link"] = {"url": "/news", "is_external": False, "nofollow": False}
                    buttons_fixed += 1
            
            if "elements" in el:
                walk(el["elements"])

    walk(data)
    
    with open("/tmp/home_buttons_fixed.json", "w") as f:
        json.dump(data, f, separators=(",", ":"))
    
    print(f"Fixed {buttons_fixed} buttons on homepage.")

if __name__ == "__main__":
    wire_buttons()
