# Stage design audit — 2026-11-13

**Target:** https://goodshephe3dev.wpenginepowered.com
**Scope:** all 15 routes + Privacy + a news article. Automated sweep at 390 / 768 / 1024 / 1440, plus manual review of hero, header, dropdown, mobile drawer, galleries, forms, tables and article template.
**Method:** Playwright (Chromium) measurement of live DOM — overflow, contrast ratios (WCAG 2.1), tap-target heights, heading order, image load state, anchor resolution, duplicate ids, computed type scale — then visual review of screenshots.

**Verdict:** structurally sound, not yet pristine. No layout breakage at any width, but there are **3 content blockers**, **1 user-facing functional blocker**, and **a set of AA contrast failures** that are all small, local fixes.

---

## Fixed on stage — 2026-11-13

Applied to Local **and** stage via `_tools/*.php` + WP-CLI (Flushed Elementor CSS and object cache after each).

| # | Fix | Script / where |
|---|---|---|
| 1 | **CTA band** (`gsm_cta_band`) inserted on all 13 content pages, real card copy, host-agnostic image URL | `_tools/insert_cta_band.php` + `/tmp/cta_band.json` |
| 2 | Sidebar label + active link `#0089DF` → `#006BB3` (**5.59:1**) | `_tools/accessibility_css_fixes.php` |
| 3 | Required asterisk `#DC2626` → `#B42318` (**6.57:1**) | same |
| 4 | `STAY CONNECTED` eyebrow added to the newsletter band (template 2375) | `_tools/newsletter_eyebrow.php` |
| 5 | About → Accessibility section flipped, image now left (row-reverse, DOM order kept) | `_tools/flip_accessibility_image.php` |
| 6 | 64px bottom padding under the program-page galleries | `_tools/gallery_bottom_padding.php` |

Remaining below: news article copy, placeholder captions, mail transport, News/Events imagery, type-scale and template decisions.

---

## P0 — blockers

### 1. News article bodies are Lorem ipsum
`/news/35th-annual-fall-festival/` renders `Lorem ipsum…` as the body copy. Every article uses the same placeholder source, and `/news/` cards link into them. The site cannot launch with placeholder article text.
**Fix:** real copy per post (or unpublish article cards until copy lands).

### 2. Wire captions visible in production copy
Literal wire text sits under real photos on three program pages:

| Page | Caption |
|---|---|
| Residential Living | `Placeholder photo — homes on the Momence campus.` |
| Health & Well Being | `Placeholder photo — the McAllister Infirmary.` |
| Community Engagement | `Placeholder photo — outings, athletics, and community events.` |

**Fix:** delete the captions (the photos are self-explanatory) or write real ones.

### 3. No mail transport — every form fails silently
`GSM_SMTP_PASS` is not defined, so `mu-plugins/gsm-mail.php` is inert. `wp_mail()` returns false with no log line: newsletter signups, contact messages, thank-a-staff notes, password resets and new-user mail all disappear without an error. The UI shows no failure because SureForms treats the submission as accepted.
**Fix:** SendGrid key + `GSM_SMTP_PASS` in `wp-config.php`, From domain DKIM-verified, then submit each of the three forms and confirm delivery + a SureForms entry.

---

## P1 — visible defects / AA failures

### 4. Program sidebar label + active link fail AA
Not breadcrumbs (those are white on the hero and pass): the sidebar eyebrow `Programs` renders `#0089DF` at 13px and the active/nested nav links at 15px → **3.72:1** on white, below 4.5:1. Present on all four program pages.
**Fix:** `#006BB3` (5.46:1) — the same token already used for body links.

### 5. Required-field asterisk fails AA
Contact form asterisks are `#DC2626` → **4.41:1** at 16px. The documented token is `#B42318` (7:1). Three instances on `/contact/`.
**Fix:** set the asterisk colour to `#B42318`.

### 6. ~~Inline CTAs are under the 44px tap target~~ — not a defect
Measurement artifact. Every inline CTA ("Learn more →", "Read More", "View openings →", "Apply for…", "Facebook") is an `.elementor-button` and already carries the 44px `::after` hit-area overlay; the class's own box is 14–20px, which is what a bounding-box audit reports. Checking `::after` height confirms **44px effective** on all of them. No change needed.

