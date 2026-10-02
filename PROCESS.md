# Good Shepherd Manor — design workflow

How to work the Figma side of the GSM site. Read this before your first review call.

For the project rules themselves — canonical IA, slugs, stack, hard rules — see [`AGENTS.md`](AGENTS.md). This file is the *how*. Where the two disagree, `AGENTS.md` wins.

---

## Read this first

**The starter is doing the design work.**

Production is WordPress: the **Non-Profit Organization 04** template on Astra + Elementor, imported once. You are not designing a new website. You are mapping that template's existing sections onto GSM's content and brand.

This one fact settles almost every argument:

> If a layout you want doesn't already exist in the 04 starter, **we drop the idea.** We don't add custom CSS, a child theme, or Elementor Theme Builder work to chase it.

So when you have an idea, the first question is always: *which existing starter section is this?* If you can point at one, it's cheap and we build it. If you can't, it needs a decision before anyone draws it.

- Starter demo: https://websitedemos.net/non-profit-organization-04/
- [Figma file **gS-Design**](https://figma.com/design/U5wiJ2dHCvnJXEkCYTZtZ9) · file key `U5wiJ2dHCvnJXEkCYTZtZ9`

---

## The 15 pages — locked

The SOW is 15 pages. This table is canonical; blog posts and newsletter items don't count. Slugs are locked because URLs are already in circulation.

| # | Page | Slug |
|---|---|---|
| 1 | Home | `/` |
| 2 | About Us | `/about` |
| 3 | Programs & Services | `/programs` |
| 4 | Community Day Services | `/programs/community-day-services` |
| 5 | Vocational Program | `/programs/vocational` |
| 6 | Residential Living | `/programs/residential-living` |
| 7 | Health & Well Being | `/programs/health-well-being` |
| 8 | GSM Foundation | `/support-gsm` |
| 9 | Ways to Give | `/ways-to-give` |
| 10 | Shepherd Endowment Society | `/shepherd-endowment-society` |
| 11 | Events | `/events` |
| 12 | News & Updates | `/news` |
| 13 | Newsletters & Family Resources | `/newsletters` |
| 14 | Careers | `/careers` |
| 15 | Contact Us | `/contact` |

`/privacy` is a utility page and doesn't count against the 15. `/sitemap` is a stakeholder artifact — **do not publish it.**

**Programs is a parent page with four children**, so breadcrumbs read `Home › Programs › Health & Well Being`. Draw them as a real hierarchy, not five flat pages.

**Things that are sections, not pages** — don't promote them without asking:

- About: History · Mission, Vision & Values · Affiliations · Accessibility
- Community Day: Digital Den
- Health: nursing · clinic · pharmacy · supports · transportation
- Events: Fall Festival · Golf Invitational · Family Events
- Careers: job openings · benefits
- Contact: form · staff directory · map · Thank a Staff Member

### Starter remap

| Imported 04 page | Becomes |
|---|---|
| Home | Home — swap copy and placeholders only |
| About Us | About Us |
| Our Work | Programs landing, **duplicated four times** for the programs |
| Stories | News & Updates |
| Donate | Ways to Give |
| Contact | Contact Us |

Duplicate, don't design fresh. GSM Foundation, Endowment, Events, Newsletters and Careers are all duplicates of these six.

---

## How to work

### The loop

```
you change it in Figma  →  note the node ID  →  hand it over  →  it lands in the wire  →  preview updates
```

The wires are built in code, so a copy change is a one-line edit rather than hours of frame updates. That only works if **the node ID travels with the change.** Figma reassigns IDs when you move or reorder frames, so before handing anything over:

1. Select the frame (or section).
2. Copy the link to selection — it's in the URL, `node-id=9009:2`.
3. Write the ID next to your note.

> "Moved the Donate band above Our Programs — node `9046:948` is unaffected, the band itself is unlabelled. I've flagged it for an ID." — a good note
>
> "Moved the Donate band above Our Programs." — a note that costs someone an afternoon

### Key nodes

| Page / frame | Node ID | Notes |
|---|---|---|
| Homepage | `9009:2` | The one frame that gets argued. Section IDs below. |
| Get Involved landing | `9179:32` (canvas `6:124`) | Jump-bar landing. Section IDs below. |
| Hero | `9046:787` | Photo overlay, one CTA |
| Intro strip | `9046:813` | Overlaps the hero — 3 cards |
| Our Impact | `9046:948` | Mission + 4 counters |
| About Us | `9046:901` | Copy + photo mosaic |

Exports of these live in `design/` as PNG + JSON, so you can see exactly which frame the wire was built from.

### Copy conventions

**Body copy is lorem ipsum on purpose.** We're presenting structure, not prose — the real copy awaits client review. So:

| Keep real | Use lorem |
|---|---|
| Headings, titles, eyebrow labels | Paragraphs, ledes, blurbs |
| Slugs, URLs, nav labels | Card body copy |
| Contact data | Story excerpts |
| Structured lists — gift methods, gift levels, timeline years | |
| Section order and count | |

Don't polish a paragraph you know is placeholder. Don't let a placeholder accidentally become real copy in production.

### Photos are placeholders

At wire stage, images are labelled placeholders, not real photography. Real assets come later. Don't spend a round on photo selection, and don't build a layout that depends on a specific image's crop or aspect ratio.

---

## The homepage wire

Node `9009:2`. Seven sections, in this order:

1. **Hero** — `9046:787`. Photo overlay, one CTA. Headline "A Community of Compassion, Dignity, and Purpose." Sub-headline about hands-on programs, caring services, and a supportive home. CTA: "Now Hiring! Apply Today" → `/careers`.
2. **Intro strip** — `9046:813`. Overlaps the hero. Three cards: `01 Projects` / `02 Get Involved` / `03 Donate`, greeked body, "Learn more."
3. **Our Impact** — `9046:948`. "Our Mission & Vision: Serving with Dignity" + mission statement + four counters: 55 years · 100+ men · 4 programs · 1971 founded. **No donate band in this section.**
4. **About Us** — `9046:901`. "A community of care, growth, and dignity for over 50 years." + four paragraphs + Read More, staggered photo mosaic.
5. **Donate CTA band** — standalone, below About. "We can create a better tomorrow" + Donate Now → `/ways-to-give`.
6. **Our Programs & Services** — four icon-placeholder cards + View all.
7. **Stories** — "Inspiring tales of transformation" + three story cards.

Notes that matter:

- **The hero is site-wide.** Every page — all 15, plus `/privacy` — uses the same photo-overlay hero. The header is transparent over the hero, then turns white on scroll. It's already been applied to every page, so don't treat it as a homepage-only thing.
- **There is no Get Involved split card or Upcoming Event block on the homepage.** They were cut deliberately. The Get Involved band is site-wide, near the footer, on every page.
- **Home does not use the starter's 01/02/03 + stories + partners pattern.** It follows the Figma wire above.

## The Get Involved wire

Node `9179:32`, route `/support-gsm`. This one changed direction mid-build, so read carefully.

1. **Hero** — breadcrumb "Get Involved", title "GSM Foundation", lorem lede.
2. **Intro strip** — `01 Donate` → `/ways-to-give`, `02 Volunteer` → `/events`, `03 Give for Good` → `/shepherd-endowment-society`. Overlaps the hero.
3. **Jump bar** — a tab-style bar of four links, sticky just under the header on scroll: GSM Foundation · Ways to Give · Shepherd Endowment Society · Events. Active link gets a blue underline.
4. **Four stacked split sections**, alternating image side:
   - `#foundation` — "Supporting the Manor for over 40 years". No read-more link; this *is* the landing page.
   - `#ways-to-give` — flipped. "Every gift stays on campus." → links to `/ways-to-give`
   - `#endowment` — "Stewardship that outlives a gift." → links to `/shepherd-endowment-society`
   - `#events` — flipped, soft image placeholder. Bullets: Fall Festival, Golf Invitational, Family Events. → links to `/events`

**The tabs scroll to anchors. They do not hide content.** All four sections stay visible, stacked. Client direction — if you see a design that swaps panels, it's wrong, not new.

The site-wide Get Involved CTA band is **not** drawn on this canvas. It sits above the footer on every page.

---

## What you can change, and what needs a call

**Change freely** — these are wireframe decisions and they cost nothing:

- Section order *within* a page, as long as both sections exist in the starter
- Headings, eyebrow labels, button labels that keep their destination
- Paragraph length and placeholder tone
- Which image placeholder goes where
- Flipping a split section's image left/right
- Card counts inside a card row, within what the starter supports

**Bring to a call first** — these change scope, cost, or URLs:

- A new page or a new slug
- A new nav item or dropdown item
- A new section type the starter doesn't already ship
- A new colour, font, or button style
- A new CTA destination
- Promoting a section to a page, or collapsing a page into a section
- A fifth Get Involved page

**Never:** a custom Astra child theme, an Elementor Theme Builder header or footer, a new plugin without a concrete need.

### URLs that have already been got wrong

These hash links are wrong and are not to be used:

| Wrong | Right |
|---|---|
| `/programs#health` | `/programs/health-well-being` |
| `/programs#community-day` | `/programs/community-day-services` |
| `/programs#vocational` | `/programs/vocational` |
| `/programs#residential` | `/programs/residential-living` |
| `/support-gsm#events` | `/events` |

---

## Colour & type

Set once, site-wide, in the Astra Customizer — not per page. If you need something outside this table, that's a conversation.

| Role | Value |
|---|---|
| Accent / buttons | `#0089DF` |
| Accent hover | `#006BB3` |
| Headings | `#002A4E` |
| Body text | `#303336` |
| Alternate background | `#FAFCFE` |
| White — header, footer | `#FFFFFF` |
| Muted | `#C8D4E0` |
| Font | DM Sans |
| Container | 1200px |

**The starter's lime is out.** The import ships lime green as its accent; it's replaced by GSM blue above. Lime still visible anywhere is an un-swapped global, not a design choice.

The site-wide CTA band is a solid GSM blue band with white type. The footer is white with a top rule — not a dark bar.

---

## Running a review round

**Before the call**
- Every frame reachable from the nav, and the nav matches the locked 6: About · Programs & Services · Get Involved (dropdown) · News · Careers · Contact, plus a Donate button
- Above-header bar: "Now Hiring — Direct Service Providers. Apply Today →" → `/careers`
- Footer: `(815) 472-3700` · P.O. Box 260, 4129 N. State Route 1-17, Momence, IL 60954 · quick links · newsletter · Facebook · Privacy · Accessibility
- The preview link is live. The GitHub Pages deploy runs on every push to `main` — check the repo's **Settings → Pages** for the URL.
- Section order matches the wire above; no stray partners row, no Get Involved split card

**During**
- Flag anything that doesn't map to a starter section, at the time you show it — not in the handover
- Say which node each change touches

**After**
- Notes with node IDs, ordered by page
- Anything you promised to check, written down with a name against it

Expect the homepage to be argued more than once, and expect the Get Involved pattern to be re-specified at least once. Both happened. That's the process working, not failing.

---

## Vocabulary

You'll hear these. Quick translations:

| Term | What it means |
|---|---|
| **Starter / template** | The pre-built WordPress theme layout we imported once and reuse everywhere |
| **Wire / wireframe** | The greyed-out, clickable version of a page — layout and structure, no real copy or photos |
| **Node ID** | Figma's address for a frame. The link that makes a change findable |
| **Duplicate** | Copy an existing page layout instead of designing a new one |
| **Section** | A block of content within a page, not a page of its own |
| **Split section** | Text on one side, image on the other; "flipped" swaps sides |
| **Intro strip** | The three cards that overlap the hero |
| **Jump bar** | The sticky tab row on Get Involved that scrolls to sections |
| **Counter** | A big number, e.g. "55 years" |
| **Greeked** | Text greyed out to placeholder |
| **Lorem** | Placeholder paragraph text |
| **Scope cut** | Something agreed to drop if the build runs long (Vocational is the designated one) |
| **Wireframe prototype** | This project — the clickable thing. Not the production site |

---

## Where things are

You'll reference these; you won't edit most of them.

| Path | What |
|---|---|
| `AGENTS.md` | Canonical rules — IA, slugs, palette, hard rules. Read this first |
| `FIGMA.md` | Node map and the Figma MCP procedure (for the code side) |
| `design/*.png` | Exports of the frames the wires were built from — your reference |
| `PROCESS.md` | This file |
| `src/pages/`, `src/components/` | The wireframes in code — the build team owns these |

If a rule isn't in `AGENTS.md` and isn't in here, ask rather than assume. The rules are written down precisely so that nobody has to remember.
