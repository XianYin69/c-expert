"""perf_advice.py — C 性能与缓存局部性静态启发式（分配/遍历/IO/别名/对齐）。"""
import argparse, re, sys

P = [
    (r"for\s*\([^;]*;\s*[^;]*strlen\s*\(", "strlen in loop condition: O(n^2)",
     "hoist len before loop, or use a sentinel-free API passing size [book]"),
    (r"\bmalloc\s*\([^)]*\)\s*;?\s*$", "allocation inside loop body (check context)",
     "hoist/reuse buffer or arena; free once [cse-adjacent]"),
    (r"\bprintf\s*\(", "formatted IO in hot path", "buffer output; write() once per batch"),
    (r"\bfgetc\s*\(|\bgetc\s*\(", "char-by-char IO", "read blocks with fread into buffer"),
    (r"\bqsort\s*\(", "qsort indirect comparator call per element",
     "sort indices, or use qsort_s/GF-merge; measure before replacing"),
    (r"\bstrcpy\s*\(|\bstrcat\s*\(", "unbounded copy: length unknown twice",
     "snprintf/strncpy with explicit size (still check truncation)"),
    (r"struct\s+\w+\s*\{[^}]*\bchar\s+\w+\s*;\s*\bint\b", "struct field order may pad badly",
     "order fields by decreasing alignment; verify with offsetof"),
    (r"\bdouble\s+\w+\s*\[\s*\d{3,}\s*\]", "large array of double traversed",
     "prefer SoA for SIMD; check cache line 64B locality"),
    (r"\bwhile\s*\(\s*\w+\s*->\s*next\s*\)", "pointer-chasing linked traversal",
     "poor prefetch: consider array/CSR layout if read-heavy"),
    (r"\bvolatile\s+\w+\b", "volatile forces reload, blocks optimization",
     "use _Atomic or accessor; volatile is for MMIO/signal only"),
    (r"\bfloat\s+\w+\s*=\s*.*\bdouble\b", "mixed float/double math",
     "pick one width; double promotion in loops costs"),
]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("files", nargs="+"); a = ap.parse_args()
    for f in a.files:
        src = open(f, encoding="utf-8", errors="ignore").read()
        hits = []
        for i, line in enumerate(src.splitlines(), 1):
            s = line.split("//")[0]
            for pat, why, fix in P:
                if re.search(pat, s):
                    hits.append((i, why, fix, s.strip()[:90])); break
        print(f"== {f}: {len(hits)} candidate(s)")
        for ln, why, fix, txt in hits[:25]:
            print(f"  L{ln}: {why} -> {fix}\n      {txt}")
    print("\nnote: heuristics only. Measure first: perf stat -e cache-misses / "
          "valgrind --tool=cachegrind "
          "/ -O2 -Rpass=loop-vectorize. Never claim 'faster' without numbers.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
