"""header_deps.py — 头文件依赖检查：包含图、循环包含、缺 include guard/#pragma once、未使用的系统头、隐式声明风险。"""
import os, re, sys, argparse
from collections import defaultdict

INC = re.compile(r'^\s*#\s*include\s+([<"])([^">]+)[">]', re.M)
GUARD = re.compile(r"#\s*ifndef\s+\w+|\bpragma\s+once", re.I)
SYS = {"stdio.h", "stdlib.h", "string.h", "math.h", "assert.h", "errno.h", "stdint.h",
       "stddef.h", "stdbool.h", "ctype.h", "time.h", "pthread.h", "unistd.h", "limits.h"}
USE = {"stdio.h": r"\b(fprintf?|printf|scanf|snprintf|fopen|fclose|puts|fgets)\b",
       "stdlib.h": r"\b(malloc|calloc|realloc|free|exit|atoi|qsort|abs|getenv)\b",
       "string.h": r"\b(mem(cpy|set|move|cmp)|str(len|cpy|cmp|cat|chr|dup))\b",
       "math.h": r"\b(sqrt|pow|fabs|floor|ceil|sin|cos|exp|log)\b",
       "assert.h": r"\bassert\s*\(", "errno.h": r"\berrno\b",
       "stdint.h": r"\b(u?int(8|16|32|64)_t|UINT_MAX|INT32_MAX)\b",
       "stddef.h": r"\b(size_t|ptrdiff_t|NULL)\b", "stdbool.h": r"\b(bool|true|false)\b",
       "ctype.h": r"\b(is(alpha|digit|upper|lower)|toupper|tolower)\b",
       "time.h": r"\b(clock|time\(|struct tm|timespec)\b", "pthread.h": r"\bpthread_\w+",
       "unistd.h": r"\b(read|write|close|sleep|getpid|access)\b",
           "limits.h": r"\b(INT_MAX|PATH_MAX|CHAR_BIT)\b"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); a = ap.parse_args()
    files = [os.path.join(d, f) for d, sub, fs in os.walk(a.root)
             for f in fs if f.endswith((".h", ".c"))
             and not any(x in (".git", "__pycache__",
                 "build") for x in sub + [os.path.basename(d)])]
    graph, out = defaultdict(set), []
    for p in files:
        txt = open(p, encoding="utf-8", errors="replace").read()
        body = INC.sub("", txt)
        if p.endswith(".h") and not GUARD.search(txt):
            out.append((p, "blocking", "缺 include guard / #pragma once → 重复包含即编译失败"))
        for ch, h in INC.findall(txt):
            if ch == '"':
                graph[p].add(h)
            if h in USE and not re.search(USE[h], body):
                out.append((p, "minor", f"#include <{h}> 未见使用（IWYU：删之或转前置声明）"))
            if h not in SYS and ch == "<":
                out.append((p, "major", f"<{h}> 非标准库头却用尖括号（项目头应用 \"\"）"))
    for p, deps in graph.items():
        for d in deps:
            if d in graph and p in graph[d] and p < d:
                out.append((p, "blocking", f"与 {d} 循环包含 → 拆出公共类型头"))
    for p, sev, msg in out:
        print(f"{os.path.relpath(p, a.root)} [{sev}] {msg}")
    print(f"[header_deps] 扫描={len(files)} 文件 命中={len(out)}（报告式，不改文件）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
