# AGENTS.md — Good Shepherd Manor

Instructions for any LLM or agent working in this repo or on the production site.

> **Picking this up mid-build?** Read **§Handoff: current build state** first. It lists the page IDs, the generator scripts, the SureForms form IDs, the tooling that lives outside the repo, and the traps that have already cost debugging time.

## What this project is

Good Shepherd Manor (GSM) is a residential care community in Momence, IL for men with intellectual and developmental disabilities. This repo is a **wireframe prototype only** (Vite + React). It is not the production frontend.

The production site is **WordPress on WP Engine**: **Astra + Elementor**, built from one official Astra starter template with as little customization as possible.

Agency: CloudMellow. SOW cap: **15 main pages**. Blog posts and newsletter archive items do not count.

## North star

Prefer the starter template’s layout over the React wires.

- The wires decide **what pages exist, what each page says, and which URLs to use**.
- The starter decides **how it looks**.
- If a wire asks for a layout the starter does not already have, **drop the wire**. Do not add custom CSS, custom theme files, or Elementor Theme Builder work to chase the prototype.
- Do not embed, port, or deploy this Vite app on WordPress.

## Locked stack

| Layer | Choice |
|---|---|
| Host | WP Engine (staging first, then production) |
| Theme | Astra (free). Astra Pro is optional. |
| Page builder | Elementor (free). Elementor Pro is optional. |
| Starter | **Non-Profit Organization** — `non-profit-organization-04` (premium) |
| Demo | https://websitedemos.net/non-profit-organization-04/ |
| Listing | https://wpastra.com/templates/non-profit-organization-04/ |

Import the **Elementor** version of Non-Profit Organization 04 on a **clean** WP Engine staging site. One import. Do not mix starters. This starter requires Premium Starter Templates (Astra paid plan).

The React wires in this repo now follow that starter’s section patterns (hero + 01/02/03, about split, impact counters, donate CTA band, story cards, partner row).

### Why Non-Profit Organization 04

Chosen as the production starter. It ships Home, About Us, Our Work, Stories, Donate, and Contact — enough layouts to duplicate for the 15-page SOW without designing new templates.

### Do not use these starters

- `elderly-care-02` — earlier candidate; do not mix it with 04
- `charity-02` — handwritten type, campaign colors, wrong voice
- `communities-02` — donate band on every page
- `general-hospital-04` — clinic/appointment site; Health is one program, not the brand

## Import rules

1. Fresh WP Engine staging. Never import a starter onto a site that already has pages.
2. Install Astra, then Premium Starter Templates. Choose Non-Profit Organization 04 → Elementor.
3. Decline plugins you will not use (SureCart, LatePoint, etc.) unless GSM is actually taking donations or bookings on-site.
4. After import, change only: logo, colors, type, menus, and content.
5. Duplicate existing layouts. Do not design new page templates.

## What goes where

**Astra Customizer (once, site-wide)**

- Colors, typography, container width
- Header: logo + nav + Support GSM button → `/support-gsm`
- Above-header bar: “A Place to Belong. A Life to Thrive. Support our Mission →” `/support-gsm#ways-to-give` (was the “Now Hiring — Direct Service Providers” careers bar; Erin changed it 2026-11-05. Copy is the client-approved Top Banner line from the content document.)
- The above-header bar is restyled by Additional CSS at `max-width: 921px` into a two-line stack with a white pill CTA. The pill is `min-height: 44px` and 14px to match the site's tap-target and type standard — keep both if you touch that block, and reset the bar to the inline underlined link at ≥922px.
- Footer: contact, quick links, newsletter, Facebook, Privacy, Accessibility, copyright
- Sticky header

Do **not** rebuild header or footer in Elementor.

**Elementor (page canvases only)**

- Home, About, Programs landing, four program pages, Support GSM cluster, Events, Newsletters, Careers, Contact
- Reuse imported layouts: Our Work for program pages, Stories for News, Donate for Ways to Give / Endowment, Contact for Careers extras as needed

**WordPress native**

- News & Updates = Posts + category archive (`/news`)
- Jobs = Careers page sections, or posts in a `jobs` category — not a custom plugin unless required
- Contact + newsletter = starter/Elementor forms wired to a real destination
- Privacy = a simple page (does not count against the 15)

**Astra Pro** — buy only for above-header banner, Programs dropdown, or header button if free Astra cannot do them cleanly.

**Elementor Pro** — skip unless Theme Builder or popup forms become necessary. They should not.

## The 15-page SOW (14 pages built)

Canonical source in this repo: `src/pages/SitemapPage.jsx`.

**Vocational Program is gone.** Client direction 2026-11-06: its content now lives inside Community Day Services (the `vocational-classroom` section), so there are 14 main pages — one under the SOW cap. Page 2089 is a **draft** and `/programs/vocational/` 301s to `/programs/community-day-services/#vocational-classroom` (rule in `mu-plugins/gsm-redirects.php`). Do not resurrect the page or re-add it to a menu.

