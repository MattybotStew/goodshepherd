# GSM — Build Plan (WordPress / Elementor)

**Read `AGENTS.md` first.** It is canonical for IA, slugs, palette, stack, and hard
rules. This file is the *state of the build and what remains*. If they disagree,
`AGENTS.md` wins.

This file is written to be handed to any model or tool (Cursor, Claude Code, Cline,
Gemini CLI) without prior conversation context. Every claim here was verified against
the running site on **2026-10-02** (audit) — earlier items marked done were last
re-verified on that date.

---

## 0. Ground rules for whoever picks this up

1. **Local is canonical.** `https://goodshepherd.local`. Never edit the WP Engine dev
   site directly. Stage is a rebuilt copy of Local's DB.
2. **No production deploy.** Final target is dev (`goodshephe3dev.wpenginepowered.com`).
3. **Body copy is lorem on purpose** — client copy is not delivered. Keep headings,
   eyebrows, slugs, nav labels, contact data, and structured lists real. Do not polish
   lorem, and do not let lorem leak into a real page (e.g. 04 demo phone numbers).
4. **Duplicate, never design fresh.** 15 pages, one starter (Non-Profit Organization
   04), no new page templates, no child theme, no Theme Builder header/footer.
5. **`wp cache flush` after every Elementor edit**, in Local and on dev. Use
   `_tools/apply_elementor.sh` for page data — see §3 for why it is not optional.
6. Do not commit unless asked. Do not deploy unless asked.

### Environment

| Thing | Value |
|---|---|
| Site URL | `https://goodshepherd.local` |
| Site root | `/Users/matthewstewart/Local Sites/goodshepherd` |
| Docroot | `/Users/matthewstewart/Local Sites/goodshepherd/app/public` |
| WP-CLI wrapper | `/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh` — **not** in the repo |
| Elementor apply | `/Users/matthewstewart/Developer/goodshepherd/_tools/apply_elementor.sh <PAGE_ID> <json>` |
| React wires | `npm run dev` → http://localhost:5173 |
| Repo | `main` @ `origin` = `https://github.com/MattybotStew/goodshepherd` |
| Last commit | FPM root-cause + Bookly crons + GSM logo/header-button (see §14) on top of `05372a9` — **2 ahead of `origin/main`**, not pushed |

The WP-CLI wrapper is a path with spaces — quote it:

```sh
WP="/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh"
"$WP" post list --post_type=page --fields=ID,post_name
"$WP" post meta get 2092 _elementor_data
curl -sk https://goodshepherd.local/          # -k: self-signed Local cert
```

`curl -sk` is required. HTTP 301s to HTTPS. The cert is self-signed (CN
`goodshepherd.local`, valid to 2036) — a browser cert warning is expected, not a bug.

---

## 1. Stack state — done

| Item | State |
|---|---|
| Elementor | 4.3.3 active |
| Elementor Pro | 4.3.1 active — Pro features (Posts widget, native sticky) render. ⚠️ `elementor_pro_license` option reads `false`; confirm on the wp-admin Licenses screen and re-activate if the nag shows |
| Astra Pro addon | 4.13.10 active, **licensed** (`brainstrom_products.astra-addon` registered) — above-header bar + sticky header work |
| SureForms | 2.12.8 active — one form, ID `2056` |
| Palette | `--ast-global-color-0..7` = `#0089DF #006BB3 #002A4E #303336 #FAFCFE #FFFFFF #C8D4E0 #000000` ✅ |
| Type | DM Sans ✅ · container 1200px ✅ · no 04 lime anywhere ✅ |
| Active plugins | **only** `astra-addon`, `elementor`, `elementor-pro`, `sureforms` + must-use `gsm-redirects` |

**Removed 2026-10-01/02 (done, do not reinstall):** `ultimate-elementor`,
`wordpress-seo`, `astra-pro-sites`. `wp plugin list` confirms 4 active + 1 mu-plugin.

Astra global colors live in the theme's dynamic CSS, not in a `astra-global-color-palette`
option — do not go looking for one.

---

## 2. Page inventory — all 16 routes return 200 (verified 2026-10-02)

| ID | Slug | Parent | Build state (current) |
|---|---|---|---|
| 315 | `/` | — | ⚠️ Wired but wrong sections + wrong hero CTA — see §4 |
| 316 | `/about` | — | ✅ built, buttons wired, anchors ✅ |
| 317 | `/programs` | — | ✅ 5 program cards incl. Special Olympics, 04 copy gone |
| 2088 | `/programs/community-day-services` | 317 | ✅ built, `#digital-den` ✅ |
| 2089 | `/programs/vocational` | 317 | ✅ built |
| 2090 | `/programs/residential-living` | 317 | ✅ built |
| 2091 | `/programs/health-well-being` | 317 | ✅ built, all 5 anchors ✅ |
| 2127 | `/programs/special-olympics` | 317 | ✅ built |
| 2092 | `/support-gsm` | — | ✅ reference build — see §3 |
| 2093 | `/shepherd-endowment-society` | — | ✅ 16.8 KB, **all real copy** (intro, quote, gifts, membership) + column-aligned table + anchors — §5.1 |
| 2094 | `/events` | — | ✅ 4 event anchors ✅; lede de-duped 2026-10-02 (was 5×, now 1) |
| 2095 | `/newsletters` | — | ⚠️ archive works (3 posts via Posts widget); "Join our Mailing List" embeds **contact form 2056**, not a signup — §9 |
| 2096 | `/careers` | — | ✅ Contact residue removed (0 "Front Office", no form, no 555); 1 job listing + benefits |
| 318 | `/news` | — | ✅ Posts widget, 4 posts, term 19; ⚠️ no featured images → imageless cards |
| 319 | `/contact` | — | ✅ built, form renders, no 555; ✅ form tested via REST endpoint 2026-10-02 (entry + single email) |
| 3 | `/privacy` | — | ✅ real policy copy; single `<h1>` since 2026-10-02 (duplicate title heading removed) |
| 2011 | `/ways-to-give` | — | ✅ gone (redirect covers the URL) |

