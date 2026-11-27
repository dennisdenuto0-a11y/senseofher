import json, datetime, sys, os
root = sys.argv[1]
J = lambda p: json.load(open(os.path.join(root, p), encoding='utf-8'))
D = J('data/posts_full.json'); O = J('data/ocr.json')
idx = {p['id']: p for p in J('data/posts_index.json')}
tz = datetime.timezone(datetime.timedelta(hours=10))
out = []
for code, r in D.items():
    mt = int(r.get('mt') or 1)
    if r.get('t'):
        date = datetime.datetime.fromtimestamp(int(r['t']), tz).strftime('%Y-%m-%d')
    elif code not in idx:
        date = datetime.datetime.now(tz).strftime('%Y-%m-%d') + '~'  # new post with no timestamp: collection day, approximate
    else:
        date =datetime.datetime.strptime(idx[code]['date'].lstrip('~'), '%B %d, %Y').strftime('%Y-%m-%d') + '~'
    s = O.get(code, {})
    out.append({'code': code, 'date': date, 'type': {1: 'image', 2: 'reel', 8: 'carousel'}.get(mt, str(mt)),
                'url': f"https://www.instagram.com/senseofher__/{'reel' if mt == 2 else 'p'}/{code}/",
                'caption': r.get('cap') or '', 'slides': [s[k] for k in sorted(s)]})
out.sort(key=lambda x: x['date'])
json.dump(out, open(os.path.join(root, 'data/corpus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'posts', sum(len(p['caption']) + sum(map(len, p['slides'])) for p in out), 'chars', sum(p['date'].endswith('~') for p in out), 'approx dates')
