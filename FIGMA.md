# Figma — all agents

**Canonical project rules:** `AGENTS.md` (IA, stack, slugs, homepage wire, Get Involved wire). This file covers Figma MCP only.

This project is wired to **Figma’s remote MCP server** at `https://mcp.figma.com/mcp`.
Use it from Grok, Claude Code, Cursor, Cline, VS Code Copilot, Codex, and Gemini.

Pair MCP (live context / screenshots) with the local pipeline (`figma sync`) for tokens, assets, and component scaffolding.

## Authenticate (once per tool)

OAuth is required. On first connect, approve access in the browser.

- **Grok:** `/mcps` → select `figma` → authenticate
- **Claude Code:** `/mcp` → `figma` → Authenticate
- **Cursor / VS Code:** Start / Connect next to the Figma server, then Allow access
- **Cline:** MCP Servers panel → Figma → authenticate

In the Figma file, enable **Share → MCP access** so the server can read it.

## Required flow for design-to-code

1. Paste a Figma file or frame URL (`Copy link to selection`).
2. Call `get_design_context` for the exact node.
3. If the payload is huge or truncated, call `get_metadata` then re-fetch only the needed node(s).
4. Call `get_screenshot` for a visual reference.
5. Only then download assets and implement.
6. Translate MCP output into **this project’s** stack, tokens, and components. Do not paste generated React/Tailwind as-is if the repo uses something else.
7. Check the result against the screenshot before calling the work done.

## Key Figma nodes (gS-Design)

File key: `U5wiJ2dHCvnJXEkCYTZtZ9`

| Page / frame | Node ID | Repo export / implementation |
|---|---|---|
| Homepage | `9009:2` | `design/node-9009-2.png` → `HomePage.jsx` |
| Get Involved landing (`/support-gsm`) | `9179:32` (canvas `6:124`) | `design/figma-node-6-124.png` → `FoundationPage.jsx`, `src/data/getInvolved.js` |
| **Dev Layer page** (handoff) | `9712:32` | 14 `[DEV]` page frames + a `Dev notes — X` card per page |

### Dev Layer page (`9712:32`)

The Dev Layer is the handoff surface: one `[DEV]` frame per SOW page (DOM copies at 1440 wide)
with a `Dev notes — <page>` card pinned above it. The cards carry slug, WP ID, React file,
canonical frame, section IDs and locked decisions. They are the fastest way to see whether a
frame is current.

Refreshed **2026-11-14** to match Local + stage after the client content-document audit:

- Footer column renamed **Get Involved** and **Volunteer** added before Memorial or Tribute, on all 14 frames;
  the footer tagline is **"Compassionate care for men with developmental disabilities"** (Global!D22), not the
  old "A residential care community in Momence…" line.
- Header nav reads **News & Updates** with no dropdown (it was "News" plus a submenu caret on 13 frames; the
  live nav has three dropdowns only — About, Programs & Services, Support GSM).
- Newsletter band gained the **STAY CONNECTED** eyebrow (Home, About, Programs, Community Day, Contact
  were missing it) and the line **"No spam – just stories worth opening."** under the form.
- Programs: **Our Programs & Services** H2 + lede restored above the cards; the four cards carry the
  Programs-sheet copy and **Learn more →**; equal-height cards with the links on one baseline; the frame
  follows the live card order. **Photography matches the live page**: the hero is media 2428 (digital den),
  the mosaic is 2429 Don C. (tall), 2430 birdfeeder (wide), 2431 nursing w Tim K. and 2432 staff and Tim
  (stacked). Other frames still carry the original Figma mock photos.
  How the photos got in, since the plugin has no network access: `upload_assets` (no `nodeIds`) drops each
  file on the page as a loose frame and returns its `imageHash`; a `use_figma` script then copies that hash
  into the target node's existing `IMAGE` paint only (the mosaic tiles also carry a `SOLID` and a
  `GRADIENT_LINEAR` fill that a direct `nodeIds` upload could replace) and deletes the loose frames.
- Support GSM: H1 is **GSM Foundation**; jump tab singular, section eyebrow plural.
- About: both partner pills (ARC of Illinois, Intersect For Ability).
- New card **`Dev notes — Content audit 2026-11-14`** (right of the "Do not implement" card) summarises
  the 7 document fixes and 4 client decisions, with the document cell references.
- The notes cards grew with the added lines, so the whole top row was re-aligned to a common top edge, kept
  ≥20px clear of every page frame (two of them had started to overlap their frame). The row sits at
  `y = -179` since the annotation pass — see §Dev Layer cleanup below.
- The 13 inner-frame headers were laid out with a 502px left padding, so the 697px nav list spilled left
  over the white logo. Their header containers are now 1200 wide with 40px padding and `SPACE_BETWEEN`:
  logo left, nav centre, Support GSM button right, no overlap.
- The newsletter band sits **flush on the footer** in all 14 frames (`band.bottom == footer.top`, and the
  frame ends exactly at the footer). Seven frames had drifted — Programs 81px short, Contact 51px short,
  Support GSM −64, Endowment −59, Events −2, News −139 and Newsletters −217 — because the band `Section`
  is a plain body child positioned by hand next to an empty spacer. The spacer (`Spacer — newsletter band
  slot`) is now resized to the band and shares its y, so the two cannot drift apart again. Programs and
  Contact are 33px taller than before: their band (309px) did not fit the 276px gap, so the footer moved
  down rather than the band covering the Support GSM card. Verify with `band.bottom == footer.top` on the
  Body-child ancestor of the "No spam" text — measuring up to the first ancestor named `Section` (or any
  other container name) gives false gaps. Home and About keep the band **inside** the footer, so their
  measurement is `n/a`, not a failure.

