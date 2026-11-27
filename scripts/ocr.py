import json, os, sys, subprocess, concurrent.futures as cf
root = sys.argv[1]
T = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
imgs = []
for d in os.listdir(os.path.join(root, 'img')):
    for f in sorted(os.listdir(os.path.join(root, 'img', d))):
        imgs.append((d, f))
def run(x):
    d, f = x
    p = os.path.join(root, 'img', d, f)
    out = subprocess.run([T, p, '-', '--psm', '3'], capture_output=True)
    return d, f, out.stdout.decode('utf-8', 'replace')
res = {}
with cf.ThreadPoolExecutor(8) as ex:
    for d, f, t in ex.map(run, imgs):
        res.setdefault(d, {})[f] = t
json.dump(res, open(os.path.join(root, 'data/ocr.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(len(imgs), 'images', sum(len(t.strip()) > 20 for v in res.values() for t in v.values()), 'with text')