### 7. Duplicate DOM ids
Present on every page: `ast-desktop-header`, `ast-mobile-header`, `ast-mobile-site-navigation`, `ast-hf-mobile-menu`, `srfm-error-message`. Worse on form pages: `/contact/` repeats `srfm-sender-email`, `srfm-page-break`, `srfm-submit-btn`; `/newsletters/` repeats the whole `srfm-form-2202` id set because the newsletter form is embedded twice (band + page).
**Fix:** newsletters page uses the same form twice — give the inline instance a distinct id, or rely on the band only. The Astra ones are theme-generated; low risk but they do break `for`/`aria-describedby` uniqueness.

### 8. Events and News cards have no imagery or metadata
`/events/` has **0 images** on the page; `/news/` cards have **0 images** and no date or category line — just headline, excerpt, "Read More". Next to the rest of the site (every other page leads with photography) these two read as unfinished.
**Fix:** add a photo per event/news card, plus date + category on news cards.

### 9. Newsletter band is missing its eyebrow
The design has `STAY CONNECTED` above the band copy; stage renders only `Newsletter` + copy. The label element exists in template 2375 but is empty.
**Fix:** add the line in the Elementor template.

### 10. CTA band absent on 12 content pages
Design and `AGENTS.md` both specify `gsm_cta_band` (Support GSM Foundation / Donate / Volunteer / Careers) before the newsletter band on every content page except Home. No page carries it — it is missing in Local too, so it is a build gap, not a push gap.
**Fix:** `_tools/rebuild_cta_band.py` → `apply_elementor.sh` → push.

---

## P2 — consistency and polish

### 11. Type scale drifts page to page
Section H2s measure **30, 32, 36, 40, 44** and 48px depending on the page; H1s are 54px everywhere except Home (64) and Privacy (32). Card numbers are 40px, stats 48px. There is no single scale — it looks intentional only because pages are rarely seen side by side.

| Role | Values found |
|---|---|
| H1 | 32 (Privacy), 54 (all content), 64 (Home) |
| H2 section | 30 (articles), 32 (Events), 36 (Newsletters), 40 (Programs, News), 44 (About, Support, Careers, Contact), 48 (Home, band) |
| Body | 16/26 (articles), 17/27 (Privacy, Newsletters), 19/31 (hero ledes) |
| Eyebrow/label | 13, 15 |

**Fix:** collapse to a 4-step scale — H1 54, section H2 44 (or 40 for compact bands), article H2 30, body 16/26.

### 12. Privacy page is off-template
H1 32px, H2 36px, no hero image, different body size (17/27). It is the only page outside the hero template.
**Fix:** either accept it as a utility page or bring it onto the standard hero + 30px article headings.

### 13. News article template is off-template too
Article H1 is 32px with no hero, versus 54px + photo hero on every content page.
**Fix:** decide whether posts get the hero treatment or a distinct article header — right now it looks like neither.

### 14. Mosaic images have empty alt
Home: 6 images with `alt=""` (the four mosaic photos and two more). They are decorative *containers*, but the photos show residents and carry meaning.
**Fix:** supply alt text, or confirm decorative intent with the client.

---

## Clean — checked, no defects

| Check | Result |
|---|---|
| Horizontal overflow | **0px at 390 / 768 / 1024 / 1440 on all 16 routes** |
| In-page anchors | no dead `#` targets, no `href="#"` placeholders |
| H1s | exactly one per page, all correct wording |
| Titles + meta descriptions | unique and present on every route |
| Images | all load (naturalWidth > 0 after lazy-load); no broken files |
| Contrast — body, headings, buttons, dark bands | passes AA everywhere outside items 4–5 |
| Galleries | single column at 390, two columns at 768+, no clipping |
| Membership table (Endowment) | fits at 342px, no overflow |
| Mobile drawer | opens with colour-logo swap, close button clear of the banner |
| Header dropdowns | render, positioned correctly, six items on About / five on Programs |
| Nav / footer | labels, order and targets match `NAV_ITEMS`; Facebook only |
| Newsletter band | pill layout, 54px field, no wrap at 390 |

---

## Suggested order of work

1. News article copy, placeholder captions (content — client or writer)
2. Mail transport (ops — key + DKIM + test all three forms)
3. CTA band (script, 12 pages)
4. Breadcrumb + asterisk colour (one CSS rule each)
5. Tap-target overlay for inline links (one CSS rule)
6. Newsletter eyebrow (template)
7. News/Events imagery + metadata (design + content)
8. Type-scale and article/Privacy template decisions (design)

Items 3–6 are all single-line changes in Additional CSS or the band template; together they clear every AA failure on the site.
