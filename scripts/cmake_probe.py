"""cmake_probe.py — CMake 探针（C 项目）：缺 C_STANDARD、未开 -Wall/-Wextra、缺 sanitizer 选项、glob 源码、缺项目选项。"""
import os, re, sys, argparse

def probe(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for i, l in enumerate(txt.splitlines(), 1):
        if re.search(r"file\s*\(\s*GLOB", l):
            out.append((i, "blocking", "file(GLOB) 收集源码：新增文件不触发重新配置，构建不可复现"))
        if re.search(r"add_(executable|library)\s*\(", l) and "target_compile_options" not in txt:
            out.append((i, "major", "有目标但无 target_compile_options：告警基线未设"))
        if re.search(r"set_target_properties.*(C_STANDARD)", l) and "C_EXTENSIONS" not in txt:
            out.append((i, "minor", "设了 C_STANDARD 未设 C_EXTENSIONS：gnu 扩展漂移未锁"))
        if "CMAKE_C_STANDARD" not in txt and "C_STANDARD" not in txt:
            out.append((1, "blocking", "未声明 C 标准（set(CMAKE_C_STANDARD 11)）：方言随编译器漂移"))
        if "SANITIZER" not in txt.upper() and "fsanitize" not in txt:
            out.append((1, "minor", "无 sanitizer 开关（建议 option(ENABLE_SANITIZERS)）"))
        if re.search(r"link_libraries\s*\(", l) and "target_link_libraries" not in txt:
            out.append((i, "major", "全局 link_libraries 污染所有目标"))
        if re.search(r"\binclude_directories\s*\(", l) and "target_include_directories" not in txt:
            out.append((i, "major", "全局 include_directories：应改 target_include_directories"))
    if not re.search(r"cmake_minimum_required", txt):
        out.append((1, "blocking", "缺 cmake_minimum_required"))
    return sorted(set(out))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("path", nargs="?")
    ap.add_argument("--root", default="."); a = ap.parse_args()
    cands = [a.path] if a.path else []
    if not cands:
        for d, _, fs in os.walk(a.root):
            if "tmp" in d or ".git" in d or "build" in d:
                continue
            cands += [os.path.join(d, f) for f in fs if f == "CMakeLists.txt"]
    if not cands:
        print("[SKIP] 未发现 CMakeLists.txt"); return 0
    n = 0
    for p in cands:
        for ln, sev, msg in probe(p):
            print(f"{p}:{ln} [{sev}] {msg}"); n += 1
    print(f"[cmake_probe] 文件={len(cands)} 命中={n}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
