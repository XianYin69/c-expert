"""review_checklist.py — 按知识叶生成 C 分级评审清单（blocking/major/minor/info）。"""
import json, os, re, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")
CHK = os.path.join(ROOT, "asset", "checklists")
BASE = [
    "blocking | 每个 malloc/calloc 家族分配都有明确所有者与释放路径 | [iso 7.22.3]",
    "blocking | 无越界：数组下标、缓冲区长度、one-past 指针均有用后不解引用论证 | [iso 6.5.6]",
    "blocking | 无 UB：移位宽度、有符号溢出、严格别名、未初始化读、序列点均取证 | [iso 4]",
    "blocking | 返回值全部检查（分配、IO、pthread_create），失败路径资源已清理 | [man]",
    "major | 字符串操作全部有界（snprintf/strlcpy 语义），无 gets/strcpy 裸用 | [google]",
    "major | 只读入参加 const，指针入参注明所有权与 restrict 别名限制 | [book]",
    "major | 跨 TU 声明与定义一致，内部符号 static，无重复定义 | [iso 6.2.2]",
    "minor | 头文件自包含（IWYU）、有 include guard、无循环包含 | [google]",
    "minor | 显式 -std= 与 -Wall -Wextra -Werror 基线，构建可复现 | [book]",
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leaf"); ap.add_argument("--file"); ap.add_argument("--out")
    ap.add_argument("--all", action="store_true"); a = ap.parse_args()
    leaves = [l["id"] for l in json.load(open(TREE, encoding="utf-8"))["leaves"]]
    sel = leaves if a.all else ([a.leaf] if a.leaf else [])
    if not sel:
        print("usage: --leaf <id> | --all | --file <src>", file=sys.stderr); return 2
    out = ["# C review checklist", "", f"scope: {a.file or 'n/a'}", ""]
    for lf in sel:
        p = os.path.join(CHK, lf + ".md")
        if not os.path.exists(p):
            continue
        out.append(f"## {lf}")
        for l in open(p, encoding="utf-8"):
            if l.strip().startswith("-"):
                out.append("- [ ] " + re.sub(r"^-\s*", "", l.strip()))
        out.append("")
    out += ["## baseline"] + ["- [ ] " + b for b in BASE]
    txt = "\n".join(out) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(txt); print(f"[OK] {a.out}")
    else:
        print(txt)
    return 0

if __name__ == "__main__":
    sys.exit(main())
