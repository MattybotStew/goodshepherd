#!/usr/bin/env python3
"""
Build the /support-gsm Elementor canvas: hero + jump bar + five anchored split
sections, matching src/data/getInvolved.js in the React wire.

Emits JSON on stdout. Apply it with:

    python3 _tools/build_support_gsm.py > /tmp/sgsm.json
    ~/Local\\ Sites/goodshepherd/_tools/wp.sh post meta update 2092 _elementor_data "$(cat /tmp/sgsm.json)"

The hero is loaded from _migration/support-gsm-hero.json (the shared photo-overlay
hero's first container) unless a source path is passed as argv[1].
"""

import json
import os
import sys

PAGE_ID = 2092  # GSM Foundation (/support-gsm/)

# Canonical hero source, committed so the builder does not depend on /tmp.
HERO_SOURCE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "_migration",
    "support-gsm-hero.json",
)

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua."
)
LOREM_LONG = LOREM + (
    " Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi "
    "ut aliquip ex ea commodo consequat."
)

WHITE = "globals/colors?id=astglobalcolor5"
ALT_BG = "globals/colors?id=astglobalcolor4"
HEADING = "globals/colors?id=astglobalcolor2"
BODY = "globals/colors?id=astglobalcolor3"
MUTED = "globals/colors?id=astglobalcolor6"
ACCENT = "globals/colors?id=astglobalcolor0"
ACCENT_HOVER = "globals/colors?id=astglobalcolor1"

# Same two Astra colours as literals, for controls that cannot take a global
# token. Keep in sync with the token table in AGENTS.md.
ACCENT_HOVER_VALUE = "#006BB3"

UPLOADS = "https://goodshepherd.local/wp-content/uploads/2023/06/"

# Split sections, in wire order. `flip` puts the image on the left.
SECTIONS = [
    {
        "id": "foundation",
        "eyebrow": "GSM Foundation",
        "title": "Supporting the Manor for over 40 years",
        "paragraphs": [LOREM_LONG, LOREM],
        "image": "about-01.jpg",
        "image_id": "397",
    },
    {
        "id": "ways-to-give",
        "eyebrow": "Ways to Give",
        "title": "Every gift stays on campus",
        "paragraphs": [LOREM_LONG, LOREM],
        "list": ["One-time gift", "Monthly giving", "Planned &amp; memorial gifts"],
        "flip": True,
        "image": "about-03.jpg",
        "image_id": "399",
    },
    {
        "id": "endowment-society",
        "eyebrow": "Shepherd Endowment Society",
        "title": "Stewardship that outlives a gift",
        "paragraphs": [LOREM_LONG, LOREM],
        "link_to": "/shepherd-endowment-society",
        "link_label": "Shepherd Endowment Society &rarr;",
        "image": "about-04.jpg",
        "image_id": "400",
    },
    {
        "id": "events",
        "eyebrow": "Events",
        "title": "Fall Festival, Brunch Auction, Golf Invitational, and family events",
        "paragraphs": [LOREM_LONG],
        "list": ["Fall Festival", "Brunch Auction", "Golf Invitational", "Family Events"],
        "flip": True,
        "soft_image": True,
        "link_to": "/events",
        "link_label": "See all events &rarr;",
    },
    {
        "id": "memorial-tribute",
        "eyebrow": "Memorial or Tribute",
        "title": "Honor a loved one through giving",
        "paragraphs": [LOREM_LONG, LOREM],
        "image": "about-05.jpg",
        "image_id": "368",
    },
]


def px(top, right, bottom, left, unit="px"):
    return {
        "unit": unit,
        "top": top,
        "right": right,
        "bottom": bottom,
        "left": left,
        "isLinked": False,
    }


def el(node_id, el_type, settings, elements=None, is_inner=False):
    return {
        "id": node_id,
        "elType": el_type,
        "settings": settings,
        "elements": elements or [],
        "isInner": is_inner,
    }


