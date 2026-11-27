const {chromium} = require('playwright'); const W = ms => new Promise(r => setTimeout(r, ms));
const prog = require('./dbread3/progress/farha.json'), bank = require('./dbbank2/bank/farha.json');
(async () => { const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']}); const docs = {'progress/farha': JSON.parse(JSON.stringify(prog)), 'bank/farha': bank};
  for(const mode of ['joined phone', 'fresh phone', 'no cloud']){
  const p = await b.newPage({viewport: {width: 390, height: 844}}); const errs = []; p.on('pageerror', e => errs.push(e.message)); if(process.argv[2]) p.route('**/index.html', r => r.fulfill({path: process.argv[2]})); p.on('console', m => { if(/error|warn/i.test(m.type())) errs.push(m.text().slice(0, 140)); });
  if(mode !== 'no cloud'){
  await p.exposeBinding('__dbGet', (_, path) => docs[path] ? JSON.parse(JSON.stringify(docs[path])) : null);
  await p.exposeBinding('__dbSet', (_, path, data) => { docs[path] = data; });
  await p.addInitScript(() => { const deepFreeze = o => { if(o && typeof o === 'object'){ Object.values(o).forEach(deepFreeze); Object.freeze(o); } return o; }; const mk = path => ({ get: async () => { const d = await window.__dbGet(path); return {exists: !!d, data: () => deepFreeze(JSON.parse(JSON.stringify(d)))}; }, set: async d => { await new Promise(r => setTimeout(r, 150)); await window.__dbSet(path, JSON.parse(JSON.stringify(d))); }, update: async () => {},
    onSnapshot(cb){ setTimeout(async () => { const d = await window.__dbGet(path); cb({exists: !!d, data: () => deepFreeze(JSON.parse(JSON.stringify(d))), metadata: {}}); }, 50); return () => {}; } }); window.claude = {use: async n => n === 'db' ? {doc: mk} : null}; }); }
  await p.goto('http://127.0.0.1:8765/index.html');
  await p.evaluate(m => { localStorage.clear(); localStorage.setItem('mishmish_sound', 'true'); if(m === 'joined phone'){ localStorage.setItem('mishmish_device_id', JSON.stringify('mw3unoukjutwmp')); localStorage.setItem('mishmish_sync_meta', JSON.stringify({ts: {}, resetTs: 1793896996217, joined: true})); } }, mode);
  await p.reload(); await W(2500);
  await p.click('#roomDoor'); const seen = [];
  for(let t = 0; t < 12; t++){ await W(500); seen.push((await p.$('#room')) ? 'R' : (await p.$('.hero')) ? 'H' : '?'); }
  const toast = await p.$eval('#toast', e => e.hidden ? '' : e.textContent).catch(() => ''); console.log(mode.padEnd(14), 'toast:', toast.slice(0, 60), 'after tapping the room, every 0.5 s:', seen.join(''), '| errors', JSON.stringify(errs.slice(0, 5)));
  await p.close(); }
  await b.close(); })();
