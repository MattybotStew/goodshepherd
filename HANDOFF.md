# HANDOFF — Good Shepherd Manor (WordPress)

One page for whoever picks this up. Read `AGENTS.md` first; it holds the full context,
the 15-page IA, the design tokens and the environment gotchas. This file is the map of
**where things live** and **what is still a placeholder**.

Canonical environment: **Local by Flywheel**, `~/Local Sites/goodshepherd`,
`https://goodshepherd.local`. Local is the source of truth — never edit WP Engine stage.

---

## Where page content is edited

All 15 SOW pages are **Elementor canvases** built from native containers plus heading,
text-editor, button, image, icon-list and SureForms widgets. No raw HTML widgets, no
Theme Builder templates.

Edit them in **wp-admin → Pages → [page] → Edit with Elementor**. That is the normal
path for a non-developer: change a heading, swap a photo, edit a link, add a section.

| Page | ID | Slug |
|---|---|---|
| Home | 315 | `/` |
| About Us | 316 | `/about` |
| Programs & Services | 317 | `/programs` |
| Community Day Services | 2088 | `/programs/community-day-services` |
| Vocational Program | 2089 | `/programs/vocational` |
| Community Engagement | 2127 | `/programs/special-olympics` *(locked slug — do not rename)* |
| Residential Living | 2090 | `/programs/residential-living` |
| Health & Well Being | 2091 | `/programs/health-well-being` |
| Support GSM Foundation | 2092 | `/support-gsm` |
| Shepherd Endowment Society | 2093 | `/shepherd-endowment-society` |
| Events | 2094 | `/events` |
| News & Updates | 318 | `/news` |
| Newsletters & Family Resources | 2095 | `/newsletters` |
| Careers | 2096 | `/careers` |
| Contact Us | 319 | `/contact` |
| Privacy Policy | 3 | `/privacy` — **plain WordPress page, not Elementor** |

**Program pages have an “On this page” sidebar.** Each section starts at a heading widget
carrying an Elementor **CSS ID** (`supporting-health`, `nursing`, `digital-den`, …). If you
rename or delete a section, update the matching sidebar link in the same page or the jump
link will go nowhere.

**Blog = posts**, not Elementor. `wp-admin → Posts`. The `/news` hub page (318) has four
hand-written story cards; when you publish a new story, update those cards too — the hub
does not query posts automatically. Category archives are native.

Support GSM Foundation is a **stacked anchor page** (`#foundation`, `#ways-to-give`,
`#endowment`, `#events`) with a sticky jump bar. Do not convert it to hidden tabs.

---

## Where header and footer are edited

**Not in Elementor.**

- **Header, hiring bar, menu, Support GSM button** — Appearance → Customize → Header
  Builder (Astra). Logo, colours and DM Sans are in Customize → Global / Typography.
  Sticky/transparent header settings: Customize → Header Builder → Transparent Header.
- **Footer columns** — Appearance → Widgets → `footer-widget-1` … `footer-widget-4`
  (block widgets, in that visual order). Free Astra caps the footer at those areas.
- **Footer copyright + Privacy/Accessibility links** — Customize → Footer Builder →
  Copyright.
- **The newsletter band is not a footer widget.** Astra → Above Footer HTML contains one
  line: `[elementor-template id="2375"]`. Do not replace it with raw HTML.

## Newsletter template and form

| Thing | Where |
|---|---|
| Band layout + copy | wp-admin → **Templates → Saved Templates → “Newsletter band”** (post 2375), edit with Elementor |
| Band styling | Additional CSS, scoped to `.elementor-element-nlband` / `.elementor-element-nlright` only |
| Signup form | SureForms → **“Newsletter Signup”** (form 2202) — the only signup form on the site |

Form 2202 appears twice: inside template 2375 and on `/newsletters`. Both are the
`SureForms Form` widget bound to 2202, so editing the form updates both. Form title is
hidden. Submissions go to **info@goodshepherdmanor.org**.