| # | Page | Slug | Notes |
|---|---|---|---|
| 1 | Home | `/` | Gateway |
| 2 | About Us | `/about` | Sections: History; Mission, Vision & Values; Affiliations; Accessibility |
| 3 | Programs & Services | `/programs` | Landing |
| 4 | Community Day Services | `/programs/community-day-services` | Sections: the seven CDS classes + Additional Activities; Digital Den is the `#digital-den` section; absorbs the old Vocational content |
| 5 | Residential Living | `/programs/residential-living` | Sections: personalized support, leadership, staff, comfort/safety, communications, history, closing |
| 6 | Health & Well Being | `/programs/health-well-being` | Sections: supporting health, McAllister Infirmary, nursing, voice in care, consistent support, community care, closing |
| 7 | Community Engagement | `/programs/special-olympics` | Was the Special Olympics page; keeps that locked slug. Special Olympics is now a section. Sections: outings, Special Olympics, arts, outdoors, volunteering, GSM events |
| 8 | Support GSM Foundation | `/support-gsm` | Merged: GSM Foundation + Ways to Give (Erin feedback). Numbered cards + jump bar with sections for Foundation, Ways to Give, Endowment, Events. Memorial/tribute gifts live inside Ways to Give. |
| 9 | Shepherd Endowment Society | `/shepherd-endowment-society` | Real copy in `src/data/endowment.js` (from production site) |
| 10 | Events | `/events` | Real copy. Numbered cards + sections: Fall Festival, Golf Invitational, Brunch Auction, Community & Family Events |
| 11 | News & Updates | `/news` | Blog hub (counts as a page) |
| 12 | Newsletters & Family Resources | `/newsletters` | Real copy: The Messenger signup + Recent Issues archive (3 issues). PDFs still placeholders |
| 13 | Careers | `/careers` | Real copy. Sections: intro feature, Benefits, Our Culture, Job Openings (DSP + RSD), Apply Today. Images pending (In-Progress) |
| 14 | Contact Us | `/contact` | Real copy. Form, staff directory, map link, Thank a Staff Member. Facebook is the only social profile GSM maintains |

Utility (not in the 14): `/privacy`. Accessibility lives on About (`/about#accessibility`) and in the footer.

Programs is a **parent page** with four children, in this order — Community Day Services, Residential Living, Health & Well Being, Community Engagement — so breadcrumbs read `Home › Programs › Residential Living`. The header dropdown, the program-page sidebar, the Programs landing cards and the homepage cards all use that same order (client direction 2026-11-06). Keep them in sync.

Do **not** publish the React `/sitemap` diagram. It is a project artifact.

### Sections vs pages

These are sections, not extra pages: History, Mission/Values, Affiliations, Accessibility, Digital Den, Health subtopics, event types, job openings/benefits, contact form/directory/map/thank-a-staff.

Phase 2 may promote a section to a page. Keep the original hash when promoting so old links still work.

## Starter page remap

| Imported 04 page | Becomes |
|---|---|
| Home | Home — swap copy and photos only |
| About Us | About Us |
| Our Work | Programs landing, then **duplicate four times** for the four programs |
| Stories | News & Updates |
| Donate | Ways to Give |
| Contact | Contact Us |

Duplicate those same layouts for GSM Foundation, Endowment, Events, Newsletters, and Careers. Do not start blank Elementor canvases.

Homepage spec is **`src/pages/HomePage.jsx`** (Figma `9137:3182`) — *not* the older `9009:2` wire (`design/node-9009-2.png`). Client decision 2026-10-02: the React proto wins; the 9009:2 order below it is superseded. Live page is **315**, built with Elementor.

**Page 315 is generated, not hand-built.** `_tools/build_home_replica.py` emits the page as native Elementor containers + heading / text-editor / button / image widgets (no raw HTML, no custom CSS on the page), so it stays editable in the Elementor editor:

```sh
python3 _tools/build_home_replica.py                 # writes /tmp/home_replica.json
./_tools/apply_elementor.sh 315 /tmp/home_replica.json
```

**Every other content page is generated by `_tools/build_pages.py`**, which shares `_tools/elementor_kit.py` with the home builder:

```sh
python3 _tools/build_pages.py all                    # /tmp/page_<id>.json for all 13
python3 _tools/build_pages.py 2088                   # just Community Day Services
./_tools/apply_elementor.sh 2088 /tmp/page_2088.json
```

Page IDs in the script: 316 About, 317 Programs, 2088 Community Day, 2127 Community Engagement, 2090 Residential, 2091 Health, 2092 Support GSM, 2093 Endowment, 2094 Events, 318 News, 2095 Newsletters, 2096 Careers, 319 Contact. (2089 Vocational is a draft — it has no builder entry.) Copy is read from `_tools/page_data.json` (a JSON dump of `src/data/*.js`); regenerate it when the data files change.

Contact embeds two SureForms forms by ID — **2056** (Simple Contact Form → “Send Message”) and **2370** (Thank a Staff Member → “Send thanks”). The builder references them with the `sureforms_form` widget, so editing a form in SureForms updates the page without touching the script.

Edit the scripts and re-apply when the wire changes, rather than editing pages in Elementor and letting the two diverge. Key conventions baked in: `content_width: 'full'` on anything with a `width`, `flex_*` prefixes for flex settings, `_element_id` for anchors, and responsive `typography_font_size_tablet/mobile` mirroring the wire's `clamp()` scale (h1 64 → 44 → 40; section h2 44/48 → 36).


Section order:

1. Hero — Figma `9046:787` (photo overlay, one CTA). Headline: “A Community of Compassion, Dignity, and Purpose.” CTA: **“Learn more” → `/about`** (the React wire is authoritative; an earlier “Now Hiring! Apply Today” CTA lives in the above-header banner, not the hero). Button uses GSM blue, not 04 lime. **Every page uses the hero header** (transparent at top, white on scroll) — `PageHero` renders the shared `.home-hero` photo-overlay hero, and the slug list is `HERO_HEADER_PATHS` in `src/data/header.js`. The sitemap artifact (`/sitemap`) keeps its own header.
2. Intro strip — Figma `9046:813` overlapping the hero (3 cards, white card with 1px dividers, pulled up 160px): 01 Get Involved → `/events` / 02 Donate → `/support-gsm` / 03 News You Can Use → `/news`, Learn more.
3. Our Impact — Figma `9046:948`: “Our Mission & Vision: Serving with Dignity” + mission statement + 4 counters (**55+** years / 100+ men / **2** core programs / 1971 founded). Heading left / statement right, then the counters. No eyebrow label above the h2, no donate band.
4. Our Programs & Services — **4** cards, in client order (2026-11-06): Community Day, Residential Living, Health & Well Being, Community Engagement, + View all. **Community Engagement** is the page at `/programs/special-olympics`; Special Olympics is a section there. Vocational is not a page and not in this row.
5. About Us / Mission — eyebrow → **real `<h2>`** (“…for over 55 years.”) → one paragraph → bordered Read More, staggered 4-image mosaic. The heading must be `header_size: h2`, not `p` — otherwise the section has no heading element at all.
6. Stories — “What's Happening at GSM” + 2 story cards. **Not in the proto; kept by client decision 2026-10-02** for events promotion. Sits above the foundation section.
7. Support GSM Foundation — 4 cards: 01 GSM Foundation → `/support-gsm`, 02 Events → `/events`, 03 Shepherd Endowment Society → `/shepherd-endowment-society`, 04 Memorial or Tribute → `/support-gsm#ways-to-give` (no standalone memorial section). `#fafcfe` background, centered h2.