def widget(node_id, widget_type, settings):
    node = el(node_id, "widget", settings, is_inner=False)
    node["widgetType"] = widget_type
    return node


def eyebrow_widget(node_id, text):
    return widget(
        node_id,
        "heading",
        {
            "title": text,
            "header_size": "h6",
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 14, "sizes": []},
            "typography_font_weight": "700",
            "typography_text_transform": "uppercase",
            "typography_letter_spacing": {"unit": "px", "size": 1, "sizes": []},
            "_margin_bottom": px("0", "0", "8", "0"),
            "__globals__": {"title_color": ACCENT},
        },
    )


def title_widget(node_id, text):
    return widget(
        node_id,
        "heading",
        {
            "title": text,
            "header_size": "h2",
            "_margin_bottom": px("0", "0", "20", "0"),
            "__globals__": {"title_color": HEADING},
        },
    )


def body_widget(node_id, paragraphs):
    return widget(node_id, "text-editor", {"editor": "".join(f"<p>{p}</p>" for p in paragraphs)})


def list_widget(node_id, items):
    return widget(
        node_id,
        "icon-list",
        {
            "icon_list": [
                {
                    "text": item,
                    "selected_icon": {"value": "fas fa-check-circle", "library": "fa-solid"},
                    "link": {"url": "", "is_external": "", "nofollow": "", "custom_attributes": ""},
                }
                for item in items
            ],
            "space_between": {"unit": "px", "size": 12, "sizes": []},
            "icon_size": {"unit": "px", "size": 18, "sizes": []},
            "text_indent": {"unit": "px", "size": 8, "sizes": []},
            "_margin_top": px("20", "0", "0", "0"),
            "__globals__": {"text_color": BODY, "icon_color": ACCENT},
        },
    )


def link_widget(node_id, label, url):
    return widget(
        node_id,
        "button",
        {
            "text": label,
            "link": {"url": url, "is_external": "", "nofollow": ""},
            "size": "sm",
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 16, "sizes": []},
            "button_text_padding": px("0", "0", "0", "0"),
            "_margin_top": px("24", "0", "0", "0"),
            "__globals__": {
                "button_text_color": WHITE,
                "background_color": ACCENT,
                "background_hover_color": ACCENT_HOVER,
            },
        },
    )


def image_widget(node_id, section):
    if section.get("soft_image"):
        return el(
            node_id,
            "container",
            {
                "content_width": "full",
                "flex_direction": "column",
                "justify_content": "center",
                "align_items": "center",
                "min_height": {"unit": "px", "size": 420, "sizes": []},
                "border_radius": px("16", "16", "16", "16"),
                "background_background": "classic",
                "background_image": {"url": "", "id": "", "size": ""},
                "__globals__": {"background_color": MUTED},
            },
            is_inner=True,
        )
    return widget(
        node_id,
        "image",
        {
            "image": {"id": section["image_id"], "url": UPLOADS + section["image"]},
            "image_border_radius": px("16", "16", "16", "16"),
            # The 04 source photos mix portrait and landscape, so an
            # intrinsic-ratio image makes each split a different height.
            # Fix the box and crop instead.
            "width": {"unit": "%", "size": 100, "sizes": []},
            "height": {"unit": "px", "size": 480, "sizes": []},
            "object-fit": "cover",
            "object-position": "center",
        },
    )


