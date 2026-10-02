#!/usr/bin/env python3
"""Stack Home (315) pre-existing rows on tablet/mobile like the wire."""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")
PAGE_ID = 315
P100 = {"unit": "%", "size": 100, "sizes": []}
P50 = {"unit": "%", "size": 50, "sizes": []}

WRAP_ROWS = ["66df653", "support_row", "e743605"]
COLS_100 = ["8aa656b", "eacef01", "137de2d", "4892689", "13489bf"]
COLS_50 = ["support_card_0", "support_card_1", "support_card_2", "support_card_3"]


def walk(nodes, fn):
    for n in nodes:
        fn(n)
        walk(n.get("elements", []), fn)


def main():
    raw = subprocess.check_output([WP, "post", "meta", "get", str(PAGE_ID),
                                   "_elementor_data"]).decode()
    data = json.loads(raw)
    changed = []

    def apply(n):
        nid = n.get("id")
        if nid in WRAP_ROWS:
            s = n["settings"]
            s["flex_wrap"] = "nowrap"
            s["flex_wrap_tablet"] = "wrap"
            s["flex_wrap_mobile"] = "wrap"
            changed.append(nid)
        if nid in COLS_100:
            n["settings"]["width_tablet"] = dict(P100)
            n["settings"]["width_mobile"] = dict(P100)
            changed.append(nid)
        if nid in COLS_50:
            n["settings"]["width_tablet"] = dict(P50)
            n["settings"]["width_mobile"] = dict(P100)
            changed.append(nid)

    walk(data, apply)
    fd, path = tempfile.mkstemp(suffix="_home_resp.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    subprocess.check_call([APPLY, str(PAGE_ID), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"Home: {changed}")


if __name__ == "__main__":
    main()
