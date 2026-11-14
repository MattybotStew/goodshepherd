"""Apply _tools/design_patches.json to generated Elementor data.

The same patch table is applied to the live pages by design_sweep_fixes.php, so
a page rebuilt from build_pages.py / build_home_replica.py keeps the fixes.

    from design_patches import apply_patches
    data = apply_patches(315, data)
"""
import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "design_patches.json")) as _f:
    _PATCHES = json.load(_f)


def _rules_for(doc_key):
    rules = []
    for scope in ("all", str(doc_key)):
        for key, settings in _PATCHES.get(scope, {}).items():
            clean = {k: v for k, v in settings.items() if not k.startswith("_why")}
            if key.startswith("re:"):
                rules.append((re.compile(key[3:]), clean))
            else:
                rules.append((key, clean))
    return rules


def _matches(rule, element_id):
    return rule.match(element_id) if hasattr(rule, "match") else rule == element_id


def apply_patches(doc_key, data):
    rules = _rules_for(doc_key)

    def walk(nodes):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            eid = node.get("id", "")
            settings = node.setdefault("settings", {})
            for rule, patch in rules:
                if _matches(rule, eid):
                    settings.update(patch)
            # Elementor only prints a container's desktop width at >=768px; below
            # that its default `.e-con.e-flex{--width:100%}` wins. A fixed px width
            # (icon tiles) therefore needs an explicit mobile value.
            width = settings.get("width")
            if (node.get("elType") == "container" and isinstance(width, dict)
                    and width.get("unit") == "px" and "width_mobile" not in settings):
                settings["width_mobile"] = dict(width)
            walk(node.get("elements", []))

    walk(data)
    return data
