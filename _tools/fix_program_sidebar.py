#!/usr/bin/env python3
"""Replace the dead UAEL nav-menu widget in the program sidebar with a plain
list of program links (the wire's ArticleSidebar). UAEL is not installed.

Run:  python3 _tools/fix_program_sidebar.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

PAGE_IDS = [2088, 2089, 2127, 2090, 2091]
PROGRAMS = [
    ("Community Day Services", "/programs/community-day-services/"),
    ("Vocational Program", "/programs/vocational/"),
    ("Special Olympics", "/programs/special-olympics/"),
    ("Residential Living", "/programs/residential-living/"),
    ("Health & Well Being", "/programs/health-well-being/"),
]

MENU_HTML = ('<ul class="gsm-sidebar">'
             + "".join(f'<li><a href="{url}">{name}</a></li>' for name, url in PROGRAMS)
             + '</ul>')

CSS = (
    "\n/* GSM program sidebar nav */\n"
    ".gsm-sidebar{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;}\n"
    ".gsm-sidebar a{color:#002A4E;font-size:15px;font-weight:600;text-decoration:none;}\n"
    ".gsm-sidebar a:hover{color:#0089DF;}\n"
)


def fix(nodes):
    n = 0
    for node in nodes:
        if node.get("widgetType") == "uael-nav-menu":
            node["widgetType"] = "text-editor"
            node["settings"] = {"editor": MENU_HTML, "_css_classes": "gsm-sidebar-wrap"}
            n += 1
        n += fix(node.get("elements", []))
    return n


def append_css():
    code = (
        "<?php $css=wp_get_custom_css();"
        "if(strpos($css,'gsm-sidebar')===false){wp_update_custom_css_post($css.'"
        + CSS.replace("'", "\\'")
        + "');echo 'css added';}else{echo 'css present';}"
    )
    subprocess.run([WP, "eval", code], stdout=subprocess.DEVNULL)


def main():
    append_css()
    for pid in PAGE_IDS:
        raw = subprocess.check_output([WP, "post", "meta", "get", str(pid),
                                       "_elementor_data"]).decode()
        data = json.loads(raw)
        count = fix(data)
        fd, path = tempfile.mkstemp(suffix=f"_sidebar_{pid}.json")
        with os.fdopen(fd, "w") as fh:
            json.dump(data, fh, separators=(",", ":"))
        subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
        os.remove(path)
        print(f"  {pid}: replaced {count} widget(s)")
    print("Done.")


if __name__ == "__main__":
    main()
