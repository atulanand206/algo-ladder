"""python3 contest.py <words from the problem statement>   e.g.  python3 contest.py "k-th smallest after updates range sum"
Ranks topics by how well their lesson (the 'think' signals count most) matches the words, and prints the pieces and files to open."""
import sys,json,re,os,glob
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"dist","data")
STOP=set("the a an of to and or in is are for with on at by from that this it as be can you your then each all any".split())
tok=lambda s:[w for w in re.findall(r"[a-z0-9]+",s.lower()) if w not in STOP and len(w)>2]
G={n["id"]:n for n in json.load(open(f"{D}/graph.json"))["graph"]}
def score(L,q):
    s=0
    for sec,w in(("think",3),("idea",1),("cost",1)):
        t=set(tok(L.get(sec,"")))
        s+=w*sum(1 for x in q if x in t)
    return s+4*sum(1 for x in q if x in set(tok(G[L["id"]]["label"])))
def main(q):
    q=tok(" ".join(q));R=[]
    for f in glob.glob(f"{D}/lessons/*.json"):
        L=json.load(open(f));i=L["id"]
        if i in G:R.append((score(L,q),i,L))
    R.sort(key=lambda r:-r[0])
    for s,i,L in R[:8]:
        if s==0:break
        first=next((l[2:] for l in L["think"].split("\n") if l.startswith("- ")),"")
        print(f"{i:14} {G[i]['label'][:34]:34} score {s}\n   signal: {first[:150]}\n   open: dist/data/lessons/{i}.json   pieces: python3 pieces.py {i}")
if __name__=="__main__":
    if len(sys.argv)<2:sys.exit(__doc__)
    main(sys.argv[1:])