Home does **not** get `gsm_cta_band`, and the Get Involved (Donate/Volunteer/Careers) block was removed — client decision 2026-10-02. Every other content page keeps `gsm_cta_band`. Do not re-add either to page 315.

Header nav: About, Programs & Services, Support GSM, News & Updates, Careers, Contact + Support GSM button (About and Programs & Services carry dropdowns, as in WordPress).

### Elementor: container width needs `content_width: 'full'`

Elementor only prints `--width` when the container's `content_width` is `'full'` — see the `width` control's `'condition'` in `wp-content/plugins/elementor/includes/elements/container.php`. A card with `width: 20%` and no `content_width` renders at the default `100%` and stacks vertically, silently. Every card in a horizontal row on Home (and any new one) must set `content_width: 'full'`. This cost a full debug cycle on page 315.

### Responsive layout: three fixed breakpoint traps

All three were found by resizing real pages, not by the overflow sweep — the
automated check reported "no issues" because none of them widen the document.

| Band | Trap | Fix (already applied) |
|---|---|---|
| any | Elementor's **Sticky** setting on the program sidebar pins it with `position: fixed` and keeps it on top of the newsletter band after the article ends | sidebar carries no Elementor sticky; Additional CSS does `position: sticky` at `min-width: 1025px`, which stops at the article row |
| 768–921 | the program row kept `calc(100% - 296px)` for the article and a 240px sidebar, so the column scrolled away and left a 296px dead gutter with 205px gallery tiles | `flex_direction_tablet: column` on `pg_body`, both columns `width_tablet: 100%` |
| 923–1010 | logo + six nav items + the Support GSM button have a hard minimum of 1008px, so the page scrolled sideways at tablet widths | Additional CSS hides the duplicate header CTA in `923–1024px`; the nav's own Support GSM item covers it |

The nav container does not shrink with its type size — at 13px/5px padding it
still bottomed out at 952px — so shrinking text is not a fix for that band.

### Elementor: flex settings need the `flex_` prefix

Same silent failure, different keys. Flex is a **group control**
(`Group_Control_Flex_Container`, `includes/controls/groups/flex-container.php`) whose
fields are stored with a `flex_` prefix. Elementor accepts the bare names into
`_elementor_data` and then emits no CSS for them at all.

| Dead key | Real key |
|---|---|
| `justify_content` | `flex_justify_content` |
| `align_items` | `flex_align_items` |
| `align_content` | `flex_align_content` |
| `wrap` | `flex_wrap` |
| `gap` (`{unit,size}`) | `flex_gap` (`{unit,size,row,column,isLinked}`) |
| `css_id` | `_element_id` (container.php:1770) |

Symptom: a `space-between` table row renders run-on
(`Member LevelsCurrent GiftDeferred Gift`); a "centred" CTA band hugs the left edge
with the button touching the headline. `flex_direction` was never affected, so rows
still laid out horizontally — which is what makes it easy to miss.

**Do not "fix" the dead keys on Home (315).** `prog_row`, `story_row`, `support_row`
and `support_card_*` carry dead `justify_content`/`gap` and are correct *because* they
are inert: 5 cards at `width:20%` plus a `gap` exceeds 100% and would wrap. Only
`gsm_cta_band` (14 pages) was migrated — see `PLAN.md` §6.7.

## Support GSM Foundation wire (`/support-gsm`)

**Merged page:** GSM Foundation + Ways to Give combined into one page per Erin feedback. The page uses a **tab-style jump bar** that scrolls to **stacked anchor sections**. The `SectionTabs` component renders four jump links labelled from each section's `eyebrow`; clicking smooth-scrolls to the matching `#id` anchor and the active tab highlights via scroll-spy. Content is fully stacked via `SplitSection`. Section data lives in `src/data/getInvolved.js`.

Section order:

1. **Hero** — breadcrumb "Support GSM", title **GSM Foundation** (client content matrix 2026-11-04; the page is still named "Support GSM Foundation" in nav and metadata), real lede about the Foundation founded in 1981. `PageHero` + transparent header.
2. **Numbered cards** — `HomeIntroStrip variant="involved"` with `foundationIntroColumns`: 01 Donate → `#ways-to-give`, 02 Volunteer → `#events`, 03 Make A Lasting Impact → `/shepherd-endowment-society`. Hash targets render as native anchors so they scroll (React Router `Link` does not).
3. **Jump bar** — `SectionTabs` **sticky** just below the header once you scroll. Four scroll-to links: GSM Foundation, Ways to Give, Shepherds Endowment Society, Events. Active link gets a blue underline.
4. **GSM Foundation** — `SplitSection` `#foundation`: copy left, image right. Eyebrow + title "Supporting the Manor for over 45 years" (Foundation founded 1981).
5. **Ways to Give** — `#ways-to-give`, **flipped** (image left). Title "Every gift stays on campus". Copy covers the three signature events, Christmas Appeal, general gifts, Family Donor Program, tribute and memorial gifts, and the Endowment Society. The "Ways to Give →" CTA links to the Qgiv giving form that backs the live Foundation donation page (`https://secure.qgiv.com/for/wdof/`, external, opens in a new tab).
6. **Shepherds Endowment Society** — `#endowment-society`, normal split. Title "Your Legacy. Their Future."; link → `/shepherd-endowment-society`.
7. **Events** — `#events`, **flipped**. Bullets: Fall Festival, Golf Invitational, Brunch Auction, Community & Family Events. Link → `/events`.
8. **Global Support GSM CTA** — `GetInvolvedCta` in `Layout.jsx` (blue band before footer newsletter, title updated to "Support GSM Foundation"). Not duplicated on the page canvas.