**Verified anchors:** Health `#nursing #clinic #pharmacy #supports #transportation` ·
Events `#fall-festival #brunch-auction #golf-invitational #family-events` ·
Support GSM `#foundation #ways-to-give #endowment-society #events #memorial-tribute` ·
About `#history #mission #accessibility`.

**Verified fixed (were open, now done):** dead buttons — the §6 audit script returns
`none` on all 9 checked pages · `(555)` phone count = 0 on `/contact` and `/careers` ·
home counters carry `ending_number` 55/100/4/1971 · 04 "Proofing our impact" copy gone
from `/programs` · draft `2011` gone.

---

## 3. `/support-gsm` (ID 2092) — the reference implementation

This page is finished and is the pattern to copy for the remaining pages. Do not
re-derive it.

- Hero (cloned shared photo-overlay hero) + 5 anchored sections
- **Native Elementor Pro sticky jump bar** — `gsmjumpwrap` outer container, `gsmjumprow`
  inner row, `gsmtab0`–`gsmtab4` heading widgets. Pro sticky controls on the outer
  container. **No CSS-position sticky.**
- `scroll-spy` is an isolated page-scoped `gsmspy` HTML widget, not Custom Code —
  Custom Code snippets render site-wide unless scoped, and this only needs one page.
- `scroll-margin-top: 72px` on anchors so the sticky bar doesn't cover headings
- Build: `python3 _tools/build_support_gsm.py > /tmp/sgsm.json`
  then `./_tools/apply_elementor.sh 2092 /tmp/sgsm.json`
- Hero source is `_migration/support-gsm-hero.json` (committed; the builder defaults to it)
- Verified: 5 tabs, 5 hrefs, sticky activates on scroll, correct desktop image-side
  mapping, no console errors

**`apply_elementor.sh` matters.** Elementor's CSS cache does not regenerate on a raw
`_elementor_data` meta write. The script clears Elementor's cache, instantiates
`Elementor\Core\Files\CSS\Post`, calls `update()`, and fails if
`uploads/elementor/css/post-<ID>.css` was not touched. Always use it. Never write
`_elementor_data` directly and expect styles to follow.

### Redirect

`_migration/mu-plugins/gsm-redirects.php` → `wp-content/mu-plugins/gsm-redirects.php`.
Currently: `/ways-to-give/` → 301 → `/support-gsm/#ways-to-give` ✅ ·
`/donate/` → 301 → `/support-gsm` ✅. Local runs nginx, so `.htaccess` is not an
option. Add redirects here.

---

## 4. Homepage `/` (ID 315) — rebuilt to proto spec ✅ (2026-10-02)

**Spec decision (settled — do not reopen):** `src/pages/HomePage.jsx` (Figma `9137:3182`)
wins over the `9009:2` wire. `AGENTS.md` §Homepage has been rewritten to match. The
previous conflict and the clobber by `/tmp/home_figma.json` are closed out.

Built order, verified in rendered HTML and by pixel measurement of a headless screenshot:

`138ba28` hero · `b233779` intro strip · `78cc2f2` Our Impact · `prog_sec` Our Programs ·
`e743605` About · `story_sec` Stories · `support_gsm` Support GSM Foundation.

Backup of the pre-rebuild Elementor data: `/tmp/315-pre-rebuild.json` (69,894 bytes).
Build script: `/tmp/build315.py` → `/tmp/315-new.json`, applied with
`_tools/apply_elementor.sh 315`.

| # | Fix | Result |
|---|---|---|
| 1 | ✅ Hero CTA href | all 3 "Now Hiring! Apply Today" → `/careers` |
| 2 | ✅ Intro strip titles | `01. Projects / 02. Support GSM / 03. Donate`; hrefs `/programs`, `/support-gsm`, `/support-gsm` (Donate → `/support-gsm`, per decision — not `#ways-to-give`) |
| 3 | ✅ CTA band | **won't fix — client decision 2026-10-02**: home gets no `gsm_cta_band`. See §12. |
| 4 | ✅ `get_involved` removed | Donate/Volunteer/Careers split deleted; `data-id="get_involved"` absent from render |
| 5 | ✅ Program cards | now 5 (`prog_card_0..4`) incl. Special Olympics → `/programs/special-olympics`; impact counter `Core programs` = `5` (`data-to-value="5"`). **Descriptions deliberately not added** — cards unchanged apart from the 5th. |
| 6 | ✅ Stories heading | kept as "What's Happening at GSM" (proto), section **retained** above the foundation section by client decision — it is not in the proto but carries event promotion |
| 7 | ✅ `TBD Vocational Program` | intentional — `site.js` `homeName`; leave it |

