import json, os, sys, urllib.request, concurrent.futures as cf
root = sys.argv[1]
D = json.load(open(os.path.join(root, 'data/posts_full.json'), encoding='utf-8'))
jobs = []
for code, r in D.items():
    for i, s in enumerate(r['slides'], 1):
        if s.get('img'):
            p = os.path.join(root, 'img', code, f'{i:02d}.jpg')
            if not os.path.exists(p):
                jobs.append((s['img'], p))
def get(j):
    u, p = j
    os.makedirs(os.path.dirname(p), exist_ok=True)
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        open(p, 'wb').write(data); return 'ok'
    except Exception as e:
        return 'fail ' + str(e)[:60]
with cf.ThreadPoolExecutor(6) as ex:
    res = list(ex.map(get, jobs))
print(len(jobs), 'jobs', sum(r == 'ok' for r in res), 'ok')
print([r for r in res if r != 'ok'][:5])