**Memorial/Tribute is no longer its own section or tab** (client content matrix 2026-11-04). Memorial and tribute gifts are described inside Ways to Give, so the header dropdown and footer "Memorial or Tribute" links now target `/support-gsm#ways-to-give`.
### Reusable section modules (React wires)

Extracted from About and reused on inner pages — **do not** invent new layout patterns when these fit:

| Component | Use for |
|---|---|
| `PageHero` | Shared photo-overlay hero on all pages in `HERO_HEADER_PATHS` |
| `HomeIntroStrip` | Overlapping 3-card strip (`home` / `about` / `involved` / `page` variants) |
| `AboutMissionSection` | Photo mosaic + copy (About hero overlap; optional eyebrow/title props) |
| `SplitSection` | Eyebrow + h2 + copy + image placeholder; `flip`, `alt`, `softImage`, optional link |
| `SectionTabs` | Sticky tab-style jump bar that scrolls to stacked anchor sections + scroll-spy (Support GSM Foundation landing) |
| `HistoryTimelineSection` | Horizontal scroll timeline (`src/data/history.js`) |
| `AffiliationsSection` | Partner pills split |
| `ProgramsIntroSection` / `ProgramsServicesSection` | Programs landing |
| `ImpactSection` | Home impact counters |
| `GetInvolvedCta` | Site-wide blue CTA band in `Layout` |

Data files: `src/data/getInvolved.js` (Support GSM landing jump-bar sections), `src/data/endowment.js` (Endowment page copy), `src/data/history.js`, `src/data/placeholders.js` (lorem), `src/data/header.js` (nav + hero-header slugs).

## URLs that must not be used

The React prototype has leftover hash URLs. They are wrong. Use the table above.

| Wrong (prototype) | Right |
|---|---|
| `/programs#health` | `/programs/health-well-being` |
| `/programs#community-day` | `/programs/community-day-services` |
| `/programs#vocational` | `/programs/community-day-services#vocational-classroom` (page retired; old URL 301s there) |
| `/programs/special-olympics` (new) | `/programs/special-olympics` |
| `/programs#residential` | `/programs/residential-living` |
| `/support-gsm#events` | `/events` |

## Global chrome

Header nav (6 items): **About** (dropdown → About Us, Mission, Vision & Values, Our History, Affiliations, Accessibility), **Programs & Services** (dropdown → Programs & Services + the five program pages), **Support GSM** (dropdown → GSM Foundation, Events, Shepherd Endowment Society, Memorial or Tribute), **News & Updates** (plain link to `/news` — no dropdown), Careers, Contact. Plus Support GSM button → `/support-gsm`. `/newsletters` is deliberately **not** in the header on either side; it is reached from page content (client call, 2026-11-05).

The header nav and the React wire's `NAV_ITEMS` are kept identical — same labels, same order, same targets — including the `#foundation` / `#ways-to-give` hashes. `_tools/verify_site.php`-style checks aside, when you change one, change the other the same day. Menu item padding is `header-menu1-menu-spacing` desktop `10px` (tablet `12px`); the six items plus the About caret overflow the header and wrap Contact onto a broken second row at ≥1280 when it is left at the Astra default of `16px`.

