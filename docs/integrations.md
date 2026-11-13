# Technical Documentation — Integrations

What the Good Shepherd Manor build is actually wired to, how each piece is configured, what it sends and stores, and which parts are not working yet. Written to be handed to an incoming developer or to QA, not to sell the stack.

**Platform:** WordPress on WP Engine · Local (by Flywheel) is canonical, stage is a rebuilt copy
**Stack as built:** WordPress 7.1.2 · PHP 8.2.29 · Astra 4.14.0 · Elementor 4.3.3 · Elementor Pro 4.3.1 · Astra Addon 4.13.10 · SureForms 2.12.8 · Rank Math 1.0.279 · WebP Converter 6.6.5 · GA Google Analytics 20260810

## 1. Summary

| # | Integration | Purpose | Status |
|---|---|---|---|
| 2 | Elementor | Page canvases | Working |
| 3 | Astra + Astra Addon | Theme, header/footer builder, transparent/sticky header | Working |
| 4 | SureForms | Contact, thank-a-staff, newsletter forms | **Captures** work; **email** blocked |
| 5 | Google Analytics | Traffic measurement | **Placeholder ID — no data** |
| 6 | Rank Math | SEO, sitemaps, indexing control | Working |
| 7 | WebP Converter | Image format conversion | Working |
| 8 | WP Engine | Hosting, page cache, CDN | Working |
| 9 | SMTP / SendGrid | Outbound mail transport | **Unconfigured** |
| 10 | mu-plugins | Redirects, security, SEO, mail | Working (mail inert) |

## 2. Elementor

Every content page except Privacy is Elementor (`_elementor_edit_mode = builder`). Pages are **generated**, not hand-built:

```sh
python3 _tools/build_home_replica.py            # page 315  -> /tmp/home_replica.json
python3 _tools/build_pages.py all               # 13 pages  -> /tmp/page_<id>.json
./_tools/apply_elementor.sh 2088 /tmp/page_2088.json
```

`_tools/elementor_kit.py` is shared by both generators. Output is native container/heading/text/button/image/icon-list widgets — no raw HTML, no custom CSS on the page — so pages stay editable in the Elementor editor.

Hand-editing a generated page in Elementor creates drift the next time the generator runs. Change the script, regenerate, re-apply.

Two Elementor-specific traps already paid for:

- A container with `width` needs `content_width: 'full'` or Elementor emits no `--width` and the card silently stacks at 100%.
- Flex controls are stored with a `flex_` prefix (`flex_justify_content`, `flex_gap`, …). Bare names are accepted into `_elementor_data` and then produce no CSS at all.

Assets URL rule: generated JSON uses root-relative `/wp-content/uploads/...` so the same file applies cleanly to Local and stage. An absolute `goodshepherd.local` URL on stage breaks through the WebP passthru.

## 3. Astra + Astra Addon

Site-wide settings live in the `astra-settings` option (a single large serialized array, ~2,291 keys). Not in code, not in a child theme.

Owned here: colours, typography (DM Sans), 1200px container, header layout, above-header banner (`header-html-1`), footer builder, `footer-copyright-editor`, `footer-html-1` (newsletter template injection).

Astra Addon supplies the transparent header, sticky header, and the four-area footer builder — it is **required**; without it the header and footer degrade.

Do not rebuild header or footer in Elementor Theme Builder.

## 4. SureForms

Three forms, referenced by ID from page content so editing a form needs no page rebuild:

| ID | Form | Used on | Notifies | Reply-to |
|---|---|---|---|---|
| 2056 | Simple Contact Form | `/contact/` | `info@goodshepherdmanor.org` | submitter |
| 2370 | Thank a Staff Member | `/contact/` | `info@goodshepherdmanor.org` | submitter |
| 2202 | Newsletter Signup | every page (template 2375) | `info@goodshepherdmanor.org` | submitter |

- Config store: post meta `_srfm_email_notification` (JSON), `_srfm_form_confirmation`, `_srfm_form_fields`
- Field definitions live in the form post content as block markup
- Submissions are persisted by SureForms inside WordPress and shown under its Entries screen
- **No external CRM or ESP.** The newsletter form does not write to Mailchimp/Constant Contact. List growth requires exporting entries
- **No CAPTCHA and no honeypot** on any form

## 5. Google Analytics — currently inert

Plugin `ga-google-analytics`, option `gap_options`:

| Key | Value |
|---|---|
| `gap_id` | **`G-XXXXXXXXXX`** (placeholder) |
| `gap_location` | `header` |
| `gap_enable` | `2` (enabled) |
| `gap_universal` | `1` |

The plugin is enabled and injecting a tag, but the measurement ID is a placeholder, so **no data is being collected**. Replacing `G-XXXXXXXXXX` with the real GA4 property ID is the only change required. Until then, any report claiming traffic figures for this site is not measuring this site.

