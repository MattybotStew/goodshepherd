# Cline — Good Shepherd Manor

Read **`AGENTS.md`** first (canonical IA, 15-page SOW, stack, hard rules). Read **`FIGMA.md`** before any Figma URL.

## MCP

Figma remote server is configured in `.cline/settings.json` → `https://mcp.figma.com/mcp`. Authenticate once in Cline’s MCP panel; enable **Share → MCP access** on the Figma file.

## Current wire focus

| Route | Figma | Key files |
|---|---|---|
| `/support-gsm` | `9179:32` in gS-Design | `FoundationPage.jsx`, `src/data/getInvolved.js`, `SplitSection`, `HomeIntroStrip` |
| `/shepherd-endowment-society` | — | `EndowmentPage.jsx`, `src/data/endowment.js` (real copy) |
| `/about` | — | Reusable splits + `HistoryTimelineSection`, `AffiliationsSection` |

**15-page cap** — dropdown items under Get Involved are pages 8–11, not extra routes. Landing teasers on `/support-gsm` link to full pages 9–11.

Do **not** add horizontal tabs to Get Involved unless Figma changes. Stacked alternating splits match the design.

Local dev: `npm run dev` (or `--port 5174` if HMR is stale).
