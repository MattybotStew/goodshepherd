#!/usr/bin/env python3
"""Insert the wire's HomeIntroStrip(involved) after the Endowment hero."""
import json
import os
import subprocess
import tempfile

from el import intro_strip

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 2093

COLUMNS = [
    ("01.", "Support GSM",
     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
     "/support-gsm"),
    ("02.", "Volunteer",
     "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.",
     "/events"),
    ("03.", "Shepherd Endowment Society",
     "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugit nulla pariatur.",
     "/shepherd-endowment-society"),
]


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    strip = intro_strip("endow_introstrip", COLUMNS)
    data = [n for n in data if n.get("id") != "endow_introstrip"]
    data.insert(1, strip)
    fd, path = tempfile.mkstemp(suffix="_endow.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path])
    os.remove(path)
    print(f"Endowment: inserted intro strip ({len(data)} sections)")


if __name__ == "__main__":
    main()
