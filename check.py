"""Checks the built site data. Run after build.py. Fails the CI build on any problem."""
import json,os,sys
D="dist/data";L=lambda k:json.load(open(f"{D}/{k}.json"))
g=L("graph");graph=g["graph"];snips=L("snips");pr=L("problems")["problems"];meta=L("meta")
ids={n["id"] for n in graph};errs=[];nouse=[];nolink=[]
by_id={n["id"]:n for n in graph}
from common import method_names,calls
for n in graph:
    for p in n["pre"]:
        if p not in ids: errs.append(f"{n['id']}: unknown prerequisite {p}")
    if n["cat"] not in g["cats"]: errs.append(f"{n['id']}: unknown category")
code={n["id"] for n in graph if n["col"]<2}
for c in code:
    if c not in snips: errs.append(f"code piece {c} has no snippet")
    else:
        for l in ("java","py","cpp"):
            if not snips[c].get(l,"").strip(): errs.append(f"snippet {c} missing {l}")
for k in snips:
    if k not in code: errs.append(f"snippet {k} matches no code piece")
for p in pr:
    if p["t"] not in ids: errs.append(f"problem {p['id']}: unknown topic {p['t']}")
    if not meta["showCode"] and (p.get("code") or p.get("file")): errs.append(f"problem {p['id']}: personal code in a public build")
for f in ("index.html",):
    if "__DATA__" in open("dist/"+f).read(): errs.append("template placeholder left in index.html")
les=json.load(open(f"{D}/lessons-index.json"))
for k in les:
    if k not in ids: errs.append(f"lesson {k} matches no topic")
    else:
        L=json.load(open(f"{D}/lessons/{k}.json"))
        for sec in ("idea","build","think","cost","java","py","cpp"):
            if not L.get(sec,"").strip(): errs.append(f"lesson {k} is missing section {sec}")
        # Build-up rule: the lesson must call the code pieces it lists under --uses, not re-implement them.
        used=[u.strip() for u in L.get("uses","").replace(",","\n").split("\n") if u.strip()]
        links=[p for p in by_id[k]["pre"] if by_id[p]["col"]<2]
        for u in used:
            if u not in code: errs.append(f"lesson {k}: --uses lists {u}, which is not a code piece");continue
            for lg in ("java","py","cpp")+(("go",) if L.get("go","").strip() and snips[u].get("go") else ()):
                if not calls(L[lg],method_names(snips[u][lg],lg)): errs.append(f"lesson {k}: the {lg} code never calls {u} ({sorted(method_names(snips[u][lg],lg))})")
        if links and not used: nouse.append(k)
        elif links and not any(u in used for u in links): nolink.append(k)
topics=[n for n in graph if n["col"]>=2]
_gp=sum(1 for c in code if snips.get(c,{}).get("go","").strip());_gl=sum(1 for k in les if json.load(open(f"{D}/lessons/{k}.json")).get("go","").strip())
print("Go:",_gp,"of",len(code),"code pieces,",_gl,"of",len(les),"lessons")
if os.environ.get("STRICT_GO") and (_gp<len(code) or _gl<len(les)):errs.append("Go is incomplete")
print(len(les),"of",len(topics),"topics have a lesson")
withlinks=[k for k in les if any(by_id[p]["col"]<2 for p in by_id[k]["pre"])]
print(len(withlinks)-len(nouse)-len(nolink),"of",len(withlinks),"lessons with linked code pieces build on them")
if nouse: print("  not yet using their code pieces (no --uses):",", ".join(sorted(nouse)))
if nolink: print("  --uses names none of the linked pieces:",", ".join(sorted(nolink)))
print(len(graph),"topics,",len(code),"code pieces,",len(pr),"problems")
if errs: print("\n".join(errs));sys.exit(1)
print("ok")
# problem coverage: every idea topic should have at least 3 problems
import json as _j
_P=_j.load(open(f"{D}/problems.json"))["problems"];_cnt={}
for _p in _P:_cnt[_p["t"]]=_cnt.get(_p["t"],0)+1
_ex=set(l.split()[0] for l in open("problems/none.txt") if l.strip() and not l.startswith("#")) if os.path.exists("problems/none.txt") else set()
_idea=[n["id"] for n in graph if n["col"]>=2 and n["id"] not in _ex]
if _idea:
    print(sum(1 for i in _idea if _cnt.get(i,0)>=3),"of",len(_idea),"topics have 3 or more problems;",sum(1 for i in _idea if not _cnt.get(i)),"have none (excused in problems/none.txt: "+str(len(_ex))+")")

_ord=set(open("ids-order.txt").read().split()) if os.path.exists("ids-order.txt") else set()
_need=[n["id"] for n in graph]+["p_"+p["id"] for p in _P]
_miss=[k for k in _need if k not in _ord]
if _miss:print("ERROR ids-order.txt is missing",len(_miss),"ids; run build.py and commit ids-order.txt");sys.exit(1)