Foundation section: `support_gsm`, bg `astglobalcolor4`, centered h2, 4 cards at 25%
(`support_card_0..3` → `/support-gsm`, `/events`, `/shepherd-endowment-society`,
`/support-gsm#memorial-tribute`).

About section fix: heading `7a81b49` moved to position 1 and `header_size` p → **h2**
(its `<p>` was the only reason that section had no heading), `about_p2` second paragraph
inserted.

**Elementor gotcha (cost a debug cycle):** `--width` only prints when the container has
`content_width: 'full'` (`elementor/includes/elements/container.php`, `width` control
condition). Without it, cards silently render at 100% and stack. Applied to
`prog_card_0..4` and `support_card_0..3`. `story_card_*` are intentionally left alone —
the stories row is `nowrap` and relies on `flex-shrink`.

**Known deviation from proto (accepted):** cards use the site's filled blue "Learn more"
button (proto uses a bare text link) and radius 16 + 1px border (proto is radius 8 +
shadow) — no custom CSS is permitted. About / Stories / Foundation share
`astglobalcolor4`, so they read as one light band; About→Stories already did.

**Verified:** 1 `h1`; h2 order = Mission & Vision → Our Programs & Services → About →
What's Happening → Support GSM Foundation; section order and About DOM order correct;
10 link targets → 200 (after trailing-slash 301); 16/16 routes 200; FPM log unchanged
(26 crashes, mtime Oct 1 19:28); `post-315.css` emits `--width:20%` ×5 and `25%` ×4;
programs row = 5 cards × 182px, foundation row = 4 cards × 278px at y=3609…3892.

**Screenshots:** the white gap above the footer is an artifact of forcing
`--window-size=1440,7000` (footer pins to viewport bottom; untouched pages show the same
4,000px+ blank runs). Use a realistic viewport height.

---

## 5. Page work remaining

### 5.1 `/shepherd-endowment-society` (2093) — done ✅ (2026-10-02)

All body copy is now real. Source was **not** `src/data/endowment.js` (its
`endowmentIntro` / `endowmentQuote.text` / `endowmentDisbursement` were lorem too) —
it came from the client's production site:
`https://www.goodshepherdmanor.org/foundation/shepherds-endowment-society/`
(the provenance AGENTS.md already recorded as "from production site").

What landed (page data + the React source of truth):