def build_split(index, section):
    flip = section.get("flip", False)
    alt_bg = index % 2 == 1

    copy_widgets = [
        eyebrow_widget(f"sb{index}e1", section["eyebrow"]),
        title_widget(f"sb{index}t1", section["title"]),
        body_widget(f"sb{index}b1", section["paragraphs"]),
    ]
    if section.get("list"):
        copy_widgets.append(list_widget(f"sb{index}l1", section["list"]))
    if section.get("link_to"):
        copy_widgets.append(link_widget(f"sb{index}k1", section["link_label"], section["link_to"]))

    # Keep the 40px gutter on whichever side faces the image.
    copy_col = el(
        f"sb{index}cc",
        "container",
        {
            "content_width": "full",
            "width": {"unit": "%", "size": 50, "sizes": []},
            "flex_justify_content": "center",
            "flex_gap": {"column": "0", "row": "0", "isLinked": False, "unit": "px", "size": 0},
            "padding": px("0", "40" if flip else "0", "0", "0" if flip else "40"),
            "padding_mobile": px("40", "0", "0", "0"),
        },
        copy_widgets,
        is_inner=True,
    )

    image_col = el(
        f"sb{index}ic",
        "container",
        {
            "content_width": "full",
            "width": {"unit": "%", "size": 50, "sizes": []},
            "padding": px("0", "0" if flip else "40", "0", "40" if flip else "0"),
            "padding_mobile": px("0", "0", "0", "0"),
        },
        [image_widget(f"sb{index}im", section)],
        is_inner=True,
    )

    row = el(
        f"sb{index}rw",
        "container",
        {
            "content_width": "full",
            # Copy is first in the DOM, matching the wire's markup. Flipped
            # sections want the image on the left (.split--flip .split__copy
            # gets order: 2), which is row-reverse given this DOM order.
            # Pin the mobile direction to column: Elementor would otherwise
            # carry row-reverse down as column-reverse and render image-first,
            # breaking both the wire and the jump-bar anchor offset.
            "flex_direction": "row-reverse" if flip else "row",
            "flex_direction_mobile": "column",
            "flex_align_items": "stretch",
            "flex_gap": {"column": "20", "row": "20", "isLinked": True, "unit": "px", "size": 20},
            "padding_mobile": px("0", "0", "0", "0"),
        },
        [copy_col, image_col],
        is_inner=True,
    )

    return el(
        f"sb{index}sc",
        "container",
        {
            "content_width": "full",
            # _element_id renders as the wrapper's id="..." attribute, which is
            # what the jump bar's hrefs and the scroll-spy both target.
            "_element_id": section["id"],
            "css_classes": "gsm-anchor",
            "custom_css": ANCHOR_CUSTOM_CSS,
            "flex_direction": "column",
            "background_background": "classic",
            "padding": px("100", "40", "100", "40"),
            "padding_tablet": px("80", "32", "80", "32"),
            "padding_mobile": px("64", "24", "64", "24"),
            "background_image": {"url": "", "id": "", "size": ""},
            "__globals__": {"background_color": ALT_BG if alt_bg else WHITE},
        },
        [row],
    )


# The sticky offset that anchors must clear. Matches the bar's own height, which
# Pro's sticky control reports to the front end as `sticky_anchor_link_offset`.
JUMP_OFFSET = 72

# Jump bar labels, in wire order. Kept next to SECTIONS so a new section means
# adding one row in two adjacent tables rather than hunting through markup.
JUMP_TABS = [
    ("foundation", "GSM Foundation"),
    ("ways-to-give", "Ways to Give"),
    ("endowment-society", "Shepherd Endowment Society"),
    ("events", "Events"),
    ("memorial-tribute", "Memorial or Tribute"),
]

# Pro's Custom CSS panel, per element. This is the smallest amount of CSS that
# Elementor has no native control for: scroll-margin-top, horizontal overflow on
# narrow screens, and the active-state underline the scroll-spy toggles.
# Sticky itself uses Pro's native sticky control (Motion Effects tab) now that
# the licence is active and Pro is on 4.3.1, matching core 4.3.3.
BAR_CUSTOM_CSS = """
selector .gsm-jump {
  scroll-behavior: smooth;
  overflow-x: auto;
}
selector .gsm-jump__tab {
  border-bottom: 3px solid transparent;
  transition: color .15s ease, border-color .15s ease;
  /* Keep every label on one line so the bar stays a single row on mobile.
     Without this the tabs wrap and the sticky bar grows past the
     scroll-margin-top, hiding the top of the section it just scrolled to. */
  white-space: nowrap;
  /* Do not let the row squeeze labels; the row scrolls horizontally instead. */
  flex: 0 0 auto;
}
selector .gsm-jump__tab:hover,
selector .gsm-jump__tab:focus-visible {
  color: var(--ast-global-color-1);
}
selector .gsm-jump__tab.is-active {
  color: var(--ast-global-color-0);
  border-bottom-color: var(--ast-global-color-0);
}
@media (prefers-reduced-motion: reduce) {
  selector .gsm-jump { scroll-behavior: auto; }
}
"""

