import re, collections, sys
t = open(sys.argv[1]).read(); c = collections.Counter()
for m in re.finditer(r"\[(\w+)\]: [^\n]*\n[^\n]*Severity: (\w+)", t): c[(m.group(1), m.group(2))] += 1
print(dict(c))
if len(sys.argv) > 2:
    for m in re.finditer(r"\[(" + sys.argv[2] + r")\]: ([^\n]*)\n([^\n]*)\n((?:    @[^\n]*\n){1,3})", t): print(m.group(1), m.group(2)[:80], "|", m.group(3).strip()[:80]); print(m.group(4))
