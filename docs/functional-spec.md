# Functional Specification — Good Shepherd Manor

Behavioural specification for the build as it exists on stage, not as it was wireframed. Every statement here is checkable with the commands in *Acceptance criteria*.

## 1. Global chrome

### 1.1 Header

Sticky. Transparent over the hero photo on Home and every page in `HERO_HEADER_PATHS`, solid white after scroll and on inner pages.

| Position | Item | Target | Dropdown |
|---|---|---|---|
| 1 | About | `/about/` | About Us · Mission, Vision & Values · Our History · Affiliations · Accessibility |
| 2 | Programs & Services | `/programs/` | Programs & Services · Community Day Services · Residential Living · Health & Well Being · Community Engagement |
| 3 | Support GSM | `/support-gsm/` | GSM Foundation · Events · Shepherd Endowment Society · Memorial or Tribute |
| 4 | News & Updates | `/news/` | none |
| 5 | Careers | `/careers/` | none |
| 6 | Contact | `/contact/` | none |
| CTA | Support GSM (button) | `/support-gsm/` | — |

Dropdown targets that are sections, not pages: GSM Foundation → `/support-gsm/#foundation`, Memorial or Tribute → `/support-gsm/#ways-to-give`, About sub-items → `/about/#mission`, `#history`, `#affiliations`, `#accessibility`.

The menu is a WordPress menu (`primary-menu`, term 15) assigned to `primary` and `mobile_menu`. It is **not** built in Elementor.

### 1.2 Above-header banner

Light-blue-on-navy bar above the header, linking to `/support-gsm#ways-to-give`:

> A Place to Belong. A Life to Thrive. Support our Mission →

At `max-width: 921px` it restacks to two lines with a white pill CTA (`min-height: 44px`, 14px type). At `≥922px` it is a single line with an underlined link. Owned by Additional CSS, not Elementor.

### 1.3 Footer

Four-column Astra footer built with the footer builder (Astra Addon is active, which is what supplies the four widget areas):

- Column 1 — logo, short description, established 1971
- Column 2 — About Us, Mission/Values, Our History, Our Programs, Affiliations
- Column 3 — GSM Foundation, Shepherd Endowment Society, Events, Memorial or Tribute
- Column 4 — Tel: (815) 472-3700, P.O. Box 260, 4129 N. State Route 1-17, Momence, IL 60954

Copyright line: `[copyright] [current_year] The Good Shepherd Manor. All rights reserved.` plus Privacy Policy and Accessibility Statement links. `[current_year]` is an Astra token resolved server-side, so the year rolls over without an edit — subject to page cache being purged after January 1.

Facebook icon → `https://www.facebook.com/goodshepherdmanormomence/` — Facebook is the only social profile GSM maintains.

### 1.4 Newsletter band

Elementor section template **2375 "Newsletter band"**, injected via Astra's `footer-html-1` as `[elementor-template id="2375"]`. Renders above the footer columns on every page. Contains heading, lede, and SureForms form 2202. Styling (glass pill, blue glow, vertically centred field text) lives in Additional CSS scoped to `.elementor-element-nlband` / `.elementor-element-nlright`.

## 2. Routing

### 2.1 Permalinks

Pages: `/%postname%/`. Posts: `/news/%postname%/`.

### 2.2 Redirects

Implemented in `mu-plugins/gsm-redirects.php` (source: `_migration/mu-plugins/gsm-redirects.php`) on `template_redirect`, 301:

| From | To | Reason |
|---|---|---|
| `/ways-to-give/` | `/support-gsm/#ways-to-give` | merged into Support GSM Foundation |
| `/donate/` | `/support-gsm/` | same |
| `/programs/vocational/` | `/programs/community-day-services/#vocational-classroom` | page retired 2026-11-06 |
| `/sitemap.xml` | `/sitemap_index.xml` | Rank Math uses the indexed form |

Fallback: any 404 whose path is a single segment that matches a published post slug 301s to `/news/<slug>/`. This keeps pre-`/news/` article links alive.

A mu-plugin is used because Local runs nginx (no `.htaccess`) and it keeps the table in version control.

### 2.3 404

Astra 404 template, customised copy:

> **This page doesn't seem to exist.**
> It looks like the link pointing here was faulty. Maybe try searching?

Followed by a search field. Returns HTTP 404 correctly. No breadcrumb, no link back to Home or Programs — see *Known gaps*.

## 3. Forms

All three forms are SureForms posts (`sureforms_form`), referenced by ID so form edits do not require a page rebuild. None uses reCAPTCHA and none has a honeypot.

| ID | Form | Fields (label → slug) | Submit label | Notifies |
|---|---|---|---|---|
| 2056 | Simple Contact Form | Full Name → `full-name` · Email → `email` · Subject → `subject` · Message → `message` | Send Message | `info@goodshepherdmanor.org` |
| 2370 | Thank a Staff Member | Your name → `your-name` · Email → `email` · Staff member → `staff-member` · Note → `note` | Send thanks | `info@goodshepherdmanor.org` |
| 2202 | Newsletter Signup | Email → `email` | Sign Up | `info@goodshepherdmanor.org` |

