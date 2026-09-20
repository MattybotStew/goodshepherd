# goodShepherd

Good Shepherd Manor **wireframe prototype** (Vite + React). Production is WordPress on WP Engine (Astra + Elementor).

**AI agents:** read [`AGENTS.md`](AGENTS.md) first (canonical IA, slugs, stack, homepage wire). For Figma MCP, see [`FIGMA.md`](FIGMA.md).

## Shareable preview

https://mattybotstew.github.io/goodshep/

GitHub Pages builds from `main`. First time only: **Settings → Pages → Source → GitHub Actions**, then re-run the **GitHub Pages** workflow (or push to `main`).

## Getting started

```bash
npm install      # install dependencies
npm run dev      # start the dev server (http://localhost:5173)
```

## Scripts

| Command          | Description                                  |
| ---------------- | -------------------------------------------- |
| `npm run dev`    | Start the Vite dev server with HMR           |
| `npm run build`  | Build the production bundle into `dist/`     |
| `npm run preview`| Locally preview the production build          |
| `npm run lint`   | Run ESLint                                   |

## Project structure

```
├── index.html          # HTML entry point
├── public/             # Static assets served at the root
├── src/
│   ├── assets/         # Bundled assets (images, icons)
│   ├── App.jsx         # Root component
│   ├── App.css         # Root component styles
│   ├── index.css       # Global styles
│   └── main.jsx        # React entry point
├── eslint.config.js    # ESLint (flat config)
├── vite.config.js      # Vite configuration
└── package.json        # Dependencies & scripts
```