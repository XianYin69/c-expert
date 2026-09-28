"""memory_audit.py — 动态内存与所有权审计：alloc/free 配对、NULL 检查、双重释放、realloc 泄漏、所有权转移。"""
import re, sys, argparse

ALLOC = re.compile(r"\b(malloc|calloc|realloc|strdup|strndup|aligned_alloc)\s*\(")
FREE = re.compile(r"\bfree\s*\(\s*(&?)\s*(\w+)")
ASSIGN = re.compile(r"(\w+)\s*=\s*(?:\([^)]*\)\s*)?(malloc|calloc|realloc|strdup|strndup)")

def audit(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    fn, depth, owns, out = "<file>", 0, {}, []
    for i, l in enumerate(lines, 1):
        if depth == 0:
            m = re.match(r"^[\w\s\*]+?(\w+)\s*\([^;]*\)\s*\{?", l)
            if m and not l.strip().startswith(("//", "typedef", "return")):
                fn, owns = m.group(1), {}
        depth += l.count("{") - l.count("}")
        for v in ASSIGN.findall(l):
            owns[v[0]] = i
            if not re.search(r"\b" + v[0] + r"\s*==\s*NULL|\b" + v[0] + r"\s*\)", l):
                out.append((i, "major", f"{fn}: {v[0]} 分配自 {v[1]} 未见 NULL 检查（分配失败即 UB）"))
        for amp, v in FREE.findall(l):
            if amp:
                out.append((i, "blocking", f"{fn}: free(&{v}) 释放非堆地址 → UB"))
            elif v not in owns:
                out.append((i, "blocking", f"{fn}: free({v}) 无本函数内分配记录（双重释放/越权释放？）"))
            else:
                owns.pop(v)
        if re.search(r"\breturn\b", l) and owns:
            for v, ln in list(owns.items()):
                if re.search(r"\b" + v + r"\b", l):
                    out.append((ln, "info", f"{fn}: {v} 随 return 移交所有权（须在契约中注明）"))
                    owns.pop(v)
    for v, ln in owns.items():
        out.append((ln, "blocking", f"{fn}: {v} 分配后本函数内无 free 亦无返回 → 泄漏"))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src", nargs="+")
    ap.add_argument("--severity", default="info", choices=["info", "major", "blocking"])
    a = ap.parse_args(); rank = {"info": 0, "major": 1, "blocking": 2}; n = 0
    for f in a.src:
        for ln, sev, msg in sorted(audit(f), key=lambda x: -rank[x[1]]):
            if rank[sev] >= rank[a.severity]:
                print(f"{f}:{ln} [{sev}] {msg}"); n += 1
    print(f"[memory_audit] 文件={len(a.src)} 命中={n}（启发式，须配合 ASan/valgrind 实测确证）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
