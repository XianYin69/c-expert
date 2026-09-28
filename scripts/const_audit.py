"""const_audit.py — C const 正确性：指针 const 位置语义、只读形参缺 const、字面量绑非 const 指针、restrict 缺失。"""
import re, sys, argparse

POINTER = [("const char *p", "指向常量：可改指针，不可改内容"),
           ("char *const p", "常量指针：可改内容，不可改指针"),
           ("const char *const p", "两者皆常")]
RX = [
    ("blocking", r"\bchar\s*\*\s*\w+\s*=\s*\"", "字符串字面量绑 char*：写之即 UB（应 const char *）"),
    ("blocking", r"\(void\s*\*\)\s*\w+\s*=\s*\"", "经 void* 绕过后写字面量：const 逃逸"),
    ("major", r"\bmemcpy\s*\(\s*\w+\s*,\s*\w+\s*,\s*sizeof\s*\(\s*char\s*\*\s*\)",
        "拷贝指针值而非所指内容（浅拷贝别名）"),
    ("major", r"\b\w+\s*\(\s*char\s*\*\s*\w+\s*\)", "只读入参用 char*：应 const char *（契约不表达只读）"),
    ("minor", r"\b\w+\s*\(\s*\w+\s*\*\s*\w+\s*,\s*\w+\s*\*\s*\w+\s*\)",
        "双指针出/入参未标 restrict：别名限制未声明"),
    ("minor", r"^\s*(?:static\s+)?\w+\s*\*\s*\w+\s*\(.*\w+\s*\*\s*\w+\s*\)\s*\{?\s*$",
        "返回内部指针须注明所有权（借用/转移）"),
]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src", nargs="+")
    ap.add_argument("--api", action="store_true", help="打印 const 位置语义对照"); a = ap.parse_args()
    if a.api:
        for k, v in POINTER:
            print(f"{k:22} -> {v}")
    n = 0
    for f in a.src:
        for i, l in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
            if l.strip().startswith(("//", "*", "/*")):
                continue
            for sev, pat, why in RX:
                if re.search(pat, l):
                    print(f"{f}:{i} [{sev}] {why}\n    | {l.strip()[:72]}"); n += 1
    print(f"[const_audit] 命中={n}（const 是契约：以 -Wcast-qual -Wwrite-strings 复核实测）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
