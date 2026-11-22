"""Pack the math narration into va/m.mp3 + va-index.json["m"] + va-h.json (djb2/base36 of the exact recorded text)."""
import json, os
D = os.path.dirname(os.path.abspath(__file__)); VA = '/home/user/Claude_Home/Mishmish/va'
def ohash(t):
    h = 5381
    for ch in t:
        # JS charCodeAt works on UTF-16 code units
        b = ch.encode('utf-16-le')
        for i in range(0, len(b), 2):
            h = ((h << 5) + h + int.from_bytes(b[i:i+2], 'little')) & 0xFFFFFFFF
    s, n = '', h
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    while True:
        s = digits[n % 36] + s; n //= 36
        if not n: break
    return s
lines = json.load(open(os.path.join(D, 'lines.json'), encoding='utf-8'))
idx = json.load(open(os.path.join(VA, 'va-index.json'))); hh = json.load(open(os.path.join(VA, 'va-h.json')))
buf = b''; ix = {}; missing = []
for cid, txt in lines:
    p = os.path.join(D, 'out', cid + '.mp3')
    if not os.path.exists(p): missing.append(cid); continue
    data = open(p, 'rb').read(); ix[cid] = [len(buf), len(data)]; buf += data; hh[cid] = ohash(txt)
open(os.path.join(VA, 'm.mp3'), 'wb').write(buf)
idx['m'] = ix
json.dump(idx, open(os.path.join(VA, 'va-index.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(hh, open(os.path.join(VA, 'va-h.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print('packed', len(ix), 'clips,', len(buf), 'bytes; missing', missing)
