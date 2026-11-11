import csv,glob,json,os,re
from content import *
import tree
here=os.path.dirname(os.path.abspath(__file__))
PRIVATE=os.environ.get("PRIVATE")=="1"   # PRIVATE=1 also embeds the author's own solutions (needs the Games clone)
root=os.path.expanduser("~/Documents/Fin/codeforces")
java=os.path.join(root,"Games/java-problems/src/main/java/com/games")
rows=list(csv.DictReader(open(os.path.join(here,"inventory.csv"))))
def clean(src):
    out=[]
    for l in src.splitlines():
        s=l.strip()
        if s.startswith(("package ","import ")): continue
        out.append(l.rstrip())
    t="\n".join(out); t=re.sub(r"\n{3,}","\n\n",t).strip()
    return t[:3800]+("\n// ... trimmed" if len(t)>3800 else "")
TAG2T=[("binary search","binary-search"),("two pointers","twop"),("dsu","dsu"),("shortest paths","dijkstra"),("dfs and similar","dfs"),("trees","tree"),("graphs","graph-rep"),("dp","dp1"),("bitmasks","bits"),("number theory","gcd"),("combinatorics","comb"),("probabilities","prob"),("geometry","geom"),("games","game"),("hashing","hashing"),("divide and conquer","divide"),("strings","str-count"),("sortings","sorting"),("greedy","greedy"),("constructive algorithms","constructive"),("math","parity"),("brute force","recursion"),("data structures","array"),("implementation","array")]
TOPIC_OVERRIDE={"1213A":"parity","1615A":"greedy","1201C":"bs-answer"}
VARTOPIC={"bs-exact":"binary-search","bs-bound":"binary-search","bs-min":"bs-answer","bs-max":"bs-answer","bs-real":"binary-search","bs-peak":"binary-search","g-sort":"greedy","g-interval":"greedy","g-heap":"greedy","g-exchange":"greedy","g-back":"greedy","dp-1d":"dp1","dp-2seq":"lcs","dp-knap":"knapsack","dp-interval":"interval","dp-mask":"bitmask","dp-tree":"treedp","m-parity":"parity","m-gcd":"gcd","m-sieve":"sieve","m-pow":"modpow"}
def topic_of(pid,tags):
    if pid in TOPIC_OVERRIDE: return TOPIC_OVERRIDE[pid]
    for tg,t in TAG2T:
        if tg in tags: return t
    return "array"
probs={};unmatched=0
for r in rows:
    if not r["problem_id"]: unmatched+=1; continue
    pid=r["problem_id"]
    if pid in probs: continue
    tags=[t for t in r["tags"].split(";") if t]
    cid=OVERRIDE.get(pid)
    if not cid:
        for tag,c in TAGMAP:
            if tag in tags: cid=c;break
    cid=cid or "ds"
    code=clean(open(os.path.join(java,r["file"])).read()) if PRIVATE else ""
    probs[pid]=dict(id=pid,name=r["name"],rating=int(r["rating"]) if r["rating"] else 0,tags=tags,c=cid,t=topic_of(pid,tags),code=code,amb=r["match"]=="ambiguous",src="repo",file=r["file"] if PRIVATE else "")
for pid,e in EXPLAIN.items():
    if pid not in probs:
        probs[pid]=dict(id=pid,name=e["title"],rating=e["rating"],tags=[],c=OVERRIDE[pid],code="",t=TOPIC_OVERRIDE[pid],amb=False,src="ladder",file="")
# Extra problems from problems/*.csv (verified by pverify.py): one row per topic, several platforms
def _plat_url(pl,pid):
    if pl=="cf":
        m=re.match(r"^(\d+)([A-Z]\d?)$",pid);return f"https://codeforces.com/problemset/problem/{m.group(1)}/{m.group(2)}"
    if pl=="cses":return f"https://cses.fi/problemset/task/{pid}"
    return f"https://atcoder.jp/contests/{pid.split('_')[0]}/tasks/{pid}"
_PN={"cf":"Codeforces","cses":"CSES","atcoder":"AtCoder"}
_cf={}
try:_cf=json.load(open(os.path.join(here,".cache","cf2.json")))
except Exception:pass
for _f in sorted(glob.glob(os.path.join(here,"problems","*.csv"))):
    for r in csv.DictReader(open(_f)):
        pl,pid,t=r["plat"].strip(),r["pid"].strip(),r["topic"].strip()
        key=pid if pl=="cf" else pl+":"+pid
        if key in probs and probs[key]["t"]!=t:key=key+"@"+t
        if key in probs:
            if r.get("note") and not probs[key].get("note"):probs[key]["note"]=r["note"]
            continue
        rating=int(r["rating"]) if r.get("rating") else 0
        probs[key]=dict(id=key,pid=pid,name=r["name"],rating=rating,tags=(_cf.get(pid,{}).get("tags",[]) if pl=="cf" else []),c="",t=t,code="",amb=False,src="catalog",file="",o=sum(1 for q in probs.values() if q["t"]==t and q.get("src")=="catalog"),plat=_PN[pl],url=_plat_url(pl,pid),note=r.get("note",""))