Footer: phone `(815) 472-3700`, P.O. Box 260, 4129 N. State Route 1-17, Momence, IL 60954; quick links; newsletter (real list, labeled field); Facebook `https://www.facebook.com/goodshepherdmanormomence/` (the client's own legacy `facebook.com/pages/Good-Shepherd-Manor/121959794503212` redirects here — `goodshepherdmanor` is a different, unused page); Privacy; Accessibility; `© 2026 The Good Shepherd Manor`. In WordPress the footer is two columns — free Astra caps it there.

## Design tokens (Astra Customizer only)

Set once. Do not restyle per page in Elementor.

Astra 04 layout, GSM blue as the primary (replace 04 lime in Customizer).

| Token | Astra var | Value |
|---|---|---|
| Accent / buttons | `--ast-global-color-0` | `#0089DF` |
| Accent hover | `--ast-global-color-1` | `#006BB3` |
| Headings | `--ast-global-color-2` | `#002A4E` |
| Body text | `--ast-global-color-3` | `#303336` |
| Alternate background | `--ast-global-color-4` | `#FAFCFE` |
| White / header / footer | `--ast-global-color-5` | `#FFFFFF` |
| Muted | `--ast-global-color-6` | `#C8D4E0` |
| Rules | `--ast-global-color-7` | `#000000` |
| Font | | DM Sans |
| Container | | 1200px |

Home uses Astra’s transparent header over the hero (white type, white logo). Inner pages use a solid white header and navy type. While the mobile menu is open (`body.ast-main-header-nav-open`), Additional CSS forces that header bar solid white and swaps the logo to `gsm-logo-color.svg` so the white logo is not left sitting on the hero photo. Footer columns are the Astra builder; the newsletter band above them is a separate Elementor template (below).

### Contrast: use `#006BB3` for blue text and button fills

`#0089DF` on white is **3.59:1**, and white on `#0089DF` is the same — both fail WCAG AA for body-size text (4.5:1). The React wire therefore keeps `#0089DF` only for decorative fills and graphics, and uses two derived tokens for anything readable:

| Token | Value | Ratio on white |
|---|---|---|
| `--ast-color-link` | `#006BB3` | 5.46:1 |
| `--ast-color-link-hover` | `#004F85` | 7.9:1 |

Applied to: `.text-link`, card/CTA links, eyebrows and labels in the article sidebar, timeline years, breadcrumb hover, primary buttons (`.btn--primary`, `.home-btn--blue`, `.header__donate`), and the skip link (navy background). The above-header banner keeps a light blue `#9FD0FF` (7:1) on navy. The required-field asterisk is `#B42318`.

**When the site moves to WordPress:** set the Astra *button* and *link* colours to `#006BB3` in the Customizer (or accept AA failure). This is a client decision — the brand accent stays `#0089DF` for graphics.


## Content sources in this repo

Use these for copy, section order, and IA. Do not treat their CSS as a spec.

| File | Use for |
|---|---|
| `src/pages/SitemapPage.jsx` | 15-page IA, sections, SOW notes |
| `src/pages/HomePage.jsx` | Homepage spec — Figma `9137:3182` (wins over the `9009:2` wire) |
| `design/node-9009-2.png` | Shared homepage wireframe export — **superseded by `HomePage.jsx`** (reference only) |
| `design/figma-node-6-124.png` | Support GSM Foundation wire export (legacy Figma node) |
| `src/pages/FoundationPage.jsx` | Support GSM Foundation merged page (`/support-gsm`) — combined GSM Foundation + Ways to Give |
| `src/pages/*.jsx` | Remaining 15-page wires (About through Contact) |
| `src/data/getInvolved.js` | Support GSM landing split-section content + IDs |
| `src/data/endowment.js` | Shepherd Endowment Society page copy (real) |
| `src/data/history.js` | About timeline entries |
| `src/data/site.js` | Shared stats, program cards, news, jobs |
| `src/data/programs.js` / `src/data/health.js` | Program page copy and section IDs |
| `src/data/header.js` | Nav items, hero-header slug list, active-state helpers |
| `src/styles/starter.css` | Shared 04-style layout classes (not a WP spec) |
| `src/components/Layout.jsx` | Nav labels, footer contact, above-header banner, Donate, `GetInvolvedCta` |
| `src/components/ProgramPage.jsx` | Program page **section order** only |
| `design/sitemap-structure.md` | Figma extract (older; SitemapPage wins on conflicts) |

> **Current state (client review round):** Descriptive body copy is placeholder **lorem ipsum** (Home, About, Support GSM Foundation, news article bodies, and the global CTA band). Keep headings, titles, slugs, eyebrow labels, contact data, structured lists (e.g. Endowment gift methods/levels), and timeline years as-is; only paragraph/body prose is placeholder. Replacing with real copy awaits client review. **Exceptions — fully real copy:** `/shepherd-endowment-society` (sourced 2026-10-02 from the client's own production page `goodshepherdmanor.org/foundation/shepherds-endowment-society/`; `src/data/endowment.js` matches it), `/programs/community-day-services` (client-supplied 2026-11-04; `src/data/programs.js` `communityDay`), `/programs/residential-living` (client-supplied 2026-11-04; `src/data/programs.js` `residential`), `/programs/health-well-being` (client-supplied 2026-11-04; `src/data/health.js`), `/programs/special-olympics` (client-supplied 2026-11-04; `src/data/programs.js` `communityEngagement` — the page is presented as Community Engagement), `/events` (client-supplied 2026-11-04; `src/pages/EventsPage.jsx`), `/careers` (client-supplied 2026-11-04; `src/data/careers.js`), `/newsletters` (client-supplied 2026-11-04; `src/pages/NewslettersPage.jsx`), `/contact` (client-supplied), and the `/news` hub page furniture (client-supplied 2026-11-04; `src/pages/NewsPage.jsx` + `site.js` `newsItems` — article bodies are still lorem). Use those as the reference for other real GSM prose.

Health & Well Being is the first program to build. Its section IDs: `supporting-health`, `mcallister-infirmary`, `nursing`, `voice-in-care`, `consistent-support`, `community-care`, `closing`. These replace the earlier placeholder anchors (`clinic`, `pharmacy`, `supports`, `transportation`); production page 317 still carries those until it is rebuilt from this content.

Community Day Services is fully real copy (client-supplied 2026-11-04). Its section IDs: `economics`, `personal-living-skills`, `digital-den`, `civic-engagement`, `physical-fitness`, `vocational-classroom`, `seniors`, `activities`. The `/news/digital-den-community-day` article keeps `#digital-den` pointing here.

Residential Living is fully real copy (client-supplied 2026-11-04). Its section IDs: `personalized-support`, `leadership`, `our-team`, `comfort-safety`, `staying-connected`, `history`, `making-home-happen`.

Community Engagement is fully real copy (client-supplied 2026-11-04) and lives at the locked `/programs/special-olympics` slug — the home card and nav already label it Community Engagement. Its section IDs: `following-interests`, `special-olympics`, `arts`, `outdoors`, `giving-back`, `gsm-events`. CDS, Community Engagement, Residential, and Health all list their sections in `ArticleSidebar` via `SECTIONS_BY_PATH`; `site.js` `programs` must include a page for its sidebar entry to appear.

## Handoff: current build state (read this first)

**Where things are**

| Thing | Location |
|---|---|
| WordPress site (canonical) | Local by Flywheel, `~/Local Sites/goodshepherd`, https://goodshepherd.local |
| Search-replace target for stage | `goodshephe3dev.wpenginepowered.com` |
| React wire (source of truth for content) | this repo, `src/` |
| Elementor page generators | this repo, `_tools/` |
| WP-CLI wrapper | `~/Local Sites/goodshepherd/_tools/wp.sh` — **outside the repo**, see below |

**All 15 SOW pages plus Privacy are built** in Elementor on Local, generated from the React wire. Nothing on the WordPress side is hand-drawn: it is all native containers + heading / text-editor / button / image / icon-list widgets.

```
_tools/elementor_kit.py        shared helpers (px, gap, heading, text, button, image, section)
_tools/build_home_replica.py   page 315
_tools/build_pages.py          every other page (`all`, or a single page ID)
_tools/page_data.json          JSON dump of src/data/*.js — copy source for the generators
_tools/refresh_page_data.sh    regenerates page_data.json from src/data
_tools/apply_elementor.sh      applies a JSON file to a post + clears Elementor caches
```

Rebuild loop:

```sh
./_tools/refresh_page_data.sh                 # only after editing src/data/*.js
python3 _tools/build_pages.py all             # -> /tmp/page_<id>.json
./_tools/apply_elementor.sh 2088 /tmp/page_2088.json
```

**Page IDs:** 315 Home · 316 About · 317 Programs · 2088 Community Day · 2127 Community Engagement · 2090 Residential · 2091 Health · 2092 Support GSM · 2093 Endowment · 2094 Events · 318 News · 2095 Newsletters · 2096 Careers · 319 Contact · 3 Privacy (plain content, not generated) · 2089 Vocational (draft, 301s to CDS).

**Forms** (SureForms, referenced by ID — editing a form updates the page, no rebuild needed):
- **2056** Simple Contact Form → “Send Message”
- **2370** Thank a Staff Member → “Send thanks”
- **2202** Newsletter Signup → “Sign Up”. The site-wide band is the Elementor section template **Newsletter band** (post **2375**, Templates → Saved Templates). Astra’s above-footer HTML (`astra-settings` → `footer-html-1`) is only `[elementor-template id="2375"]`. Edit the heading, lede, and form widget in that template. Do not replace the shortcode with raw HTML (`_tools/wire_forms.php` will not). The glass pill, blue glow, and vertically centered field text are Additional CSS scoped to `.elementor-element-nlband` and `.elementor-element-nlright`. Newsletters embeds form 2202 with a **SureForms Form widget** (`srfm_form_block: 2202`), not a shortcode, so it is editable in Elementor like any other widget.

**Media:** the client's live media library was imported (209 attachments as of 2026-11-04): program photography, `/dollars-at-work/` set, golf galleries, event flyers, plus four pre-cropped mosaic images (2371–2374) at the wire's ratios. Real GSM photos are used everywhere; the Unsplash stand-ins exist only in the React prototype.

**Tooling that lives outside the repo.** `apply_elementor.sh` expects `~/Local Sites/goodshepherd/_tools/wp.sh`; it is not committed. Recreate it if missing:

```sh
# PHP ships with Local; WP-CLI does not
curl -sSLo ~/Local\ Sites/goodshepherd/_tools/wp-cli.phar \
  https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
# wrapper: Local PHP + per-site MySQL socket, see the file itself
```
The socket is `~/Library/Application Support/Local/run/<id>/mysql/mysqld.sock`; the wrapper discovers it.

**Gotchas that already cost time**
- A stray `app/public/.maintenance` file appears after some WP-CLI runs and puts the whole site into a 503. Delete it.
- Elementor caches `_elementor_element_cache`, `_elementor_css` and `uploads/elementor/css/post-<id>.css`. Always apply through `apply_elementor.sh`, never `wp post meta update` directly.
- Additional CSS (`wp_posts` ID 2078, `wp_get_custom_css`) still has a global `.srfm-submit-button { border-radius: 8px !important }`. The newsletter pill wins only because `.elementor-element-nlright .srfm-submit-button` is more specific and also uses `!important`. Old `.gsm-signup` rules are dead; do not add new ones.
- The mobile drawer lives inside `.header` (z-index 100) — the above-header banner must not cover the drawer's close button. In practice the bar sits above the header in normal flow (Additional CSS gives it `z-index: 101`), so they never overlap; measured at 360px and 390px with the menu open, the bar ends at 85px, the close button starts at 109px, a 24px gap. Re-check that gap if you change the bar's padding or stack it further.

**Well-known content gaps (not build bugs)**
- ~~Vocational (2089) is lorem in both React and WordPress — waiting on the client.~~ Resolved 2026-11-06: the page is retired (draft) and its content lives in Community Day Services.
- “Apply for Clinical Service Provider →” under the RSD posting is the client's verbatim text; likely a copy-paste slip, left as supplied.
- Newsletter archive entries are placeholders — the client's site has no 2025/2026 issues.
- Contact has Facebook only. No Instagram or LinkedIn profile exists.
- The map is a “Open in Google Maps” button, not an embedded map (Local has no Maps API key).

**Do not** hand-edit generated pages in Elementor and expect it to survive: change the script and re-apply, or accept the drift and stop using the generator for that page.

**Verifying a change** (the loop used while building these pages):

```sh
# 0. assert the documented state: page IDs/slugs, builder mode, form IDs and
#    recipients, newsletter template + footer slot, the 28 program anchors,
#    /news links, image files on disk. Exits non-zero on any failure.
./_tools/wp.sh eval-file _tools/verify_site.php

# 1. every route returns 200
for p in "" about programs support-gsm events news newsletters careers contact privacy; do
  printf '%-14s ' "/$p"; curl -sk -o /dev/null -w '%{http_code}\n' "https://goodshepherd.local/$p/"
done

# 2. no horizontal scroll at 390 / 1024 / 1440, plus a full-page screenshot
#    (Playwright MCP: contexts need ignoreHTTPSErrors:true for .local)
```

`verify_site.php` finds the repo through `GSM_REPO`, falling back to
`$HOME/Developer/goodshepherd`. Point it elsewhere on another machine.

A page is "done" when it renders at 1440/1024/390 with no horizontal overflow, the H1 is correct, and every image resolves.

The last full pass (2026-11-04) checked all 16 pages at **320 / 360 / 390 / 768 / 921 / 922 / 1024 / 1440** with no overflow anywhere.

## Build order (WordPress)

1. Import Non-Profit Organization 04 on staging
2. Astra globals: colors, type, logo, header, above-header banner, footer, menus
3. Create the 15 pages with the slugs above (empty is fine)
4. Home — swap copy into the imported layout
5. Duplicate Services → Health & Well Being, then the other three programs
6. About, Contact, Careers
7. Support GSM, Ways to Give, Endowment, Events
8. News (posts) + Newsletters
9. Wire forms, real Facebook URL, Accessibility, staging QA
10. 301s on WP Engine if this replaces the current GSM site, then production

## Working in this React repo

This app is a clickable wire. Further React work is optional and should stay thin.

- Keep the 15-page IA and the locked slugs if you add pages.
- Keep visual tokens in `src/styles/tokens.css`. Primary is GSM blue `#0089DF`, not the 04 lime.
- Do not add routes, components, or comments that invent a different sitemap.
- `/sitemap` is for stakeholders. Production will not have it.
- Do not commit `.env` secrets or copy them into docs.

Local: `npm install` then `npm run dev` (default http://localhost:5173). Use `npm run dev -- --port 5174` if the preview is stuck on stale HMR.

## Deployment: Local is canonical

**Local is the source of truth. Stage is a rebuilt copy — never edit stage directly.**
Edits go into Local, get verified, then the database is pushed to WP Engine stage.

| Env | URL |
|---|---|
| Local | https://goodshepherd.local |
| WPE stage | https://goodshephe3dev.wpenginepowered.com |

### Push sequence

1. **Export.** `_tools/wp.sh db export` does not work in this environment. `mysqldump` is not on PATH, and once it is, it does not inherit the socket the wrapper sets for PHP — it fails with `Can't connect to local MySQL server through socket '/tmp/mysql.sock'`. Drive Local's own mysqldump with a throwaway client config instead:

   ```sh
   SOCK="$(find "$HOME/Library/Application Support/Local/run" -maxdepth 3 -name mysqld.sock | head -1)"
   DUMP="$(find "$HOME/Library/Application Support/Local/lightning-services" -maxdepth 5 -path '*bin/mysqldump' | head -1)"
   printf '[client]\nsocket=%s\nuser=root\npassword=root\n' "$SOCK" > /tmp/gsm_my.cnf && chmod 600 /tmp/gsm_my.cnf
   "$DUMP" --defaults-extra-file=/tmp/gsm_my.cnf --single-transaction --quick \
     --default-character-set=utf8mb4 local > /tmp/gsm_export.sql
   ```

   Sanity check: the dump is ~24 MB for the current library.

2. **Do NOT sed the dump.** Rewriting `goodshepherd.local` → `goodshephe3dev.wpenginepowered.com` with `sed` **changes string lengths inside serialized option values**, so those arrays stop unserializing. Astra then silently rewrites `astra-settings` from defaults: the option drops from 2,291 keys to the 4 queue keys (`theme-auto-version`, `is_theme_queue_running`, `astra-addon-auto-version`, `is_astra_addon_queue_running`) and the above-header banner, colours, menu spacing and footer social URL all vanish. `theme_mods_astra` gets hollowed out the same way, and the result looks exactly like the object-cache trap below, which is what makes it expensive to find.

   Import the dump **unmodified** and let WP-CLI do a serialization-aware replace on the server, *after* the import:

   ```sh
   wp search-replace 'goodshepherd.local' 'goodshephe3dev.wpenginepowered.com' \
     --all-tables --precise --report-changed-only --allow-root
   wp cache flush --allow-root
   ```

   `--precise` re-serializes every affected value, so no string is left with a stale length. Expect **~2,400 replacements** for the current library (the count is printed at the end) — don't compare against a fixed number. Check `astra-settings` afterwards: `wp eval` it and confirm `count()` is ~2,291 and `header-html-1` is set.

3. `gzip -9 -c /tmp/gsm_export.sql > /tmp/gsm-raw.sql.gz`, then `gzip -t` (~2.6 MB)
4. rsync to `/sites/goodshephe3dev/gsm-raw.sql.gz`. The key is Local's `~/Library/Application Support/Local/ssh/wpe-connect`, used as `goodshephe3dev@goodshephe3dev.ssh.wpengine.net`; no `~/.ssh/config` is needed, just pass `-e "ssh -i \"$KEY\" -o BatchMode=yes"` to rsync.
5. Import with **`gunzip -c gsm-raw.sql.gz | wp db import - --allow-root`**. `wp db import file.sql.gz` does **not** decompress — it feeds gzip bytes to mysql and dies with `ASCII '\0' appeared in the statement`. Delete the dump from the webroot afterwards; it is publicly reachable.
6. Run the `search-replace` from step 2, then **`wp cache flush`**, `wp page-cache flush`, `wp cdn-cache flush`, `wp elementor flush-css`, then verify all 16 routes

### A database push does not carry files

The import replaces tables only. These live on the filesystem and must already be on stage or be copied separately:

| Not carried | Symptom if missing on stage |
|---|---|
| `mu-plugins/gsm-redirects.php`, `gsm-security.php`, `gsm-seo.php` | `/ways-to-give/` and `/donate/` 404 instead of 301; SureForms URLs return to the sitemap |
| `uploads/elementor/css/post-*.css` | pages serve stale CSS — flush and regenerate after the import |
| `uploads/` media | any photo added locally breaks on stage |
| plugin and theme files | the DB references widgets/options the stage code cannot render |

Before pushing, confirm stage runs the same versions as Local (Elementor 4.3.3, Astra 4.14.0, SureForms 2.12.8 at time of writing).

**Stage can be missing whole plugins.** A fresh stage may only carry Elementor, Premium Starter Templates (`astra-pro-sites`) and SureForms — which is not the stack Local runs. Check before importing, because `active_plugins` comes from the dump and WordPress silently skips files that are absent:

```sh
rsync -az --no-perms --no-owner --no-group -e "ssh -i \"$KEY\" -o BatchMode=yes" \
  plugins/<name>/ goodshephe3dev@goodshephe3dev.ssh.wpengine.net:/sites/goodshephe3dev/wp-content/plugins/<name>/
```

Local's stack on 2026-11-05: `astra-addon` 4.13.10, `elementor` 4.3.3, `elementor-pro` 4.3.1, `webp-converter-for-media` 6.6.5, `seo-by-rank-math` 1.0.279, `ga-google-analytics`, `sureforms` 2.12.8. Missing `astra-addon` costs you the transparent/sticky header and the above-header banner; missing `webp-converter-for-media` 404s every image that routes through the passthru.

Uploads are a separate rsync of `wp-content/uploads/` (additive, never `--delete`). Compare file counts afterwards with `find … -type f | wc -l` on both sides — stage had 325 files against Local's 1,223 before the last push.

### What an import changes on stage besides content

- **Users are replaced** by whatever exists on Local — currently a single `develop@cloudmellow.com` administrator. Anyone with a stage login loses it. Have that password to hand, and remember a reset email now goes to `info@goodshepherdmanor.org`, not to you.
- **`admin_email` becomes `info@goodshepherdmanor.org`**, so form submissions and password resets during staging QA reach GSM. Fine if the client expects it; warn them if not.
- **`blog_public` is `0`** on Local, so stage imports as `noindex, nofollow`. Harmless on stage, but **flip it back on production** or the live site ships invisible.

### Environment gotchas (each one cost real debugging time)

- **WP Engine has a persistent object cache. Flush it after every DB import, or stage will silently serve pre-import options.** This is the single most important step. Symptom: the database row is correct when inspected with raw SQL, but `get_option()` returns a stale/short value and the front end renders old markup.
- **WP-CLI is available on stage** at `/usr/local/bin/wp`. Use `wp --path=/sites/goodshephe3dev --allow-root`.
- **`webpc-passthru.php` is generated per site.** WebP Converter for Media's passthru loader bakes an allowlist of `home_url()` prefixes into `wp-content/webpc-passthru.php` (`PassthruLoader::activate_loader()`). Copying the file from Local with the uploads rsync leaves it allowlisting `goodshepherd.local`, so on stage every image that routes through the passthru returns 404 while direct `.jpg` URLs still work. Re-bake it after a domain change with `wp eval 'do_action("webpc_refresh_loader", true, false);'` (or by re-saving the plugin settings), then confirm the allowlist in the file mentions the stage host.
- **`scp` is blocked** for the `local+db+push+` user. Use an ssh config file for rsync (`IdentityFile` must be quoted — the key path has a space), and write remote scratch files over the shell instead of scp.
- **WPE `/tmp` is ephemeral per SSH session.** Anything that must persist goes in `/sites/goodshephe3dev`.
- **`sed` on the dump needs `LC_ALL=C`**, otherwise it dies with "illegal byte sequence".
- **Astra settings live in the `astra-settings` option** (a large serialized array), not `astra_options`. Verify with `count(get_option('astra-settings'))` — a value far below the Local count means a stale cache, not a bad import.
- **Free Astra has no 4-column footer.** The advanced footer (`footer-adv`, `advanced-footer-widget-1..4`) is Astra Pro. Free Astra renders only the small footer, which supports `footer-widget-1` and `footer-widget-2`. The GSM footer is consolidated into those two areas. Do not chase the 04 four-column layout.
- Enable those areas with `footer-sml-section-1` / `footer-sml-section-2` = `widget` and `footer-sml-layout` = `layout-1`.
- **Privacy lives at `/privacy/`**, not `/privacy-policy/`.

## Hard rules

- 15 main pages. No more.
- One starter, one import, one inner-page layout reused.
- No custom Astra child-theme CSS unless a real accessibility or header-offset bug requires a few lines.
- No Elementor Theme Builder header/footer.
- No new plugins without a concrete need (donations, jobs board, events calendar). Events is **one page with sections**, not The Events Calendar, unless the client will run many dated events.
- Do not invent pages, slugs, or nav items.
- Do not add extra pages beyond 15 or turn dropdown items into extra routes — they are four of the 15 SOW pages plus sections on `/support-gsm`.
- Support GSM Foundation uses a `SectionTabs` jump bar above stacked `SplitSection`s (client direction) — tabs scroll to anchors, all content stays visible. Do not replace the stacked content with hidden tab panels.
- Vocational was the approved scope cut and is now done: the page is a draft, `/programs/vocational/` 301s to the CDS vocational section, and no menu links to it.
- Purge WP Engine cache after Elementor edits.

## Conflicts

1. This file wins over chat history.
2. `src/pages/SitemapPage.jsx` wins over `design/sitemap-structure.md`.
3. Locked slugs in this file win over hash links in `HomePage.jsx` / `Layout.jsx`.
4. Non-Profit Organization 04 layout wins over React CSS when building WordPress.


## Figma MCP

Official remote server: `https://mcp.figma.com/mcp`. Read `FIGMA.md` before implementing from a Figma URL.
