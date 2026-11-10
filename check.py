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
            for lg in ("java","py","cpp"):
                if not calls(L[lg],method_names(snips[u][lg],lg)): errs.append(f"lesson {k}: the {lg} code never calls {u} ({sorted(method_names(snips[u][lg],lg))})")
        if links and not used: nouse.append(k)
        elif links and not any(u in used for u in links): nolink.append(k)
topics=[n for n in graph if n["col"]>=2]
print(len(les),"of",len(topics),"topics have a lesson")
withlinks=[k for k in les if any(by_id[p]["col"]<2 for p in by_id[k]["pre"])]
print(len(withlinks)-len(nouse)-len(nolink),"of",len(withlinks),"lessons with linked code pieces build on them")
if nouse: print("  not yet using their code pieces (no --uses):",", ".join(sorted(nouse)))
if nolink: print("  --uses names none of the linked pieces:",", ".join(sorted(nolink)))
print(len(graph),"topics,",len(code),"code pieces,",len(pr),"problems")
if errs: print("\n".join(errs));sys.exit(1)
print("ok")