## 6. Rank Math

Modules active: `link-counter`, `analytics`, `seo-analysis`, `sitemap`, `rich-snippet`, `local-seo`, `role-manager`.

- Sitemap served at `/sitemap_index.xml`; `/sitemap.xml` 301s to it via mu-plugin
- SureForms URLs (`sureforms_form` post type) are excluded from the sitemap and marked `noindex, nofollow` by `gsm-seo.php` — form URLs are not content
- `blog_public` is `0` on Local. Stage imports as `noindex, nofollow` and this must be flipped on production or the live site ships invisible

## 7. Outbound email — unconfigured

This is the integration with a real, known failure.

**Symptom:** form notifications and password resets vanish. No email, no error surfaced to the user.

**Cause:** the host has no working transport. `sendmail_path` is `/usr/sbin/sendmail -t -i`, and that binary does not exist; nothing listens on `127.0.0.1:25`. PHP `mail()` therefore fails below WordPress, `wp_mail()` returns `false`, and callers ignore the return value.

This is a **configuration gap, not a WP Engine platform limit**: outbound 465/587 are open, and WP Engine supports ordinary `wp_mail()` while recommending an external provider for reliable delivery and logging.

**Remedy in place:** `mu-plugins/gsm-mail.php` (source `_migration/mu-plugins/gsm-mail.php`) hooks `phpmailer_init` and routes PHPMailer over SMTP. It is **inert until credentials exist** — no constant, no behaviour change.

Required in `wp-config.php`:

```php
define( 'GSM_SMTP_PASS', 'SG.…' );   // only required value
define( 'GSM_SMTP_HOST', 'smtp.sendgrid.net' );
define( 'GSM_SMTP_PORT', 587 );
define( 'GSM_SMTP_SECURE', 'tls' );
define( 'GSM_SMTP_USER', 'apikey' );
define( 'GSM_MAIL_FROM', 'info@goodshepherdmanor.org' );
```

The plugin also defaults the From address to `info@goodshepherdmanor.org` and logs `wp_mail_failed` so a future outage is not silent.

**DNS prerequisite:** the zone is `v=spf1 include:sendgrid.net include:_spf.google.com -all` with `DMARC p=quarantine`. SPF already authorises SendGrid, but the sending domain must be DKIM-authenticated in SendGrid (three CNAMEs) or DMARC alignment fails and the client's own notifications are quarantined. MX records point at Google Workspace and must not be touched.

**Ownership:** DNS and mail delivery are not part of the website build task. This section documents the dependency so the handoff is explicit.

## 8. WebP Converter for Media

Option `webpc_settings`: converts `jpg`, `jpeg`, `png` → `webp`, `conversion_method: gd`. Served through `wp-content/webpc-passthru.php`, which is generated per site with a baked-in allowlist of `home_url()` prefixes.

Consequences:

- After any domain change, re-bake the loader (`wp eval 'do_action("webpc_refresh_loader", true, false);'`) or every passthru image 404s on the new host
- Never copy `webpc-passthru.php` between environments — it will still allowlist the old domain
- Image URLs in markup therefore begin `/wp-content/webpc-passthru.php?src=…`; that is expected

## 9. WP Engine

- **Object cache is persistent.** After any database import, `wp cache flush` — otherwise stage serves pre-import option values and looks broken while the DB row is correct
- Page cache must be purged after Elementor changes (`wp page-cache flush`, `wp elementor flush-css`)
- Elementor CSS lives in `uploads/elementor/css/post-<id>.css`; regenerate after an import
- WP-CLI on stage: `wp --path=/sites/goodshephe3dev --allow-root`

## 10. mu-plugins

Source of truth is `_migration/mu-plugins/`; deployed copies are compared by md5 in `_tools/verify_site.php`.

| File | Responsibility |
|---|---|
| `gsm-redirects.php` | 301 table + post-slug fallback |
| `gsm-security.php` | XML-RPC/pingbacks off, user-enumeration block, security headers, version fingerprints stripped, login rate limiting |
| `gsm-seo.php` | keep SureForms URLs out of sitemap and indexes |
| `gsm-mail.php` | SMTP transport (inert without credentials) + failure logging |

## 11. Verification

```sh
# 47 assertions across pages, forms, template wiring, anchors, images, settings
./_tools/wp.sh eval-file _tools/verify_site.php
```

Exits non-zero on any failure, so it can gate a push. It is the fastest way to confirm an environment is intact after a migration.

## 12. Open items owned outside this build

1. SendGrid account access + API key + DKIM records → enables all email
2. Real GA4 measurement ID → enables analytics
3. Spam protection decision on public forms (reCAPTCHA/Turnstile/honeypot)
4. ESP decision if the newsletter list is to grow outside WordPress
5. Production `blog_public` flip and 301s for the legacy site