**Contact forms on `/contact`** are also SureForms, embedded by ID:
**2056** Simple Contact Form (“Send Message”) and **2370** Thank a Staff Member
(“Send thanks”). Same inbox. Change a recipient in SureForms → Form → Email Notifications;
no code or CSS involved.

---

## The three must-use plugins

They live in `wp-content/mu-plugins/`, load automatically, and **do not appear in the
Plugins screen**. Do not move them into a normal plugin and do not delete them.

A copy of all three is tracked in this repo at `_migration/mu-plugins/` and is kept in
sync with the live site, so a fresh environment can be given them with `git checkout`
rather than a manual copy. If you change one in `wp-content/mu-plugins/`, copy it back
there or the two will drift.

| File | What it does |
|---|---|
| `gsm-redirects.php` | 301s `/ways-to-give/` → `/support-gsm/#ways-to-give`, `/donate/` → `/support-gsm`, `/sitemap.xml` → `/sitemap_index.xml`, plus old flat post URLs → `/news/<slug>/`. Local runs nginx, so `.htaccess` is not an option — this keeps the redirect table in version control. |
| `gsm-security.php` | Disables XML-RPC and pingbacks, adds security response headers (nosniff, frame options, referrer policy, HSTS), strips version fingerprints, rate-limits `wp-login.php`, blocks anonymous user enumeration. |
| `gsm-seo.php` | Keeps SureForms’ public `sureforms_form` post type out of the Rank Math sitemap and sets it `noindex, nofollow`, so form URLs never surface in search. |

## Additional CSS

Appearance → Customize → Additional CSS. Everything left is in use or is a deliberate
fallback: newsletter pill, program sidebar, tap-target overlay, footer/nav styling,
mobile nav, hero/CTA background fallbacks. Prefer editing the widget in Elementor over
adding rules here.

---

## Local → stage database push

The full sequence is in `AGENTS.md` § *Deployment: Local is canonical*. Summary:

1. `_tools/wp.sh db export /tmp/gsm_export.sql`
2. `LC_ALL=C sed -i '' 's#goodshepherd\.local#goodshephe3dev.wpenginepowered.com#g' /tmp/gsm_export.sql` (expect 26 replacements, 0 left)
3. `gzip -9` → `_migration/stage-db-final.sql.gz`, then `gzip -t`
4. rsync to `/sites/goodshephe3dev/gsm-import.sql.gz`
5. Import, **then `wp cache flush`** — WP Engine’s object cache will otherwise serve pre-import options
6. Delete the dump from the webroot, verify all 16 routes

`wp.sh` lives at `~/Local Sites/goodshepherd/_tools/wp.sh` and is **not in the repo**.
Recreate it from `AGENTS.md` if missing.

### Pre-launch checklist item

Search-engine visibility is **discouraged on Local** (`blog_public = 0`), so every page
carries `noindex, nofollow`. That value is in the database and travels with a push. **Set
Settings → Reading → “Discourage search engines” back off on production**, or the live
site will be invisible to Google.

---

## Licences the client must keep

| Service | Why |
|---|---|
| **WP Engine** | hosting (stage `goodshephe3dev`, then production) |
| **Astra Pro** | the header/footer builder, above-header hiring bar, transparent header, footer widgets |
| **Elementor Pro** | currently active; the build does not depend on Theme Builder templates, but deactivating it will disable Pro widgets already in use |
| **SureForms** | all three forms and their notification settings |
| **Rank Math** | titles, descriptions, sitemap, noindex rules |

Theme: **Astra 4.14.0** (active). **Twenty Twenty-Five** is kept as a recovery fallback;
every other theme was removed.

Users: **one administrator** — `develop@cloudmellow.com`. Site admin email is
`info@goodshepherdmanor.org`.

---

## Known placeholders (client has not supplied copy)