Notification settings on all three: `from_name` = `{site_title}`, `from_email` = `info@goodshepherdmanor.org`, `email_reply_to` = `{form:email}` (submitter), body = `{all_data}`.

Confirmation behaviour: 2056 and 2370 show an in-page success message; 2202 hides the form after submit and shows "Thanks for subscribing to Good Shepherd Manor updates."

**Storage:** submissions are stored by SureForms inside WordPress (Entries screen) and emailed. There is no external marketing platform — the newsletter form does **not** write to Mailchimp, Constant Contact, or any ESP. Growing a mailing list from 2202 requires exporting SureForms entries manually, or a later integration.

**Delivery dependency:** the notification email is only as good as the site's mail transport. See `docs/integrations.md` §7.

Placement:

| Form | Appears on |
|---|---|
| 2056 | `/contact/` |
| 2370 | `/contact/` |
| 2202 | every page, via template 2375 |

## 4. Page-level behaviour

### 4.1 Program pages

Four pages under Programs, in this fixed order: Community Day Services, Residential Living, Health & Well Being, Community Engagement. The same order is used by the header dropdown, the Programs landing cards, the homepage cards, and the article sidebar — keep them in sync.

Each has a sticky sidebar listing its in-page sections. Sidebar uses CSS `position: sticky` at `min-width: 1025px` (deliberately **not** Elementor's Sticky control, which pins it over the footer after the article ends). Below 1025px the sidebar becomes a column above the article.

### 4.2 Support GSM Foundation

One merged page (Foundation + Ways to Give, client direction). Numbered cards at top, then a sticky jump bar (`SectionTabs`) scrolling to stacked anchor sections: `#foundation`, `#ways-to-give`, `#endowment-society`, `#events`. All four sections are always visible — the tabs are scroll targets, not hidden panels. Active tab tracks scroll position.

### 4.3 Home

Ten sections in order: hero → intro strip (3 cards) → mission/impact counters → programs (4 cards + View all) → about/mission mosaic → stories (2 cards) → Support GSM Foundation (4 cards). Home intentionally carries **no** `gsm_cta_band` (client decision 2026-10-02).

### 4.4 Responsive contract

Verified bands: 320, 390, 768, 1024, 1440. Zero horizontal overflow at any of them, on all 15 routes.

Three fixed traps worth knowing before editing CSS:

| Band | Behaviour |
|---|---|
| 768–921 | Program page body switches to `flex_direction: column`; article and sidebar both go 100% width. Without this the article scrolls away and leaves a dead 296px gutter |
| 923–1024 | The duplicate header CTA is hidden; the nav's own Support GSM item covers it. Logo + 6 nav items + CTA have a hard minimum of 1008px |
| any | Program sidebar carries no Elementor sticky; CSS sticky stops at the article row |

### 4.5 Accessibility

- Skip link to content, first focusable element, navy background for contrast
- Text and button fills use `#006BB3` (5.46:1 on white) rather than brand `#0089DF` (3.59:1); the brand blue is reserved for decorative fills
- Headings are real heading elements (`h1`/`h2`), not styled paragraphs
- Tap targets ≥44px on the mobile banner CTA and primary buttons
- Mobile drawer forces the header bar solid white with the colour logo so a white logo never sits on a hero photo

## 5. Content state

Real, client-approved copy: all program pages, Endowment, Events, Careers, Newsletters, Contact, News hub furniture.

Still placeholder: descriptive body prose on Home, About, Support GSM Foundation, and news article bodies (lorem), pending client review. A client-facing note belongs on any URL shared for review.

## 6. Known gaps

1. **404 has no recovery path** — search only; no links back to Home or Programs.
2. **No spam protection** on the contact forms — no reCAPTCHA, no honeypot.
3. **Newsletter has no ESP** — entries stay in WordPress.
4. **Analytics is a placeholder** — `G-XXXXXXXXXX` is configured as the measurement ID (see `docs/integrations.md` §5).
5. **Mail delivery unconfigured** — form notifications and password resets do not currently leave the server.

## 7. Acceptance criteria

A page is "done" when all of the following hold:

```sh
# 47 assertions: IDs/slugs, builder mode, form IDs and recipients,
# newsletter template + footer slot, program anchors, /news links, images on disk
./_tools/wp.sh eval-file _tools/verify_site.php

# every route 200
for p in about programs support-gsm events news newsletters careers contact privacy; do
  printf '%-14s ' "/$p"; curl -sk -o /dev/null -w '%{http_code}\n' "https://goodshepherd.local/$p/"
done
```

plus: no horizontal overflow at 320/390/768/1024/1440, correct `h1`, every image resolves.
