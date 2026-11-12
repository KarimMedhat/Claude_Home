"""Compress msa_clips/*.mp3 (24 kbps, 16 kHz mono) and pack one JSON per lesson: voice_ar/<lesson>.json, plus g.json.
usage: msa_pack.py <clipdir> <packdir>"""
import base64, glob, json, os, re, subprocess, sys
src, dst = sys.argv[1:3]
small = src.rstrip('/') + '_24k'
os.makedirs(small, exist_ok=True); os.makedirs(dst, exist_ok=True)
for old in glob.glob(os.path.join(dst, '*.json')):
    os.remove(old)
packs = {}
for f in sorted(glob.glob(os.path.join(src, '*.mp3'))):
    cid = os.path.basename(f)[:-4]
    s = os.path.join(small, cid + '.mp3')
    if not os.path.exists(s) or os.path.getmtime(s) < os.path.getmtime(f):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-ac', '1', '-ar', '16000', '-b:a', '24k', s], check=True)
    k = re.match(r'(c\d+l\d+|g)', cid).group(1)
    packs.setdefault(k, {})[cid] = base64.b64encode(open(s, 'rb').read()).decode()
tot = 0
for k, d in sorted(packs.items()):
    p = os.path.join(dst, k + '.json')
    json.dump(d, open(p, 'w'), separators=(',', ':'))
    tot += os.path.getsize(p)
print(len(packs), 'packs,', round(tot / 1e6, 1), 'MB total, biggest', max(round(os.path.getsize(os.path.join(dst, k + '.json')) / 1e6, 2) for k in packs), 'MB')
