"""advice_compose.py — 组装结构化交付（结论/证据/清单/重构/风险/引用）。"""
import argparse, json, os, sys, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default=""); ap.add_argument("--std", default="c11")
    ap.add_argument("--evidence", default="none", choices=["none", "probe", "sanitizer",
        "compiler"])
    ap.add_argument("--findings", help="JSON 数组: [{level,item,cite,cmd}]"); ap.add_argument("--out")
    a = ap.parse_args()
    items = json.loads(a.findings) if a.findings else []
    order = {"blocking": 0, "major": 1, "minor": 2, "info": 3}
    items.sort(key=lambda x: order.get(x.get("level", "info"), 9))
    out = [f"# c-expert 交付 · {a.topic or '未命名问题'}",
           f"- 标准档: {a.std}  · 取证级别: {a.evidence}  · 时间: {time.strftime('%Y-%m-%d %H:%M')}",
           "", "## 结论摘要"]
    out += [f"- [{i.get('level','info')}] {i.get('item','')}" for i in items[:8]] or ["- （无条目）"]
    out += ["", "## 证据与复现"]
    ev = [f"- {i.get('cmd','')}" for i in items if i.get("cmd")]
    out += ev or ["- evidence=none：未实测，仅知识判断"]
    out += ["", "## 评审清单"]
    ck = [f"- [ ] {i.get('item','')}  <!-- {i.get('cite','')} -->" for i in items]
    out += ck or ["- [ ] review_checklist.py --all"]
    out += ["", "## 重构建议", "- 顺序：正确性 → 所有权与生命周期 → const/restrict 契约 → 性能；最小 diff，一次一判据。"]
    out += ["", "## 风险与边界",
            "- 未取证项须由 -fsanitize=address,undefined 或编译器诊断复现后方可升级为 blocking。",
            "- 结论失效条件：-DNDEBUG、freestanding 无 libc、无堆嵌入式、跨 ABI/平台字长差异。"]
    out += ["", "## 引用"]
    ct = [f"- {i.get('cite','[iso]')}" for i in items if i.get("cite")]
    out += ct or ["- [iso] ISO/IEC 9899"]
    txt = "\n".join(out) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(txt); print(f"[OK] {a.out}")
    else:
        print(txt)
    return 0

if __name__ == "__main__":
    sys.exit(main())
