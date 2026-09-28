"""classify_topic.py — 把问题文本/源文件映射到十二叶知识树（关键词加权计分）。"""
import json, os, re, sys, argparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE = os.path.join(ROOT, "asset", "knowledge_tree.json")

def load():
    return json.load(open(TREE, encoding="utf-8"))["leaves"]

def score(text, leaves):
    t = text.lower(); out = []
    for lf in leaves:
        hit = [k for k in lf.get("keywords", []) if k.lower() in t]
        if hit:
            out.append({"id": lf["id"], "score": len(hit), "keywords": hit[:6],
                        "priority": lf.get("priority", 5)})
    out.sort(key=lambda x: (-x["score"], x["priority"]))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text"); ap.add_argument("--file"); ap.add_argument("--top", type=int,
        default=3)
    ap.add_argument("--json", action="store_true"); a = ap.parse_args()
    text = a.text or ""
    if a.file:
        text += " " + re.sub(r"[^\w:<>_*&]", " ", open(a.file, encoding="utf-8",
            errors="ignore").read())
    if not text.strip():
        print("用法: --text \"...\" 或 --file src.c", file=sys.stderr); return 2
    res = score(text, load())[:a.top]
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json
          else "\n".join(f"{i+1}. {r['id']} score={r['score']} kw={','.join(r['keywords'])}"
                         for i, r in enumerate(res)) or "未命中任何知识叶，请补充问题细节")
    return 0

if __name__ == "__main__":
    sys.exit(main())
