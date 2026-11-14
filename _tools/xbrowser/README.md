# Cross-browser layout check (no browser downloads)

Runs one measurement script (`xmeasure.js`) in three engines against stage and
prints one line per page/width, so the outputs can be diffed.

| Engine | Driver | Notes |
|---|---|---|
| Chromium | Playwright (cached build) | any Playwright install |
| Firefox (stock app) | `ffbidi.mjs` — WebDriver BiDi over Node's built-in WebSocket | `ffrun.mjs`; uses a throwaway profile, never your own |
| WebKit = Safari's engine | `wkrun.swift` — offscreen `WKWebView` | `swiftc -O -framework WebKit -framework AppKit wkrun.swift -o wkrun` |

```sh
S=/tmp/xb node ffrun.mjs 1440,1024,390          # Firefox (writes screenshots to $S/ffshots)
./wkrun xmeasure.js /tmp/xb/wk 1440 URL [URL...] # WebKit, one width per run, run in the foreground
```

`xmeasure.js` reports: horizontal overflow, broken images, DM Sans not loaded,
flex rows stopping short of the grid, unexpected wraps, hero gaps, strip/icon
widths, post column alignment, a white above-header banner, a hidden newsletter label.
Lines that differ between engines are the cross-browser bugs.

In zsh, pass URLs as an array (`"${U[@]}"`); an unquoted `$U` is not word-split.
