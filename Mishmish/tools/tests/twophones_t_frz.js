/* two phones on one shared database (a fake of the artifact db, live like the real one) */
const {chromium} = require('playwright'); const W = ms => new Promise(r => setTimeout(r, ms));
(async () => { const b = await chromium.launch(); const docs = {}, subs = []; let writes = 0;
  const mkPhone = async name => {
    const ctx = await b.newContext({viewport: {width: 390, height: 844}}); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.exposeBinding('__dbGet', (_, path) => docs[path] ? JSON.parse(JSON.stringify(docs[path])) : null);
    await p.exposeBinding('__dbSet', (_, path, data) => { writes++; docs[path] = data; subs.filter(x => x.path === path).forEach(x => x.page.evaluate(([path, d]) => window.__dbPush(path, d), [path, data]).catch(() => {})); });
    await p.exposeBinding('__dbSub', (src, path) => { subs.push({path, page: src.page}); });
    await p.addInitScript(() => { window.__df = o => { if(o && typeof o === 'object'){ Object.values(o).forEach(window.__df); Object.freeze(o); } return o; }; });
    await p.addInitScript(() => { const L = {};
      window.__dbPush = (path, d) => (L[path] || []).forEach(cb => cb({exists: !!d, data: () => JSON.parse(JSON.stringify(d)), metadata: {}}));
      const mk = path => ({ get: async () => { const d = await window.__dbGet(path); return {exists: !!d, data: () => window.__df(JSON.parse(JSON.stringify(d)))}; },
        set: async d => { await new Promise(r => setTimeout(r, 120)); await window.__dbSet(path, JSON.parse(JSON.stringify(d))); },
        update: async () => {}, onSnapshot(cb){ (L[path] = L[path] || []).push(cb); window.__dbSub(path); setTimeout(async () => { const d = await window.__dbGet(path); cb({exists: !!d, data: () => window.__df(JSON.parse(JSON.stringify(d))), metadata: {}}); }, 50); return () => {}; } });
      window.claude = {use: async n => n === 'db' ? {doc: mk} : null}; });
    await p.goto('http://127.0.0.1:8765/index.html'); await p.evaluate(() => { localStorage.clear(); localStorage.setItem('mishmish_sound', 'false'); }); await p.reload(); await W(1500);
    return {p, errs, name};
  };
  const A = await mkPhone('dad'), B = await mkPhone('mum');
  const stars = P => P.p.$eval('#starCount', e => e.textContent.replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d)));
  const out = [];
  // 1) dad's phone: Farha learns the 4 times table (6 stars)… simulate quickly by earning stars through the daily math practice
  await A.p.click('[data-world="math"]'); await W(300);
  await A.p.evaluate(() => { localStorage.setItem('mishmish_debug', '1'); });
  // earn stars on A via a real flow: math hub -> daily practice answer everything
  await A.p.click('#mDaily'); await W(300);
  const EN = s => s.replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d));
  for(let k = 0; k < 30; k++){ if(!(await A.p.$('#mQ'))) break; const q = EN(await A.p.$eval('#mQ', e => e.textContent)).replace(/ = \?$/, ''); let m, ans;
    if((m = q.match(/^(\d+) \+ \? = (\d+)$/))) ans = +m[2] - +m[1]; else if((m = q.match(/^(\d+) ([+−×]) (\d+)$/))) ans = m[2] === '+' ? +m[1] + +m[3] : m[2] === '−' ? +m[1] - +m[3] : +m[1] * +m[3]; else break;
    for(const d of String(ans)) await A.p.click(`.m-key[data-mk="${d}"]`); await A.p.click('.m-key[data-mk="✔"]'); await W(800); }
  await W(2500);
  out.push(`after dad's phone practised: dad stars ${await stars(A)} | mum stars (live, on home page) ${await stars(B)}`);
  // 2) both earn at the same moment: dad adopts nothing, mum opens science hall (today's exam) - check same exam
  await A.p.goto('http://127.0.0.1:8765/index.html'); await W(1500); await A.p.click('[data-world="sci"]'); await W(300); await A.p.click('#sxDoor'); await W(1500);
  const tA = await A.p.$eval('#sxToday small', e => e.textContent).catch(() => '?');
  await W(2500);
  await B.p.click('[data-world="sci"]'); await W(300); await B.p.click('#sxDoor'); await W(800);
  const tB = await B.p.$eval('#sxToday small', e => e.textContent).catch(() => '?');
  out.push(`today's exam — dad: ${tA} | mum: ${tB} | same: ${tA === tB}`);
  // 3) simultaneous changes on both phones within the same second: each names a different cat... use bank + progress: write different keys at once
  await A.p.goto('http://127.0.0.1:8765/index.html'); await B.p.goto('http://127.0.0.1:8765/index.html'); await W(2000);
  await Promise.all([A.p.click('#roomDoor'), B.p.click('#roomDoor')]); await W(800);

  // dad toggles the window curtain (room), mum renames... simplest: both tap the window (room.curtain) and feed (treats) at the same time
  await Promise.all([A.p.evaluate(() => document.querySelector('#rwin').dispatchEvent(new MouseEvent('click', {bubbles: true}))), B.p.evaluate(() => document.querySelector('[data-feed]') && document.querySelector('[data-feed]').click())]);
  await W(5000);
  const sa = await A.p.evaluate(() => [localStorage.getItem('mishmish_treats'), JSON.parse(localStorage.getItem('mishmish_room')).curtain]);
  const sb = await B.p.evaluate(() => [localStorage.getItem('mishmish_treats'), JSON.parse(localStorage.getItem('mishmish_room')).curtain]);
  out.push(`after both phones changed things at once — dad: treats ${sa[0]} curtain ${sa[1]} | mum: treats ${sb[0]} curtain ${sb[1]} | cloud treats ${JSON.stringify(docs['progress/farha'].data.treats)} curtain ${docs['progress/farha'].data.room.curtain}`);
  out.push(`final stars — dad ${await stars(A)} mum ${await stars(B)} | writes ${writes}`);
  console.log(out.join('\n')); console.log('errors', A.errs, B.errs); await b.close(); })();

// deepFreeze
