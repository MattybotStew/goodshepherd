# Cline — Good Shepherd Manor

Read **`AGENTS.md`** first (canonical IA, 15-page SOW, stack, hard rules). Read **`FIGMA.md`** before any Figma URL.

## MCP

Figma remote server is configured in `.cline/settings.json` → `https://mcp.figma.com/mcp`. Authenticate once in Cline's MCP panel; enable **Share → MCP access** on the Figma file.

## Current wire focus

| Route | Figma | Key files |
|---|---|---|
| `/support-gsm` | `9179:32` in gS-Design (legacy) | `FoundationPage.jsx`, `src/data/getInvolved.js`, `SplitSection`, `HomeIntroStrip` — **merged page** (GSM Foundation + Ways to Give) |
| `/shepherd-endowment-society` | — | `EndowmentPage.jsx`, `src/data/endowment.js` (real copy) |
| `/about` | — | Reusable splits + `HistoryTimelineSection`, `AffiliationsSection` |
| `/programs/special-olympics` | — | `SpecialOlympicsPage.jsx`, `src/data/programs.js` |

**15-page cap** — dropdown items under Support GSM are pages 9–12, not extra routes. Landing teasers on `/support-gsm` link to full pages.

Support GSM Foundation uses a `SectionTabs` jump bar above stacked `SplitSection`s (client direction). Do **not** replace stacked content with hidden tab panels.

Local dev: `npm run dev` (or `--port 5174` if HMR is stale).
