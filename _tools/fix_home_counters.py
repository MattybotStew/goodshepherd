import json

def update_counters():
    with open("/tmp/home.json", "r") as f:
        data = json.load(f)

    impact_stats = [
        {"value": "55", "label": "Years serving our community"},
        {"value": "100+", "label": "Men supported daily"},
        {"value": "5", "label": "Core programs offered"},
        {"value": "1971", "label": "Founded in Momence, IL"},
    ]

    # Counter widgets in Elementor have 'number' or 'end' settings
    # We need to find the counters and update their values and labels
    counter_found = 0
    
    def walk(elements):
        nonlocal counter_found
        for el in elements:
            if el.get("widgetType") == "counter":
                settings = el.get("settings", {})
                if counter_found < len(impact_stats):
                    stat = impact_stats[counter_found]
                    # Update the ending number
                    settings["end"] = stat["value"].rstrip('+')
                    # If there is a suffix/prefix for the '+'
                    settings["number_prefix"] = ""
                    settings["number_suffix"] = "+" if "+" in stat["value"] else ""
                    
                    # Update the title/label if it exists in the widget settings
                    # Usually counter labels are in 'title'
                    if "title" in settings:
                        settings["title"] = stat["label"]
                    
                    counter_found += 1
            
            if "elements" in el:
                walk(el["elements"])

    walk(data)
    
    with open("/tmp/home_fixed.json", "w") as f:
        json.dump(data, f, separators=(",", ":"))
    
    print(f"Updated {counter_found} counters.")

if __name__ == "__main__":
    update_counters()
