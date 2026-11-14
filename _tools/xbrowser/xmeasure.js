await document.fonts.ready;
document.documentElement.style.scrollBehavior = 'auto';
for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 600));
const out = [];
const vis = e => { const r = e.getBoundingClientRect(), c = getComputedStyle(e); return r.width > 0 && r.height > 0 && c.visibility !== 'hidden' && c.display !== 'none'; };
if (document.documentElement.scrollWidth > innerWidth + 1) out.push('OVERFLOW ' + document.documentElement.scrollWidth);
const broken = [...document.images].filter(i => vis(i) && i.complete && i.naturalWidth === 0).map(i => (i.currentSrc || i.src).split('/').pop().slice(0, 40));
if (broken.length) out.push('BROKEN ' + broken.join(','));
const fam = getComputedStyle(document.body).fontFamily; const dm = [...document.fonts].some(f => /DM Sans/.test(f.family) && f.status === 'loaded'); if (!dm) out.push('DM SANS NOT LOADED');
// rows stopping short
for (const c of document.querySelectorAll('.e-con')) { const inner = c.querySelector(':scope > .e-con-inner') || c; const ics = getComputedStyle(inner);
  if (ics.display !== 'flex' || !ics.flexDirection.startsWith('row')) continue; const kids = [...inner.children].filter(k => k.getBoundingClientRect().width > 0 && getComputedStyle(k).position !== 'absolute'); if (kids.length < 2) continue;
  const ir = inner.getBoundingClientRect(); const lines = {}; for (const k of kids) { const t = Math.round(k.getBoundingClientRect().top / 4); (lines[t] = lines[t] || []).push(k.getBoundingClientRect()); }
  for (const L of Object.values(lines)) { if (L.length < 2) continue; const slack = (ir.right - parseFloat(ics.paddingRight)) - Math.max(...L.map(x => x.right)); const ls = Math.min(...L.map(x => x.left)) - (ir.left + parseFloat(ics.paddingLeft));
    if (slack > 6 && slack < ir.width * 0.3 && ls < 3 && /normal|start/.test(ics.justifyContent)) out.push(`SHORT ${c.dataset.id} ${Math.round(slack)}`); break; } }
// unexpected wraps in fixed rows (4-up stats, timeline, strips) at >=1024
if (innerWidth >= 1024) for (const id of ['imp_stats', 'ab_hist_row', 'hi_row', 'nw_grid']) { const r = document.querySelector('[data-id=' + id + ']'); if (!r) continue; const kids = [...(r.querySelector(':scope > .e-con-inner') || r).children].filter(vis); const tops = new Set(kids.map(k => Math.round(k.getBoundingClientRect().top / 8))); if (tops.size > 1) out.push(`WRAP ${id} ${tops.size} rows`); }
// hero optical position
const hero = document.querySelector('.elementor-element-hero');
if (hero) { const hdr = document.querySelector('#masthead'); let hb = 0;
  for (const e of hdr.querySelectorAll('.custom-logo, .ast-header-button-1 .ast-custom-button, .main-header-menu > .menu-item > .menu-link, .menu-toggle')) { if (!vis(e)) continue; const r = e.getBoundingClientRect(); if (r.bottom > 0 && r.top < 400) hb = Math.max(hb, r.bottom); }
  const h1 = hero.querySelector('h1').getBoundingClientRect(); const ws = [...hero.querySelectorAll('.elementor-widget')].filter(vis); const cb = Math.max(...ws.map(w => w.getBoundingClientRect().bottom));
  let visBot = hero.getBoundingClientRect().bottom; const n = hero.nextElementSibling; const card = n && n.querySelector('[data-id$="_row"], #home-intro, [data-id=contact_bar]'); if (card) visBot = Math.min(visBot, card.getBoundingClientRect().top);
  out.push(`HERO top ${Math.round(h1.top - hb)} bottom ${Math.round(visBot - cb)}`); }
const q = s => document.querySelector(s);
if (q('#home-intro')) out.push('strip ' + Math.round(q('#home-intro').getBoundingClientRect().width));
if (q('[data-id=prog_icon0]')) out.push('icon ' + Math.round(q('[data-id=prog_icon0]').getBoundingClientRect().width));
if (q('[data-id=post_content]')) out.push(`post content ${Math.round(q('[data-id=post_content]').getBoundingClientRect().left)} back ${Math.round(q('[data-id=post_back]').getBoundingClientRect().left)} h ${Math.round(q('[data-id=post_content]').getBoundingClientRect().height)}`);
const bar = q('.ast-above-header-bar'); if (bar && vis(bar)) { const bg = getComputedStyle(bar).backgroundColor; if (/255, 255, 255/.test(bg)) out.push('BANNER WHITE'); }
const nl = q('.elementor-element-nlright input[type=email]'); if (nl) { const lb = document.querySelector('label[for="' + nl.id + '"]'); if (!lb || getComputedStyle(lb).display === 'none') out.push('NL LABEL HIDDEN'); }
return out.join(' | ');
