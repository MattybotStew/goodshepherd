// Minimal WebDriver BiDi client for the stock Firefox (no Playwright build needed).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
const FF = '/Applications/Firefox.app/Contents/MacOS/firefox';
export async function launch(profileDir, port = 9333) {
  fs.mkdirSync(profileDir, { recursive: true });
  const proc = spawn(FF, ['--headless', '-no-remote', '-profile', profileDir, `--remote-debugging-port=${port}`, '--remote-allow-hosts=localhost,127.0.0.1'], { stdio: ['ignore', 'ignore', 'pipe'] });
  await new Promise((res, rej) => { const t = setTimeout(() => rej(new Error('ff start timeout')), 30000); proc.stderr.on('data', d => { if (/WebDriver BiDi listening/.test(String(d))) { clearTimeout(t); res(); } }); });
  const ws = new WebSocket(`ws://127.0.0.1:${port}/session`);
  await new Promise(r => ws.addEventListener('open', r, { once: true }));
  let id = 0; const pending = new Map();
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.type === 'error' ? rej(new Error(m.error + ': ' + m.message)) : res(m.result); } });
  const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
  await send('session.new', { capabilities: { alwaysMatch: { acceptInsecureCerts: true } } });
  const created = await send('browsingContext.create', { type: 'tab' }); const ctx = created.context;
  const api = {
    send, ctx,
    async viewport(w, h) { await send('browsingContext.setViewport', { context: ctx, viewport: { width: w, height: h } }); },
    async goto(url) { await send('browsingContext.navigate', { context: ctx, url, wait: 'complete' }); },
    async eval(fnSrc) { const r = await send('script.evaluate', { target: { context: ctx }, expression: `(async()=>{ ${fnSrc} })()`, awaitPromise: true, resultOwnership: 'none' }); if (r.type === 'exception') throw new Error(r.exceptionDetails.text); return r.result.value; },
    async shot(path, full = true) { const r = await send('browsingContext.captureScreenshot', { context: ctx, origin: full ? 'document' : 'viewport' }); fs.writeFileSync(path, Buffer.from(r.data, 'base64')); },
    async close() { try { await send('session.end'); } catch {} ws.close(); proc.kill(); },
  };
  return api;
}
