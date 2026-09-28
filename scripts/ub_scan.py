"""ub_scan.py — 未定义行为排查：序列点、有符号溢出、移位宽度、空指针解引用、strict aliasing、未初始化、VLA。"""
import re, sys, argparse

RULES = [
    ("blocking", r"\bassert\s*\([^)]*(\+\+|--|=[^=])", "assert 内含副作用：NDEBUG 下行为改变"),
    ("blocking", r"\b\w+\s*<<\s*(3[2-9]|[4-9]\d)", "移位量 ≥32：int 宽度上溢出 → UB"),
    ("blocking", r"\(\s*(?:unsigned|uint32_t|char)\s*\*\s*\)\s*&", "跨类型指针强转：strict aliasing 违规"),
    ("blocking", r"\bfree\s*\([^)]*\)\s*;\s*[^#\n]*\bfree\s*\(", "同一行区段疑似双重释放"),
    ("major", r"\b(int|long|short)\s+\w+\s*=\s*\w+\s*\*\s*\w+\s*;", "有符号乘法无溢出防护（INT_MAX 边界）"),
    ("major", r"\b(char|int)\s*\[\s*\w+\s*\]", "VLA：C11 可选特性，MSVC 不支持且栈溢出风险"),
    ("major", r"\bgets\s*\(|\bsprintf\s*\(|\bstrcpy\s*\(|\bstrcat\s*\(",
        "无界 I/O/拷贝函数（C11 已 Annex K 建议弃用）"),
    ("major", r"\breturn\s+&\s*\w+\s*;|\breturn\s*\(\s*\w+\s*\*\s*\)\s*&", "返回局部对象地址 → 悬垂"),
    ("blocking", r"\[\s*-\d+\s*\]\s*=", "常量负下标写入 → 越界 UB"),
    ("blocking", r"\b\w+\s*\[\s*0\s*\]\s*=\s*'", "疑似向字符串字面量写入 → UB"),
    ("minor", r"^\s*(?:static\s+)?(?:char|int|void|\w+)\s*\*\s*\w+\s*;", "指针声明未初始化：解引用前须赋值或置 NULL"),
    ("major", r"\b\w+\s*\+=\s*\w+\s*\[\s*\w+\s*\]\s*\*\s*\d{4,}", "有符号乘加累积：溢出即 UB"),
    ("minor", r"\bvolatile\b(?!\s+\*|\s+\w+\s*\[)", "volatile 用于同步（应 sig_atomic_t / _Atomic）"),
    ("minor", r"\bstrtok\s*\(", "strtok 非线程安全且改原串"),
    ("minor", r"\b\w+\s*\?\s*\w+\s*:\s*\w+\s*\+\s*\w+", "?: 与 + 混用未加括号，优先级易误读"),
]

def scan(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for i, l in enumerate(txt.splitlines(), 1):
        s = l.strip()
        if s.startswith(("//", "/*", "*")):
            continue
        for sev, pat, why in RULES:
            if re.search(pat, l):
                out.append((i, sev, why, s[:72]))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src", nargs="+")
    ap.add_argument("--top", type=int, default=40); a = ap.parse_args()
    n = 0
    for f in a.src:
        for ln, sev, why, s in scan(f)[: a.top]:
            print(f"{f}:{ln} [{sev}] {why}\n    | {s}"); n += 1
    print(f"[ub_scan] 命中={n}；blocking 项须以 -fsanitize=undefined 实测复现后方可下结论")
    return 0

if __name__ == "__main__":
    sys.exit(main())
