import json, re, os, sys, collections, html
root = sys.argv[1]
allc = []
for i in range(1, 7):
    allc += json.load(open(os.path.join(root, f'data/claims/claims{i}.json'), encoding='utf-8'))
ALIAS = {
 'Andrew': 'Andrew Irvine', 'Irvine': 'Andrew Irvine', 'NAB CEO': 'Andrew Irvine',
 'Ana': 'Ana Marinkovic', 'Anna': 'Ana Marinkovic', 'Putina': 'Ana Marinkovic',
 'Daniela LoCastro': 'Dani LoCastro', 'PW': 'Patrick Wright', 'Patrick': 'Patrick Wright', 'P Wright': 'Patrick Wright',
 'Cath Carver': 'Cathryn Carver', 'Cath': 'Cathryn Carver', 'Peter K': 'Peter Karagounis', 'PK': 'Peter Karagounis', 'Peter': 'Peter Karagounis',
 'Bel': 'Belinda Mamet', 'Bel M': 'Belinda Mamet', 'Belinda M': 'Belinda Mamet', 'Mamet': 'Belinda Mamet', 'Belinda': 'Belinda Mamet',
 'Will': 'Will Costabir', 'Costabir': 'Will Costabir', 'Costaber': 'Will Costabir', 'William Costabir': 'Will Costabir', 'Costabar': 'Will Costabir',
 'Ross': 'Ross McEwan', 'Mr Miller': 'Anthony Miller', 'Chronican': 'Phil Chronican', 'NAB chairman': 'Phil Chronican', 'USyd chancellor / NAB chairman': 'Phil Chronican', 'PC': 'Phil Chronican',
 'Court': 'Sarah Court', 'Nicole Rose PSM': 'Nicole Rose', 'Brian H': 'Brian Hartzer', 'Nash': 'Peter Nash',
 'Carmel': 'Carmel Cauchi', 'Aneka': 'Aneka Manners', 'Chi Le / Linh Chi Le': 'Linh Chi Le', 'Lucia Labella': 'Lucia La Bella',
 'Kerri': 'Kerri Webster', 'Stef': 'Stefan Milosavljevic', 'Stef Milo': 'Stefan Milosavljevic', 'Stefan Milo': 'Stefan Milosavljevic',
 'Sandro': 'Sandro B', 'Shaq': 'Shaq Johnson', 'Brendan': 'Brendan Wreford', 'Dee White': 'Deanna White', 'Zacc': 'Adam Zaccaria',
 'Angie': 'Angie Dickinson', 'Ronald': 'Ronald Purnomo', 'Ronald P': 'Ronald Purnomo', 'Inder': 'Inder Singh', 'Sweth Mehra': 'Sweta',
}
def canon(s):
    base = re.sub(r'\s*\(.*?\)\s*', ' ', s).strip()
    m = re.match(r'(?i)^unnamed|^two |^an? |^the ', base)
    if m: return None, s
    return ALIAS.get(base, base), s
people = collections.defaultdict(list)
for n, c in enumerate(allc):
    c['id'] = n
    c['people'] = []
    for s in c['subjects']:
        k, raw = canon(s)
        if k and k not in c['people']:
            c['people'].append(k); people[k].append(n)
roles = collections.defaultdict(collections.Counter)
for c in allc:
    for s in c['subjects']:
        k, raw = canon(s)
        r = re.findall(r'\((.*?)\)', raw)
        if k and r: roles[k][r[0]] += 1
P = {k: {'n': len(v), 'role': (roles[k].most_common(1)[0][0] if roles[k] else ''), 'ids': v} for k, v in people.items()}
corpus = {p['code']: p for p in json.load(open(os.path.join(root, 'data/corpus.json'), encoding='utf-8'))}
data = {'claims': allc, 'people': P, 'posts': {k: {'date': v['date'], 'type': v['type'], 'url': v['url'], 'n': len(v['slides'])} for k, v in corpus.items()}}
tpl = open(os.path.join(root, 'scripts/template.html'), encoding='utf-8').read()
out = tpl.replace('/*DATA*/null', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
os.makedirs(os.path.join(root, 'site'), exist_ok=True)
open(os.path.join(root, 'site/index.html'), 'w', encoding='utf-8').write(out)
print(len(allc), 'claims', len(P), 'people', sum(1 for v in P.values() if v['n'] >= 3), 'with 3+')
