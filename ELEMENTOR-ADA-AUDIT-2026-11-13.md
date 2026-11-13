# Elementor editability + ADA audit — 2026-11-13

**Target:** stage (`goodshephe3dev.wpenginepowered.com`) and Local, both checked.
**Question 1:** can everything the client should edit actually be edited in Elementor (no raw HTML, no baked-in content, no CSS-only content)?
**Question 2:** does the site pass WCAG 2.1 AA (axe-core, desktop + mobile + drawer open)?

---

## 1. Elementor editability — PASS

Scanned `_elementor_data` for all 14 Elementor pages plus the Newsletter band template (2375), counting widget types and looking for anything that hides content from the editor.

| Check | Result |
|---|---|
| Raw `html` widgets | **0** on every page |
| `shortcode` widgets | **0** (forms use the native SureForms widget) |
| Per-element custom CSS (`custom_css`) | **0** |
| Inline `<style>` / `<script>` inside text editors | **0** |
| Shortcodes inside text editors | none found |
| Native widget mix | heading / text-editor / button / image / icon-list / sureforms_form only |
| Privacy page | plain WP content, no Elementor — editable in the block editor ✔ |
| Header + footer | Astra Customizer, not Elementor Theme Builder ✔ (per spec) |
| Hero / band photography | Elementor `background_image` controls, not CSS ✔ |
| Newsletter band | template 2375, referenced from Astra's above-footer slot ✔ |
| Forms | SureForms widgets by ID (2056, 2370, 2202) ✔ |

**Every string and every photo on the site is editable in the Elementor canvas.** Nothing needs a developer for a copy or image change.

Fixes made this pass:

- **Removed 7 dead CSS rules** (`.gsm-bg-hero`, `.gsm-bg-cta`, `.gsm-bg-donate`, 1,691 bytes) that set background images with `!important` on classes no element uses — the images come from Elementor, so these would have silently overridden a client's image change if the class were ever re-added.
- `_tools/verify_site.php`: **47/47 checks pass** after the changes.

### Maintenance notes (not defects)

1. **Program sidebar nav is hand-built.** Each section has its own button widget (`nav_<section>`). Adding a new section means adding its sidebar button too — two edits, not one.
2. **The newsletter band is global.** Editing template 2375 changes every page. That is intended, but worth telling the client before they "fix" one band and wonder why all 15 changed.
3. **Reused forms keep their IDs.** `/newsletters/` embeds form 2202 twice (band + page body), so its DOM ids repeat. Axe does not flag it and nothing breaks visually; if a strict HTML validator is part of acceptance, use only one instance.

---

## 2. ADA / WCAG 2.1 AA — PASS on automated checks

axe-core 4.10.2, rules `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`.

| Scope | Routes | Violations |
|---|---|---|
| Desktop 1440 | all 15 pages + a news article | **0** |
| Mobile 390 | Home, About, CDS, Support, Contact | **0** |
| Mobile 390, drawer open | same five | **0** |
| 404 page | one bogus URL | **0** |

Fixes this pass (all verified by re-running axe):

| Element | Was | Now |
|---|---|---|
| Header "Support GSM" button | white on `#0089DF` — **3.59:1** | `#006BB3` — **5.46:1** |
| Program sidebar current-page button | `#0089DF` on white — **3.72:1** | `#006BB3` (set in Elementor, not CSS, so it stays editable) |
| Program sidebar label | `#0089DF` — 3.72:1 | `#006BB3` |
| Required asterisk | `#DC2626` — 4.41:1 | `#B42318` — 6.57:1 |

### What automation cannot cover

axe catches roughly 30–40% of WCAG issues. These still need a human pass before sign-off:

1. **Keyboard-only walk** — tab through each page, confirm the focus ring is visible on navy and on photo heroes, and that the drawer traps focus and returns it on close.
2. **Screen reader pass** — one page per template (Home, a program page, Support GSM, Contact) with VoiceOver: heading order, landmark names, the jump bar announcing as tabs/links, and form error announcements.
3. **Zoom / reflow** — 200% and 400% zoom at 1280 wide; text must not clip inside the heroes and the program sidebar must not overlap the article.
4. **Reduced motion** — `prefers-reduced-motion` should stop the hero parallax/fades.
5. **Colour-independent meaning** — the active sidebar item is signalled by colour only; confirm it also carries `aria-current`.

---

## 3. Still open (content / ops, not code)

| # | Item | Owner |
|---|---|---|
| 1 | News article bodies are Lorem ipsum | writer / client |
| 2 | Three "Placeholder photo —" captions (Residential, Health, Engagement) | writer |
| 3 | Mail transport: `GSM_SMTP_PASS` + DKIM, then test all three forms | ops |
| 4 | News/Events cards: no imagery, no date/category | design + content |
| 5 | Type scale drift (H2 30/32/36/40/44/48) and Privacy/article templates | design decision |
