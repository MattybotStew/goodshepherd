import { launch } from './ffbidi.mjs'; import fs from 'node:fs';
const S = process.env.S; const js = fs.readFileSync(S + '/xmeasure.js', 'utf8'); const B = 'https://goodshephe3dev.wpenginepowered.com';
const routes = ['/','/about/','/programs/','/programs/community-day-services/','/programs/residential-living/','/programs/health-well-being/','/programs/special-olympics/','/support-gsm/','/shepherd-endowment-society/','/events/','/news/','/newsletters/','/careers/','/contact/','/privacy/','/news/35th-annual-fall-festival/'];
fs.mkdirSync(S + '/ffshots', { recursive: true });
const ff = await launch(S + '/ffprof3');
for (const w of (process.argv[2] || '1440,1024,390').split(',').map(Number)) { await ff.viewport(w, 900);
  for (const r of routes) { let res = 'ERR';
    for (let t = 0; t < 3; t++) { try { await ff.goto(B + r); res = await ff.eval(js); if (!/DM SANS NOT LOADED/.test(res) || t === 2) break; } catch (e) { res = 'ERR ' + e.message.slice(0, 80); } await new Promise(z => setTimeout(z, 3000)); }
    console.log(String(w).padEnd(5), r.padEnd(36), res);
    if (w !== 1024) await ff.shot(`${S}/ffshots/${w}${r.replace(/\//g, '_')}.png`).catch(() => {});
    await new Promise(z => setTimeout(z, 1500)); } }
await ff.close();
