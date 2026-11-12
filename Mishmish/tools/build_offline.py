"""Build a single self-contained offline copy of Mishmish.
- every voice file (voice/*.json, voice_ar/*.json) is embedded and served to the page's own fetch() calls
- Google Fonts are embedded as data URIs
- cloud sync is switched off: window.claude is hidden, so all progress stays in this browser only
usage: build_offline.py <Mishmish dir> <out.html> <fonts dir>"""
import base64, glob, json, os, re, sys
src, out, fonts = sys.argv[1:4]
h = open(os.path.join(src, 'index.html'), encoding='utf-8').read()

# 1) fonts
css = open(os.path.join(fonts, 'fonts.css'), encoding='utf-8').read()
def inline(m):
    url = m.group(1); f = os.path.join(fonts, os.path.basename(url.split('?')[0]))
    return 'url(data:font/woff2;base64,' + base64.b64encode(open(f, 'rb').read()).decode() + ')'
css = re.sub(r'url\((https://[^)]+)\)', inline, css)
h = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', h)
link = re.search(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>', h).group(0)
h = h.replace(link, '<style>' + css + '</style>')

# 1b) optional nameless copy (NONAME=<path to g.json recorded without the name>)
noname = os.environ.get('NONAME')
if noname:
    R = [("'برافو يا ' + KID_AR + '! 🎉'", "'برافو عليكي! 🎉'"),
         ('منهج الإنجليزي بتاع ${KID_AR}:', 'منهج الإنجليزي بتاعك:'),
         ('عوالم ${KID_AR} ', 'عوالمي '),
         ('حصالة ${KID_AR}', 'حصالتي'), ('دفتر ${KID_AR}', 'دفتري'), ('أوضة ${KID_AR}', 'أوضتي'),
         ('`${KID_AR} نسيت الرقم السري بتاع دفترها.', '`صاحبة الدفتر نسيت الرقم السري بتاعه.'),
         ("Farha's Room", 'My Room'), ("Farha\\'s room", 'My room'),
         ("'رائع يا فرحة!'", "'رائع جدًا!'"), ("'أحسنتِ يا فرحة! أنتِ ذكية جدًا.'", "'أحسنتِ! أنتِ ذكية جدًا.'"),
         ('علشان فرحة تبدأ', 'علشان بنتكم تبدأ'), ('لما فرحة تسحب', 'لما بنتكم تسحب'), ('`فرحة عاوزة تسحب', '`بنتكم عاوزة تسحب'),
         ("const kidName = () => S.name || 'Farha';", "const kidName = () => S.name || 'friend';")]
    for a, b in R:
        assert a in h, a
        h = h.replace(a, b)
    # anything left in visible text?
    left = [l for l in h.split('\n') if not l.startswith('const KID_AR') and ('فرحة' in l or 'KID_AR}' in l or "Farha'" in l) and not l.lstrip().startswith('/*')]
    assert not left, left[:3]

# 2) voices + offline mode, injected before any other script
files = {}
for d in ('voice', 'voice_ar'):
    for f in sorted(glob.glob(os.path.join(src, d, '*.json'))):
        files[d + '/' + os.path.basename(f)] = open(f, encoding='utf-8').read()
if noname:
    files['voice_ar/g.json'] = open(noname, encoding='utf-8').read()
boot = ('<script>/* offline copy: no cloud sync, voices built in */\n'
        'try{ Object.defineProperty(window, "claude", {value: undefined, writable: false, configurable: false}); }catch(e){}\n'
        'window.__OFFLINE_FILES = {' + ','.join(json.dumps(k) + ':' + v for k, v in files.items()) + '};\n'
        '(function(){ const real = window.fetch ? window.fetch.bind(window) : null;\n'
        '  window.fetch = function(u, o){ const k = String(u).split("?")[0].replace(/^\\.\\//, "");\n'
        '    if(k in window.__OFFLINE_FILES) return Promise.resolve({ok: true, status: 200, json: () => Promise.resolve(window.__OFFLINE_FILES[k])});\n'
        '    return real ? real(u, o) : Promise.reject(new Error("offline")); };\n'
        '})();\n</script>\n')
i = h.index('<script>')
h = h[:i] + boot + h[i:]
if '<meta charset' not in h:   # the hosted page gets these from its wrapper; a local file needs them itself
    h = ('<!DOCTYPE html>\n<html lang="ar">\n<meta charset="utf-8">\n'
         '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + h + '\n</html>\n')
open(out, 'w', encoding='utf-8').write(h)
print('voice files', len(files), '| size', round(os.path.getsize(out) / 1e6, 1), 'MB')
