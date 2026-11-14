# Cline — Good Shepherd Manor

Read **`AGENTS.md`** first (canonical IA, 14-page SOW, stack, hard rules, stage fix ledger). Read **`FIGMA.md`** before any Figma URL.

## MCP

Figma remote server is configured in `.cline/settings.json` → `https://mcp.figma.com/mcp`. Authenticate once in Cline's MCP panel; enable **Share → MCP access** on the Figma file.

## Environments

| Env | URL |
|---|---|
| Local (canonical) | `https://goodshepherd.local` |
| Stage (rebuilt from Local) | `https://goodshephe3dev.wpenginepowered.com` |
| Live (being replaced) | `https://www.goodshepherdmanor.org` |

## Current build (2026-11-13)

All 14 SOW pages + Privacy are built and generated from the React wire in this repo. Content is real copy except the newsletter archive; news posts were imported from the live site.

- **Pages are generated, not hand-built:** `_tools/build_pages.py` / `build_home_replica.py` emit Elementor JSON; `_tools/apply_elementor.sh` applies it.
- **Fixes are scripts too:** hero centring, CTA band, news hub, post template, gallery padding, contrast and the news import all live in `_tools/` — re-run them rather than editing pages in Elementor.
- **Hero padding is CSS-owned** (it tracks the transparent header height per band). Do not change it in Elementor.
- **Post template** is Theme Builder `Single Post — News` with condition `include/singular/post`.
- **Editability contract:** `_tools/audit_editability.php` must report 0 raw HTML widgets, 0 shortcodes, 0 per-element custom CSS.

## Still open

Form mail transport (`GSM_SMTP_PASS`), newsletter archive PDFs, news archive/pagination, news card imagery.

See `AGENTS.md` §Stage fixes 2026-11-13 for the measured numbers and the reason behind each rule.