1. **`/programs/vocational` (2089)** — body copy is still lorem ipsum. The page carries a
   visible “Scope” callout saying so. Vocational is the approved scope cut if the build
   runs long. Replace the copy, then delete that callout.
2. **News article bodies** — headings, titles and slugs are real; the article prose inside
   each post is lorem. The `/news` hub cards link to real published posts.
3. **Newsletter archive** on `/newsletters` — three issues are listed but the client has no
   PDFs. The “Download PDF” buttons were removed rather than left as dead `#` links. Add
   them back (button → media file URL) when the files arrive.
4. **Affiliations** on `/about` — the ARC of Illinois button was removed because no
   destination was supplied. Add it when the client confirms the URL.

---

## What was fixed in this pass (2026-11-04)

- Added the **28 missing section anchors** on the four program pages so the “On this page”
  sidebars actually jump somewhere.
- Replaced the single shared stand-in photo on all four program pages with real GSM
  photography (Vocational, Community Engagement, Residential, Health) and deleted the
  “Placeholder photo — …” captions. Alt text added to 11 images.
- `/news` cards pointed at three posts that did not exist (404). Re-pointed to published
  posts.
- Dead `#` buttons removed (About / ARC of Illinois, Newsletters / Download PDF).
- Newsletters form converted from a `[sureforms]` shortcode to a **SureForms Form widget**,
  so it is editable in Elementor like the rest.
- **Fixed a 138px horizontal overflow at 390px on every page**: Astra gave the above-footer
  a fixed 528px grid column, so the newsletter band was wider than the viewport.
- **Privacy had invisible white nav text on white** (only page with no hero behind the
  header) — scoped nav colours added for `.page-id-3`.
- Nav current-item and submenu active colours moved from `#0089DF` (3.59:1) to `#006BB3`
  (5.46:1) for WCAG AA.
- Footer tagline was lorem — replaced with the real tagline already drafted in a leftover
  block. Footer “Memorial or Tribute” pointed at a removed anchor; now
  `/support-gsm/#ways-to-give`.
- Newsletter band copy read “STAY CONNECTED Stay connected with …” — duplicate eyebrow
  removed.
- Imports lorem out of four pages’ hidden `post_content` (About, Programs, Support GSM,
  News) so search and excerpt fallbacks are clean.
- Form notifications now go to `info@goodshepherdmanor.org` instead of a developer inbox.
- Comments/pingbacks off site-wide; unused themes and user accounts removed; Rank Math
  title for Community Engagement corrected (was “Special Olympics”); Privacy title and
  description added.

Verified after the pass: 16/16 routes return 200, no horizontal overflow at 390 / 1024 /
1440, every internal link and anchor resolves, no Elementor notices, no broken images,
sitemap contains 16 pages + 7 posts and no SureForms URLs.

### Follow-up fixes (same day)

- **Hiring banner at ≤921px** restyled into a two-line stack with a white pill CTA, then
  brought to a 44px tap target and 14px type to match the rest of the site.
- **Newsletter band “Sign Up”** moved from `#0089DF` (3.72:1, failed AA) to `#006BB3`
  (5.59:1).
- **Mobile-menu logo swap** rewritten — `content: url()` on an `<img>` is ignored by
  Firefox, which left a white logo on the white bar. The colour logo is now painted on
  the wrapping link with the bitmap hidden.
- **Endowment membership table** no longer pushes the page 2px wide below ~387px; the
  columns share the width and wrap under 400px.
- **Push runbook corrected** in `AGENTS.md` — the documented `wp db export` did not work
  and the expected replacement count was off by two orders of magnitude.
- **Database dumps ignored in git** — the runbook writes them into `_migration/`, which
  is tracked, so they would have been committed with `wp_users` hashes.

Re-verified: 16 pages × 8 widths (320–1440), no overflow anywhere, all 200; and a
restore test of the 2026-11-04 backup matched the live database exactly.

`.mcp.json` is untracked and git-ignored — it holds machine-specific absolute paths.
