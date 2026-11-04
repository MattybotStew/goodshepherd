#!/usr/bin/env python3
"""Port the 2026-10-27 client content matrix (commit ae7703e) to Local WP.

Covers the five pages the commit touched:
  315  Home          intro strip callouts + 4-up program cards
  316  About         Memberships + Accessibility copy
  317  Programs      hero lede, intro headline/copy, catalog intro, 4-up cards
  2088 Community Day real overview + Digital Den copy
  319  Contact       hero lede, contact bar, directory, location, thank-a-staff

Also switches the five program/service hero backgrounds from photo to the
gradient introduced for ArticleDetailPage.

Run:  python3 _tools/port_2026-10-27_matrix.py
"""
import json
import os
import subprocess
import tempfile

HOME = os.path.expanduser("~")
WP = os.path.join(HOME, "Local Sites/goodshepherd/_tools/wp.sh")
APPLY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply_elementor.sh")

BLUE_DARK = "#005A9C"
NAVY = "#002A4E"
SPECIAL_ICON = {"id": "2178", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/special-olympics.svg"}

PROGRAM_CARDS = [
    {
        "title": "Community Day Services",
        "text": "Our Community Day Services build skills, friendships, and meaningful community connections.",
        "url": "/programs/community-day-services/",
        "icon": {"id": "2176", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/community-day.svg"},
    },
    {
        "title": "Community Engagement",
        "text": "Explore interests and connect with others through activities, outings and Special Olympics.",
        "url": "/programs/special-olympics/",
        "icon": SPECIAL_ICON,
    },
    {
        "title": "Residential Living",
        "text": "Our 13 CILA homes offer welcoming living across our 60-acre campus and the city of Momence",
        "url": "/programs/residential-living/",
        "icon": {"id": "2179", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/residential.svg"},
    },
    {
        "title": "Health & Well Being",
        "text": "Personalized support helps each man stay active, feel his best, and enjoy a fulfilling life.",
        "url": "/programs/health-well-being/",
        "icon": {"id": "2180", "url": "https://goodshepherd.local/wp-content/uploads/2026/10/health.svg"},
    },
]

COMMUNITY_OVERVIEW = [
    ("art_overview_p0", "<p>Community Day Services at Good Shepherd Manor provide a dynamic, engaging environment where men with intellectual and developmental disabilities can learn, grow, and build meaningful connections. Our structured classes and hands-on activities are tailored to each individual’s interests and abilities, with a focus on building practical skills for greater independence and confidence in daily life. From vocational training and technology to personal living skills and economics, each day offers opportunities to discover strengths and try new things in a supportive, caring atmosphere.</p>"),
    ("art_overview_p1", "<p>Beyond the classroom, community engagement is a key part of our program. Men enjoy outings for shopping, attending Mass, participating in Special Olympics, and taking part in events throughout the Momence community. Through these experiences, friendships grow, social skills strengthen, and a sense of belonging flourishes both on campus and beyond.</p>"),
    ("art_overview_p3", "<p>Each day is thoughtfully structured to balance learning and recreation. The morning may begin with classroom instruction or skill-building activities, followed by hands-on projects or community outings. Afternoons often include time for hobbies, physical activity, or specialized programs like our Digital Den. Throughout the day, caring staff provide encouragement, guidance, and support, ensuring that every man has the chance to participate at his own pace and according to his interests.</p>"),
    ("art_overview_ul4", "<ul>"
        "<li>Skill-building classes in technology, budgeting, cooking, and personal care</li>"
        "<li>Vocational experiences that prepare for meaningful work opportunities</li>"
        "<li>Community outings to local businesses, churches, and events</li>"
        "<li>Active participation in Special Olympics and recreational activities</li>"
        "</ul>"),
]

COMMUNITY_FINAL_P = ("<p>At the heart of Community Day Services is our belief that every man has gifts to share. "
                     "By nurturing those gifts in a welcoming, family-like environment, we help each individual build "
                     "confidence, develop independence, and enjoy a full, purposeful life.</p>")

ACC_P1 = ("<p>Good Shepherd Manor is committed to treating every person with dignity and respect. In keeping with our "
          "mission of providing high-quality, compassionate care to men with intellectual and developmental disabilities, "
          "we strive to make our website accessible and welcoming to people of all abilities.</p>"
          "<p>Our goal is to continually improve the accessibility and usability of our website so everyone can learn about "
          "our programs, access resources, and connect with our mission.</p>")

ACC_P2 = ("<p>If you experience difficulty accessing any part of our website or need information in an alternative format, "
          "please contact us at 815-472-3700 or info@goodshepherdmanor.org. Please include the page address and a brief "
          "description of the difficulty so we can better assist you.</p>"
          "<p>We welcome your feedback as we work toward a more accessible online experience.</p>")


# ---------------------------------------------------------------- helpers
def load(pid):
    raw = subprocess.check_output([WP, "post", "meta", "get", str(pid), "_elementor_data"]).decode()
    return json.loads(raw)


def save(pid, data):
    fd, path = tempfile.mkstemp(suffix=f"_port_{pid}.json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
    subprocess.check_call([APPLY, str(pid), path], stdout=subprocess.DEVNULL)
    os.remove(path)
    print(f"  applied {pid}")


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.get("elements", []))


def need(data, nid):
    for n in walk(data):
        if n.get("id") == nid:
            return n
    raise SystemExit(f"missing node {nid}")


def parent_of(data, nid):
    for n in walk(data):
        for child in n.get("elements", []):
            if child.get("id") == nid:
                return n
    raise SystemExit(f"missing parent for {nid}")


def insert_after(data, nid, node):
    p = parent_of(data, nid)
    i = next(i for i, c in enumerate(p["elements"]) if c.get("id") == nid)
    p["elements"].insert(i + 1, node)


def remove(data, nid):
    p = parent_of(data, nid)
    p["elements"] = [c for c in p["elements"] if c.get("id") != nid]


def clone(node, nid):
    out = json.loads(json.dumps(node))
    out["id"] = nid
    for c in out.get("elements", []):
        c["id"] = c["id"] + "_copy"
    return out


# ---------------------------------------------------------------- pages
def home(data):
    # Intro strip: 01 Get Involved / 02 Donate / 03 News You Can Use
    for nid, title, text, url in [
        ("7b6ee0d", "Get Involved",
         "Share your time and talents, join an event, or volunteer to make a meaningful difference in the lives of the men at GSM.",
         "/support-gsm/"),
        ("0497ba5", "Donate",
         "Help the men of GSM enjoy meaningful opportunities, lasting friendships, and a place to call home.",
         "/support-gsm/"),
        ("67bdf6f", "News You Can Use",
         "Get connected with Manor news, newsletters, useful updates and resources for GSM families",
         "/news/"),
    ]:
        s = need(data, nid)["settings"]
        s["title_text"] = title
        s["description_text"] = text
    for nid, url in [("9db92a4", "/support-gsm/"), ("7b30df7", "/support-gsm/"), ("4dc8404", "/news/")]:
        need(data, nid)["settings"]["link"] = {"url": url, "is_external": False, "nofollow": False}

    # Programs catalog: lede + 4 cards
    need(data, "prog_lede")["settings"]["title"] = (
        "Explore the programs and services that bring care, opportunity, and purpose to everyday life.")

    for i, card in enumerate(PROGRAM_CARDS):
        need(data, f"prog_title_{i}")["settings"]["title"] = card["title"]
        need(data, f"prog_desc_{i}")["settings"]["editor"] = f"<p>{card['text']}</p>"
        need(data, f"prog_btn_{i}")["settings"]["link"] = {
            "url": card["url"], "is_external": False, "nofollow": False}
        need(data, f"prog_icon_{i}")["settings"]["image"] = dict(card["icon"])
    for i in range(4):
        cs = need(data, f"prog_card_{i}")["settings"]
        cs["width"] = {"unit": "%", "size": 25, "sizes": []}
    need(data, "prog_card_4").get("settings")  # ensure it exists before removal
    remove(data, "prog_card_4")


def about(data):
    need(data, "about_aff_eyebrow")["settings"]["title"] = "Memberships"
    need(data, "about_aff_h2")["settings"]["title"] = "Member Organizations or Affiliations"
    need(data, "about_aff_p")["settings"]["editor"] = (
        "<p>GSM is a member of a variety of local professional and civic organizations, as well as statewide "
        "organizations such as the Kankakee &amp; Momence Chamber of Commerce, Intersect For Ability, "
        "United Way of Kankakee County, Special Olympics &amp; ARC of IL.</p>")
    pill = ("display:inline-block;padding:12px 18px;margin:0 12px 12px 0;border:1px solid #C8D4E0;"
            "border-radius:8px;background:#fff;font-size:14px;font-weight:700;color:#002A4E;")
    need(data, "about_aff_pills")["settings"]["editor"] = (
        f'<p><span style="{pill}">ARC of Illinois</span>'
        f'<span style="{pill.replace("margin:0 12px 12px 0", "margin:0 0 12px 0")}">Intersect For Ability</span></p>')

    need(data, "about_acc_h2")["settings"]["title"] = "Website Accessibility Statement"
    need(data, "about_acc_p1")["settings"]["editor"] = ACC_P1
    need(data, "about_acc_p2")["settings"]["editor"] = ACC_P2
    need(data, "about_acc_link")["settings"]["text"] = "Contact Us for More Information"


def programs(data):
    need(data, "prog_sub")["settings"]["title"] = (
        "From welcoming homes and engaging day programs to personalized health and wellness support, we help each "
        "man build skills, explore interests, form friendships, and enjoy a meaningful, fulfilling life.")
    need(data, "prog_intro_h2")["settings"]["title"] = "Building Skills, Connections, and Confidence"
    need(data, "prog_intro_p")["settings"]["editor"] = (
        "<p>Through personalized support and engaging experiences, each man discovers his strengths, develops "
        "everyday skills, builds lasting friendships, and gains confidence to try new things.</p>")
    need(data, "prog_services_p")["settings"]["editor"] = (
        "<p>Explore the programs and services that bring care, opportunity, and purpose to everyday life.</p>")

    for i, card in enumerate(PROGRAM_CARDS):
        need(data, f"prog_title_{i}")["settings"]["title"] = card["title"]
        need(data, f"prog_desc_{i}")["settings"]["editor"] = f"<p>{card['text']}</p>"
        need(data, f"prog_btn_{i}")["settings"]["link"] = {
            "url": card["url"], "is_external": False, "nofollow": False}
        need(data, f"prog_icon_{i}")["settings"]["image"] = dict(card["icon"])
        need(data, f"prog_card_{i}")["settings"]["width"] = {"unit": "%", "size": 25, "sizes": []}
    remove(data, "prog_card_4")


def community_day(data):
    need(data, "afed91e")["settings"]["editor"] = (
        "<p>Classes explore vocational skills, economics, personal living skills, technology and more, with "
        "hands-on activities tailored to each resident’s needs.</p>")

    for nid, html in COMMUNITY_OVERVIEW:
        need(data, nid)["settings"]["editor"] = html
    need(data, "art_overview_h3_2")["settings"]["title"] = "A Typical Day"
    final = clone(need(data, "art_overview_p3"), "art_overview_p5")
    final["settings"]["editor"] = COMMUNITY_FINAL_P
    insert_after(data, "art_overview_ul4", final)

    need(data, "art_sec_0_p0")["settings"]["editor"] = (
        "<p>The Digital Den is a dedicated space where men at Good Shepherd Manor can build computer literacy and "
        "explore the world of technology in a fun, supportive setting. With guidance from trained staff, individuals "
        "learn essential skills like typing, navigating the internet safely, using word processing and spreadsheet "
        "programs, and communicating through email or video calls to stay connected with loved ones.</p>")
    need(data, "art_sec_0_q1")["settings"]["editor"] = (
        "<blockquote><p>Technology opens new doors to learning, independence, and connection.</p>"
        "<cite>GSM Community Day Services</cite></blockquote>")
    need(data, "art_sec_0_h3_2")["settings"]["title"] = "What the Space Is For"
    need(data, "art_sec_0_p3")["settings"]["editor"] = (
        "<p>The Digital Den is more than a computer lab—it’s a place of creativity and discovery. Men can work on "
        "personal projects, explore educational games, research topics of interest, or learn practical skills "
        "they’ll use in everyday life. Lessons are individualized to match each person’s goals and skill level, "
        "allowing for growth at a comfortable, encouraging pace.</p>")
    need(data, "art_sec_0_p4")["settings"]["editor"] = (
        "<ol>"
        "<li>Building digital literacy for everyday tasks</li>"
        "<li>Staying connected with family and friends</li>"
        "<li>Exploring hobbies, music, photos, and creative projects</li>"
        "</ol>")
    closing = clone(need(data, "art_sec_0_p3"), "art_sec_0_p6")
    closing["settings"]["editor"] = (
        "<p>Whether learning to send an email for the first time or mastering a new program, time in the Digital "
        "Den helps build confidence and independence—skills that carry over into the wider community.</p>")
    remove(data, "art_sec_0_co5")
    insert_after(data, "art_sec_0_p4", closing)


def contact(data):
    need(data, "ba8c4c0")["settings"]["description_text"] = (
        "Have a question about Good Shepherd Manor, our services or ways to get involved? Connect with our team to "
        "learn more, thank a staff member or find the information you need. We’d love to hear from you!")

    need(data, "2e6064d")["settings"]["title"] = "Campus"
    need(data, "f51218b")["settings"]["title"] = "Need Assistance?"
    value = need(data, "835d4d4")["settings"]
    value["title"] = "Our Team Is Here to Help"
    value["link"] = {"url": "#thank", "is_external": False, "nofollow": False}

    need(data, "ddd017c")["settings"]["description_text"] = (
        "Whether you’re exploring care for a loved one, sharing feedback or recognizing someone who made a "
        "difference, we’re here to listen and help you take the next step.")

    office = need(data, "7c41d15")["settings"]
    office["title_text"] = "Main Office"
    office["description_text"] = (
        "(815) 472-3700<br>4129 N. State Route 1-17, Momence, IL 60954<br>P.O. Box 260, Momence, IL 60954")
    office.pop("link", None)

    careers = need(data, "bc1fa16")["settings"]
    careers["title_text"] = "Careers"
    careers["description_text"] = "View openings →"
    careers["link"] = {"url": "/careers/", "is_external": False, "nofollow": False}

    need(data, "6bea4aa")["settings"]["title"] = "Follow us on:"

    need(data, "3e55118")["settings"]["title"] = "Our Location"
    loc = need(data, "5d637fd")["settings"]
    loc["title"] = "Rooted in Momence. Connected by Care."
    loc["link"] = {
        "url": "https://maps.google.com/?q=4129+N.+State+Route+1-17,+Momence,+IL+60954",
        "is_external": True,
        "nofollow": False,
    }
    need(data, "70a8434")["settings"]["address"] = "4129 N. State Route 1-17, Momence, IL 60954"

    need(data, "a353d98")["settings"]["title"] = "Make Their Day"
    need(data, "070a6b2")["settings"]["editor"] = (
        "<p>Has a GSM staff member made a difference? Share your appreciation and let them know how much their "
        "kindness and dedication mean to you.</p>")


def gradient_hero(data):
    hero = data[0]
    s = hero["settings"]
    s["background_background"] = "gradient"
    s["background_color"] = BLUE_DARK
    s["background_color_b"] = NAVY
    s["background_color_stop"] = {"unit": "%", "size": 0, "sizes": []}
    s["background_color_b_stop"] = {"unit": "%", "size": 100, "sizes": []}
    s["background_gradient_type"] = "linear"
    s["background_gradient_angle"] = {"unit": "deg", "size": 180, "sizes": []}
    s["background_image"] = {"url": "", "id": "", "size": ""}
    for k in ("background_overlay_background", "background_overlay_color", "background_overlay_opacity"):
        s.pop(k, None)
    gl = s.get("__globals__", {})
    for k in ("background_color", "background_color_b"):
        gl.pop(k, None)
    if gl:
        s["__globals__"] = gl
    elif "__globals__" in s:
        del s["__globals__"]


if __name__ == "__main__":
    print("Home")
    d = load(315); home(d); save(315, d)
    print("About")
    d = load(316); about(d); save(316, d)
    print("Programs")
    d = load(317); programs(d); save(317, d)
    print("Community Day")
    d = load(2088); community_day(d); save(2088, d)
    print("Contact")
    d = load(319); contact(d); save(319, d)
    print("Program hero gradients")
    for pid in (2088, 2089, 2090, 2091, 2127):
        d = load(pid); gradient_hero(d); save(pid, d)
    print("Done.")
