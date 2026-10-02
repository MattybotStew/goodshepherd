# GSM — Build Plan (WordPress / Elementor)

**Read `AGENTS.md` first.** It is canonical for IA, slugs, palette, stack, and hard
rules. This file is the *state of the build and what remains*. If they disagree,
`AGENTS.md` wins.

This file is written to be handed to any model or tool (Cursor, Claude Code, Cline,
Gemini CLI) without prior conversation context. Every claim here was verified against
the running site on 2026-10-01.

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
| Last commit | `a371256 Use Elementor Pro native sticky for Support GSM jump bar` |

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
| Elementor Pro | 4.3.1 active, license `ACTIVE` through 2027-04-26 (`sticky`, `custom-css`, `custom_code`) |
| Astra Pro addon | 4.13.10 active — above-header bar and sticky header work |
| SureForms | 2.12.8 active — one form, ID `2056` |
| Palette | `--ast-global-color-0..7` = `#0089DF #006BB3 #002A4E #303336 #FAFCFE #FFFFFF #C8D4E0` ✅ |
| Type | DM Sans ✅ · container 1200px ✅ · no 04 lime anywhere ✅ |
| Astro global colors live in the theme's dynamic CSS, not in a `astra-global-color-palette` option — do not go looking for one |

### Plugins to remove

| Plugin | Why |
|---|---|
| `ultimate-elementor` 1.45.5 | Starter import junk. Adds ~20 shortcodes/blocks nothing uses, and can conflict with Elementor's own addons. Deactivate + delete. |
| `wordpress-seo` 28.5 | Inactive. Delete unless SEO is explicitly commissioned — AGENTS.md lists no SEO plugin. |
| `astra-pro-sites` 4.7.7 | Only needed to re-import the starter. The import is done. Delete before push. |

---

## 2. Page inventory — all 16 routes return 200

| ID | Slug | Parent | `_elementor_data` | Build state |
|---|---|---|---|---|
| 315 | `/` | — | 98 KB | Needs section fixes — see §4 |
| 316 | `/about` | — | 64 KB | Mostly built; dead buttons |
| 317 | `/programs` | — | 38 KB | Still 04 copy; needs program cards |
| 2088 | `/programs/community-day-services` | 317 | 20 KB | ✅ Built |
| 2089 | `/programs/vocational` | 317 | 21 KB | ✅ Built |
| 2090 | `/programs/residential-living` | 317 | 21 KB | ✅ Built |
| 2091 | `/programs/health-well-being` | 317 | 21 KB | ✅ Built, all 5 anchors ✅ |
| 2127 | `/programs/special-olympics` | 317 | 19 KB | ✅ Built |
| 2092 | `/support-gsm` | — | 31 KB | ✅ Reference build — see §3 |
| 2093 | `/shepherd-endowment-society` | — | 8 KB | ❌ Nearly empty — see §5 |
| 2094 | `/events` | — | 48 KB | ✅ 4 event anchors ✅ |
| 2095 | `/newsletters` | — | 61 KB | ❌ 04 Stories clone — see §5 |
| 2096 | `/careers` | — | 36 KB | ❌ Inherits Contact's contact block — see §5 |
| 318 | `/news` | — | 62 KB | ❌ Static cards, 0 posts — see §5 |
| 319 | `/contact` | — | 36 KB | ⚠️ Built; placeholder phone numbers |
| 3 | `/privacy` | — | 0 | Utility page, still WP suggested text |
| 2011 | `/ways-to-give` | — | — | `draft`. Redirect covers it. Trash it. |

**Verified anchors:** Health `#nursing #clinic #pharmacy #supports #transportation` ·
Events `#fall-festival #brunch-auction #golf-invitational #family-events` ·
Support GSM `#foundation #ways-to-give #endowment-society #events #memorial-tribute` ·
About `#accessibility`.

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
- Verified: 5 tabs, 5 hrefs, 5 active states, 69px bar, mobile horizontal scroll with no
  document overflow, native sticky activates on scroll, correct desktop image-side
  mapping, no console errors

**`apply_elementor.sh` matters.** Elementor's CSS cache does not regenerate on a raw
`_elementor_data` meta write. The script clears Elementor's cache, instantiates
`Elementor\Core\Files\CSS\Post`, calls `update()`, and fails if
`uploads/elementor/css/post-<ID>.css` was not touched. Always use it. Never write
`_elementor_data` directly and expect styles to follow.