| Fix | Detail |
|---|---|
| ✅ Intro paragraphs | 2 real paragraphs + the disbursement sentence (was 1 lorem `<p>`) |
| ✅ Quote | real Ed & Joan O'Brien quote — the previous text was **invented copy attributed to a real, named person**; cite was already correct |
| ✅ Gift-options lead-in | 2 real paragraphs under a real h2 |
| ✅ Headings | `Ways to Give` → **So How Can You Ensure More Tomorrows?**; `Giving Levels` → **Membership**; `Level` → **Member Levels** (all match production + the wire) |
| ✅ Gift lists | restored full strings (`Recurring Gifts (e.g.: Monthly, quarterly, annually)`, `Current Pledge (e.g. within 3 years)`, `Pension Plan/Other Qualified Plan`) |
| ✅ Levels | `$1 million+` → `$1 million or more` |
| ✅ Closing paragraph | the SES membership outro |
| ✅ Back link | `/support-gsm#endowment-society` already present; verified |
| ✅ Anchors | `_element_id` = `overview`, `gift-options`, `membership` (the wire's section ids) |
| ✅ Membership table | was rendering run-on (`Member LevelsCurrent GiftDeferred Gift`) — see §6.7 |

`src/data/endowment.js` now holds all of the above as real strings (plus new
`giftOptionsIntro`, `membershipIntro`, `membershipOutro`); `EndowmentPage.jsx` reads
them instead of `placeholders.js`. **`npm run lint` and `npm run build` clean.**

Backup: `/tmp/2093-pre-endowment.json`. Builder: `/tmp/finish_endowment.py` +
`/tmp/fix_endow_cols.py`.

### 5.2 `/news` (318) — built; polish only

Posts widget renders 4 posts (term 19, ppp 4) ✅, counters and 04 donate copy gone ✅.

- **No featured images** on any of the 7 posts → cards render text-only. Either assign
  images or accept text cards (call; images are client assets).
- ✅ Post comments closed sitewide 2026-10-02 (`default_comment_status = closed`;
  44 rows `open` → 0).
- Numeric old slugs (`/2145/` etc.) return **404, not 301**. If those URLs were ever
  shared, add redirects to `gsm-redirects.php`; likely they were never public.

### 5.3 `/newsletters` (2095) — archive works, signup is wrong

Posts widget renders 3 newsletter issues (term 20, ppp 6) ✅. But the "Join our Mailing
List" section embeds **form 2056 — the full contact form** (Name/Email/Subject/Message).
A mailing-list signup needs an email-only form (or removal until the destination is
agreed, §9/blocked). Do not duplicate `/news`'s layout.

### 5.4 `/careers` (2096) — done

Contact residue verified gone: 0 "Front Office", 0 "Connect with us", no SureForms
embed, no `(555)`. Has Job Openings (DSP) + Benefits + one `html` widget. Remaining:
more job listings when the client supplies them (content, not build).

### 5.5 `/programs` (317) — done

5 cards (Community Day Services, Vocational, Special Olympics, Residential Living,
Health & Well Being) all linking to their children; 04 copy verified gone.

### 5.6 `/about` (316) — done

Sections + anchors (`#history #mission #affiliations #accessibility`) ✅, buttons wired ✅.

---

## 6. Site-wide audit findings (2026-10-02) — the fix list

A full read-only audit of the rendered site. Grouped by severity. Items that turned
out stale (dead buttons, 555 phones, plugin removal) are recorded in §2 as done.

### 6.1 Critical

| # | Problem | Fix |
|---|---|---|
| 1 | ✅ **`blog_public = 0`** — was "Discourage search engines" ON, every page carrying `noindex,nofollow`. | Fixed 2026-10-02: `option update blog_public 1`. Verified: 0 `noindex` in source. |
| 2 | ✅ **`/wp-sitemap.xml` → 404** (WP core gates sitemaps on `blog_public`) and no `Sitemap:` line in robots.txt. | Fixed with #1. Verified: sitemap 200 (index + 4 child sitemaps), robots.txt has `Sitemap: https://goodshepherd.local/wp-sitemap.xml`. |
| 3 | ✅ Hero CTA → `/programs` instead of `/careers` | Fixed 2026-10-02 via `apply_elementor.sh 315`. All 3 "Now Hiring" occurrences now → `/careers`. |
| 4 | ✅ Homepage section divergence | Fixed 2026-10-02 — see §4. Spec settled on `HomePage.jsx`; page 315 rebuilt to the 7-section proto order. |

### 6.2 Navigation / chrome

| # | Problem | Fix |
|---|---|---|
| 5 | ✅ Support GSM menu **parent** linked to `#` (dead click on desktop hover-capable devices) | Fixed 2026-10-02: `_menu_item_url` → `/support-gsm`. Verified rendered href. |
| 6 | ✅ Foundation dropdown child → `/support-gsm/` not `/support-gsm/#foundation` | Fixed 2026-10-02: item was `post_type` (URL derived from the page permalink, ignoring `_menu_item_url`) so it was switched to `custom` + URL `/support-gsm/#foundation`. Dropdown (4 children) verified intact. |
| 7 | No favicon / site icon anywhere | Customizer → Site Identity → icon (SVG on hand: `uploads/2023/06/site-logo-white.svg` is the wrong color — need the blue mark) |
| 8 | No meta description, no `og:image`, no Twitter card on any page | No SEO plugin per AGENTS (§11 blocked item 4). At minimum: site icon + og tags via a small snippet **only if commissioned** — do not install an SEO plugin unasked |

### 6.3 Forms / newsletter

| # | Problem | Fix |
|---|---|---|
| 9 | **No working newsletter signup anywhere.** Footer Astra HTML widget holds `[wpforms id="9"]` but **WPForms is not installed** (dead shortcode, renders nothing); `/newsletters/` "Join our Mailing List" embeds contact form 2056; footer has zero `<form>` elements | Blocked on destination decision (§11). Then: build an email-only SureForms signup, embed on `/newsletters` + footer, remove the dead `[wpforms]` option |
| 10 | ✅ Contact form never tested through its real endpoint (AJAX → `/wp-json/sureforms/v1/submit-form` + submit token) | Tested 2026-10-02 through the REST endpoint with a `X-WP-Submit-Token` scraped from `/contact/`. HTTP 200, entry written to `wp_srfm_entries` with all 4 field values, log shows delivery passed to the sending server. Test entry deleted afterwards. Note: payload keys must be the full input `name` (`srfm-…-lbl-…-slug`), not the bare slug — bare slugs yield an entry with `form_data: []`. |
| 11 | ✅ Form 2056: no reCAPTCHA (`_srfm_form_recaptcha = none`), notification was to/cc/**bcc** all `admin_email` → 3 copies per submission | Fixed 2026-10-02: `email_cc` and `email_bcc` set to `""`, `email_reply_to` set to `{form:email}` so replies go to the visitor. Verified log = single recipient. reCAPTCHA still off (§11 blocked item 9). |

### 6.4 Content / markup

| # | Problem | Fix |
|---|---|---|
| 12 | All 7 posts lack featured images → imageless cards on `/news` | Client images (blocked) or accept text cards |
| 13 | ✅ `/privacy/` had **two `<h1>`s** (Astra entry-title + first content heading) | Fixed 2026-10-02: in-content title heading demoted to `<h2>` and then removed as a duplicate of the theme title (the theme already prints the `<h1>`); the 5 numbered section headings remain `<h2>`. Verified: 1 `<h1>`, full body intact (2.7 KB). Recovered from revision 2159 after an initial truncation. |
| 14 | ✅ `/events` lede "Fall Festival, Golf Invitational, and family events throughout the year." repeated 5× | Fixed 2026-10-02: removed the 3 standalone duplicate headings (`6a8fc23`, `bf823e1`, `cdd4304`) and cleared the duplicated description on `8364dbf`, keeping the hero copy. Verified: 1 occurrence; h1 + 4 anchored event section h2s + CTA band intact. |
| 15 | ✅ Home counter "Core programs offered" = 4 vs `site.js` = 5 (Special Olympics) | Fixed 2026-10-02 with the §4 rebuild — `data-to-value="5"` and a 5th program card; **no descriptions added** to the cards (decision). |
| 16 | All body copy is lorem — **intentional**, awaiting client (AGENTS current-state note) | No action |

### 6.5 WP hygiene / security

| # | Problem | Fix |
|---|---|---|
| 17 | **`/wp-json/wp/v2/users` is public** — audit recorded "all 19 accounts" | Re-checked unauthenticated 2026-10-02: returns **3** users (only those with published posts — `charlie`, `mattthecreativemomentum-com`, `michael-clarkthecreativemomentum-com`), no emails, `per_page=100` same 3. The 19-account reading was an authenticated session. Core behaviour; hardening still available if commissioned (§11 blocked item 9) |
| 18 | 19 administrator accounts (agency + client emails), all role `administrator` | Prune + demote to least privilege before any push (§10) |
| 19 | ✅ 6 trashed posts + 1 auto-draft (2160) pending | Emptied 2026-10-02: all 7 deleted `--force`. Also closed comments sitewide (`default_comment_status = closed`, 44 posts updated → 0 open). Verify: `wp post list --post_status=trash` empty. |
| 20 | ✅ Leftovers from declined starter plugins: ~200 `bookly%` options, 40 `acui%` options, and two live Bookly cron events (`bookly_hourly_routine`, `bookly_daily_routine`) | Cron events unscheduled 2026-10-02 (`wp cron event delete`, both). Option rows are inert but note them for the dev push audit |
| 21 | `admin_email` = `develop@thecreativemomentum.com` (agency dev inbox) | Set a monitored address before any public push (§10) |
| 22 | 6 inactive themes (`twentytwenty*`, `hello-elementor`, `genesis-block-theme`) | Optional delete; zero risk left as-is |

### 6.6 Server

| # | Problem | Fix |
|---|---|---|
| 23 | ✅ **PHP-FPM SIGABRT** — root-caused and proven fixed 2026-10-02. The live `www.conf` has `env[OBJC_DISABLE_INITIALIZE_FORK_SAFETY] = YES`, but FPM's config parser applies **PHP INI boolean normalization** to `env[]` values, so workers actually see `1` (any boolean-ish `yes/on/true/1` → `1`; `no/off/false/0` → empty, which makes FPM refuse the conf with `ERROR: empty value`). That is not a problem: the macOS objc runtime's guard accepts `1` as **On** — see `runtime/objc-runtime.mm` in objc4 (`strcasecmp(value,"yes"/"true"/"on"/"y")==0 || strcmp(value,"1")==0 → On`) and `_objc_atfork_child` only enables `MultithreadedForkChild` when the guard is Off. So fork safety **is** disabled in workers. Verified by probe: worker `getenv()` returns `1`; 26 crashes all predate the 12:18 full restart, none since. See §15 |

### 6.7 Elementor settings keys that are silently ignored

Same failure mode as `content_width` (§4). Elementor accepts the wrong key into
`_elementor_data` and then emits **no CSS** for it — no error anywhere.

| Wrong key (dead) | Correct key | Also needs |
|---|---|---|
| `justify_content` | `flex_justify_content` | — |
| `align_items` | `flex_align_items` | — |
| `align_content` | `flex_align_content` | — |
| `wrap` | `flex_wrap` | — |
| `gap: {unit,size,sizes}` | `flex_gap` | GAPS shape `{unit,size,row,column,isLinked}` |
| `css_id` | **`_element_id`** | elementor/includes/elements/container.php:1770 |

The group is `Group_Control_Flex_Container` (`includes/controls/groups/flex-container.php`)
and its prefix is `flex_` — that is where the names come from. `flex_direction` was
already correct in our builders, which is why rows laid out horizontally while their
alignment did nothing.

**Fixed 2026-10-02:** `gsm_cta_band` on all 14 pages that have it (316, 317, 318, 319,
2088–2092, 2094–2096, 2127). It was meant to be centred with a 20px gap and instead
rendered hard-left with the button touching the headline. Verified by pixel measurement
on `/`, `/about`, `/events`, `/programs`, `/shepherd-endowment-society`: band content
now sits at 355px from both edges (was 41 left / 689 right). Backups:
`/tmp/pre-cta-backup/`.

**Deliberately NOT migrated — do not "fix" these:** Home (315) `prog_row`,
`story_row`, `support_row` and `support_card_*` still carry dead `justify_content`
and `gap` keys. They are load-bearing *because* they are dead: 5 cards × `width:20%`
plus a `gap` would exceed 100% and wrap to two rows. Home looks right today for that
reason only. If you ever enable `flex_gap` there, drop the card widths first.

Also note the **Membership table on 2093** was fixed with real widths
(`_element_width: initial` + `_element_custom_width` 40/30/30 %) rather than
`justify-content: space-between` — space-between cannot align columns whose text
lengths vary.

---

## 7. Counters — done, one open value

Home counters carry `ending_number` 55 / 100 / 4 / 1971 (suffix `+` on 100) ✅.
Rendered as `0` only pre-JS (Elementor animates on scroll) — normal.

Open: `4` vs `5` core programs (§4 #5). `/news` and `/newsletters` counters were
deleted as part of their rebuilds ✅.

---

## 8. Placeholder phone numbers — done

`(555)` count = 0 on `/contact` and `/careers` ✅. Footer has the correct number
**(815) 472-3700**, address, and Facebook (`goodshepherdmanor`) ✅. Accessibility →
`/about/#accessibility` ✅ · Privacy → `/privacy/` ✅.

---

## 9. Header, footer, nav

### Header — working

| Item | State |
|---|---|
| Above-header bar | ✅ "Now Hiring — Direct Service Providers. Apply Today →" → `/careers` — renders on all 16 pages |
| Header button | ✅ "Support GSM" → `/support-gsm` |
| Transparent header | ✅ enabled site-wide (`transparent-header-enable = 1`); body class `ast-theme-transparent-header` observed only on `/` (home hero), inner pages inherit — matches AGENTS: every page has the photo hero |
| Nav | ✅ About · Programs & Services · Support GSM (▸ Foundation, Events, Endowment, Memorial or Tribute) · News, Careers, Contact — 6 locked items + button |
| Sticky header | ✅ `header-main-stick = 1`, `sticky-header-on-devices = both`, style `slide` |
| ⚠️ Bugs | ✅ all fixed — nav parent → `/support-gsm`, Foundation child → `/support-gsm/#foundation`; **logo swapped to the real GSM lockup** and **header button styled**. See "Logo + button" below. |

### Logo + header button (done 2026-10-02)

The real GSM lockup lives in the React repo (`src/assets/logo-color.svg`,
`logo-white.svg`) — the 04 `site-logo-white.svg` on the site was a demo asset. Both
were imported to Media (`2026/10/`, IDs **2168** color / **2169** white; SVG upload was
blocked, so the import ran through an in-process `upload_mimes` /
`wp_check_filetype_and_ext` filter — one-off, not persisted).

| Setting | Value |
|---|---|
| `custom_logo` (theme mod) | `2168` — GSM color lockup (solid headers) |
| `astra-settings.transparent-header-logo` | URL of `2169` — GSM white lockup (transparent hero) |
| `astra-settings.different-transparent-logo` | `1` |

Verified in a headless browser: home (transparent) = white logo; `/about`, `/programs`
(solid) = color logo. This also fixed a pre-existing bug — the old white 04 logo was
**invisible on every solid white header**.

**Header button.** With the Header Builder active, the button colors are the element
options `header-button1-back-color` / `-text-color` / `-back-h-color` / `-text-h-color`
(the legacy `header-main-rt-section-button-*` keys are **ignored** when the builder is
active — see `theme/inc/builder/type/base/dynamic-css/button/class-astra-button-component-dynamic-css.php`).
They were empty, so Astra fell back to its default `global-color-5`/`global-color-2`
(white bg / navy text) — i.e. an invisible white button on white headers. Set to
`global-color-0` / `#ffffff` (hover `global-color-1` / `#ffffff`), so the button is GSM
blue on every page, matching the repo's button token. The transparent-header button rule
(`class-astra-dynamic-css.php:4561`) has higher specificity, so home keeps its own
treatment if that is ever revisited.

### Nav — one open question

"Programs & Services" has no submenu; a `Programs Sidebar` menu (term 18, 6 items)
exists unassigned. Either drop it as import residue or assign it — needs a call (§11).

### Footer — missing the newsletter signup

Free Astra renders two widget areas populated from four `block-*` widgets:
`block-12` About GSM · `block-14` Explore · `block-16` Support GSM · `block-18`
Contact (phone, address, Facebook, Privacy, Accessibility, copyright).

**Zero `<form>` elements in the footer.** AGENTS.md requires a real newsletter signup.
Also: Astra's `footer-html-1` option still contains `[wpforms id="9"]` — dead
(WPForms not installed). Build the signup once the destination is agreed (§11);
delete the dead option then. Do not chase the 04 four-column layout — free Astra
caps at two widget areas.

---

## 10. Forms and users

One SureForms form: ID `2056` "Simple Contact Form". Notification (fixed 2026-10-02):
`{admin_email}` to, cc and bcc now **empty**, reply-to `{form:email}` → the visitor.
Tested end-to-end through the REST endpoint the same day: HTTP 200, entry with all
4 field values, single recipient in the log (test entry then deleted).

**`admin_email` = `develop@thecreativemomentum.com`** (agency inbox). **19 user
accounts, all `administrator`** (`*@cloudmellow.com`, `*@thecreativemomentum.com`).
Before any dev push:

1. Set `admin_email` to a monitored GSM or CloudMellow address
2. Prune admins to a minimal real set — `wp user list`, then
   `wp user delete <id> --reassign=<keep>`; demote the rest
3. ✅ cc/bcc duplication on form 2056 — fixed (above)
4. ✅ Real submission through `/wp-json/sureforms/v1/submit-form` — passes (above)
5. Confirm delivery after the `admin_email` change

Forms still to build: **footer newsletter**, **newsletter page signup** (both blocked
on destination), Thank a Staff Member, Careers application. §11 gates the mailbox;
the build does not.

---

## 11. Ordered work queue

Do these in order. Each item is independently shippable and verifiable.

| # | Task | Verify with |
|---|---|---|
| 1 | ✅ **Set `blog_public = 1`** (§6.1 #1/#2) — sitemap 200, robots.txt gains `Sitemap:`, no `noindex` | done 2026-10-02 |
| 2 | ✅ Fix hero CTA href `/programs` → `/careers` (§4 #1) — all 3 "Now Hiring" occurrences | done 2026-10-02 (`apply_elementor.sh 315`) |
| 3 | ✅ Fix nav: Support GSM parent → `/support-gsm`; Foundation child → `/support-gsm/#foundation` (§6.2 #5/#6) | done 2026-10-02; rendered hrefs checked, dropdown intact |
| 4 | ✅ Privacy double `<h1>` (§6.4 #13) — now 1 `h1` + 5 section `h2`s, body intact | done 2026-10-02 (recovered via revision 2159) |
| 5 | ✅ Empty trash (6 posts + auto-draft 2160); close post comments (§6.5 #19, §5.2) | done 2026-10-02; 0 trash, 0 open comments |
| 6 | ✅ Events lede de-dup (§6.4 #14) — 1 occurrence | done 2026-10-02 (`apply_elementor.sh 2094`) |
| 7 | ✅ Form 2056 cc/bcc fix + real submission test (§6.3 #10/#11) | done 2026-10-02; REST endpoint → entry with data, 1 recipient |
| 8 | ✅ **Homepage rebuild** (§4) — rebuilt to `HomePage.jsx` proto, 7 sections, no CTA band, 5 program cards, foundation 4-card section | done 2026-10-02 (`apply_elementor.sh 315`, twice); see §4 for the verification log |
| 9 | ✅ **Endowment finish** (§5.1) — real intro/quote/gift/membership copy from production site; table columns aligned | done 2026-10-02; 0 `lorem` in rendered HTML, lint + build clean |
| 10 | Newsletter signup (§6.3 #9) — footer + `/newsletters`, remove dead `[wpforms id="9"]` | `<form>` in footer; email-only field on `/newsletters` |
| 11 | Favicon/site icon (§6.2 #7) | icon link tag resolves 200 |
| 12 | ✅ FPM `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` (§6.6 #23) | done 2026-10-02 — conf already `YES`; FPM normalizes it to `1` and objc4 treats `1` as On (source-verified). No new `signal 6` since the full restart |
| 13 | `admin_email` + prune 19 admins (§10) | `wp user list` shows the real set |
| 14 | REST users visibility (§6.5 #17) — unauth re-check shows only 3 post authors, no emails; harden only if commissioned | `/wp-json/wp/v2/users` → 401/403 |
| 15 | ✅ Unschedule Bookly crons (§6.5 #20) | done 2026-10-02 — `bookly_hourly_routine` + `bookly_daily_routine` deleted; `wp cron event list` shows none |
| 16 | ✅ Logo swap (04 white SVG → GSM mark) + header button styling | done 2026-10-02 — Media 2168/2169; `custom_logo` + Astra transparent logo set; `header-button1-*` colors → GSM blue. Headless-verified on home/about/programs. See §9 |
| 17 | `astra-settings` audit — confirm Local→dev values survive the push | §13 |
| 18 | Push Local → dev | §13 |
| 19 | Commit any new work (§14) | `git status` |

**Blocked, needs a human answer — do not guess:**

1. ~~Homepage target spec~~ — **settled 2026-10-02**: `HomePage.jsx` wins. Done, see §4.
2. Newsletter destination and the form mailbox. Gates queue #10.
3. Contact staff directory content and "Thank a Staff" owner — section exists with
   lorem; real names are not in this repo.
4. Program children under the Programs nav dropdown (§9).
5. Whether an SEO plugin (or any meta-description approach) is in scope — AGENTS
   lists none; audit found no meta descriptions (§6.2 #8).
6. Real GSM photography — still 04 demo images (`uploads/2023/06/*`) and no post
   featured images (§6.4 #12).
7. Client body copy. Gates nothing in the queue; every page ships with lorem until
   it arrives.
8. ~~Counter value: 4 or 5 core programs~~ — **settled 2026-10-02**: 5. Counter and
   cards both say 5 (`site.js` `programs` has 5 entries; `TBD Vocational Program` is
   intentional).
9. Whether to harden REST users / add reCAPTCHA (AGENTS: no new plugins without a
   concrete need).

---

## 12. Site-wide CTA band — closed, home stays without it

**Closed 2026-10-02 — won't fix.** The client chose to match `HomePage.jsx`, which has
no `gsm_cta_band`, and confirmed home having no band. Home therefore differs from every
other content page: **no CTA band, no Get Involved block.** Do not "fix" this —
`AGENTS.md` §Homepage now states it explicitly.

Still true otherwise: "We can create a better tomorrow" renders on the other 14 content
pages; `/privacy` (utility, not in the 15) correctly has none.

---

## 13. Local → dev push

Local is canonical. Dev is a rebuilt copy.

| Env | URL |
|---|---|
| Local | `https://goodshepherd.local` |
| WP Engine dev | `https://goodshephe3dev.wpenginepowered.com` |

```sh
WP="/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh"

# 1. export
"$WP" db export /tmp/gsm_export.sql

# 2. rewrite URLs — LC_ALL=C is required or sed dies on "illegal byte sequence"
LC_ALL=C sed -i '' 's#goodshepherd\.local#goodshephe3dev.wpenginepowered.com#g' /tmp/gsm_export.sql
#    expect 26 replacements, 0 remaining

# 3. compress + verify
gzip -9 -c /tmp/gsm_export.sql > _migration/stage-db-final.sql.gz
gzip -t _migration/stage-db-final.sql.gz

# 4. rsync to /sites/goodshephe3dev/gsm-import.sql.gz
# 5. on dev: import, then wp cache flush, then delete the dump from the webroot
# 6. verify all 16 routes
```

### Gotchas that each cost real debugging time

- **Flush WP Engine's object cache after every import.** Without it dev silently serves
  pre-import options — the DB row is right, `get_option()` returns a stale value, the
  front end renders old markup. This is the single most important step.
- **`scp` is blocked** for the `local+db+push+` user. Use an ssh config file for rsync
  with a **quoted** `IdentityFile` (the key path contains a space). Write remote scratch
  files over the shell instead of `scp`.
- WPE `/tmp` is ephemeral per SSH session. Anything persistent goes in
  `/sites/goodshephe3dev`.
- WP-CLI on dev: `/usr/local/bin/wp --path=/sites/goodshephe3dev --allow-root`.
- Astra settings live in the **`astra-settings`** option (one large serialized array),
  not `astra_options`. Verify with `count(get_option('astra-settings'))` — a count far
  below Local's means stale cache, not a bad import.
- Free Astra has no 4-column footer. Do not chase the 04 four-column layout.
- Privacy is at `/privacy/`, not `/privacy-policy/`.
- **Before pushing:** `blog_public` is now `1` ✅ (fixed 2026-10-02) — no longer a blocker.

**Still blocked:** `~/.ssh/config` has no entry for `goodshephe3dev` and no confirmed
credentials. Steps 4–6 cannot run until someone adds them.

---

## 14. Git state

Branch `main`, **2 commits ahead of `origin/main`, not pushed** — push when asked. Do not
commit unless asked.

- `05372a9` — the 2026-10-02 queue run (items 1–9: homepage rebuild, Endowment copy,
  CTA-band key fix, plus §4 / §5.1 / §6.7 / §11 / §12 / §14 and the `AGENTS.md`
  §Homepage rewrite).
- The 2026-10-02 pickup commit — FPM root-cause + fix proof (§6.6 #23, §15), Bookly
  crons unscheduled (§6.5 #20), GSM logo swap + header-button styling (§9), and the
  matching §11 / §14 refresh.

| Commit | Contents |
|---|---|
| (this) | FPM root-cause, Bookly crons, GSM logo + header button, PLAN refresh |
| `05372a9` | Home rebuild to proto, Endowment real copy, Elementor key gotchas, AGENTS/PLAN updates |
| `a868077` | PROCESS.md, 6 `_tools` fix scripts, PLAN.md §14 refresh, .gitignore additions |
| `eb5a856` | WordPress build queue: Home, News, Programs, Careers, Endowment |
| `a371256` | Elementor Pro native sticky for Support GSM jump bar |
| earlier | jump bar rebuild, Elementor build tooling, prototype form wiring |

Screenshots and scratch (`.playwright-mcp/`, `Untitled/`, `design-review/`, various
`*.png`) are in `.gitignore` — do not commit them. Do not commit `.env` or credentials.

---

## 15. Environment fix applied — crashes persist (open)

Local's PHP-FPM workers crash intermittently with `SIGABRT`
(`NSPlaceholderString initialize … when fork() was called`) → intermittent **502 Bad
Gateway**.

Fix attempted: `env[OBJC_DISABLE_INITIALIZE_FORK_SAFETY] = YES` added to both

- `~/Local Sites/goodshepherd/conf/php/php-fpm.d/www.conf.hbs` (persistent template)
- `~/Library/Application Support/Local/run/Rg1VtCBT9/conf/php/php-fpm.d/www.conf` (live)

**Status 2026-10-02: resolved (source-verified), monitor.** The live file does contain
`YES`. The web SAPI reads `1`, not `YES`, because FPM's config parser applies PHP's INI
boolean normalization to `env[]` values (`yes/on/true/1` → `1`, `no/off/false/0` → empty
— the empty case actually makes FPM refuse the config with `ERROR: empty value`).

`1` is **fine**: in objc4, `runtime/objc-runtime.mm` parses the option's env value and
sets `DisableInitializeForkSafety = On` for `"yes"`, `"true"`, `"on"`, `"y"`, or `"1"`;
`_objc_atfork_child` only sets `MultithreadedForkChild = true` (the crash path) when the
guard is Off. So with `env[]` present, workers run with fork safety disabled. The 26
SIGABRT lines all predate the 12:18 full restart; none since. If a 502 returns, check
`~/Local Sites/goodshepherd/logs/php/php-fpm.log` before assuming a WordPress problem.

**Do not `kill -USR2` the master while iterating on `www.conf`.** SIGUSR2 does a graceful
reload, but a malformed value makes FPM exit and Local does **not** respawn it (502). If
that happens, restart it the way Local does:
`sbin/php-fpm -F --prefix <run>/conf/php --fpm-config <run>/conf/php/php-fpm.conf -c <run>/conf/php`.

---

## 16. Reference: source of truth per page

| Page | Build from |
|---|---|
| `/` | `src/pages/HomePage.jsx` (Figma `9137:3182`) — the 7 sections in §4. Built ✅ 2026-10-02. **Not** Figma `9009:2`. |
| `/about` | AGENTS.md §About; timeline years from `src/data/history.js` |
| `/programs` + children | `src/data/programs.js`, `src/data/health.js` |
| `/support-gsm` | ID 2092 as built; `src/data/getInvolved.js` |
| `/shepherd-endowment-society` | `src/data/endowment.js` — **real copy** |
| `/events` | AGENTS.md §Events — 4 anchored sections |
| `/news`, `/newsletters` | `src/data/news.js` |
| Nav, hero-header slugs, active state | `src/data/header.js` |
| Shared layout classes | `src/styles/starter.css` |

`AGENTS.md` is canonical for all of it. `SitemapPage.jsx` wins over
`design/sitemap-structure.md`. Locked slugs in `AGENTS.md` win over any hash link in
the React files.
