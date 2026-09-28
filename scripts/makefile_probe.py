"""makefile_probe.py — Makefile 探针：配方行空格缩进、缺 .PHONY、缺 -std/-Wall、缺 clean/sanitizer 档。"""
import os, re, sys, argparse
PSEUDO = {".PHONY", "all", "clean", "install", "test", "check",
          "distclean", "lint", "fmt", "help", "run"}

def probe(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    txt = "\n".join(lines); out = []
    chk = lambda hit, sev, msg: hit and out.append((1, sev, msg))
    chk(".PHONY" not in txt, "major", "无 .PHONY：all/clean 遇同名文件即静默不执行")
    chk(not re.search(r"-std=(gnu)?(89|99|11|17|23)", txt), "blocking", "未显式 -std=：方言随编译器漂移")
    chk("-Wall" not in txt, "major", "未开 -Wall（基线 -Wall -Wextra -Werror）")
    chk("-Wextra" not in txt, "minor", "未开 -Wextra：告警长期积压")
    chk("clean:" not in txt, "minor", "无 clean 目标")
    chk("-fsanitize" not in txt, "minor", "无 sanitizer 构建档（asan/ubsan 目标）")
    for i, l in enumerate(lines, 1):
        if re.match(r"^[A-Za-z_.$][\w.$-]*\s*:.*$", l) and not l.startswith("\t"):
            name = l.split(":")[0].strip()
            if name in PSEUDO and ".PHONY" not in txt:
                out.append((i, "major", f"伪目标 {name} 未登记 .PHONY"))
        elif l[:1] == " " and re.match(r"^\s+[-@\w$(]", l) and \
                not re.match(r"^[\w.]+\s*[:+?]?=", l):
            out.append((i, "blocking", "配方行以空格开头：Make 要求制表符，此行永不执行"))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    cands = [a.path] if a.path else []
    for d, _, fs in os.walk(a.root):
        if "tmp" in d or ".git" in d:
            continue
        cands += [os.path.join(d, f) for f in fs if f.lower() in ("makefile", "gnumakefile")]
    if not cands:
        print("[SKIP] 未发现 Makefile")
        return 0
    n = 0
    for p in cands:
        for ln, sev, msg in probe(p):
            print(f"{p}:{ln} [{sev}] {msg}")
            n += 1
    print(f"[makefile_probe] 文件={len(cands)} 命中={n}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
