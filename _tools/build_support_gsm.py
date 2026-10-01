#!/usr/bin/env python3
"""
Build the /support-gsm Elementor canvas: hero + jump bar + five anchored split
sections, matching src/data/getInvolved.js in the React wire.

Emits JSON on stdout. Apply it with:

    python3 _tools/build_support_gsm.py > /tmp/sgsm.json
    ~/Local\\ Sites/goodshepherd/_tools/wp.sh post meta update 2092 _elementor_data "$(cat /tmp/sgsm.json)"
"""

import json
import sys

PAGE_ID = 2092  # GSM Foundation (/support-gsm/)

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
            # Copy is first in the DOM, so the row inverts to put the image on
            # the left for non-flipped splits. Pin the mobile direction to
            # column: Elementor would otherwise carry row-reverse down as
            # column-reverse and render image-first, breaking both the wire and
            # the jump-bar anchor offset.
            "flex_direction": "row" if flip else "row-reverse",
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


JUMP_BAR_HTML = """
<nav class="gsm-jump" aria-label="Support GSM Foundation sections">
  <ul class="gsm-jump__list">
    <li><a class="gsm-jump__tab" href="#foundation">GSM Foundation</a></li>
    <li><a class="gsm-jump__tab" href="#ways-to-give">Ways to Give</a></li>
    <li><a class="gsm-jump__tab" href="#endowment-society">Shepherd Endowment Society</a></li>
    <li><a class="gsm-jump__tab" href="#events">Events</a></li>
    <li><a class="gsm-jump__tab" href="#memorial-tribute">Memorial or Tribute</a></li>
  </ul>
</nav>
<style>
  .gsm-jump-wrap { position: sticky; top: 0; z-index: 3; background: var(--ast-global-color-5, #fff); border-bottom: 1px solid var(--ast-global-color-7, #000); }
  .gsm-jump { overflow-x: auto; }
  .gsm-jump__list { display: flex; gap: 32px; list-style: none; margin: 0 auto; padding: 0 40px; max-width: 1200px; }
  .gsm-jump__tab { display: block; padding: 18px 0; white-space: nowrap; font-size: 15px; font-weight: 600; color: var(--ast-global-color-2, #002A4E); text-decoration: none; border-bottom: 3px solid transparent; }
  .gsm-jump__tab:hover { color: var(--ast-global-color-1, #006BB3); }
  .gsm-jump__tab.is-active { color: var(--ast-global-color-0, #0089DF); border-bottom-color: var(--ast-global-color-0, #0089DF); }
  @media (max-width: 921px) { .gsm-jump__list { gap: 24px; padding: 0 24px; } }
  html { scroll-behavior: smooth; }
  .gsm-anchor { scroll-margin-top: 72px; }
  @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
</style>
<script>
(function () {
  var ids = ["foundation", "ways-to-give", "endowment-society", "events", "memorial-tribute"];
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".gsm-jump__tab"));
  function activate(id) {
    tabs.forEach(function (tab) {
      var on = tab.getAttribute("href") === "#" + id;
      tab.classList.toggle("is-active", on);
      if (on) { tab.setAttribute("aria-current", "location"); } else { tab.removeAttribute("aria-current"); }
    });
  }
  if (!("IntersectionObserver" in window) || !tabs.length) { return; }
  var seen = {};
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) { seen[entry.target.id] = entry.isIntersecting ? entry.boundingClientRect.top : null; });
    var best = null;
    ids.forEach(function (id) {
      var top = seen[id];
      if (top === null || top === undefined) { return; }
      if (best === null || top < best.top) { best = { id: id, top: top }; }
    });
    if (best) { activate(best.id); }
  }, { rootMargin: "-72px 0px -55% 0px", threshold: 0 });
  ids.forEach(function (id) {
    var target = document.getElementById(id);
    if (target) { observer.observe(target); }
  });
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () { activate(tab.getAttribute("href").slice(1)); });
  });
  activate(ids[0]);
})();
</script>
""".strip()


def build_jump_bar():
    return el(
        "gsmjumpwrap",
        "container",
        {
            "content_width": "full",
            "flex_direction": "column",
            "css_classes": "gsm-jump-wrap",
            "background_background": "classic",
            "background_image": {"url": "", "id": "", "size": ""},
            "__globals__": {"background_color": WHITE},
        },
        [widget("gsmjump", "html", {"html": JUMP_BAR_HTML})],
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
    source = sys.argv[1] if len(sys.argv) > 1 else None
    if source:
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

    json.dump(canvas, sys.stdout, separators=(",", ":"))


if __name__ == "__main__":
    main()