ANCHOR_CUSTOM_CSS = f"selector {{ scroll-margin-top: {JUMP_OFFSET}px; }}"


def jump_tab_widget(node_id, anchor, label):
    """A heading styled as a tab. The link target and the text are both editable
    in the Elementor panel, so adding or renaming a tab needs no code."""
    return widget(
        node_id,
        "heading",
        {
            "title": label,
            "link": {"url": f"#{anchor}", "is_external": "", "nofollow": ""},
            # A div, not a heading: these are links, and five more h2s would
            # compete with the real section headings in the document outline.
            "header_size": "div",
            # Widgets use _css_classes; containers use css_classes.
            "_css_classes": "gsm-jump__tab",
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 15, "sizes": []},
            "typography_font_weight": "600",
            "typography_line_height": {"unit": "px", "size": 24, "sizes": []},
            "_padding": px("18", "0", "18", "0"),
            "__globals__": {"title_color": HEADING},
            # Hover is a plain value, not a global: this control has no `global`
            # key, so a globals/colors?id= string renders literally as CSS text.
            "title_hover_color": ACCENT_HOVER_VALUE,
        },
    )


def build_jump_bar():
    """Native Elementor: a container wrapping a row of heading widgets.

    No HTML widget, so labels, links and colours are all visual edits. Sticky
    uses Pro's native sticky control on the wrapper.
    """
    row = el(
        "gsmjumprow",
        "container",
        {
            "content_width": "full",
            "css_classes": "gsm-jump",
            "flex_direction": "row",
            "flex_direction_mobile": "row",
            # Keys are prefixed with the group's name, `flex`. The value is
            # `nowrap` with no hyphen: "no-wrap" emits invalid CSS, gets
            # dropped, and the row wraps instead of scrolling horizontally.
            "flex_wrap": "nowrap",
            "flex_wrap_mobile": "nowrap",
            "flex_align_items": "center",
            "flex_gap": {"column": "32", "row": "32", "isLinked": True, "unit": "px", "size": 32},
            "padding": px("0", "40", "0", "40"),
            "padding_mobile": px("0", "24", "0", "24"),
        },
        [jump_tab_widget(f"gsmtab{index}", anchor, label) for index, (anchor, label) in enumerate(JUMP_TABS)],
        is_inner=True,
    )

    return el(
        "gsmjumpwrap",
        "container",
        {
            "content_width": "full",
            "css_classes": "gsm-jump-wrap",
            "flex_direction": "column",
            # BAR_CUSTOM_CSS targets `selector .gsm-jump` and the tab classes,
            # so it stays on this wrapper (the tabs' ancestor).
            "custom_css": BAR_CUSTOM_CSS.strip(),
            # Pro's native sticky (Motion Effects tab). The bar sits at the top
            # because the Astra header is not sticky on this page.
            "sticky": "top",
            "sticky_on": ["desktop", "tablet", "mobile"],
            "sticky_offset": 0,
            "z_index": 3,
            "background_background": "classic",
            "background_image": {"url": "", "id": "", "size": ""},
            "border_border": "solid",
            "border_width": {"unit": "px", "size": 1, "sizes": []},
            "border_color": HEADING,
            "__globals__": {"background_color": WHITE},
        },
        [row],
    )


