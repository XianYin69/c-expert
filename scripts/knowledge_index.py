"""knowledge_index.py — 取知识叶要点与权威出处锚点（供「知识检索」步）。"""
import json, os, re, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")
KNOW = os.path.join(ROOT, "asset", "knowledge")

def leaf_ids():
    return [l["id"] for l in json.load(open(TREE, encoding="utf-8"))["leaves"]]

def lines(lf):
    p = os.path.join(KNOW, lf + ".md")
    return open(p, encoding="utf-8").read().splitlines() if os.path.exists(p) else []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--leaf"); ap.add_argument("--list", action="store_true")
    ap.add_argument("--full", action="store_true"); a = ap.parse_args()
    ids = leaf_ids()
    if a.list or not a.leaf:
        print("\n".join(ids)); return 0
    if a.leaf not in ids:
        print(f"unknown leaf '{a.leaf}'; choices: {', '.join(ids)}", file=sys.stderr); return 2
    ls = lines(a.leaf)
    pts = [re.sub(r"^[-*]\s*", "", l.strip()) for l in ls if l.strip().startswith(("-", "*"))]
    cites = sorted(set(re.findall(r"\[(cref|iso|google|book|man)\]", "\n".join(ls))))
    print(f"# {a.leaf}\n")
    for x in (pts if a.full else pts[:14]):
        print("- " + x)
    print("\ncitations: " + (", ".join(cites) or "none"))
    return 0

if __name__ == "__main__":
    sys.exit(main())
