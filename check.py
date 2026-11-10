"""Checks the built site data. Run after build.py. Fails the CI build on any problem."""
import json,os,sys
D="dist/data";L=lambda k:json.load(open(f"{D}/{k}.json"))
g=L("graph");graph=g["graph"];snips=L("snips");pr=L("problems")["problems"];meta=L("meta")
ids={n["id"] for n in graph};errs=[]
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
topics=[n for n in graph if n["col"]>=2]
print(len(les),"of",len(topics),"topics have a lesson")
print(len(graph),"topics,",len(code),"code pieces,",len(pr),"problems")
if errs: print("\n".join(errs));sys.exit(1)
print("ok")