### Redirect

`_migration/mu-plugins/gsm-redirects.php` → `wp-content/mu-plugins/gsm-redirects.php`.
Currently: `/ways-to-give/` → 301 → `/support-gsm/#ways-to-give` ✅ verified.
Local runs nginx, so `.htaccess` is not an option. Add redirects here.

---

## 4. Homepage `/` (ID 315) — 6 containers, wrong in 4 places

Current container order: `[0]` hero · `[1]` intro strip · `[2]` About Us ·
`[3]` Our Mission & Vision + counters · `[4]` Get Involved · `[5]` Our Partners

AGENTS.md requires this order instead:

1. Hero — headline "A Community of Compassion, Dignity, and Purpose." **CTA must be
   "Now Hiring! Apply Today" → `/careers`** (currently reads "Donate Now", unlinked)
2. Intro strip overlapping hero — three cards `01. Projects` / `02. Support GSM` /
   `03. Donate`, greeked body, "Learn more" → `/programs`, `/support-gsm`,
   `/support-gsm`. Card titles are currently missing; only the `01.` `02.` `03.`
   headings and the buttons render.
3. Our Impact — "Our Mission & Vision: Serving with Dignity" + mission statement +
   4 counters. **No donate band in this section.** Counter titles are right, values
   are empty (see §6).
4. About Us — "A community of care, growth, and dignity for over 50 years." + photo
   mosaic, shares `#f1f5f9` with Our Impact (no gradient seam)
5. Support GSM Foundation CTA band — "We can create a better tomorrow" + Support GSM
6. Our Programs & Services — program cards + View all
7. Stories — "Inspiring tales of transformation" + 3 story cards

**Deltas:**

| Fix | Detail |
|---|---|
| Hero CTA | "Donate Now" → "Now Hiring! Apply Today" → `/careers` |
| Intro strip | Add the three card titles; wire all three buttons |
| Remove | `[5]` "Our Partners" — not on the wire |
| Add | Our Programs & Services cards + View all |
| Add | Stories: 3 cards from `src/data/news.js` |

**"Our Partners" is the trap.** AGENTS.md says explicitly: *do not replace this Home
layout with the 04 01/02/03 / stories / partners pattern.* Home follows the Figma wire
(`9009:2`), not the starter's homepage.

---

## 5. Pages that need real work

### 5.1 `/shepherd-endowment-society` (2093) — effectively empty

8 KB of `_elementor_data`, one `image-box` widget. Needs the Donate-page layout
duplicated and filled from `src/data/endowment.js` — **that file already holds real
copy pulled from the live production site**, so this page can be finished now, before
client review. It is the only page with real body copy. Sections: intro, how gifts are
used, gift methods, gift levels, a CTA band, and a link back into
`/support-gsm/#endowment-society`.

### 5.2 `/news` (318) — needs to be a real post archive

