"""portability_scan.py — 方言与平台可移植性：C89/C99/C11/C23 特性、POSIX/MSVC 专有 API、整数与字节序假设。"""
import re, sys, argparse

FEAT = [("c99", r"//[^\n]*$", "行注释"), ("c99", r"\b(char|int|float)\s*\w+\s*\[\s*\w+\s*\]", "VLA"),
        ("c99", r"\bfor\s*\(\s*(int|size_t|char)\s+\w+", "for 内声明"),
        ("c99", r"\b(long long|snprintf|stdbool|stdint)\b", "C99 专有类型/函数"),
        ("c11", r"\b_Generic\s*\(", "_Generic"), ("c11", r"\b_Static_assert\s*\(", "静态断言"),
        ("c11", r"\b_Atomic\b|\batomic_", "C11 原子"), ("c23", r"\bnullptr\b|#\s*embed\b", "C23 特性")]
PLAT = [("posix", r"\bunistd\.h|\bpthread\.h|\bsys/\w+\.h|\bgettimeofday\b", "POSIX 专有"),
        ("msvc", r"\bwindows\.h|\b_io\.h|\b_snprintf\b", "MSVC 专有"),
        ("libc", r"\bgets\b|\bstrlcpy\b|\bstrlcat\b|\bbzero\b", "非标准 libc 扩展")]
RISK = [("blocking", r"\bsizeof\s*\(\s*long\s*\)", "以 sizeof(long) 假设指针宽度"),
        ("major", r"\bprintf\s*\([^)]*%l[du]", "%ld 打印 size_t（Win64 截断）"),
        ("major", r"\bunsigned\s+\w+\s*-\s*1\b", "无符号回绕作边界"),
        ("major", r"\bhtonl|ntohl\b", "字节序须显式转换"),
        ("minor", r"\bchar\s*\*\s*\w+\s*=\s*\(char\s*\*\)", "char 符号性随平台")]
ORD = {"c89": 0, "c99": 1, "c11": 2, "c23": 3}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src", nargs="+")
    ap.add_argument("--std", default="c11"); a = ap.parse_args()
    lim = ORD.get(a.std.replace("gnu", "c"), 2); n = 0
    for f in a.src:
        for i, l in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            if l.strip().startswith(("*", "/*")):
                continue
            for std, pat, why in FEAT:
                if ORD[std] > lim and re.search(pat, l):
                    print(f"{f}:{i} [std] {std} 特性高于 --std={a.std}：{why}"); n += 1
            for tag, pat, why in PLAT + RISK:
                if re.search(pat, l):
                    print(f"{f}:{i} [{tag}] {why}"); n += 1
    print(f"[portability_scan] 命中={n}（须以目标编译器 -std 实测确证）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