Traps found while editing the frames: the notes and page frames are plain frames, not auto-layout
containers, so they do **not** reflow when a text grows — check `Main Content` is `HUG` (Home and
About were `FILL` and silently clipped their last section), and a footer column with a fixed-height
`List` will clip a new item until the list is switched to `HUG`. Text **layer names** do not follow the
characters either, so a renamed string still shows the old copy in the layers panel until it is renamed
too — check names, not just text, when auditing a frame against the live page.

## Dev Layer cleanup and annotations (2026-11-14)

The page is now a handoff surface rather than a working file: 33 top-level nodes, no overlaps, and every
annotation written from the same text as its notes card.

**Dev Mode annotations.** Each of the 14 `[DEV]` frames carries exactly one annotation (category
`2011:0`), and its text is the body of that page's `Dev notes` card. They had drifted badly — the Programs
annotation still had no content-document update, News still said article bodies *may* be placeholder — so
treat the card as the single source and re-write the frame's annotation from it whenever a card changes.
`node.annotations` is writable from the plugin (`node.annotations = [{ label, categoryId: '2011:0' }]`);
`labelMarkdown` is derived from `label`, so plain text is what you control.

**Body-child names are the same on every frame** (and unique inside each body, which they were not before —
every frame had two layers called `Section` and one called `Header`):

| Layer | What it is |
|---|---|
| `Content — page wrapper` | Home only — the wrapper holding hero → footer |
| `Banner — above-header` | the “A Place to Belong…” bar (real content, plus its × ) |
| `Spacer — banner slot` | the empty 42px placeholder above it (artboards without the banner) |
| `Header — transparent nav` | the nav frame (108px inner pages, 176px Home, transparent over the hero) |
| `Main Content` / `Article` | the page body (News uses `Article`) |
| `Section — Page content` | the last content section |
| `Spacer — newsletter band slot` | the empty area the band is seated in |
| `Section — Newsletter band` | the newsletter band itself (inside `Footer` on Home and About) |
| `Footer` | footer |

Notes-card text layers are `Notes — title` and `Notes — body`, so a name no longer encodes stale copy.

**Row geometry.** Notes cards share a top edge (`y = -179` as of 2026-11-14) so the tallest card — Programs,
359px — clears the frames at `y = 200` by 20px. The legend sits *above* that row with a 40px gap; it used to
sit at `y = -200` and overlapped the Home card by 124px. `Dev notes — Content audit 2026-11-14` sits 40px
under `Dev notes — Do not implement`, in the same right-hand column.

**Removed as clutter.** A `Support cards` frame and a loose “Donate to help the men of GSM…” paragraph were
sitting at the page origin, on top of the Home frame — they are build fragments, now on the `BIN` page. Five
empty text layers were deleted from the QA pack. The 356 default-named `Vector` / `Text` nodes inside logo
and icon groups were left alone: renaming those is churn, not clarity.

**The QA pack** (`🧪 QA — Stage QA pack (2026-11-13)`, a section to the left of Home) is the pre-launch
checklist — page index, anchor map, redirects, form specs, breakpoint checklist — not page designs. Keep it
content-accurate; it is not part of the 14 frames.

**Stale claims corrected** when the annotations were resynced: the Programs card says the frame keeps the
original Figma mock photography (it claimed to match the live page, and listed the media IDs as if the frames
used them); the News card documents the Elementor Pro Posts widget, the `include/singular/post` template and
real imported article bodies; the Endowment card no longer says its CTA band is placeholder copy.

When implementing from Figma, call `get_design_context` on the **frame node** (e.g. `9179:32`), not the canvas parent alone. If MCP returns “nothing selected”, retry with the inner frame ID from `get_metadata`.

Adapt MCP output to this repo: Vite + React, `src/styles/tokens.css`, `starter.css`, existing components (`SplitSection`, `HomeIntroStrip`, `PageHero`, etc.). No Tailwind in the wires.

## Asset rules

- If MCP returns a localhost URL for an image or SVG, use that source directly.
- Do not invent placeholders when a real asset URL was provided.
- Do not add a new icon package when the Figma payload already has the asset.

## Local pipeline (tokens / assets / components)

```bash
figma sync --project .
# or, if this repo has npm scripts:
npm run figma:sync
```

- Config: `figma.config.json`
- Credentials (REST pipeline only): `FIGMA_TOKEN` and `FIGMA_FILE_KEY` in `.env`
- Create a token: Figma → Account → Settings → Security → Personal access tokens

## MCP configs in this folder

| Tool | Instructions | MCP config |
| ---- | ------------ | ---------- |
| All agents | `AGENTS.md` | — |
| Claude Code | `CLAUDE.md` → `AGENTS.md` + `FIGMA.md` | `.claude/settings.json`, `.mcp.json` |
| Cursor | `.cursor/rules/agents.mdc` + `figma.mdc` | `.cursor/mcp.json` |
| Codex | `AGENTS.md` (+ `FIGMA.md` fallback) | `.codex/config.toml` |
| Gemini CLI | `GEMINI.md` → `AGENTS.md` + `FIGMA.md` | `.gemini/settings.json` |
| Grok | `AGENTS.md` (auto-discovered) | `.grok/config.toml` |
| Cline | `CLINE.md` → `AGENTS.md` + `FIGMA.md` | `.cline/settings.json` |
| VS Code / Copilot | `AGENTS.md` | `.vscode/mcp.json` |