AGENTS.md: **News & Updates = WordPress posts + category archive.** Currently it is a
static Elementor page with 04 "Stories" copy, 04 impact counters
("People served worldwide / Projects funded / People to take action / Partner
organizations" with `M+`/`M` suffixes), a donate band, and four hardcoded story cards.

- Add 4 placeholder posts in the `news` category so the archive renders
- Rebuild the page as a post-listing template, not static cards
- Delete the 04 counters section and the donate band
- Delete the two `auto-draft` posts (IDs 2075, 2076) first
- Use `src/data/news.js` for the card titles/excerpts

### 5.3 `/newsletters` (2095) — a `/news` clone with 04 counters

Same problem: 04 Stories copy, 04 counters, donate band, hardcoded cards. Needs an
archive of newsletter issues (posts in a `newsletters` category) plus a real signup
form. Do not duplicate `/news` — build this one after it and share the listing layout.

### 5.4 `/careers` (2096) — cloned from `/contact`, inheriting the wrong sections

Rendered output on `/careers` includes Contact's hero copy ("Connect with us for more
information…"), a "Phone" block, "Ways to Give", "Get in touch", "Front Office", and
"Follow us on". Those do not belong here.

- Keep: Job Openings (incl. DSP listing) and Benefits — both present ✅
- Remove: the inherited Contact contact-info block and the "Connect with us" hero copy
- The `sureforms` contact form (2056) is currently embedded here too. Careers needs an
  application form or a mailto, not the Contact form.
- `google_maps` is correctly absent from Careers and correctly present on Contact ✅
  (the reverse of an old note in the previous plan)

### 5.5 `/programs` (317) — landing page still has 04 copy

Renders "Every small act of kindness creates a ripple of positive change", "How we
work", "Proofing our impact", "Join us in our mission to create a positive impact on
the world." — all 04 starter copy. Needs:

- Intro (`ProgramsIntroSection` equivalent)
- Cards for all **five** programs: Community Day Services, Vocational, Special Olympics,
  Residential Living, Health & Well Being — from `src/data/programs.js`
- View-all link

### 5.6 `/about` (316) — nearly right

Sections present: Dignity/ Purpose, `01. Our History`, `02. Mission, Vision & Values`,
`03. Affiliations`, History timeline, `#accessibility` ✅. Only the dead buttons
(§6) need fixing. Also per AGENTS.md: Accessibility lives here, and the hero overlaps
the mission section.

---

## 6. Dead buttons — every page has some

These buttons render but carry **no `href` at all**. They are not styling placeholders;
they are broken CTAs. 15 across the site:

| Page | Unlinked buttons |
|---|---|
| `/` | Donate Now, Learn More ×2, View Programs, Read More ×3, Get Involved |
| `/about` | Our Impact, Ways to Give, Learn More, Donate Now |
| `/programs` | Learn More, Our Impact |
| `/events` | Learn More ×2 |
| `/news` | Donate Now, Read More ×4 |
| `/newsletters` | Donate Now, Read More ×4 |

**Destinations** (from `src/data/header.js` + AGENTS.md, never the 04 originals):

| Label | Goes to |
|---|---|
| Read More / story cards | the post permalink |
| Learn More (intro strip) | `/programs` · `/support-gsm` · `/support-gsm` |
| View Programs | `/programs` |
| Our Impact / Ways to Give (About) | `/about#mission` · `/support-gsm#ways-to-give` |
| Donate Now | `/support-gsm/#ways-to-give` |
| Get Involved | `/support-gsm` |
| View all (stories) | `/news` |
| See all events → | `/events` |
| Support GSM (any band) | `/support-gsm` |
| Apply Today / Now Hiring | `/careers` |

Verify after fixing with:

```sh
python3 - <<'PY'
import json,re,subprocess
for pid,slug in {315:'/',316:'/about',317:'/programs',2094:'/events',318:'/news',2095:'/newsletters'}.items():
    raw=subprocess.run(["/Users/matthewstewart/Local Sites/goodshepherd/_tools/wp.sh",
        "post","meta","get",str(pid),"_elementor_data"],capture_output=True,text=True).stdout
    d=json.loads(raw); bad=[]
    def walk(els):
        for e in els or []:
            if e.get('widgetType') in ('button','btn'):
                t=e.get('settings',{}) or {}
                txt=re.sub(r'<[^>]+>','',t.get('text','')).strip()
                if txt and not ((t.get('link') or {}).get('url') or t.get('link')): bad.append(txt)
            walk(e.get('elements'))
    walk(d)
    print(f"{slug:16} {bad or 'none'}")
PY
```

---

## 7. Counters render as `0`

Every Elementor counter has empty `start`/`end`/`prefix`. Home renders
`0 · 0+ · 0 · 0`.

**Home and `/about` — use `src/data/site.js` `impactStats`:**

| Value | Label |
|---|---|
| `55` | Years serving our community |
| `100+` | Men supported daily |
| `5` | Core programs offered |
| `1971` | Founded in Momence, IL |

(`src/data/site.js` says `5` core programs — Special Olympics was added as the fifth.
AGENTS.md's older "4 programs" is stale.)

Counter titles on `/` are already correct. `/news` and `/newsletters` counters should be
deleted outright (§5.2, §5.3), not fixed.

---

## 8. Placeholder phone numbers on `/contact` and `/careers`

`(555) 123-2222` and `Fax: (555) 123-2225` appear twice on each page — 04 starter
demo data. This is the exact failure mode AGENTS.md warns about: placeholder copy
becoming real content.

- Real number: **(815) 472-3700**
- Replace both. On Careers, remove the block entirely (§5.4)
- After: `curl -sk <page> | grep -c '(555)'` must return `0`

The footer already has the correct number and address, and Facebook
(`goodshepherdmanor`) ✅. Footer's Accessibility → `/about/#accessibility` ✅ and
Privacy → `/privacy/` ✅.

---

## 9. Header, footer, nav

### Header — working, two things to confirm/fix

| Item | State |
|---|---|
| Above-header bar | ✅ "Now Hiring — Direct Service Providers. Apply Today →" → `/careers` |
| Header button | ✅ "Support GSM" → `/support-gsm` |
| Transparent header | ✅ enabled |
| Nav | ✅ About · Programs & Services · Support GSM (▸ Foundation, Events, Endowment, Memorial or Tribute) · News · Careers · Contact |
| Sticky header | ⚠️ `sticky-header-on-devices = both`, `sticky-header-style = slide`, but the bare `sticky-header` toggle key is **unset**. Open the site, scroll, and confirm the header sticks. If not, set it in the Customizer. |
| Header logo | ⚠️ Still the 04 white SVG (`site-logo-white.svg`) |
| Header button style | ⚠️ Renders as `ast-custom-button` (plain text), not a styled button |

### Nav — one open question

The primary nav's "Programs & Services" item has **no submenu**, but Programs is a
parent page with five children and AGENTS.md wants breadcrumbs and a hierarchy. A
`Programs Sidebar` menu (term 18, 6 items) exists — it is not assigned to the primary
location. Either drop it as leftover import data, or assign it. Needs a call; do not
add nav items without one.

### Footer — missing the newsletter signup

Free Astra renders two widget areas (`footer-widget-1`, `footer-widget-2`) populated
from four `block-*` widgets:

- `block-12` About GSM · `block-14` Explore (6 links)
- `block-16` Support GSM · `block-18` Contact (phone, P.O. Box, Facebook, Privacy,
  Accessibility)

**There is no newsletter form anywhere in the footer — zero `<form>` elements.** The
"Newsroom" text that reads like a signup is a static link to `/newsletters/`. AGENTS.md
requires a real newsletter signup in the footer. Build it once the signup destination
is agreed (§11).

Note `advanced-footer-widget-1`/`-2` also hold `block-12`/`block-13`. That is Astra Pro
advanced-footer residue; free Astra renders the two small-footer areas. Do not chase the
04 four-column layout — it is not available on free Astra.

---

## 10. Forms

One SureForms form exists: ID `2056` "Simple Contact Form". Email notification is
`{admin_email}`.

**`admin_email` = `develop@thecreativemomentum.com`** — the agency inbox. 19
administrator accounts exist, mostly `*@cloudmellow.com` and
`*@thecreativemomentum.com`. Before any dev push:

1. Set `admin_email` to a monitored GSM or CloudMellow address
2. Prune admins to a minimal real set — `wp user list`, then `wp user delete <id> --reassign=<keep>`
3. Confirm the form renders and delivers after both changes

Forms still to build: footer newsletter, newsletter page signup, Thank a Staff Member,
Careers application. §11 gates the mailbox; the build does not.

---

## 11. Ordered work queue

Do these in order. Each item is independently shippable and verifiable.

| # | Task | Verify with |
|---|---|---|
| 1 | Remove `ultimate-elementor`, `wordpress-seo`, `astra-pro-sites` | `"$WP" plugin list` |
| 2 | Fix `(555)` phone on `/contact`; remove the contact block from `/careers` | `curl -sk <page> \| grep -c '(555)'` → `0` |
| 3 | Populate the 4 home counters from `src/data/site.js` | rendered values `55 / 100+ / 5 / 1971` |
| 4 | Wire every dead button (§6), homepage first | the verification script in §6 |
| 5 | Homepage rebuild (§4): hero CTA, intro titles, drop Our Partners, add Programs + Stories | 7 sections in order |
| 6 | Build `/shepherd-endowment-society` from `src/data/endowment.js` | 8 KB → 30 KB+ |
| 7 | `/programs` landing — 5 program cards, delete 04 copy | 5 cards link to the 5 children |
| 8 | `/news` — 4 posts + real archive template, drop counters + donate band | `/news` lists posts |
| 9 | `/newsletters` — archive + signup form | `/newsletters` lists issues |
| 10 | `/careers` — remove Contact residue, swap in application form | no "Front Office" on the page |
| 11 | Site-wide CTA band audit (§12) | per-page band check |
| 12 | Footer newsletter signup (§9) | a `<form>` in the footer |
| 13 | `/privacy` — replace WP "Suggested text" boilerplate | no suggested text on the page |
| 14 | Trash page `2011` (`/ways-to-give` draft) | `wp post list --post_status=draft` is empty |
| 15 | Add `/donate` → 301 `/support-gsm` to `gsm-redirects.php` | `curl -skI .../donate/` |
| 16 | Confirm sticky header; fix header button styling; swap the logo | manual scroll test |
| 17 | Forms + admin email + prune users (§10) | form delivers |
| 18 | `astro-settings` audit — confirm the Local→dev values survive the push | §13 |
| 19 | Push Local → dev | §13 |
| 20 | Commit uncommitted work (§14) | `git status` |

**Blocked, needs a human answer — do not guess:**

1. Newsletter destination and the form mailbox.
2. Contact staff directory content and "Thank a Staff" owner. The section exists with
   lorem; the real names are not in this repo.
3. Program children under the Programs nav dropdown (§9).
4. Whether `wordpress-seo` is in scope. It is installed and inactive.
5. Real GSM photography — still 04 demo images (`uploads/2023/06/home-*.jpg`) throughout.
6. Client body copy. Gates nothing in the queue above; every page is meant to ship
   with lorem until it arrives.

---

## 12. Site-wide CTA band — inconsistent

The "We can create a better tomorrow" band appears on `/`, `/about`, `/news`,
`/newsletters`, `/shepherd-endowment-society` — and is **absent** from `/programs`,
`/contact`, `/careers`, `/events`, `/support-gsm`, all program children, and
`/privacy`.

AGENTS.md: the band is site-wide, near the footer, on every page. Decide once, then
make it consistent. The pages missing it are the ones currently reading thin — which is
probably the whole reason they read thin.

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

**Still blocked:** `~/.ssh/config` has no entry for `goodshephe3dev` and no confirmed
credentials. Steps 4–6 cannot run until someone adds them.

---

## 14. Git state

Branch `main`. The WordPress build queue, `_migration/support-gsm-hero.json`,
and `_migration/mu-plugins/gsm-redirects.php` are committed (`eb5a856`). Still
untracked at the time of writing:

| Path | Status |
|---|---|
| `PROCESS.md` | untracked — design workflow doc |
| `_tools/fix_contact_careers.py`, `fix_contact_careers_v2.py`, `fix_home_counters.py`, `wire_home_buttons.py`, `wire_remaining_buttons.py`, `wire_remaining_buttons_v2.py` | untracked — one-off Elementor fix scripts |

Screenshots and scratch (`.playwright-mcp/`, `Untitled/`, `design-review/`,
`design/home.png`, `design-homepage-full.png`, `designs-branch-home-5174.png`,
`dev-home-5173.png`, `gsm-home.png`) are now in `.gitignore` — do not commit
them. Do not commit `.env` or credentials.

Recent commits: `eb5a856` WordPress build queue · `a371256` native sticky jump
bar · `9172f6b` rebuild jump bar with native Elementor controls · `3a74635`
Elementor build tooling · `8cbab17` wire prototype forms.

---

## 15. Environment fix already applied — do not regress

Local's PHP-FPM workers were crashing intermittently with `SIGABRT`
(`NSPlaceholderString initialize … when fork() was called`), which nginx surfaced as
intermittent **502 Bad Gateway** on `wp-admin` pages, including
`wp-admin/plugins.php?bsf-inline-license-form=astra-pro-sites`.

Fix: `env[OBJC_DISABLE_INITIALIZE_FORK_SAFETY] = YES` added to both

- `~/Local Sites/goodshepherd/conf/php/php-fpm.d/www.conf.hbs` (persistent template)
- `~/Library/Application Support/Local/run/Rg1VtCBT9/conf/php/php-fpm.d/www.conf` (live)

**FPM reads `env[]` only at full start** — `kill -USR2` silently does nothing here. The
master had to be killed; Local.app respawns it. If a 502 ever returns, check
`~/Local Sites/goodshepherd/logs/php/php-fpm.log` for a new `exited on signal` line
before assuming a WordPress problem.

---

## 16. Reference: source of truth per page

| Page | Build from |
|---|---|
| `/` | Figma `9009:2` (see AGENTS.md §Homepage for the 7 sections) |
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