def build_spy_snippet():
    """Scroll-spy, isolated at the end of the canvas.

    There is no Elementor control for this, so it stays a small Pro HTML
    snippet. It is deliberately separate from the bar: the bar above is fully
    visual, and editing a tab label or link there does not touch this code.
    """
    return widget(
        "gsmspy",
        "html",
        {
            # Ids come from the tabs in the DOM, not from JUMP_TABS, so renaming
            # or reordering a tab in Elementor does not require touching this.
            "html": f"""<script>
(function () {{
  var OFFSET = {JUMP_OFFSET};
  var wrappers = [].slice.call(document.querySelectorAll(".gsm-jump__tab"));
  // The class sits on the heading widget; the link lives on the inner anchor.
  var tabs = wrappers
    .map(function (w) {{ return {{ wrapper: w, anchor: w.querySelector("a[href^='#']") }}; }})
    .filter(function (t) {{ return t.anchor; }});
  if (!tabs.length || !("IntersectionObserver" in window)) {{ return; }}
  var ids = tabs.map(function (t) {{ return t.anchor.getAttribute("href").slice(1); }});

  function activate(id) {{
    tabs.forEach(function (t) {{
      var on = t.anchor.getAttribute("href") === "#" + id;
      t.wrapper.classList.toggle("is-active", on);
      if (on) {{ t.anchor.setAttribute("aria-current", "location"); }}
      else {{ t.anchor.removeAttribute("aria-current"); }}
    }});
  }}

  // The section that owns the reading position is the last one whose top has
  // crossed the bar. Comparing tops numerically does not work: a section
  // already scrolled past has the smallest (most negative) top, so picking the
  // minimum always selects a section behind the reader and gets the wrong tab
  // on a direct hash load. Measure every target and take the last crossing.
  function currentId() {{
    // A hash jump lands the section a few px past the offset, so allow a small
    // tolerance; otherwise the target reads as "not yet crossed" and the tab
    // lags one section behind.
    var line = OFFSET + 16;
    var last = null;
    var next = null;
    ids.forEach(function (id) {{
      var target = document.getElementById(id);
      if (!target) {{ return; }}
      var top = target.getBoundingClientRect().top;
      if (top <= line) {{
        last = id;
      }} else if (next === null) {{
        next = id;
      }}
    }});
    return last || next || ids[0];
  }}
  var ticking = false;
  function update() {{
    ticking = false;
    activate(currentId());
  }}
  var observer = new IntersectionObserver(function () {{
    if (ticking) {{ return; }}
    ticking = true;
    window.requestAnimationFrame(update);
  }}, {{ rootMargin: "-" + OFFSET + "px 0px -55% 0px", threshold: 0 }});
  ids.forEach(function (id) {{
    var target = document.getElementById(id);
    if (target) {{ observer.observe(target); }}
  }});
  tabs.forEach(function (t) {{
    t.anchor.addEventListener("click", function () {{
      activate(t.anchor.getAttribute("href").slice(1));
    }});
  }});
  update();
}})();
</script>"""
        },
    )


def retitle_hero(hero):
    """The wire titles the hero 'Support GSM Foundation', not 'GSM Foundation'."""
    stack = [hero]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if node.get("widgetType") == "image-box":
                node["settings"]["title_text"] = "Support GSM Foundation"
            stack.extend(node.get("elements", []))
    return hero


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else HERO_SOURCE
    if os.path.exists(source):
        with open(source) as handle:
            existing = json.load(handle)
    else:
        import subprocess

        wp = subprocess.run(
            [
                "wp",
                "post",
                "meta",
                "get",
                str(PAGE_ID),
                "_elementor_data",
                "--path=/Users/matthewstewart/Local Sites/goodshepherd/app/public",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        existing = json.loads(wp.stdout)

    # Keep the first container: it is the shared photo-overlay hero.
    hero = retitle_hero(existing[0])

    canvas = [hero, build_jump_bar()]
    for index, section in enumerate(SECTIONS):
        canvas.append(build_split(index, section))
    canvas.append(build_spy_snippet())

    json.dump(canvas, sys.stdout, separators=(",", ":"))


if __name__ == "__main__":
    main()