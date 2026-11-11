"""python3 pieces.py <topic-id>  -- lists the code pieces a topic is built on, with the method names to call."""
import sys,tree
from common import parse_snips,method_names
ns=tree.load();by={n["id"]:n for n in ns};S=parse_snips()
def direct(t):return [p for p in by[t]["pre"] if by[p]["col"]<2]
if __name__=="__main__":
    if len(sys.argv)<2 or sys.argv[1] not in by: sys.exit("usage: python3 pieces.py <topic-id>")
    t=sys.argv[1];ps=direct(t)
    print(f"{t}: {by[t]['label']}  (needs ideas: {[p for p in by[t]['pre'] if by[p]['col']>=2]})")
    if not ps: print("no code pieces are linked to this topic")
    for p in ps:
        print(f"\n[{p}] {by[p]['label']}: {by[p]['d']}")
        for l in ("java","py","cpp","go"):
            if l in S[p]: print(f"  {l}: calls it as {sorted(method_names(S[p][l],l))}")
        print("  python version:\n    "+S[p]["py"].replace("\n","\n    "))
