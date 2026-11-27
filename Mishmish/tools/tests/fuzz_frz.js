/* damaged saved data + damaged cloud copies: every screen must open, every exam must reach its result, zero page errors */
const {chromium} = require('playwright'); const W = ms => new Promise(r => setTimeout(r, ms));
const KEYS = ['starLedger','owned','equip','gallery','tricky','mish','room','treats','pet','day','name','readWords','famDone','storyDone','wl','gDone','vDone','writings','exams','pDone','wDone','sci','spellOk','gymExt','fnd','fndHard','catProf','pets','math'];
const bad = {nul: null, arr: [1, null, 'x'], str: 'oops', num: 7, obj: {a: null, b: 'x', c: [1]}, nest: {dev: 'x', base: 'y', items: 5, date: 3, hearts: 'z'}};
const setups = [['clean', {}, null]];
for(const [n, v] of Object.entries(bad)){ const all = {}; KEYS.forEach(k => all[k] = v); setups.push(['local_all_' + n, {...all, bank: v}, null]); setups.push(['cloud_all_' + n, {}, {prog: {data: all, ts: Object.fromEntries(KEYS.map(k => [k, Date.now() + 9e6])), resetTs: 0}, bank: v}]); }
setups.push(['cloud_reset_weird', {}, {prog: {data: Object.fromEntries(KEYS.map(k => [k, 'x'])), ts: {}, resetTs: Date.now() + 1e9}, bank: {log: [null, {amt: '5', t: 'in'}, 'x'], paid: [], examPass: 'abc'}}]);
setups.push(['ledger_dev_weird', {starLedger: {base: '12', dev: {a: null, b: 'x', c: {e: '3', s: null}}}}, null]);
(async () => {
  const b = await chromium.launch(); let fails = 0;
  const only = process.argv[2];
  for(const [name, local, cloud] of setups){
    if(only && !name.includes(only)) continue;
    const p = await b.newPage({viewport: {width: 390, height: 844}}); const errs = []; p.on('pageerror', e => errs.push(e.message));
    if(cloud) await p.addInitScript(c => { const docs = {'progress/farha': c.prog, 'bank/farha': c.bank};
      const mk = path => ({onSnapshot(cb){ setTimeout(() => { try{ cb({exists: docs[path] != null, data: () => { const f = o => { if(o && typeof o === 'object'){ Object.values(o).forEach(f); Object.freeze(o); } return o; }; return f(JSON.parse(JSON.stringify(docs[path]))); }, metadata: {}}); }catch(e){ setTimeout(() => { throw e; }); } }, 60); return () => {}; }, set: async () => {}, update: async () => {}, get: async () => ({exists: false, data: () => null})});
      window.claude = {use: async () => ({doc: mk})}; }, cloud);
    await p.goto('http://127.0.0.1:8765/index.html');
    await p.evaluate(st => { localStorage.clear(); localStorage.setItem('mishmish_sound', 'false'); for(const k in st) localStorage.setItem('mishmish_' + k, JSON.stringify(st[k])); }, local);
    await p.reload(); await W(700); await p.evaluate(() => { try{ const o = JSON.parse(localStorage.getItem('mishmish_owned')); if(Array.isArray(o) && !o.includes('fr_bobo')){ o.push('fr_bobo', 'fr_luna'); localStorage.setItem('mishmish_owned', JSON.stringify(o)); } }catch(e){} }); await p.reload(); await W(700);
    const res = []; const ok = async (label, sel) => { const f = !!(await p.$(sel)); res.push((f ? '' : '✘') + label); if(!f) fails++; };
    const home = async () => { await p.goto('http://127.0.0.1:8765/index.html'); await W(500); };
    const clk = async s => { await p.evaluate(s => { const e = document.querySelector(s); if(!e) throw new Error('no ' + s); e.click(); }, s); await W(250); };
    const run = async (label, fn) => { try{ await fn(); }catch(e){ res.push('✘' + label + ':' + e.message.split('\n')[0].slice(0, 80)); fails++; } };
    await ok('home', '.hero');
    for(const d of ['#roomDoor', '#mallDoor', '#bankDoor', '#nbDoor']) await run(d, async () => { await home(); await clk(d); await ok(d, '#backBtn, .hub, .stage'); });
    await run('en', async () => { await home(); await clk('[data-world="en"]'); await ok('en', '#examDoor'); await clk('#examDoor'); await ok('enExams', '.hub, .stage'); });
    await run('en_book', async () => { await home(); await clk('[data-world="en"]'); await clk('#bookDoor'); await ok('book', '.hub, .stage'); });
    await run('fnd', async () => { await home(); await clk('[data-world="en"]'); await clk('#fndDoor'); await ok('fnd', '.hub, .stage'); });
    await run('sci', async () => { await home(); await clk('[data-world="sci"]'); await ok('sciMap', '#sxDoor'); });
    const exam = async id => { await home(); await clk('[data-world="sci"]'); await clk('#sxDoor'); if(id[0] === "f") await clk("#sxFinals"); await clk(`[data-sxi="${id}"]`);
      for(let t = 0; t < 80; t++){ if(await p.$('.sx-res')) break;
        const kind = await p.evaluate(() => document.querySelector('#sxShow, #sxOk') ? 'open' : document.querySelector('[data-si]') ? 'sort' : 'choice');
        if(kind === 'open'){ await p.evaluate(() => document.querySelector('#sxShow') && document.querySelector('#sxShow').click()); await W(30); await p.evaluate(() => document.querySelector('#sxOk').click()); await W(380); }
        else if(kind === 'sort'){ const n = await p.$$eval('.sxr-srow', a => a.length); for(let k = 0; k < n; k++){ await p.evaluate(k => document.querySelector(`[data-si="${k}"][data-sg="0"]`).click(), k); await W(30); } await W(380); }
        else { await p.evaluate(() => document.querySelector('.sci-opts .opt').click()); await W(380); }
        if(await p.$('#sxEnd:not([disabled])')){ await p.click('#sxEnd'); await W(300); } }
      await ok('exam ' + id, '.sx-res'); };
    for(const id of ['u1b', 'w1', 'c1l2', 'f1']) await run('exam ' + id, () => exam(id));
    await run('math', async () => { await home(); await clk('[data-world="math"]'); await ok('mathWorld', '#mDaily'); await clk('#mMul'); await ok('castle', '.m-grid'); await home(); await clk('[data-world="math"]'); await clk('#mMen'); await ok('club', '.m-strats'); await home(); await clk('[data-world="math"]'); await clk('#mDaily'); await ok('daily', '#mQ'); });
    const bad = [...new Set(errs)]; if(bad.length) fails++;
    console.log(name.padEnd(20), res.filter(x => x.startsWith('✘')).join(' ') || 'all screens OK', bad.length ? 'ERRORS ' + JSON.stringify(bad.slice(0, 4)) : '');
    await p.close();
  }
  console.log('FAILS', fails); await b.close();
})();
