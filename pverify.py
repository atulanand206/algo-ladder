"""python3 pverify.py [--fix]
Checks problems/*.csv (columns: topic,plat,pid,name,rating,note) against the real sites and fills name and rating with --fix.
  cf      pid like 1520D       checked against the Codeforces API (name, rating, tags)
  cses    pid like 1068        checked against the CSES problem list
  atcoder pid like abc123_d    page title must contain the name
Rows that do not exist are errors. Run it before every commit that touches problems/."""
import csv,glob,json,os,re,sys,urllib.request,time
here=os.path.dirname(os.path.abspath(__file__));C=os.path.join(here,".cache");os.makedirs(C,exist_ok=True)
FIX="--fix" in sys.argv
def get(u):
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"});return urllib.request.urlopen(r,timeout=25).read().decode("utf8","replace")
def cache(name,fn):
    p=os.path.join(C,name)
    if os.path.exists(p):return json.load(open(p))
    v=fn();json.dump(v,open(p,"w"));return v
def cfdata():
    d=json.loads(get("https://codeforces.com/api/problemset.problems"))["result"]["problems"]
    return {f"{p['contestId']}{p['index']}":dict(name=p["name"],rating=p.get("rating",0),tags=p["tags"]) for p in d}
def csesdata():
    h=get("https://cses.fi/problemset/list/")
    return {m[0]:m[1].replace("&#39;","'").replace("&amp;","&") for m in re.findall(r'/problemset/task/(\d+)/?">([^<]+)</a>',h)}
CF=cache("cf2.json",cfdata);CS=cache("cses.json",csesdata)
ATC=json.load(open(os.path.join(C,"atc.json"))) if os.path.exists(os.path.join(C,"atc.json")) else {}
def atc(pid):
    if pid in ATC:return ATC[pid]
    c=pid.split("_")[0]
    try:
        t=re.search(r"<title>(.*?)</title>",get(f"https://atcoder.jp/contests/{c}/tasks/{pid}"),re.S).group(1).strip()
        m=re.match(r"^[A-Z0-9]+ - (.*?) - ",t);ATC[pid]=m.group(1) if m else t
    except Exception:ATC[pid]=None
    time.sleep(0.3)
    if ATC[pid] is None:return ATC.pop(pid)
    json.dump(ATC,open(os.path.join(C,"atc.json"),"w"));return ATC[pid]
sys.path.insert(0,here)
import tree
ids={n["id"] for n in tree.load()}
errs=[];tot=0;per={}
for f in sorted(glob.glob(os.path.join(here,"problems","*.csv"))):
    rows=list(csv.DictReader(open(f)));out=[]
    for i,r in enumerate(rows,2):
        tot+=1;w=f"{os.path.basename(f)}:{i}"
        t,pl,pid=r["topic"].strip(),r["plat"].strip(),r["pid"].strip()
        if t not in ids:errs.append(f"{w} unknown topic {t}")
        if pl=="cf":
            d=CF.get(pid)
            if not d:errs.append(f"{w} Codeforces has no problem {pid}");out.append(r);continue
            if FIX:r["name"]=d["name"];r["rating"]=str(d["rating"] or "")
            elif r.get("name","").lower()!=d["name"].lower():errs.append(f"{w} {pid} is called '{d['name']}' not '{r.get('name')}'")
        elif pl=="cses":
            n=CS.get(pid)
            if not n:errs.append(f"{w} CSES has no task {pid}");out.append(r);continue
            if FIX:r["name"]=n;r["rating"]=""
            elif r.get("name","").lower()!=n.lower():errs.append(f"{w} CSES {pid} is called '{n}' not '{r.get('name')}'")
        elif pl=="atcoder":
            n=atc(pid)
            if not n:errs.append(f"{w} AtCoder page for {pid} not found");out.append(r);continue
            if FIX:r["name"]=n;r["rating"]=""
            elif r.get("name","").lower()!=n.lower():errs.append(f"{w} AtCoder {pid} is called '{n}' not '{r.get('name')}'")
        else:errs.append(f"{w} platform must be cf, cses or atcoder, got {pl}")
        per[t]=per.get(t,0)+1;out.append(r)
    if FIX:
        w=csv.DictWriter(open(f,"w",newline=""),fieldnames=["topic","plat","pid","name","rating","note"],extrasaction="ignore");w.writeheader();w.writerows(out)
print(tot,"rows,",len(per),"topics covered of",len(ids)-0)
for e in errs:print("ERROR",e)
sys.exit(1 if errs else 0)