variants=[dict(v,topic=VARTOPIC[v['id']],alt=ALT.get(v['id'],{})) for c in CONCEPTS for v in c['variants']]
import tree as _t
_ids={n['id'] for n in _t.load()}
for _k,_v in list(VARTOPIC.items())+list(TOPIC_OVERRIDE.items())+[(a,c) for a,c in TAG2T]: assert (_v in _ids),(_k,_v)
_full=dict(variants=variants,concepts=CONCEPTS,problems=sorted(probs.values(),key=lambda p:(p["rating"],p["name"])),explain={k:dict(e,alt=EXALT.get(k,{})) for k,e in EXPLAIN.items()},graph=tree.load(),cats=tree.CATS,unmatched=unmatched,showCode=True)
import os,shutil
shutil.rmtree("dist",ignore_errors=True);os.makedirs("dist/data")
def put(k,v):open(f"dist/data/{k}.json","w").write(json.dumps(v,ensure_ascii=False,separators=(",",":")))
put("meta",dict(showCode=PRIVATE))
put("graph",dict(graph=_full["graph"],cats=_full["cats"]))
put("concepts",dict(variants=_full["variants"],concepts=_full["concepts"]))
_none={}
if os.path.exists(os.path.join(here,"problems","none.txt")):
    for _l in open(os.path.join(here,"problems","none.txt")):
        if _l.strip() and not _l.startswith("#"):
            _a,_,_b=_l.strip().partition(" ");_none[_a]=_b.strip().rstrip(".")
put("problems",dict(problems=_full["problems"],unmatched=_full["unmatched"],none=_none))
put("explain",dict(explain=_full["explain"]))
# Append-only id order: progress codes index into this list, so existing ids must never move. Commit ids-order.txt.
_op=os.path.join(here,"ids-order.txt")
_order=[l.strip() for l in open(_op)] if os.path.exists(_op) else []
_seen=set(_order)
for _k in sorted([n["id"] for n in _full["graph"]]+["p_"+p["id"] for p in _full["problems"]]):
    if _k not in _seen:_order.append(_k);_seen.add(_k)
open(_op,"w").write("\n".join(_order)+"\n")
put("order",_order)
import glob
def parse_snips():
    out={}
    for f in sorted(glob.glob(os.path.join(here,"snips","*.txt"))):
        for blk in open(f).read().split("### ")[1:]:
            head,_,body=blk.partition("\n")
            parts=re.split(r"^--(java|py|cpp|go)\n",body,flags=re.M)
            out.setdefault(head.strip(),{}).update({parts[i]:parts[i+1].rstrip("\n") for i in range(1,len(parts),2)})   # later files override per language
    return out
put("snips",parse_snips())
# Lessons: lessons/*.txt blocks "### id" with sections --idea --build --think --cost --java --py --cpp.
# One small JSON file per topic, loaded only when a topic is opened; lessons-index.json lists which topics have one.
SECS=("idea","build","think","cost","uses","java","py","cpp","go")
def parse_lessons():
    out={}
    for f in sorted(glob.glob(os.path.join(here,"lessons","*.txt"))):
        for blk in open(f).read().split("### ")[1:]:
            head,_,body=blk.partition("\n")
            parts=re.split(r"^--("+"|".join(SECS)+r")\n",body,flags=re.M)
            out[head.strip()]={parts[i]:parts[i+1].strip("\n") for i in range(1,len(parts),2)}
    return out
LES=parse_lessons()
os.makedirs("dist/data/lessons",exist_ok=True)
for k,v in LES.items(): open(f"dist/data/lessons/{k}.json","w").write(json.dumps(dict(id=k,**v),ensure_ascii=False,separators=(",",":")))
put("lessons-index",sorted(LES))
# Small search index for "find the technique": the signal line, first idea sentence and cost per lesson
def _first(t,pre=""):
    for l in t.split("\n"):
        l=l.strip()
        if l.startswith("- "):return l[2:]
    return t.strip().split("\n")[0] if t.strip() else ""
_refs={}
_rp=os.path.join(here,"refs","refs.csv")
if os.path.exists(_rp):
    for _r in csv.DictReader(open(_rp)):_refs.setdefault(_r["topic"].strip(),[]).append([_r["site"].strip(),_r["url"].strip(),_r["title"].strip()])
put("refs",_refs)
put("signals",{k:[_first(v.get("think","")) [:260],(v.get("idea","").split("\n")[0])[:200]] for k,v in LES.items()})
import shutil
if os.path.isdir(os.path.join(here,"static")):
    for _f in os.listdir(os.path.join(here,"static")):shutil.copy(os.path.join(here,"static",_f),"dist/"+_f)
open("dist/index.html","w").write(open("app.html").read())
from collections import Counter
from collections import Counter as C2
print(C2(p["t"] for p in probs.values()).most_common(8))
print(len(probs),"problems;",Counter(p["c"] for p in probs.values()),"unmatched",unmatched)
