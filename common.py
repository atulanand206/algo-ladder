"""Shared helpers: parse the code-piece snippets and find the method names each piece defines."""
import glob,os,re
here=os.path.dirname(os.path.abspath(__file__))
def parse_snips():
    out={}
    for f in sorted(glob.glob(os.path.join(here,"snips","*.txt"))):
        for blk in open(f).read().split("### ")[1:]:
            head,_,body=blk.partition("\n")
            parts=re.split(r"^--(java|py|cpp|go)\n",body,flags=re.M)
            out.setdefault(head.strip(),{}).update({parts[i]:parts[i+1].rstrip("\n") for i in range(1,len(parts),2)})   # later files override per language
    return out
_KW={"if","for","while","switch","return","else","catch","sizeof","new"}
def method_names(code,lang):
    """Names of the methods (and classes) a piece of code defines."""
    names=set()
    if lang=="go":
        names|=set(re.findall(r"^func\s+(?:\(\s*\w+\s+\*?\w+\s*\)\s*)?(\w+)\s*[\(\[]",code,flags=re.M))
        names|=set(re.findall(r"^type\s+(\w+)\s+(?:struct|interface)",code,flags=re.M))
        return names
    if lang=="py":
        names|=set(re.findall(r"^\s*def\s+(\w+)\s*\(",code,flags=re.M))
        names|=set(re.findall(r"^\s*class\s+(\w+)",code,flags=re.M))
    else:
        for m in re.finditer(r"^\s*(?:template\s*<[^>]*>\s*)?(?:static\s+|public\s+|private\s+|inline\s+)*[\w:<>\[\],\*&\s]+?[\s\*&](\w+)\s*\([^;{]*\)\s*(?:const\s*)?\{",code,flags=re.M):
            if m.group(1) not in _KW: names.add(m.group(1))
        names|=set(re.findall(r"^\s*(?:static\s+)?(?:class|struct)\s+(\w+)",code,flags=re.M))
        names|=set(re.findall(r"^\s*(?:typedef\s+)?(?:static\s+)?(?:final\s+)?[\w<>]+\s+(INF|LINF)\b",code,flags=re.M))
    return names
def calls(code,names):
    return any(re.search(r"\b"+re.escape(n)+r"\b",code) for n in names)
