# The full topic tree: code layers (primitives, utilities) plus every algorithm in catalog.txt.
import os
CATS={"prim":"Primitives","util":"Utilities","ds":"Data structures","sort":"Sorting and searching","tech":"Techniques","graph":"Graphs","dp":"Dynamic programming","math":"Math","geom":"Geometry","str":"Strings","app":"Applied","sys":"Real systems"}
UTILS="""
u-swap|swap(a, b)|0|prim|
u-minmax|min, max, clamp|0|prim|
u-abs|abs and sign|0|prim|
u-mod|mod(a, m) never negative|0|prim|
u-ceildiv|ceilDiv(a, b)|0|prim|
u-mid|mid(lo, hi) no overflow|0|prim|
u-bit|get, set, clear bit|0|prim|
u-lowbit|lowbit(x)|0|prim|
u-idx|idx(r, c), inBounds|0|prim|
u-dirs|dx, dy directions|0|prim|
u-cmp|compare(a, b)|0|prim|
u-in|readInt, fast input|0|prim|
u-out|print array, join|0|prim|
u-fill|fill, copy array|0|prim|
u-edge|addEdge(u, v)|0|prim|
u-sqrt|sqrtFloor(n)|0|prim|
u-digits|digits(n)|0|prim|
u-gcd|gcd(a, b)|1|util|u-mod
u-lcm|lcm(a, b)|1|util|u-gcd
u-powmod|powMod(b, e, m)|1|util|u-mod
u-mulmod|mulMod(a, b, m)|1|util|u-mod
u-isprime|isPrime(n)|1|util|u-sqrt
u-digsum|digitSum(n)|1|util|u-digits
u-popcount|popcount(x)|1|util|u-lowbit,u-bit
u-reverse|reverse(a, i, j)|1|util|u-swap
u-rotate|rotate(a, k)|1|util|u-reverse
u-prefix|buildPrefix(a)|1|util|u-fill
u-rangesum|rangeSum(l, r)|1|util|u-prefix
u-freq|countFreq(a)|1|util|u-fill
u-lower|lowerBound(a, x)|1|util|u-mid,u-cmp
u-upper|upperBound(a, x)|1|util|u-lower
u-first|firstTrue(lo, hi, test)|1|util|u-mid
u-part|partition(a, lo, hi)|1|util|u-swap,u-cmp
u-merge|merge two sorted|1|util|u-cmp
u-sift|siftUp, siftDown|1|util|u-swap,u-cmp
u-find|find with compression|1|util|u-fill
u-sortidx|sortIndices(a)|1|util|u-cmp,u-swap
u-adj|buildAdj(edges)|1|util|u-edge,u-fill
u-nbr|neighbors(r, c)|1|util|u-idx,u-dirs
"""
UDESC={'u-swap': 'Exchange two values using a temporary.', 'u-minmax': 'Pick the smaller or larger, or keep a value inside a range.', 'u-abs': 'Distance from zero, and which side of zero a number is on.', 'u-mod': 'A remainder that stays between 0 and m-1, even for negative numbers.', 'u-ceildiv': 'Divide and round up using only whole numbers.', 'u-mid': 'The middle of two numbers without overflowing.', 'u-bit': 'Read, turn on, or turn off one bit of a number.', 'u-lowbit': 'Isolate the lowest bit that is on.', 'u-idx': 'Turn a row and column into one index, and check you are inside the grid.', 'u-dirs': 'The four (or eight) steps you can take on a grid.', 'u-cmp': 'Say whether one value comes before, after, or equals another.', 'u-in': 'Read many numbers quickly from input.', 'u-out': 'Print a whole array in one fast call.', 'u-fill': 'Set every slot of an array to one value, or copy it.', 'u-edge': 'Record that two nodes are connected.', 'u-sqrt': 'The largest whole number whose square still fits.', 'u-digits': 'Split a number into its digits.', 'u-gcd': 'The largest number dividing both, found by repeated remainders.', 'u-lcm': 'The smallest number both divide, from the gcd.', 'u-powmod': 'Raise to a huge power under a modulus in log steps.', 'u-mulmod': 'Multiply under a modulus without overflow.', 'u-isprime': 'Test one number by trying divisors up to its square root.', 'u-digsum': 'Add up the digits of a number.', 'u-popcount': 'Count how many bits are on.', 'u-reverse': 'Flip a range of an array in place.', 'u-rotate': 'Shift an array around its end using three reversals.', 'u-prefix': 'Running totals, so any range sum becomes a subtraction.', 'u-rangesum': 'The sum of a range from two prefix values.', 'u-freq': 'How many times each value appears.', 'u-lower': 'The first position whose value is not less than x.', 'u-upper': 'The first position whose value is greater than x.', 'u-first': 'The smallest value where a yes or no test turns true.', 'u-part': 'Split an array around a pivot: small on the left, large on the right.', 'u-merge': 'Combine two sorted lists into one sorted list.', 'u-sift': 'Move an item up or down a heap until the order holds.', 'u-find': 'Which group an item is in, flattening the path as you go.', 'u-sortidx': 'Sort positions by their values, leaving the array untouched.', 'u-adj': 'Turn a list of edges into neighbor lists.', 'u-nbr': 'The valid cells next to a cell on a grid.'}
def load():
    nodes=[]
    for l in UTILS.strip().splitlines():
        i,n,c,cat,p=l.split("|");nodes.append(dict(id=i,label=n,col=int(c),cat=cat,pre=[x for x in p.split(",") if x],d=UDESC[i]))
    here=os.path.dirname(os.path.abspath(__file__))
    for l in open(os.path.join(here,"catalog.txt")).read().strip().splitlines():
        i,n,t,cat,p,d=l.split("|");nodes.append(dict(id=i,label=n,col=int(t)+2,cat=cat,pre=[x for x in p.split(",") if x],d=d))
    for l in open(os.path.join(here,"utils_extra.txt")).read().strip().splitlines():
        i,n,c,cat,p,d=l.split("|");nodes.append(dict(id=i,label=n,col=int(c),cat=cat,pre=[x for x in p.split(",") if x],d=d))
    for l in open(os.path.join(here,"systems.txt")).read().strip().splitlines():
        i,n,t,cat,p,d=l.split("|");nodes.append(dict(id=i,label=n,col=int(t)+2,cat=cat,pre=[x for x in p.split(",") if x],d=d))
    by0={n["id"]:n for n in nodes}
    for l in open(os.path.join(here,"utils_links.txt")).read().strip().splitlines():
        a,us=l.split(":");assert a in by0,("links: unknown algorithm",a)
        for u in us.split(","):
            if u not in by0[a]["pre"]: by0[a]["pre"].append(u)
    ids=[n["id"] for n in nodes];assert len(ids)==len(set(ids)),[i for i in ids if ids.count(i)>1]
    by={n["id"]:n for n in nodes};errs=[]
    for n in nodes:
        assert n["cat"] in CATS,n["id"]
        for p in n["pre"]:
            if p not in by: errs.append(("missing",n["id"],p))
            elif by[p]["col"]>n["col"]: errs.append(("tier",n["id"],n["col"]-2,p,by[p]["col"]-2))
    assert not errs,errs
    seen={}
    def vis(x):
        if seen.get(x)==2:return
        assert seen.get(x)!=1,"cycle "+x
        seen[x]=1
        for p in by[x]["pre"]:vis(p)
        seen[x]=2
    for n in nodes:vis(n["id"])
    return nodes
if __name__=="__main__":
    from collections import Counter
    ns=load();print(len(ns),"nodes",sum(len(n["pre"]) for n in ns),"links",sorted(Counter(n["cat"] for n in ns).items()),Counter(n["col"]-2 for n in ns if n["col"]>=2))
